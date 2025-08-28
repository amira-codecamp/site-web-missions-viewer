<template>
  <form @submit.prevent="submitForm">
    <!-- Login -->
    <div class="field mb-6">
        <label class="label has-text-weight-medium has-text-grey-dark">Login</label>
        <div class="control">
        <input type="text" v-model="form.login" class="input" required />
        </div>
    </div>

    <!-- Is Active -->
    <div class="field mb-6">
        <label class="checkbox has-text-grey-dark">
        <input type="checkbox" v-model="form.is_active" />
        &nbsp;<b>Is Active</b>
        </label>
    </div>

    <!-- Group -->
    <div class="field mb-6">
        <label class="label has-text-weight-medium has-text-grey-dark">Group</label>
        <div class="control">
        <input
            class="input"
            list="groups-list"
            v-model="form.group"
            placeholder="Type group"
            required
        />
        <datalist id="groups-list">
            <option v-for="group in data.groups" :key="group.group_name" :value="group.group_name" />
        </datalist>
        </div>
    </div>

    <!-- Employee -->
    <div class="field mb-6">
        <label class="label has-text-weight-medium has-text-grey-dark">Employee</label>
        <div class="control">
            <input
            class="input"
            list="employees-list"
            v-model="selectedEmployeeName"
            placeholder="Select employee"
            required
            />
            <datalist id="employees-list">
            <option
                v-for="employee in data.employees"
                :key="employee.employee_id"
                :value="employee.first_name + ' ' + employee.last_name + ' - ' + employee.employee_adm_num"
            />
            </datalist>
        </div>
    </div>

    <!-- Buttons -->
    <div class="field is-grouped is-grouped-centered mt-6">
      <div class="control">
        <button class="button is-dark" type="submit">Submit</button>
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


const data = computed(() => getData())

const emit = defineEmits(['submitted', 'cancelled'])

const form = ref({
  login: '',
  is_active: true,
  group: 'STANDARD',
  employee: null,
})

const selectedEmployeeName = ref('')

const submitForm = async () => {
  try {
    const token = await fetchToken();

    const matchedEmployee = data.value.employees.find(emp => {
      const parts = selectedEmployeeName.value.split('-').map(s => s.trim());
      return emp.employee_adm_num === parts[1];
    });

    form.value.employee = matchedEmployee.employee_id

    await services.users.create(token, form.value);

    const response = await services.users.list(token);
    data.value.users = response;

    setTimeout(() => {
      setData(data.value);
      getData()
      alert('User created successfully !')
      emit('submitted');
    }, 100);

  } catch (error) {
    const messages =
      error.response?.data &&
      Object.entries(error.response.data)
        .map(([key, val]) => `${key}: ${val}`)
        .join('\n');
    alert(messages || 'Something went wrong. Please try again.');
  }
};

onMounted(() => {})
</script>