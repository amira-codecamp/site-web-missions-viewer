
<template>
    <section class="section" style="padding-top: 0.5rem;">
        <div class="container" v-if="users.length!=0">
            <div class="table-wrapper">

                <div class="columns">
                    <div class="column is-half">
                    <input
                        v-model="searchword"
                        class="input is-small"
                        type="text"
                        placeholder="Search users..."
                    />
                    </div>
                    <div class="column is-one-quarter"></div>
                    <div class="column is-one-quarter">
                        <div class="columns">
                        <div class="column is-three-third"></div>
                        <div class="column is-one-third">
                            <button 
                            class="button is-dark is-fullwidth is-small" 
                            v-if="isAdmin" 
                            @click="showUserForm(null)"
                            style="font-weight: bold;"
                            title="Add user"
                            >
                                Create User
                            </button>
                        </div>
                        </div>
                    </div>
                </div>

                <div class="table-content is-scrollable">
                    <table class="table is-fullwidth is-hoverable is-bordered is-size-7">
                    <thead>
                        <tr>
                        <th>Login</th>
                        <th>Is Active</th>
                        <th>Group</th>
                        <th>Employee</th>
                        <th colspan="2"></th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="user in filteredUsers" :key="user.login">
                        <td>{{ user.login }} </td>
                        <td>{{ user.is_active === true ? '×' : '' }}</td>
                        <td>{{ user.group.group_name }}</td>
                        <td>{{ user.employee.first_name }} {{ user.employee.last_name }}</td>
                        <td>
                            <button 
                            class="button is-link is-light is-small" 
                            v-if="isAdmin" 
                            @click="showUserForm(user)"
                            style="font-weight: bold; padding: 0 6px;"
                            title="Modify user"
                            >
                            <span class="icon is-small">
                                <i class="fas fa-pencil-alt"></i>
                            </span>
                            </button>
                        </td>
                        <td>
                            <button 
                                v-if="isAdmin"
                                class="button is-small is-danger is-light" 
                                @click="deleteUser(user)" 
                                title="Delete user"
                                style="font-weight:bold; padding: 0 6px;"
                            >
                                <span class="icon is-small">
                                <i class="fas fa-times"></i>
                                </span>
                            </button>
                        </td>
                        </tr>
                    </tbody>
                    </table>
                </div>
            </div>

            <div class="modal" :class="{ 'is-active': userFormActive }">
                <div class="modal-background" @click="hideUserForm"></div>
                <div class="modal-card" style="width: 50%;">
                <header class="modal-card-head has-background-white">
                    <p class="modal-card-title has-text-grey-dark">User Form</p>
                    <button class="delete" aria-label="close" @click="hideUserForm"></button>
                </header>
                <section class="modal-card-body has-background-light">
                    <UserForm
                    @close="hideUserForm" />
                </section>
                </div>
            </div>
        </div>
        <div class="mb-4" v-else>
            <span>No trips available.</span>
        </div>
    </section>
</template>

<script setup>
defineOptions({
  name: 'UsersPage',
})

import services from '@/services'

import { useStore } from '@/store'
import { ref, computed } from 'vue'

import UserForm from '@/pages/UserForm.vue'

const store = useStore()
const searchword = ref('')
const userFormActive = ref(false)
const selectedUser = ref(null)

const isAdmin = computed(() => store.state.isAdmin)

const users = computed(() => store.state.users)

// Table
function normalizeString(str) {
  if (!str) return ''
  return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase()
}

const filteredUsers = computed(() => {
  if (!searchword.value) return users.value
  const term = normalizeString(searchword.value)
  return users.value.filter(user => {
    const fields = [
      user.login,
      user.group.group_name,
      `${user.employee?.first_name || ''} ${user.employee?.last_name || ''}`,
    ]
    return fields.some(field => normalizeString(field).includes(term))
  })
})

// Operations on User
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

const deleteUser = async (user) => {
  try {

    await fetchToken();

    const access = store.state.accessToken;

    await services.users.deleteUser(access, user);

    const response1 = await services.users.fetchUsers(access);
    store.setItem('users', response1.users);

    alert(`User deleted successfully!`)
  
  } catch (error) {
    if (error.response?.data) {
      const messages = Object.entries(error.response.data).map(([key, val]) => `${key}: ${val}`)
      alert(messages.join('\n'))
    } else {
      alert('Something went wrong. Please try again.')
    }
  }
}

function showUserForm(user) {
  selectedUser.value = user
  userFormActive.value = true
}

function hideUserForm() {
  selectedUser.value = null
  userFormActive.value = false
}
</script>

<style scoped>
.table-content {
  overflow-y: scroll;
  height: 20rem !important;
}

.table-wrapper, .table-wrapper canvas {
  width: 100% !important;
  min-height: unset;
}
</style>