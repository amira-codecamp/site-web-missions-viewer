<template>
  <form @submit.prevent="submitForm">

    <div class="columns">

        <div class="column is-half">

            <div class="field mb-5">
                <label class="label has-text-weight-medium has-text-grey-dark">First Name</label>
                <div class="control">
                    <input type="text" 
                    v-model="form.first_name" 
                    class="input"
                    required />
                </div>
            </div>

            <div class="field mb-5">
                <label class="label has-text-weight-medium has-text-grey-dark">Last Name</label>
                <div class="control">
                    <input type="text" 
                    v-model="form.last_name" 
                    class="input"
                    required />
                </div>
            </div>
        </div>

        <div class="column is-half">

            <div class="field mb-5">
                <label class="label has-text-weight-medium has-text-grey-dark">Email</label>
                <div class="control">
                    <input type="email"
                    v-model="form.email" 
                    class="input"
                    required />
                </div>
            </div>

            <!-- Status -->
            <div class="field mb-5">
                <label class="label has-text-weight-medium has-text-grey-dark">Status</label>
                <div class="control">
                  <input
                    class="input"
                    list="status-list"
                    v-model="form.status.status_name"
                    placeholder="Type status"
                    required
                  />
                  <datalist id="status-list">
                      <option
                          v-for="s in status"
                          :key="s.status_name"
                          :value="s.status_name"
                      />
                  </datalist>
                </div>
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
  name: 'EmployeeForm',
})

const props = defineProps({
  employee: {
    type: Object,
    required: true
  },
})

const store = useStore()

const status = computed(() => store.state.status)

const form = ref({
    employee_id: null,
    first_name: '',
    last_name: '',
    email: '',
    status: {
        status_name: ''
    }
})

const emit = defineEmits(['close'])

const submitForm = async () => {

    const email = form.value.email;
    const emailRegex1 = /^[^@]+@lipn\.fr$/;
    const emailRegex2 = /^[^@]+@lipn\.univ-paris13\.fr$/;

    if (!emailRegex1.test(email) && !emailRegex2.test(email)) {
        alert('Invalid email address. Only members of LIPN are allowed!');
        return;
    }

    try {

        await fetchToken();

        const access = store.state.accessToken;

        await services.employees.modifyEmployee(access, { ...form.value })
        alert(`Employee altered successfully!`)

        const response = await services.employees.fetchEmployees(access)
        store.setItem('employees', response.employees)

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
  if (props.employee) {
    form.value = {
      employee_id: props.employee.employee_id,
      first_name: props.employee.first_name,
      last_name: props.employee.last_name,
      email: props.employee.email,
      status: {
        status_name: props.employee.status?.status_name
      }
    }
  }
})
</script>