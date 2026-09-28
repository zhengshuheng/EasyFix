<template>
  <div class="select-kid">
    <div class="intro">
      <div class="hello-badge">✨ 开始今天的学习之旅</div>
      <h1><span class="wave">👋</span> 今天谁学习？</h1>
      <p>选择一个名字，进入 ta 的学习空间</p>
      <p v-if="ownerName" class="owner-name">🏠 欢迎来到 {{ ownerName }} 的家庭空间</p>

      <!-- 空间订阅状态条：正式版（含调试空间 easyfix_demo）不显示剩余天数 -->
      <div v-if="trialStore.is_pro" class="trial-status pro">✅ 正式版，不受体验期限制</div>
      <div v-else-if="trialStore.days_left !== null && !trialStore.expired" class="trial-status">
        ⏳ 免费体验剩余 {{ trialStore.days_left }} 天
      </div>
      <div v-else-if="trialStore.expired" class="trial-status expired">⚠️ 体验期已结束，请前往官网续费</div>
    </div>

    <div v-loading="loading" class="kid-grid">
      <div
        v-for="k in kids"
        :key="k.id"
        class="kid-card"
        :class="{ disabled: !k.enabled }"
        @click="enter(k)"
      >
        <div class="avatar" :style="{ background: avatarColor(k) }">
          {{ k.display_name?.slice(0, 1) || '?' }}
        </div>
        <div class="name">{{ k.display_name }}</div>
        <div v-if="k.current_grade" class="grade-badge">{{ gradeName(k.current_grade) }}</div>
      </div>

      <!-- 首次进入：还没有任何小孩时提供创建入口（宽松模式可直接创建） -->
      <div v-if="kids.length === 0" class="kid-card add-card" @click="openCreate">
        <div class="avatar add-avatar">＋</div>
        <div class="name">创建账号</div>
      </div>
    </div>

    <!-- 家长入口：卡片区下方居中的低调设置按钮（家长可见、小孩不抢眼） -->
    <div class="parent-entry">
      <el-tooltip content="管理小孩、题库、学习报告等" placement="top">
        <el-button class="parent-gear-btn" plain @click="parentLockVisible = true">
          <el-icon :size="15" style="margin-right: 4px; vertical-align: -2px;"><Setting /></el-icon>
          家长设置
        </el-button>
      </el-tooltip>
      <el-button class="guide-btn" text @click="guideVisible = true">
        <el-icon :size="14" style="margin-right: 4px; vertical-align: -2px;"><Reading /></el-icon>
        使用指南
      </el-button>
      <el-button class="logout-btn" text @click="logout">
        <el-icon :size="14" style="margin-right: 4px; vertical-align: -2px;"><SwitchButton /></el-icon>
        退出
      </el-button>
    </div>

    <!-- 创建小孩 -->
    <el-dialog v-model="createVisible" :title="kids.length ? '添加小孩' : '创建小孩账号'" width="380px">
      <el-form label-width="70px" @submit.prevent>
        <el-form-item label="名字">
          <el-input v-model="createForm.display_name" placeholder="怎么称呼你？" maxlength="20" autofocus />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="createVisible = false">取消</el-button>
        <el-button type="primary" :loading="creating" @click="handleCreate">开始学习</el-button>
      </template>
    </el-dialog>

    <!-- 家长中心（密码验证后进入管理） -->
    <ParentLockDialog v-model="parentLockVisible" @success="goParentCenter" />
    <!-- 使用指南 -->
    <UsageGuide v-model="guideVisible" />
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { usersApi } from '@/api/users'
import { useKidStore } from '@/stores/kid'
import { useSubjectStore } from '@/stores/subject'
import { useAuthStore } from '@/stores/auth'
import { useTrialStore } from '@/stores/trial'
import ParentLockDialog from '@/components/ParentLockDialog.vue'
import UsageGuide from '@/components/UsageGuide.vue'

const router = useRouter()
const kidStore = useKidStore()
const subjectStore = useSubjectStore()
const guideVisible = ref(false)
const authStore = useAuthStore()
const trialStore = useTrialStore()

// 家庭空间归属：官网账号用户名（优先实时查询 /api/trial/status；localStorage 兜底）
// 注意：dist-trial 空间内 401 处理会清除官网 easyfix_user，不能依赖它
const ownerName = ref('')
try {
  const saved = JSON.parse(localStorage.getItem('easyfix_user') || 'null')
  if (saved && saved.username) ownerName.value = saved.username
} catch { /* 忽略解析错误 */ }

async function loadOwnerName() {
  try {
    const key = localStorage.getItem('easyfix_trial_key')
    if (!key) return
    const res = await fetch('/api/trial/status', { headers: { 'X-Trial-Key': key } })
    if (res.ok) {
      const data = await res.json()
      if (data.space && data.space.username) ownerName.value = data.space.username
    }
  } catch { /* 查询失败保持 localStorage 兜底值 */ }
}

const kids = ref([])
const loading = ref(false)

const createVisible = ref(false)
const creating = ref(false)
const createForm = reactive({ display_name: '' })

// 年级文案：1~6 年级 / 初一~初三 / 高一~高三
function gradeName(g) {
  const n = Number(g) || 1
  if (n <= 6) return ['一', '二', '三', '四', '五', '六'][n - 1] + '年级'
  if (n <= 9) return '初一'.slice(0, 0) + '初' + ['一', '二', '三'][n - 7]
  return '高' + ['一', '二', '三'][n - 10]
}

const parentLockVisible = ref(false)

// 头像渐变配色（比纯色更活泼）
const AVATAR_GRADIENTS = [
  'linear-gradient(135deg, #667eea, #764ba2)',
  'linear-gradient(135deg, #f093fb, #f5576c)',
  'linear-gradient(135deg, #4facfe, #00f2fe)',
  'linear-gradient(135deg, #43e97b, #38f9d7)',
  'linear-gradient(135deg, #fa709a, #fee140)',
  'linear-gradient(135deg, #30cfd0, #330867)',
  'linear-gradient(135deg, #ff9a9e, #fad0c4)',
  'linear-gradient(135deg, #a18cd1, #fbc2eb)',
]

function avatarColor(k) {
  const seed = k.id || k.username?.length || 0
  return AVATAR_GRADIENTS[seed % AVATAR_GRADIENTS.length]
}

async function load() {
  loading.value = true
  try {
    const { data } = await usersApi.listKids()
    kids.value = (data.kids || []).filter((k) => k.enabled)
    // 首次使用引导：新注册空间（sessionStorage 标记）或空间还没有小孩且未完成/跳过引导 → 进入初始化引导
    // 完成标记按空间隔离（easyfix_onboarded_{key}），避免同浏览器多空间串扰
    const trialKey = localStorage.getItem('easyfix_trial_key') || ''
    const onboarded = localStorage.getItem('easyfix_onboarded_' + trialKey) === '1'
    const newSpace = sessionStorage.getItem('easyfix_new_space')
    if ((newSpace && !onboarded) || (kids.value.length === 0 && !onboarded)) {
      router.push('/onboarding')
      return
    }
  } catch (e) {
    ElMessage.error('加载失败，请确认服务已启动')
  } finally {
    loading.value = false
  }
}

function enter(kid) {
  kidStore.select(kid)
  // 点姓名自动进入当前阶段所属年级（由入学日期推断；未设置则默认一年级）
  subjectStore.select(null)
  subjectStore.applyKidDefaultGrade(kid)
  router.push('/home')
}

function openCreate() {
  createForm.display_name = ''
  createVisible.value = true
}

async function handleCreate() {
  const name = createForm.display_name.trim()
  if (!name) {
    ElMessage.warning('请输入名字')
    return
  }
  creating.value = true
  try {
    // 宽松模式（首次）无需家长登录即可创建第一个小孩
    const payload = {
      username: `kid_${Date.now()}`,
      role: 'child',
      display_name: name,
    }
    const { data } = await usersApi.create(payload)
    const newKid = data.user
    kidStore.select(newKid)
    // 新建小孩无入学日期 → 默认一年级
    subjectStore.select(null)
    subjectStore.applyKidDefaultGrade(newKid)
    ElMessage.success('创建成功，开始学习吧！')
    createVisible.value = false
    router.push('/home')
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '创建失败')
  } finally {
    creating.value = false
  }
}

function goParentCenter() {
  // 从选人页进入：记录返回选人页
  sessionStorage.setItem('easyfix_return_path', '/')
  router.push('/parent-center')
}

function logout() {
  authStore.logout()
  localStorage.removeItem('easyfix_trial_key')
  localStorage.removeItem('easyfix_kid')
  localStorage.removeItem('easyfix_account_token') // 官网账号 token 一并删除，否则官网面板残留"已登录"
  localStorage.removeItem('easyfix_user')
  // 退出登录 → 官网登录表单（浏览官网内容用顶部「官网」按钮）
  window.location.href = '/site/#trial?tab=login'
}

onMounted(() => {
  load()
  loadOwnerName()
  subjectStore.loadSubjects()
})
</script>

<style scoped>
.select-kid {
  max-width: 680px;
  margin: 0 auto;
  padding: 44px 16px 48px;
  text-align: center;
  min-height: 100vh;
  box-sizing: border-box;
  background:
    radial-gradient(1200px 500px at 15% -10%, rgba(102, 126, 234, 0.16), transparent 60%),
    radial-gradient(1000px 460px at 90% 0%, rgba(79, 172, 254, 0.14), transparent 55%),
    linear-gradient(180deg, #f6f9ff 0%, #eef4ff 100%);
}

.hello-badge {
  display: inline-block;
  font-size: 12px;
  letter-spacing: 1px;
  color: #667eea;
  background: rgba(102, 126, 234, 0.1);
  border: 1px solid rgba(102, 126, 234, 0.25);
  border-radius: 999px;
  padding: 4px 14px;
  margin-bottom: 14px;
}

.intro h1 {
  font-size: 34px;
  margin: 0 0 10px;
  letter-spacing: 0.5px;
}

.intro h1 .wave {
  display: inline-block;
  margin-right: 6px;
}

.intro p {
  color: #909399;
  margin: 0 0 30px;
  font-size: 15px;
}

.owner-name {
  display: inline-block;
  margin: -18px 0 26px;
  color: #667eea;
  background: rgba(102, 126, 234, 0.08);
  border: 1px solid rgba(102, 126, 234, 0.22);
  border-radius: 999px;
  padding: 5px 16px;
  font-size: 13px;
  font-weight: 600;
}

.trial-status {
  display: inline-block;
  margin: 0 0 26px;
  font-size: 13px;
  font-weight: 600;
  color: #b8821c;
  background: rgba(255, 193, 7, 0.1);
  border: 1px solid rgba(255, 193, 7, 0.3);
  border-radius: 999px;
  padding: 5px 16px;
}

.trial-status.pro {
  color: #27a05c;
  background: rgba(39, 160, 92, 0.08);
  border-color: rgba(39, 160, 92, 0.3);
}

.trial-status.expired {
  color: #e8566d;
  background: rgba(232, 86, 109, 0.08);
  border-color: rgba(232, 86, 109, 0.3);
}

.kid-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(118px, 1fr));
  gap: 20px;
  min-height: 60px;
}

.kid-card {
  cursor: pointer;
  padding: 22px 10px 18px;
  border-radius: 18px;
  background: #fff;
  box-shadow: 0 4px 14px rgba(36, 60, 120, 0.08);
  border: 1px solid rgba(255, 255, 255, 0.8);
  transition: all 0.28s ease;
}

.kid-card:hover {
  transform: translateY(-6px);
  box-shadow: 0 12px 30px rgba(64, 111, 222, 0.22);
  border-color: rgba(102, 126, 234, 0.35);
}

.kid-card.disabled {
  opacity: 0.45;
  pointer-events: none;
}

.avatar {
  width: 66px;
  height: 66px;
  margin: 0 auto 12px;
  border-radius: 50%;
  color: #fff;
  font-size: 28px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 6px 16px rgba(64, 111, 222, 0.28);
  transition: transform 0.28s ease;
}

.kid-card:hover .avatar {
  transform: scale(1.08) rotate(-4deg);
}

.kid-card .name {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
}

.kid-card .grade-badge {
  display: inline-block;
  margin-top: 6px;
  font-size: 12px;
  color: #409eff;
  background: #ecf5ff;
  padding: 2px 12px;
  border-radius: 12px;
}

.add-card {
  border: 2px dashed #c6cbe0;
  background: rgba(255, 255, 255, 0.6);
  box-shadow: none;
}

.add-card:hover {
  border-color: #667eea;
  box-shadow: 0 8px 24px rgba(102, 126, 234, 0.18);
}

.add-avatar {
  background: linear-gradient(135deg, #e4e7f0, #cfd6e8);
  color: #7a86a8;
  font-size: 32px;
  box-shadow: none;
}

.parent-entry {
  margin-top: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
}

/* 退出登录：低调灰字，位于家长设置旁 */
.logout-btn {
  color: #a0a8ba;
  font-size: 13px;
  padding: 8px 14px;
  border-radius: 999px;
}
.logout-btn:hover {
  color: #e11d48;
  background: rgba(225, 29, 72, 0.06);
}

/* 使用指南：与退出登录同色系低调按钮 */
.guide-btn {
  color: #8a94b5;
  font-size: 13px;
  padding: 8px 14px;
  border-radius: 999px;
}
.guide-btn:hover {
  color: #4f7df3;
  background: rgba(79, 125, 243, 0.08);
}

/* 家长设置按钮：低调灰色系（不抢小孩卡片风头），但位置明确家长一眼可见 */
.parent-gear-btn {
  color: #7a86a8;
  background: rgba(255, 255, 255, 0.7);
  border: 1px dashed #c6cbe0;
  border-radius: 999px;
  padding: 9px 22px;
  font-size: 14px;
  transition: all 0.25s ease;
}

.parent-gear-btn:hover {
  color: #409eff;
  background: #fff;
  border-color: #409eff;
  border-style: solid;
  box-shadow: 0 4px 14px rgba(64, 158, 255, 0.2);
}

.lock-tip {
  margin: 0 0 12px;
  color: #909399;
  font-size: 13px;
}
</style>
