import axios from 'axios';

const API_URL = process.env.VUE_APP_SERVER;

/**
 * Auth service for login and token refresh
 */
const auth = {
  async login(credentials: any): Promise<any> {
    const response = await axios.post<any>(
      `${API_URL}/auth/jwt/create`,
      credentials
    );
    return response.data;
  },

  async refresh(refreshToken: any): Promise<any> {
    const response = await axios.post<any>(
      `${API_URL}/auth/jwt/refresh`,
      { refresh: refreshToken }
    );
    return response.data;
  },
};

/**
 * Carbon footprint computing service
 */
const carbon = {
  async getCarbonFootprint(payload: any, accessToken: any): Promise<any> {
    try {
      const response = await axios.post(
        `${API_URL}/api/carbon/`,
        payload,
        {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'application/json',
          },
        }
      );
      return response.data;
    } catch (error: any) {
      if (error.response) {
        throw new Error(`API Error: ${error.response.status} - ${error.response.data}`);
      } else {
        throw new Error(`Network Error: ${error.message}`);
      }
    }
  },
};

/**
 * Employees data fetching service
 */
const employees = {
  async fetchEmployees(token: any): Promise<any> {
    const response = await axios.get(
      `${API_URL}/api/employees`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  },
  async modifyEmployee(token: any, employeeData: any): Promise<any> {
    const response = await axios.put(
      `${API_URL}/api/employees/`,
      employeeData,
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

/**
 * Status data fetching service
 */
const status = {
  async fetchStatus(token: any): Promise<any> {
    const response = await axios.get(
      `${API_URL}/api/status`,
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

/**
 * Users data fetching service
 */
const users = {
  async fetchUsers(token: any): Promise<any> {
    const response = await axios.get(
      `${API_URL}/api/users`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  },
  async deleteUser(token: any, userData: any): Promise<void> {
    const response = await axios.delete(
      `${API_URL}/api/users/`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        data: userData,
      }
    );
    return response.data;
  },
  async createUser(token: any, user: any): Promise<any> {
    const response = await axios.post(
      `${API_URL}/api/users/`,
      user,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  },
  async modifyUser(token: any, userData: any): Promise<any> {
    const response = await axios.put(
      `${API_URL}/api/users/`,
      userData,
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

/**
 * Groups data fetching service
 */
const groups = {
  async fetchGroups(token: any): Promise<any> {
    const response = await axios.get(
      `${API_URL}/api/groups`,
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

/**
 * Transports data fetching service
 */
const transports = {
  async fetchTransports(token: any): Promise<any> {
    const response = await axios.get(
      `${API_URL}/api/transports`,
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

/**
 * Trips service with CRUD methods
 */
const trips = {
  async fetchTrips(token: any): Promise<any> {
    const response = await axios.get(
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

  async createTrip(token: any, tripData: any): Promise<any> {
    const response = await axios.post(
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

  async deleteTrip(token: any, tripData: any): Promise<void> {
    const response = await axios.delete(
      `${API_URL}/api/trips/`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        data: tripData,
      }
    );
    return response.data;
  },

  async alterTrip(token: any, tripData: any): Promise<any> {
    const response = await axios.put(
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

/**
 * Missions service with fetch and create
 */
const missions = {
  async fetchMissions(token: any): Promise<any> {
    const response = await axios.get(
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

  async createMission(token: any, mission: any): Promise<any> {
    const response = await axios.post(
      `${API_URL}/api/missions/`,
      mission,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
      }
    );
    return response.data;
  },

  async deleteMission(token: any, mission: any): Promise<void> {
    const response = await axios.delete(
      `${API_URL}/api/missions/`,
      {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-Type': 'application/json',
        },
        data: mission,
      }
    );
    return response.data;
  },

  async alterMission(token: any, mission: any): Promise<any> {
    const response = await axios.put(
      `${API_URL}/api/missions/`,
      mission,
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

/**
 * Cities fetching service using GeoNames API
 */
const cities = {
  async fetchCities(cityName: string) {
    const username = 'lipncarbonapi';
    const url = `http://api.geonames.org/searchJSON?q=${encodeURIComponent(cityName)}&username=${username}`;
    try {
      const response = await axios.get(url);
      const data = response.data;
      if (data.geonames && data.geonames.length > 0) {
        return data.geonames;
      } else {
        throw new Error("No results found");
      }
    } catch (error) {
      console.error('GeoNames API error:', error);
      throw error;
    }
  },
};

export default {
  auth,
  carbon,
  employees,
  status,
  users,
  groups,
  transports,
  trips,
  missions,
  cities,
};