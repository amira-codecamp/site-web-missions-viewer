
<template>
  <div class="page">

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

  .page {
    display: flex;
    flex-direction: column;
    min-height: 100vh;
  }

  .page-header {
    flex-shrink: 0;
  }

  .page-body {
    flex-grow: 1;
    overflow: auto;
    display: flex;
    flex-direction: column;
    justify-content: center;
  }

  .page-footer {
    flex-shrink: 0;
  }
</style>