<template>
  <form-wizard
    :key="wizardKey"
    @on-complete="submitForm"
    :start-index="activeTab"
    @on-change="onTabChange"
    ref="wizardRef"
    color="#4a76a8"
    next-button-text="Next"
    back-button-text="Back"
    finish-button-text="Submit"
  >
    <!-- Mission Tab -->
    <tab-content title="Mission" icon="ti-briefcase">
      <div class="body-tab">

        <div class="mb-5">
          <label class="label has-text-weight-medium has-text-grey-dark">Mission Num</label>
          <input
            class="input"
            v-model="form.mission_adm_num"
            placeholder="Type mission"
            required
          />
        </div>

        <div class="mb-5">
          <label class="label has-text-weight-medium has-text-grey-dark">Mission Description</label>
          <input
            class="input"
            v-model="form.mission_desc"
            placeholder="Type description"
            required
          />
        </div>

        <div class="mb-5">
          <label class="label has-text-weight-medium has-text-grey-dark">Start Date</label>
          <input type="date" v-model="form.start_date" class="input" required />
        </div>

        <div class="mb-5">
          <label class="label has-text-weight-medium has-text-grey-dark">End Date</label>
          <input type="date" v-model="form.end_date" class="input" required />
        </div>

        <div class="mb-5">
          <label class="label has-text-weight-medium has-text-grey-dark">
            Employee
            <button class="button is-text is-small has-text-link" @click="openEmployeeModal(null, 'add')">
              Add
            </button>
          </label>
          <input
            class="input"
            list="employees-list"
            v-model="selectedEmployee"
            placeholder="Select employee"
            required
          />
          <datalist id="employees-list">
            <option
              v-for="employee in data.employees"
              :key="employee.employee_id"
              :value="`${employee.first_name} ${employee.last_name} - ${employee.employee_adm_num}`"
            />
          </datalist>
        </div>

      </div>
    </tab-content>

    <!-- Dynamic Trip Tabs -->
    <tab-content
      v-for="(trip, index) in form.trips"
      :key="index"
      :title="`Trip ${index + 1}`"
      :icon="'ti-location-pin'"
    >
      <div class="body-tab columns is-multiline">
        <div class="column is-5">
          <div class="mb-5">
            <label class="label has-text-weight-medium has-text-grey-dark">Departure City</label>
            <input
              class="input"
              :list="`departure-cities-list-${index}`"
              v-model="trip.inputDepartureCity"
              placeholder="Type departure city"
              @input="() => updateDepartureCityList(trip)"
              @change="() => onInputDepartureCityChange(trip)"
              required
            />
            <datalist :id="`departure-cities-list-${index}`">
              <option
                v-for="city in trip.departureCities"
                :key="city.geonameId"
                :value="`${city.name} ${countryCodeToFlagEmoji(city.countryCode)}`"
              />
            </datalist>
          </div>

          <div class="mb-5">
            <label class="label has-text-weight-medium has-text-grey-dark">Destination City</label>
            <input
              class="input"
              :list="`destination-cities-list-${index}`"
              v-model="trip.inputDestinationCity"
              placeholder="Type destination city"
              @input="() => updateDestinationCityList(trip)"
              @change="() => onInputDestinationCityChange(trip)"
              required
            />
            <datalist :id="`destination-cities-list-${index}`">
              <option
                v-for="city in trip.destinationCities"
                :key="city.geonameId"
                :value="`${city.name} ${countryCodeToFlagEmoji(city.countryCode)}`"
              />
            </datalist>
          </div>

          <div class="mb-5">
            <label class="label has-text-weight-medium has-text-grey-dark">Transport</label>
            <input
              class="input"
              list="transports-list"
              v-model="trip.transport"
              placeholder="Select transport"
              required
            />
            <datalist id="transports-list">
              <option v-for="transport in data.transports" :key="transport.transport_name" :value="transport.transport_name" />
            </datalist>
          </div>

          <div class="mb-5">
            <label class="label has-text-weight-medium has-text-grey-dark">Carpooling</label>
            <input
              class="input"
              type="number"
              v-model.number="trip.carpooling"
              min="1"
              placeholder="Number of carpoolers"
            />
          </div>

          <div class="mb-5">
            <label class="checkbox has-text-grey-dark">
              <input type="checkbox" v-model="trip.is_round_trip" />
              &nbsp;Round Trip
            </label>
          </div>

          <button 
            class="button is-secondary is-light mt-3" 
            type="button" 
            @click="addTrip()"
            v-if="form.trips.length == index+1"
          >
            <i class="fas fa-plus"></i>
          </button>

          <button
            class="button is-secondary is-light mt-3"
            type="button"
            @click="removeTrip(index)"
            v-if="form.trips.length > 1"
          >
            <i class="fas fa-minus"></i>
          </button>

        </div>

        <div class="column is-7">
            <div class="card mb-4">
                <div class="card-content is-flex is-flex-direction-column p-5">
                    <div id="map_wrapper">
                        <l-map
                        :zoom="6"
                        :center="[48.8566, 2.3522]"
                        :bounds="trip.initBounds"
                        :ref="el => trip.mapRef = el"
                        style="height: 100%;"
                        v-if="trip.departureCoords && trip.destinationCoords"
                        >
                        <l-tile-layer
                            url="https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png"
                            attribution='&copy; OpenStreetMap contributors, Tiles style by Humanitarian OSM Team'
                        />
                        <l-marker :lat-lng="trip.departureCoords" />
                        <l-marker :lat-lng="trip.destinationCoords" />
                        <l-polyline
                            :lat-lngs="[trip.departureCoords, trip.destinationCoords]"
                            color="rgb(231, 76, 60)"
                        />
                        </l-map>
                    </div>
                </div>
            </div>
        </div>
      </div>
    </tab-content>

  </form-wizard>

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
import { ref, computed, nextTick, watch } from 'vue'
import { FormWizard, TabContent } from 'vue3-form-wizard'
import 'vue3-form-wizard/dist/style.css'
import debounce from 'lodash.debounce'
import { LMap, LTileLayer, LMarker, LPolyline } from '@vue-leaflet/vue-leaflet'
import services from '@/composables/services'
import { fetchToken, getData, setData } from '@/composables/session'
import EmployeeForm from "@/components/EmployeeForm.vue";


const emit = defineEmits(['submitted'])

const wizardRef = ref(null)
const data = computed(() => getData())
const wizardKey = ref(0)

const isEmployeeModalActive = ref(false);
const employeeProps = ref(null);
const operationProps = ref(null);

const selectedEmployee = ref('')

const form = ref({
  mission_id: null,
  mission_adm_num: '',
  mission_desc: '',
  start_date: null,
  end_date: null,
  employee: null,
  trips: [createEmptyTrip()],
})

function createEmptyTrip() {
  return {
    inputDepartureCity: '',
    inputDestinationCity: '',
    transport: '',
    carpooling: 1,
    is_round_trip: false,
    departureCities: [],
    destinationCities: [],
    departureCoords: null,
    destinationCoords: null,
    departure_country: '',
    destination_country: '',
    departure_city: '',
    destination_city: '',
    initBounds: null,
    mapRef: null,
  }
}

const activeTab = ref(0)

async function addTrip() {
  form.value.trips.push(createEmptyTrip())
  activeTab.value = form.value.trips.length
  wizardKey.value++
  await nextTick()
  wizardRef.value?.navigateToTab(activeTab.value)
}

async function removeTrip(index) {
  form.value.trips.splice(index, 1)
  activeTab.value = index
  wizardKey.value++
  await nextTick()
  wizardRef.value?.navigateToTab(activeTab.value)
}

function updateDepartureCityList(trip) {
  if (trip.inputDepartureCity.length < 2) {
    trip.departureCities = []
    return
  }
  debounceFetchCities(trip.inputDepartureCity, (cities) => {
    trip.departureCities = cities
  })
}

function updateDestinationCityList(trip) {
  if (trip.inputDestinationCity.length < 2) {
    trip.destinationCities = []
    return
  }
  debounceFetchCities(trip.inputDestinationCity, (cities) => {
    trip.destinationCities = cities
  })
}

const debounceFetchCities = debounce(async (query, cb) => {
  try {
    const cities = await services.cities.fetch(query)
    cb(cities)
  } catch {
    cb([])
  }
}, 400)

function countryCodeToFlagEmoji(countryCode) {
  if (!countryCode || typeof countryCode !== 'string') return ''
  return countryCode
    .toUpperCase()
    .split('')
    .map((char) => String.fromCodePoint(127397 + char.charCodeAt()))
    .join('')
}

function onInputDepartureCityChange(trip) {
  const selectedCity = trip.departureCities.find((city) => {
    return `${city.name} ${countryCodeToFlagEmoji(city.countryCode)}` === trip.inputDepartureCity
  })
  if (selectedCity) {
    trip.departureCoords = { lat: selectedCity.lat, lng: selectedCity.lng }
    trip.departure_country = selectedCity.countryCode
    trip.departure_city = selectedCity.name
    updateMapBounds(trip)
  } else {
    trip.departureCoords = null
    trip.departure_country = ''
    trip.departure_city = ''
  }
}

function onInputDestinationCityChange(trip) {
  const selectedCity = trip.destinationCities.find((city) => {
    return `${city.name} ${countryCodeToFlagEmoji(city.countryCode)}` === trip.inputDestinationCity
  })
  if (selectedCity) {
    trip.destinationCoords = { lat: selectedCity.lat, lng: selectedCity.lng }
    trip.destination_country = selectedCity.countryCode
    trip.destination_city = selectedCity.name
    updateMapBounds(trip)
  } else {
    trip.destinationCoords = null
    trip.destination_country = ''
    trip.destination_city = ''
  }
}

function updateMapBounds(trip) {
  nextTick(() => {
    if (trip.departureCoords && trip.destinationCoords) {
      trip.initBounds = [
        [trip.departureCoords.lat, trip.departureCoords.lng],
        [trip.destinationCoords.lat, trip.destinationCoords.lng],
      ];
    } else if (trip.departureCoords) {
      trip.initBounds = [
        [trip.departureCoords.lat, trip.departureCoords.lng],
      ];
    } else if (trip.destinationCoords) {
      trip.initBounds = [
        [trip.destinationCoords.lat, trip.destinationCoords.lng],
      ];
    } else {
      trip.initBounds = null;
    }
  });
}

function onTabChange(prevIndex, nextIndex) {
  activeTab.value = nextIndex
  if (nextIndex === 0) return
  nextTick(() => {
    const currentTrip = form.value.trips[activeTab.value - 1]
    if (currentTrip.mapRef && currentTrip.mapRef.leafletObject) {
      currentTrip.mapRef.leafletObject.invalidateSize()
    }
  })
}

function handleValidation() {
    if (
        !selectedEmployee.value ||
        !form.value.start_date ||
        !form.value.end_date ||
        !form.value.mission_adm_num
    ) {
        alert('Please fill all fields in Mission Tab.')
        return false;
    }
    const exists = data.value.missions?.some(
      (m) => m.mission_adm_num === form.value.mission_adm_num
    );
    if (exists) {
      alert(`Mission ${form.value.mission_adm_num} already exists. Please edit instead.`);
      return false;
    }
    const now = new Date()
    const start = new Date(form.value.start_date)
    const end = new Date(form.value.end_date)
    if (start > now) {
        alert('Start date cannot be in the future.')
        return false;
    }
    if (end > now) {
        alert('End date cannot be in the future.')
        return false;
    }
    if (start > end) {
        alert('Start date cannot be after end date.')
        return false;
    }
    for (const trip of form.value.trips) {
        if (
        !trip.inputDepartureCity ||
        !trip.inputDestinationCity ||
        !trip.transport
        ) {
            alert('Please fill all fields in Trips Tabs.')
            return false;
        }
    }
    return true;
}

watch(
  () => form.value.start_date,
  (newVal) => {
    form.value.end_date = newVal;
  }
);


watch(selectedEmployee, (newVal) => {
  const admNum = newVal?.split(' - ')[1];
  const matched = data.value.employees.find(emp => emp.employee_adm_num === admNum);
  form.value.employee = matched ? matched.employee_id : null;
});

async function submitForm() {
  if (!handleValidation()) return;

  const token = await fetchToken();
  
  const mission_payload = {
    employee: form.value.employee,
    start_date: form.value.start_date,
    end_date: form.value.end_date,
    mission_adm_num: form.value.mission_adm_num,
    mission_desc: form.value.mission_desc,
  };

  const createdMission = await services.missions.create(token, mission_payload);
  form.value.mission_id = createdMission.mission_id

  for (const trip of form.value.trips) {
    const trip_payload = {
      departure_city: trip.departure_city,
      departure_country: trip.departure_country,
      destination_city: trip.destination_city,
      destination_country: trip.destination_country,
      is_round_trip: trip.is_round_trip,
      carpooling: trip.carpooling,
      transport: trip.transport,
      mission: form.value.mission_id,
    };
    await services.trips.create(token, trip_payload);
  }
  
  emit('submitted');
}

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
  const index = data.value.employees.findIndex(
    (e) => e.employee_id === updatedEmployee.employee_id
  );
  if (index !== -1) {
    data.value.employees[index] = { ...updatedEmployee };
    setData(data.value);
  }
  closeEmployeeModal();
}
</script>

<style scoped>
#map_wrapper {
  height: 400px;
}
.body-tab {
  padding: 15px;
}

.card {
  border-radius: 8px;
  background-color: #f9fafb;
}
</style>