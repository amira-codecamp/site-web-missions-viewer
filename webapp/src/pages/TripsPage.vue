<template>
  <section class="section">
    <div class="container">

      <div class="columns is-multiline is-gapless">

        <div class="column is-3">
          <span class="has-text-weight-semibold is-size-6">Total Carbon Footprint: {{ totalCarbonFootprint }}</span>
        </div>

        <div class="column is-5">
          <div class="wrapper bar-wrapper">
            <Chart :labels="baselineChart.labels" :values="baselineChart.values" title="Carbon Footprint" chartType="bar" />
          </div>
        </div>

       <div class="column is-2">
          <div class="wrapper pie-wrapper">
            <Chart :labels="transportChart.labels" :values="transportChart.values" title="By Transport" chartType="pie" />
          </div>
        </div>

        <div class="column is-2">
          <div class="wrapper pie-wrapper">
            <Chart :labels="missionChart.labels" :values="missionChart.values" title="By Mission" chartType="pie" />
          </div>
        </div>

        <div class="column is-12">
          <div class="wrapper">
            <div class="mb-4">
              <span class="has-text-weight-semibold is-size-6">Trips</span>
            </div>

            <div class="columns">
              <div class="column is-7">
                <input
                  v-model="search"
                  class="input is-small"
                  type="text"
                  placeholder="Search trips..."
                />
              </div>
              <div class="column is-3"></div>
              <div class="column is-1">
                <button class="button is-dark is-fullwidth is-small" v-if="isManager" @click="showAddForm">Add</button>
              </div>
              <div class="column is-1">
                <button class="button is-dark is-fullwidth is-small" @click="exportToXLSX">Export</button>
              </div>
            </div>

            <div class="table-content is-scrollable">
              <table class="table is-fullwidth is-hoverable is-striped is-size-7">
                <thead>
                  <tr>
                    <th>Dates</th>
                    <th>Mission</th>
                    <th>Departure</th>
                    <th>Destination</th>
                    <th>Transport</th>
                    <th>Carpoolers</th>
                    <th>Round Trip</th>
                    <th>Footprint</th>
                    <th>Employee</th>
                    <th></th>
                    <th></th>
                  </tr>
                </thead>
                <tbody>
                  <tr v-for="trip in filteredTrips" :key="trip.trip_id">
                    <td>{{ trip.mission.start_date }} → {{ trip.mission.end_date }}</td>
                    <td>{{ trip.mission.mission_desc }}</td>
                    <td>{{ trip.departure_city }}, {{ trip.departure_country }}</td>
                    <td>{{ trip.destination_city }}, {{ trip.destination_country }}</td>
                    <td>{{ trip.transport.transport_name }}</td>
                    <td>{{ trip.carpooling === 1 ? '' : trip.carpooling }}</td>
                    <td>{{ trip.is_round_trip === true ? '×' : '' }}</td>
                    <td class="has-text-weight-semibold">{{ trip.carbon_footprint }} kg CO2</td>
                    <td>{{ trip.employee.first_name }} {{ trip.employee.last_name }}</td>
                    <td>
                      <button 
                        class="button is-info is-light is-small" 
                        v-if="isManager" 
                        @click="showAlterForm(trip)"
                        style="font-weight: bold; padding: 0 6px;"
                        title="Modify trip">
                        Modify
                      </button>
                    </td>
                    <td>
                      <button 
                        v-if="isManager" 
                        class="button is-small is-danger is-light" 
                        @click="deleteTrip(trip.trip_id)" 
                        title="Delete trip"
                        style="font-weight:bold; padding: 0 6px;"
                      >
                        Delete
                      </button>
                    </td>
                  </tr>
                </tbody>
              </table>
            </div>

            <div class="modal" :class="{ 'is-active': showAddTripForm }">
              <div class="modal-background" @click="hideAddForm"></div>
              <div class="modal-card" style="width: 90%;">
                <header class="modal-card-head has-background-white">
                  <p class="modal-card-title has-text-grey-dark">Add a New Trip</p>
                  <button class="delete" aria-label="close" @click="hideAddForm"></button>
                </header>
                <section class="modal-card-body has-background-light">
                  <TripForm
                  :operation="'add'"
                  :trip="null" 
                  :disableQuantity="'false'"
                  @close="hideAddForm" />
                </section>
              </div>
            </div>

            <div class="modal" :class="{ 'is-active': showAlterTripForm }">
              <div class="modal-background" @click="hideAlterForm"></div>
              <div class="modal-card" style="width: 90%;">
                <header class="modal-card-head has-background-white">
                  <p class="modal-card-title has-text-grey-dark">Alter Trip</p>
                  <button class="delete" aria-label="close" @click="hideAlterForm"></button>
                </header>
                <section class="modal-card-body has-background-light">
                  <TripForm
                  :operation="'alter'"
                  :trip="selectedTrip"
                  :disableQuantity="'true'"
                  @close="hideAlterForm" />
                </section>
              </div>
            </div>

          </div>
        </div>

      </div>

    </div>
  </section>
</template>

<script setup>
defineOptions({
  name: 'TripsPage',
})

import tripsservice from '@/services/tripsservice'
import authservice from '@/services/authservice'

import { useStore } from '@/store'
import { ref, computed, onMounted } from 'vue'
import Chart from '@/components/Chart.vue'
import TripForm from '@/pages/TripForm.vue'
import * as XLSX from 'xlsx'
import { saveAs } from 'file-saver'

const store = useStore()
const search = ref('')
const showAddTripForm = ref(false)
const showAlterTripForm = ref(false)
const selectedTrip = ref(null)

const isManager = computed(() => store.state.isManager)
const trips = computed(() => store.state.trips)

const transportChart = computed(() => {
  const carbonByTransport = {}

  trips.value.forEach(trip => {
    const transportName = trip.transport?.transport_name || ''
    const carbon = Number(trip.carbon_footprint) || 0
    carbonByTransport[transportName] = (carbonByTransport[transportName] || 0) + carbon
  })

  return {
    labels: Object.keys(carbonByTransport),
    values: Object.values(carbonByTransport),
  }
})

const missionChart = computed(() => {
  const carbonByMission = {}

  trips.value.forEach(trip => {
    const missionDescription = trip.mission?.mission_desc || ''
    const carbon = Number(trip.carbon_footprint) || 0
    carbonByMission[missionDescription] = (carbonByMission[missionDescription] || 0) + carbon
  })

  return {
    labels: Object.keys(carbonByMission),
    values: Object.values(carbonByMission),
  }
})

const baselineChart = computed(() => {
  let totalCarbon = 0

  trips.value.forEach(trip => {
    const carbon = Number(trip.carbon_footprint) || 0
    totalCarbon += carbon
  })

  return {
    labels: ['Footprint'],
    values: [totalCarbon],
  }
})

const totalCarbonFootprint = computed(() => {
  if (!trips.value.length) return "0.00"
  return trips.value
    .reduce((total, trip) => total + (parseFloat(trip.carbon_footprint) || 0), 0)
    .toFixed(2)
})

function normalizeString(str) {
  if (!str) return ''
  return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase()
}

const filteredTrips = computed(() => {
  if (!search.value) return trips.value
  const term = normalizeString(search.value)
  return trips.value.filter(trip => {
    const fields = [
      trip.mission?.start_date,
      trip.mission?.end_date,
      trip.mission?.mission_desc,
      trip.departure_city,
      trip.departure_country,
      trip.destination_city,
      trip.destination_country,
      trip.transport?.transport_name,
      `${trip.employee?.first_name || ''} ${trip.employee?.last_name || ''}`,
      trip.carbon_footprint?.toString() || '',
    ]
    return fields.some(field => normalizeString(field).includes(term))
  })
})

const fetchToken = async () => {
  try {
    const refresh = store.state.refreshToken;
    const responsetok = await authservice.refresh(refresh);
    store.setItem("accessToken", responsetok.access);

  } catch (error) {
    alert("Session expired. Please login again.");

    store.clearItem('trips');
    store.clearItem('employees');
    store.clearItem('transports');
    store.clearItem('missions');
    store.clearItem('isManager');
    store.clearItem('user');
    store.clearItem('accessToken');
    store.clearItem('refreshToken');

    window.location.href = '/login';
    return;
  }
}

const deleteTrip = async (tripId) => {
  try {

    await fetchToken();

    const access = store.state.accessToken;

    await tripsservice.trips.deleteTrip(access, { trip_id: tripId });

    const response1 = await tripsservice.trips.fetchTrips(access);
    store.setItem('trips', response1.trips);

    alert(`Trip deleted successfully!`)
  
  } catch (error) {
    if (error.response?.data) {
      const messages = Object.entries(error.response.data).map(([key, val]) => `${key}: ${val}`)
      alert(messages.join('\n'))
    } else {
      alert('Something went wrong. Please try again.')
    }
  }
}

function exportToXLSX() {
  if (!filteredTrips.value.length) {
    alert('No trips to export !')
    return
  }
  const exportData = filteredTrips.value.map(trip => ({
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
  }))
  const worksheet = XLSX.utils.json_to_sheet(exportData)
  const workbook = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(workbook, worksheet, 'Trips')
  const wbout = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' })
  const blob = new Blob([wbout], { type: 'application/octet-stream' })
  saveAs(blob, 'trips_export.xlsx')
}

function showAlterForm(trip) {
  selectedTrip.value = trip
  showAlterTripForm.value = true
}

function hideAlterForm() {
  selectedTrip.value = null
  showAlterTripForm.value = false
}

function showAddForm() {
  showAddTripForm.value = true
}

function hideAddForm() {
  showAddTripForm.value = false
}

onMounted(() => {
  document.title = 'Trips | LIPN-carbon'
})
</script>

<style scoped>
.table-content {
  overflow-y: scroll;
  height: 40rem !important;
}

.wrapper, .wrapper canvas {
  width: 100% !important;
  min-height: unset;
}

.pie-wrapper{
  height: 15rem !important;
}

.bar-wrapper{
  height: 20rem !important;
}

.column {
  padding-top: 0 !important;
  padding-bottom: 0 !important; 
  margin-bottom: 0 !important; 
  margin-top: 0 !important; 
}
</style>