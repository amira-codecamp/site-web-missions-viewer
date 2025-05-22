
import { createStore } from 'vuex';

const store = createStore({
  state: {
    trips: JSON.parse(localStorage.getItem('trips') || '[]'),
    missions: JSON.parse(localStorage.getItem('missions') || '[]'),
    transports: JSON.parse(localStorage.getItem('transports') || '[]'),
    employees: JSON.parse(localStorage.getItem('employees') || '[]'),
    user: localStorage.getItem('user') || '',
    is_manager: JSON.parse(localStorage.getItem('is_manager') || 'false'),
  },
  mutations: {
    SET_TRIPS(state, trips) {
      state.trips = trips;
      localStorage.setItem('trips', JSON.stringify(trips));
    },
    CLEAR_TRIPS(state) {
      state.trips = [];
      localStorage.removeItem('trips');
    },
    SET_MISSIONS(state, missions) {
      state.missions = missions;
      localStorage.setItem('missions', JSON.stringify(missions));
    },
    CLEAR_MISSIONS(state) {
      state.missions = [];
      localStorage.removeItem('missions');
    },
    SET_TRANSPORTS(state, transports) {
      state.transports = transports;
      localStorage.setItem('transports', JSON.stringify(transports));
    },
    CLEAR_TRANSPORTS(state) {
      state.transports = [];
      localStorage.removeItem('transports');
    },
    SET_EMPLOYEES(state, employees) {
      state.employees = employees;
      localStorage.setItem('employees', JSON.stringify(employees));
    },
    CLEAR_EMPLOYEES(state) {
      state.employees = [];
      localStorage.removeItem('employees');
    },
    SET_USER(state, user) {
      state.user = user;
      localStorage.setItem('user', user);
    },
    CLEAR_USER(state) {
      state.user = '';
      localStorage.removeItem('user');
    },
    SET_ISMANAGER(state) {
      state.is_manager = true;
      localStorage.setItem('is_manager', JSON.stringify(true));
    },
    CLEAR_ISMANAGER(state) {
      state.is_manager = false;
      localStorage.setItem('is_manager', JSON.stringify(false));
    },
  },
  actions: {
    setTrips({ commit }, trips) {
      commit('SET_TRIPS', trips);
    },
    clearTrips({ commit }) {
      commit('CLEAR_TRIPS');
    },
    setMissions({ commit }, missions) {
      commit('SET_MISSIONS', missions);
    },
    clearMissions({ commit }) {
      commit('CLEAR_MISSIONS');
    },
    setTransports({ commit }, transports) {
      commit('SET_TRANSPORTS', transports);
    },
    clearTransports({ commit }) {
      commit('CLEAR_TRANSPORTS');
    },
    setEmployees({ commit }, employees) {
      commit('SET_EMPLOYEES', employees);
    },
    clearEmployees({ commit }) {
      commit('CLEAR_EMPLOYEES');
    },
    setUser({ commit }, user) {
      commit('SET_USER', user);
    },
    clearUser({ commit }) {
      commit('CLEAR_USER');
    },
    setIsManager({ commit }) {
      commit('SET_ISMANAGER');
    },
    clearIsManager({ commit }) {
      commit('CLEAR_ISMANAGER');
    },
  },
  getters: {
    trips: (state) => state.trips,
    missions: (state) => state.missions,
    transports: (state) => state.transports,
    employees: (state) => state.employees,
    user: (state) => state.user,
    is_manager: (state) => state.is_manager,
    isAuthenticated: (state) => state.user !== '',
  },
});

export default store;