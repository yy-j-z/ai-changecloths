import { createRouter, createWebHistory } from 'vue-router'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    {
      path: '/',
      name: 'studio',
      component: () => import('../views/AvatarStudioView.vue'),
    },
  ],
})

export default router

