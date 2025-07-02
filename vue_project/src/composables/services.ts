import axios from "axios";

const API_URL = process.env.VUE_APP_SERVER_URL;
const GEONAMES_USERNAME = process.env.VUE_APP_GEONAMES_USERNAME;

const authHeader = (token: string) => ({
  headers: { Authorization: `Bearer ${token}` },
});

/** JWT */
const token = {
  create: async (credentials: { login: string; password: string }) => {
    return (await axios.post(`${API_URL}/token/jwt/create/`, credentials)).data;
  },
  refresh: async (refreshToken: string) => {
    return (await axios.post(`${API_URL}/token/jwt/refresh/`, { refresh: refreshToken })).data;
  },
  verify: async (token: string) => {
    return (await axios.post(`${API_URL}/token/jwt/verify/`, { token: token })).data;
  },
};

/** Users */
const users = {
  list: async (token: string) => axios.get(`${API_URL}/carbon/users/`, authHeader(token)).then(res => res.data),
  me: async (token: string) => axios.get(`${API_URL}/carbon/users/me/`, authHeader(token)).then(res => res.data),
  retrieve: async (token: string, id: number) => axios.get(`${API_URL}/carbon/users/${id}/`, authHeader(token)).then(res => res.data),
  create: async (token: string, data: any) => axios.post(`${API_URL}/carbon/users/`, data, authHeader(token)).then(res => res.data),
  update: async (token: string, id: number, data: any) => axios.put(`${API_URL}/carbon/users/${id}/`, data, authHeader(token)).then(res => res.data),
  partialUpdate: async (token: string, id: number, data: any) => axios.patch(`${API_URL}/carbon/users/${id}/`, data, authHeader(token)).then(res => res.data),
  destroy: async (token: string, id: number) => axios.delete(`${API_URL}/carbon/users/${id}/`, authHeader(token)).then(res => res.data),
};

/** Groups */
const groups = {
  list: async (token: string) => axios.get(`${API_URL}/carbon/groups/`, authHeader(token)).then(res => res.data),
};

/** Status */
const status = {
  list: async (token: string) => axios.get(`${API_URL}/carbon/status/`, authHeader(token)).then(res => res.data),
};

/** Employees */
const employees = {
  list: async (token: string) => axios.get(`${API_URL}/carbon/employees/`, authHeader(token)).then(res => res.data),
  retrieve: async (token: string, id: number) => axios.get(`${API_URL}/carbon/employees/${id}/`, authHeader(token)).then(res => res.data),
  update: async (token: string, id: number, data: any) => axios.put(`${API_URL}/carbon/employees/${id}/`, data, authHeader(token)).then(res => res.data),
  partialUpdate: async (token: string, id: number, data: any) => axios.patch(`${API_URL}/carbon/employees/${id}/`, data, authHeader(token)).then(res => res.data),
};

/** Transports */
const transports = {
  list: async (token: string) => axios.get(`${API_URL}/carbon/transports/`, authHeader(token)).then(res => res.data),
};

/** Trips */
const trips = {
  list: async (
    token: string,
    years?: (number | string)[],
    employee_ids?: (number | string)[],
    mission_ids?: (number | string)[]
  ) => {
    const params = new URLSearchParams();
    if (years && years.length > 0) {
      years.forEach(y => params.append('year', y.toString()));
    }
    if (employee_ids && employee_ids.length > 0) {
      employee_ids.forEach(id => params.append('employee_id', id.toString()));
    }
    if (mission_ids && mission_ids.length > 0) {
      mission_ids.forEach(id => params.append('mission_id', id.toString()));
    }
    const url = `${API_URL}/carbon/trips/?${params.toString()}`;
    const res = await axios.get(url, authHeader(token));
    return res.data;
  },
  retrieve: async (token: string, id: number) => axios.get(`${API_URL}/carbon/trips/${id}/`, authHeader(token)).then(res => res.data),
  create: async (token: string, data: any) => axios.post(`${API_URL}/carbon/trips/`, data, authHeader(token)).then(res => res.data),
  update: async (token: string, id: number, data: any) => axios.put(`${API_URL}/carbon/trips/${id}/`, data, authHeader(token)).then(res => res.data),
  partialUpdate: async (token: string, id: number, data: any) => axios.patch(`${API_URL}/carbon/trips/${id}/`, data, authHeader(token)).then(res => res.data),
  destroy: async (token: string, id: number) => axios.delete(`${API_URL}/carbon/trips/${id}/`, authHeader(token)).then(res => res.data),
};

/** Missions */
const missions = {
  list: async (token: string) => (await axios.get(`${API_URL}/carbon/missions/`, authHeader(token))).data,
  retrieve: async (token: string, id: number) => axios.get(`${API_URL}/carbon/missions/${id}/`, authHeader(token)).then(res => res.data),
  create: async (token: string, data: any) => axios.post(`${API_URL}/carbon/missions/`, data, authHeader(token)).then(res => res.data),
  update: async (token: string, id: number, data: any) => axios.put(`${API_URL}/carbon/missions/${id}/`, data, authHeader(token)).then(res => res.data),
  partialUpdate: async (token: string, id: number, data: any) => axios.patch(`${API_URL}/carbon/missions/${id}/`, data, authHeader(token)).then(res => res.data),
  destroy: async (token: string, id: number) => axios.delete(`${API_URL}/carbon/missions/${id}/`, authHeader(token)).then(res => res.data),
};

/** Cities - GeoNames external API */
const cities = {
  fetch: async (name: string) => {
    const url = `http://api.geonames.org/searchJSON?q=${encodeURIComponent(name)}&username=${GEONAMES_USERNAME}`;
    const { data } = await axios.get(url);
    if (!data.geonames?.length) throw new Error("No cities found");
    return data.geonames;
  },
};

export default {
  token,
  users,
  groups,
  status,
  employees,
  transports,
  trips,
  missions,
  cities,
};