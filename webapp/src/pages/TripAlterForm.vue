
<template>
    <div class="box has-background-white-bis">
        <TripGenericForm :disableQuantity="true" :initialForm="form" @submit="submitForm" v-if="isFormReady" :list1Name="'depcities_listalter'" :list2Name="'destcities_listalter'"/>
    </div>
</template>

<script setup>

import { ref, onMounted, watch } from 'vue'
import { useStore } from '@/store'

import TripGenericForm from '@/pages/TripGenericForm.vue'

import services from '@/services'
import { fetchToken } from '@/session'

const store = useStore()

const props = defineProps({
  trip: {
    type: Object,
    required: true,
  },
})

const isFormReady = ref(false)

const form = ref({
    mission: {
      start_date: '',
      end_date: '',
      mission_desc: '',
      employee: {
        first_name: '',
        last_name: '',
        email: '',
        status: {
          status_name: ''
        },
      },
    },
    transport: {
      transport_name: '',
    },
    departure_city: '',
    departure_country: '',
    destination_city: '',
    destination_country: '',
    is_round_trip: false,
    carpooling: 1,
    carbon_footprint: null,
})

const initializeForm = async () => {

    if (props.trip) {
        const trip = props.trip

        form.value.trip_id = trip.trip_id
        form.value.mission = trip.mission
        form.value.transport = trip.transport
        form.value.is_round_trip = trip.is_round_trip
        form.value.carpooling = trip.carpooling
        form.value.departure_city = trip.departure_city
        form.value.departure_country = trip.departure_country
        form.value.destination_city = trip.destination_city
        form.value.destination_country = trip.destination_country

        isFormReady.value = true
    }
}

const submitForm = async (formData, numRows) => {
  try {

    await fetchToken();

    const access = store.state.accessToken

    await services.trips.alterTrip(access, { ...formData });

    const response = await services.trips.fetchTrips(access);
    store.setItem('trips', response.trips);

    alert('Trip updated successfully!');

    setTimeout(() => {}, 1000)

  } catch (error) {
    if (error.response?.data) {
      const messages = Object.entries(error.response.data).map(([key, val]) => `${key}: ${val}`)
      alert(messages.join('\n'))
    } else {
      alert('Something went wrong. Please try again.')
    }
  }
}

onMounted(() => {
  initializeForm()
})

watch(() => props.trip, () => {
  isFormReady.value = false
  initializeForm()
})

</script>