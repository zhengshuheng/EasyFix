# PARENT_OWNER_DELETE — 家长中心账号管理：仅主账号可删除

**日期**：2026-09-28
**需求**：家长中心·账号管理优化——只有主账号（`users.is_owner`）允许删除其他账号，辅助家长账号不允许删除小孩和账号。

## 改动

### 后端（backend/app/routers/users.py）
- `delete_user` 新增**主账号校验**：`if not admin.is_owner: raise 403「仅主账号可删除账号/小孩，辅助家长无删除权限」`
  - 原有保护保留：不能删自己（400）、不能删最后一个家长（400）、主账号目标不可删（400/403）
  - `require_admin` 仍只校验 role=admin，删除权限收口到 is_owner 一个开关

### 前端（frontend/src/views/UserManage.vue）
- 删除按钮改为 `v-if="authStore.user?.is_owner"`：**辅助家长视角完全不显示删除按钮**（用户第二轮要求"连删除按钮都不需要显示"，先实现为 disabled，后调整为隐藏）；主账号视角显示，主账号行仍 disabled（不可删自己/主账号）
- `onMounted` 增加 `authStore.refreshMe()`：旧登录态 localStorage 可能缺 `is_owner` 字段，刷新保证判断准确（失败静默）

## 验证（全部通过）

1. **单元冒烟**（直接调 delete_user 函数，7/7）：
   - 辅助家长删小孩/删家长/删主账号 → 403
   - 主账号删小孩/删辅助家长 → 200
   - 主账号删自己 → 400
2. **HTTP 端到端**（8012 起服务 + 隔离测试空间 test_owner_del_e2e，4/4）：
   - 辅助家长 `DELETE /api/users/{kid}` → 403；删主账号 → 403
   - 主账号删小孩/删辅助家长 → 200
   - 辅助家长被删后其 token 立即 401（既有行为：删除家长后 token 失效）
3. **浏览器 UI**（Browser SDK，隔离空间）：
   - 辅助家长登录：删除按钮**完全不显示**（count=0，行内只剩 编辑/改密码）
   - 主账号登录：删除按钮显示 3 个；主账号行 disabled，小孩行/辅助家长行可用

## 测试方法备忘

- 隔离空间 = 复制 `trial_data/tenants/easyfix_demo.db` → 新 key db（改主账号密码 + SQL 直插辅助家长，**不建主库 Account** 避免残留）+ registry 手动注册行
- 坑：**服务进程持有副本文件句柄时 shutil.copy 覆盖会导致副本数据混乱**（旧引擎/WAL 残留）→ 验证前必须先停服务、删旧副本文件（db/-wal/-shm）、重建、再起服务
- 测试账号/token 用后即弃；结束清理 registry 行 + 副本文件

## 产物

- `npm run build:trial`（dist-trial/UserManage chunk 含新逻辑）
- 测试脚本已清理（tools/tmp/ 无残留）
