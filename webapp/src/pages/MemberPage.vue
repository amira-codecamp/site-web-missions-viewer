<template>
  <div class="page-header">
    <nav class="navbar is-light">
      <div class="navbar-brand">
        <div class="navbar-item">
          <span class="has-text-weight-semibold is-size-6">{{ logged }}</span>
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
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div class="navbar-menu" :class="{ 'is-active': isBurgerActive }">
        <div class="navbar-end">
          <a class="navbar-item" @click="viewTrips" v-if="!isAdmin">Trips</a>
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

import services from '@/services'

const store = useStore()
const router = useRouter()

const isBurgerActive = ref(false)
const logged = computed(() => store.state.logged)
const isAdmin = computed(() => store.state.isAdmin)

function toggleBurger() {
  isBurgerActive.value = !isBurgerActive.value
}

function logout() {
  store.clearItem('trips')
  store.clearItem('employees')
  store.clearItem('transports')
  store.clearItem('missions')
  store.clearItem('users')
  store.clearItem('isManager')
  store.clearItem('isAdmin')
  store.clearItem('logged')
  store.clearItem('accessToken')
  store.clearItem('refreshToken')

  router.push('/login')
}

function viewTrips() {
  router.push('/member/trips')
}

async function getTransports(accessToken) {
  try {
    const transportsResponse = await services.transports.fetchTransports(accessToken);
    store.setItem('transports', transportsResponse.transports);
  } catch (error) {
    console.error('Error fetching transports:', error);
  }
}

async function getTrips(accessToken) {
  try {
    const tripsResponse = await services.trips.fetchTrips(accessToken);
    store.setItem('trips', tripsResponse.trips);
  } catch (error) {
    console.error('Error fetching trips:', error);
  }
}

async function getEmployees(accessToken) {
  try {
    const employeesResponse = await services.employees.fetchEmployees(accessToken);
    store.setItem('employees', employeesResponse.employees);
  } catch (error) {
    console.error('Error fetching employees:', error);
  }
}

async function getMissions(accessToken) {
  try {
    const missionsResponse = await services.missions.fetchMissions(accessToken);
    store.setItem('missions', missionsResponse.missions);
    store.setItem('isManager', true);
  } catch (error) {
    console.error('Error fetching missions:', error);
  }
}

async function getUsers(accessToken) {
  try {
    const usersResponse = await services.users.fetchUsers(accessToken);
    store.setItem('users', usersResponse.users);
    store.setItem('isAdmin', true);
  } catch (error) {
    console.error('Error fetching users:', error);
  }
}

async function fetchData() {
  const accessToken = store.state.accessToken;

  await Promise.all([
    getTransports(accessToken),
    getTrips(accessToken),
    getMissions(accessToken),
    getEmployees(accessToken),
    getUsers(accessToken),
  ]);
}

onMounted(() => {
  document.title = 'Dashboard | LIPN-carbon'
  fetchData()
})
</script>