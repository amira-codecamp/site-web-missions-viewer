
import { createRouter, createWebHistory } from 'vue-router';
import LogInPage from '@/components/LogInPage.vue';
import MemberPage from '@/components/MemberPage.vue';
import store from '@/store/index';


const routes = [
  {
    path: '/',
    redirect: '/login',
  },
  {
    path: '/login',
    name: 'login',
    component: LogInPage,
  },
  {
    path: '/member',
    name: 'member',
    component: MemberPage,
    meta: { requiresAuth: true },
  },
];


const router = createRouter({
  history: createWebHistory(),
  routes,
});


// router.beforeEach((to, from, next) => {
//   const isAuthenticated = store.state.isAuthenticated;
//   if (to.meta.requiresAuth && !isAuthenticated) {
//     next('/login');
//   } else {
//     next();
//   }
// });


export default router;