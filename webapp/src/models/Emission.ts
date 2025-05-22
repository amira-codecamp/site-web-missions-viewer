
export interface TravelEmission {
    transport: string;
    departure_country: string;
    destination_country: string;
    departure_lat: number;
    departure_long: number;
    destination_lat: number;
    destination_long: number;
    carpooling: number;
    year: string;
    is_round_trip: boolean;
}