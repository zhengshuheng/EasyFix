<template>
  <el-dialog v-model="innerVisible" :title="title" width="360px" :close-on-click-modal="false">
    <p class="lock-tip">{{ tip }}</p>
    <el-input
      v-model="password"
      type="password"
      placeholder="家长密码"
      show-password
      autofocus
      @keyup.enter="unlock"
    />
    <template #footer>
      <el-button @click="innerVisible = false">取消</el-button>
      <el-button type="primary" :loading="loading" @click="unlock">{{ confirmText }}</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  modelValue: { type: Boolean, default: false },
  /** 弹窗标题（默认：家长中心） */
  title: { type: String, default: '家长中心' },
  /** 提示文案（默认：请输入家长密码以进入管理） */
  tip: { type: String, default: '请输入家长密码以进入管理' },
  /** 确认按钮文案（默认：进入） */
  confirmText: { type: String, default: '进入' },
})
const emit = defineEmits(['update:modelValue', 'success'])

const authStore = useAuthStore()
const innerVisible = computed({
  get: () => props.modelValue,
  set: (v) => emit('update:modelValue', v),
})

const password = ref('')
const loading = ref(false)

watch(
  () => props.modelValue,
  (v) => {
    if (v) password.value = ''
  }
)

async function unlock() {
  if (!password.value) {
    ElMessage.warning('请输入家长密码')
    return
  }
  loading.value = true
  try {
    // 家长中心验证：密码校验对象 = 空间内的家长账号，候选按以下优先级收集，
    // 逐个尝试——任一候选账号密码匹配即通过（避免 registry username 与空间 User
    // 不一致、或会话账号密码与默认家长密码不同时被卡死）：
    // 1) 当前会话账号（token 解出；家长会话直接用它）
    // 2) registry 空间主账号（/api/trial/status space.username；学生(child)会话用它）
    // 3) admin 兜底（旧空间默认家长）
    const candidates = []
    const token = localStorage.getItem('easyfix_token')
    // 当前空间 key：URL /{key}/ 优先（空间 SPA 部署路径即真相）；localStorage 全局共享，
    // 可能残留别的空间 key 或缺失（官网跳转前瞬间），仅作兜底。
    const trialKey =
      (window.location.pathname.match(/^\/([^/]+)\//) || [])[1] ||
      localStorage.getItem('easyfix_trial_key') ||
      ''
    try {
      // 原生 fetch 必须带 X-Trial-Key：不带则租户中间件不切库，/api/auth/me 会落到
      // 主库，主库 User.id 与租户库错位（主库同 id 可能是 child）→ 当前会话账号候选
      // 丢失 → 辅助账号输对密码也会因候选错位全败，密码锁卡死（9/28 回归根因）。
      const headers = token ? { Authorization: `Bearer ${token}` } : {}
      if (trialKey) headers['X-Trial-Key'] = trialKey
      const meRes = await fetch('/api/auth/me', { headers })
      if (meRes.ok) {
        const me = await meRes.json()
        if (me && me.role === 'admin' && me.username && !candidates.includes(me.username)) {
          candidates.push(me.username)
        }
      }
    } catch { /* 忽略，走下一优先级 */ }
    try {
      if (trialKey) {
        const res = await fetch('/api/trial/status', { headers: { 'X-Trial-Key': trialKey } })
        if (res.ok) {
          const data = await res.json()
          if (data.space && data.space.username && !candidates.includes(data.space.username)) {
            candidates.push(data.space.username)
          }
        }
      }
    } catch { /* 忽略，保持兜底值 */ }
    if (!candidates.includes('admin')) candidates.push('admin')
    let lastErr = null
    for (const username of candidates) {
      try {
        await authStore.login({ username, password: password.value })
        innerVisible.value = false
        ElMessage.success('家长验证通过')
        emit('success')
        return
      } catch (e) {
        lastErr = e
      }
    }
    ElMessage.error(lastErr?.response?.data?.detail || '密码错误')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.lock-tip {
  margin: 0 0 12px;
  color: #909399;
  font-size: 13px;
}
</style>
