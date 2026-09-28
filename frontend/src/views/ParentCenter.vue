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
const topbarTitle = computed(() => {
  const p = route.path
  if (p.startsWith('/parent-center/management')) return '题库管理'
  if (p.startsWith('/parent-center/incentive')) return '激励配置'
  if (p.startsWith('/parent-center/settings')) return '系统配置'
  return '账号管理'
})

function backToKid() {
  // 返回学生空间：保留登录态（路由登录墙要求空间内始终存在 easyfix_token，
  // 清 token 会被踢到 #/login?redirect=...）。只切回小孩视角；真正退出登录
  // 在选人页「退出登录」按钮（清 token 并回官网）。
  const ret = sessionStorage.getItem('easyfix_return_path')
  sessionStorage.removeItem('easyfix_return_path')
  if (ret) {
    router.push(ret)
  } else if (kidStore.isKidSelected) {
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

/* 移动端适配：竖屏窄屏下左侧导航改为顶部横排菜单，内容区占满宽度 */
@media (max-width: 768px) {
  .parent-center {
    flex-direction: column;
    min-height: auto;
  }

  .pc-aside {
    width: 100% !important;
    border-right: none;
    border-bottom: 1px solid #eef0f4;
    flex-direction: row;
    align-items: center;
    flex-wrap: wrap;
  }

  .pc-title {
    padding: 8px 12px;
    font-size: 14px;
  }

  .pc-menu {
    flex: 1;
    min-width: 0;
    display: flex;
    flex-direction: row;
  }

  .pc-menu :deep(.el-menu-item) {
    flex: 1 1 0;
    justify-content: center;
    padding: 0 4px !important;
    height: 42px;
    line-height: 42px;
  }

  .pc-menu :deep(.el-menu-item.is-active) {
    border-right: none;
    border-bottom: 3px solid #409eff;
    background: transparent;
  }

  .pc-menu :deep(.el-menu-item .el-icon) {
    margin-right: 4px;
  }

  .pc-footer {
    display: none;
  }

  .pc-content {
    padding: 10px;
  }

  .pc-topbar {
    padding: 8px 10px;
    margin-bottom: 10px;
  }

  .pc-topbar-title {
    font-size: 14px;
  }

  .pc-topbar .el-button {
    padding: 6px 12px;
  }
}

/* ==================== 移动端（≤768px）：左侧导航转顶部横条 ====================
 * 桌面 190px 固定侧栏在竖屏占半屏；移动端改为：顶部一行（标题 + 横向可滑菜单），
 * 内容区占满剩余高度。菜单项用 CSS 把 el-menu 的 vertical（column）改成 row 横排，
 * 不依赖 el-menu 的 horizontal 渲染模式，避免动模板结构。 */
@media screen and (max-width: 768px) {
  .parent-center {
    flex-direction: column;
    min-height: calc(100vh - 80px);
  }

  .pc-aside {
    width: 100% !important; /* 覆盖 el-aside 内联 width="190px" */
    flex-direction: row;
    align-items: center;
    border-right: none;
    border-bottom: 1px solid #eef0f4;
    padding: 0;
    flex: 0 0 auto;
  }

  .pc-title {
    padding: 10px 10px;
    font-size: 14px;
    white-space: nowrap;
  }

  /* el-menu 默认 vertical 是 flex column → 改为 row 横排 + 横向可滑 */
  .pc-menu {
    flex-direction: row;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    flex: 1;
    border-bottom: none;
  }

  .pc-menu .el-menu-item {
    height: 42px;
    line-height: 42px;
    flex: 0 0 auto;
    padding: 0 12px;
    white-space: nowrap;
    width: auto !important; /* 覆盖 el-menu--vertical 对 item 的 width:100% */
  }

  .pc-menu .el-menu-item.is-active {
    border-right: none;
    border-bottom: 3px solid #409eff;
  }

  /* 桌面版底部「返回小孩端」由顶栏「返回学习空间」按钮承担，移动端隐藏避免重复 */
  .pc-footer {
    display: none;
  }

  .pc-content {
    padding: 12px;
    flex: 1;
    min-height: 0;
  }

  .pc-topbar {
    padding: 8px 12px;
    margin-bottom: 10px;
  }

  .pc-topbar-title {
    font-size: 14px;
  }
}
</style>
