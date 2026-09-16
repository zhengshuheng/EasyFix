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
        <el-menu-item index="/parent-center/incentive">
          <el-icon><Trophy /></el-icon><span>激励配置</span>
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
      <div class="pc-topbar">
        <span class="pc-topbar-title">{{ topbarTitle }}</span>
        <el-button type="primary" size="large" round @click="backToKid">
          <el-icon><Back /></el-icon>
          <span style="margin-left: 6px">返回学习空间</span>
        </el-button>
      </div>
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
    const subs = ['/parent-center/users', '/parent-center/management', '/parent-center/incentive', '/parent-center/settings']
    return subs.includes(p) ? p : '/parent-center/users'
  }
  return p
})

// 顶部返回条标题：跟随当前家长中心子页面
const topbarTitle = computed(() => {
  const p = route.path
  if (p.startsWith('/parent-center/management')) return '题库管理'
  if (p.startsWith('/parent-center/incentive')) return '激励配置'
  if (p.startsWith('/parent-center/settings')) return '系统配置'
  return '账号管理'
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

.pc-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  background: #fff;
  border-radius: 8px;
  padding: 10px 16px;
  margin-bottom: 16px;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.05);
}

.pc-topbar-title {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
}

.pc-content {
  padding: 20px;
  background: #f5f7fa;
}
</style>
