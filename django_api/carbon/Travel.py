import math
import os
import json


class Travel:
    FACTORS_DIR = os.path.join(os.path.dirname(__file__), 'factors')

    # Transport modes
    MODE_PLANE = 'plane'
    MODE_CAR = 'car'
    MODE_CAB = 'cab'
    MODE_BUS = 'bus'
    MODE_TRAIN = 'train'
    MODE_TRAM = 'tram'
    MODE_RER = 'rer'
    MODE_SUBWAY = 'subway'
    MODE_FERRY = 'ferry'

    # Distance correction factors per transport mode
    TRANSPORTS_CORRECTION_FACTORS = {
        'plane': lambda d: d * 1.1,
        'car': lambda d: d,
        'cab': lambda d: d,
        'bus': lambda d: d * 1.05,
        'train': lambda d: d * 1.02,
        'tram': lambda d: d,
        'rer': lambda d: d,
        'subway': lambda d: d,
        'ferry': lambda d: d * 1.2,
    }

    TRANSPORTS_FACTORS = None  # Transport emissions factors data
    VEHICLES_FACTORS = None    # Vehicle emissions factors data

    @classmethod
    def _factors(cls):
        # Lazy-load emissions factors JSON
        if cls.VEHICLES_FACTORS is None or cls.TRANSPORTS_FACTORS is None:
            vehicles_path = os.path.join(cls.FACTORS_DIR, 'vehiclesFactors.json')
            transports_path = os.path.join(cls.FACTORS_DIR, 'transportsFactors.json')

            with open(vehicles_path, encoding='utf-8') as f:
                cls.VEHICLES_FACTORS = json.load(f)

            with open(transports_path, encoding='utf-8') as f:
                cls.TRANSPORTS_FACTORS = json.load(f)

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

    @classmethod
    def correct_distance(cls, transport, distance, carpooling, is_round_trip):
        # Transports distance correction factors
        key = transport if transport in cls.TRANSPORTS_CORRECTION_FACTORS else None
        if key:
            distance = cls.TRANSPORTS_CORRECTION_FACTORS[key](distance)

        # Adjust for carpooling
        if transport == cls.MODE_CAB:
            distance = distance * (1 + 1 / max(1, carpooling))
        elif transport == cls.MODE_CAR:
            distance = distance / max(1, carpooling)

        # Double distance if round trip
        if is_round_trip:
            distance = 2 * distance

        return distance

    @classmethod
    def travel_scope(cls, departure_country, destination_country):
        # Travel scope: National (NA), Mixed (MX), International (IN)
        if not departure_country or not destination_country:
            return None
        if departure_country == 'FR' and destination_country == 'FR':
            return 'NA'
        elif departure_country == 'FR' or destination_country == 'FR':
            return 'MX'
        else:
            return 'IN'

    @classmethod
    def get_mode(cls, transport, distance, travel_scope):
        # Transport mode subtype
        if transport == cls.MODE_PLANE:
            if distance < 1000:
                mode = ('plane', 'shorthaul.contrails')
            elif distance < 3501:
                mode = ('plane', 'mediumhaul.contrails')
            else:
                mode = ('plane', 'longhaul.contrails')

        elif transport in (cls.MODE_CAR, cls.MODE_CAB):
            mode = ('car', 'unknown.engine')

        elif transport == cls.MODE_BUS:
            mode = ('bus', 'bus.intercity')

        elif transport == cls.MODE_TRAIN:
            if travel_scope == 'NA':
                mode = ('railway', 'train.shortdistance' if distance < 200 else 'train.longdistance')
            elif travel_scope == 'MX':
                mode = ('railway', 'train.mixed')
            else:
                mode = ('railway', 'train.international')

        elif transport == cls.MODE_TRAM:
            mode = ('railway', 'tram.bigcity')
        elif transport == cls.MODE_RER:
            mode = ('railway', 'rer')
        elif transport == cls.MODE_SUBWAY:
            mode = ('railway', 'subway')
        elif transport == cls.MODE_FERRY:
            mode = ('boat', 'ferry')
        else:
            mode = (None, None)

        return mode

    @classmethod
    def get_factor(cls, transport, mode, year):
        # Get emission factor
        if mode[0] is None or mode[1] is None:
            return None

        factors = cls.VEHICLES_FACTORS if transport in (cls.MODE_CAR, cls.MODE_CAB) else cls.TRANSPORTS_FACTORS
        factor_entry = factors.get(mode[0], {}).get(mode[1])
        if not factor_entry:
            return None

        decomposition = factor_entry.get("decomposition", {})
        # Return factor for year or fallback to latest
        return decomposition.get(year) or decomposition.get(next(iter(decomposition), None))

    @classmethod
    def carbon_footprint(cls, transport, 
                         departure_country, destination_country,
                         departure_lat, departure_long, 
                         destination_lat, destination_long,
                         carpooling, is_round_trip,
                         year):
        cls._factors()  # Load factors

        # Calculate geographic distance
        distance = cls.geodesic_distance(departure_lat, departure_long, destination_lat, destination_long)
        # Apply corrections
        corrected_distance = cls.correct_distance(transport, distance, carpooling, is_round_trip)

        # Travel scope and mode
        scope = cls.travel_scope(departure_country, destination_country)
        mode = cls.get_mode(transport, corrected_distance, scope)

        # Get emission factor
        factor = cls.get_factor(transport, mode, year)
        if factor is None:
            return None
        factor_value = factor['total']['total']

        # Compute carbon footprint (kg CO2)
        carbon_footprint_kg = corrected_distance * factor_value
        return carbon_footprint_kg