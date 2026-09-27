# HELPER_PARENT_LOCK — 辅助账号进家长中心密码锁卡死修复（2026-09-28 完成）

## 现象
- 用户报告：辅助账号官网登录 + 登录墙登录都通了，但**登录后家长中心进不去**（密码锁弹窗输密码不关）。

## 根因（curl 实证）
- `ParentLockDialog.vue` 家长密码锁第一步用**原生 fetch(`/api/auth/me`)**，**没带 X-Trial-Key** → 租户中间件不切库 → 落到**主库**。
- 主库 `User.id` 与租户库**错位**：辅助账号在租户库 id=3，主库 id=3 是「演示小孩」(role=child) → `role==='admin'` 候选收集失败。
- 候选只剩 registry 主账号名（18954578119）→ 拿辅助密码去试主账号 → 全败 → 弹窗不关。
- 验证：`curl me + X-Trial-Key` → helper_test_928(admin)；`curl me 无 X-Trial-Key` → 演示小孩(child)。

## 修复
- `frontend/src/components/ParentLockDialog.vue`：me 请求手动拼 `X-Trial-Key`（URL pathname 解析 `/{key}/`，回退 localStorage `easyfix_trial_key`）。

## 验证
- 浏览器端到端：注册新号 → 建空间 ES0JZNhEKXaRkQ → 添加辅助账号 helper_test_928 → 辅助账号官网登录 → 家长设置 → 输 H3lp0928 → **进入家长中心** ✅。
- 注意：**旧 JS 缓存会导致部署后验证仍失败**——需强制刷新/`?v=` cache-busting 后才加载新 bundle。

## 提交
- git `f9dafad`（dev1.0 → mine 已推送）。
- 部署：`deploy.bat skipdb`（保留服务器数据），health 200，trial 资源 hash 已更新。

## 遗留
- 测试空间 ES0JZNhEKXaRkQ（手机号 18954578119 / helper_test_928 / 密码 H3lp0928 / 体验 15 天）待运营删除（ops 凭据在远端库，本地无权限）。
