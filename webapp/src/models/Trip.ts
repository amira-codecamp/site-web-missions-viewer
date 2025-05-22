
import { Transport } from '@/models/Transport'
import { EmployeeWithStatus, Employee } from '@/models/Employee'

export interface Mission {
    mission_num: number,
    start_date: string;
    end_date: string;
    mission_desc: string;
}
  
export interface Trip {
    trip_id: number;
    departure_city: string;
    departure_country: string;
    destination_city: string;
    destination_country: string;
    is_round_trip: boolean;
    carpooling: number;
    carbon_footprint: number;
    transport: Transport;
    mission: Mission;
    employee: EmployeeWithStatus;
}
  
export interface TripCreate {
    departure_city: string;
    departure_country: string;
    destination_city: string;
    destination_country: string;
    is_round_trip: boolean;
    carpooling: number;
    carbon_footprint: number;
    transport_name: string;
    mission_num: string;
    employee: Employee;
}