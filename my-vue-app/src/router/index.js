import { createRouter, createWebHistory } from 'vue-router';
import MainPage from '../components/MainPage.vue';
import UserPage from '../components/UserPage.vue';

const routes = [
  {
    path: '/',
    name: 'MainPage',
    component: MainPage
  },
  {
    path: '/user/:id',
    name: 'UserPage',
    component: UserPage
  }
];

const router = createRouter({
  history: createWebHistory(),
  routes
});

export default router;