
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

import { fetchToken } from '@/session'

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

const submitForm = async (formData, numRows) => {
  try {

    await fetchToken();

    const access = store.state.accessToken

    for (let i = 0; i < numRows; i++) {
      await services.trips.create(access, { ...formData });
    }

    const response = await services.trips.list(access);
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