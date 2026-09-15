<template>
  <div class="select-kid">
    <div class="intro">
      <div class="hello-badge">✨ 开始今天的学习之旅</div>
      <h1><span class="wave">👋</span> 今天谁学习？</h1>
      <p>选择一个名字，进入 ta 的学习空间</p>
    </div>

    <!-- 空间预选：进入前选定学科/年级，点击小孩即直达指定学科空间 -->
    <div class="space-pick">
      <div class="pick-title">🎯 快速进入指定空间</div>
      <div class="pick-row">
        <span class="pick-label"><el-icon class="pick-icon"><Collection /></el-icon>学科</span>
        <el-select v-model="pickSubjectId" placeholder="全部学科" clearable style="width: 170px">
          <el-option label="全部学科" value="" />
          <el-option v-for="s in subjectStore.subjects" :key="s.id" :label="s.name" :value="String(s.id)" />
        </el-select>
        <span class="pick-label"><el-icon class="pick-icon"><Histogram /></el-icon>年级</span>
        <el-select v-model="pickGrade" placeholder="全部年级" clearable style="width: 150px">
          <el-option label="全部年级" value="" />
          <el-option v-for="g in gradeOptions" :key="g.value" :label="g.label" :value="String(g.value)" />
        </el-select>
      </div>
      <div class="pick-tip">选择后点小孩直接进入对应空间（默认全部学科 / 全部年级）</div>
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
      </div>

      <!-- 首次进入：还没有任何小孩时提供创建入口（宽松模式可直接创建） -->
      <div v-if="kids.length === 0" class="kid-card add-card" @click="openCreate">
        <div class="avatar add-avatar">＋</div>
        <div class="name">创建账号</div>
      </div>
    </div>

    <p v-if="kids.length > 0" class="add-hint">
      ✏️ 需要添加更多小孩？请在「🔒 家长中心」中管理
    </p>

    <div class="parent-entry">
      <el-button link type="primary" class="parent-btn" @click="parentLockVisible = true">
        🔒 家长中心
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
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { usersApi } from '@/api/users'
import { useKidStore } from '@/stores/kid'
import { useSubjectStore } from '@/stores/subject'
import ParentLockDialog from '@/components/ParentLockDialog.vue'

const router = useRouter()
const kidStore = useKidStore()
const subjectStore = useSubjectStore()

const kids = ref([])
const loading = ref(false)

const createVisible = ref(false)
const creating = ref(false)
const createForm = reactive({ display_name: '' })

const parentLockVisible = ref(false)

// 空间预选（'' = 全部学科 / 全部年级）
const pickSubjectId = ref('')
const pickGrade = ref('')

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

function applySpace() {
  subjectStore.select(pickSubjectId.value === '' ? null : Number(pickSubjectId.value))
  subjectStore.setGrade(pickGrade.value === '' ? null : Number(pickGrade.value))
}

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
  } catch (e) {
    ElMessage.error('加载失败，请确认服务已启动')
  } finally {
    loading.value = false
  }
}

function enter(kid) {
  kidStore.select(kid)
  applySpace()
  // 选了具体学科 → 直达学科空间（tab）；全部学科 → 首页概览
  if (subjectStore.activeSubjectId !== null) {
    router.push('/space/' + subjectStore.activeSubjectId)
  } else {
    router.push('/home')
  }
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
    applySpace()
    ElMessage.success('创建成功，开始学习吧！')
    createVisible.value = false
    if (subjectStore.activeSubjectId !== null) {
      router.push('/space/' + subjectStore.activeSubjectId)
    } else {
      router.push('/home')
    }
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '创建失败')
  } finally {
    creating.value = false
  }
}

function goParentCenter() {
  router.push('/parent-center')
}

onMounted(() => {
  load()
  subjectStore.loadSubjects()
  // 预选值默认 = 当前空间（保留上次选择）
  pickSubjectId.value = subjectStore.activeSubjectId !== null ? String(subjectStore.activeSubjectId) : ''
  pickGrade.value = subjectStore.activeGrade !== null ? String(subjectStore.activeGrade) : ''
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

.space-pick {
  display: inline-flex;
  flex-direction: column;
  align-items: center;
  gap: 12px;
  margin-bottom: 30px;
  padding: 16px 26px 14px;
  border-radius: 18px;
  background: rgba(255, 255, 255, 0.86);
  box-shadow: 0 8px 28px rgba(64, 111, 222, 0.12);
  backdrop-filter: blur(6px);
}

.pick-title {
  font-size: 14px;
  font-weight: 600;
  color: #4a5c8a;
}

.pick-row {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  justify-content: center;
}

.pick-label {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 14px;
  color: #606266;
  font-weight: 500;
}

.pick-icon {
  color: #667eea;
}

.pick-tip {
  font-size: 12px;
  color: #a0a8bf;
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
  margin-top: 40px;
}

.parent-btn {
  font-size: 14px;
  padding: 8px 18px;
  border-radius: 999px;
  background: rgba(255, 255, 255, 0.7);
  box-shadow: 0 2px 10px rgba(36, 60, 120, 0.08);
}

.add-hint {
  margin-top: 26px;
  color: #909399;
  font-size: 13px;
}

.lock-tip {
  margin: 0 0 12px;
  color: #909399;
  font-size: 13px;
}
</style>
