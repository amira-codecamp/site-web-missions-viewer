
<template>
  <div class="columns is-multiline is-gapless">

    <div class="column is-7">
      <div class="chart-wrapper bar-wrapper">
        <GenericChart
          :chartType="'bar'"
          :labels="yearBarChart.labels"
          :datasets="yearBarChart.datasets"
          :options="yearBarChart.options"
        />
      </div>
    </div>

    <div class="mb-4 column is-full">
      <span class="has-text-weight-semibold is-size-7">Trips Footprint</span>
    </div>

    <div class="column is-8">
      <div class="chart-wrapper bar-wrapper">
        <GenericChart
          :chartType="'bar'"
          :labels="TripBarChart.labels"
          :datasets="TripBarChart.datasets"
          :options="TripBarChart.options"
        />
      </div>
    </div>

    <div class="column is-2">
      <div class="chart-wrapper pie-wrapper">
        <GenericChart
          :labels="tripPieChart.labels"
          :datasets="tripPieChart.datasets"
          :options="tripPieChart.options"
          :chartType="'pie'"
        />
      </div>

      <div class="chart-wrapper pie-wrapper">
        <GenericChart
          :labels="missionPieChart.labels"
          :datasets="missionPieChart.datasets"
          :options="missionPieChart.options"
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

  </div>
</template>

<script setup>
defineOptions({
  name: 'TripsCharts',
})

import { useStore } from '@/store'
import { computed } from 'vue'
import GenericChart from '@/components/GenericChart.vue'

const store = useStore()

const props = defineProps({
  totalCarbonFootprint: {
    type: Number,
    required: true,
  },
})

const trips = computed(() => store.state.trips)

// Charts
const BORDER_COLOR = 'rgba(88, 80, 141, 1)';
const BASELINE_LABEL_PREFIX = 'Baseline';
const BORDER_WIDTH = 1;
const BAR_TICKNESS = 25;

const getValueColor = (value, baseline = 1000) => {
  const intensity = Math.min(1, value / baseline);
  return `rgba(88, 134, 165, ${0.2 + 0.8 * intensity})`;
};

const createBaselineAnnotation = (baseline, borderColor, labelPrefix) => ({
  drawTime: 'afterDatasetsDraw',
  annotations: {
    baselineLine: {
      type: 'line',
      yMin: baseline,
      yMax: baseline,
      borderColor,
      borderWidth: 2,
      borderDash: [6, 6],
      label: {
        display: true,
        content: `${labelPrefix} ${baseline}`,
        position: 'start',
        backgroundColor: 'white',
        color: borderColor,
        font: { weight: 'bold' },
      },
    },
  },
});

const createDatasetItem = ({ label, values, baselineValue }) => ({
  label,
  data: values,
  borderColor: BORDER_COLOR,
  backgroundColor: values.map(v => getValueColor(v, baselineValue)),
  borderWidth: BORDER_WIDTH,
  barThickness: BAR_TICKNESS
});

const createBarOptions = (title, baselineValue, stacked = false) => ({
  responsive: true,
  plugins: {
    legend: { display: false },
    title: { display: true, text: title },
    annotation: baselineValue !== null
      ? createBaselineAnnotation(baselineValue, BORDER_COLOR, BASELINE_LABEL_PREFIX)
      : undefined,
  },
  scales: {
    x: { 
      ticks: { display: false },
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
    title: { display: true, text: title },
  },
});

const buildBarChartConfig = ({ labels, datasets, title, baselineValue = null, stacked = false }) => ({
  labels,
  datasets: datasets,
  options: createBarOptions(title, baselineValue, stacked),
});

const buildPieChartConfig = ({ labels, datasets, title }) => ({
  labels,
  datasets: datasets,
  options: createPieOptions(title),
});

const baseline = computed(() => {
  // baseline: 1-tonne CO2 per person per year
  const dates = trips.value
    .map(trip => trip.mission?.start_date)
    .filter(Boolean)
    .map(dateStr => new Date(dateStr));

  if (dates.length === 0) return 1000;

  const minDate = new Date(Math.min(...dates.map(d => d.getTime())));
  const now = new Date();

  const yearsDiff = now.getFullYear() - minDate.getFullYear();
  const monthsDiff = now.getMonth() - minDate.getMonth();

  const totalMonths = yearsDiff * 12 + monthsDiff + 1;
  const baselinePerMonth = 1000 / 12;

  return Math.round(totalMonths * baselinePerMonth);
});

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

const tripPieChart = computed(() => {
  const { labels, values } = tripChartData(trips);
  const datasets = [
    createDatasetItem({ label: '', values, baselineValue: baseline.value })
  ];
  return buildPieChartConfig({ labels, datasets, title: 'Destination City' });
});

const transportPieChart = computed(() => {
  const { labels, values } = transportChartData(trips);
  const datasets = [
    createDatasetItem({ label: '', values, baselineValue: baseline.value })
  ];
  return buildPieChartConfig({ labels, datasets, title: 'Transport Mode' });
});

const missionPieChart = computed(() => {
  const { labels, values } = missionChartData(trips);
  const datasets = [
    createDatasetItem({ label: '', values, baselineValue: baseline.value })
  ];
  return buildPieChartConfig({ labels, datasets, title: 'Travel Reason' });
});

const yearBarChart = computed(() => {
  const { labels, values } = yearChartData(trips);
  const datasets = [
    createDatasetItem({
      label: '',
      values: [props.totalCarbonFootprint, ...values],
      baselineValue: baseline.value
    })
  ];
  return buildBarChartConfig({
    labels: ['Total Footprint', ...labels],
    datasets,
    title: 'Footprint By Year',
    baselineValue: baseline.value
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
      label: i >= 2 ? transportLabels[transportValues.indexOf(data[data.length - 1])] : '',
      values: data,
      baselineValue: baseline.value
    });
  });

  return buildBarChartConfig({
    labels: ['Total Footprint', ...tripLabels, 'Transport'],
    datasets,
    title: '',
    baselineValue: baseline.value,
    stacked: true
  });
});
</script>

<style scoped>
.chart-wrapper, .chart-wrapper canvas {
  width: 100% !important;
  min-height: unset;
}

.pie-wrapper{
  height: 15rem !important;
}

.bar-wrapper{
  height: 25rem !important;
}

.column {
  padding-top: 0 !important;
  padding-bottom: 0 !important; 
  margin-bottom: 0 !important; 
  margin-top: 0 !important; 
}
</style>