
import { createRouter, createWebHistory } from 'vue-router';
import LogInForm from '@/pages/LogInForm.vue';
import Dashboard from '@/components/Dashboard.vue';
import TripsPage from '@/pages/TripsPage.vue';
import store from '@/store/index';


const routes = [
  {
    path: '/',
    redirect: '/login',
  },
  {
    path: '/login',
    name: 'login',
    component: LogInForm,
  },
  // {
  //   path: '/member',
  //   name: 'member',
  //   component: MemberPage,
  //   meta: { requiresAuth: true },
  // },
  {
    path: '/dashboard',
    name: 'dashboard',
    component: Dashboard,
    meta: { requiresAuth: true },
    children: [
      {
        path: '/trips',
        name: 'trips',
        component: TripsPage
      },
    ]
  }
];


const router = createRouter({
  history: createWebHistory(),
  routes,
});


router.beforeEach((to, from, next) => {
  const isAuthenticated = store.getters.isAuthenticated;
  if (to.meta.requiresAuth && !isAuthenticated)  {
    next('/login');
  } else {
    next();
  }
});


export default router;