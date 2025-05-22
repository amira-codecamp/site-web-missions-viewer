
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
          <div class="field mb-5">
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
              <PasswordPrompt ref="passwordPrompt" />
              <button class="button is-dark is-fullwidth is-medium">
                + Add Trip
              </button>
            </div>
          </div>

        </div>
      </div>
    </form>
  </div>
</template>

<script>
import tripsservice from '@/services/tripsservice'
import authservice from '@/services/authservice'
import geonamesservice from '@/services/geonamesservice'
import emissionsservice from '@/services/emissionsservice'
import debounce from 'lodash.debounce'
import PasswordPrompt from '@/components/PasswordPrompt.vue'
import { LMap, LTileLayer, LMarker, LPolyline } from '@vue-leaflet/vue-leaflet'

export default {
  name: 'TripForm',
  components: {
    PasswordPrompt,
    LMap, 
    LTileLayer, 
    LMarker,
    LPolyline
  },
  data() {
    return {
      form: {
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
      },
      departureCities: [],
      destinationCities: [],
      quantityField: 1,
      selectedDepartureCity: '',
      selectedDestinationCity: '',
      initialBounds: null
    }
  },
  computed: {
    missions() {
      return this.$store.state.missions;
    },
    employees() {
      return this.$store.state.employees;
    },
    transports() {
      return this.$store.state.transports;
    },
  },
  methods: {
    formatEmployee(emp) {
      return `${emp.first_name} ${emp.last_name} <${emp.email}>`;
    },
    countryCodeToFlag(countryIsoCode) {
      if (!countryIsoCode || typeof countryIsoCode !== 'string') {
        return '';
      }
      return countryIsoCode
        .toUpperCase()
        .replace(/./g, c => String.fromCodePoint(c.charCodeAt(0) + 127397));
    },
    formatCity(city) {
      const country_flag = this.countryCodeToFlag(city.countryCode);
      return `${city.name}, ${city.countryName} ${country_flag}`;
    },
    async fetchCities(cityName) {
      const response = await geonamesservice.fetchCities(cityName);
      return response;
    },
    callGeoName: debounce(function(cityName, targetKey) {
      if (cityName.length >= 2) {
        this.fetchCities(cityName)
          .then(response => {
            this[targetKey] = response;
          })
          .catch(err => {
            console.error('GeoName fetch error:', err);
          });
      }
    }, 400),
    onDepartureInput() {
      this.callGeoName(this.selectedDepartureCity, 'departureCities');
    },
    onDestinationInput() {
      this.callGeoName(this.selectedDestinationCity, 'destinationCities');
    },
    getDepartureCoords() {
      const city = this.departureCities.find(cit => this.formatCity(cit) === this.selectedDepartureCity);
      return city ? [city.lat, city.lng] : null;
    },
    getDestinationCoords() {
      const city = this.destinationCities.find(cit => this.formatCity(cit) === this.selectedDestinationCity);
      return city ? [city.lat, city.lng] : null;
    },
    async fitBoundsMap() {
      await this.$nextTick();

      const map = this.$refs.mapRef?.mapObject || this.$refs.mapRef?.leafletObject;
      const polyline = this.$refs.polylineRef?.leafletObject;

      if (map && polyline) {
        const bounds = polyline.getBounds();
        if (bounds.isValid()) {
          map.fitBounds(bounds, { animate: false });
        } else {
          console.warn('Bounds invalid');
        }
      } else {
        console.warn('Map or polyline not found');
      }
    },
    async submitForm() {
      try {
        const pwd = await this.$refs.passwordPrompt.open();
        if (!pwd) {
          return;
        }
        const credentials = { login: this.$store.state.user, password: pwd };
        const { access, _ } = await authservice.login(credentials);

        this.form.employee = this.employees.find(emp => this.formatEmployee(emp) === this.selectedEmployee);

        const city1 = this.departureCities.find(cit => this.formatCity(cit) === this.selectedDepartureCity);
        this.form.departure_country = city1.countryName;
        this.form.departure_city = city1.name;

        const city2 = this.destinationCities.find(cit => this.formatCity(cit) === this.selectedDestinationCity);
        this.form.destination_country = city2.countryName;
        this.form.destination_city = city2.name;

        const mission = this.missions.find(mission => mission.mission_num === this.form.mission_num);
        const full_year = new Date(mission.start_date).getFullYear().toString();

        const payload = {
          transport: this.form.transport_name,
          departure_country: city1.countryCode,
          destination_country: city2.countryCode,
          departure_lat: city1.lat,
          departure_long: city1.lng,
          destination_lat: city2.lat,
          destination_long: city2.lng,
          carpooling: this.form.carpooling,
          year: full_year,
          is_round_trip: this.form.is_round_trip,
        };

        const response0 = await emissionsservice.getCarbonFootprint(payload, access);
        this.form.carbon_footprint = Number(Number(response0.carbon_footprint).toFixed(2));

        const numRows = this.quantityField;
        for (let i = 0; i < numRows; i++) {
          await tripsservice.trips.createTrip(access, {
            ...this.form,
          });
        }

        const response = await tripsservice.trips.fetchTrips(access);
        this.$store.dispatch('setTrips', response.trips);

        alert(`${numRows} trip${numRows === 1 ? '' : 's'} created successfully!`);

        setTimeout(() => {
          this.$emit('close');
        }, 1000);
      } catch (error) {
        if (error.response && error.response.data) {
          const messages = [];
          for (const property in error.response.data) {
            messages.push(`${property}: ${error.response.data[property]}`);
          }
          alert(messages.join('\n'));
        } else {
          alert('Something went wrong. Please try again.');
        }
      }
    },
  },
  watch: {
    selectedDepartureCity() {
      this.fitBoundsMap();
    },
    selectedDestinationCity() {
      this.fitBoundsMap();
    }
  },
}
</script>