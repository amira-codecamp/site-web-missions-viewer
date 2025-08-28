<template>
  <nav class="navbar mb-5">
    <div class="navbar-start">
      <div class="navbar-item">
        <span class="has-text-weight-semibold is-size-5">Panel</span>
      </div>
    </div>

    <div class="navbar-end">
      <div class="navbar-item">
          <button
            v-if="isAdmin"
            class="button is-info is-small"
            @click="triggerImport"
          >
            <span class="icon is-small"><i class="fas fa-file-csv"></i></span>
            <span>Import</span>
          </button>
          <input
            ref="fileInput"
            type="file"
            accept=".csv"
            style="display: none"
            @change="handleCSVUpload"
          />
      </div>
      <div class="navbar-item">
          <button
            v-if="isAdmin"
            class="button is-dark is-small"
            @click="openEmployeeModal(null, 'add')"
          >
            <span class="icon is-small"><i class="fas fa-plus"></i></span>
            <span>New Employee</span>
          </button>
      </div>
      <div class="navbar-item">
          <button
            v-if="isAdmin"
            class="button is-dark is-small"
            @click="openNewUserModal"
          >
            <span class="icon is-small"><i class="fas fa-plus"></i></span>
            <span>New User</span>
          </button>
      </div>
    </div>
  </nav>

  <div class="flex-content columns is-multiline mb-5">
    <div class="column is-12">
      <div class="card mb-4">
        <div class="card-content is-flex is-flex-direction-column p-5">
          <input
            v-model="searchword"
            class="input is-small mb-5"
            type="text"
            placeholder="Search users..."
          />

          <div class="table-container is-scrollable">
            <table class="table is-fullwidth is-hoverable is-size-7">
              <thead>
                <tr>
                  <th>Login</th>
                  <th>Date Joined</th>
                  <th>Last Login</th>
                  <th>Group</th>
                  <th>Is Active</th>
                  <th>Employee</th>
                  <th colspan="3"></th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td
                    colspan="9"
                    class="has-background-light has-text-weight-bold has-text-dark py-5"
                  >
                    Active Accounts
                  </td>
                </tr>

                <tr
                  v-for="user in filteredActiveUsers"
                  :key="'active-' + user.user_id"
                >
                  <td v-if="editedUserId === user.user_id">
                    <input
                      v-model="editedUserData.login"
                      class="input is-small"
                      type="text"
                      placeholder="Login"
                    />
                  </td>
                  <td v-else>{{ user.login }}</td>

                  <td>{{ user.date_joined }}</td>
                  <td>{{ user.last_login }}</td>

                  <td v-if="editedUserId === user.user_id">
                    <input
                      class="input is-small"
                      list="group-options"
                      v-model="editedUserData.group"
                      placeholder="Select Group"
                    />
                    <datalist id="group-options">
                      <option
                        v-for="group in data.groups"
                        :key="group.group_name"
                        :value="group.group_name"
                      />
                    </datalist>
                  </td>
                  <td v-else>{{ user.group }}</td>

                  <td v-if="editedUserId === user.user_id">
                    <input
                      type="checkbox"
                      v-model="editedUserData.is_active"
                    />
                  </td>
                  <td v-else><span>{{ user.is_active ? 'x' : '' }}</span></td>

                  <td v-if="editedUserId === user.user_id">
                    <input
                      class="input is-small"
                      list="employee-options"
                      v-model="editedUserData.employee"
                      placeholder="Select Employee"
                    />
                    <datalist id="employee-options">
                      <option
                        v-for="emp in data.employees"
                        :key="emp.employee_id"
                        :value="`${emp.first_name} ${emp.last_name} - ${emp.employee_adm_num}`"
                      >
                      </option>
                    </datalist>
                  </td>
                  <td v-else>
                    <span>{{ user.employee.first_name }} {{ user.employee.last_name }} - {{ user.employee.employee_adm_num }}</span>
                    <button
                      v-if="isAdmin"
                      class="button is-info is-light is-small ml-2"
                      @click="openEmployeeModal(user.employee, 'edit')"
                      title="Edit Employee"
                      style="font-weight: bold; padding: 0 6px;"
                    >
                      <span class="icon is-small">
                        <i class="fas fa-user-edit"></i>
                      </span>
                    </button>
                  </td>

                  <td
                    colspan="2"
                    v-if="editedUserId === user.user_id"
                    class="is-flex is-align-items-center"
                  >
                    <button
                      class="button is-secondary is-light is-small"
                      @click="saveLocalChanges"
                      title="Submit"
                      style="font-weight: bold; padding: 0 6px;"
                    >
                      <span class="icon is-small"><i class="fas fa-check"></i></span>
                    </button>
                    <button
                      class="button is-secondary is-light is-small mr-2"
                      @click="cancelEdit"
                      title="Cancel"
                      style="font-weight: bold; padding: 0 6px;"
                    >
                      <span class="icon is-small"><i class="fas fa-times"></i></span>
                    </button>
                  </td>

                  <td v-else>
                    <button
                      v-if="isAdmin && editedUserId !== user.user_id"
                      class="button is-link is-light is-small"
                      @click="editUser(user)"
                      title="Edit"
                      style="font-weight: bold; padding: 0 6px;"
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
                      title="Delete"
                      style="font-weight: bold; padding: 0 6px;"
                    >
                      <span class="icon is-small">
                        <i class="fas fa-times"></i>
                      </span>
                    </button>
                  </td>
                </tr>

                <tr>
                  <td
                    colspan="9"
                    class="py-5 has-background-light has-text-weight-bold has-text-dark"
                  >
                    Inactive Accounts
                  </td>
                </tr>

                <tr
                  v-for="user in filteredInactiveUsers"
                  :key="'inactive-' + user.user_id"
                >
                  <td v-if="editedUserId === user.user_id">
                    <input
                      v-model="editedUserData.login"
                      class="input is-small"
                      type="text"
                      placeholder="Login"
                    />
                  </td>
                  <td v-else>{{ user.login }}</td>

                  <td>{{ user.date_joined }}</td>
                  <td>{{ user.last_login }}</td>

                  <td v-if="editedUserId === user.user_id">
                    <div class="select is-small is-fullwidth">
                      <select v-model="editedUserData.group">
                        <option disabled value="">Select Group</option>
                        <option
                          v-for="group in data.groups"
                          :key="group.group_name"
                          :value="group.group_name"
                        >
                          {{ group.group_name }}
                        </option>
                      </select>
                    </div>
                  </td>
                  <td v-else>{{ user.group }}</td>

                  <td v-if="editedUserId === user.user_id">
                    <input
                      type="checkbox"
                      v-model="editedUserData.is_active"
                    />
                  </td>
                  <td v-else><span>{{ user.is_active ? 'x' : '' }}</span></td>

                  <td v-if="editedUserId === user.user_id">
                    <input
                      class="input is-small"
                      list="employee-options"
                      v-model="editedUserData.employee"
                      placeholder="Select Employee"
                    />
                    <datalist id="employee-options">
                      <option
                        v-for="emp in data.employees"
                        :key="emp.employee_id"
                        :value="`${emp.first_name} ${emp.last_name} - ${emp.employee_adm_num}`"
                      >
                      </option>
                    </datalist>
                  </td>
                  <td v-else>
                    <span>{{ user.employee.first_name }} {{ user.employee.last_name }} - {{ user.employee.employee_adm_num }}</span>
                    <button
                      v-if="isAdmin"
                      class="button is-info is-light is-small ml-2"
                      @click="openEmployeeModal(user.employee, 'edit')"
                      title="Edit Employee"
                      style="font-weight: bold; padding: 0 6px;"
                    >
                      <span class="icon is-small">
                        <i class="fas fa-user-edit"></i>
                      </span>
                    </button>
                  </td>

                  <td
                    colspan="2"
                    v-if="editedUserId === user.user_id"
                    class="is-flex is-align-items-center"
                  >
                    <button
                      class="button is-secondary is-light is-small"
                      @click="saveLocalChanges"
                      title="Submit"
                      style="font-weight: bold; padding: 0 6px;"
                    >
                      <span class="icon is-small"><i class="fas fa-check"></i></span>
                    </button>
                    <button
                      class="button is-secondary is-light is-small mr-2"
                      @click="cancelEdit"
                      title="Cancel"
                      style="font-weight: bold; padding: 0 6px;"
                    >
                      <span class="icon is-small"><i class="fas fa-times"></i></span>
                    </button>
                  </td>

                  <td v-else>
                    <button
                      v-if="isAdmin && editedUserId !== user.user_id"
                      class="button is-link is-light is-small"
                      @click="editUser(user)"
                      title="Edit"
                      style="font-weight: bold; padding: 0 6px;"
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
                      title="Delete"
                      style="font-weight: bold; padding: 0 6px;"
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
      </div>
    </div>
  </div>

  <div class="modal" :class="{ 'is-active': isEmployeeModalActive }">
    <div class="modal-background" @click="closeEmployeeModal"></div>
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">{{ selectedOperation === 'edit' ? 'Edit Employee' : 'New Employee' }}</p>
        <button class="delete" aria-label="close" @click="closeEmployeeModal"></button>
      </header>
      <section class="modal-card-body">
        <EmployeeForm
          v-if="selectedOperation"
          :employee="selectedEmployee"
          :operation="selectedOperation"
          @updated="handleEmployeeUpdated"
          @cancelled="closeEmployeeModal"
        />
      </section>
    </div>
  </div>

  <div class="modal" :class="{ 'is-active': isUserModalActive }">
    <div class="modal-background" @click="closeNewUserModal"></div>
    <div class="modal-card">
      <header class="modal-card-head">
        <p class="modal-card-title">Create New User</p>
        <button class="delete" aria-label="close" @click="closeNewUserModal"></button>
      </header>
      <section class="modal-card-body">
        <UserForm
          @submitted="handleNewUserSubmit"
          @cancelled="closeNewUserModal"
        />
      </section>
    </div>
  </div>

</template>

<script setup>
import { ref, computed } from "vue";
import services from "@/composables/services";
import { fetchToken, getData, getPermission, setData } from "@/composables/session";
import EmployeeForm from "@/components/EmployeeForm.vue";
import UserForm from "@/components/UserForm.vue";
import Papa from 'papaparse';

const { isAdmin } = getPermission();
const data = computed(() => getData());

const searchword = ref("");
const editedUserId = ref(null);
const editedUserData = ref({});

const isEmployeeModalActive = ref(false);
const selectedEmployee = ref(null);
const selectedOperation = ref(null);

function openEmployeeModal(employee, operation) {
  selectedEmployee.value = employee ? { ...employee } : null;
  selectedOperation.value = operation
  isEmployeeModalActive.value = true;
}

function closeEmployeeModal() {
  isEmployeeModalActive.value = false;
  selectedEmployee.value = null;
  selectedOperation.value = '';
}

function handleEmployeeUpdated(updatedEmployee) {
  const index = data.value.employees.findIndex(
    (e) => e.employee_id === updatedEmployee.employee_id
  );
  if (index !== -1) {
    data.value.employees[index] = { ...updatedEmployee };
    setData(data.value);
  }
  closeEmployeeModal();
}

const usersWithEmployees = computed(() => {
  if (!data.value.users || !data.value.employees) return [];
  return data.value.users.map(user => {
    const employeeObj = data.value.employees.find(emp => emp.employee_id === user.employee) || {};
    return {
      ...user,
      employee: employeeObj,
    };
  });
});

const filteredActiveUsers = computed(() => {
  const sw = searchword.value.toLowerCase();
  return usersWithEmployees.value
    .filter(user => user.is_active)
    .filter(user =>
      !sw ||
      user.login.toLowerCase().includes(sw) ||
      user.employee.first_name?.toLowerCase().includes(sw) ||
      user.employee.last_name?.toLowerCase().includes(sw)
    );
});

const filteredInactiveUsers = computed(() => {
  const sw = searchword.value.toLowerCase();
  return usersWithEmployees.value
    .filter(user => !user.is_active)
    .filter(user =>
      !sw ||
      user.login.toLowerCase().includes(sw) ||
      user.employee.first_name?.toLowerCase().includes(sw) ||
      user.employee.last_name?.toLowerCase().includes(sw)
    );
});

function editUser(user) {
  editedUserId.value = user.user_id;
  editedUserData.value = {
    ...user,
    employee: `${user.employee.first_name} ${user.employee.last_name} - ${user.employee.employee_adm_num}`,
  };
}

function cancelEdit() {
  editedUserId.value = null;
  editedUserData.value = {};
}

async function saveLocalChanges() {
  if (!editedUserId.value) return;
  const idx = data.value.users.findIndex(u => u.user_id === editedUserId.value);
  if (idx === -1) return;

  const clone = { ...editedUserData.value };
  const employee_adm_num = clone.employee.split('-')[1].trim();
  const match = data.value.employees.find(
    emp => `${emp.employee_adm_num}` === employee_adm_num
  );
  data.value.users[idx] = {
    ...clone,
    employee: match.employee_id,
  };

  try {
    const token = await fetchToken();
    await services.users.partialUpdate(token, editedUserId.value, {
      ...clone,
      employee: match.employee_id,
    });
  } catch (error) {
    console.error("Failed to sync user update:", error);
  }

  editedUserId.value = null;
  editedUserData.value = {};

  setTimeout(() => {
    setData(data.value);
    getData()
    alert('User updated successfully.');
  }, 100);
}

async function deleteUser(userId) {
  if (!confirm("Are you sure you want to delete this user?")) return;

  try {
    const token = await fetchToken();
    await services.users.destroy(token, userId);

    const resp = await services.users.list(token);
    data.value.users = resp;

    setTimeout(() => {
      setData(data.value);
      getData()
      alert("User deleted successfully!");
    }, 100);
  } catch (error) {
    console.error(error);
  }
}

const isUserModalActive = ref(false);

function openNewUserModal() {
  isUserModalActive.value = true;
}

function closeNewUserModal() {
  isUserModalActive.value = false;
}

async function handleNewUserSubmit() {
  const refreshedData = getData()
  data.value = refreshedData
  closeNewUserModal()
}

const fileInput = ref(null)

const triggerImport = () => {
  fileInput.value.click()
}

const handleCSVUpload = (event) => {
  const file = event.target.files[0]
  if (!file) return
  Papa.parse(file, {
    header: true,
    skipEmptyLines: true,
    complete: (results) => {
      console.log('CSV data :', results.data)
      processImportedEmployees(results.data)
    },
    error: (error) => {
      console.error('Error while parsing CSV :', error.message)
    }
  })
}

// Sanitize fields from injections
function escapeCSVField(value) {
  if (typeof value === 'string' && /^[=+\-@]/.test(value)) {
    return `'${value}'`
  }
  return value
}

function escapeCSVLine(line) {
  const escapedLine = {}
  for (const key in line) {
    escapedLine[key] = escapeCSVField(line[key])
  }
  return escapedLine
}

// HTML-safe string sanitizer
function sanitizeString(str) {
  return String(str).replace(/[<>]/g, '').trim()
}

async function createEmployee(line, token) {
  if (!line.last_name || !line.first_name || !line.email || !line.status || !line.group) {
    throw new Error("Missing required fields")
  }
  const employee = {
    employee_adm_num: sanitizeString(line.employee_adm_num.trim()),
    last_name: sanitizeString(line.last_name).toUpperCase(),
    first_name: sanitizeString(line.first_name).toLowerCase(),
    email: sanitizeString(line.email.trim()),
    research_team: sanitizeString(line.research_team.trim()),
    status: sanitizeString(line.status).toUpperCase()
  }
  await services.employees.create(token, employee)
  return { originalLine: line, employee }
}

async function createUser(created, token) {
  const emp = created.employee
  const employeeObj = data.value.employees.find(e =>
    e.employee_adm_num === emp.employee_adm_num
  )
  if (!employeeObj || !employeeObj.employee_id) {
    throw new Error(`Employee not found after creation: ${emp.email}`)
  }
  const user = {
    login: employeeObj.last_name.toLowerCase(),
    is_active: true,
    group: sanitizeString(created.originalLine.group).toUpperCase(),
    employee: employeeObj.employee_id
  }
  await services.users.create(token, user)
}

async function processImportedEmployees(fileData) {
  const token = await fetchToken()
  const failedLines = []
  const createdEmployees = []
  for (const line of fileData) {
    try {
      const created = await createEmployee(line, token)
      createdEmployees.push(created)
    } catch (error) {
      failedLines.push(escapeCSVLine({ ...line, error: error.message }))
      console.error(`❌ Error creating employee on row: ${JSON.stringify(line)}\n`, error)
    }
  }
  const employeesList = await services.employees.list(token)
  data.value.employees = employeesList
  await new Promise(resolve => setTimeout(resolve, 1000));
  for (const created of createdEmployees) {
    try {
      await createUser(created, token)
    } catch (error) {
      failedLines.push(escapeCSVLine({ ...created.originalLine, error: error.message }))
      console.error(`❌ Error creating user for row: ${JSON.stringify(created.originalLine)}\n`, error)
    }
  }
  const usersList = await services.users.list(token)
  data.value.users = usersList
  await new Promise(resolve => setTimeout(resolve, 1000));

  setData(data.value)

  if (failedLines.length > 0) {
    const csv = Papa.unparse(failedLines)
    const blob = new Blob([csv], { type: 'text/csv;charset=utf-8;' })
    const url = URL.createObjectURL(blob)
    const link = document.createElement("a")
    link.href = url
    link.setAttribute("download", "import_errors.csv")
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  } else {
    alert('Data Imported successfully !')
  }
}
</script>

<style scoped>
.card {
  border-radius: 8px;
  background-color: #f9fafb;
}
.table-container {
  overflow-y: scroll;
  height: 1100px !important;
}
.modal-card {
  width: 80%;
  height: 800px;
}
</style>