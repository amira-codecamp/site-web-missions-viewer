
<template>
  <section class="section">
    <div class="container">

      <div class="mb-4">
        <span class="has-text-weight-semibold is-size-6">Carbon Footprint : {{ totalCarbonFootprint }} kg CO2</span>
      </div>

      <!-- <div class="mb-4">
        <Slider
          v-model="yearRange"
          :min="yearRangeMin"
          :max="yearRangeMax"
          :range="true"
          :step="1"
          :marks="true"
          class="w-14rem"
        />
        <span class="has-text-weight-semibold is-size-7">Year Range : {{ yearRange[0] }} - {{ yearRange[1] }}</span>
      </div> -->

      <TripsCharts :totalCarbonFootprint="totalCarbonFootprint" />

      <TripsTable />

    </div>
  </section>
</template>

<script setup>
defineOptions({
  name: 'TripsPage',
})

import { useStore } from '@/store'
import { ref, computed, onMounted, watch } from 'vue'
import TripsCharts from '@/pages/TripsCharts.vue'
import TripsTable from '@/pages/TripsTable.vue'
import Slider from '@vueform/slider';

const store = useStore()
const trips = computed(() => store.state.trips)

const totalCarbonFootprint = computed(() => {
  if (!trips.value.length) return "0.00"
  return trips.value
    .reduce((total, trip) => total + (parseFloat(trip.carbon_footprint) || 0), 0)
    .toFixed(2)
})

// const yearRangeMin = computed(() => {
//   return Math.min(...trips.value.map(t => new Date(t.mission.start_date).getFullYear()))
// })

// const yearRangeMax = computed(() => {
//   return Math.max(...trips.value.map(t => new Date(t.mission.start_date).getFullYear()))
// })

// const yearRange = ref([yearRangeMin.value, yearRangeMax.value])

onMounted(() => {
  document.title = 'Trips | LIPN-carbon'
})
</script>