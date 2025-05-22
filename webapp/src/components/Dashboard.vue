
<template>

  <div class="page-header">
    <nav class="navbar is-light">
      <div class="navbar-brand">
        <div class="navbar-item">
          <span class="has-text-weight-semibold is-size-6">{{ user }}</span>
        </div>

        <a
          role="button"
          class="navbar-burger"
          :class="{ 'is-active': isBurgerActive }"
          aria-label="menu"
          aria-expanded="false"
          @click="toggleBurger"
        >
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
          <span aria-hidden="true"></span>
        </a>
      </div>

      <div class="navbar-menu" :class="{ 'is-active': isBurgerActive }">
        <div class="navbar-end">
          <a class="navbar-item" @click="viewDashboard">Home</a>
          <a class="navbar-item" @click="viewTrips">Trips</a>
          <a class="navbar-item" @click="logout">Logout</a>
        </div>
      </div>
    </nav>
  </div>

  <div class="page-body">
    <router-view />
  </div>

</template>

<script>
  export default {
    name: 'Dashboard',
    data() {
      return {
        isBurgerActive: false
      };
    },
    computed: {
      user() {
        return this.$store.state.user;
      },
    },
    methods: {
      toggleBurger() {
        this.isBurgerActive = !this.isBurgerActive;
      },
      logout() {
        Promise.all([
          this.$store.dispatch('clearTrips'),
          this.$store.dispatch('clearEmployees'),
          this.$store.dispatch('clearTransports'),
          this.$store.dispatch('clearMissions'),
          this.$store.dispatch('clearIsManager'),
          this.$store.dispatch('clearUser')
        ]).then(() => {
          this.$router.push('/login');
        });
      },
      viewTrips() {
        this.$router.push('/trips');
      },
      viewDashboard() {
        this.$router.push('/dashboard');
      },
    },
    watch: {
      $route(to) {
        if (to.path === '/dashboard') {
          document.title = "Dashboard | LIPN-carbon";
        }
      },
    },
    mounted() {
      document.title = "Dashboard | LIPN-carbon";
    }
  };
</script>