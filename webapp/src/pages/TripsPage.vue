
<template>

  <div class="page-body">

    <div class="is-flex is-justify-content-start is-align-items-center mb-4">
      <div class="has-text-left">
        <span class="has-text-weight-semibold">Total Carbon Footprint : </span>
        <span class="has-text-weight-bold">{{ totalCarbonFootprint }}</span>
      </div>
    </div>

    <div v-if="!trips || trips.length === 0">
      No trips available.
    </div>

    <div v-else class="table-container">
      <table class="table is-fullwidth is-hoverable">
        <!-- <thead>
          <tr>
            <th></th>
            <th>Travel</th>
            <th>From</th>
            <th>To</th>
            <th>Transport</th>
            <th>Carbon</th>
            <th v-if="ManageEmployee">Employee</th>
          </tr>
        </thead> -->
        <tbody>
          <tr v-for="trip in trips" :key="trip.trip_id">
            <td>{{ trip.mission.start_date }} → {{ trip.mission.end_date }}</td>
            <td>{{ trip.mission.mission_desc }}</td>
            <td>{{ trip.departure_city }}, {{ trip.departure_country }}</td>
            <td>{{ trip.destination_city }}, {{ trip.destination_country }}</td>
            <td>{{ trip.transport.transport_name }}</td>
            <td>{{ trip.carbon_footprint }}</td>
            <td v-if="ManageEmployee">{{ trip.employee.first_name }} {{ trip.employee.last_name }}</td>
          </tr>
        </tbody>
      </table>
    </div>

  </div>

</template>

<script>
  export default {
    name: 'TripsPage',
    computed: {
      trips() {
        return this.$store.state.trips.trips;
      },
      totalCarbonFootprint() {
        if (Array.isArray(this.trips) && this.trips.length > 0) {
          return this.trips.reduce((total, trip) => {
            const carbon = parseFloat(trip.carbon_footprint) || 0;
            return total + carbon;
          }, 0).toFixed(2);
        }
        return "0.00";
      },
      ManageEmployee() {
        if (!this.trips) {
          return false;
        }
        const employees = this.trips.map(trip => trip.employee.email);
        const uniqueEmployees = [...new Set(employees)];
        return uniqueEmployees.length > 1;
      }
    },
    mounted() {
      document.title = "Trips | LIPN-carbon";
    }
  };
</script>

<style scoped>
  .page-body {
    padding-left: 1.5rem;
    padding-top: 1.5rem;
    display: block;
  }

  .table-container {
    max-height: 30rem;
    overflow-y: scroll;
  }
</style>