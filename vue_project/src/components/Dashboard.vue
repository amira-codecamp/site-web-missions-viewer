<template>
  <div class="layout columns">
    <div class="side-bar column is-1">
      <SidebarMenu :menu="sidebarMenu" @item-click="onItemClick" />
    </div>

    <div class="main-content column is-11">
      <Mission v-if="isManager || isStandard" />
      <Admin v-if="isAdmin" />
      <!-- <Account /> -->
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { SidebarMenu } from 'vue-sidebar-menu'
import 'vue-sidebar-menu/dist/vue-sidebar-menu.css'

import { logout, getPermission, fetchToken, getData, setData } from '@/composables/session'
const { isAdmin, isManager, isStandard } = getPermission()
import services from '@/composables/services'

import Mission from '@/components/Mission.vue'
import Admin from '@/components/Admin.vue' 
// import Account from '@/components/Account.vue'


const sidebarMenu = ref([]);

function onItemClick(event, item) {
  if (item.title === 'Logout') {
    logout()
  }
}

onMounted(async () => {
  document.title = 'Dashboard'
  sidebarMenu.value = [
    {
      header: 'HOME',
      hiddenOnCollapse: true,
    },
    ...(isAdmin.value ? [{
      title: 'Admin',
      icon: 'fa fa-users',
    }] : []),
    ...(isManager.value || isStandard.value ? [{
      title: 'Mission',
      icon: 'fa fa-route',
    }] : []),
    // {
    //   title: 'Account',
    //   icon: 'fa fa-user-cog',
    // },
    {
      title: 'Logout',
      icon: 'fa fa-sign-out-alt',
    },
  ];
  if (Object.keys(getData()).length === 0) {
    const token = await fetchToken()
    const data = {}
    if (isAdmin.value) {
      data.employees = await services.employees.list(token)
      data.groups = await services.groups.list(token)
      data.users = await services.users.list(token)
      data.status = await services.status.list(token)
    } else if (isStandard.value) {
      data.trips = await services.trips.list(token)
      data.missions = await services.missions.list(token)
    } else if (isManager.value) {
      data.transports = await services.transports.list(token)
      data.trips = await services.trips.list(token)
      data.employees = await services.employees.list(token)
      data.missions = await services.missions.list(token)
      data.status = await services.status.list(token)
    }
    setData(data)
  }
})
</script>

<style scoped>
.v-sidebar-menu {
  --vsm-base-bg: #f5f7fa;
  --vsm-item-color: #333;
  --vsm-icon-bg: #333;
  --vsm-icon-color: white;
  --vsm-header-item-color: rgb(46, 66, 165);
}
</style>