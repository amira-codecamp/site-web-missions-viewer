
<template>
    <form @submit.prevent="onSubmit">
        <div class="columns is-multiline is-variable is-5">

            <div class="column is-5">
                <!-- Mission -->
                <div class="field mb-5">
                  <label class="label has-text-weight-medium has-text-grey-dark">Mission</label>
                  <div class="columns" style="display: flex; align-items: center; justify-content: center; height: 100%;">
                    <div class="column is-8">
                      <div class="control">
                          <input
                          class="input"
                          list="missions-list"
                          v-model="selectedMission"
                          placeholder="Type mission"
                          required
                          />
                          <datalist id="missions-list">
                              <option
                                v-for="mission in missions"
                                :key="mission.mission_desc"
                                :value="mission.mission_desc"
                              > 
                                {{ mission.start_date }} -> {{ mission.end_date }}
                              </option>
                          </datalist>
                      </div>
                    </div>
                    <div class="column is-2">
                      <button class="button is-dark is-small" v-if="isManager" @click="showMissionForm()"><span>Add</span></button>
                      <div class="modal" :class="{ 'is-active': MissionFormActive }" style="z-index: 2000;">
                        <div class="modal-background" @click="hideMissionForm"></div>
                        <div class="modal-card" style="width: 30%; z-index: 2001;">
                          <header class="modal-card-head has-background-white">
                            <p class="modal-card-title has-text-grey-dark">Add a New Mission</p>
                            <button class="delete" aria-label="close" @click="hideMissionForm"></button>
                          </header>
                          <section class="modal-card-body has-background-light">
                            <MissionForm @close="hideMissionForm" />
                          </section>
                        </div>
                      </div>
                    </div>
                    <div class="column is-2"></div>
                  </div>
                </div>

                <!-- Transport -->
                <div class="field mb-5">
                    <label class="label has-text-weight-medium has-text-grey-dark">Transport</label>
                    <div class="control">
                        <input
                        class="input"
                        list="transports-list"
                        v-model="form.transport.transport_name"
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
                                :list="list1Name"
                                v-model="selectedDepartureCity"
                                placeholder="Type departure city"
                                @input="onDepartureInput"
                                required
                                />
                                <datalist :id="list1Name">
                                    <option
                                        v-for="city in departureCities"
                                        :key="city.geonameId"
                                        :value="formatCityWithFlag(city)"
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
                                :list="list2Name"
                                v-model="selectedDestinationCity"
                                placeholder="Type destination city"
                                @input="onDestinationInput"
                                required
                                />
                                <datalist :id="list2Name">
                                    <option
                                        v-for="city in destinationCities"
                                        :key="city.geonameId"
                                        :value="formatCityWithFlag(city)"
                                    />
                                </datalist>
                            </div>
                        </div>
                    </div>
                </div>

                <!-- Map Placeholder -->
                <div class="field mb-5">
                    <div id="map_wrapper" style="height: 40vh;">
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
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted } from 'vue'
import { useStore } from '@/store'
import debounce from 'lodash.debounce'
import { LMap, LTileLayer, LMarker, LPolyline } from '@vue-leaflet/vue-leaflet'
import services from '@/services'
import MissionForm from '@/pages/MissionForm.vue'

import { fetchToken } from '@/session'


defineOptions({ name: 'TripGenericForm' })

const emit = defineEmits(['submit'])

const store = useStore()

const isManager = computed(() => store.state.isManager)

const props = defineProps({
  initialForm: {
    type: Object,
    required: true
  },
  disableQuantity: {
    type: Boolean,
    required: true
  },
  list1Name: {
    type: String,
    required: true
  },
  list2Name: {
    type: String,
    required: true
  },
})

const form = ref({ ...props.initialForm })

const disableQuantity = ref(props.disableQuantity)

const list1Name = ref(props.list1Name)
const list2Name = ref(props.list2Name)

const departureCities = ref([])
const destinationCities = ref([])
const selectedMission = ref('');
const quantityField = ref(1)
const mapRef = ref(null)
const polylineRef = ref(null)
const initialBounds = ref(null)

const missions = computed(() => store.state.missions)
const transports = computed(() => store.state.transports)

const countryCodeToFlag = (countryIsoCode) => {
  if (!countryIsoCode || typeof countryIsoCode !== 'string') return ''
  return countryIsoCode.toUpperCase().replace(/./g, c => String.fromCodePoint(c.charCodeAt(0) + 127397))
}

const formatCityWithFlag = (city) => {
  const flag = countryCodeToFlag(city.countryCode)
  return `${city.name}, ${city.countryCode} ${flag}`
}

const fetchCities = async (cityName) => {
  const response = await services.cities.fetch(cityName)
  return response
}

const selectedDepartureCity = ref('');
const selectedDestinationCity = ref('');

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
  const city = departureCities.value.find(cit => formatCityWithFlag(cit) === selectedDepartureCity.value)
  return city ? [city.lat, city.lng] : null
}

const getDestinationCoords = () => {
  const city = destinationCities.value.find(cit => formatCityWithFlag(cit) === selectedDestinationCity.value)
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

const MissionFormActive = ref(false)

function showMissionForm() {
  MissionFormActive.value = true
}

function hideMissionForm() {
  MissionFormActive.value = false
}

const onSubmit = async () => {

  const [dep_city_obj, dest_city_obj] = [
    departureCities.value.find(cit => formatCityWithFlag(cit) === selectedDepartureCity.value),
    destinationCities.value.find(cit => formatCityWithFlag(cit) === selectedDestinationCity.value)
  ]

  const mission = missions.value.find(m => m.mission_desc === selectedMission.value);
  form.value.mission = mission;

  form.value.departure_country = dep_city_obj.countryCode
  form.value.departure_city = dep_city_obj.name
  form.value.destination_country = dest_city_obj.countryCode
  form.value.destination_city = dest_city_obj.name

  emit('submit', form.value, quantityField.value)
}

watch([selectedDepartureCity, selectedDestinationCity], fitBoundsMap)

onMounted(async () => {
  if (props.initialForm.departure_city) {
    const cities = await fetchCities(props.initialForm.departure_city);
    if (cities.length > 0) {
      departureCities.value = cities;
      selectedDepartureCity.value = formatCityWithFlag(cities[0]);
    }
  }

  if (props.initialForm.destination_city) {
    const cities = await fetchCities(props.initialForm.destination_city);
    if (cities.length > 0) {
      destinationCities.value = cities;
      selectedDestinationCity.value = formatCityWithFlag(cities[0]);
    }
  }

  if (props.initialForm.mission) {
    selectedMission.value = props.initialForm.mission.mission_desc;
  }
});
</script>