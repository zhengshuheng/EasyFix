<template>
  <div id="app">
    <el-container>
      <el-header>
        <div class="header-content">
          <h1 class="logo" @click="navTo('/home')">EasyFix</h1>

          <!-- 选择页隐藏导航，其余页面显示。
               全部学科：学科(tab页入口) 平铺；指定学科：该学科功能项直接作为一级菜单 -->
          <el-menu v-if="!isSelectPage" mode="horizontal" :default-active="activeMenu">
            <template v-if="subjectStore.isAll">
              <el-menu-item
                v-for="s in subjectStore.subjects"
                :key="s.id"
                :index="'/space/' + s.id"
                @click="openSubjectSpace(s.id)"
              >{{ s.name }}</el-menu-item>
            </template>
            <template v-else>
              <template v-if="subjectStore.isEnglish">
                <el-menu-item index="/words" @click="navTo('/words')">单词</el-menu-item>
                <el-menu-item index="/phonics" @click="navTo('/phonics')">拼读</el-menu-item>
                <el-menu-item index="/grammar" @click="navTo('/grammar')">语法</el-menu-item>
                <el-menu-item index="/reading" @click="navTo('/reading')">阅读</el-menu-item>
              </template>
              <el-menu-item index="/practice-sets" @click="navTo('/practice-sets')">练习</el-menu-item>
              <el-menu-item index="/questions" @click="navTo('/questions')">错题</el-menu-item>
              <el-menu-item index="/assessment" @click="navTo('/assessment')">评测</el-menu-item>
              <el-menu-item index="/learning-reports" @click="navTo('/learning-reports')">报告</el-menu-item>
            </template>
            <!-- 学习分析：小孩可公开查看自己的学习状态；激励中心孩子与家长都需要 -->
            <el-menu-item index="/stats" @click="navTo('/stats')">分析</el-menu-item>
            <el-menu-item index="/motivation" @click="navTo('/motivation')">激励中心</el-menu-item>
            <!-- 家长中心：与激励中心并列，点击弹密码锁验证后进入 -->
            <el-menu-item index="/parent-center" @click="parentLockVisible = true">家长中心</el-menu-item>
          </el-menu>

          <div v-if="!isSelectPage && !isParentCenter" class="header-user">
            <!-- 学科切换：学习空间 = 小孩 + 学科（null = 全部/汇总） -->
            <el-dropdown v-if="kidStore.isKidSelected" trigger="click" @command="handleSubjectCommand">
              <span class="subject-chip">
                <el-icon class="subject-icon"><Collection /></el-icon>
                <span class="subject-name">{{ subjectStore.isAll ? '全部学科' : subjectStore.activeSubject?.name }}</span>
                <el-icon class="arrow"><ArrowDown /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="subject:" :class="{ active: subjectStore.isAll }">
                    全部（汇总）
                    <el-icon v-if="subjectStore.isAll"><Check /></el-icon>
                  </el-dropdown-item>
                  <el-dropdown-item
                    v-for="s in subjectStore.subjects"
                    :key="s.id"
                    :command="'subject:' + s.id"
                    :class="{ active: s.id === subjectStore.activeSubjectId }"
                  >
                    {{ s.name }}
                    <el-icon v-if="s.id === subjectStore.activeSubjectId"><Check /></el-icon>
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
            <!-- 年级切换：学习空间 = 小孩 + 学科 + 年级（null = 全部年级） -->
            <el-dropdown v-if="kidStore.isKidSelected" trigger="click" @command="handleGradeCommand">
              <span class="subject-chip grade-chip">
                <el-icon class="subject-icon"><Histogram /></el-icon>
                <span class="subject-name">{{ subjectStore.activeGradeName }}</span>
                <el-icon class="arrow"><ArrowDown /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="grade:" :class="{ active: subjectStore.isAllGrade }">
                    全部年级
                    <el-icon v-if="subjectStore.isAllGrade"><Check /></el-icon>
                  </el-dropdown-item>
                  <el-dropdown-item
                    v-for="g in gradeOptions"
                    :key="g.value"
                    :command="'grade:' + g.value"
                    :class="{ active: g.value === subjectStore.activeGrade }"
                  >
                    <span class="grade-option">
                      <span>{{ g.label }}</span>
                      <span v-if="kidGrade && g.value <= kidGrade" class="grade-badge" :class="{ 'is-current': g.value === kidGrade }">
                        {{ g.value === kidGrade ? '当前' : '已学' }}
                      </span>
                    </span>
                    <el-icon v-if="g.value === subjectStore.activeGrade"><Check /></el-icon>
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
            <!-- 小孩会话：当前小孩 + 下拉切换 -->
            <el-dropdown v-if="kidStore.isKidSelected" trigger="click" @command="handleKidCommand">
              <span class="user-chip">
                <span class="mini-avatar" :style="{ background: avatarColor(kidStore.activeKid) }">
                  {{ kidStore.kidName.slice(0, 1) || '?' }}
                </span>
                <span class="user-name">{{ kidStore.kidName }}</span>
                <el-icon class="arrow"><ArrowDown /></el-icon>
              </span>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item
                    v-for="k in kids"
                    :key="k.id"
                    :command="'kid:' + k.id"
                    :class="{ active: k.id === kidStore.activeKid?.id }"
                  >
                    {{ k.display_name }}
                    <el-icon v-if="k.id === kidStore.activeKid?.id"><Check /></el-icon>
                  </el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
            <!-- 官网：新标签打开官网首页（浏览营销内容），不打断当前学习会话 -->
            <a class="site-link" href="/site/" target="_blank" rel="noopener">官网</a>
            <!-- 退出登录：清空空间+官网双 token，回官网登录/注册表单 -->
            <el-button class="logout-btn" text @click="logout">
              <el-icon :size="15" style="margin-right: 3px; vertical-align: -2px;"><SwitchButton /></el-icon>
              退出
            </el-button>
          </div>
        </div>

        <ParentLockDialog v-model="parentLockVisible" @success="goParentCenter" />
      </el-header>
      <el-main>
        <router-view :key="spaceKey" />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAppConfigStore } from '@/stores/appConfig'
import { useKidStore } from '@/stores/kid'
import { useSubjectStore } from '@/stores/subject'
import { useAuthStore } from '@/stores/auth'
import { usersApi } from '@/api/users'
import ParentLockDialog from '@/components/ParentLockDialog.vue'

const route = useRoute()
const router = useRouter()
const appConfigStore = useAppConfigStore()
const kidStore = useKidStore()
const subjectStore = useSubjectStore()
const authStore = useAuthStore()

// 年级选项（学习空间年级切换）
const gradeOptions = [
  { label: '一年级', value: 1 },
  { label: '二年级', value: 2 },
  { label: '三年级', value: 3 },
  { label: '四年级', value: 4 },
  { label: '五年级', value: 5 },
  { label: '六年级', value: 6 },
  { label: '初一', value: 7 },
  { label: '初二', value: 8 },
  { label: '初三', value: 9 },
  { label: '高一', value: 10 },
  { label: '高二', value: 11 },
  { label: '高三', value: 12 },
]

// 当前小孩的年级（由入学日期动态推断）；未选小孩/未填入学日期时返回 null（不标"已学"）
const kidGrade = computed(() => {
  const g = kidStore.activeKid?.current_grade
  const n = Number(g)
  return n >= 1 && n <= 12 ? n : null
})

const parentLockVisible = ref(false)
const kids = ref([])

// 选择页（选人/创建入口）不显示顶部导航与用户区
const isSelectPage = computed(() => route.path === '/')

// 学习空间指纹（小孩 + 学科 + 年级）：任一变化就让当前页面重新挂载并重新拉数据，
// 否则页面只在 onMounted 读一次空间，切换后数据不更新，看起来像"没切换成功"
const spaceKey = computed(() => [
  kidStore.activeKid?.id ?? 'all',
  subjectStore.activeSubjectId ?? 'all',
  subjectStore.activeGrade ?? 'all',
].join('|'))
// 家长中心：隐藏顶部菜单与学科/年级/小孩切换，由家长中心内部提供出口
const isParentCenter = computed(() => route.path.startsWith('/parent-center'))
// 顶部菜单高亮：家长中心子路由统一高亮"家长中心"
const activeMenu = computed(() =>
  route.path.startsWith('/parent-center') ? '/parent-center' : route.path
)

function navTo(path) {
  if (route.path !== path) router.push(path)
}

// 英语专属功能页（其他学科没有这些功能）：切到非英语学科时不能停留，跳到该学科默认页
const ENGLISH_ONLY_PAGES = ['/words', '/phonics', '/grammar', '/reading', '/learning-reports']

// 学科一级菜单：切换空间学科；留在当前功能页（spaceKey 重挂载重新拉数据），
// 仅当选择页或当前页是英语专属页且切到非英语学科时跳该学科默认页
function openSubjectSpace(id) {
  subjectStore.select(id)
  if (route.path === '/') {
    router.push('/home')
    return
  }
  if (!subjectStore.isEnglish && ENGLISH_ONLY_PAGES.includes(route.path)) {
    if (route.path !== '/practice-sets') router.push('/practice-sets')
  }
  // 其余情况留在当前页面，由 spaceKey 变化触发重挂载重新拉数据
}

// 家长齿轮入口：弹密码锁，验证成功直达家长中心
// 进入前记录小孩端来源页面，退出家长中心时按此返回原状态
function goParentCenter() {
  sessionStorage.setItem('easyfix_return_path', route.fullPath)
  router.push('/parent-center')
}

const AVATAR_COLORS = ['#409eff', '#67c23a', '#e6a23c', '#f56c6c', '#9b59b6', '#00b5ad']

function avatarColor(k) {
  const seed = k?.id || k?.username?.length || 0
  return AVATAR_COLORS[seed % AVATAR_COLORS.length]
}

async function loadKids() {
  try {
    const { data } = await usersApi.listKids()
    kids.value = (data.kids || []).filter((k) => k.enabled)
  } catch (e) {
    // 忽略：家长会话下拉展示失败不影响使用
  }
}

onMounted(() => {
  loadKids()
  subjectStore.loadSubjects()
  // 家长会话时预加载默认年级等应用配置（config 接口需家长权限）
  if (localStorage.getItem('easyfix_token')) {
    appConfigStore.load()
  }
})

// 学科切换：更新学习空间学科；留在当前页面（由 spaceKey 触发重挂载重新拉数据），
// 仅当选择页或当前页是英语专属页且切到非英语学科时跳该学科默认页
function handleSubjectCommand(cmd) {
  const raw = cmd.startsWith('subject:') ? cmd.slice('subject:'.length) : ''
  subjectStore.select(raw === '' ? null : Number(raw))
  if (route.path === '/') {
    router.push('/home')
    return
  }
  if (!subjectStore.isAll && !subjectStore.isEnglish && ENGLISH_ONLY_PAGES.includes(route.path)) {
    if (route.path !== '/practice-sets') router.push('/practice-sets')
  }
  // 其余情况留在当前页面，由 spaceKey 触发重挂载重新拉数据
}

// 年级切换：更新学习空间年级；**留在当前页面**（由 spaceKey 触发重挂载重新拉数据），仅在选择页时进首页
function handleGradeCommand(cmd) {
  const raw = cmd.startsWith('grade:') ? cmd.slice('grade:'.length) : ''
  subjectStore.setGrade(raw === '' ? null : Number(raw))
  if (route.path === '/') router.push('/home')
}

// 小孩会话下拉
function handleKidCommand(cmd) {
  if (cmd.startsWith('kid:')) {
    const k = kids.value.find((x) => x.id === Number(cmd.split(':')[1]))
    if (k) {
      kidStore.select(k)
      // 切换小孩：默认年级跟随新小孩（用户手动选过年级则保持不动）；不重置学科空间
      subjectStore.applyKidDefaultGrade(k)
      // 若当前在选择页则进入首页；否则原地切换
      if (route.path === '/') router.push('/home')
      else loadKids()
    }
  }
}

// 退出登录：与选择页一致，清空空间+官网双 token 后回官网登录表单
function logout() {
  authStore.logout()
  localStorage.removeItem('easyfix_trial_key')
  localStorage.removeItem('easyfix_kid')
  localStorage.removeItem('easyfix_account_token') // 官网账号 token 一并删除，否则官网面板残留"已登录"
  localStorage.removeItem('easyfix_user')
  window.location.href = '/site/#trial?tab=login'
}
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

#app {
  min-height: 100vh;
}

/* 移动端适配见 src/styles/mobile.css（由 main.js 最后 import，
   源序在后才能覆盖下方 .el-header 的 height:60px !important） */

.el-header {
  background-color: #409eff;
  color: white;
  padding: 0;
  height: 60px !important;
  line-height: 60px;
}

.header-content {
  display: flex;
  align-items: center;
  height: 100%;
  padding: 0 20px;
  width: 100%;
  gap: 10px;
}

.header-content h1 {
  margin-right: 20px;
  font-size: 18px;
  white-space: nowrap;
  flex-shrink: 0;
  cursor: pointer;
  user-select: none;
}

.header-content .el-menu {
  background-color: transparent;
  border: none;
  flex: 1;
  display: flex;
  overflow-x: auto;
}

.header-content .el-menu::-webkit-scrollbar {
  display: none;
}

.header-content .el-menu-item {
  color: white !important;
  font-size: 16px;
  padding: 0 16px;
  height: 60px;
  line-height: 60px;
  min-width: auto;
  white-space: nowrap;
  flex-shrink: 0;
  transition: all 0.3s ease;
}

.header-content .el-sub-menu .el-sub-menu__title {
  color: white !important;
  background-color: transparent !important;
  font-size: 16px;
  padding: 0 16px;
  height: 60px;
  line-height: 60px;
  white-space: nowrap;
  flex-shrink: 0;
}

.header-content .el-sub-menu .el-sub-menu__title:hover,
.header-content .el-sub-menu .el-sub-menu__title.is-active {
  color: white !important;
  background-color: rgba(255, 255, 255, 0.2) !important;
}

.header-user {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: auto;
  flex-shrink: 0;
  white-space: nowrap;
}

.user-chip {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #fff;
  cursor: pointer;
  padding: 4px 10px;
  border-radius: 20px;
  transition: background 0.2s ease;
}

.user-chip:hover {
  background: rgba(255, 255, 255, 0.2);
}

.subject-chip {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #fff;
  cursor: pointer;
  padding: 4px 10px;
  border-radius: 20px;
  transition: background 0.2s ease;
}

.subject-chip:hover {
  background: rgba(255, 255, 255, 0.2);
}

.subject-icon {
  font-size: 14px;
}

.subject-name {
  color: #fff;
  font-size: 14px;
  max-width: 80px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.mini-avatar {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  color: #fff;
  font-size: 13px;
  font-weight: bold;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.admin-avatar {
  background: #f56c6c;
}

.arrow {
  font-size: 12px;
}

.user-name {
  color: #fff;
  font-size: 14px;
  max-width: 120px;
  overflow: hidden;
  text-overflow: ellipsis;
}

.logout-btn {
  color: #fff !important;
}

.site-link {
  color: #fff;
  margin-left: 10px;
  font-size: 14px;
  opacity: 0.92;
}

.site-link:hover {
  opacity: 1;
  text-decoration: underline;
}

.el-dropdown-menu .active {
  color: #409eff;
  font-weight: bold;
}

.header-content .el-menu-item:hover {
  background-color: rgba(255, 255, 255, 0.2) !important;
}

.header-content .el-menu-item.is-active {
  background-color: rgba(255, 255, 255, 0.3) !important;
  transform: scale(1.1);
  font-weight: bold;
}

.el-main {
  padding: 20px;
  background-color: #f5f5f5;
  min-height: calc(100vh - 60px);
}

/* 全局 H5 适配（表格/卡片/按钮等）统一在 src/styles/mobile.css，此处不再重复 */

/* ==================== 全局字体层级 ==================== */
h1, .h1 {
  font-size: var(--font-h1);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
  margin: 0 0 16px 0;
}

h2, .h2 {
  font-size: var(--font-h2);
  font-weight: var(--font-weight-bold);
  color: var(--text-primary);
  margin: 0 0 12px 0;
}

h3, .h3 {
  font-size: var(--font-h3);
  font-weight: var(--font-weight-semibold);
  color: var(--text-primary);
  margin: 0 0 8px 0;
}

body, p {
  font-size: var(--font-body);
  color: var(--text-secondary);
  line-height: 1.6;
}

.text-secondary, .text-muted {
  font-size: var(--font-small);
  color: var(--text-muted);
}

/* 全局字体平滑 */
body {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* 统一卡片hover效果 */
.el-card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg) !important;
  transition: all 0.3s ease;
}

/* 统一按钮hover效果 */
.el-button:not(.is-text):not(.is-link):hover {
  transform: translateY(-2px);
  box-shadow: var(--shadow-md);
}

/* 统一输入框focus */
.el-input__wrapper:focus-within {
  box-shadow: 0 0 0 1px var(--accent-blue) inset;
}

/* 渐变按钮样式 */
.btn-gradient {
  background: var(--accent-gradient) !important;
  border: none !important;
  color: var(--text-white) !important;
}

.btn-gradient:hover {
  opacity: 0.9;
  transform: translateY(-2px);
}

/* 年级下拉：已学/当前 标识 */
.grade-option {
  display: flex;
  align-items: center;
  gap: 8px;
  min-width: 90px;
}

.grade-badge {
  font-size: 11px;
  line-height: 18px;
  padding: 0 6px;
  border-radius: 9px;
  color: #909399;
  background: #f4f4f5;
}

.grade-badge.is-current {
  color: #fff;
  background: #409eff;
}
</style>
