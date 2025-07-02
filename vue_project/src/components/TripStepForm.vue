<template>
    <form @submit.prevent="submitForm">
      <div class="body-tab columns is-multiline">
          <div class="column is-half">
              <div class="mb-5">
                  <label class="label has-text-weight-medium has-text-grey-dark">Departure City</label>
                  <input
                  class="input"
                  :list="`departure-cities-list-${stepId}`"
                  v-model="inputDepartureCity"
                  placeholder="Type departure city"
                  @input="onInputDepartureCityChange"
                  required
                  />
                  <datalist :id="`departure-cities-list-${stepId}`">
                      <option
                          v-for="city in departureCities"
                          :key="city.geonameId"
                          :value="`${city.name} ${countryCodeToFlagEmoji(city.countryCode)}`"
                      />
                  </datalist>
              </div>

              <div class="mb-5">
                  <label class="label has-text-weight-medium has-text-grey-dark">Destination City</label>
                  <input
                  class="input"
                  :list="`destination-cities-list-${stepId}`"
                  v-model="inputDestinationCity"
                  placeholder="Type destination city"
                  @input="onInputDestinationCityChange"
                  required
                  />
                  <datalist :id="`destination-cities-list-${stepId}`">
                      <option
                          v-for="city in destinationCities"
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
                  v-model="inputTransportMode"
                  placeholder="Select transport"
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

              <div class="mb-5">
                  <label class="label has-text-weight-medium has-text-grey-dark">Carpooling</label>
                  <input
                  class="input"
                  type="number"
                  v-model.number="inputCarpoolers"
                  min="1"
                  :disabled="readonlyCarpooling"
                  placeholder="Number of carpoolers"
                  />
              </div>

              <div class="mb-5">
                  <label class="checkbox has-text-grey-dark">
                      <input type="checkbox" v-model="checkIsRound" />
                      &nbsp;Round Trip
                  </label>
              </div>
          </div>


          <div class="column is-half">
              <div id="map_wrapper" style="height:100%;">
                  <l-map
                  v-if="currentStep === index"
                  ref="mapRef"
                  :bounds="initBounds"
                  >
                      <l-tile-layer
                      url="https://{s}.tile.openstreetmap.fr/hot/{z}/{x}/{y}.png"
                      attribution='&copy; OpenStreetMap contributors, Tiles style by Humanitarian OSM Team'
                      />
                      <l-marker v-if="departureCoords" :lat-lng="departureCoords" />
                      <l-marker v-if="destinationCoords" :lat-lng="destinationCoords" />
                      <l-polyline
                      ref="polylineRef"
                      v-if="departureCoords && destinationCoords"
                      :lat-lngs="[departureCoords, destinationCoords]"
                      color="rgb(231, 76, 60)"
                      />
                  </l-map>
              </div>
          </div>
      </div>
    </form>
</template>

<script setup>
import { ref, computed, watch, nextTick, defineProps } from 'vue'
import debounce from 'lodash.debounce'

import { LMap, LTileLayer, LMarker, LPolyline } from '@vue-leaflet/vue-leaflet'

import { useStore } from '@/store'
const store = useStore()

import services from '@/composables/services'


const transports = computed(() => store.state.transports)

const inputCarpoolers = ref(1)
const inputTransportMode = ref('')
const checkIsRound = ref(false)
const readonlyCarpooling = ref(true)
const departureCities = ref([])
const destinationCities = ref([])
const inputDestinationCity = ref('')
const inputDepartureCity = ref('')
const departureCoords = ref(null)
const destinationCoords = ref(null)
const destinationCountry = ref('')
const departureCountry = ref('')
const destinationCity = ref('')
const departureCity = ref('')

const props = defineProps({
  values: {
    type: Object,
    required: true,
  },
})

watch(
  () => props.values,
  (newVal) => {
    if (newVal && Object.keys(newVal).length > 0) {
      inputDepartureCity.value = newVal.departure_city
      departureCountry.value = newVal.departure_country
      departureCity.value = newVal.departure_city
      inputDestinationCity.value = newVal.destination_city
      destinationCountry.value = newVal.destination_country
      destinationCity.value = newVal.destination_city
      inputCarpoolers.value = newVal.carpooling
      inputTransportMode.value = newVal.transport.transport_name
      checkIsRound.value = newVal.is_round_trip
      readonlyCarpooling.value = ['CAB', 'CAR'].includes(inputTransportMode.value)
    }
  },
  { immediate: true }
)

watch(inputTransportMode, (newTransportMode) => {
  if (newTransportMode === 'CAB' || newTransportMode === 'CAR') {
    readonlyCarpooling.value = false
  } else {
    inputCarpoolers.value = 1
    readonlyCarpooling.value = true
  }
})

const updateDepartureCityList = debounce(async (cityName) => {
  if (cityName.length < 2) {
    departureCities.value = []
    return
  }
  try {
    const cities = await services.cities.fetch(cityName)
    departureCities.value = cities
  } catch (err) {
    console.error('Departure city fetch error:', err)
  }
}, 400)

const updateDestinationCityList = debounce(async (cityName) => {
  if (cityName.length < 2) {
    destinationCities.value = []
    return
  }
  try {
    const cities = await services.cities.fetch(cityName)
    destinationCities.value = cities
  } catch (err) {
    console.error('Destination city fetch error:', err)
  }
}, 400)

watch(inputDepartureCity, (val) => {
  updateDepartureCityList(val)
})

watch(inputDestinationCity, (val) => {
  updateDestinationCityList(val)
})

function countryCodeToFlagEmoji(countryCode) {
    if (!countryCode || typeof countryCode !== 'string') {
        return ''
    }
    return countryCode
        .toUpperCase()
        .split('')
        .map(char => String.fromCodePoint(127397 + char.charCodeAt()))
        .join('')
}

function onInputDestinationCityChange() {
  const selectedCity = destinationCities.value.find(city => {
    const cityValue = `${city.name} ${countryCodeToFlagEmoji(city.countryCode)}`
    return cityValue === inputDestinationCity.value
  })
  if (selectedCity) {
    console.log('User selected:', selectedCity)
    destinationCoords.value = { lat: selectedCity.lat, lng: selectedCity.lng }
    destinationCountry.value = selectedCity.countryCode
    destinationCity.value = selectedCity.name
  } else {
    destinationCoords.value = null
    destinationCountry.value = null
    destinationCity.value = null
  }
}

function onInputDepartureCityChange() {
  const selectedCity = departureCities.value.find(city => {
    const cityValue = `${city.name} ${countryCodeToFlagEmoji(city.countryCode)}`
    return cityValue === inputDepartureCity.value
  })
  if (selectedCity) {
    console.log('User selected:', selectedCity)
    departureCoords.value = { lat: selectedCity.lat, lng: selectedCity.lng }
    departureCountry.value = selectedCity.countryCode
    departureCity.value = selectedCity.name
  } else {
    departureCoords.value = null
    departureCountry.value = null
    departureCity.value = null
  }
}

const mapRef = ref(null)
const polylineRef = ref(null)
const initBounds = ref(null)

async function fitBoundsMap() {
  await nextTick()
  const map = mapRef.value?.mapObject || mapRef.value?.leafletObject
  const polyline = polylineRef.value?.mapObject || polylineRef.value?.leafletObject
  if (!map) {
    console.warn('Map instance not ready')
    return
  }
  if (!polyline) {
    console.warn('Polyline instance not ready')
    return
  }
  const bounds = polyline.getBounds()
  if (bounds && bounds.isValid()) {
    map.fitBounds(bounds, { animate: false })
  } else {
    console.warn('Bounds not valid')
  }
}

watch(
  () => departureCoords.value && destinationCoords.value,
  async (coordsReady) => {
    if (!coordsReady) return
    await fitBoundsMap()
  }
)

const submitForm = () => {
  emit('form-submitted', {
    transport: {
      transport_name: inputTransportMode.value,
    },
    departure_city: departureCity.value,
    departure_country: departureCountry.value,
    destination_city: destinationCity.value,
    destination_country: destinationCountry.value,
    is_round_trip: checkIsRound.value,
    carpooling: inputCarpoolers.value,
  });
};
</script>

<style scoped>
.body-tab {
  height: 70vh; 
  overflow-y: auto;  
  box-sizing: border-box;
  padding: 1rem;
}
</style>