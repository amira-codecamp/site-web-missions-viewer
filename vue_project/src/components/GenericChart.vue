
<template>
  <component
    :is="chartComponent"
    :data="computedChartData"
    :options="chartOptions"
  />
</template>

<script setup>
import { computed } from 'vue'
import { Bar, Pie } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement,
  BarController
} from 'chart.js'
import annotationPlugin from 'chartjs-plugin-annotation'

ChartJS.register(
  Title,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement,
  BarController,
  annotationPlugin
)

defineOptions({
  name: 'GenericChart',
})

const props = defineProps({
  chartType: {
    type: String,
    required: true,
  },
  labels: {
    type: Array,
    required: true,
  },
  datasets: {
    type: Array,
    required: true,
  },
  options: {
    type: Object,
    default: () => ({}),
  },
})

const chartComponent = computed(() => {
  switch (props.chartType) {
    case 'pie':
      return Pie
    case 'bar':
    default:
      return Bar
  }
})

const computedChartData = computed(() => ({
  labels: props.labels,
  datasets: props.datasets,
}))

const chartOptions = computed(() => props.options)
</script>