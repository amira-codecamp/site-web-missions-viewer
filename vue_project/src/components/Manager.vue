<template>
    <nav class="navbar mb-5">
        <div class="navbar-start">
            <div class="navbar-item">
                <span class="has-text-weight-semibold is-size-5">Analytics</span>
            </div>
        </div>

        <div class="navbar-end">
            <div class="navbar-item">
                <input class="input is-small" list="yearsList" v-model="selectedPeriod" placeholder="Select date">
                <datalist id="yearsList">
                    <option v-for="y in years" :key="y" :value="y"></option>
                </datalist>
            </div>

            <div class="navbar-item">
                <button class="button is-link is-small" @click="filterByYear">
                    <span>Filter</span>
                </button>
            </div>
        </div>
    </nav>

    <div class="flex-content columns is-multiline mb-5">

        <div class="column is-4">
          <div class="card">
            <div class="card-content is-flex is-flex-direction-column p-5">
              <select v-model="pieChartType" class="select is-small mb-3">
                <option value="Employees">Employees</option>
                <option value="Status">Status</option>
                <option value="Trips">Trips</option>
                <option value="Transports">Transports</option>
                <option value="Years">Years</option>
              </select>
              <span class="is-size-7 mb-3 has-text-link has-text-weight-semibold">
                  Carbon Footprints per {{ pieChartType }}
              </span>
              <span class="is-size-7 mb-3">Over {{ period }}</span>
              <div class="chart-container pie-container">
                <div ref="pieChartRef" style="width: 100%; height: 100%;"></div>
              </div>
            </div>
          </div>
        </div>

        <div class="column is-2">
          <div class="card">
            <div class="card-content is-flex is-flex-direction-column p-5">
                <span class="is-size-7 mb-3 has-text-link has-text-weight-semibold">Carbon Emission</span>
                <span class="has-text-weight-semibold is-size-5 mb-3">{{ totalFootprint }} kg</span>
                <span class="is-size-7 mb-3">Over {{ period }}</span>
            </div>
          </div>
        </div>

        <div class="column is-6">
          <div class="card">
            <div class="card-content is-flex is-flex-direction-column p-5">
                <select v-model="barChartType" class="select is-small mb-3">
                  <option value="Employees">Employees</option>
                  <option value="Trips">Trips</option>
                  <option value="Transports">Transports</option>
                  <option value="Years">Years</option>
                </select>
                <span class="is-size-7 mb-3 has-text-link has-text-weight-semibold">
                    Carbon Footprints per {{ barChartType }}
                </span>
                <span class="is-size-7 mb-3">Over {{ period }}</span>
                <div class="chart-container bar-container">
                  <div ref="barChartRef" style="width: 100%; height: 100%;"></div>
                </div>
            </div>
          </div>
        </div>

        <div class="column is-12">
          <div class="card">
            <div class="card-content is-flex is-flex-direction-column p-5">
              <input
                  v-model="searchword"
                  class="input is-small mb-5"
                  type="text"
                  placeholder="Search trips..."
              />
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
                      <th></th>
                      <th></th>
                    </tr>
                </thead>
                <tbody>
                  <tr v-for="trip in filteredTrips" :key="trip.trip_id">
                    <td>{{ trip.mission.employee.first_name }} {{ trip.mission.employee.last_name }}</td>
                    <td>{{ trip.mission.mission_desc }}</td>
                    <td>{{ trip.mission.start_date }}</td>
                    <td>{{ trip.mission.end_date }}</td>
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
                        @click="showForm(trip)"
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
                          @click="deleteTrip(trip.trip_id)" 
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
          </div>
        </div>
        <div class="column is-1"></div>
    </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, onBeforeUnmount, nextTick, reactive, watchEffect } from 'vue'

import { useStore } from '@/store'
const store = useStore()

import services from '@/services'
import { fetchToken } from '@/session'

import * as echarts from 'echarts/core'
import {
  BarChart,
  PieChart
} from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DataZoomComponent,
  GraphicComponent,
} from 'echarts/components'
import {
  CanvasRenderer
} from 'echarts/renderers'

echarts.use([
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DataZoomComponent,
  GraphicComponent,
  BarChart,
  PieChart,
  CanvasRenderer
])


const selectedTrips = ref(store.state.trips)

const isManager = ref(store.state.account.group?.group_name === 'MISSIONMANAGER');

const totalFootprint = computed(() => {
  if (!selectedTrips.value.length) return "0.00"
    return selectedTrips.value
    .reduce((total, trip) => total + (parseFloat(trip.carbon_footprint) || 0), 0)
    .toFixed(2)
})

const minYear = computed(() => {
  const trips = store.state.trips
  const dates = trips
    .map(trip => trip.mission?.start_date)
    .filter(Boolean)
    .map(dateStr => new Date(dateStr).getFullYear())
  if (dates.length === 0) {
    return null
  } else {
    return Math.min(...dates)
  }
})

const currentYear = new Date().getFullYear()

const selectedPeriod = ref(`Past ${currentYear - minYear.value} year${currentYear - minYear.value === 1 ? '' : 's'}`);
const period = ref(`Past ${currentYear - minYear.value} year${currentYear - minYear.value === 1 ? '' : 's'}`);
const years = ref([]);

const generateYearList = () => {
  const years_list = [];
  for (let year = currentYear; year >= minYear.value; year--) {
    years_list.push(`Year ${year}`);
  }
  const yearDifference = currentYear - minYear.value;
  for (let i = 1; i <= yearDifference; i++) {
    years_list.push(`Past ${i} Year${i > 1 ? 's' : ''}`);
  }
  years.value = years_list;
};

function filterByYear () {
    const trips = store.state.trips;
    if (selectedPeriod.value.startsWith('Year')) {
        const year = parseInt(selectedPeriod.value.split(' ')[1]);
        selectedTrips.value = trips.filter(trip => {
        const dateStr = trip.mission.start_date;
        const tripYear = new Date(dateStr).getFullYear();
        return tripYear === year;
        });
    }
    else if (selectedPeriod.value.startsWith('Past')) {
        const n = parseInt(selectedPeriod.value.split(' ')[1]);
        const startYear = currentYear - n;
        selectedTrips.value = trips.filter(trip => {
        const dateStr = trip.mission.start_date;
        const tripYear = new Date(dateStr).getFullYear();
        return tripYear >= startYear && tripYear <= currentYear;
        });
    }
    period.value = selectedPeriod.value
}

const employeesFootprints = computed(() => {
  const map = {}
  selectedTrips.value.forEach(trip => {
    const employee = trip.mission?.employee
    const id = employee.employee_id
    const name = `${employee.first_name} ${employee.last_name}`
    if (!map[id]) {
      map[id] = { key: name, footprint: 0 }
    }
    const footprint = parseFloat(trip.carbon_footprint) || 0
    map[id].footprint += footprint
  })
  return Object.values(map)
})

const statusFootprints = computed(() => {
  const statusFootprintMap = {}
  selectedTrips.value.forEach(trip => {
    const statusKey = trip.mission?.employee?.status.status_name
    if (!statusFootprintMap[statusKey]) {
      statusFootprintMap[statusKey] = { 
        key: statusKey, 
        footprint: 0 
      }
    }
    statusFootprintMap[statusKey].footprint += parseFloat(trip.carbon_footprint) || 0
  })
  return Object.values(statusFootprintMap)
})

const tripsFootprint = computed(() => {
  const tripFootprintMap = {}
  selectedTrips.value.forEach(trip => {
    const departureKey = `${trip.departure_city}, ${trip.departure_country}`
    const destinationKey = `${trip.destination_city}, ${trip.destination_country}`
    const key = `${departureKey} -> ${destinationKey}`
    if (!tripFootprintMap[key]) {
      tripFootprintMap[key] = { 
        key: key, 
        footprint: 0 
      }
    }
    tripFootprintMap[key].footprint += parseFloat(trip.carbon_footprint) || 0
  })
  return Object.values(tripFootprintMap)
})

const transportsFootprints = computed(() => {
  const transportFootprintMap = {}
  selectedTrips.value.forEach(trip => {
    const transportKey = trip.transport.transport_name
    if (!transportFootprintMap[transportKey]) {
      transportFootprintMap[transportKey] = { 
        key: transportKey, 
        footprint: 0 
      }
    }
    transportFootprintMap[transportKey].footprint += parseFloat(trip.carbon_footprint) || 0
  })
  return Object.values(transportFootprintMap)
})

const yearsFootprints = computed(() => {
  const missionFootprintMap = {}
  selectedTrips.value.forEach(trip => {
    const tripYear = new Date(trip.mission.start_date).getFullYear()
    if (tripYear >= minYear.value && tripYear <= currentYear) {
      if (!missionFootprintMap[tripYear]) {
        missionFootprintMap[tripYear] = {
          key: tripYear, 
          footprint: 0
        }
      }
      missionFootprintMap[tripYear].footprint += parseFloat(trip.carbon_footprint) || 0
    }
  })
  return Object.values(missionFootprintMap)
})

const barChartRef = ref(null)
let barChartInstance = null
const barChartType = ref('Transports')

const updateBarChartData = () => {
  let chartData = []
  let showXTicks = true
  const annotations = []
  switch (barChartType.value) {
    case 'Employees':
      chartData = employeesFootprints.value
      break
    case 'Trips':
      chartData = tripsFootprint.value
      showXTicks = false
      break
    case 'Transports':
      chartData = transportsFootprints.value
      break
    case 'Years':
      chartData = yearsFootprints.value
      annotations.push({
        type: 'line',
        yAxis: 1000,
        label: {
          show: true,
          formatter: '1t-CO2',
          position: 'insideStart',
          color: 'red',
          fontSize: 10,
        },
        lineStyle: {
          color: 'red',
          width: 2,
        },
      })
      break
  }
  const sortedData = chartData
    .map(item => ({ key: item.key, footprint: item.footprint }))
    .sort((a, b) => b.footprint - a.footprint)
  const labels = ['Total', ...sortedData.map(i => i.key)]
  const values = [parseFloat(totalFootprint.value), ...sortedData.map(i => i.footprint)]
  barChartInstance.setOption({
    yAxis: { data: labels },
    xAxis: { axisLabel: { show: showXTicks } },
    series: [{ data: values }],
    graphic: annotations,
  })
}

const pieChartRef = ref(null)
let pieChartInstance = null
const pieChartType = ref('Transports')

const updatePieChartData = () => {
  let pieData = []
  let palette = ["#440154","#482878","#3e4989","#31688e","#26828e","#1f9e89","#35b779","#6ece58","#b5de2b","#fde725"]
  switch (pieChartType.value) {
    case 'Employees':
      pieData = employeesFootprints.value
      break
    case 'Trips':
      pieData = tripsFootprint.value
      break
    case 'Transports':
      pieData = transportsFootprints.value
      break
    case 'Years':
      pieData = yearsFootprints.value
      break
    case 'Status':
      pieData = statusFootprints.value
      break
  }
  const formattedData = pieData.map(item => ({
    name: item.key,
    value: item.footprint,
  }))
  const legendLabels = formattedData.map(item => item.name);
  pieChartInstance.setOption({
    legend: {
      data: legendLabels,
    },
    series: [{ 
      data: formattedData, 
      itemStyle: {
        color: (params) => {
          return palette[params.dataIndex % palette.length]
        },
      }, 
    }],
  })
}

onMounted(async () => {
  generateYearList();
  barChartInstance = echarts.init(barChartRef.value)
  barChartInstance.setOption({
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    grid: { containLabel: true, top: 0, bottom: 50, left: 0, right: 110 },
    xAxis: { type: 'value', axisLabel: { fontSize: 10 } },
    yAxis: { type: 'category', data: [], axisLabel: { fontSize: 10 } },
    dataZoom: [
      { type: 'slider', 
        xAxisIndex: 0, 
        height: 15, 
        width: 350, 
        bottom: 20, 
        right: 100, 
        left: 80, 
        labelFormatter: value => `Footprint: ${value}`,
        textStyle: 
        {
          fontSize: 10,
          color: '#333'
        } 
      }, 
      { type: 'slider', 
        yAxisIndex: 0, 
        width: 15, 
        height: 230, 
        right: 40, 
        labelFormatter: function (index) {
          const axisData = barChartInstance.getOption().yAxis[0].data;
          return `Category: ${axisData[index]}`;
        },
        textStyle: 
        {
          fontSize: 10,
          color: '#333'
        }  
      }
    ],
    series: [{
      type: 'bar',
      data: [],
      barWidth: '50%',
      itemStyle: {
        color: '#3498db',
        borderColor: '#2980b9',
        borderWidth: 1
      }
    }]
  })
  updateBarChartData()
  window.addEventListener('resize', () => {
    barChartInstance.resize()
  })
  pieChartInstance = echarts.init(pieChartRef.value)
  pieChartInstance.setOption({
    tooltip: {
      trigger: 'item',
      formatter: (params) => `${params.name}: ${params.percent}%`
    },
    legend: {
      show: true,
      orient: 'vertical',
      type: 'scroll',
      right: 0,
      selectMode: 'multiple',
    },
    series: [
      {
        type: 'pie',
        radius: '80%',
        left: 0,
        center: ['20%', '50%'],
        data: [],
        label: { show: false },
        emphasis: { show: false },
      }
    ]
  })
  updatePieChartData()
  window.addEventListener('resize', () => {
    pieChartInstance.resize()
  })
})

onBeforeUnmount(() => {
  if (barChartInstance) {
    barChartInstance.dispose()
    barChartInstance = null
  }
  if (pieChartInstance) {
    pieChartInstance.dispose()
    pieChartInstance = null
  }
})

watch(barChartType, () => {
  updateBarChartData()
})

watch(pieChartType, () => {
  updatePieChartData()
})

watch(selectedTrips, () => {
  updateBarChartData();
  updatePieChartData();
});

const deleteTrip = async (trip_id) => {
  try {
    await fetchToken();
    const access = store.state.accessToken;
    await services.trips.destroy(access, trip_id);
    const response = await services.trips.list(access);
    store.setItem('trips', response.trips);
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

watch(
  () => store.state.trips,
  (newTrips) => {
    selectedTrips.value = newTrips
  },
  { immediate: true, deep: true }
)

const searchword = ref('')

function normalizeString(str) {
  if (!str) return ''
  return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase()
}

const filteredTrips = computed(() => {
  if (!searchword.value) return selectedTrips.value
  const term = normalizeString(searchword.value)
  return selectedTrips.value.filter(trip => {
    const fields = [
      trip.mission?.start_date.toString(),
      trip.mission?.end_date.toString(),
      trip.mission?.mission_desc,
      trip.departure_city,
      trip.departure_country,
      trip.destination_city,
      trip.destination_country,
      trip.transport?.transport_name,
      `${trip.mission?.employee?.first_name} ${trip.mission?.employee?.last_name}`,
      trip.carbon_footprint?.toString(),
    ]
    return fields.some(field => normalizeString(field).includes(term))
  })
})
</script>

<style scoped>
.chart-container {
  width: 100%;
}
.bar-container {
  height: 300px;
  width: 100%;
}
.pie-container {
  height: 150px;
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