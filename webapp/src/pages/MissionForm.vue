<template>
  <form @submit.prevent="submitForm">

    <!-- Employee -->
    <div class="field mb-5">
        <label class="label has-text-weight-medium has-text-grey-dark">Employee</label>
        <div class="control">
            <input
            class="input"
            list="employees-list"
            v-model="selectedEmployee"
            placeholder="Type employee"
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
import { ref, computed, onMounted } from 'vue'

import { useStore } from '@/store'

import services from '@/services'

import { fetchToken } from '@/session'


defineOptions({
  name: 'MissionForm',
})

const emit = defineEmits(['close'])

const store = useStore()

const employees = computed(() => store.state.employees)

const props = defineProps({
  missionObj: {
    type: Object,
    required: true
  },
  task: {
    type: String,
    required: true
  }
})

const form = ref({
  mission_id: props.missionObj?.mission_id || null,
  start_date: props.missionObj?.start_date || '',
  end_date: props.missionObj?.end_date || '',
  employee: {
    'first_name': props.missionObj?.employee?.first_name || '',
    'last_name': props.missionObj?.employee?.last_name || '',
    'email': props.missionObj?.employee?.email || '',
    'status': {
        'status_name': props.missionObj?.employee?.status?.status_name || '',
    }
  },
  mission_desc: props.missionObj?.mission_desc || ''
})

const formatEmployee = (emp) => `${emp.first_name} ${emp.last_name} <${emp.email}>`

const selectedEmployee = ref(props.missionObj ? formatEmployee(props.missionObj?.employee) : '')

const submitForm = async () => {
    try {

        const employee = employees.value.find(m => formatEmployee(m) === selectedEmployee.value);
        form.value.employee = employee;

        await fetchToken();

        const access = store.state.accessToken

        if (props.task === 'add') {
            await services.missions.createMission(access, { ...form.value })
            alert(`Mission created successfully!`)
            
        } else {
            await services.missions.alterMission(access, { ...form.value })
            alert(`Mission altered successfully!`)
        }

        const response = await services.missions.fetchMissions(access)
        store.setItem('missions', response.missions)

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
  if (props.missionObj) {
    form.value = {
        mission_id: props.missionObj?.mission_id,
        start_date: props.missionObj?.start_date,
        end_date: props.missionObj?.end_date,
        employee: {
            'first_name': props.missionObj?.employee?.first_name,
            'last_name': props.missionObj?.employee?.last_name,
            'email': props.missionObj?.employee?.email,
            'status': {
                'status_name': props.missionObj?.employee?.status?.status_name,
            }
        },
        mission_desc: props.missionObj?.mission_desc
    }
    selectedEmployee.value = formatEmployee(props.missionObj.employee)
  }
})
</script>
