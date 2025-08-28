<template>
  <form @submit.prevent="submitForm">

    <!-- Employee Adm Num -->
    <div class="field mb-5">
      <label class="label has-text-weight-medium has-text-grey-dark">Employee Adm Num</label>
      <div class="control">
        <input
          type="text"
          v-model="form.employee_adm_num"
          class="input"
          required
        />
      </div>
    </div>

    <div class="columns is-mobile">
      <!-- First Name -->
      <div class="field mb-5 column is-half">
        <label class="label has-text-weight-medium has-text-grey-dark">First Name</label>
        <div class="control">
          <input
            type="text"
            v-model="form.first_name"
            class="input"
            required
          />
        </div>
      </div>

      <!-- Last Name -->
      <div class="field mb-5 column is-half">
        <label class="label has-text-weight-medium has-text-grey-dark">Last Name</label>
        <div class="control">
          <input
            type="text"
            v-model="form.last_name"
            class="input"
            required
          />
        </div>
      </div>
    </div>

    <!-- Email -->
    <div class="field mb-5">
      <label class="label has-text-weight-medium has-text-grey-dark">Email</label>
      <div class="control">
        <input
          type="email"
          v-model="form.email"
          class="input"
          required
        />
      </div>
    </div>

    <!-- Research Team -->
    <div class="field mb-5">
      <label class="label has-text-weight-medium has-text-grey-dark">Research Team</label>
      <div class="control">
        <input
          type="text"
          v-model="form.research_team"
          class="input"
          required
        />
      </div>
    </div>

    <!-- Status -->
    <div class="field mb-5">
      <label class="label has-text-weight-medium has-text-grey-dark">Status</label>
      <div class="control">
        <input
          class="input"
          list="status-list"
          v-model="form.status"
          placeholder="Type status"
          required
        />
        <datalist id="status-list">
          <option
            v-for="s in data.status"
            :key="s.status_name"
            :value="s.status_name"
          />
        </datalist>
      </div>
    </div>

    <!-- Submit -->
    <div class="field is-grouped is-grouped-centered mt-5">
      <div class="control">
        <button class="button is-dark is-fullwidth">
          <span>Submit</span>
        </button>
      </div>
      <div class="control">
        <button class="button is-light" type="button" @click="$emit('cancelled')">Cancel</button>
      </div>
    </div>
  </form>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import services from '@/composables/services'
import { fetchToken, getData, setData } from '@/composables/session'

const props = defineProps({
  employee: {
    type: Object,
    required: true
  },
  operation: {
    type: String,
    required: true
  }
})

const data = computed(() => getData())

const form = ref({
  employee_id: null,
  employee_adm_num: '',
  first_name: '',
  last_name: '',
  email: '',
  research_team: '',
  status: ''
})

const emit = defineEmits(['updated', 'cancelled'])

const submitForm = async () => {

  try {
    const token = await fetchToken()

    let message = ''

    if (props.operation === 'add') {
      await services.employees.create(token, {
        ...form.value
      })
      message = 'Employee added successfully!'
    } else if (props.operation === 'edit') {
      await services.employees.partialUpdate(token, form.value.employee_id, {
        ...form.value
      })
      message = 'Employee edited successfully!'
    }

    data.value.employees = await services.employees.list(token)
    
    setTimeout(() => {
      setData(data.value);
      getData()
      alert(message)
      emit('updated', form.value)
    }, 100);

  } catch (error) {
    if (error.response?.data) {
      const messages = Object.entries(error.response.data).map(
        ([key, val]) => `${key}: ${val}`
      )
      alert(messages.join('\n'))
    } else {
      alert('Something went wrong. Please try again.')
    }
  }
}

onMounted(() => {
  if (props.operation === 'edit') {
    form.value = {
      employee_id: props.employee.employee_id,
      employee_adm_num: props.employee.employee_adm_num,
      first_name: props.employee.first_name,
      last_name: props.employee.last_name,
      email: props.employee.email,
      status: props.employee.status,
      research_team: props.employee.research_team
    }
  } else if (props.operation === 'add') {
    form.value = {
      employee_adm_num: '',
      first_name: '',
      last_name: '',
      email: '',
      status: '',
      research_team: ''
    }
  }
})
</script>