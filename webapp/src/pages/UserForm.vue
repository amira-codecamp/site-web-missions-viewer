<template>
  <form @submit.prevent="submitForm">

    <div class="columns">

        <div class="column is-5">
            <div class="field mb-5">
                <label class="label has-text-weight-medium has-text-grey-dark">Login</label>
                <div class="control">
                    <input type="text" 
                    v-model="form.login" 
                    class="input" 
                    :readonly="props.task === 'modify'" 
                    required />
                </div>
            </div>

            <div class="field mb-5" v-if="props.task==='add'">
                <label class="label has-text-weight-medium has-text-grey-dark">Password</label>
                <div class="control">
                    <input type="password" 
                    v-model="form.password" 
                    class="input" 
                    required />
                </div>
            </div>

            <div class="field mb-5" v-if="props.task==='add'">
                <label class="label has-text-weight-medium has-text-grey-dark">Confirm Password</label>
                <div class="control">
                    <input type="password" v-model="confirm_password" class="input" required />
                </div>
            </div>
        </div>

        <div class="column is-7">

            <!-- Group -->
            <div class="field mb-5">
                <label class="label has-text-weight-medium has-text-grey-dark">Group</label>
                <div class="control">
                  <input
                    class="input"
                    list="groups-list"
                    v-model="form.group.group_name"
                    placeholder="Type group"
                    required
                  />
                  <datalist id="groups-list">
                      <option
                          v-for="group in groups"
                          :key="group.group_name"
                          :value="group.group_name"
                      />
                  </datalist>
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
                    &nbsp;<b>Is Active</b>
                </label>
            </div>

        </div>

    </div>

    <!-- Submit -->
    <div class="field mb-5" style="display: flex; justify-content: center;">
        <div class="control" style="width: 80%;">
            <button class="button is-dark is-medium is-fullwidth">
                <span>Submit</span>
            </button>
        </div>
    </div>

  </form>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'

import { useStore } from '@/store'

import services from '@/services'

import { fetchToken } from '@/session'


defineOptions({
  name: 'UserForm',
})

const props = defineProps({
  user: {
    type: Object,
    required: true
  },
  task: {
    type: String,
    required: true
  }
})

const store = useStore()

const employees = computed(() => store.state.employees)

const groups = computed(() => store.state.groups)

const form = ref({
  login: props.user?.login || '',
  password: '',
  is_active: props.user?.is_active ?? true,
  group: {
    group_name: props.user?.group?.group_name || 'standard',
  },
  employee: props.user?.employee || {
    first_name: '',
    last_name: '',
    email: '',
    status: {
      status_name: '',
    },
  },
  date_joined: props.user?.date_joined || new Date().toISOString().split('T')[0],
  last_login: props.user?.last_login || new Date().toISOString(),
})

const formatEmployee = (emp) => `${emp.first_name} ${emp.last_name} <${emp.email}>`

const confirm_password = ref('');

const selectedEmployee = ref(props.user ? formatEmployee(props.user.employee) : '')

const emit = defineEmits(['close'])

const submitForm = async () => {

    try {

        await fetchToken();

        const access = store.state.accessToken

        const employee = employees.value.find(m => formatEmployee(m) === selectedEmployee.value);
        form.value.employee = employee;

        if (props.task === 'add') {
            if (confirm_password.value !== form.value.password) {
                alert("Passwords do not match.");
                return;
            }

            await services.users.createUser(access, { ...form.value })
            alert(`User created successfully!`)

        } else {
            await services.users.modifyUser(access, { ...form.value })
            alert(`User altered successfully!`)
        }

        const response = await services.users.fetchUsers(access)
        store.setItem('users', response.users)

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

onMounted(() => {
  if (props.user) {
    form.value = {
      login: props.user.login,
      password: '',
      is_active: props.user.is_active,
      group: {
        group_name: props.user.group?.group_name
      },
      employee: props.user.employee,
      date_joined: props.user.date_joined,
      last_login: props.user.last_login
    }
  }
})
</script>