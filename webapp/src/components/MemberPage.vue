
<template>
  <div class="container">
    <div class="columns is-mobile is-vcentered">
      <div class="column is-half">
        <h1 class="title">Trip List</h1>
      </div>
      <div class="column is-half has-text-right">
        <button class="button is-dark" @click="logout">Logout</button>
      </div>
    </div>
    <div class="box">
      <h2 class="subtitle">Total Carbon Footprint : <span>{{ totalCarbonFootprint }}</span></h2>
      <table class="table is-striped is-bordered is-hoverable is-fullwidth">
        <thead>
          <tr>
            <th>Employee</th>
            <th>Departure</th>
            <th>Destination</th>
            <th>Transport</th>
            <th>Carbon Footprint</th>
            <th>Travel Reason</th>
            <th>Mission Dates</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="trip in trips" :key="trip.trip_id">
            <td>{{ trip.employee.first_name }} {{ trip.employee.last_name }}</td>
            <td>{{ trip.departure_city }}, {{ trip.departure_country }}</td>
            <td>{{ trip.destination_city }}, {{ trip.destination_country }}</td>
            <td>{{ trip.transport.transport_name }}</td>
            <td>{{ trip.carbon_footprint }}</td>
            <td>{{ trip.mission.mission_desc }}</td>
            <td>{{ trip.mission.start_date }} to {{ trip.mission.end_date }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>


<script>
export default {
  computed: {
    trips() {
      return this.$store.state.trips.trips;
    },
    totalCarbonFootprint() {
      if (Array.isArray(this.trips) && this.trips.length > 0) {
        return this.trips.reduce((total, trip) => {
          const carbonFootprint = parseFloat(trip.carbon_footprint) || 0;
          return total + carbonFootprint;
        }, 0).toFixed(2);
      }
      return "0.00";
    }
  },
  methods: {
    logout() {
      this.$store.dispatch('clearTrips').then(() => {
        this.$router.push('/login');
      });
    }
  },
  mounted() {
    document.title = "Trips | LIPN-carbon";
  }
};
</script>