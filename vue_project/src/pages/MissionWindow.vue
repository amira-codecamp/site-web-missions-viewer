<template>
  <section class="section" style="padding-top: 0.5rem;">
    <div class="container" v-if="missions.length!=0">
      <div class="table-wrapper">

        <div class="mb-4">
          <input
              v-model="searchword3"
              class="input is-small is-fullwidth"
              type="text"
              placeholder="Search missions..."
          />
        </div>

        <div class="table-content is-scrollable">
          <table class="table is-fullwidth is-hoverable is-bordered is-size-7">
          <thead>
              <tr>
              <th>Dates</th>
              <th>Description</th>
              <th>Employee</th>
              <th colspan="2">
                <button 
                class="button is-dark is-small is-light is-fullwidth" 
                v-if="isManager" 
                @click="showMissionForm(null, 'add')"
                style="font-weight: bold;"
                title="Add mission"
                >
                  Add Mission
                </button>
              </th>
              </tr>
          </thead>
          <tbody>
              <tr v-for="mission in filteredMissions" :key="mission.mission_id">
              <td>{{ mission.start_date }} -> {{ mission.end_date }} </td>
              <td>{{ mission.mission_desc }}</td>
              <td>{{ mission.employee?.first_name }} {{ mission.employee?.last_name }}</td>
              <td>
                  <button 
                  class="button is-link is-light is-small" 
                  v-if="isManager" 
                  @click="showMissionForm(mission, 'modify')"
                  style="font-weight: bold; padding: 0 6px;"
                  title="Modify mission"
                  >
                  <span class="icon is-small">
                      <i class="fas fa-pencil-alt"></i>
                  </span>
                  </button>
              </td>
              <td>
                  <button 
                      v-if="isManager"
                      class="button is-small is-danger is-light" 
                      @click="deleteMission(mission.mission_id)" 
                      title="Delete mission"
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

        <div class="modal" :class="{ 'is-active': MissionFormActive }">
          <div class="modal-background" @click="hideMissionForm"></div>
          <div class="modal-card" style="width: 30%;">
            <header class="modal-card-head has-background-white">
              <p class="modal-card-title has-text-grey-dark">Add a New Mission</p>
              <button class="delete" aria-label="close" @click="hideMissionForm"></button>
            </header>
            <section class="modal-card-body has-background-light">
              <MissionForm 
              :missionObj="selectedMission"
              :task="inputTask"
              :key="missionFormKey"
              @close="hideMissionForm" 
              />
            </section>
          </div>
        </div>
      </div>
    </div>
    <div class="mb-4" v-else>
        <span>No missions available.</span>
    </div>
  </section>
</template>

<script setup>
import { ref, computed, watch } from 'vue'

import { useStore } from '@/store'

import services from '@/services'

import { fetchToken } from '@/session'

import MissionForm from '@/pages/MissionForm.vue'

defineOptions({
  name: 'MissionWindow',
})

const store = useStore()

const searchword3 = ref('')
const selectedMission = ref(null)
const inputTask = ref('')
const missionFormKey = ref(0);

const isManager = computed(() => store.state.isManager)
const missions = computed(() => store.state.missions)

function normalizeString(str) {
  if (!str) return ''
  return str.normalize('NFD').replace(/[\u0300-\u036f]/g, '').toLowerCase()
}

const filteredMissions = computed(() => {
  if (!searchword3.value) return missions.value
  const term = normalizeString(searchword3.value)
  return missions.value.filter(mission => {
    const fields = [
      mission.start_date,
      mission.end_date,
      mission.mission_desc,
      `${mission.employee?.first_name || ''} ${mission.employee?.last_name || ''}`,
    ]
    return fields.some(field => normalizeString(field).includes(term))
  })
})

const deleteMission = async (mission_id) => {
  try {

    await fetchToken();

    const access = store.state.accessToken;

    await services.missions.destroy(access, mission_id);

    const response = await services.missions.list(access);
    store.setItem('missions', response.missions);

    alert(`Mission deleted successfully!`)
  
  } catch (error) {
    if (error.response?.data) {
      const messages = Object.entries(error.response.data).map(([key, val]) => `${key}: ${val}`)
      alert(messages.join('\n'))
    } else {
      alert('Something went wrong. Please try again.')
    }
  }
}

const MissionFormActive = ref(false)

function showMissionForm(mission, task) {
  selectedMission.value = mission
  inputTask.value = task
  MissionFormActive.value = true
}

function hideMissionForm() {
  selectedMission.value = null
  inputTask.value = ''
  MissionFormActive.value = false
}

watch(selectedMission, () => {
  missionFormKey.value++;
})
</script>

<style scoped>
.table-content {
  overflow-y: scroll;
  height: 25rem !important;
}

.table-wrapper, .table-wrapper canvas {
  width: 100% !important;
  min-height: unset;
}
</style>
