<template>
  <el-container class="ops-layout">
    <el-aside width="220px" class="ops-aside">
      <div class="brand">🛠 运营后台</div>
      <el-menu :default-active="$route.path" router class="ops-menu" background-color="#1f2937" text-color="#cbd5e1" active-text-color="#fff">
        <el-sub-menu index="data">
          <template #title>📚 教材数据</template>
          <el-menu-item index="/kp">▸ 知识点管理</el-menu-item>
          <el-menu-item index="/word">▸ 英语单词管理</el-menu-item>
          <el-menu-item index="/editions">▸ 教材版本</el-menu-item>
        </el-sub-menu>
        <el-sub-menu index="sys">
          <template #title>⚙️ 系统配置</template>
          <el-menu-item index="/config">▸ 系统设置</el-menu-item>
          <el-menu-item index="/ai-market">▸ AI 模型市场</el-menu-item>
          <el-menu-item index="/prompt-rules">▸ 出题规则</el-menu-item>
          <el-menu-item index="/assess-rules">▸ 评测规则</el-menu-item>
          <el-menu-item index="/incentive-rules">▸ 激励规则</el-menu-item>
          <el-menu-item index="/grammar-tutorials">▸ 语法教程</el-menu-item>
          <el-menu-item index="/trial-accounts">▸ 体验账号管理</el-menu-item>
        </el-sub-menu>
      </el-menu>
      <div class="ops-footer">
        <el-button text style="color:#f87171;" @click="logout">↩ 退出登录</el-button>
      </div>
    </el-aside>
    <el-main class="ops-main">
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useSession } from '../stores/session.js'

const router = useRouter()
const session = useSession()

function logout() {
  session.logout()
  router.push('/')
}
</script>

<style scoped>
.ops-layout {
  min-height: 100vh;
}
.ops-aside {
  background: #1f2937;
  display: flex;
  flex-direction: column;
  position: sticky;
  top: 0;
  height: 100vh;
  overflow-y: auto;
}
.brand {
  color: #f9fafb;
  font-size: 15px;
  font-weight: 700;
  padding: 16px 18px 14px;
  border-bottom: 1px solid #374151;
}
.ops-menu {
  border-right: none;
  flex: 1;
}
.ops-menu :deep(.el-sub-menu__title) {
  color: #e5e7eb;
  font-weight: 600;
}
.ops-menu :deep(.el-menu-item.is-active) {
  background: #2563eb;
}
.ops-menu :deep(.el-menu-item:hover),
.ops-menu :deep(.el-sub-menu__title:hover) {
  background: #374151;
}
.ops-footer {
  padding: 12px 16px;
  border-top: 1px solid #374151;
}
.ops-main {
  background: #f5f7fa;
  padding: 24px;
}
</style>
