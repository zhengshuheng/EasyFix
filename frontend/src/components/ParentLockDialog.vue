<template>
  <el-dialog v-model="innerVisible" title="家长中心" width="360px" :close-on-click-modal="false">
    <p class="lock-tip">请输入家长密码以进入管理</p>
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
      <el-button type="primary" :loading="loading" @click="unlock">进入</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  modelValue: { type: Boolean, default: false },
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
    // 家长中心验证即登录默认家长账号，token 供管理接口使用
    await authStore.login({ username: 'admin', password: password.value })
    innerVisible.value = false
    ElMessage.success('家长验证通过')
    emit('success')
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '密码错误')
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
