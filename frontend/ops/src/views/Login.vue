<template>
  <div class="login-wrap">
    <el-card class="login-card" shadow="always">
      <h1>🛠 运营后台</h1>
      <p class="sub">运营管理后台 · 授权访问</p>
      <el-form label-position="top" @submit.prevent="doLogin">
        <el-form-item label="运营账号">
          <el-input v-model="username" placeholder="输入运营账号" autocomplete="username" />
        </el-form-item>
        <el-form-item label="运营口令">
          <el-input v-model="password" type="password" placeholder="输入运营口令" show-password autocomplete="current-password" @keyup.enter="doLogin" />
        </el-form-item>
        <el-button type="primary" class="w-full" :loading="loading" @click="doLogin">进入后台 →</el-button>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'
import { useSession } from '../stores/session.js'

const router = useRouter()
const session = useSession()
const username = ref('')
const password = ref('')
const loading = ref(false)

async function doLogin() {
  if (!username.value.trim() || !password.value.trim()) {
    ElMessage.warning('请输入运营账号与口令')
    return
  }
  loading.value = true
  try {
    await axios.get('/api/ops/config', {
      headers: { 'X-Ops-Username': username.value.trim(), 'X-Ops-Password': password.value.trim() },
    })
    session.login(username.value.trim(), password.value.trim())
    router.push('/kp')
  } catch (e) {
    ElMessage.error('账号或口令错误，无法进入')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-wrap {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #f5f7fa;
}
.login-card {
  width: 420px;
  padding: 8px 16px;
}
.login-card h1 { font-size: 22px; margin: 4px 0; }
.login-card .sub { color: #6b7280; font-size: 14px; margin: 0 0 20px; }
.w-full { width: 100%; }
</style>
