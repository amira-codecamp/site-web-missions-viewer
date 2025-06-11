
<template>
  <div class="columns is-multiline is-gapless">

    <div class="column is-5">
      <div class="chart-wrapper bar-wrapper">
        <GenericChart
          :chartType="'bar'"
          :labels="TripBarChart.labels"
          :datasets="TripBarChart.datasets"
          :options="TripBarChart.options"
        />
      </div>
    </div>

    <div class="column is-1"></div>

    <div class="column is-5">
      <div class="chart-wrapper bar-wrapper">
        <GenericChart
          :chartType="'bar'"
          :labels="yearBarChart.labels"
          :datasets="yearBarChart.datasets"
          :options="yearBarChart.options"
        />
      </div>
    </div>

    <div class="column is-1"></div>

    <div class="column is-2">
      <div class="chart-wrapper pie-wrapper">
        <GenericChart
          :labels="tripPieChart.labels"
          :datasets="tripPieChart.datasets"
          :options="tripPieChart.options"
          :chartType="'pie'"
        />
      </div>
    </div>

    <div class="column is-2">
      <div class="chart-wrapper pie-wrapper">
        <GenericChart
          :labels="transportPieChart.labels"
          :datasets="transportPieChart.datasets"
          :options="transportPieChart.options"
          :chartType="'pie'"
        />
      </div>
    </div>

    <div class="column is-2">
      <div class="chart-wrapper pie-wrapper">
        <GenericChart
          :labels="yearPieChart.labels"
          :datasets="yearPieChart.datasets"
          :options="yearPieChart.options"
          :chartType="'pie'"
        />
      </div>
    </div>

    <div class="column is-2">
      <div class="chart-wrapper pie-wrapper">
        <GenericChart
          :labels="missionPieChart.labels"
          :datasets="missionPieChart.datasets"
          :options="missionPieChart.options"
          :chartType="'pie'"
        />
      </div>
    </div>

    <div class="column is-2" v-if="isManager">
      <div class="chart-wrapper pie-wrapper">
        <GenericChart
          :labels="employeePieChart.labels"
          :datasets="employeePieChart.datasets"
          :options="employeePieChart.options"
          :chartType="'pie'"
        />
      </div>
    </div>

     <div class="column is-2">
      <div class="chart-wrapper pie-wrapper">
        <GenericChart
          :labels="statusPieChart.labels"
          :datasets="statusPieChart.datasets"
          :options="statusPieChart.options"
          :chartType="'pie'"
        />
      </div>
    </div>

    <!-- <div class="mb-4 column is-full">
      <span class="has-text-weight-semibold is-size-7">Trips Footprint</span>
    </div> -->

    <!-- <div class="column is-1"></div> -->

  </div>
</template>

<script setup>
defineOptions({
  name: 'TripsCharts',
})

import { ref, computed, onMounted, watch } from 'vue'
import { useStore } from '@/store'
import GenericChart from '@/components/GenericChart.vue'

const store = useStore()

const isManager = computed(() => store.state.isManager)

const props = defineProps({
  totalCarbonFootprint: {
    type: Number,
    required: true,
  },
  trips: {
    type: Object,
    required: true,
  },
})

const trips = ref(props.trips)

const baseline = ref(0)

// Charts
const BORDER_COLOR = 'rgba(54, 54, 54, 0.8)';
const BORDER_WIDTH = 1;
const BAR_TICKNESS = 25;

const COLORS = [
  'rgba(160, 122, 176',
  'rgba(140, 160, 150',
  'rgba(141, 169, 196',
  'rgba(210, 180, 120',
  'rgba(1, 120, 176',
  'rgba(1, 120, 176',
  'rgba(141, 169, 196',
  'rgba(125, 140, 180',
];

const getValueColor = (rgbStr, value, maxValue) => {
  const intensity = Math.min(1, value / maxValue);
  return `${rgbStr}, ${intensity})`;
};

const createBaselineAnnotation = (baseline, annotType, annotLabel, borderColor, xValue = null) => ({
  drawTime: 'afterDatasetsDraw',
  annotations: {
    baselineAnnotation: annotType === 'label'
      ? {
        type: annotType,
        xValue: xValue ?? 0,
        yValue: baseline + 200,
        backgroundColor: 'white',
        borderColor: borderColor,
        borderWidth: 0,
        content: `${annotLabel} ${baseline}`,
        font: { weight: 'bold', size: 12 },
        color: borderColor,
        position: 'start',
        padding: 4,
        cornerRadius: 4,
      }
      : {
          type: annotType,
          yMin: baseline,
          yMax: baseline,
          borderColor,
          borderWidth: 2,
          borderDash: [6, 6],
          label: {
            display: true,
            content: `${annotLabel} ${baseline}`,
            position: 'start',
            backgroundColor: 'white',
            color: borderColor,
            font: { weight: 'bold' },
          },
        },
  },
});

const createDatasetItem = ({ rgbStr, label, values }) => ({
  label,
  data: values,
  borderColor: BORDER_COLOR,
  backgroundColor: values.map(v => getValueColor(rgbStr, v, Math.max(...values))),
  borderWidth: BORDER_WIDTH,
  barThickness: BAR_TICKNESS
});

const createBarOptions = (title, baselineValue, annotType, stacked = false, xticks = [], annotLabel) => ({
  responsive: true,
  plugins: {
    legend: { display: false },
    title: { display: true, text: title, color: '#363636' },
    annotation: baselineValue !== null
      ? createBaselineAnnotation(baselineValue, annotType, annotLabel, BORDER_COLOR)
      : undefined,
  },
  scales: {
    x: { 
      ticks: { display: xticks.length === 0 ? false : true, },
      stacked: stacked,
    },
    y: { 
      ticks: { beginAtZero: true },
      stacked: stacked,
    },
  },
});

const createPieOptions = (title) => ({
  responsive: true,
  plugins: {
    legend: { display: false },
    title: { display: true, text: title, color: '#363636' },
  },
});

const buildBarChartConfig = ({ labels, datasets, title, baselineValue = null, annotType = 'line', stacked = false, xticks = [], annotLabel = '' }) => ({
  labels,
  datasets: datasets,
  options: createBarOptions(title, baselineValue, annotType, stacked, xticks, annotLabel),
});

const buildPieChartConfig = ({ labels, datasets, title }) => ({
  labels,
  datasets: datasets,
  options: createPieOptions(title),
});

const computeBaseline = (tripsData) => {
  // baseline: 1-tonne CO2 per person per year
  const dates = tripsData
    .map(trip => trip.mission?.start_date)
    .filter(dateStr => !!dateStr)
    .map(dateStr => new Date(dateStr));

  const minDate = new Date(Math.min(...dates.map(d => d.getTime())));
  const maxDate = new Date(Math.max(...dates.map(d => d.getTime())));

  const yearsDiff = maxDate.getFullYear() - minDate.getFullYear();
  const monthsDiff = maxDate.getMonth() - minDate.getMonth();

  const totalMonths = yearsDiff * 12 + monthsDiff + 1;
  const baselinePerMonth = 1000 / 12;

  return Math.round(totalMonths * baselinePerMonth);
};

function aggregateByKey(trips, keyFn) {
  const carbonByKey = {};

  trips.value.forEach(trip => {
    const key = keyFn(trip) || '';
    const carbon = Number(trip.carbon_footprint) || 0;
    carbonByKey[key] = (carbonByKey[key] || 0) + carbon;
  });

  return {
    labels: Object.keys(carbonByKey),
    values: Object.values(carbonByKey),
  };
}

function tripChartData(trips) {
  return aggregateByKey(trips, trip => {
    const source = `${trip.departure_city || ''}, ${trip.departure_country || ''}`;
    const destination = `${trip.destination_city || ''}, ${trip.destination_country || ''}`;
    return `${source} -> ${destination}`;
  });
}

function yearChartData(trips) {
  return aggregateByKey(trips, trip => {
    const startDate = trip.mission?.start_date;
    return startDate ? new Date(startDate).getFullYear().toString() : '';
  });
}

function transportChartData(trips) {
  return aggregateByKey(trips, trip => trip.transport?.transport_name || '');
}

function missionChartData(trips) {
  return aggregateByKey(trips, trip => trip.mission?.mission_desc || '');
}

function employeeChartData(trips) {
  return aggregateByKey(trips, trip => {
    const firstname = `${trip.employee.first_name || ''}`;
    const lastname = `${trip.employee.last_name || ''}`;
    return `${firstname} ${lastname}`;
  });
}

function statusChartData(trips) {
  return aggregateByKey(trips, trip => trip.employee?.status?.status_name || '');
}

const statusPieChart = computed(() => {
  const { labels, values } = statusChartData(trips);
  const datasets = [
    createDatasetItem({ rgbStr: COLORS[6], label: '', values })
  ];
  return buildPieChartConfig({ labels, datasets, title: 'Status' });
});

const employeePieChart = computed(() => {
  const { labels, values } = employeeChartData(trips);
  const datasets = [
    createDatasetItem({ rgbStr: COLORS[7], label: '', values })
  ];
  return buildPieChartConfig({ labels, datasets, title: 'by Employee' });
});

const tripPieChart = computed(() => {
  const { labels, values } = tripChartData(trips);
  const datasets = [
    createDatasetItem({ rgbStr: COLORS[0], label: '', values })
  ];
  return buildPieChartConfig({ labels, datasets, title: 'Trip' });
});

const yearPieChart = computed(() => {
  const { labels, values } = yearChartData(trips);
  const datasets = [
    createDatasetItem({ rgbStr: COLORS[1], label: '', values })
  ];
  return buildPieChartConfig({ labels, datasets, title: 'per Year' });
});

const transportPieChart = computed(() => {
  const { labels, values } = transportChartData(trips);
  const datasets = [
    createDatasetItem({ rgbStr: COLORS[2], label: '', values })
  ];
  return buildPieChartConfig({ labels, datasets, title: 'Transport' });
});

const missionPieChart = computed(() => {
  const { labels, values } = missionChartData(trips);
  const datasets = [
    createDatasetItem({ rgbStr: COLORS[3], label: '', values })
  ];
  return buildPieChartConfig({ labels, datasets, title: 'Mission' });
});

const yearBarChart = computed(() => {
  const { labels, values } = yearChartData(trips);
  const datasets = [
    createDatasetItem({
      rgbStr: COLORS[4],
      label: '',
      // values: [props.totalCarbonFootprint, ...values]
      values: values
    })
  ];
  return buildBarChartConfig({
    xticks: labels,
    // labels: ['Total', ...labels],
    labels: labels,
    datasets,
    title: 'per Year',
    baselineValue: 1000,
    annotType: 'line',
    annotLabel: 'baseline:'
  });
});

const TripBarChart = computed(() => {
  const { labels: tripLabels, values: tripValues } = tripChartData(trips);
  const { labels: transportLabels, values: transportValues } = transportChartData(trips);

  const totalDatasets = 2 + tripValues.length;

  const datasetValues = [];

  datasetValues[0] = Array(totalDatasets).fill(0);
  datasetValues[0][0] = props.totalCarbonFootprint;

  const tripArray = [0, ...tripValues, 0];
  datasetValues.push(tripArray);

  transportValues.forEach((val, i) => {
    const transportArray = Array(totalDatasets).fill(0);
    transportArray[totalDatasets - 1] = val;
    datasetValues.push(transportArray);
  });

  const datasets = datasetValues.map((data, i) => {
    return createDatasetItem({
      rgbStr: COLORS[5],
      label: i >= 2 ? transportLabels[transportValues.indexOf(data[data.length - 1])] : '',
      values: data
    });
  });

  return buildBarChartConfig({
    labels: ['Total', ...tripLabels, 'Transport'],
    datasets,
    title: 'Carbon Footprint',
    baselineValue: baseline.value,
    annotType: 'label',
    stacked: true,
    annotLabel: 'recommended:'
  });
});

watch(
  () => props.trips,
  (newVal) => {
    trips.value = newVal;
    baseline.value = computeBaseline(newVal);
  },
  { immediate: true }
);
</script>

<style scoped>
.chart-wrapper, .chart-wrapper canvas {
  width: 100% !important;
  min-height: unset;
}

.pie-wrapper{
  height: 10rem !important;
  width: 80% !important;
}

.bar-wrapper{
  height: 20rem !important;
}

</style>