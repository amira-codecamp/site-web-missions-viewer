<template>
  <div class="page-header">
    <nav class="navbar is-light">
      <div class="navbar-brand">
        <div class="navbar-item">
          <span class="has-text-weight-semibold is-size-6">{{ user }}</span>
        </div>

        <a
          role="button"
          class="navbar-burger"
          :class="{ 'is-active': isBurgerActive }"
          aria-label="menu"
          aria-expanded="false"
          @click="toggleBurger"
        >
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div class="navbar-menu" :class="{ 'is-active': isBurgerActive }">
        <div class="navbar-end">
          <a class="navbar-item" @click="viewTrips">Trips</a>
          <a class="navbar-item" @click="logout">Logout</a>
        </div>
      </div>
    </nav>
  </div>

  <div class="page-body">
    <router-view />
  </div>
</template>

<script setup>
defineOptions({ name: 'Dashboard' })

import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useStore } from '@/store'

import tripsservice from '@/services/tripsservice'
import employeesservice from '@/services/employeesservice'
import transportsservice from '@/services/transportsservice'

const store = useStore()
const router = useRouter()

const isBurgerActive = ref(false)
const user = computed(() => store.state.user)

function toggleBurger() {
  isBurgerActive.value = !isBurgerActive.value
}

function logout() {
  store.clearItem('trips')
  store.clearItem('employees')
  store.clearItem('transports')
  store.clearItem('missions')
  store.clearItem('isManager')
  store.clearItem('user')
  store.clearItem('accessToken')
  store.clearItem('refreshToken')

  router.push('/login')
}

function viewTrips() {
  router.push('/member/trips')
}

async function fetchData() {
  const accessToken = store.state.accessToken

  try {
    const tripsResponse = await tripsservice.trips.fetchTrips(accessToken)
    store.setItem('trips', tripsResponse.trips)
  } catch (error) {
    console.error('Error fetching trips:', error)
    return
  }

  try {
    const [transportsRes, employeesRes, missionsRes] = await Promise.all([
      transportsservice.fetchTransports(accessToken),
      employeesservice.fetchEmployees(accessToken),
      tripsservice.missions.fetchMissions(accessToken),
    ])
    store.setItem('transports', transportsRes.transports)
    store.setItem('employees', employeesRes.employees)
    store.setItem('missions', missionsRes.missions)

    store.setItem('isManager', true)
  } catch (error) {
    if (error?.response?.status === 401) {
      store.setItem('isManager', false)
    } else {
      console.error('Error fetching manager data:', error)
    }
  }
}

onMounted(() => {
  document.title = 'Dashboard | LIPN-carbon'
  fetchData()
})
</script>