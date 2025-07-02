<template>

    <form-wizard
    ref="wizard"
    :start-index="currentStep"
    @on-complete="onSubmit"
    @on-change="onStepChange"
    :key="steps.length"
    >
        <tab-content title="Mission Details" :before-change="validateMissionDetails">
            <div class="body-tab">
                <div class="mb-5">
                    <label class="label has-text-weight-medium has-text-grey-dark">Employee</label>
                    <input
                    class="input"
                    list="employees-list"
                    v-model="inputEmployeeEmail"
                    placeholder="Select employee"
                    required
                    />
                    <datalist id="employees-list">
                        <option
                            v-for="employee in employees"
                            :key="employee.employee_id"
                            :value="employee.email"
                        >
                            {{ employee.first_name }} {{ employee.last_name }}
                        </option>
                    </datalist>
                </div>

                <div class="mb-5">
                    <label class="label has-text-weight-medium has-text-grey-dark">From</label>
                    <input type="date" v-model="inputStartDate" class="input" required />
                </div>

                <div class="mb-5">
                    <label class="label has-text-weight-medium has-text-grey-dark">To</label>
                    <input type="date" v-model="inputEndDate" class="input" required />
                </div>

                <div class="mb-5">
                    <label class="label has-text-weight-medium has-text-grey-dark">Mission</label>
                    <input
                    class="input"
                    list="missions-list"
                    v-model="inputMissionDesc"
                    :disabled="readonlyMission"
                    placeholder="Type mission"
                    required
                    />
                    <datalist id="missions-list">
                        <option
                            v-for="mission in filteredMissions"
                            :key="mission.mission_id"
                            :value="mission.mission_desc"
                        >
                        </option>
                    </datalist>
                </div>
            </div>
            
        </tab-content>

        <tab-content
        v-for="(step, index) in steps"
        :key="step.id"
        :title="step.title"
        :before-change="validateTripDetails"
        >
            <TripStepForm :key="step.id" :stepId="step.id"></TripStepForm>

            <div class="buttons is-right">
              <button class="button is-secondary" type="button" @click="removeStep" v-if="steps.length !== 1">
                  <i class="fas fa-minus"></i>
              </button>
              <button class="button is-secondary" type="button" @click="addStep" v-if="step.id !== 0">
                  <i class="fas fa-plus"></i>
              </button>
          </div>
        </tab-content>

    </form-wizard>

</template>

<script setup>
import { ref, computed, watch, defineExpose } from 'vue'

import { useStore } from '@/store'
const store = useStore()

import services from '@/composables/services'
import { fetchToken } from '@/composables/session'

import TripStepForm from '@/components/TripStepForm.vue'

import { FormWizard, TabContent } from 'vue3-form-wizard'
import 'vue3-form-wizard/dist/style.css'

const employees = computed(() => store.state.employees)
const missions = computed(() => store.state.missions)
const filteredMissions = ref([])

const inputEmployeeEmail = ref('')
const inputMissionDesc = ref('')
const inputStartDate = ref('')
const inputEndDate = ref('')
const readonlyMission = ref(true)

function updateMissions() {
  const employeeObj = employees.value.find(emp => emp.email === inputEmployeeEmail.value)
  if (employeeObj) {
    filteredMissions.value = missions.value.filter(mission => {
      const isEmployeeMatch = mission.employee.employee_id === employeeObj.employee_id
      const isStartDateMatch = inputStartDate.value
        ? mission.start_date === inputStartDate.value
        : true
      const isEndDateMatch = inputEndDate.value
        ? mission.end_date === inputEndDate.value
        : true
      return isEmployeeMatch && isStartDateMatch && isEndDateMatch
    })
    readonlyMission.value = false
  } else {
    filteredMissions.value = []
    readonlyMission.value = true
  }
}

watch(inputStartDate, (newStartDate) => {
  inputEndDate.value = newStartDate
})

watch(
  [inputEmployeeEmail, inputStartDate, inputEndDate],
  ([newEmail, newStart, newEnd], [oldEmail, oldStart, oldEnd]) => {
    if (newEmail && newStart && newEnd &&
        (newEmail !== oldEmail || newStart !== oldStart || newEnd !== oldEnd)) {
      updateMissions()
    }
  }
)

const wizard = ref(null)
const currentStep = ref(0)

const steps = ref([
  { id: 1, title: 'Trip 1' }
])

function updateStepTitles() {
  steps.value.forEach((step, index) => {
    step.title = `Trip ${index + 1}`
    step.id = index + 1
  })
}

function addStep() {
    steps.value.push({
        title: `Step ${steps.value.length + 1}`,
    });
    currentStep.value = steps.value.length - 1;
    updateStepTitles();
}

function removeStep() {
  if (steps.value.length > 1) {
    steps.value.pop()
    steps.value = [...steps.value]
    updateStepTitles()
  }
}

function onStepChange(newIndex) {
  currentStep.value = newIndex
}

// function validateMissionDetails() {
//   if (!inputEmployeeEmail.value) {
//     alert('Employee email is required.')
//     return false
//   }
//   if (!inputStartDate.value) {
//     alert('Start date is required.')
//     return false
//   }
//   if (!inputEndDate.value) {
//     alert('End date is required.')
//     return false
//   }
//   if (!inputMissionDesc.value) {
//     alert('Mission description is required.')
//     return false
//   }
//   const regex1 = /^[^@]+@lipn\.fr$/
//   const regex2 = /^[^@]+@lipn\.univ-paris13\.fr$/
//   if (!regex1.test(inputEmployeeEmail.value) && !regex2.test(inputEmployeeEmail.value)) {
//     alert('Employee email must be from lipn domains.')
//     return false
//   }
//   if (inputStartDate.value > inputEndDate.value) {
//     alert('Start date cannot be after end date.')
//     return false
//   }
//   return true
// }

// function validateTripDetails() {
//   if (!inputDepartureCity.value) {
//     alert('Departure city is required.')
//     return false
//   }
//   if (!inputDestinationCity.value) {
//     alert('Destination city is required.')
//     return false
//   }
//   if (!inputTransportMode.value) {
//     alert('Transport mode is required.')
//     return false
//   }
//   if (!inputCarpoolers.value) {
//     alert('Number of carpoolers is required.')
//     return false
//   }
//   return true
// }

const onSubmit = async () => {
    alert('yes')
    return;
    const employeeObj = employees.value.find(emp => emp.email === inputEmployeeEmail.value)
    if (!employeeObj) {
      console.error('Employee not found with this email:', inputEmployeeEmail.value)
      return
    }
    const exists = employeeObj && missions.value.some(mission =>
        mission.mission_desc === inputMissionDesc.value &&
        mission.start_date === inputStartDate.value &&
        mission.end_date === inputEndDate.value &&
        mission.employee.employee_id === employeeObj.employee_id
    )
    if (!exists) {
        const payload = {
            mission_desc: inputMissionDesc.value,
            start_date: inputStartDate.value,
            end_date: inputEndDate.value,
            employee: employeeObj,
        }
        try {
            await fetchToken()
            const access = store.state.accessToken
            await services.missions.create(access, payload)
            const response = await services.missions.list(access)
            store.setItem('missions', response.missions)
            console.log('Mission created successfully.')
        } catch (error) {
            console.error('Failed to create mission:', error)
        }
    } else {
        console.log('Mission already exists.')
    }
}

defineExpose({ onSubmit })
</script>

<style scoped>
.body-tab {
  height: 70vh; 
  overflow-y: auto;  
  box-sizing: border-box;
  padding: 1rem;
}
</style>