import { createRouter, createWebHistory, RouteRecordRaw } from 'vue-router'
import LogIn from '@/components/LogIn.vue'
import Dashboard from '@/components/Dashboard.vue'
import ResetPassword from '@/components/ResetPassword.vue'
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
  },
  {
    path: '/login',
    name: 'login',
    component: LogIn,
  },
  {
    path: '/reset',
    name: 'ResetPassword',
    component: ResetPassword,
    props: route => ({ token: route.query.token })
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