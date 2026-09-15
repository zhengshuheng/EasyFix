import { createRouter, createWebHistory } from 'vue-router'
import { useKidStore } from '@/stores/kid'

const routes = [
  {
    path: '/',
    name: 'SelectKid',
    component: () => import('@/views/SelectKid.vue'),
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
  },
  {
    path: '/space/:id',
    name: 'SubjectSpace',
    component: () => import('@/views/SubjectSpace.vue'),
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
    path: '/parent-center',
    component: () => import('@/views/ParentCenter.vue'),
    meta: { adminOnly: true },
    redirect: '/parent-center/users',
    children: [
      {
        path: 'users',
        name: 'UserManage',
        component: () => import('@/views/UserManage.vue'),
      },
      {
        path: 'management',
        name: 'Management',
        component: () => import('@/views/Management.vue'),
      },
      {
        path: 'settings',
        name: 'Settings',
        component: () => import('@/views/Settings.vue'),
      },
    ],
  },
  // 旧独立家长页面路径重定向到家长中心
  { path: '/user-manage', redirect: '/parent-center/users' },
  { path: '/management', redirect: '/parent-center/management' },
  { path: '/settings', redirect: '/parent-center/settings' },
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

// 守卫：
// - 除首页（选小孩）外，学习页面必须已选择小孩
// - 家长专属页必须已通过家长密码验证（存在 easyfix_token）
router.beforeEach((to) => {
  const kidStore = useKidStore()
  if (to.path === '/') return true
  if (to.meta?.adminOnly) {
    return localStorage.getItem('easyfix_token') ? true : '/'
  }
  if (!kidStore.isKidSelected) {
    return '/'
  }
  return true
})

export default router
