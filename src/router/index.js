import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import Tasklist from '@/components/TaskList.vue'
import TaskStatus from '@/components/TaskStatus.vue'
import LoginPage from '@/components/LoginPage.vue'

const routes = [
  {
    path: '/',
    name: 'HomeView',
    component: HomeView
  },
  {
    path: '/list',
    name: 'TaskList',
    component: Tasklist
  },
  {
    path: '/status',
    name: 'TaskStatus',
    component: TaskStatus
  },
  {
    path: '/login',
    name: 'LoginPage',
    component: LoginPage
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
