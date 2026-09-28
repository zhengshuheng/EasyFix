# 体验账号管理（运营后台）— OPS_TRIAL_ACCOUNT_MGMT

运营后台新增「体验账号管理」页（系统配置组）：查看体验账号基本信息、延长体验时间、删除账号。

## 现状模型

- 体验账号 = 主库 `easyfix.db` accounts（全局身份）+ `registry.db` spaces（key ↔ account_id ↔ db_path ↔ trial_end_at）+ 空间库 `trial_data/tenants/{key}.db`（小孩在 users role='child'）。
- 体验期：`spaces.trial_end_at`（创建时 = now + app_config.trial_days；NULL = 正式版不限）。

## 改动

### 后端 `backend/app/routers/ops_trial_accounts_router.py`（新，prefix /api/ops/trial-accounts，X-Ops 双因子）

- `GET ""` → 列表：账号 / subscription_plan / 小孩数量（只读打开空间库统计 role='child'，文件缺失按 0）/ 创建时间（spaces.created_at）/ 到期时间 / 状态（ok=体验中 / expired=已过期 / pro=正式版）。
- `POST /{account_id}/extend {days}` → 延长：`trial_end_at += days`（1~3650 整数校验）；正式版（NULL）拒绝延长。
- `DELETE /{account_id}` → 删除账号：`delete_space(key)`（引擎缓存 + db 文件 + registry 行）+ 删 accounts 行；返回是否连带删空间。
- `main.py` 注册 router。

### 修复 `backend/app/trial.py` `delete_space()`

原实现只 `_tenant_engines.pop(key)` 不移除连接池句柄 → Windows 下空间库文件被占用，`os.remove` 静默失败（registry 删了但 .db 文件残留，reset/删除功能都会留孤儿文件）。已改为 pop 前取 engine 并 `dispose()` 释放底层连接，再删文件。

### 前端 `frontend/ops/src/views/TrialAccounts.vue`（新）+ router.js + OpsLayout.vue 菜单

- 表格列：账号 / 订阅（正式版/体验 tag）/ 小孩数量 / 创建时间 / 到期时间（正式版"不限"、过期标红）/ 状态 / 操作（延长体验、删除）。
- 延长弹窗：当前到期 + 延长天数（1~3650 + 快捷 +7/+15/+30/+90）+ 延长后到期实时预览；正式版禁用并提示。
- 删除确认弹窗：账号名 + 小孩数量警告 + 不可恢复提示。

## 验证（全部通过）

| 项 | 结果 |
|---|---|
| 列表 | 17 项真实账号，小孩计数 1/3 正常，状态 ok |
| 注册临时账号 | /api/account/register → 空间 + trial_end_at（now+15天）出现在列表 |
| 延长 | +30 天：2026-10-11 → 2026-11-10；再 +7 叠加 → 2026-11-17 |
| 非法天数 | -1 → 400「延长时间需为 1~3650 天的整数」 |
| 删除 | 账号+空间+registry 全删，列表不再出现 |
| delete_space 修复 | 注册→删除后空间库 .db 文件真正不存在（修复前残留） |
| 浏览器 UI | 菜单（系统配置组）+ 表格列完整 + 延长弹窗预览正确（+30：10-09→11-08）+ 删除确认文案 |

## 测试数据

两个临时账号（13911112222 / 13913334444）均已在删除流程中清理，空间库文件与 registry 无残留；上轮遗留孤儿文件 `7I-tkNaNuSRgSw.db` 也在验证中一并删除。

## 遗留

无。学生端到期行为（`/api/trial/status` 剩余天数/过期）复用现有 `trial_end_at` 字段，运营延长/删除后立即生效。
