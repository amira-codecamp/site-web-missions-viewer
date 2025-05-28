
<template>
  <component 
    :is="chartComponent" 
    :data="chartData" 
    :options="chartOptions" 
  />
</template>

<script setup>
defineOptions({
  name: 'Chart',
})

import { computed } from 'vue'
import { Bar, Pie } from 'vue-chartjs'
import annotationPlugin from 'chartjs-plugin-annotation'

import {
  Chart as ChartJS,
  Title,
  Tooltip,
  Legend,
  ArcElement,
  CategoryScale,
  LinearScale,
  BarElement,
  BarController,
} from 'chart.js'

ChartJS.register(Title, Tooltip, Legend, ArcElement, CategoryScale, LinearScale, BarElement, BarController, annotationPlugin)

const props = defineProps({
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
    default: ''
  },
  chartType: {
    type: String,
    required: true
  },
})

const FIXED_MAX_VALUE = 1000 // 1-tonne CO2 per person

const getColorFromValue = (value, maxValue) => {
  const grayIntensity = Math.floor((value / maxValue) * 85);
  return `rgba(181, 181, 181, ${(grayIntensity / 85) + 0.2})`;
}

const chartData = computed(() => {
  return {
    labels: props.labels,
    datasets: [
      {
        label: '',
        data: props.values,
        borderColor: 'rgba(181, 181, 181, 1)',
        backgroundColor: props.values.map(value => getColorFromValue(value, FIXED_MAX_VALUE)),
        borderWidth: 1,
        barThickness: 150
      }
    ]
  };
});

const chartOptions = computed(() => {
  const baseOptions = {
    responsive: true,
    plugins: {
      legend: {
        position: 'bottom'
      },
      title: {
        display: true,
        text: props.title
      },
      annotation: {}
    },
    events: []
  }

  if (props.chartType === 'bar') {
    baseOptions.plugins.annotation = {
      drawTime: 'afterDatasetsDraw',
      annotations: {
        line1: {
          type: 'line',
          yMin: 1000,
          yMax: 1000,
          borderColor: 'rgba(54, 69, 79, 1)',
          borderWidth: 2,
          borderDash: [6, 6],
          label: {
            display: true,
            content: 'Baseline 1000',
            position: 'end',
            backgroundColor: 'white',
            color: 'rgba(54, 69, 79, 1)',
            font: {
              weight: 'bold'
            }
          },
        }
      }
    }
  }
  
  return baseOptions
});

const chartComponent = computed(() => {
  return props.chartType === 'pie' ? Pie : Bar;
});
</script>