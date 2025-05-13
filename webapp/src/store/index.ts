
import { createStore } from 'vuex';


const store = createStore({
  state: {
    trips: JSON.parse(localStorage.getItem('trips') || '[]'),
    user: JSON.parse(localStorage.getItem('user') || 'null'),
  },
  mutations: {
    SET_TRIPS(state, trips) {
      state.trips = trips;
      localStorage.setItem('trips', JSON.stringify(trips));
    },
    CLEAR_TRIPS(state) {
      state.trips = [];
      localStorage.setItem('trips', JSON.stringify([]));
    },
    SET_USER(state, user) {
      state.user = user;
      localStorage.setItem('user', JSON.stringify(user));
    },
    CLEAR_USER(state) {
      state.user = null;
      localStorage.removeItem('user');
    },
  },
  actions: {
    setTrips({ commit }, trips) {
      commit('SET_TRIPS', trips);
    },
    clearTrips({ commit }) {
      commit('CLEAR_TRIPS');
    },
    setUser({ commit }, user) {
      commit('SET_USER', user);
    },
    clearUser({ commit }) {
      commit('CLEAR_USER');
    },
  },
  getters: {
    trips: state => state.trips,
    user: state => state.user,
    isAuthenticated: state => !!state.user,
  }
});

export default store;