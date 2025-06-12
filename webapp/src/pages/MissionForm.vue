<template>
  <form @submit.prevent="submitForm">

    <!-- Administrative Number -->
    <div class="field mb-5">
        <div class="columns">
            <div class="column is-5">
                <label class="label has-text-weight-medium has-text-grey-dark">Number</label>
                <div class="control">
                    <input type="text" v-model="form.mission_num" class="input" required />
                </div>
            </div>
        </div>
    </div>

    <div class="field mb-5">
        <div class="columns">

            <!-- Start Date -->
            <div class="column is-6">
                <label class="label has-text-weight-medium has-text-grey-dark">From</label>
                <div class="control">
                    <input type="date" v-model="form.start_date" class="input" required />
                </div>
            </div>

            <!-- End Date -->
            <div class="column is-6">
                <label class="label has-text-weight-medium has-text-grey-dark">To</label>
                <div class="control">
                    <input type="date" v-model="form.end_date" class="input" required />
                </div>
            </div>

        </div>
    </div>

    <!-- Description -->
    <div class="field mb-5">
      <label class="label has-text-weight-medium has-text-grey-dark">Description</label>
      <div class="control">
        <input type="text" v-model="form.mission_desc" class="input" required />
      </div>
    </div>

    <!-- Submit -->
    <div class="field mb-5">
        <div class="control">
            <div class="columns">
                <div class="column is-4"></div>
                <div class="column is-4">
                    <button class="button is-dark is-medium">
                        <span>Add</span>
                    </button>
                </div>
                <div class="column is-4"></div>
            </div>
        </div>
    </div>

  </form>
</template>

<script setup>
import { ref } from 'vue'

import { useStore } from '@/store'

import tripsservice from '@/services/tripsservice'
import authservice from '@/services/authservice'


defineOptions({
  name: 'MissionForm',
})

const store = useStore()

const form = ref({
  start_date: '',
  end_date: '',
  mission_num: '',
  mission_desc: ''
})

const submitForm = async () => {
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

        await tripsservice.missions.createMission(access, { ...form.value })

        const response = await tripsservice.missions.fetchMissions(access)
        store.setItem('missions', response.missions)

        alert(`Mission created successfully!`)

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
