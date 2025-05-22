
<template>
  <Bar :data="chartData" :options="chartOptions" />
</template>

<script>
import { Bar } from 'vue-chartjs'
import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  BarElement,
  CategoryScale,
  LinearScale
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, BarElement, CategoryScale, LinearScale)

export default {
  name: 'HistogramChart',
  components: { Bar },
  props: {
    labels: {
      type: Array,
      required: true
    },
    values: {
      type: Array,
      required: true
    },
    title: {
      type: String,
      default: 'Histogram'
    }
  },
  computed: {
    chartData() {
      const maxItems = 5
      return {
        labels: this.labels.slice(0, maxItems),
        datasets: [
          {
            data: this.values.slice(0, maxItems)
          }
        ]
      }
    },
    chartOptions() {
      return {
        responsive: true,
        plugins: {
          legend: {
            display: false
          },
          title: {
            display: true,
            text: this.title
          }
        }
      }
    }
  }
}
</script>