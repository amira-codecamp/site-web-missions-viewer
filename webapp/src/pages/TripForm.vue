
<template>
  <div class="box has-background-white-bis">
    <form @submit.prevent="submitForm">
      <div class="columns is-multiline is-variable is-5">

        <div class="column is-5">
          <!-- Mission -->
          <div class="field mb-5">
            <label class="label has-text-weight-medium has-text-grey-dark">Mission</label>
            <div class="control">
              <input
                class="input"
                list="missions-list"
                v-model="form.mission_num"
                placeholder="Type mission"
                required
              />
              <datalist id="missions-list">
                <option
                  v-for="mission in missions"
                  :key="mission.mission_num"
                  :value="mission.mission_num"
                />
              </datalist>
            </div>
          </div>

          <!-- Transport -->
          <div class="field mb-5">
            <label class="label has-text-weight-medium has-text-grey-dark">Transport</label>
            <div class="control">
              <input
                class="input"
                list="transports-list"
                v-model="form.transport_name"
                placeholder="Type transport"
                required
              />
              <datalist id="transports-list">
                <option
                  v-for="transport in transports"
                  :key="transport.transport_name"
                  :value="transport.transport_name"
                  />
              </datalist>
            </div>
          </div>

          <!-- Employee -->
          <div class="field mb-5">
            <label class="label has-text-weight-medium has-text-grey-dark">Employee</label>
            <div class="control">
              <input
                class="input"
                list="employees-list"
                v-model="selectedEmployee"
                placeholder="Type employee"
                required
              />
              <datalist id="employees-list">
                <option
                  v-for="employee in employees"
                  :key="employee.email"
                  :value="formatEmployee(employee)"
                />
              </datalist>
            </div>
          </div>

          <!-- Round Trip Checkbox -->
          <div class="field mb-5">
            <label class="checkbox has-text-grey-dark">
              <input type="checkbox" v-model="form.is_round_trip" />
              &nbsp;Round Trip
            </label>
          </div>

          <!-- Carpooling -->
          <div class="field mb-5">
            <label class="label has-text-weight-medium has-text-grey-dark">Carpooling</label>
            <div class="control">
              <input
                class="input"
                type="number"
                v-model.number="form.carpooling"
                min="1"
                placeholder="Number of carpoolers"
              />
            </div>
          </div>

          <!-- Quantity -->
          <div class="field mb-5" v-if="!disableQuantity">
            <label class="label has-text-weight-medium has-text-grey-dark">Quantity</label>
            <div class="control">
              <input
                class="input"
                type="number"
                v-model.number="quantityField"
                min="1"
                placeholder="Number of trips"
              />
            </div>
          </div>
        </div>

        <div class="column is-7">
          <div class="columns">
            <!-- Departure City -->
            <div class="column is-half">
              <div class="field mb-5">
                <label class="label has-text-weight-medium has-text-grey-dark">Departure City</label>
                <div class="control">
                  <input
                    class="input"
                    list="depcities-list"
                    v-model="selectedDepartureCity"
                    placeholder="Type departure city"
                    @input="onDepartureInput"
                    required
                  />
                  <datalist id="depcities-list">
                    <option
                      v-for="city in departureCities"
                      :key="city.geonameId"
                      :value="formatCity(city)"
                    />
                  </datalist>
                </div>
              </div>
            </div>

            <!-- Destination City -->
            <div class="column is-half">
              <div class="field mb-5">
                <label class="label has-text-weight-medium has-text-grey-dark">Destination City</label>
                <div class="control">
                  <input
                    class="input"
                    list="descities-list"
                    v-model="selectedDestinationCity"
                    placeholder="Type destination city"
                    @input="onDestinationInput"
                    required
                  />
                  <datalist id="descities-list">
                    <option
                      v-for="city in destinationCities"
                      :key="city.geonameId"
                      :value="formatCity(city)"
                    />
                  </datalist>
                </div>
              </div>
            </div>
          </div>

          <!-- Map Placeholder -->
          <div class="field mb-5">
            <div id="map_wrapper" style="height: 55vh;">
              <l-map
                ref="mapRef"
                :bounds="initialBounds"
              >
              <l-tile-layer
                url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                attribution="&copy; OpenStreetMap contributors"
              />
                <l-marker v-if="getDepartureCoords()" :lat-lng="getDepartureCoords()" />
                <l-marker v-if="getDestinationCoords()" :lat-lng="getDestinationCoords()" />
                <l-polyline ref="polylineRef"
                  v-if="getDepartureCoords() && getDestinationCoords()"
                  :lat-lngs="[getDepartureCoords(), getDestinationCoords()]"
                  color="#4E6688"
                />
              </l-map>
            </div>
          </div>
        </div>

        <!-- FULL WIDTH FOOTER -->
        <div class="column is-full">

          <!-- Submit -->
          <div class="field">
            <div class="control">
              <button class="button is-dark is-fullwidth is-medium">
                <span v-if="!disableQuantity">+ Add Trip</span>
                <span v-if="disableQuantity">Alter Trip</span>
              </button>
            </div>
          </div>

        </div>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import { useStore } from '@/store'
import debounce from 'lodash.debounce'
import { LMap, LTileLayer, LMarker, LPolyline } from '@vue-leaflet/vue-leaflet'

import authservice from '@/services/authservice'
import geonamesservice from '@/services/geonamesservice'
import tripsservice from '@/services/tripsservice'
import emissionsservice from '@/services/emissionsservice'

defineOptions({ name: 'TripForm' })

const store = useStore()

const props = defineProps({
  operation: {
    type: String,
    required: true,
  },
  trip: {
    type: Object,
    required: true,
  },
  disableQuantity: {
    type: String,
    required: true,
  }
})

const form = ref({})
const departureCities = ref([])
const destinationCities = ref([])
const quantityField = ref(1)
const selectedDepartureCity = ref('')
const selectedDestinationCity = ref('')
const selectedEmployee = ref('')
const mapRef = ref(null)
const polylineRef = ref(null)
const selectedTrip = ref(null)
const disableQuantity = ref(null)

const missions = computed(() => store.state.missions)
const employees = computed(() => store.state.employees)
const transports = computed(() => store.state.transports)

const initForm = () => {
  if (props.operation === 'add') {
    form.value = {
      mission_num: '',
      transport_name: '',
      employee: {
        first_name: '',
        last_name: '',
        email: '',
      },
      departure_city: '',
      departure_country: '',
      destination_city: '',
      destination_country: '',
      is_round_trip: false,
      carpooling: 1,
      carbon_footprint: null,
    }
    selectedEmployee.value = ''
    selectedDepartureCity.value = ''
    selectedDestinationCity.value = ''
  }
  // else if (props.operation === 'alter' && (props.trip)) {
  //   selectedTrip.value = props.trip;
  //   disableQuantity.value = props.disableQuantity;
  //   form.value = {
  //     trip_id: selectedTrip.value.trip_id,
  //     mission_num: selectedTrip.value.mission.mission_num,
  //     transport_name: selectedTrip.value.transport.transport_name,
  //     is_round_trip: selectedTrip.value.is_round_trip,
  //     carpooling: selectedTrip.value.carpooling,
  //     employee: selectedTrip.value.employee,
  //     departure_city: selectedTrip.value.departure_city,
  //     departure_country: selectedTrip.value.departure_country,
  //     destination_city: selectedTrip.value.destination_city,
  //     destination_country: selectedTrip.value.destination_country,
  //     carbon_footprint: 3,
  //   }
  //   selectedEmployee.value = formatEmployee(selectedTrip.value.employee)
  //   selectedDepartureCity.value = `${selectedTrip.value.departure_city}, ${selectedTrip.value.departure_country}`;
  //   selectedDestinationCity.value = `${selectedTrip.value.destination_city}, ${selectedTrip.value.destination_country}`;
  // }
}

const formatEmployee = (emp) => `${emp.first_name} ${emp.last_name} <${emp.email}>`

const countryCodeToFlag = (countryIsoCode) => {
  if (!countryIsoCode || typeof countryIsoCode !== 'string') return ''
  return countryIsoCode.toUpperCase().replace(/./g, c => String.fromCodePoint(c.charCodeAt(0) + 127397))
}

const formatCity = (city) => {
  const flag = countryCodeToFlag(city.countryCode)
  return `${city.name}, ${city.countryName} ${flag}`
}

const fetchCities = async (cityName) => {
  const response = await geonamesservice.fetchCities(cityName)
  return response
}

const callGeoName = debounce(async (cityName, targetKey) => {
  if (cityName.length >= 2) {
    try {
      const response = await fetchCities(cityName)
      if (targetKey === 'departureCities') departureCities.value = response
      else if (targetKey === 'destinationCities') destinationCities.value = response
    } catch (err) {
      console.error('GeoName fetch error:', err)
    }
  }
}, 400)

const onDepartureInput = () => {
  callGeoName(selectedDepartureCity.value, 'departureCities')
}

const onDestinationInput = () => {
  callGeoName(selectedDestinationCity.value, 'destinationCities')
}

const getDepartureCoords = () => {
  const city = departureCities.value.find(cit => formatCity(cit) === selectedDepartureCity.value)
  return city ? [city.lat, city.lng] : null
}

const getDestinationCoords = () => {
  const city = destinationCities.value.find(cit => formatCity(cit) === selectedDestinationCity.value)
  return city ? [city.lat, city.lng] : null
}

const fitBoundsMap = async () => {
  await nextTick()
  const map = mapRef.value?.mapObject || mapRef.value?.leafletObject
  const polyline = polylineRef.value?.leafletObject

  if (map && polyline) {
    const bounds = polyline.getBounds()
    if (bounds.isValid()) {
      map.fitBounds(bounds, { animate: false })
    } else {
      console.warn('Bounds invalid')
    }
  } else {
    console.warn('Map or polyline not found')
  }
}

const submitForm = async () => {
  try {

    try {
      const refresh = store.state.refreshToken
      const responsetok = await authservice.refresh(refresh);
      store.setItem("accessToken", responsetok.access);

    } catch (error) {
      alert("Session expired. Please login again.");

      store.clearItem('trips')
      store.clearItem('employees')
      store.clearItem('transports')
      store.clearItem('missions')
      store.clearItem('isManager')
      store.clearItem('user')
      store.clearItem('accessToken')
      store.clearItem('refreshToken')

      window.location.href = '/login';
      return;
    }

    const access = store.state.accessToken

    const [dep_city_obj, dest_city_obj] = [
      departureCities.value.find(cit => formatCity(cit) === selectedDepartureCity.value),
      destinationCities.value.find(cit => formatCity(cit) === selectedDestinationCity.value)
    ]

    const mission = missions.value.find(m => m.mission_num === form.value.mission_num)
    const full_year = new Date(mission.start_date).getFullYear().toString()

    const payload = {
      departure_country: dep_city_obj.countryCode,
      departure_lat: dep_city_obj.lat,
      departure_long: dep_city_obj.lng,
      destination_country: dest_city_obj.countryCode,
      destination_lat: dest_city_obj.lat,
      destination_long: dest_city_obj.lng,
      transport: form.value.transport_name,
      carpooling: form.value.carpooling,
      is_round_trip: form.value.is_round_trip,
      year: full_year,
    }

    const response0 = await emissionsservice.getCarbonFootprint(payload, access)
    form.value.carbon_footprint = Number(Number(response0.carbon_footprint).toFixed(2))

    form.value.departure_country = dep_city_obj.countryName
    form.value.departure_city = dep_city_obj.name
    form.value.destination_country = dest_city_obj.countryName
    form.value.destination_city = dest_city_obj.name

    form.value.employee = employees.value.find(emp => formatEmployee(emp) === selectedEmployee.value)

    if (props.operation === 'add') {

      const numRows = quantityField.value
      for (let i = 0; i < numRows; i++) {
        await tripsservice.trips.createTrip(access, { ...form.value })
      }

      const response1 = await tripsservice.trips.fetchTrips(access)
      store.setItem('trips', response1.trips)

      alert(`${quantityField.value} trip${quantityField.value === 1 ? '' : 's'} created successfully!`)

    } else if (props.operation === 'alter') {

      // await tripsservice.trips.alterTrip(access, { ...form.value });

      // const response2 = await tripsservice.trips.fetchTrips(access);
      // store.setItem('trips', response2.trips);

      // alert('Trip updated successfully!');
    }

    setTimeout(() => {
    }, 1000)

  } catch (error) {
    if (error.response?.data) {
      const messages = Object.entries(error.response.data).map(([key, val]) => `${key}: ${val}`)
      alert(messages.join('\n'))
    } else {
      alert('Something went wrong. Please try again.')
    }
  }
}

watch([selectedDepartureCity, selectedDestinationCity], fitBoundsMap)

watch(
  () => [props.action, props.trip],
  () => {
    initForm();
  },
  { immediate: true }
);
</script>