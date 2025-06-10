
<template>
    <div class="box has-background-white-bis">
        <TripGenericForm :disableQuantity="false" :initialForm="form" @submit="submitForm" :list1Name="'depcities_listadd'" :list2Name="'destcities_listadd'" />
    </div>
</template>

<script setup>

import { ref } from 'vue'
import { useStore } from '@/store'

import TripGenericForm from '@/pages/TripGenericForm.vue'

import tripsservice from '@/services/tripsservice'
import authservice from '@/services/authservice'

const store = useStore()

const form = ref({
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
})

const submitForm = async (formData, numRows) => {
  try {

    try {
        const refresh = store.state.refreshToken
        const responsetok = await authservice.refresh(refresh)
        store.setItem("accessToken", responsetok.access)

    } catch (error) {
        alert("Session expired. Please login again.")

        store.clearItem('trips')
        store.clearItem('employees')
        store.clearItem('transports')
        store.clearItem('missions')
        store.clearItem('isManager')
        store.clearItem('user')
        store.clearItem('accessToken')
        store.clearItem('refreshToken')

        window.location.href = '/login'
        return
    }

    const access = store.state.accessToken

    for (let i = 0; i < numRows; i++) {
        await tripsservice.trips.createTrip(access, { ...formData })
    }

    const response = await tripsservice.trips.fetchTrips(access)
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