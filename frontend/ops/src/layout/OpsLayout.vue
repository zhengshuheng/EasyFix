<template>
  <el-container class="ops-layout">
    <el-aside width="220px" class="ops-aside">
      <div class="brand">🛠 运营后台</div>
      <el-menu :default-active="$route.path" router class="ops-menu" :mode="isMobile ? 'horizontal' : 'vertical'" background-color="#1f2937" text-color="#cbd5e1" active-text-color="#fff">
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
import { ref, onMounted, onUnmounted } from 'vue'
import { useRouter } from 'vue-router'
import { useSession } from '../stores/session.js'

const router = useRouter()
const session = useSession()

// 移动端断点（≤768px）：左侧导航转顶部横滑菜单，右侧内容占满整宽
// （桌面 220px 固定侧栏在竖屏占半屏以上，右侧内容被压到无法操作）
const isMobile = ref(window.matchMedia('(max-width: 768px)').matches)
const mobileMq = window.matchMedia('(max-width: 768px)')
const syncMobile = (e) => { isMobile.value = e.matches }
onMounted(() => mobileMq.addEventListener('change', syncMobile))
onUnmounted(() => mobileMq.removeEventListener('change', syncMobile))

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

/* ===== 移动端（≤768px）：左侧导航转顶部横滑菜单 =====
 * 桌面 220px 固定侧栏在竖屏占半屏以上，右侧内容被压到 ~155px 无法操作；
 * 移动端改 column：aside 变顶部一行（brand + 菜单横滑 + 退出按钮），
 * main 占满整宽；菜单用 el-menu horizontal 模式（sub-menu 弹层不占布局）。 */
@media screen and (max-width: 768px) {
  .ops-layout {
    flex-direction: column;
  }
  .ops-aside {
    position: static;
    width: 100% !important;
    height: auto;
    max-height: none;
    flex-direction: row;
    flex-wrap: wrap;
    align-items: center;
    overflow: visible;
    border-bottom: 1px solid #374151;
  }
  .brand {
    padding: 10px 12px;
    font-size: 14px;
    border-bottom: none;
    flex: 0 0 auto;
  }
  .ops-menu {
    flex: 1 1 auto;
    min-width: 0;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
  }
  .ops-menu :deep(.el-menu--horizontal) {
    display: inline-flex;
    flex-wrap: nowrap;
  }
  .ops-menu :deep(.el-menu--horizontal > .el-sub-menu),
  .ops-menu :deep(.el-menu--horizontal > .el-menu-item) {
    flex: 0 0 auto;
  }
  .ops-footer {
    padding: 8px 12px;
    border-top: none;
    border-left: 1px solid #374151;
    flex: 0 0 auto;
  }
  .ops-main {
    padding: 12px;
    min-height: 0;
  }
}
</style>

<style>
/* 运营后台全局移动端兜底（非 scoped：覆盖挂载在 body 的 el-dialog / 表格内部类） */
@media screen and (max-width: 768px) {
  .login-card {
    width: calc(100vw - 24px) !important;
    max-width: 100%;
  }
  .el-dialog {
    width: calc(100vw - 24px) !important;
    max-width: 100%;
  }
  .ops-main .el-table__inner-wrapper,
  .ops-main .el-table__body-wrapper,
  .ops-main .el-table__header-wrapper {
    max-width: 100%;
    overflow-x: auto;
  }
  .ops-main .el-form-item {
    display: block;
    margin-right: 0;
  }
  .ops-main .el-form-item__label {
    float: none;
    text-align: left;
    padding: 0 0 6px;
    line-height: 1.4;
    width: auto !important;
  }
}
</style>
