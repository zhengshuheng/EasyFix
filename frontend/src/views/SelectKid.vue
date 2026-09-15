<template>
  <div class="select-kid">
    <div class="intro">
      <h1>👋 今天谁学习？</h1>
      <p>选择你的名字开始吧</p>
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
      需要添加更多小孩？请在「🔒 家长中心」中管理
    </p>

    <div class="parent-entry">
      <el-button link type="primary" @click="parentLockVisible = true">
        🔒 家长中心
      </el-button>
    </div>

    <!-- 创建小孩 -->
    <el-dialog v-model="createVisible" :title="kids.length ? '添加小孩' : '创建小孩账号'" width="380px">
      <el-form label-width="70px" @submit.prevent>
        <el-form-item label="名字">
          <el-input v-model="createForm.display_name" placeholder="怎么称呼你？" maxlength="20" autofocus />
        </el-form-item>
        <el-form-item label="PIN 码">
          <el-input
            v-model="createForm.pin"
            placeholder="4 位数字（可留空）"
            maxlength="4"
            inputmode="numeric"
          />
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
import ParentLockDialog from '@/components/ParentLockDialog.vue'

const router = useRouter()
const kidStore = useKidStore()

const kids = ref([])
const loading = ref(false)

const createVisible = ref(false)
const creating = ref(false)
const createForm = reactive({ display_name: '', pin: '' })

const parentLockVisible = ref(false)

const AVATAR_COLORS = ['#409eff', '#67c23a', '#e6a23c', '#f56c6c', '#9b59b6', '#00b5ad']

function avatarColor(k) {
  const seed = k.id || k.username?.length || 0
  return AVATAR_COLORS[seed % AVATAR_COLORS.length]
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
  router.push('/home')
}

function openCreate() {
  createForm.display_name = ''
  createForm.pin = ''
  createVisible.value = true
}

async function handleCreate() {
  const name = createForm.display_name.trim()
  if (!name) {
    ElMessage.warning('请输入名字')
    return
  }
  if (createForm.pin && !/^\d{4}$/.test(createForm.pin)) {
    ElMessage.warning('PIN 码必须是 4 位数字，或留空')
    return
  }
  creating.value = true
  try {
    // 宽松模式（首次）无需家长登录即可创建第一个小孩
    const payload = {
      username: `kid_${Date.now()}`,
      role: 'child',
      display_name: name,
      pin: createForm.pin || undefined,
    }
    const { data } = await usersApi.create(payload)
    const newKid = data.user
    kidStore.select(newKid)
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
  router.push('/parent-center')
}

onMounted(load)
</script>

<style scoped>
.select-kid {
  max-width: 640px;
  margin: 0 auto;
  padding: 40px 16px;
  text-align: center;
}

.intro h1 {
  font-size: 30px;
  margin: 0 0 8px;
}

.intro p {
  color: #909399;
  margin: 0 0 32px;
}

.kid-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
  gap: 18px;
  min-height: 60px;
}

.kid-card {
  cursor: pointer;
  padding: 20px 10px;
  border-radius: 16px;
  background: #fff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.06);
  transition: all 0.25s ease;
}

.kid-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 6px 18px rgba(64, 158, 255, 0.25);
}

.kid-card.disabled {
  opacity: 0.45;
  pointer-events: none;
}

.avatar {
  width: 64px;
  height: 64px;
  margin: 0 auto 10px;
  border-radius: 50%;
  color: #fff;
  font-size: 28px;
  font-weight: bold;
  display: flex;
  align-items: center;
  justify-content: center;
}

.add-card {
  border: 2px dashed #c0c4cc;
  background: transparent;
  box-shadow: none;
}

.add-card:hover {
  border-color: #409eff;
}

.add-avatar {
  background: #e4e7ed;
  color: #909399;
  font-size: 30px;
}

.parent-entry {
  margin-top: 36px;
}

.add-hint {
  margin-top: 24px;
  color: #909399;
  font-size: 13px;
}

.lock-tip {
  margin: 0 0 12px;
  color: #909399;
  font-size: 13px;
}
</style>
