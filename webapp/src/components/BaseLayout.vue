
<template>
  <div class="app">

    <div class="page-header">
      <Header />
    </div>

    <div class="page-body">
      <router-view />
    </div>

    <div class="page-footer">
      <Footer />
    </div>

  </div>
</template>


<script>
  import Header from '@/components/Header.vue'
  import Footer from '@/components/Footer.vue'

  export default {
    name: 'BaseLayout',
    components: {
      Header,
      Footer
    },
  }
</script>


<style lang="scss">
  @import "~bulma/bulma";
</style>