import axios from 'axios';

const API_URL = process.env.VUE_APP_SERVER_URL;
const GEONAMES_USERNAME = process.env.VUE_APP_GEONAMES_USERNAME;

// Helper: Authentication header
const authHeader = (token: string) => ({
  headers: { Authorization: `Bearer ${token}` },
});

/** JWT auth API */
const auth = {
  login: async (credentials: unknown) => {
    const res = await axios.post(`${API_URL}/token/jwt/create`, credentials);
    return res.data;
  },
  refresh: async (refreshToken: string) => {
    const res = await axios.post(`${API_URL}/token/jwt/refresh`, { refresh: refreshToken });
    return res.data;
  },
};

/** Users API, full CRUD */
const users = {
  list: async (token: string) => {
    const res = await axios.get(`${API_URL}/carbon/users/`, authHeader(token));
    return res.data;
  },
  me: async (token: string) => {
    const res = await axios.get(`${API_URL}/carbon/users/me/`, authHeader(token));
    return res.data;
  },
  create: async (token: string, data: unknown) => {
    const res = await axios.post(`${API_URL}/carbon/users/`, data, authHeader(token));
    return res.data;
  },
  update: async (token: string, id: number, data: unknown) => {
    const res = await axios.put(`${API_URL}/carbon/users/${id}/`, data, authHeader(token));
    return res.data;
  },
  destroy: async (token: string, id: number) => {
    const res = await axios.delete(`${API_URL}/carbon/users/${id}/`, authHeader(token));
    return res.data;
  },
};

/** Groups - list */
const groups = {
  list: async (token: string) => {
    const res = await axios.get(`${API_URL}/carbon/groups/`, authHeader(token));
    return res.data;
  },
};

/** Status - list */
const status = {
  list: async (token: string) => {
    const res = await axios.get(`${API_URL}/carbon/status/`, authHeader(token));
    return res.data;
  },
};

/** Employees - list and update */
const employees = {
  list: async (token: string) => {
    const res = await axios.get(`${API_URL}/carbon/employees/`, authHeader(token));
    return res.data;
  },
  update: async (token: string, id: number, data: unknown) => {
    const res = await axios.put(`${API_URL}/carbon/employees/${id}/`, data, authHeader(token));
    return res.data;
  },
};

/** Transports - list */
const transports = {
  list: async (token: string) => {
    const res = await axios.get(`${API_URL}/carbon/transports/`, authHeader(token));
    return res.data;
  },
};

/** Trips - full CRUD */
const trips = {
  list: async (token: string) => {
    const res = await axios.get(`${API_URL}/carbon/trips/`, authHeader(token));
    return res.data;
  },
  create: async (token: string, data: unknown) => {
    const res = await axios.post(`${API_URL}/carbon/trips/`, data, authHeader(token));
    return res.data;
  },
  update: async (token: string, id: number, data: unknown) => {
    const res = await axios.put(`${API_URL}/carbon/trips/${id}/`, data, authHeader(token));
    return res.data;
  },
  destroy: async (token: string, id: number) => {
    const res = await axios.delete(`${API_URL}/carbon/trips/${id}/`, authHeader(token));
    return res.data;
  },
};

/** Missions - full CRUD */
const missions = {
  list: async (token: string) => {
    const res = await axios.get(`${API_URL}/carbon/missions/`, authHeader(token));
    return res.data;
  },
  create: async (token: string, data: unknown) => {
    const res = await axios.post(`${API_URL}/carbon/missions/`, data, authHeader(token));
    return res.data;
  },
  update: async (token: string, id: number, data: unknown) => {
    const res = await axios.put(`${API_URL}/carbon/missions/${id}/`, data, authHeader(token));
    return res.data;
  },
  destroy: async (token: string, id: number) => {
    const res = await axios.delete(`${API_URL}/carbon/missions/${id}/`, authHeader(token));
    return res.data;
  },
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
  auth,
  users,
  groups,
  status,
  employees,
  transports,
  trips,
  missions,
  cities,
};