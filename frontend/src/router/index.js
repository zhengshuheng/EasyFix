import { createRouter, createWebHistory, createWebHashHistory } from 'vue-router'
import { useKidStore } from '@/stores/kid'
import { useTrialStore } from '@/stores/trial'

// 试用版（VITE_TRIAL=true 构建，部署在 /{trial_key}/ 下）使用 hash 路由：
// 页面路径固定为 /{trial_key}/，资源走相对路径，路由切换不请求服务器。
const isTrial = import.meta.env.VITE_TRIAL === 'true'

const routes = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
  },
  {
    path: '/subscribe',
    name: 'Subscribe',
    component: () => import('@/views/Subscribe.vue'),
  },
  {
    path: '/',
    name: 'SelectKid',
    component: () => import('@/views/SelectKid.vue'),
  },
  {
    path: '/onboarding',
    name: 'Onboarding',
    component: () => import('@/views/Onboarding.vue'),
  },
  {
    path: '/home',
    // 首页已合并进分析页（/stats），旧路径全部重定向
    redirect: '/stats',
  },
  {
    path: '/questions',
    name: 'Questions',
    component: () => import('@/views/Questions.vue'),
  },
  {
    path: '/assessment',
    name: 'Assessment',
    component: () => import('@/views/Assessment.vue'),
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
        path: 'incentive',
        name: 'IncentiveConfig',
        component: () => import('@/views/IncentiveConfig.vue'),
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
    path: '/grammar',
    name: 'Grammar',
    component: () => import('@/views/Grammar.vue'),
  },
  {
    path: '/grammar/:id',
    name: 'GrammarLesson',
    component: () => import('@/views/Grammar.vue'),
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
    path: '/phonics',
    name: 'Phonics',
    component: () => import('@/views/Phonics.vue'),
  },
  {
    path: '/textbook-library',
    name: 'TextbookLibrary',
    component: () => import('@/views/TextbookLibrary.vue'),
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
  // 试用版（VITE_TRIAL=true）：hash 路由（部署在 /{trial_key}/ 下）
  // 正式版：history 路由，base=/app（/ 已让给官网主页）；本地 dev 未设置 VITE_APP_BASE 时保持 '/'
  history: isTrial ? createWebHashHistory() : createWebHistory(import.meta.env.VITE_APP_BASE || '/'),
  routes,
})

// 守卫：
// 1. 到期校验（刷新页面即重新查 /api/trial/status）：已到期 → 一律拦到订阅续费页
//    （subscribe 页无需登录；正式版/永不过期 is_pro=true 不受影响，如 easyfix_demo）
// 2. 登录墙：除 /login 外，无本地登录态（easyfix_token）一律跳登录页（带 redirect 回跳）
// 3. 除首页（选小孩）外，学习页面必须已选择小孩
// 4. 家长专属页必须已通过家长密码验证（存在 easyfix_token）
router.beforeEach(async (to) => {
  const trialStore = useTrialStore()
  if (!trialStore.statusLoaded) {
    await trialStore.loadStatus()
  }
  if (trialStore.expired && to.path !== '/subscribe') {
    return '/subscribe'
  }

  const kidStore = useKidStore()
  const token = localStorage.getItem('easyfix_token')
  if (to.path === '/login' || to.path === '/subscribe') return true
  if (!token) {
    return { path: '/login', query: { redirect: to.fullPath } }
  }
  if (to.path === '/') return true
  if (to.path === '/onboarding') return true
  if (to.meta?.adminOnly) {
    return token ? true : '/'
  }
  if (!kidStore.isKidSelected) {
    return '/'
  }
  return true
})

export default router
