<template>
  <form @submit.prevent="submitForm">

    <div class="columns">

        <div class="column is-half">
            <div class="field mb-5">
                <label class="label has-text-weight-medium has-text-grey-dark">Login</label>
                <div class="control">
                    <input type="text" v-model="form.login" class="input" required />
                </div>
            </div>

            <div class="field mb-5">
                <label class="label has-text-weight-medium has-text-grey-dark">Password</label>
                <div class="control">
                    <input type="password" v-model="form.password" class="input" required />
                </div>
            </div>

            <div class="field mb-5">
                <label class="label has-text-weight-medium has-text-grey-dark">Confirm Password</label>
                <div class="control">
                    <input type="password" v-model="confirm_password" class="input" required />
                </div>
            </div>
        </div>

        <div class="column is-half">

            <!-- Group -->
            <div class="field mb-5">
                <label class="label has-text-weight-medium has-text-grey-dark">Group</label>
                <div class="control">
                    <select class="input" v-model="selectedGroup" required>
                        <option disabled value="">Select a group</option>
                        <option>admin</option>
                        <option>missionmanager</option>
                        <option>standard</option>
                    </select>
                </div>
            </div>

            <!-- Employee -->
            <div class="field mb-5">
                <label class="label has-text-weight-medium has-text-grey-dark">Employee</label>
                <div class="control">
                    <input
                    class="input"
                    list="employees-list"
                    v-model="selectedEmployee"
                    placeholder="Select employee"
                    required
                    />
                    <datalist id="employees-list">
                        <option
                            v-for="employee in employees"
                            :key="employee.email"
                            :value="formatEmployee(employee)"
                        />
                    </datalist>
                </div>
            </div>

            <div class="field mb-5">
                <label class="checkbox has-text-grey-dark">
                    <input type="checkbox" v-model="form.is_active" />
                    &nbsp;Is Active
                </label>
            </div>
        </div>

    </div>

    <!-- Submit -->
    <div class="field mb-5">
        <div class="control">
            <button class="button is-dark is-medium is-fullwidth">
                <span>Add</span>
            </button>
        </div>
    </div>

  </form>
</template>

<script setup>
import { ref, computed } from 'vue'

import { useStore } from '@/store'

import services from '@/services'


defineOptions({
  name: 'UserForm',
})

const store = useStore()

const employees = computed(() => store.state.employees)

const form = ref({
  login: '',
  password: '',
  is_active: true,
  group: {
    'group_name': 'standard',
  },
  employee: {
    'first_name': '',
    'last_name': '',
    'email': '',
    'status': {
        'status_name': '',
    }
  },
  'date_joined': new Date().toISOString().split('T')[0],
  'last_login': new Date().toISOString(),
})

const confirm_password = ref('');

const selectedGroup = ref('standard');

const formatEmployee = (emp) => `${emp.first_name} ${emp.last_name} <${emp.email}>`

const selectedEmployee = ref('');

const emit = defineEmits(['close'])

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

const submitForm = async () => {

    if (confirm_password.value !== form.value.password) {
      alert("Passwords do not match.");
      return;
    }

    try {

        const employee = employees.value.find(m => formatEmployee(m) === selectedEmployee.value);
        form.value.employee = employee;

        form.value.group = { group_name: selectedGroup.value };

        await fetchToken();

        const access = store.state.accessToken

        await services.users.createUser(access, { ...form.value })

        const response = await services.users.fetchUsers(access)
        store.setItem('users', response.users)

        alert(`User created successfully!`)

        emit('close')

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