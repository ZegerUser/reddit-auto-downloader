import { createRouter, createWebHistory } from 'vue-router'
import mainPage from '../pages/mainPage.vue'
import configPage from '../pages/configPage.vue'
import subredditsViewerPage from '../pages/subredditsViewerPage.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'main',
      component: mainPage
    },
    {
      path: '/config',
      name: 'config',
      component: configPage
    },
    {
      path: '/r',
      name: 'subredditsViewer',
      component: subredditsViewerPage
    }
  ]
})

export default router
