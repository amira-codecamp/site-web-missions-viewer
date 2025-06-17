
<template>
    <div class="box has-background-white-bis">
        <TripGenericForm :disableQuantity="false" :initialForm="form" @submit="submitForm" :list1Name="'depcities_listadd'" :list2Name="'destcities_listadd'" />
    </div>
</template>

<script setup>

import { ref } from 'vue'
import { useStore } from '@/store'

import TripGenericForm from '@/pages/TripGenericForm.vue'

import services from '@/services'

const store = useStore()

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

const fetchToken = async () => {
  try {
    const refresh = store.state.refreshToken;
    const responsetok = await services.auth.refresh(refresh);
    store.setItem("accessToken", responsetok.access);

  } catch (error) {
    alert("Session expired. Please login again.");

    store.clearItem('trips');
    store.clearItem('employees');
    store.clearItem('users');
    store.clearItem('transports');
    store.clearItem('missions');
    store.clearItem('isManager');
    store.clearItem('isAdmin');
    store.clearItem('logged');
    store.clearItem('accessToken');
    store.clearItem('refreshToken');

    window.location.href = '/login';
    return;
  }
}

const submitForm = async (formData, numRows) => {
  try {

    await fetchToken();

    const access = store.state.accessToken

    for (let i = 0; i < numRows; i++) {
      await services.trips.createTrip(access, { ...formData });
    }

    const response = await services.trips.fetchTrips(access);
    store.setItem('trips', response.trips)

    alert(`${numRows} trip${numRows === 1 ? '' : 's'} created successfully!`)

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