
import { createStore } from 'vuex';


const store = createStore({
  state: {
    trips: JSON.parse(localStorage.getItem('trips') || '[]'),
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
  },
  actions: {
    setTrips({ commit }, trips) {
      commit('SET_TRIPS', trips);
    },
    clearTrips({ commit }) {
      commit('CLEAR_TRIPS');
    },
  },
  getters: {
    trips: state => state.trips,
  }
});

export default store;