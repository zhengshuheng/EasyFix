<template>
  <div class="login-page">
    <el-card class="login-card">
      <template #header>
        <div class="login-header">
          <h1>EasyFix</h1>
          <p>错题整理与学习系统</p>
        </div>
      </template>

      <el-tabs v-model="activeRole" class="role-tabs">
        <el-tab-pane label="家长" name="admin" />
        <el-tab-pane label="小孩" name="child" />
      </el-tabs>

      <el-form @submit.prevent="handleLogin" label-position="top">
        <el-form-item label="用户名">
          <el-input
            v-model="form.username"
            placeholder="请输入用户名"
            size="large"
            autocomplete="username"
          />
        </el-form-item>

        <el-form-item v-if="activeRole === 'admin'" label="密码">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            size="large"
            show-password
            autocomplete="current-password"
            @keyup.enter="handleLogin"
          />
        </el-form-item>

        <el-form-item v-else label="PIN 码（4 位数字）">
          <el-input
            v-model="form.pin"
            placeholder="请输入 4 位 PIN 码"
            size="large"
            maxlength="4"
            inputmode="numeric"
            @keyup.enter="handleLogin"
          />
        </el-form-item>

        <el-button
          type="primary"
          size="large"
          class="login-btn"
          :loading="loading"
          native-type="submit"
        >
          登 录
        </el-button>
      </el-form>

      <div v-if="activeRole === 'admin'" class="login-tip">
        首次使用默认账号：admin / 32167
      </div>
    </el-card>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

const activeRole = ref('admin')
const loading = ref(false)
const form = reactive({
  username: '',
  password: '',
  pin: '',
})

async function handleLogin() {
  if (!form.username.trim()) {
    ElMessage.warning('请输入用户名')
    return
  }
  if (activeRole.value === 'admin' && !form.password) {
    ElMessage.warning('请输入密码')
    return
  }
  if (activeRole.value === 'child' && !/^\d{4}$/.test(form.pin || '')) {
    ElMessage.warning('PIN 码必须是 4 位数字')
    return
  }

  loading.value = true
  try {
    const payload =
      activeRole.value === 'admin'
        ? { username: form.username.trim(), password: form.password }
        : { username: form.username.trim(), pin: form.pin }
    const data = await authStore.login(payload)
    ElMessage.success(data.role === 'admin' ? '家长登录成功' : '登录成功，欢迎回来')
    router.push('/')
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '登录失败，请检查账号信息')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #409eff 0%, #6f8bff 100%);
  padding: 20px;
}

.login-card {
  width: 380px;
  max-width: 100%;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0, 0, 0, 0.2);
}

.login-header {
  text-align: center;
}

.login-header h1 {
  margin: 0;
  font-size: 26px;
  color: #409eff;
}

.login-header p {
  margin: 6px 0 0;
  color: #909399;
  font-size: 13px;
}

.role-tabs {
  margin-bottom: 8px;
}

.login-btn {
  width: 100%;
  margin-top: 8px;
}

.login-tip {
  margin-top: 14px;
  font-size: 12px;
  color: #909399;
  text-align: center;
}
</style>
