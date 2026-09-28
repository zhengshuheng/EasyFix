# easyfix_demo — 架构统一（注册即建空间 + 正式数据收编 easyfix_demo + 移除 /app）

> 用户确认（2026-09-24）：租户 key 固定 `easyfix_demo`（仅自用调试）；`/app` 直接移除不重定向（无老用户包袱）；A+B+C 一起做，阶段 D（前端合并）后续再做。

## 背景查证结论

- `backend/easyfix.db`（正式库）与 `trial_data/template.db` 业务表 **40 张完全一致**；正式库仅多 `accounts`/`app_config`（主库专属，不搬），`practice_set_question` 多 `student_answer` 列 → **直接复制正式库为租户库最稳**。
- 正式库数据：accounts 6 个（zhengshuheng=id1 为主账号）；users 1 家长(admin)+3 小孩（郑予 id4/郑好 id5/演示小孩 id3）；practice_question 759、practice_set 43、assessment_record 39、error_question 64、word 313 等。
- registry.db 现有 6 空间；`tenants` 表已迁移 DROP。
- **隐患**：租户引擎是进程内字典，仅建空间/登录时注册——服务重启后已有空间 API 会回退正式库。阶段 B 必须补懒注册。
- **隐患**：前端 `http.js` 从 localStorage 读 trial_key——直接访问 `/easyfix_demo/` 会带错 key，需改为 URL 优先解析。
- 官网前端 `app.js` 对 `r.space` 自适应（有空间显示"进入空间"）→ 阶段 A 后端改完即生效，前端零改动。

## 计划

- [x] 查证：路由结构 / 注册流程 / 租户机制 / schema 比对 / 前端 trial_key 机制
- [x] A. `account_api.register` 成功后自动建空间（复用 `create_space_for_account`），返回带 `space`
- [x] B1. `trial.py` 加 `ensure_tenant_engine(key)` 懒注册 + `main.py` middleware 调用（修重启泄漏）
- [x] B2. 复制 `easyfix.db` → `tenants/easyfix_demo.db` + registry 登记（account_id=1, zhengshuheng, trial_end_at=NULL 正式）
- [x] B3. `http.js` trial key 改为 URL path 优先解析 + 重建 `dist-trial`
- [x] C. `main.py` 删 `/app` 路由 + spa_fallback 改 404（保留 /assets /icons mount）
- [x] 验证：起服务 → A 注册自动建空间 / B `/easyfix_demo/` 数据完整 / C `/app`、`/home` 404 且 `/site`、`/` 200（**19/19 通过**）
- [x] 清理测试数据 + 收尾 `python tools/cleanup.py`

## 验证结果（2026-09-24，`tools/tmp/test_arch_unify.py`，端口 8017）

- 阶段 C：`/`、`/site` 200；`/app`、`/app/parent-center`、`/home` 404 ✅
- 阶段 B：`/easyfix_demo/` 200；`X-Trial-Key: easyfix_demo` status → is_pro=True + username=zhengshuheng（懒注册生效）；既有空间 `zxc0ishrSBJ5OQ` is_pro=False；无效 key 403 ✅
- 阶段 A：注册返回 space.key + db 文件 + registry 登记；登录复用；空间内官网账号密码可登家长中心 ✅
- 测试账号/空间已清理（spaces=7：原 6 + easyfix_demo；accounts 无残留）
