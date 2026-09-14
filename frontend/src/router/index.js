import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
  },
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
  },
  {
    path: '/questions',
    name: 'Questions',
    component: () => import('@/views/Questions.vue'),
  },
  {
    path: '/upload',
    name: 'Upload',
    component: () => import('@/views/Upload.vue'),
  },
  {
    path: '/stats',
    name: 'Stats',
    component: () => import('@/views/Stats.vue'),
  },
  {
    path: '/settings',
    name: 'Settings',
    component: () => import('@/views/Settings.vue'),
    meta: { adminOnly: true },
  },
  {
    path: '/management',
    name: 'Management',
    component: () => import('@/views/Management.vue'),
    meta: { adminOnly: true },
  },
  {
    path: '/upload',
    name: 'Upload',
    component: () => import('@/views/Upload.vue'),
    meta: { adminOnly: true },
  },
  {
    path: '/practice-sets',
    name: 'PracticeSets',
    component: () => import('@/views/PracticeSets.vue'),
  },
  {
    path: '/reading',
    name: 'Reading',
    component: () => import('@/views/Reading.vue'),
  },
  {
    path: '/reading-test/:id',
    name: 'ReadingTest',
    component: () => import('@/views/ReadingTest.vue'),
  },
  {
    path: '/words',
    name: 'Words',
    component: () => import('@/views/Words.vue'),
  },
  {
    path: '/learning-reports',
    name: 'LearningReports',
    component: () => import('@/views/LearningReports.vue'),
  },
  {
    path: '/motivation',
    name: 'Motivation',
    component: () => import('@/views/Motivation.vue'),
  },
  {
    path: '/learning-analysis',
    name: 'LearningAnalysis',
    component: () => import('@/views/LearningAnalysis.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

// 登录守卫：未登录一律跳转登录页；家长专属页面仅 admin 可进
router.beforeEach((to) => {
  const auth = useAuthStore()
  if (to.path === '/login') {
    return auth.isLoggedIn ? '/' : true
  }
  if (!auth.isLoggedIn) {
    return { path: '/login', query: to.fullPath !== '/' ? { redirect: to.fullPath } : {} }
  }
  if (to.meta?.adminOnly && !auth.isAdmin) {
    return '/'
  }
  return true
})

export default router
