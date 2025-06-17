
<template>
  <div class="table-wrapper">

      <div class="columns">
          <div class="column is-half">
          <input
              v-model="search"
              class="input is-small"
              type="text"
              placeholder="Search trips..."
          />
          </div>
          <div class="column is-one-quarter"></div>
          <div class="column is-one-quarter">
            <div class="columns">
              <div class="column is-three-third"></div>
              <div class="column is-one-third">
                <button 
                  class="button is-dark is-fullwidth is-small" 
                  v-if="isManager" 
                  @click="showAddForm"
                  style="font-weight: bold;"
                  title="Add trip"
                >
                  <span>Create Trip</span>
                </button>
              </div>
            </div>
          </div>
      </div>

      <div class="table-content is-scrollable">
          <table class="table is-fullwidth is-hoverable is-bordered is-size-7">
          <thead>
              <tr>
              <th>Dates</th>
              <th>Mission</th>
              <th>Employee</th>
              <th>Departure</th>
              <th>Destination</th>
              <th>Transport</th>
              <th>Carpoolers</th>
              <th>IsRound</th>
              <th>Footprint</th>
              <th colspan="2">
                <button class="button is-secondary is-small" @click="exportToXLSX">
                  <span class="icon is-small">
                    <i class="fas fa-file-export"></i>
                  </span>
                  <span>Export</span>
                </button>
              </th>
              </tr>
          </thead>
          <tbody>
              <tr v-for="trip in filteredTrips" :key="trip.trip_id">
              <td>{{ trip.mission.start_date }} → {{ trip.mission.end_date }}</td>
              <td>{{ trip.mission.mission_desc }}</td>
              <td>{{ trip.mission.employee.first_name }} {{ trip.mission.employee.last_name }}</td>
              <td>{{ trip.departure_city }}, {{ trip.departure_country }}</td>
              <td>{{ trip.destination_city }}, {{ trip.destination_country }}</td>
              <td>{{ trip.transport.transport_name }}</td>
              <td>{{ trip.carpooling === 1 ? '' : trip.carpooling }}</td>
              <td>{{ trip.is_round_trip === true ? '×' : '' }}</td>
              <td class="has-text-weight-semibold">{{ trip.carbon_footprint }} kg CO2</td>
              <td>
                <button 
                  class="button is-link is-light is-small" 
                  v-if="isManager" 
                  @click="showAlterForm(trip)"
                  style="font-weight: bold; padding: 0 6px;"
                  title="Modify trip"
                >
                  <span class="icon is-small">
                    <i class="fas fa-pencil-alt"></i>
                  </span>
                </button>
              </td>
              <td>
                  <button 
                    v-if="isManager"
                    class="button is-small is-danger is-light" 
                    @click="deleteTrip(trip)" 
                    title="Delete trip"
                    style="font-weight:bold; padding: 0 6px;"
                  >
                    <span class="icon is-small">
                      <i class="fas fa-times"></i>
                    </span>
                  </button>
              </td>
            </tr>
          </tbody>
          </table>
      </div>
  </div>

  <div class="modal" :class="{ 'is-active': showAddTripForm }">
      <div class="modal-background" @click="hideAddForm"></div>
      <div class="modal-card" style="width: 90%;">
      <header class="modal-card-head has-background-white">
          <p class="modal-card-title has-text-grey-dark">Add a New Trip</p>
          <button class="delete" aria-label="close" @click="hideAddForm"></button>
      </header>
      <section class="modal-card-body has-background-light">
          <TripAddForm
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
          <TripAlterForm
          :trip="selectedTrip"
          @close="hideAlterForm" />
      </section>
      </div>
  </div>
</template>

<script setup>
defineOptions({
  name: 'TripsTable',
})

import services from '@/services'

import { useStore } from '@/store'
import { ref, computed } from 'vue'
import * as XLSX from 'xlsx'
import { saveAs } from 'file-saver'

import TripAddForm from '@/pages/TripAddForm.vue'
import TripAlterForm from '@/pages/TripAlterForm.vue'

const store = useStore()
const search = ref('')
const showAddTripForm = ref(false)
const showAlterTripForm = ref(false)
const selectedTrip = ref(null)

const isManager = computed(() => store.state.isManager)

const props = defineProps({
  trips: {
    type: Object,
    required: true,
  },
})

const trips = ref(props.trips)

// Table
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
      `${trip.mission?.employee?.first_name || ''} ${trip.mission?.employee?.last_name || ''}`,
      trip.carbon_footprint?.toString() || '',
    ]
    return fields.some(field => normalizeString(field).includes(term))
  })
})

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
    'Employee Name': `${trip.mission?.employee?.first_name || ''} ${trip.mission?.employee?.last_name || ''}`.trim(),
  }))
  const worksheet = XLSX.utils.json_to_sheet(exportData)
  const workbook = XLSX.utils.book_new()
  XLSX.utils.book_append_sheet(workbook, worksheet, 'Trips')
  const wbout = XLSX.write(workbook, { bookType: 'xlsx', type: 'array' })
  const blob = new Blob([wbout], { type: 'application/octet-stream' })
  saveAs(blob, 'trips_export.xlsx')
}

// Operations on Trip
const fetchToken = async () => {
  try {
    const refresh = store.state.refreshToken;
    const responsetok = await services.auth.refresh(refresh);
    store.setItem("accessToken", responsetok.access);

  } catch (error) {
    alert("Session expired. Please login again.");

    store.clearItem('trips');
    store.clearItem('employees');
    store.clearItem('users');
    store.clearItem('transports');
    store.clearItem('missions');
    store.clearItem('isManager');
    store.clearItem('isAdmin');
    store.clearItem('logged');
    store.clearItem('accessToken');
    store.clearItem('refreshToken');

    window.location.href = '/login';
    return;
  }
}

const deleteTrip = async (trip) => {
  try {

    await fetchToken();

    const access = store.state.accessToken;

    await services.trips.deleteTrip(access, trip);

    const response1 = await services.trips.fetchTrips(access);
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

function showMissionsPanel() {

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
</script>

<style scoped>
.table-content {
  overflow-y: scroll;
  height: 40rem !important;
}

.table-wrapper, .table-wrapper canvas {
  width: 100% !important;
  min-height: unset;
}

thead th:nth-child(1),
tbody td:nth-child(1),
thead th:nth-child(2),
tbody td:nth-child(2),
thead th:nth-child(4),
tbody td:nth-child(4),
thead th:nth-child(5),
tbody td:nth-child(5) {
  width: 15%;
}

thead th:nth-child(8),
tbody td:nth-child(8),
thead th:nth-child(6),
tbody td:nth-child(6),
thead th:nth-child(7),
tbody td:nth-child(7) {
  width: 5%;
}

thead th:nth-child(3),
tbody td:nth-child(3),
thead th:nth-child(9) ,
tbody td:nth-child(9) {
  width: 10%;
}

thead th:nth-child(10),
tbody td:nth-child(10),
thead th:nth-child(11),
tbody td:nth-child(11) {
  width: 2.5%;
}
</style>