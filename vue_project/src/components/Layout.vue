<template>
  <div class="page">

    <div class="page-body">
      <router-view />
    </div>

    <div class="page-footer">
      <Footer />
    </div>

  </div>
</template>

<script setup>
defineOptions({
  name: 'BaseLayout',
})

import 'bulma-multiselect/css/bulma-multiselect.min.css'
import 'bulma-tooltip/dist/css/bulma-tooltip.min.css'
import 'leaflet/dist/leaflet.css'

import Footer from '@/components/Footer'
</script>

<style lang="scss">
@import "~bulma/bulma";
@import "~@fortawesome/fontawesome-free/css/all.css";

.page {
  display: flex;
  flex-direction: column;
  min-height: 200vh;
}

.navbar,
.navbar-brand {
  height: 2rem !important;
  min-height: unset;
}

.page-header {
  flex-shrink: 0;
  height: 3rem;
}

.page-body {
  flex-grow: 1;
  overflow: auto;
  padding: 1rem;
}

.page-footer {
  flex-shrink: 0;
  padding: 1rem;
  height: 10rem;
}
</style>