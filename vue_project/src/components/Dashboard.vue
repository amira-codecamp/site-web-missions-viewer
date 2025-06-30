<template>
  <div class="layout columns">
    <div class="side-bar column is-1">
      <SidebarMenu :menu="sidebarMenu" @item-click="onItemClick" />
    </div>

    <div class="main-content column is-11">
      <Manager v-if="activePage === 'Trips' && !isAdmin" />
      <Admin v-if="activePage === 'Users' && isAdmin" />
      <Account v-if="activePage === 'Account'" />
      <!-- <router-view v-if="!activePage || activePage === 'Dashboard'" /> -->
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import { useStore } from '@/store'

const store = useStore()

import { SidebarMenu } from 'vue-sidebar-menu'
import 'vue-sidebar-menu/dist/vue-sidebar-menu.css'

import { logout } from '@/session'
import services from '@/services'

import Manager from '@/components/Manager.vue'
import Admin from '@/components/Admin.vue' 
import Account from '@/components/Account.vue'

import { fetchToken } from '@/session'


const isAdmin = ref(false);

const sidebarMenu = ref([]);

const activePage = ref('Dashboard')

function onItemClick(event, item) {
  if (item.title === 'Logout') {
    localStorage.removeItem('activePage');
    logout()
  } else {
    activePage.value = item.title
    localStorage.setItem('activePage', activePage.value)
  }
}

async function storeState() {
  await fetchToken();
  const accessToken = store.state.accessToken;

  const transports = await services.transports.list(accessToken)
  const status = await services.status.list(accessToken)
  const groups = await services.groups.list(accessToken)
  store.setItem('transports', transports.transports);
  store.setItem('status', status.status);
  store.setItem('groups', groups.groups);

  const account = store.state.account;

  if (account.group?.group_name === 'ADMIN') {
    const employees = await services.employees.list(accessToken)
    store.setItem('employees', employees.employees);
    const users = await services.users.list(accessToken)
    store.setItem('users', users.users);
  
  } else {
    const trips = await services.trips.list(accessToken)
    store.setItem('trips', trips.trips);
  }

  if (account.group?.group_name === 'MISSIONMANAGER') {
    const missions = await services.missions.list(accessToken)
    store.setItem('missions', missions.missions);
    const employees = await services.employees.list(accessToken)
    store.setItem('employees', employees.employees);
  }

}

onMounted(async () => {
  const savedPage = localStorage.getItem('activePage');
  activePage.value = savedPage
  document.title = 'Dashboard'
  if (!savedPage) {
    await storeState()
  }
  const account = store.state.account;
  const groupName = account.group?.group_name;
  if (groupName) {
    isAdmin.value = groupName === 'ADMIN';
  } else {
    console.error("Group name is undefined");
  }
  sidebarMenu.value = [
    {
      header: 'HOME',
      hiddenOnCollapse: true,
    },
    ...(isAdmin.value ? [{
      title: 'Users',
      icon: 'fa fa-users',
    }] : []),
    ...(!isAdmin.value ? [{
      title: 'Trips',
      icon: 'fa fa-route',
    }] : []),
    {
      title: 'Account',
      icon: 'fa fa-user-cog',
    },
    {
      title: 'Logout',
      icon: 'fa fa-sign-out-alt',
    },
  ];
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