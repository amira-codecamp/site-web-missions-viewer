import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import LogInForm from '@/pages/LogInForm.vue'
import TripsPage from '@/pages/TripsPage.vue'
import MemberPage from '@/pages/MemberPage.vue'
import TripForm from '@/pages/TripForm.vue'
import { useStore } from '@/store'

const routes: RouteRecordRaw[] = [
  {
    path: '/',
    redirect: '/login',
  },
  {
    path: '/login',
    name: 'login',
    component: LogInForm,
  },
  {
    path: '/member',
    name: 'member',
    component: MemberPage,
    meta: { requiresAuth: true },
    children: [
      {
        path: 'trips',
        name: 'trips',
        component: TripsPage,
      },
    ],
  },
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