
<template>
  <section class="section has-background-light">
    <div class="container">

      <!-- Summary Card -->
      <div class="box has-background-white has-shadow mb-5">
        <p class="is-size-6 has-text-grey-dark mb-1">Total Carbon Footprint</p>
        <p class="is-size-3 has-text-weight-bold has-text-secondary">
          {{ totalCarbonFootprint }}
        </p>
      </div>

      <!-- No Trips Message -->
      <div v-if="!trips || trips.length === 0" class="notification is-light">
        No trips available.
      </div>

      <!-- Main Content -->
      <div v-else class="columns is-variable is-5">

        <!-- Charts Column -->
        <div class="column is-6">
          <div class="box has-background-white">
            <h2 class="is-size-6 has-text-grey-dark mb-4">Most Carbon Footprint Sources</h2>
            <div class="mb-4">
              <div class="wrapper">
                  <HistogramChart
                    :labels="Object.keys(transportHistogram)"
                    :values="Object.values(transportHistogram).map(item => item.value)"
                    :baseline="Object.values(transportHistogram).map(item => item.baseline)"
                    title="Transport"
                  />
                </div>
            </div>
            <div class="columns is-multiline">
              <div class="column is-half">
                <div class="wrapper">
                  <PieChart
                    :labels="Object.keys(missionCarbonMap)"
                    :values="Object.values(missionCarbonMap)"
                    title="Mission"
                  />
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Trips Table Column -->
        <div class="column is-6">
          <div class="box has-background-white">
            <div class="is-flex is-justify-content-space-between is-align-items-center mb-4">
              <h2 class="is-size-6 has-text-grey-dark">Trips</h2>
              <button
                class="button is-small is-dark"
                @click="exportToXLSX"
              >
                ⬇ Export
              </button>
            </div>

            <div class="field mb-3">
              <div class="control">
                <input
                  v-model="search"
                  class="input is-small"
                  type="text"
                  placeholder="Search trips..."
                />
              </div>
            </div>

            <div class="table-container is-scrollable">
              <table class="table is-fullwidth is-hoverable is-striped is-size-7">
                <thead>
                  <tr>
                    <th>Dates</th>
                    <th>Mission</th>
                    <th>Departure</th>
                    <th>Destination</th>
                    <th>Transport</th>
                    <th>Footprint</th>
                    <th>Employee</th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="trip in filteredData" :key="trip.trip_id">
                    <td>{{ trip.mission.start_date }} → {{ trip.mission.end_date }}</td>
                    <td>{{ trip.mission.mission_desc }}</td>
                    <td>{{ trip.departure_city }}, {{ trip.departure_country }}</td>
                    <td>{{ trip.destination_city }}, {{ trip.destination_country }}</td>
                    <td>{{ trip.transport.transport_name }}</td>
                    <td class="has-text-weight-semibold">
                      {{ trip.carbon_footprint }}
                    </td>
                    <td>{{ trip.employee.first_name }} {{ trip.employee.last_name }}</td>
                  </tr>
                </tbody>
              </table>
            </div>

            <!-- Add Trip Button -->
            <div class="mt-4" v-if="isManager">
              <button
                class="button is-dark is-fullwidth"
                @click="showForm"
              >
                + Add Trip
              </button>
            </div>
          </div>
        </div>
      </div>

      <!-- Modal -->
      <div class="modal" :class="{ 'is-active': showTripForm }">
        <div class="modal-background" @click="hideForm"></div>
        <div class="modal-card" style="width: 90%;">
          <header class="modal-card-head has-background-white">
            <p class="modal-card-title has-text-grey-dark">Add a New Trip</p>
            <button class="delete" aria-label="close" @click="hideForm"></button>
          </header>
          <section class="modal-card-body has-background-light">
            <TripForm @close="hideForm" />
          </section>
        </div>
      </div>

    </div>
  </section>
</template>

<script>
  import PieChart from '@/components/PieChart.vue';
  import HistogramChart from '@/components/HistogramChart.vue';
  import TripForm from '@/pages/TripForm.vue';
  import * as XLSX from 'xlsx';
  import { saveAs } from 'file-saver';

  export default {
    name: 'TripsPage',
    components: { PieChart, HistogramChart, TripForm },
    data() {
      return {
        search: '',
        trips: [],
        showTripForm: false,
      }
    },
    computed: {
      isManager() {
        return this.$store.state.is_manager;
      },
      transportHistogram(baselineValue) {
        const result = {};
        this.trips.forEach(trip => {
          const key = trip.transport.transport_name;
          const carbon = Number(trip.carbon_footprint);
          if (!result[key]) {
            result[key] = { value: 0, baseline: 0 };
          }
          result[key].value += carbon;
        });
        return result;
      },
      missionCarbonMap() {
        const result = {};
        this.trips.forEach(trip => {
          const key = trip.mission.mission_desc;
          const carbon = Number(trip.carbon_footprint);
          result[key] = (result[key] || 0) + carbon;
        });
        return result;
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
      filteredData() {
        if (!this.search) return this.trips;
        function normalizeString(str) {
          if (!str) return '';
          return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase();
        }
        const search = normalizeString(this.search.toLowerCase());
        return this.trips.filter(trip => {
          const fieldsToCheck = [
            trip.mission?.start_date,
            trip.mission?.end_date,
            trip.mission?.mission_desc,
            trip.departure_city,
            trip.departure_country,
            trip.destination_city,
            trip.destination_country,
            trip.transport?.transport_name,
            (trip.employee?.first_name || '') + ' ' + (trip.employee?.last_name || ''),
            trip.carbon_footprint,
          ];
          return fieldsToCheck.some(field => normalizeString(field).includes(search));
        });
      },
    },
    methods: {
      getTrips() {
      try {
          const trips = this.$store.state.trips;
          if (!trips) {
            this.trips = [];
            return;
          }
          this.trips = trips;
        } catch (error) {
          console.error('Failed to fetch trips:', error);
          this.trips = [];
        }
      },
      exportToXLSX() {
        if (!this.filteredData.length) {
          alert("No trips to export !");
          return;
        }
        const exportData = this.filteredData.map(trip => ({
          'Start Date': trip.mission?.start_date || '',
          'End Date': trip.mission?.end_date || '',
          'Mission Description': trip.mission?.mission_desc || '',
          'Departure City': trip.departure_city || '',
          'Departure Country': trip.departure_country || '',
          'Destination City': trip.destination_city || '',
          'Destination Country': trip.destination_country || '',
          'Transport': trip.transport?.transport_name || '',
          'Carbon Footprint': trip.carbon_footprint || '',
          'Employee Name': `${trip.employee?.first_name || ''} ${trip.employee?.last_name || ''}`.trim(),
        }));
        const worksheet = XLSX.utils.json_to_sheet(exportData);
        const workbook = XLSX.utils.book_new();
        XLSX.utils.book_append_sheet(workbook, worksheet, "Trips");
        const wbout = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' });
        const blob = new Blob([wbout], { type: 'application/octet-stream' });
        saveAs(blob, 'trips_export.xlsx');
      },
      showForm() {
        this.showTripForm = true;
      },
      hideForm() {
        this.showTripForm = false;
      },
    },
    mounted() {
      document.title = "Trips | LIPN-carbon";
      this.getTrips();
    }
  };
</script>

<style scoped>
  .table-container {
    height: 30rem;
    overflow-y: scroll;
  }

  .wrapper, .wrapper canvas {
    height: 100% !important;
    width: 100% !important;
    min-height: unset;
  }
</style>