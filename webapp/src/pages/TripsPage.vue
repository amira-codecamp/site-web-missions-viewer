
<template>
  <section class="section">
    <div class="container">

      <div class="mb-4">
        <span class="has-text-weight-semibold is-size-6">Carbon Footprint : {{ totalCarbonFootprint }} kg CO2</span>
      </div>

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

const store = useStore()
const trips = computed(() => store.state.trips)

const totalCarbonFootprint = computed(() => {
  if (!trips.value.length) return "0.00"
  return trips.value
    .reduce((total, trip) => total + (parseFloat(trip.carbon_footprint) || 0), 0)
    .toFixed(2)
})

onMounted(() => {
  document.title = 'Trips | LIPN-carbon'
})
</script>