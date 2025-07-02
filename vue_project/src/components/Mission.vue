<template>
  <nav class="navbar mb-5">
    <div class="navbar-start">
      <div class="navbar-item">
        <span class="has-text-weight-semibold is-size-5">Analytics</span>
      </div>
    </div>

    <div class="navbar-end">
      <div class="navbar-item">
        <input class="input is-small" list="yearsList" v-model="selectedPeriod" placeholder="Select date" />
        <datalist id="yearsList">
          <option v-for="year in years" :key="year" :value="year" />
        </datalist>
      </div>

      <div class="navbar-item">
        <button class="button is-link is-small" @click="filterByYear">Filter</button>
      </div>
    </div>
  </nav>

  <div class="flex-content columns is-multiline mb-5">

    <div class="column is-4">
      <!-- Pie Chart Card -->
      <div class="card mb-4">
        <div class="card-content is-flex is-flex-direction-column p-5">
          <select v-model="pieChartType" class="select is-small mb-3">
            <option v-for="option in chartOptions" :key="option" :value="option">{{ option }}</option>
          </select>
          <span class="is-size-7 mb-3 has-text-link has-text-weight-semibold">
            Carbon Pie per {{ pieChartType }}
          </span>
          <span class="is-size-7 mb-3">Over {{ period }}</span>
          <div class="chart-container pie-container" ref="pieChartRef"></div>
        </div>
      </div>
    </div>

    <div class="column is-2">
      <!-- Total Footprint Card -->
      <div class="card mb-4">
        <div class="card-content is-flex is-flex-direction-column p-5">
          <span class="is-size-7 mb-3 has-text-link has-text-weight-semibold">Carbon Emission</span>
          <span class="has-text-weight-semibold is-size-5 mb-3">{{ totalFootprint }} kg</span>
          <span class="is-size-7 mb-3">Over {{ period }}</span>
        </div>
      </div>
    </div>

    <div class="column is-6">
      <!-- Line Chart Card -->
      <div class="card mb-4">
        <div class="card-content is-flex is-flex-direction-column p-5">
          <span class="is-size-7 mb-3 has-text-link has-text-weight-semibold">
            Carbon Line per year
          </span>
          <span class="is-size-7 mb-3">Over {{ period }}</span>
          <div class="chart-container line-container" ref="lineChartRef"></div>
        </div>
      </div>
    </div>

    <!-- Bar Chart Card -->
    <div class="column is-6">
      <div class="card mb-4">
        <div class="card-content is-flex is-flex-direction-column p-5">
          <select v-model="barChartType" class="select is-small mb-3">
            <option v-for="option in chartOptions" :key="option" :value="option">{{ option }}</option>
          </select>
          <span class="is-size-7 mb-3 has-text-link has-text-weight-semibold">
            Carbon Bar per {{ barChartType }}
          </span>
          <span class="is-size-7 mb-3">Over {{ period }}</span>
          <div class="chart-container bar-container" ref="barChartRef" >
          </div>
        </div>
      </div>
    </div>

    <!-- Trips Table Card -->
    <div class="column is-12">
      <div class="card mb-4">
        <div class="card-content is-flex is-flex-direction-column p-5">
          <input v-model="searchword" class="input is-small mb-5" type="text" placeholder="Search trips..." />
          <span class="is-size-7 mb-3">Over {{ period }}</span>
          <div class="table-container is-scrollable">
            <table class="table is-fullwidth is-hoverable is-size-7">
              <thead>
                <tr>
                  <th>Employee Name</th>
                  <th>Mission Num</th>
                  <th>Departure Date</th>
                  <th>Arrival Date</th>
                  <th>Departure City</th>
                  <th>Destination City</th>
                  <th>Transport Mode</th>
                  <th>Number Of Carpoolers</th>
                  <th>Is Round Trip</th>
                  <th>Carbon Footprint</th>
                  <th colspan="2">
                    <button
                      v-if="isManager"
                      class="button is-dark is-light is-small"
                      @click="showAddForm"
                      title="Add trip"
                      style="font-weight: bold; padding: 0 6px;"
                    >
                      <span class="icon is-small"><i class="fas fa-plus"></i></span>
                      <span>Add</span>
                    </button>
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="trip in tripsTable" :key="trip.trip_id">
                  <td>{{ trip.mission.employee.first_name }} {{ trip.mission.employee.last_name }}</td>
                  <td>{{ trip.mission.mission_desc }}</td>
                  <td>{{ trip.mission.start_date }}</td>
                  <td>{{ trip.mission.end_date }}</td>
                  <td>{{ trip.departure_city }}, {{ trip.departure_country }}</td>
                  <td>{{ trip.destination_city }}, {{ trip.destination_country }}</td>
                  <td>{{ trip.transport }}</td>
                  <td>{{ trip.carpooling === 1 ? '' : trip.carpooling }}</td>
                  <td>{{ trip.is_round_trip ? '×' : '' }}</td>
                  <td class="has-text-weight-semibold">{{ trip.carbon_footprint }} kg CO2</td>
                  <td>
                    <button
                      v-if="isManager"
                      class="button is-link is-light is-small"
                      @click="showAlterForm(trip)"
                      title="Modify trip"
                      style="font-weight: bold; padding: 0 6px;"
                    >
                      <span class="icon is-small"><i class="fas fa-pencil-alt"></i></span>
                    </button>
                  </td>
                  <td>
                    <button
                      v-if="isManager"
                      class="button is-small is-danger is-light"
                      @click="deleteTrip(trip.trip_id)"
                      title="Delete trip"
                      style="font-weight: bold; padding: 0 6px;"
                    >
                      <span class="icon is-small"><i class="fas fa-times"></i></span>
                    </button>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>

    <!-- Add Trip Modal -->
    <div class="modal" :class="{ 'is-active': addFormActive }">
      <div class="modal-background" @click="hideAddForm"></div>
      <div class="modal-card" style="width: 90%;">
        <header class="modal-card-head has-background-white">
          <p class="modal-card-title has-text-grey-dark">Add New Trip</p>
          <button class="delete" aria-label="close" @click="hideAddForm"></button>
        </header>
        <section class="modal-card-body has-background-light">
          <TripAddForm ref="addFormRef" @close="hideAddForm" />
        </section>
        <footer class="modal-card-foot has-background-light">
          <button class="button is-dark" @click="submitAddForm">Submit</button>
        </footer>
      </div>
    </div>

    <!-- Alter Trip Modal -->
    <div class="modal" :class="{ 'is-active': alterFormActive }">
      <div class="modal-background" @click="hideAlterForm"></div>
      <div class="modal-card" style="width: 90%;">
        <header class="modal-card-head has-background-white">
          <p class="modal-card-title has-text-grey-dark">Alter Trip</p>
          <button class="delete" aria-label="close" @click="hideAlterForm"></button>
        </header>
        <section class="modal-card-body has-background-light">
          <TripAlterForm ref="alterFormRef" :trip="alterTrip" @close="hideAlterForm" />
        </section>
        <footer class="modal-card-foot has-background-light">
          <button class="button is-dark" @click="submitAlterForm">Submit</button>
        </footer>
      </div>
    </div>

  </div>
</template>

<script setup>
import { ref, computed, onMounted, onBeforeUnmount, watch } from 'vue'

import services from '@/composables/services'

import { fetchToken, getData, getPermission, setData } from '@/composables/session'
const { isAdmin, isManager, isStandard } = getPermission()

import TripAddForm from '@/components/TripAddForm'
import TripAlterForm from '@/components/TripAlterForm'

import * as echarts from 'echarts/core'
import { BarChart, PieChart } from 'echarts/charts'
import {
  TitleComponent, TooltipComponent, LegendComponent,
  GridComponent, DataZoomComponent, GraphicComponent,
} from 'echarts/components'
import { LineChart } from 'echarts/charts'
import { CanvasRenderer } from 'echarts/renderers'

echarts.use([
  TitleComponent, TooltipComponent, LegendComponent,
  GridComponent, DataZoomComponent, GraphicComponent,
  BarChart, PieChart, CanvasRenderer, LineChart
])


const chartOptions = ['mission', 'transport', 'employee', 'status']
const pieChartType = ref(chartOptions[0])
const barChartType = ref(chartOptions[0])
const lineChartRef = ref(null)
let lineChartInstance = null
const pieChartRef = ref(null)
const barChartRef = ref(null)
let pieChartInstance = null
let barChartInstance = null

const tripsData = ref([])
const tripsFiltered = ref([])
const totalFootprint = ref(0)
const selectedPeriod = ref(null)
const period = ref(null)
const years = ref([])

const footprintsByYear = computed(() => {
  const map = new Map()
  tripsFiltered.value.forEach(trip => {
    const year = new Date(trip.mission.start_date).getFullYear().toString()
    const carbon = Number(trip.carbon_footprint) || 0
    map.set(year, (map.get(year) || 0) + carbon)
  })
  return Array.from(map.entries()).map(([year, value]) => ({
    name: year,
    value: Number(value.toFixed(2))
  }))
})

const lineChartOptions = computed(() => {
  const data = footprintsByYear.value
  return {
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: data.map(d => d.name),
      boundaryGap: false
    },
    yAxis: {
      type: 'value',
      name: 'kg CO2'
    },
    series: [{
      type: 'line',
      smooth: false,
      data: data.map(d => d.value),
      lineStyle: { width: 3 },
      areaStyle: { color: 'rgba(59, 130, 246, 0.2)' },
      itemStyle: { color: '#1e40af' },
    }],
  }
})

function loadTrips() {
  if (selectedPeriod.value === 'All') {
    tripsFiltered.value = tripsData.value
  } else {
    tripsFiltered.value = tripsData.value.filter(trip => {
      const tripDate = new Date(trip.mission.start_date)
      return tripDate.getFullYear() === Number(selectedPeriod.value)
    })
  }
  totalFootprint.value = tripsFiltered.value.reduce((sum, trip) => {
    const val = parseFloat(trip.carbon_footprint)
    return sum + (isNaN(val) ? 0 : val)
  }, 0).toFixed(2)
}

// Initialize years and current period on mount
onMounted(() => {
  tripsData.value = getData()

  years.value = ['All', ...new Set(tripsData.value.map(trip => new Date(trip.mission.start_date).getFullYear()))]
  selectedPeriod.value = years.value[0]
  period.value = years.value[0]

  loadTrips()

  initCharts()
  window.addEventListener('resize', resizeCharts)
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', resizeCharts)
  pieChartInstance?.dispose()
  barChartInstance?.dispose()
  lineChartInstance?.dispose()
})

watch(lineChartOptions, (newOptions) => {
  lineChartInstance.setOption(newOptions)
  lineChartInstance.resize()
})

// Filter button handler
function filterByYear() {
  loadTrips()
  period.value = selectedPeriod.value
}

// Chart initialization
function initCharts() {
  pieChartInstance = echarts.init(pieChartRef.value)
  updatePieChart()
  barChartInstance = echarts.init(barChartRef.value)
  updateBarChart()
  lineChartInstance = echarts.init(lineChartRef.value)
  lineChartInstance.setOption(lineChartOptions.value)
}

function resizeCharts() {
  pieChartInstance?.resize()
  barChartInstance?.resize()
  lineChartInstance?.resize()
}

// Chart update
function updatePieChart() {
  if (!tripsFiltered.value.length) return;

  const pieData = aggregateData(pieChartType.value);

  pieChartInstance.setOption({
    tooltip: { trigger: 'item' },
    legend: { show: false},
    series: [{
      name: 'Carbon Footprint',
      type: 'pie',
      radius: '50%',
      data: pieData,
      emphasis: {
        itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0,0,0,0.5)' }
      }
    }]
  });
}

function updateBarChart() {
  if (!tripsFiltered.value.length) return;

  const barData = aggregateData(barChartType.value);

  barChartInstance.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: {
      type: 'category',
      data: barData.map(item => item.name),
      axisLabel: { rotate: 30 }
    },
    yAxis: { type: 'value', name: 'kg CO2' },
    series: [{
      type: 'bar',
      data: barData.map(item => item.value),
      itemStyle: { color: '#3b82f6' },
      barMaxWidth: 10
    }]
  });
}

// Aggregate trips by a given key and sum carbon footprint
function aggregateData(key) {
  const map = new Map();

  tripsFiltered.value.forEach(trip => {
    let groupKey = '';
    switch (key) {
      case 'mission':
        groupKey = `${trip.departure_city}, ${trip.departure_country} -> ${trip.destination_city}, ${trip.destination_country}`;
        break;
      case 'transport':
        groupKey = trip.transport;
        break;
      case 'employee':
        groupKey = `${trip.mission.employee.first_name}, ${trip.mission.employee.last_name}`;
        break;
      case 'status':
        groupKey = `${trip.mission.employee.status}`;
        break;
      default:
        groupKey = '';
    }

    if (groupKey) {
      const carbon = Number(trip.carbon_footprint) || 0;
      const current = Number(map.get(groupKey)) || 0;
      map.set(groupKey, current + carbon);
    }
  });

  return Array.from(map.entries()).map(([name, value]) => ({
    name,
    value: Number(value.toFixed(2))
  }));
}

// Watchers for type changes to update charts
watch([pieChartType, tripsFiltered], updatePieChart)
watch([barChartType, tripsFiltered], updateBarChart)

const searchword = ref('')

// Modal states and refs
const addFormActive = ref(false)
const alterFormActive = ref(false)
const alterTrip = ref(null)
const addFormRef = ref(null)
const alterFormRef = ref(null)

// Filtered trips by searchword
const tripsTable = computed(() => {
  if (!searchword.value.trim()) return tripsFiltered.value

  const term = searchword.value.toLowerCase()
  return tripsFiltered.value.filter(trip =>
    trip.mission.employee.first_name.toLowerCase().includes(term) ||
    trip.mission.employee.last_name.toLowerCase().includes(term) ||
    trip.mission.mission_desc.toLowerCase().includes(term) ||
    trip.departure_city.toLowerCase().includes(term) ||
    trip.destination_city.toLowerCase().includes(term) ||
    trip.transport.toLowerCase().includes(term)
  )
})

// Modal controls
function showAddForm() {
  addFormActive.value = true
}

function hideAddForm() {
  addFormActive.value = false
}

function submitAddForm() {
  addFormRef.value?.submit()
}

function showAlterForm(trip) {
  alterTrip.value = trip
  alterFormActive.value = true
}

function hideAlterForm() {
  alterFormActive.value = false
  alterTrip.value = null
}

function submitAlterForm() {
  alterFormRef.value?.submit()
}

// Delete trip
async function deleteTrip(tripId) {
  if (confirm('Are you sure you want to delete this trip?')) {
    try {
      const token = await fetchToken()
      await services.trips.destroy(token, tripId)
      
      const resp = await services.trips.list(token)
      tripsData.value = resp
      setData(resp)
      
      alert('Trip deleted successfully!')
    } catch (error) {
      console.error(error)
    }
  }
}

watch(tripsData, () => {
  loadTrips()
})
</script>

<style scoped>
.chart-container {
  width: 100%;
}
.bar-container {
  height: 250px;
  width: 100%;
}
.pie-container {
  height: 200px;
  width: 100%;
}
.line-container {
  height: 250px;
  width: 100%;
}
.card {
  border-radius: 8px;
  background-color: #f9fafb;
}
.no-shadow {
  box-shadow: none;
  background-color: transparent;
}
.table-container {
  overflow-y: scroll;
  height: 800px !important;
}
</style>