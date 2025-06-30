import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import LogIn from '@/components/LogIn.vue'
import TripsPage from '@/pages/TripsPage.vue'
import MemberPage from '@/pages/MemberPage.vue'
import AdminPage from '@/pages/AdminPage.vue'
import Dashboard from '@/components/Dashboard.vue'
import { useStore } from '@/store'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/login',
  },
  {
    path: '/dashboard',
    name: '/dashboard',
    component: Dashboard,
    meta: { requiresAuth: true },
    children: [
      {
        path: 'trips',
        name: 'trips',
        component: TripsPage,
      },
      {
        path: 'admin',
        name: 'admin',
        component: AdminPage,
      },
    ],
  },
  {
    path: '/login',
    name: 'login',
    component: LogIn,
  },
  // {
  //   path: '/member',
  //   name: 'member',
  //   component: MemberPage,
  //   meta: { requiresAuth: true },
  //   children: [
  //     {
  //       path: 'trips',
  //       name: 'trips',
  //       component: TripsPage,
  //     },
  //     {
  //       path: 'admin',
  //       name: 'admin',
  //       component: AdminPage,
  //     },
  //   ],
  // },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const store = useStore()
  const { isAuthenticated, state } = store

  if (to.meta.requiresAuth && !isAuthenticated.value) {
    return next('/login')
  }

  next()
})

export default router