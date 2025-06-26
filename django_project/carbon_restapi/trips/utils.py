import math
import os
import json
from typing import Optional, Tuple, Dict, Callable, Any
from dataclasses import dataclass, field
import requests
from dotenv import load_dotenv

load_dotenv()

# Transport modes
MODE_PLANE = 'PLANE'
MODE_CAR = 'CAR'
MODE_CAB = 'CAB'
MODE_BUS = 'BUS'
MODE_TRAIN = 'TRAIN'
MODE_TRAM = 'TRAM'
MODE_RER = 'RER'
MODE_SUBWAY = 'SUBWAY'
MODE_FERRY = 'FERRY'


@dataclass
class EmissionFactors:
    """
    Load emission factors from JSON files for vehicles and transports.
    """
    vehicles_factors: Dict[str, Any] = field(default_factory=dict)
    transports_factors: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def load_from_dir(cls) -> 'EmissionFactors':
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            factors_dir = os.path.join(current_dir, 'factors')
            with open(os.path.join(factors_dir, 'vehicles.json'), encoding='utf-8') as f:
                vehicles = json.load(f)
            with open(os.path.join(factors_dir, 'transports.json'), encoding='utf-8') as f:
                transports = json.load(f)
            return cls(vehicles_factors=vehicles, transports_factors=transports)
        except (IOError, json.JSONDecodeError) as e:
            raise RuntimeError(f"Error loading emission factors: {e}")


class TripUtils:
    """
    Utility to compute carbon footprint of a trip instance.
    """

    # Transport-specific correction factors
    TRANSPORT_CORRECTIONS: Dict[str, Callable[[float], float]] = {
        MODE_PLANE: lambda d: d + 95,
        MODE_CAR: lambda d: 1.2 * d,
        MODE_CAB: lambda d: 1.3 * d,
        MODE_BUS: lambda d: 1.3 * d,
        MODE_TRAIN: lambda d: 1.5 * d,
        MODE_TRAM: lambda d: 1.5 * d,
        MODE_RER: lambda d: 1.2 * d,
        MODE_SUBWAY: lambda d: 1.7 * d,
        MODE_FERRY: lambda d: 1.0 * d,
    }

    def __init__(self):
        self._emission_factors: Optional[EmissionFactors] = None
        self.factors_dir = None
        self.geonames_username = os.getenv('GEONAMES_USERNAME')

    @property
    def emission_factors(self) -> EmissionFactors:
        """
        Lazily load emission factors once.
        """
        if self._emission_factors is None:
            self._emission_factors = EmissionFactors.load_from_dir()
        return self._emission_factors

    @staticmethod
    def geodesic_distance(lat1, lon1, lat2, lon2):
        # Calculate distance between two geo points (in km)
        if lat1 == lat2 and lon1 == lon2:
            return 0.0
        radlat1 = math.radians(lat1)
        radlat2 = math.radians(lat2)
        theta = lon1 - lon2
        radtheta = math.radians(theta)
        dist = (math.sin(radlat1) * math.sin(radlat2) +
                math.cos(radlat1) * math.cos(radlat2) * math.cos(radtheta))
        dist = min(1, dist)
        dist = math.acos(dist)
        dist = math.degrees(dist)
        dist = dist * 60 * 1.1515  # miles
        dist = dist * 1.609344     # convert miles to km
        return dist

    def correct_distance(self, transport: str, distance: float, carpooling: int, is_round_trip: bool) -> float:
        """
        Adjust distance based on transport type, carpooling, and round trip.
        """
        correction_func = self.TRANSPORT_CORRECTIONS.get(transport, lambda d: d)
        corrected = correction_func(distance)

        if transport == MODE_CAB:
            # Cab emissions increased by other passengers
            corrected *= (1 + 1 / carpooling)
        elif transport == MODE_CAR:
            # Car emissions shared among passengers
            corrected /= carpooling

        if is_round_trip:
            corrected *= 2

        return corrected

    @staticmethod
    def travel_scope(dep_country: Optional[str], dest_country: Optional[str]) -> Optional[str]:
        """
        Classify trip as national (NA), mixed (MX), or international (IN).
        """
        if not dep_country or not dest_country:
            return None
        if dep_country == 'FR' and dest_country == 'FR':
            return 'NA'
        if dep_country == 'FR' or dest_country == 'FR':
            return 'MX'
        return 'IN'

    def get_mode(self, transport: str, distance: float, scope: Optional[str]) -> Tuple[Optional[str], Optional[str]]:
        """
        Determine emission factor category and subcategory based on transport and distance.
        """
        t = transport.upper()
        if t == MODE_PLANE:
            if distance < 1000:
                return 'plane', 'shorthaul.contrails'
            if distance < 3501:
                return 'plane', 'mediumhaul.contrails'
            return 'plane', 'longhaul.contrails'

        if t in (MODE_CAR, MODE_CAB):
            return 'car', 'unknown.engine'
        if t == MODE_BUS:
            return 'bus', 'bus.intercity'
        if t == MODE_TRAIN:
            if scope == 'NA':
                return 'railway', 'train.shortdistance' if distance < 200 else 'train.longdistance'
            if scope == 'MX':
                return 'railway', 'train.mixed'
            return 'railway', 'train.international'
        if t == MODE_TRAM:
            return 'railway', 'tram.bigcity'
        if t == MODE_RER:
            return 'railway', 'rer'
        if t == MODE_SUBWAY:
            return 'railway', 'subway'
        if t == MODE_FERRY:
            return 'boat', 'ferry'
        return None, None

    def get_factor(self, transport: str, mode: Tuple[Optional[str], Optional[str]], year: str) -> Optional[Dict[str, Any]]:
        """
        Get emission factor for the transport, mode, and year.
        """
        category, subcategory = mode
        if category is None or subcategory is None:
            return None

        factors_source = (self.emission_factors.vehicles_factors
                          if transport in (MODE_CAR, MODE_CAB)
                          else self.emission_factors.transports_factors)

        factor_entry = factors_source.get(category, {}).get(subcategory)
        if not factor_entry:
            return None

        decomposition = factor_entry.get('decomposition', {})
        # Prefer requested year or fallback to earliest available year
        return decomposition.get(year) or decomposition.get(next(iter(decomposition), None))

    def carbon_footprint(
        self,
        transport: str,
        dep_country: Optional[str],
        dest_country: Optional[str],
        dep_lat: float,
        dep_lon: float,
        dest_lat: float,
        dest_lon: float,
        carpooling: int,
        is_round_trip: bool,
        year: str
    ) -> Optional[float]:
        """
        Calculate carbon footprint (kg CO2e).
        """
        distance = self.geodesic_distance(dep_lat, dep_lon, dest_lat, dest_lon)
        corrected_distance = self.correct_distance(transport, distance, carpooling, is_round_trip)
        scope = self.travel_scope(dep_country, dest_country)
        mode = self.get_mode(transport, corrected_distance, scope)
        factor = self.get_factor(transport, mode, year)

        if factor is None:
            return None

        factor_value = factor.get('total', {}).get('total')
        if factor_value is None:
            return None

        return corrected_distance * factor_value

    # def get_lat_long(self, city: str, country: str) -> Optional[Tuple[float, float]]:
    #     """
    #     Get latitude and longitude from GeoNames API for a city-country.
    #     """
    #     url = 'http://api.geonames.org/searchJSON'
    #     params = {
    #         'q': city,
    #         'country': country,
    #         'maxRows': 1,
    #         'username': self.geonames_username,
    #         'featureClass': 'P'  # Only populated places
    #     }
    #     try:
    #         resp = requests.get(url, params=params, timeout=5)
    #         resp.raise_for_status()
    #         data = resp.json()
    #         if data.get('totalResultsCount', 0) > 0:
    #             geoname = data['geonames'][0]
    #             return float(geoname['lat']), float(geoname['lng'])
    #     except requests.RequestException:
    #         pass
    #     return None

    def get_lat_long(self, city: str, country: str) -> Optional[Tuple[float, float]]:
        """
        Get latitude and longitude from Photon API for a city-country.
        """
        query = f"{city}, {country}"
        url = f"https://photon.komoot.io/api/?q={query}&limit=1"
        headers = {
            "User-Agent": "YourAppName/1.0 (your.email@example.com)"
        }

        try:
            resp = requests.get(url, headers=headers, timeout=5)
            resp.raise_for_status()
            data = resp.json()
            features = data.get("features", [])
            if features:
                coords = features[0]["geometry"]["coordinates"]
                return coords[1], coords[0]  # (lat, lon)
        except requests.RequestException as e:
            print(f"[Photon] Erreur de requête : {e}")
        except Exception as e:
            print(f"[Photon] Erreur inattendue : {e}")
        return None

    def get_mission_year(self, trip) -> Optional[str]:
        """
        Extract mission start year from trip object.
        """
        start_date = getattr(getattr(trip, 'mission', None), 'start_date', None)
        if start_date:
            return str(start_date.year)
        return None

    def compute_footprint(self, trip) -> Optional[float]:
        """
        Compute carbon footprint for a Trip instance.
        """
        dep_coords = self.get_lat_long(trip.departure_city, trip.departure_country)

        dest_coords = self.get_lat_long(trip.destination_city, trip.destination_country)

        year = self.get_mission_year(trip)

        carbon = self.carbon_footprint(
            transport=trip.transport.transport_name,
            dep_country=trip.departure_country,
            dest_country=trip.destination_country,
            dep_lat=dep_coords[0],
            dep_lon=dep_coords[1],
            dest_lat=dest_coords[0],
            dest_lon=dest_coords[1],
            carpooling=trip.carpooling,
            is_round_trip=trip.is_round_trip,
            year=year
        )

        return carbon