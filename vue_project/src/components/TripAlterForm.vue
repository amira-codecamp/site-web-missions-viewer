<template>
  <div v-if="formReady" class="container">
    <div class="mb-5">
      <label class="label has-text-weight-medium has-text-grey-dark">Employee</label>
      <input
      class="input"
      :value="`${form.mission.employee.first_name} ${form.mission.employee.last_name}`"
      readonly
      required
      />
    </div>

    <div class="mb-5">
      <label class="label has-text-weight-medium has-text-grey-dark">Dates</label>
      <input
      class="input"
      :value="`${form.mission.start_date} To ${form.mission.end_date}`"
      readonly
      required
      />
    </div>

    <div class="mb-5">
      <label class="label has-text-weight-medium has-text-grey-dark">Mission</label>
      <input
      class="input"
      :value="`${form.mission.mission_desc}`"
      readonly
      required
      />
    </div>

    <TripStepForm 
    @form-submitted="onFormSubmit" 
    :values="values"
    />
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'

import TripStepForm from '@/components/TripStepForm.vue'

import { useStore } from '@/store'
const store = useStore()

import services from '@/composables/services'
import { fetchToken } from '@/composables/session'


const formReady = ref(false)

const values = ref({
  departure_city: '',
  departure_country: '',
  destination_city: '',
  destination_country: '',
  is_round_trip: false,
  carpooling: 1,
  transport: '',
})

const form = ref({
  trip_id: null,
  mission: null,
  ...values.value,
})

const props = defineProps({
  trip: {
    type: Object,
    required: true,
  },
})

watch(() => props.trip, (trip) => {
  if (
    trip &&
    Object.keys(trip).length > 0 &&
    trip.trip_id
  ) {
    values.value = {
      departure_city: trip.departure_city,
      departure_country: trip.departure_country,
      destination_city: trip.destination_city,
      destination_country: trip.destination_country,
      is_round_trip: trip.is_round_trip,
      carpooling: trip.carpooling,
      transport: trip.transport?.transport_name,
    };
    form.value = {
      trip_id: trip.trip_id,
      mission: trip.mission,
      ...values.value,
    };
    formReady.value = true;
  }
}, { immediate: true });

const onFormSubmit = async (data) => {
  try {
    await fetchToken();
    const access = store.state.accessToken
    Object.assign(form.value, data);
    await services.trips.update(access, form.value.trip_id, { ...form.value });
    const response = await services.trips.list(access);
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
</script>