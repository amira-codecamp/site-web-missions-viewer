<template>
    <Pie :data="chartData" :options="chartOptions" />
</template>
  
<script>
  import { Pie } from 'vue-chartjs'
  import {
    Chart as ChartJS,
    Title,
    Tooltip,
    Legend,
    ArcElement
  } from 'chart.js'
  
  ChartJS.register(Title, Tooltip, Legend, ArcElement)
  
  export default {
    name: 'PieChart',
    components: { Pie },
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
        default: 'Pie Chart'
      }
    },
    computed: {
      chartData() {
        const maxItems = 5;
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
              position: 'bottom'
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