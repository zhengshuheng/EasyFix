<template>
  <div class="login-page">
    <div class="login-card">
      <div class="logo-badge">🏠</div>
      <h1>家长登录</h1>
      <p class="sub">登录后可进入学习空间管理</p>

      <el-form label-position="top" @submit.prevent>
        <el-form-item label="用户名">
          <el-input v-model="form.username" placeholder="请输入家长用户名" size="large" autofocus @keyup.enter="submit" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input
            v-model="form.password"
            type="password"
            placeholder="请输入密码"
            size="large"
            show-password
            @keyup.enter="submit"
          />
        </el-form-item>
      </el-form>

      <el-button class="login-btn" type="primary" size="large" :loading="loading" @click="submit">
        登 录
      </el-button>

      <p class="hint">主账号（官网注册）或辅账号（家长添加）均可登录；忘记密码请联系管理员重置</p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useAuthStore } from '@/stores/auth'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()

const form = reactive({ username: '', password: '' })
const loading = ref(false)

async function submit() {
  const username = form.username.trim()
  const password = form.password
  if (!username || !password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }
  loading.value = true
  try {
    await authStore.login({ username, password })
    // 登录成功：回跳原目标页（守卫带 redirect），默认选人页
    const redirect = Array.isArray(route.query.redirect) ? route.query.redirect[0] : route.query.redirect
    router.replace(redirect || '/')
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '登录失败，请重试')
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
  padding: 24px;
  box-sizing: border-box;
  background:
    radial-gradient(1200px 500px at 15% -10%, rgba(102, 126, 234, 0.18), transparent 60%),
    radial-gradient(1000px 460px at 90% 0%, rgba(79, 172, 254, 0.16), transparent 55%),
    linear-gradient(180deg, #f6f9ff 0%, #eef4ff 100%);
}

.login-card {
  width: 380px;
  max-width: 100%;
  background: #fff;
  border-radius: 20px;
  padding: 36px 32px 30px;
  box-shadow: 0 12px 40px rgba(36, 60, 120, 0.14);
  text-align: center;
}

.logo-badge {
  width: 56px;
  height: 56px;
  margin: 0 auto 14px;
  border-radius: 50%;
  font-size: 28px;
  line-height: 56px;
  background: linear-gradient(135deg, #667eea, #764ba2);
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.35);
}

.login-card h1 {
  font-size: 22px;
  margin: 0 0 6px;
  color: #303133;
}

.login-card .sub {
  color: #909399;
  font-size: 13px;
  margin: 0 0 24px;
}

.login-btn {
  width: 100%;
  margin-top: 4px;
  border-radius: 12px;
  font-weight: 600;
}

.hint {
  margin-top: 18px;
  font-size: 12px;
  color: #b0b6c4;
}
</style>
