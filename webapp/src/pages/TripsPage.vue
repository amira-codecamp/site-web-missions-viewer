
<template>
  <section class="section">
    <div class="container">

      <div class="mb-4 columns">
        <div class="column is-1">
          <label class="is-size-7">From</label>
          <input
            class="input is-small"
            list="begin_years_list"
            v-model="beginYear"
            placeholder="Start year"
            required
          />
          <datalist id="begin_years_list">
              <option
                  v-for="year in startYears"
                  :key="year"
                  :value="year"
              />
          </datalist>
        </div>
        <div class="column is-1">
          <label class="is-size-7">To</label>
          <input
            class="input is-small"
            list="end_years_list"
            v-model="endYear"
            placeholder="End year"
            required
          />
          <datalist id="end_years_list">
            <option v-for="year in endYears" :key="year" :value="year" />
          </datalist>
        </div>
        <div class="column is-2">
          <span class="has-text-weight-semibold is-size-7">Total Footprint (kg CO2): </span>
          <span class="has-text-weight-semibold has-background-info has-text-dark is-size-7">{{ totalCarbonFootprint }}</span>
        </div>
      </div>

      <div class="mb-4">
          <span class="has-text-weight-semibold is-size-7">Trips Charts</span>
      </div>

      <TripsCharts :totalCarbonFootprint="totalCarbonFootprint" :trips="trips" :key="chartsKey" />

      <div class="mb-4">
          <span class="has-text-weight-semibold is-size-7">Trips Table</span>
      </div>

      <TripsTable :trips="trips" :key="tableKey" />

    </div>
  </section>
</template>

<script setup>
defineOptions({
  name: 'TripsPage',
})

import { useStore } from '@/store'
import { ref, computed, onMounted, watch } from 'vue'

import TripsCharts from '@/pages/TripsCharts.vue'
import TripsTable from '@/pages/TripsTable.vue'

const store = useStore()
const trips = ref(store.state.trips)

const totalCarbonFootprint = computed(() => {
  if (!trips.value.length) return "0.00"
    return trips.value
    .reduce((total, trip) => total + (parseFloat(trip.carbon_footprint) || 0), 0)
    .toFixed(2)
})

const chartsKey = ref(0);
const tableKey = ref(0);

const currentYear = new Date().getFullYear()

const minYear = computed(() => {
  const dates = trips.value
    .map(trip => trip.mission?.start_date)
    .filter(Boolean)
    .map(dateStr => new Date(dateStr).getFullYear())
  if (dates.length === 0) {
    return null
  } else {
    return Math.min(...dates)
  }
})

const startYears = computed(() => {
  const length = currentYear - minYear.value + 1
  return Array.from({ length }, (_, index) => minYear.value + index)
})

const beginYear = ref(null)
const endYear = ref(null)

const endYears = ref([])

const generateEndYears = () => {
  const startY = parseInt(beginYear.value)
  const length = currentYear - startY + 1
  endYears.value = Array.from({ length }, (_, index) => startY + index)
}

const filterTripsByYear = () => {
  const allTrips = store.state.trips

  const startY = parseInt(beginYear.value)
  const endY = parseInt(endYear.value)

  trips.value = allTrips.filter(trip => {
    const dateStr = trip.mission.start_date
    const tripYear = new Date(dateStr).getFullYear()
    return tripYear >= startY && tripYear <= endY
  })
}

watch(beginYear, () => {
  generateEndYears();
})

watch(trips, () => {
  chartsKey.value++;
  tableKey.value++;
})

watch(
  () => store.state.trips,
  (newTrips) => {
    trips.value = newTrips
  },
  { immediate: true, deep: true }
)

onMounted(() => {
  document.title = 'Trips | LIPN-carbon'

  beginYear.value = minYear.value
  endYear.value = currentYear
  generateEndYears()
})
</script>