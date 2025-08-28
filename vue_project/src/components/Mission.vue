<template>
    <nav class="navbar mb-5">
      <div class="navbar-start">
        <div class="navbar-item">
          <h1 class="title is-5 has-text-weight-semibold">Analytics</h1>
        </div>
      </div>
      <div class="navbar-menu is-active">
        <div class="navbar-end">
          <!-- Year filter -->
          <div class="field is-grouped navbar-item">
            <input
              class="input is-small"
              list="year-list"
              v-model="selectedYear"
              placeholder="Select year"
              @keydown.enter="applyYearFilter"
            />
            <datalist id="year-list">
              <option v-for="year in years" :key="year" :value="year" />
            </datalist>
            <button class="button is-link is-small" @click="applyYearFilter">Filter</button>
          </div>
        </div>
      </div>
    </nav>

    <div class="columns is-multiline">

      <div class="column is-3 mb-4">
        <div class="card">
          <div class="card-content is-flex is-flex-direction-column p-5">
            <span class="is-size-7 mb-3 has-text-link has-text-weight-semibold">Carbon Emission</span>
            <span class="has-text-weight-semibold is-size-5 mb-3">{{ totalFootprint }} kg</span>
          </div>
        </div>
      </div>

      <div class="column is-2 mb-4"></div>

      <div class="column is-7 mb-4">
        <div class="card">
          <div class="card-content is-flex is-flex-direction-column p-5">
            <span class="is-size-7 mb-3 has-text-link has-text-weight-semibold">Carbon Line per year</span>
            <div class="chart-container line-container" ref="lineChartRef"></div>
          </div>
        </div>
      </div>

      <div class="column is-5 mb-4">
        <div class="card">
          <div class="card-content is-flex is-flex-direction-column p-5">
            <select v-model="pieChartType" class="select is-small mb-3">
              <option v-for="option in chartOptions" :key="option" :value="option">{{ option }}</option>
            </select>
            <span class="is-size-7 mb-3 has-text-link has-text-weight-semibold">Carbon Pie per {{ pieChartType }}</span>
            <div class="chart-container pie-container" ref="pieChartRef"></div>
          </div>
        </div>
      </div>

      <div class="column is-7 mb-4">
        <div class="card">
          <div class="card-content is-flex is-flex-direction-column p-5">
            <select v-model="barChartType" class="select is-small mb-3">
              <option v-for="option in chartOptions" :key="option" :value="option">{{ option }}</option>
            </select>
            <span class="is-size-7 mb-3 has-text-link has-text-weight-semibold">Carbon Bar per {{ barChartType }}</span>
            <div class="chart-container bar-container" ref="barChartRef"></div>
          </div>
        </div>
      </div>

      <div class="column is-12 mb-4">
        <div class="card">
          <div class="card-content p-5">
            <div class="columns is-vcentered is-mobile mb-3">
              
              <div class="column is-5">
                <!-- Search box -->
                <div class="field is-grouped">
                  <input
                    v-model="searchInput"
                    class="input is-small"
                    type="search"
                    placeholder="Enter search keyword"
                    autocomplete="off"
                  />
                  <div class="select is-small is-fullwidth">
                    <select v-model="searchColumn">
                      <option value="" selected>Search field</option>
                      <option value="employee_name">Employee Name</option>
                      <option value="mission_adm_num">Mission Num</option>
                      <option value="mission_desc">Mission Description</option>
                      <option value="transport">Transport</option>
                      <option value="departure">Departure</option>
                      <option value="destination">Destination</option>
                    </select>
                  </div>
                  <button @click="applySearch" class="button is-small is-info"><i class="fas fa-search"></i></button>
                </div>
              </div>

              <div class="column is-4"></div>

              <div class="column is-2">
                <div class="select is-small is-fullwidth">
                  <select v-model="sortInput">
                    <option value="" disabled>Sort by</option>
                    <option value="employee_asc">Employee Name (ASC)</option>
                    <option value="employee_desc">Employee Name (DESC)</option>
                    <option value="mission_asc">Mission Num (ASC)</option>
                    <option value="mission_desc">Mission Num (DESC)</option>
                    <option value="footprint_asc">Carbon Footprint (ASC)</option>
                    <option value="footprint_desc">Carbon Footprint (DESC)</option>
                  </select>
                </div>
              </div>

              <div class="column is-1 has-tooltip" data-tooltip="Export to CSV">
                <button class="button is-secondary is-small is-fullwidth" @click="exportData">
                  <span class="icon is-small">
                    <i class="fa-solid fa-arrow-up-from-bracket"></i>
                  </span>
                </button>
              </div>
            </div>

            <div class="table-wrapper">
              <TreeTable
                class="table is-fullwidth is-striped is-hoverable compact-table"
                :columns="tableColumns"
                :table-data="sortedData"
                children-key="children"
                :expand-all="false"
              >
                <template #headerTemplate>
                  <tr class="row header">
                    <th v-for="column in tableColumns" :key="column.label">
                      {{ column.label }}
                    </th>
                  </tr>
                </template>
                <template #nodeTemplate="{ rowData }">
                  <tr
                    class="row"
                    :class="{ 
                      'has-error': rowData.hasError,
                      'disabled-row': rowData.isValid 
                    }"
                  >
                    <td class="cell">
                      <span
                        class="icon is-small"
                        style="cursor: pointer; user-select:none;"
                        @click="() => { rowData._expanded = !rowData._expanded }"
                        title="Expand/Collapse"
                      >
                        <i :class="rowData._expanded ? 'fas fa-caret-down' : 'fas fa-caret-right'"></i>
                      </span>
                    </td>
                    <td class="cell">
                      <template v-if="editedMission[rowData.mission_adm_num]">
                        <input
                          v-model="editedMission[rowData.mission_adm_num].mission_adm_num"
                          class="input is-small"
                          placeholder="Adm Num"
                        />
                      </template>
                      <template v-else>
                        {{ rowData.mission_adm_num }}
                      </template>
                    </td>
                    <td class="cell">
                      <template v-if="editedMission[rowData.mission_adm_num]">
                        <DatePicker
                          v-model:value="editedMission[rowData.mission_adm_num].selectedDateRange"
                          range
                          type="date"
                          format="YYYY-MM-DD"
                          separator=" To "
                          value-type="format"
                          placeholder="Select dates"
                          :clearable="true"
                          :append-to-body="true"
                          popup-class="custom-datepicker-popup"
                        />
                      </template>
                      <template v-else>
                        {{ rowData.dates }}
                      </template>
                    </td>
                    <td class="cell">
                      <template v-if="editedMission[rowData.mission_adm_num]">
                        <input
                          v-model="editedMission[rowData.mission_adm_num].mission_desc"
                          class="input is-small"
                          placeholder="Description"
                        />
                      </template>
                      <template v-else>
                        {{ rowData.mission_desc }}
                      </template>
                    </td>
                    <td class="cell">
                      <template v-if="editedMission[rowData.mission_adm_num]">
                        <input
                          v-model="editedMission[rowData.mission_adm_num].employee_name"
                          class="input is-small"
                          placeholder="Employee"
                          list="employees-list"
                        />
                        <datalist id="employees-list">
                          <option
                            v-for="emp in rawData.employees"
                            :key="emp.employee_id"
                            :value="`${emp.first_name} ${emp.last_name} - ${emp.employee_adm_num}`"
                          />
                        </datalist>
                        <button class="button is-text is-small has-text-link" @click="openEmployeeModal(null, 'add')">
                          New Employee
                        </button>
                      </template>
                      <template v-else>
                        {{ rowData.employee_name }}
                      </template>
                    </td>
                    <td class="cell"></td>
                    <td class="cell"></td>
                    <td class="cell"></td>
                    <td class="cell"></td>
                    <td class="cell"></td>
                    <td class="cell"></td>
                    <td class="cell">{{ rowData.carbon_footprint }}  kg co2</td>
                    <td class="cell">
                      <template v-if="editedMission[rowData.mission_adm_num]">
                        <button
                          class="button is-small is-secondary is-light"
                          @click="submitEditMission(rowData.mission_adm_num)"
                          v-if="!rowData.hasError"
                          title="Save"
                          style="font-weight: bold; padding: 0 6px;"
                        >
                          <span class="icon is-small"><i class="fas fa-check"></i></span>
                        </button>
                        <button
                          class="button is-small is-light is-secondary"
                          @click="cancelEditMission(rowData.mission_adm_num)"
                          title="Cancel"
                          v-if="!rowData.hasError"
                          style="font-weight: bold; padding: 0 6px;"
                        >
                          <span class="icon is-small"><i class="fas fa-times"></i></span>
                        </button>
                        <button
                          class="button is-small is-secondary is-light"
                          @click="submitCorrectMission(rowData.mission_adm_num)"
                          v-if="rowData.hasError && !rowData.isValid"
                          title="Save correction"
                          style="font-weight: bold; padding: 0 6px;"
                        >
                          <span class="icon is-small"><i class="fas fa-check"></i></span>
                        </button>
                      </template>
                      <template v-else>
                        <button
                          v-if="isManager && !rowData.hasError"
                          class="button is-small is-link is-light"
                          @click.stop="addTrip(rowData.mission_adm_num)"
                          title="Add trip"
                          style="font-weight: bold; padding: 0 6px;"
                        >
                          <span class="icon is-small">
                            <i class="fas fa-plus"></i>
                          </span>
                        </button>
                        <button
                          v-if="isManager && !rowData.hasError"
                          class="button is-link is-light is-small"
                          @click="editMission(rowData)"
                          title="Edit mission"
                          style="font-weight: bold; padding: 0 6px;"
                        >
                          <span class="icon is-small"><i class="fas fa-pencil-alt"></i></span>
                        </button>
                        <button
                          v-if="isManager && !rowData.hasError"
                          class="button is-small is-danger is-light"
                          @click.stop="deleteMission(rowData.mission_id)"
                          title="Delete mission"
                          style="font-weight: bold; padding: 0 6px;"
                        >
                          <span class="icon is-small"><i class="fas fa-times"></i></span>
                        </button>
                      </template>
                    </td>
                  </tr>
                  <tr
                    :class="{ 
                      'has-error': rowData.hasError,
                      'disabled-row': rowData.isValid 
                    }"
                    v-for="(child, index) in rowData.children" 
                    v-if="rowData._expanded" 
                    :key="index" 
                    class="row child-row"
                  >
                    <td class="cell"></td>
                    <td class="cell"></td>
                    <td class="cell"></td>
                    <td class="cell"></td>
                    <td class="cell"></td>
                    <td class="cell"></td>
                    <td class="cell">
                      <template v-if="editingTripId[`${rowData.mission_adm_num}_${index}`]">
                        <input
                          v-model="editedTrip[`${rowData.mission_adm_num}_${index}`].departure"
                          class="input is-small"
                          @input="debouncedUpdateDepartureCityList(editedTrip[`${rowData.mission_adm_num}_${index}`].departure)"
                          placeholder="City"
                          list="departure-cities-list"
                        />
                        <datalist id="departure-cities-list">
                          <option
                            v-for="city in departureCities"
                            :key="city.id"
                            :value="`${city.name}, ${city.countryCode}`"
                          />
                        </datalist>
                      </template>
                      <template v-else>
                        {{ child.departure }}
                      </template>
                    </td>
                    <td class="cell">
                      <template v-if="editingTripId[`${rowData.mission_adm_num}_${index}`]">
                        <input
                          v-model="editedTrip[`${rowData.mission_adm_num}_${index}`].destination"
                          @input="debouncedUpdateDestinationCityList(editedTrip[`${rowData.mission_adm_num}_${index}`].destination)"
                          class="input is-small"
                          placeholder="City"
                          list="destination-cities-list"
                        />
                        <datalist id="destination-cities-list">
                          <option
                            v-for="city in destinationCities"
                            :key="city.id"
                            :value="`${city.name}, ${city.countryCode}`"
                          />
                        </datalist>
                      </template>
                      <template v-else>
                        {{ child.destination }}
                      </template>
                    </td>
                    <td class="cell">
                      <template v-if="editingTripId[`${rowData.mission_adm_num}_${index}`]">
                        <input
                          v-model="editedTrip[`${rowData.mission_adm_num}_${index}`].transport"
                          class="input is-small"
                          placeholder="Transport"
                          list="transports-list"
                        />
                        <datalist id="transports-list">
                          <option
                            v-for="t in rawData.transports"
                            :key="t.transport_name"
                            :value="t.transport_name"
                          />
                        </datalist>
                      </template>
                      <template v-else>
                        {{ child.transport }}
                      </template>
                    </td>
                    <td class="cell">
                      <template v-if="editingTripId[`${rowData.mission_adm_num}_${index}`]">
                        <input
                          v-model="editedTrip[`${rowData.mission_adm_num}_${index}`].carpooling"
                          type="number" 
                          min="1"
                          class="input is-small"
                        />
                      </template>
                      <template v-else>
                        {{ child.carpooling }}
                      </template>
                    </td>
                    <td class="cell">
                      <template v-if="editingTripId[`${rowData.mission_adm_num}_${index}`]">
                        <input
                          v-model="editedTrip[`${rowData.mission_adm_num}_${index}`].is_round_trip"
                          type="checkbox"
                        />
                      </template>
                      <template v-else>
                        {{ child.is_round_trip ? 'x' : '' }}
                      </template>
                    </td>
                    <td class="cell">{{ child.carbon_footprint }} kg co2</td>
                    <td class="cell">
                      <template v-if="editingTripId[`${rowData.mission_adm_num}_${index}`]">
                        <button
                          class="button is-small is-secondary is-light"
                          @click="submitEditTrip(rowData.mission_adm_num, index, child.trip_id)"
                          v-if="!rowData.hasError"
                          title="Save"
                          style="font-weight: bold; padding: 0 6px;"
                        >
                          <span class="icon is-small"><i class="fas fa-check"></i></span>
                        </button>
                        <button
                          class="button is-small is-light is-secondary"
                          @click="cancelEditTrip(rowData.mission_adm_num, index)"
                          title="Cancel"
                          v-if="!rowData.hasError"
                          style="font-weight: bold; padding: 0 6px;"
                        >
                          <span class="icon is-small"><i class="fas fa-times"></i></span>
                        </button>
                      </template>
                      <template v-else>
                        <button
                          v-if="isManager && !rowData.hasError"
                          class="button is-link is-light is-small"
                          @click="editTrip(child, rowData.mission_adm_num, index)"
                          title="Edit trip"
                          style="font-weight: bold; padding: 0 6px;"
                        >
                          <span class="icon is-small"><i class="fas fa-pencil-alt"></i></span>
                        </button>
                        <button
                          v-if="isManager && !rowData.hasError"
                          class="button is-small is-danger is-light"
                          @click.stop="deleteTrip(child.trip_id, rowData.mission_adm_num, index)"
                          title="Delete trip"
                          style="font-weight: bold; padding: 0 6px;"
                        >
                          <span class="icon is-small"><i class="fas fa-times"></i></span>
                        </button>
                      </template>
                    </td>
                  </tr>
                </template>
              </TreeTable>
            </div>

            <div class="columns is-vcentered is-mobile mb-3">
              <div class="column is-6">
                <button
                  v-if="isManager"
                  class="button is-info is-small is-fullwidth"
                  @click="triggerImport"
                >
                  <span class="icon is-small"><i class="fa-solid fa-arrow-down"></i></span>
                  <span>Import Missions</span>
                </button>
                <input
                  ref="fileInput"
                  type="file"
                  accept=".csv,text/csv"
                  style="display: none"
                  @change="handleFile"
                />
              </div>
              
              <div class="column is-6">
                <button
                  v-if="isManager"
                  class="button is-info is-small is-fullwidth"
                  @click="openMissionModal"
                >
                  <span class="icon is-small"><i class="fas fa-plus"></i></span>
                  <span>Create Mission</span>
                </button>
              </div>
            </div>
          </div>

          <div class="modal" :class="{ 'is-active': missionModalActive }">
            <div class="modal-background" @click="closeMissionModal"></div>
            <div class="modal-card">
              <header class="modal-card-head">
                <p class="modal-card-title">Create New Mission</p>
                <button class="delete" aria-label="close" @click="closeMissionModal"></button>
              </header>
              <section class="modal-card-body">
                <MissionForm
                  @submitted="handleMissionSubmit"
                />
              </section>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="modal" :class="{ 'is-active': isEmployeeModalActive }">
      <div class="modal-background" @click="closeEmployeeModal"></div>
      <div class="modal-card">
        <header class="modal-card-head">
          <p class="modal-card-title">{{ operationProps === 'edit' ? 'Edit Employee' : 'New Employee' }}</p>
          <button class="delete" aria-label="close" @click="closeEmployeeModal"></button>
        </header>
        <section class="modal-card-body">
          <EmployeeForm
            v-if="operationProps"
            :employee="employeeProps"
            :operation="operationProps"
            @updated="handleEmployeeUpdated"
            @cancelled="closeEmployeeModal"
          />
        </section>
      </div>
    </div>
</template>

<script setup>
import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'
import TreeTable from 'vue-tree-table-component'
import DatePicker from 'vue-datepicker-next'
import * as echarts from 'echarts/core'
import debounce from 'lodash/debounce';
import cloneDeep from 'lodash/cloneDeep';
import { LineChart, PieChart, BarChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DataZoomComponent,
  GraphicComponent,
  MarkLineComponent
} from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { fetchToken, getData, getPermission, setData, getUser } from '@/composables/session'
import Papa from 'papaparse'
import MissionForm from '@/components/MissionForm.vue'
import EmployeeForm from "@/components/EmployeeForm.vue";
import services from '@/composables/services'

echarts.use([
  TitleComponent,
  TooltipComponent,
  LegendComponent,
  GridComponent,
  DataZoomComponent,
  GraphicComponent,
  LineChart,
  PieChart,
  BarChart,
  CanvasRenderer,
  MarkLineComponent
])

const selectedYear = ref('All years')
const appliedYear = ref('All years')
const rawData = ref(null)
const workingData = ref([])
const displayData = ref([])
const sortedData = ref([])
const searchInput = ref('')
const searchColumn = ref('')
const sortInput = ref('')
const lineChartRef = ref(null)
const pieChartRef = ref(null)
const barChartRef = ref(null)
let lineChartInstance = null
let pieChartInstance = null
let barChartInstance = null
const chartOptions = ['mission', 'employee', 'status', 'transport', 'trip']
const pieChartType = ref(chartOptions[0])
const barChartType = ref(chartOptions[0])
const { isManager, isAdmin, isStandard } = getPermission()
const missionModalActive = ref(false)
const editingTripId = ref({})
const editedTrip = ref({})
const editedMission = ref({})
const departureCities = ref([])
const destinationCities = ref([])
const selectedMissionAdmNum = ref(null);
const fileInput = ref(null);
const MAX_FILE_SIZE = 2 * 1024 * 1024;
const isEmployeeModalActive = ref(false);
const employeeProps = ref(null);
const operationProps = ref(null);

const FILE_HEADER = computed(() => ({
  "Numéro mission": "num",
  "Date de départ": "start",
  "Date de retour": "end",
  "Motif du déplacement": "desc",
  "Pays de départ": "fromCountry",
  "Ville de départ": "fromCity",
  "Pays de destination": "toCountry",
  "Ville de destination": "toCity",
  "Moyens de transport": "transport",
  "Aller / Retour": "round",
  "Statut agent": "status",
  "Nb de pers. dans la voiture": "carpool",
  "Missionnaire": "empNum"
}))

const tableColumns = computed(() => [
  { id: 'mission_id', label: '' },
  { id: 'mission_adm_num', label: 'Adm Num' },
  { id: 'dates', label: 'Dates' },
  { id: 'mission_desc', label: 'Description' },
  { id: 'employee_name', label: 'Employee' },
  { id: 'trip_id', label: '' },
  { id: 'departure', label: 'Departure' },
  { id: 'destination', label: 'Destination' },
  { id: 'transport', label: 'Mode' },
  { id: 'carpooling', label: 'Carpool' },
  { id: 'is_round_trip', label: 'Round Trip' },
  { id: 'carbon_footprint', label: 'Carbon Value' },
  { label: '', id: 'actions' },
])

const years = computed(() => {
  if (!rawData.value?.missions) return ['All years']
  const yearSet = new Set(
    rawData.value.missions
      .filter(m => m.start_date)
      .map(m => new Date(m.start_date).getFullYear())
  )
  return ['All years', ...Array.from(yearSet).sort((a, b) => a - b)]
})

onMounted(() => {
  const initialData = getData()
  if (initialData) {
    rawData.value = initialData
  }
})

watch(() => getData(), (data) => {
  if (data) {
    rawData.value = data
  }
})

const applyYearFilter = () => {
  appliedYear.value = selectedYear.value || 'All years'
}

const buildTable = (missions) => {
  const { trips = [], employees = [] } = rawData.value || {}
  const missionFields = ['mission_id', 'mission_adm_num', 'dates', 'mission_desc']
  const tripFields = ['trip_id', 'departure', 'destination', 'transport', 'carpooling', 'is_round_trip', 'carbon_footprint']
  return missions.map(mission => {
    let emp = {}
    if (isManager.value) {
      emp = employees.find(e => e.employee_id === mission.employee)
    } else if (isStandard.value) {
      emp = getUser().employee
    }
    const missionTrips = trips.filter(t => t.mission === mission.mission_id)
    const totalCarbon = missionTrips.reduce((sum, t) => sum + (parseFloat(t.carbon_footprint) || 0), 0)
    return {
      ...Object.fromEntries(missionFields.map(k => [k, mission[k]])),
      dates: `${mission.start_date || ''} To ${mission.end_date || ''}`,
      employee_name: `${emp.first_name || ''} ${emp.last_name || ''} - ${emp.employee_adm_num || ''}`.trim(),
      employee_status: emp.status,
      carbon_footprint: totalCarbon.toFixed(2),
      children: missionTrips.map(trip => {
        const enrichedTrip = {
          ...trip,
          departure: `${trip.departure_city || ''}, ${trip.departure_country || ''}`,
          destination: `${trip.destination_city || ''}, ${trip.destination_country || ''}`
        }
        return Object.fromEntries(tripFields.map(k => [k, enrichedTrip[k]]))
      })
    }
  })
}

watch([rawData, appliedYear], () => {
  if (!rawData.value || !Array.isArray(rawData.value.missions)) return
  const filtered =
    appliedYear.value === 'All years'
      ? rawData.value.missions
      : rawData.value.missions.filter(m => new Date(m.start_date).getFullYear() === Number(appliedYear.value))
  workingData.value = buildTable(filtered || [])
}, { immediate: true })

watch(workingData, () => {
  displayData.value = workingData.value
  sortedData.value = workingData.value
  sortInput.value = ''
})

const filterBySearch = (data, term, column) => {
  if (!term) return data
  const lowerTerm = term.toLowerCase()
  return data
    .map(mission => {
      let match = false
      let filteredChildren = []
      const missionFields = ['mission_adm_num', 'mission_desc', 'employee_name']
      const tripFields = ['transport', 'departure', 'destination']
      if (!column || missionFields.includes(column)) {
        const fields = column ? [column] : missionFields
        match = fields.some(f => mission[f]?.toString().toLowerCase().includes(lowerTerm))
      }
      if (!match && (!column || tripFields.includes(column))) {
        const fields = column ? [column] : tripFields
        filteredChildren = (mission.children || []).filter(trip =>
          fields.some(f => trip[f]?.toString().toLowerCase().includes(lowerTerm))
        )
        match = filteredChildren.length > 0
      }
      return match
        ? { ...mission, children: filteredChildren.length ? filteredChildren : mission.children }
        : null
    })
    .filter(Boolean)
}

const sortData = data => {
  if (!sortInput.value) return data;
  const [field, direction] = sortInput.value.split('_');
  const dir = direction === 'asc' ? 1 : -1;
  return [...data].sort((a, b) => {
    let valA, valB;
    if (field === 'employee') {
      valA = a.employee_name.toLowerCase();
      valB = b.employee_name.toLowerCase();
      if (valA < valB) return -1 * dir;
      if (valA > valB) return 1 * dir;
      return 0;
    } else if (field === 'mission') {
      valA = a.mission_adm_num;
      valB = b.mission_adm_num;
      return valA.localeCompare(valB, undefined, { numeric: true }) * dir;
    } else if (field === 'footprint') {
      valA = parseFloat(a.carbon_footprint) || 0;
      valB = parseFloat(b.carbon_footprint) || 0;
      if (valA < valB) return -1 * dir;
      if (valA > valB) return 1 * dir;
      return 0;
    }
    return 0;
  });
};

const applySearch = () => {
  const term = searchInput.value.trim()
  const column = searchColumn.value
  const filtered = filterBySearch(workingData.value, term, column)
  displayData.value = filtered
  sortedData.value = filtered
}

watch(sortInput, () => {
  sortedData.value = sortData(displayData.value)
}, { immediate: false })

const totalFootprint = computed(() => {
  return workingData.value.reduce((sum, mission) => {
    const footprint = parseFloat(mission.carbon_footprint) || 0
    return sum + footprint
  }, 0).toFixed(2)
})

const footprintByYear = computed(() => {
  if (!Array.isArray(workingData.value)) return {}
  const map = {}
  workingData.value.forEach(mission => {
    const year = mission.dates.split(' To ')[0] ? new Date(mission.dates.split(' To ')[0]).getFullYear() : null
    if (!year) return
    const footprint = parseFloat(mission.carbon_footprint) || 0
    map[year] = (map[year] || 0) + footprint
  })
  Object.keys(map).forEach(year => {
    map[year] = map[year].toFixed(2)
  })
  return map
})

const lineChartOptions = computed(() => {
  const dataObj = footprintByYear.value
  const data = Object.entries(dataObj)
    .map(([year, footprint]) => ({
      name: year,
      value: parseFloat(footprint)
    }))
    .sort((a, b) => a.name - b.name)
  return {
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: data.map(d => d.name), boundaryGap: false },
    yAxis: { type: 'value', name: 'kg CO2' },
    series: [
      {
        type: 'line',
        smooth: false,
        data: data.map(d => d.value),
        lineStyle: { width: 3 },
        areaStyle: { color: 'rgba(59, 130, 246, 0.2)' },
        itemStyle: { color: '#1e40af' }
      }
    ]
  }
})

function aggregateData(type) {
  if (!displayData.value.length) return []
  const map = new Map()
  displayData.value.forEach(mission => {
    if (type === 'transport') {
      mission.children?.forEach(trip => {
        const transportType = trip.transport
        const val = parseFloat(trip.carbon_footprint) || 0
        map.set(transportType, (map.get(transportType) || 0) + val)
      })
    } else if (type === 'trip') {
      mission.children?.forEach(trip => {
        const key = `${trip.departure} -> ${trip.destination}`;
        const val = parseFloat(trip.carbon_footprint) || 0;
        map.set(key, (map.get(key) || 0) + val);
      });
    } else {
      let key = ''
      switch (type) {
        case 'mission':
          key = mission.mission_adm_num
          break
        case 'employee':
          key = mission.employee_name
          break
        case 'status':
          key = mission.employee_status
          break
        default:
          key = 'mission'
      }
      const val = parseFloat(mission.carbon_footprint) || 0
      map.set(key, (map.get(key) || 0) + val)
    }
  })
  return Array.from(map.entries()).map(([name, value]) => ({
    name,
    value: Number(value.toFixed(2))
  }))
}

function updatePieChart() {
  if (!displayData.value.length || !pieChartInstance) return
  pieChartInstance.setOption({
    tooltip: { trigger: 'item' },
    legend: { show: false },
    series: [{
      name: 'Carbon Footprint',
      type: 'pie',
      radius: '60%',
      data: aggregateData(pieChartType.value),
      emphasis: { itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0,0,0,0.5)' } }
    }]
  })
}

function updateBarChart() {
  if (!displayData.value.length || !barChartInstance) return
  const barData = aggregateData(barChartType.value)
  const seriesConfig = {
    type: 'bar',
    data: barData.map(i => i.value),
    itemStyle: { color: '#3b82f6' },
    barMaxWidth: 10
  };
  if (barChartType.value === 'employee') {
    seriesConfig.markLine = {
      silent: true,
      symbol: 'none',
      data: [
        {
          yAxis: appliedYear.value === 'All years'
            ? 1000 * (years.value.length - 1)
            : 1000,
          name: appliedYear.value === 'All years'
            ? `1 tonne × ${years.value.length - 1}`
            : '1 tonne',
          lineStyle: { color: 'red', type: 'dashed', width: 2 },
          label: {
            show: true,
            formatter: appliedYear.value === 'All years'
              ? `1 tonne × ${years.value.length - 1}`
              : '1 tonne',
            color: 'red',
            position: 'end'
          }
        }
      ]
    };
  }
  barChartInstance.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: { 
     type: 'category', 
     data: barData.map(i => i.name), 
     // axisLabel: { rotate: 30 } ,
     axisLabel: {
        show: false
      },
    },
    yAxis: { type: 'value', name: 'kg CO2' },
    series: [seriesConfig]
  })
}

watch([displayData, pieChartType], () => {
  updatePieChart()
}, { immediate: true })

watch([displayData, barChartType], () => {
  updateBarChart()
}, { immediate: true })

onMounted(() => {
  if (lineChartRef.value) {
    lineChartInstance = echarts.init(lineChartRef.value)
  }
  if (pieChartRef.value) {
    pieChartInstance = echarts.init(pieChartRef.value)
  }
  if (barChartRef.value) {
    barChartInstance = echarts.init(barChartRef.value)
  }
})

window.addEventListener('resize', () => {
  lineChartInstance?.resize()
  pieChartInstance?.resize()
  barChartInstance?.resize()
})

onBeforeUnmount(() => {
  window.removeEventListener('resize', () => {
    lineChartInstance?.resize()
    pieChartInstance?.resize()
    barChartInstance?.resize()
  })
})

watch(lineChartOptions, newOptions => {
  if (lineChartInstance) {
    lineChartInstance.setOption(newOptions)
  }
}, { immediate: true })

function escapeCSVField(field) {
  const value = String(field ?? '');
  const needsEscape = /^[=+\-@]/.test(value);
  const safeValue = needsEscape ? `'${value}` : value;
  return `"${safeValue.replace(/"/g, '""')}"`;
}

function exportData() {
  const header = [
    'Row', 'Mission', 'Start Date', 'End Date', 'Travel Purpose',
    'Departure City', 'Departure Country', 'Destination City', 'Destination Country',
    'Mode of Transport', 'Carpooling', 'IsRoundTrip',
    'Agent Position', 'Agent Name', 'Carbon Footprint'
  ];

  let rowIndex = 0;
  const rows = [];

  workingData.value.forEach(mission => {
    const dates = (mission.dates || '').split(' To ');
    const startDate = dates[0] || '';
    const endDate = dates[1] || '';

    if (mission.children && mission.children.length > 0) {
      mission.children.forEach(child => {
        const departure = (child.departure || '').split(', ');
        const destination = (child.destination || '').split(', ');

        rowIndex++;
        rows.push({
          'Row': rowIndex,
          'Mission': mission.mission_adm_num,
          'Start Date': startDate,
          'End Date': endDate,
          'Travel Purpose': mission.mission_desc,
          'Departure City': departure[0],
          'Departure Country': departure[1],
          'Destination City': destination[0],
          'Destination Country': destination[1],
          'Mode of Transport': child.transport,
          'Carpooling': child.carpooling,
          'IsRoundTrip': child.is_round_trip ? 'Yes' : 'No',
          'Agent Position': mission.employee_status,
          'Agent Name': mission.employee_name,
          'Carbon Footprint': child.carbon_footprint
        });
      });
    }
  });

  exportToCSV(header, rows);
}

function exportToCSV(header, rows) {
  const csvRows = [
    header.map(escapeCSVField).join(';'),
    ...rows.map(row =>
      header.map(field => escapeCSVField(row[field])).join(';')
    )
  ];
  const csvContent = csvRows.join('\r\n');
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const link = document.createElement('a');
  link.href = URL.createObjectURL(blob);
  link.setAttribute('download', 'missions.csv');
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
}

function openMissionModal() {
  missionModalActive.value = true
}

function closeMissionModal() {
  missionModalActive.value = false
}

async function handleMissionSubmit() {
  const token = await fetchToken();
  const missions = await services.missions.list(token);
  const trips = await services.trips.list(token);
  rawData.value = { ...rawData.value, trips, missions }
  setTimeout(() => {
    setData(rawData.value)
    getData()
    alert('Mission submitted successfully.');
  }, 100);
  closeMissionModal()
}

function addTrip(admNum) {
  const index = displayData.value.findIndex(m => m.mission_adm_num === admNum);
  if (index !== -1) {
    const current = displayData.value[index];
    const childIndex = current.children.length;
    const trip = {
      'departure': '',
      'destination': '',
      'transport': '',
      'carpooling': 1,
      'is_round_trip': false,
      'carbon_footprint': 0,
    };
    displayData.value[index] = {
      ...current,
      children: [...current.children, trip],
    };
    editTrip(trip, admNum, childIndex)
  }
}

async function deleteTrip(tripId, missionNum, childIdx) {
  if (!confirm('Are you sure you want to delete this trip?')) return;
  try {
    const token = await fetchToken();
    if (tripId != null) {
      await services.trips.destroy(token, tripId);
      const resp = await services.trips.list(token);
      rawData.value = { ...rawData.value, trips: resp };
      setTimeout(() => {
        setData(rawData.value);
        getData();
        alert("Trip deleted successfully!");
      }, 100);
    } else {
      const missionIndex = displayData.value.findIndex(
        (m) => m.mission_adm_num === missionNum
      );
      displayData.value[missionIndex].children.splice(childIdx, 1);
      alert("Trip removed locally!");
    }
  } catch (e) {
    alert(`Failed to remove trip. See console for details.`);
    console.error(e);
  }
}

async function deleteMission(missionId) {
  if (!confirm('Are you sure you want to delete this mission?')) return;
  try {
    const token = await fetchToken();
    const missionEntry = workingData.value.find(m => m.mission_id === missionId);
    const tripDeletions = (missionEntry.children || []).map(trip =>
      services.trips.destroy(token, trip.trip_id)
    );
    await Promise.all(tripDeletions);
    await services.missions.destroy(token, missionId);
    const [respTrips, respMissions] = await Promise.all([
      services.trips.list(token),
      services.missions.list(token)
    ]);
    rawData.value = { ...rawData.value, trips: respTrips, missions: respMissions };
    setTimeout(() => {
      setData(rawData.value)
      getData()
      alert('Mission deleted successfully.');
    }, 100);
  } catch (e) {
    console.error(e);
    alert('Failed to delete mission. See console for details.');
  }
}

async function submitEditTrip(missionNum, index, tripId) {
  const key = `${missionNum}_${index}`
  const trip = editedTrip.value[key]
  const payload = {
    'fromCity': trip.departure.split(', ')[0] || '',
    'fromCountry': trip.departure.split(', ')[1] || '',
    'toCity': trip.destination.split(', ')[0] || '',
    'toCountry': trip.destination.split(', ')[1] || '',
    'transport': trip.transport || '',
    'carpool': trip.carpooling || 1,
    'round': trip.is_round_trip || false,
  }
  const validated = await validateTrip(payload);
  try {
    let message = ""
    const token = await fetchToken();
    if (tripId != null) {
      await services.trips.partialUpdate(token, tripId, validated);
      message = "Trip updated successfully!";
    } else {
      const mission = rawData.value.missions.find(m => m.mission_adm_num === missionNum);
      await services.trips.create(token, { ...validated, mission: mission.mission_id });
      message = "Trip added successfully!";
    }
    delete editingTripId.value[key];
    delete editedTrip.value[key];
    const resp = await services.trips.list(token);
    rawData.value = { ...rawData.value, trips: resp };
    setTimeout(() => {
      setData(rawData.value);
      getData();
      alert(message);
    }, 100);
  } catch (e) {
    alert(`Failed to edit trip. See console for details.`);
    console.error(e);
  }
}

function editTrip(trip, missionNum, index) {
  const key = `${missionNum}_${index}`
  editingTripId.value[key] = true
  editedTrip.value[key] = cloneDeep(trip)
}

function cancelEditTrip(missionNum, index) {
  const key = `${missionNum}_${index}`
  delete editingTripId.value[key]
  delete editedTrip.value[key]
}

function updateCityList(cityName, citiesRef) {
  if (!cityName || cityName.length < 2) {
    citiesRef.value = []
    return
  }
  services.cities.fetch(cityName)
    .then(cities => { citiesRef.value = cities })
    .catch(err => console.error('City fetch error:', err));
}

const debouncedUpdateDepartureCityList = debounce(cityName => updateCityList(cityName, departureCities), 400)
const debouncedUpdateDestinationCityList = debounce(cityName => updateCityList(cityName, destinationCities), 400)

function editMission(mission) {
  selectedMissionAdmNum.value = mission.mission_adm_num;
  editedMission.value[mission.mission_adm_num] = {
    ...cloneDeep(mission),
    selectedDateRange: mission.dates ? mission.dates.split(' To ') : [null, null],
  };
}

function cancelEditMission(missionAdmNum) {
  delete editedMission.value[missionAdmNum]
}

watch(
  () => editedMission.value[selectedMissionAdmNum.value]?.selectedDateRange,
  (val) => {
    if (val && val[0] && val[1]) {
      editedMission.value[selectedMissionAdmNum.value].dates = `${val[0]} To ${val[1]}`;
    }
  }
);

async function submitEditMission(missionAdmNum) {
  if (!editedMission.value || !missionAdmNum) return;
  try {
    const mission = editedMission.value[missionAdmNum];
    const token = await fetchToken();
    const [mission_start_date, mission_end_date] = mission.dates.split(' To ').map(s => s.trim());
    const employee_adm_num = mission.employee_name.split(' - ')[1];
    const matchedEmployee = rawData.value.employees.find(
      emp => emp.employee_adm_num === employee_adm_num
    );
    const payload = {
      mission_desc: mission.mission_desc,
      mission_adm_num: mission.mission_adm_num,
      employee: matchedEmployee?.employee_id,
      start_date: mission_start_date,
      end_date: mission_end_date,
    };
    await services.missions.partialUpdate(token, mission.mission_id, payload);
    cancelEditMission(missionAdmNum);
    const resp = await services.missions.list(token);
    rawData.value = { ...rawData.value, missions: resp };
    setTimeout(() => {
      setData(rawData.value);
      getData();
      alert('Mission updated successfully!');
    }, 100);
  } catch (e) {
    console.error('Failed to update mission. See console for details.', e);
  }
}

const triggerImport = () => fileInput.value?.click()

const handleFile = async (e) => {
  const file = e.target.files?.[0]
  e.target.value = null
  if (!file || file.size > MAX_FILE_SIZE) return alert('File too large (> 2MB).')
  const raw = await file.text()
  const parsed = Papa.parse(raw.replace(/""(.*?)""/g, m => m.replace(/,/g, '-')).replace(/"/g, ''), {
    header: true,
    skipEmptyLines: true
  })
  if (!parsed.data.length || !checkColumns(parsed.data[0])) return
  const mapped = parsed.data.map(row => mapRowHeaders(row))
  const cleaned = mapped.map(cleanRow)
  await processMissions(cleaned)
}

const checkColumns = (row) => {
  const missing = Object.keys(FILE_HEADER.value).filter(col => !(col in row))
  if (missing.length) {
    alert(`Missing columns: ${missing.join(', ')}`)
    return false
  }
  return true
}

const mapRowHeaders = (row) => {
  const r = {}
  for (const [k, v] of Object.entries(FILE_HEADER.value)) {
    r[v] = row[k] || ''
  }
  return r
}

const cleanRow = (row) => {
  return Object.fromEntries(
    Object.entries(row).map(([k, v]) => [k, String(v).trim().toLowerCase()])
  )
}

const groupMissions = (rows) => {
  const res = {}
  for (const r of rows) {
    const key = `${r.num}_${r.empNum}`
    if (!res[key]) {
      const { fromCity, fromCountry, toCity, toCountry, transport, carpool, round, ...mission } = r
      res[key] = { ...mission, trips: [] }
    } else {
      if (new Date(r.start) < new Date(res[key].start)) {
        res[key].start = r.start;
      }
      if (new Date(r.end) > new Date(res[key].end)) {
        res[key].end = r.end;
      }
    }
    const { num, empNum, start, end, desc, ...trip } = r
    res[key].trips.push(trip)
  }
  return Object.values(res)
}

const validateMission = (m) => {
  if (!m.num || !m.empNum || !m.start) throw 'Missing required mission fields'
  const emp = rawData.value.employees.find(e => e.employee_adm_num === m.empNum)
  if (!emp) throw `Unknown employee ${m.empNum}`

  const sDate = new Date(m.start)
  const eDate = new Date(m.end || m.start)
  if (sDate > eDate || isNaN(sDate) || isNaN(eDate)) throw 'Invalid mission dates'

  return {
    mission_adm_num: m.num,
    employee: emp.employee_id,
    start_date: sDate.toISOString().slice(0, 10),
    end_date: eDate.toISOString().slice(0, 10),
    mission_desc: m.desc || ''
  }
}

const transportMap = { 
  avion: 'PLANE', voiture: 'CAR', 'véhicule personnel': 'CAR', 
  taxi: 'CAB', bus: 'BUS', ferry: 'FERRY', train: 'TRAIN', rer: 'RER', 
  tram: 'TRAM', metro: 'SUBWAY', 'métro': 'SUBWAY' 
}

const validateTrip = async (t) => {
  if (!t.fromCity || !t.fromCountry) {
    throw 'Departure location is required';
  }
  if (!t.toCity || !t.toCountry) {
    throw 'Destination location is required';
  }

  const [from] = await services.cities.fetch(`${t.fromCity}, ${t.fromCountry}`)
  const [to] = await services.cities.fetch(`${t.toCity}, ${t.toCountry}`)
  if (!from || !from.geonameId || !from.lat || !from.lng) throw `Unknown departure city: ${from}`
  if (!to || !to.geonameId || !to.lat || !to.lng) throw `Unknown destination city: ${to}`

  const carpool = parseInt(t.carpool || '1')
  if (isNaN(carpool) || carpool <= 0) throw 'Invalid carpooling number (must be >=1)'

  const transport = /\b(avion|plane)\b/i.test(t.transport)
    ? 'PLANE'
    : transportMap[t.transport] || t.transport.toUpperCase();
  // const transport = transportMap[t.transport] || t.transport.toUpperCase();
  if (!Object.values(transportMap).includes(transport)) {
    throw `Invalid transport. Choose from: PLANE, BUS, CAR, CAB, TRAIN, FERRY, RER, SUBWAY, TRAM`
  }

  return {
    departure_city: from.name.toLowerCase(),
    departure_country: from.countryCode,
    destination_city: to.name.toLowerCase(),
    destination_country: to.countryCode,
    transport,
    is_round_trip: ["oui", "true", true].includes(t.round),
    carpooling: carpool
  }
}

// === Insert new mission or crush the old one ===
const insertMission = async (token, missionPayload, trips, admNum) => {
  const existingMissions = rawData.value.missions;
  const existing = existingMissions.find(
    (m) => m.mission_adm_num === admNum
  );

  let missionId;

  if (existing) {
    missionId = existing.mission_id;
    const existingTrips = rawData.value.trips.filter(t => t.mission === missionId);

    // const preview = JSON.stringify(existingTrips, null, 2);
    // const confirmed = confirm(
    //   `Mission ${admNum} already exists with the following trips:\n\n${preview}\n\nDo you want to overwrite it?`
    // );

    // if (!confirmed) {
    //   alert('Mission overwrite cancelled.');
    //   return;
    // }

    await services.missions.update(token, missionId, missionPayload);

    await Promise.all(existingTrips.map(t =>
      services.trips.destroy(token, t.trip_id)
    ));
    // alert('Mission has been overwritten.');

  } else {
    const created = await services.missions.create(token, missionPayload);
    missionId = created.mission_id;
  }

  await Promise.all(trips.map(t =>
    services.trips.create(token, { ...t, mission: missionId })
  ));
};

const reloadMissions = async (token) => {
  const [missions, trips] = await Promise.all([
    services.missions.list(token),
    services.trips.list(token),
  ]);

  rawData.value = { ...(rawData.value || {}), missions, trips };

  setTimeout(() => {
    setData(rawData.value);
    getData();
  }, 100);

};

// === Mission Runner ===
const processMissions = async (rows) => {
  const token = await fetchToken();
  const groups = groupMissions(rows);
  const errors = [];

  await Promise.allSettled(groups.map(async (g) => {
    try {
      const missionPayload = validateMission(g);
      const trips = await Promise.all(g.trips.map(validateTrip));
      const admNum = missionPayload.mission_adm_num;

      await insertMission(token, missionPayload, trips, admNum);
    } catch (err) {
      errors.push({ mission: g, error: err.toString() });
    }
  }));

  reloadMissions(token);

  setTimeout(() => {
    errors.forEach(showError);
    alert('Import done');
  }, 100);
};

// === Error Injection ===
const showError = ({ mission, error }) => {
  const emp = rawData.value.employees.find(e => e.employee_adm_num === mission.empNum) || {}
  const uiMission = {
    mission_id: null,
    mission_adm_num: mission.num,
    dates: `${mission.start} To ${mission.end || mission.start}`,
    mission_desc: mission.desc,
    employee_name: `${emp.first_name || ''} ${emp.last_name || ''} - ${mission.empNum}`,
    employee_status: emp.status || '',
    carbon_footprint: '0.00',
    hasError: true,
    isValid: false,
    message: error,
    children: mission.trips.map(t => ({
      trip_id: null,
      transport: t.transport,
      carpooling: t.carpool || '1',
      is_round_trip: t.round || 'false',
      carbon_footprint: '0.00',
      departure: `${t.fromCity}, ${t.fromCountry}`,
      destination: `${t.toCity}, ${t.toCountry}`
    }))
  }
  displayData.value.unshift(uiMission)
  editMission(uiMission)
  uiMission.children.forEach((trip, i) => editTrip(trip, mission.num, i))
};

const submitCorrectMission = async (admNum) => {
  try {
    const mission = editedMission.value[admNum];

    const missionPayload = validateMission({
      num: mission.mission_adm_num,
      start: mission.dates.split(' To ')[0],
      end: mission.dates.split(' To ')[1],
      desc: mission.mission_desc,
      empNum: mission.employee_name.split(' - ')[1],
    });

    const tripsPayloads = await Promise.all(
      mission.children.map((_, i) => {
        const trip = editedTrip.value[`${admNum}_${i}`];
        return validateTrip({ 
          fromCity: trip.departure.split(', ')[0],
          fromCountry: trip.departure.split(', ')[1],
          toCity: trip.destination.split(', ')[0],
          toCountry: trip.destination.split(', ')[1],
          carpool: trip.carpooling,
          round: trip.is_round_trip,
          transport: trip.transport
        });
      })
    );

    const token = await fetchToken();
    await insertMission(token, missionPayload, tripsPayloads, admNum);

    const emp = rawData.value.employees.find(e => e.employee_id === missionPayload.employee);
    const rowUpdate = {
      mission_id: null,
      mission_adm_num: missionPayload.mission_adm_num,
      mission_desc: missionPayload.mission_desc,
      dates: `${missionPayload.start_date} To ${missionPayload.end_date}`,
      employee_name: `${emp.first_name} ${emp.last_name} - ${emp.employee_adm_num}`.trim(),
      employee_status: emp.status,
      carbon_footprint: 0,
      _expanded: true,
      isValid: true,
      hasError: false,
      children: tripsPayloads.map(t => ({
        trip_id: null,
        departure: `${t.departure_city}, ${t.departure_country}`,
        destination: `${t.destination_city}, ${t.destination_country}`,
        carpooling: t.carpooling,
        is_round_trip: t.is_round_trip,
        transport: t.transport,
        carbon_footprint: 0
      })),
    };

    const indexes = displayData.value
                    .map((m, i) => m.mission_adm_num === admNum ? i : -1)
                    .filter(i => i !== -1);
    for (const i of indexes) {
      displayData.value[i] = rowUpdate;
      // displayData.value[i].isValid = true;
      // displayData.value[i].hasError = false;
    }

    cancelEditMission(admNum);
    Object.keys(editedTrip.value)
    .filter(key => key.startsWith(`${admNum}_`))
    .forEach(key => {
      const index = key.split('_')[1];
      cancelEditTrip(admNum, index);
    });
    alert('Mission corrected successfully');
  } catch (error) {
    alert(`Validation or correction error: ${error}`);
  }
};

// const stillCorrections = computed(() => {
//   const missions = displayData.value;
//   return missions.some(m => m.hasError === true);
// });

// watch(stillCorrections, async (hasErrors) => {
//   if (!hasErrors) {
//     const token = await fetchToken();
//     reloadMissions(token);
//   }
// }, { immediate: true });

function openEmployeeModal(employee, operation) {
  employeeProps.value = employee ? { ...employee } : null;
  operationProps.value = operation
  isEmployeeModalActive.value = true;
}

function closeEmployeeModal() {
  isEmployeeModalActive.value = false;
  employeeProps.value = null;
  operationProps.value = '';
}

function handleEmployeeUpdated(updatedEmployee) {
  const index = rawData.value.employees.findIndex(
    (e) => e.employee_id === updatedEmployee.employee_id
  );
  if (index !== -1) {
    rawData.value.employees[index] = { ...updatedEmployee };
    setData(rawData.value);
  }
  closeEmployeeModal();
}
</script>

<style scoped>
.chart-container {
  width: 100%;
  height: 250px;
}

.bar-container {
  width: 100%;
  height: 400px;
}

.card {
  border-radius: 8px;
  background-color: #f9fafb;
}

.modal-card {
  width: 80%;
}

.table-wrapper {
  overflow-y: scroll;
  height: 800px !important;
  margin-bottom: 2rem;
}

.compact-table {
  width: 100%;
  border-collapse: separate;
  border-spacing: 0;
  font-size: 0.75rem;
  table-layout: fixed;
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.compact-table .row{
  padding-left: 0rem;
}

.compact-table thead {
  background: #f5f7fa;
  border-bottom: 1.5px solid #d1d5db;
}

.compact-table th,
.compact-table td {
  padding: 5px 8px;
  /* white-space: nowrap; */
  white-space: normal;
  overflow: visible;
  /* text-overflow: ellipsis; */
  border-right: 1px solid #e1e4e8;
  color: #374151;
}

.compact-table th:last-child,
.compact-table td:last-child {
  border-right: none;
}

.compact-table tbody tr {
  background: #fff;
  border-bottom: 1px solid #e6ebf1;
  transition: background-color 0.25s ease;
}

.compact-table tbody tr:hover {
  background-color: #f0f4f8;
}

.compact-table th:nth-child(2),
.compact-table td:nth-child(2),
.compact-table th:nth-child(9),
.compact-table td:nth-child(9),
.compact-table th:nth-child(10),
.compact-table td:nth-child(10),
.compact-table th:nth-child(11),
.compact-table td:nth-child(11),
.compact-table th:nth-child(12),
.compact-table td:nth-child(12) {
  width: 6% !important;
  min-width: 6%;
  max-width: 6%;
  text-align: left;
}

.compact-table th:nth-child(5),
.compact-table td:nth-child(5) {
  width: 11% !important;
  min-width: 11%;
  max-width: 11%;
  text-align: left;
}

.compact-table th:nth-child(7),
.compact-table td:nth-child(7),
.compact-table th:nth-child(8),
.compact-table td:nth-child(8) {
  width: 8% !important;
  min-width: 8%;
  max-width: 8%;
  text-align: left;
}

.compact-table th:nth-child(3),
.compact-table td:nth-child(3),
.compact-table th:nth-child(4),
.compact-table td:nth-child(4) {
  width: 16% !important;
  min-width: 16%;
  max-width: 16%;
  text-align: left;
}

.compact-table th:nth-child(1),
.compact-table td:nth-child(1),
.compact-table th:nth-child(6),
.compact-table td:nth-child(6),
.compact-table th:nth-child(13),
.compact-table td:nth-child(13) {
  width: 3% !important;
  min-width: 3%;
  max-width: 3%;
  text-align: center !important;
}

.has-error {
  background-color: #ffe6e6;
  border-left: 4px solid #ff4d4d;
}

.disabled-row {
  opacity: 0.5;
  pointer-events: none;
}

.custom-datepicker-popup {
  max-width: 300px;
  min-width: 260px;
  white-space: normal;
  word-break: break-word;
  z-index: 9999;
  padding: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
  background-color: white;
  border-radius: 6px;
}

.mx-datepicker {
  width: 100%;
  min-width: 150px;
}

.mx-input {
  white-space: normal !important;
  overflow-wrap: break-word;
}
</style>