
import axios from 'axios';
import { Trip, TripCreate, Mission } from '@/models/Trip';

const API_URL = process.env.VUE_APP_SERVER;


const trips = {
  async fetchTrips(token: string): Promise<Trip[]> {
    const response = await axios.get<Trip[]>(
      `${API_URL}/api/trips`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  },
  async createTrip(token: string, tripData: TripCreate): Promise<Trip> {
    const response = await axios.post<Trip>(
      `${API_URL}/api/trips/`,
      tripData,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  },
};


const missions = {
  async fetchMissions(token: string): Promise<Mission[]> {
    const response = await axios.get<Mission[]>(
      `${API_URL}/api/missions`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  },
};

export default { trips, missions };