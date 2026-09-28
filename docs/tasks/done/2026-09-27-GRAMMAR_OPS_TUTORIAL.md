# GRAMMAR_OPS_TUTORIAL — 语法教程运营化

**状态：已完成（2026-09-27）**
**根因**：主库 grammar_lesson 44 条教程内容已完备，但模板库/存量空间是旧快照（29 条 skeleton 无内容）→ 前端显示「教程内容暂缺」。

## 方案（主库 ops 权威 + 建空间自动同步 + 显式更新逻辑）

- **权威源**：主库 grammar_lesson（trial.copy_global_content 建空间时复制、保留主键 id → 空间/主库 id 一致）
- **自动同步**：`trial._sync_template_grammar()` 在 ensure_template_db 每次调用时把主库教程 upsert 进模板库 → 新空间创建（复制模板）必带最新教程；main.py 启动时 ensure_template_db 已触发
- **更新逻辑**：空间端 `POST /api/grammar/sync-tutorials`（家长管理页「同步官方教程」按钮）；运营后台「推送到所有空间」`POST /api/ops/grammar/sync-tenants`（遍历 registry spaces + 模板库）
- **固化**：空间端 create/update/delete/ai-generate-skeleton/ai-generate-tutorial 全部 403；家长端 GrammarManager 只读 + 同步按钮

## 改动文件

- 新增 `backend/app/services/grammar_sync.py`：sync_grammar_from_main（SQLAlchemy）/ sync_grammar_sqlite（sqlite3 直写），按 id upsert + 软删主库已移除点，subject_id 用目标库英语学科
- 新增 `backend/app/routers/ops_grammar_router.py`：`/api/ops/grammar/lessons` GET/PUT/详情、`/ai-generate`（AI 批量生成缺失教程）、`/sync-tenants`；X-Ops-* 鉴权
- `backend/app/routers/grammar.py`：新增 `POST /sync-tutorials`；写接口固化 403（_ensure_readonly）
- `backend/app/trial.py`：新增 `_sync_template_grammar()`；ensure_template_db 幂等分支与生成分支均调用
- `backend/app/main.py`：注册 ops_grammar_router
- 前端 ops：`GrammarTutorialsManage.vue`（列表/编辑弹窗/生成缺失/推送同步）+ 路由 `/grammar-tutorials` + 菜单「系统配置 ▸ 语法教程」；api/ops.js 加 5 个函数
- 前端空间：`GrammarManager.vue` 只读 + 「🔄 同步官方教程」按钮；api/grammar.js 加 syncTutorials

## 验证（8012 重启后全通过）

| 项 | 结果 |
|---|---|
| 模板库启动自动同步 | ✓ 日志 updated 44，missing 0 |
| 空间端同步（SvXXG4zukMip0A） | ✓ missing 29→0 |
| 固化 403 | ✓ create / ai-generate-tutorial / delete 全 403 |
| ops 推送全部空间 | ✓ 模板+3 空间各 updated 44，无失败 |
| 编辑→同步→空间生效 | ✓ ops PUT mnemonic → 空间 sync → 空间库更新（已还原原值） |
| ops 前端页 | ✓ 菜单/列表/状态 badge/编辑按钮 |
| 主库数据还原 | ✓ id=1 mnemonic 原值 + source=ai（测试值已还原） |

## 运维备忘

- ops 凭证：admin / easyfix-ops（X-Ops-* 头）
- 8012 重启方式：wmic terminate 旧 PID → `wmic process call create "cmd /c cd /d E:\qianwenpaw\EasyFix-main\backend && E:\qianwenpaw\EasyFix-main\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8012 > E:\qianwenpaw\EasyFix-main\tools\tmp\server_8012.log 2>&1"`
- 以后运营改教程：/ops/ → 系统配置 → 语法教程 → 编辑保存 → 「推送到所有空间」；家长空间内也可自行点「同步官方教程」

## 追加：教程版面体验优化（2026-09-27，用户反馈「滚动很长」）

**问题**：教程页 = 标题 + 总结 + 长篇正文 + 例句 + 易错点 + 口诀一条纵向长流，找内容要滚很久。

**改动**（仅 `frontend/src/views/Grammar.vue`，无后端改动）：

- 正文按 `##` 拆成**分节卡片**（`contentSections` computed：`md.split(/^##\s+/m)`，`###` 归属父节），每节独立卡片 + 序号 + 折叠头（`collapsed` 对象 + `toggleBlock`）
- 顶部「📖 本课包含」chips（`outlineItems`：各节 + 例句 n + 易错点 n + 口诀），点击直达；右侧「全部收起/展开」按钮
- 右栏新增吸顶「📑 本课目录」，点击平滑滚动（`scrollToSection`，`nextTick` 后 `scrollIntoView`）；**目标块折叠时自动展开**；window scroll 节流 80ms 高亮当前节（`activeSection`）
- 例句/易错点/口诀由 `lesson-section` 改为同款折叠卡片；底部新增「← 上一个 / n / N / 下一个 →」（`siblingNav`）+ `el-backtop`
- `ensureLessonIndex()`：直达 `/grammar/:id` 时补载 allLessons（原先只有列表页加载 → 同板块导航为空）
- 样式：`.lesson-block/.block-head/.toc-item/.lesson-footer-nav/.lesson-outline`，`scroll-margin-top: 84px` 防吸顶遮挡

**验证**（临时空间 dI24YSzDQmBUOw，账号 ui_grammar_0927，验证后已用 DELETE /api/ops/trial-accounts/3 彻底清理：registry 0 行、db 文件不存在、accounts 0 行）：

| 项 | 结果 |
|---|---|
| 新建空间自带全部教程 | ✓ 44 条、missing 0（顺带验证建空间自动同步） |
| 分节卡片 | ✓ gsec-0「1 这是啥」/ gsec-1「2 怎么用」… 按 `##` 正确拆分 |
| 本课包含 chips + 目录 | ✓ 这是啥/怎么用/小练习/例句（8）/易错点（5）/记忆口诀 |
| 块头折叠切换 | ✓ `locator('.block-head').first.click()` 三次：收起→展开→收起 |
| 全部收起 | ✓ 正文全部隐藏 |
| 目录跳转 + 自动展开 | ✓ 收起态点「记忆口诀」→ 口诀内容出现、其它块仍收起 |
| 底部上下节导航 | ✓ 「1 / 8」+「祈使句 →」点击后切换标题、折叠重置、回顶部 |
| 同板块导航（直达页） | ✓ ensureLessonIndex 后显示 |

**坑**：首轮构建只跑了 `npm run build`（dist），而空间入口用 `dist-trial` → 页面没变化；补 `npm run build:trial` 才生效。浏览器还会缓存旧 index.html，验证时用 `?v=N` 换 URL；`findstr` 搜 UTF-8 中文假阴性，用 Python 查产物字符串。
