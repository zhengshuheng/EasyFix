<template>
  <el-container class="parent-center">
    <el-aside width="190px" class="pc-aside">
      <div class="pc-title">🔒 家长中心</div>
      <el-menu :router="true" :default-active="activeMenu" class="pc-menu">
        <el-menu-item index="/parent-center/users">
          <el-icon><User /></el-icon><span>账号管理</span>
        </el-menu-item>
        <el-menu-item index="/parent-center/management">
          <el-icon><Collection /></el-icon><span>题库管理</span>
        </el-menu-item>
        <el-menu-item index="/parent-center/settings">
          <el-icon><Setting /></el-icon><span>系统配置</span>
        </el-menu-item>
      </el-menu>
      <div class="pc-footer">
        <el-button size="small" plain @click="backToKid">← 返回小孩端</el-button>
      </div>
    </el-aside>

    <el-main class="pc-content">
      <router-view />
    </el-main>
  </el-container>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useKidStore } from '@/stores/kid'

const route = useRoute()
const router = useRouter()
const kidStore = useKidStore()

// 左侧菜单高亮：子路由精确匹配，其余家长中心路径回落到账号管理
const activeMenu = computed(() => {
  const p = route.path
  if (p.startsWith('/parent-center')) {
    const subs = ['/parent-center/users', '/parent-center/management', '/parent-center/settings']
    return subs.includes(p) ? p : '/parent-center/users'
  }
  return p
})

function backToKid() {
  // 退出家长会话，回到小孩端（保留当前小孩身份）
  localStorage.removeItem('easyfix_token')
  localStorage.removeItem('easyfix_user')
  if (kidStore.isKidSelected) {
    router.push('/home')
  } else {
    router.push('/')
  }
}
</script>

<style scoped>
.parent-center {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.06);
  overflow: hidden;
  min-height: calc(100vh - 100px);
}

.pc-aside {
  background: #f8fafc;
  border-right: 1px solid #eef0f4;
  padding: 0;
  display: flex;
  flex-direction: column;
}

.pc-title {
  padding: 20px 18px 12px;
  font-size: 17px;
  font-weight: bold;
  color: #303133;
}

.pc-menu {
  border-right: none;
  flex: 1;
}

.pc-menu .el-menu-item {
  height: 46px;
  line-height: 46px;
}

.pc-menu .el-menu-item.is-active {
  background: #ecf5ff;
  border-right: 3px solid #409eff;
  font-weight: bold;
}

.pc-footer {
  padding: 14px;
  text-align: center;
}

.pc-content {
  padding: 20px;
  background: #f5f7fa;
}
</style>
