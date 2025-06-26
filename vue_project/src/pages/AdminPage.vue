
<template>
    <section class="section" style="padding-top: 0.5rem;">
      <div class="columns is-multiline">
        <div class="column is-two-quarter">
          <input
            v-model="searchword"
            class="input is-small is-fullwidth"
            type="text"
            placeholder="Search employees..."
          />
        </div>
        <div class="column is-4"></div>
        <div class="column is-2">
          <button class="button is-secondary is-small" @click="importFromCSV">
            <span class="icon is-small">
              <i class="fas fa-file-import"></i>
            </span>
            <span>Import employees</span>
          </button>
          <input type="file" id="csvInput" accept=".csv" style="display:none" />
        </div>
        <div class="column is-half">
          <div class="container" v-if="employees.length!=0">
            <div class="table-wrapper">

              <div class="table-content is-scrollable">
                <table class="table is-fullwidth is-hoverable is-bordered is-size-7">
                <thead>
                    <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Status</th>
                    <th>
                    </th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="employee in filteredData.employees" :key="employee.email">
                    <td>{{ employee.first_name }} {{ employee.last_name }}</td>
                    <td>{{ employee.email }}</td>
                    <td>{{ employee.status.status_name }}</td>
                    <td>
                        <button 
                        class="button is-link is-light is-small" 
                        v-if="isAdmin" 
                        @click="showEmployeeForm(employee)"
                        style="font-weight: bold; padding: 0 6px;"
                        title="Modify employee"
                        >
                        <span class="icon is-small">
                            <i class="fas fa-pencil-alt"></i>
                        </span>
                        </button>
                    </td>
                    </tr>
                </tbody>
                </table>
              </div>

              <div class="modal" :class="{ 'is-active': employeeFormActive }">
                <div class="modal-background" @click="hideEmployeeForm"></div>
                <div class="modal-card" style="width: 50%;">
                <header class="modal-card-head has-background-white">
                    <p class="modal-card-title has-text-grey-dark">Employee Form</p>
                    <button class="delete" aria-label="close" @click="hideEmployeeForm"></button>
                </header>
                <section class="modal-card-body has-background-light">
                    <EmployeeForm
                    :employee="employeeInfo"
                    :key="formEmployeeKey"
                    @close="hideEmployeeForm" />
                </section>
                </div>
              </div>
            </div>
          </div>
          <div class="mb-4" v-else>
              <span>No employees available.</span>
          </div>
        </div>

        <div class="column is-half">
          <div class="container" v-if="users.length!=0">
            <div class="table-wrapper">

              <div class="table-content is-scrollable">
                <table class="table is-fullwidth is-hoverable is-bordered is-size-7">
                <thead>
                    <tr>
                    <th>Login</th>
                    <th>Is Active</th>
                    <th>Group</th>
                    <th>Employee</th>
                    <th colspan="2">
                      <button 
                      class="button is-dark is-small is-fullwidth" 
                      v-if="isAdmin" 
                      @click="showUserForm(null, 'add')"
                      style="font-weight: bold;"
                      title="Add user"
                      >
                        Add User
                      </button>
                    </th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="user in filteredData.users" :key="user.login">
                    <td>{{ user.login }} </td>
                    <td>{{ user.is_active === true ? '×' : '' }}</td>
                    <td>{{ user.group.group_name }}</td>
                    <td>{{ user.employee.first_name }} {{ user.employee.last_name }}</td>
                    <td>
                        <button 
                        class="button is-link is-light is-small" 
                        v-if="isAdmin" 
                        @click="showUserForm(user, 'modify')"
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
                            @click="deleteUser(user.user_id)" 
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

              <div class="modal" :class="{ 'is-active': userFormActive }">
                <div class="modal-background" @click="hideUserForm"></div>
                <div class="modal-card" style="width: 50%;">
                <header class="modal-card-head has-background-white">
                    <p class="modal-card-title has-text-grey-dark">User Form</p>
                    <button class="delete" aria-label="close" @click="hideUserForm"></button>
                </header>
                <section class="modal-card-body has-background-light">
                    <UserForm
                    :user = "selectedUser"
                    :key="userFormKey"
                    :task="taskValue"
                    @close="hideUserForm" />
                </section>
                </div>
              </div>
            </div>
          </div>
          <div class="mb-4" v-else>
              <span>No users available.</span>
          </div>
        </div>
      </div>
    </section>
</template>

<script setup>
defineOptions({
  name: 'UsersPage',
})

import services from '@/services'

import { useStore } from '@/store'
import { ref, computed, watch } from 'vue'

import UserForm from '@/pages/UserForm.vue'
import EmployeeForm from '@/pages/EmployeeForm.vue'

import { fetchToken } from '@/session'

const store = useStore()
const searchword = ref('')
const userFormActive = ref(false)
const employeeFormActive = ref(false)
const selectedUser = ref(null)
const employeeInfo = ref(null)
const userFormKey = ref(0);
const formEmployeeKey = ref(0);
const taskValue = ref('');

const isAdmin = computed(() => store.state.isAdmin)

const users = computed(() => store.state.users)

const employees = computed(() => store.state.employees)

// Table
function normalizeString(str) {
  if (!str) return ''
  return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase()
}

const filteredData = computed(() => {
  if (!searchword.value) {
    return {
      employees: employees.value,
      users: users.value,
    }
  }
  const term = normalizeString(searchword.value)
  const matchedEmployees = employees.value.filter(employee => {
    const fields = [
      employee.email,
      employee.status?.status_name || '',
      `${employee.first_name || ''} ${employee.last_name || ''}`,
    ]
    return fields.some(field => normalizeString(field).includes(term))
  })
  const matchedEmployeeIds = new Set(matchedEmployees.map(e => e.employee_id))
  const matchedUsers = users.value.filter(user => matchedEmployeeIds.has(user.employee?.employee_id))
  return {
    employees: matchedEmployees,
    users: matchedUsers,
  }
})

async function importFromCSV() {
  const input = document.getElementById('csvInput')
  if (!input) return
  input.value = ''

  input.addEventListener('change', async function handler(event) {
    const file = event.target.files[0]
    if (!file) return

    const reader = new FileReader()
    reader.onload = async e => {
      const csvContent = e.target.result
      console.log('CSV content:\n' + csvContent)

      // try {
      //   await fetchToken()
      //   const token = store.state.accessToken
      //   const response = await services.employees.postCSV(token, {'csv_content': csvContent})
      //   console.log('Backend response:', response)
      //   alert('CSV posted successfully!')
      // } catch (error) {
      //   console.error('Failed to post CSV:', error)
      //   alert('Posting CSV failed: ' + (error.response?.data || error.message))
      // }
    }
    reader.readAsText(file)
    input.removeEventListener('change', handler)
  })

  input.click()
}

// Operations on User / Employee

const deleteUser = async (user_id) => {
  try {

    await fetchToken();

    const access = store.state.accessToken;

    await services.users.destroy(access, user_id);

    const response1 = await services.users.list(access);
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

function showUserForm(user, task) {
  if (task === 'modify') {
    user.password = '*****'
  }
  selectedUser.value = user
  taskValue.value = task
  userFormActive.value = true
}

function showEmployeeForm(employee) {
  employeeInfo.value = employee
  employeeFormActive.value = true
}

function hideUserForm() {
  selectedUser.value = null
  userFormActive.value = false
}

function hideEmployeeForm() {
  employeeInfo.value = null
  employeeFormActive.value = false
}

watch(selectedUser, () => {
  userFormKey.value++;
})

watch(employeeInfo, () => {
  formEmployeeKey.value++;
})
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