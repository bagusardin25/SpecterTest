import { createRouter, createWebHistory } from 'vue-router'
import BindingView from '../views/BindingView.vue'
import SimulationView from '../views/SimulationView.vue'
import ReportView from '../views/ReportView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'binding',
      component: BindingView
    },
    {
      path: '/simulate',
      name: 'simulation',
      component: SimulationView
    },
    {
      path: '/report',
      name: 'report',
      component: ReportView
    }
  ]
})

export default router
