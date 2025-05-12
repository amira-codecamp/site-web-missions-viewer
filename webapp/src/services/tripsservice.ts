
import axios from 'axios';

const API_URL = process.env.VUE_APP_SERVER;


export interface Transport {
  transport_name: string;
}

export interface Mission {
  start_date: string;
  end_date: string;
  mission_desc: string;
}

export interface Status {
  status_name: string;
}

export interface Employee {
  first_name: string;
  last_name: string;
  email: string;
  status: Status;
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
  employee: Employee;
}


const trips = {
  async fetchTrips(token: string): Promise<Trip[]> {
    const response = await axios.get<Trip[]>(
      `${API_URL}/api/trips`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      }
    );
    return response.data;
  },
};

export default trips;