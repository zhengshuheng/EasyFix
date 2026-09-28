# AGENTS.md

## 项目简介

EasyFix：学生错题整理应用。Vue 3 + Vite 前端，Python FastAPI 后端，默认 SQLite，可切换 MySQL。

完整架构参考见 `CLAUDE.md`，本文件仅记录实操要点。

## 开发命令

项目无测试套件、无 linter、无 typecheck、无 CI、无 pre-commit hook。

```bash
# 后端（从仓库根目录执行）
cd backend
pip install -r requirements.txt
python -m app.main              # 启动服务，默认端口 :8000
# 或：uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload

# 前端（从仓库根目录执行）
cd frontend
npm install
npm run dev                     # 启动开发服务器 :5173，自动代理 /api 和 /uploads 到 :8000
npm run build                   # 生产构建，输出到 dist/
```

## 关键事实

- **数据隔离（多小孩，必读）**：家长账户下多个小孩（role=child）。前端 `frontend/src/api/http.js`
  自动注入 `X-Kid-Id` 请求头；后端一律用 `app/utils/kid_context.py` 的
  `get_current_kid_id`（读，未选=全部）/ `get_required_kid_id`（写，未选=400）依赖 + `filter_by_kid` 过滤。
  **禁止**在请求体传 user_id、禁止 `_resolve_user_id` 回退"第一个小孩"、禁止硬编码 `user_id=1`。
  新增功能前先读 `docs/ARCHITECTURE.md`（数据隔离架构说明 + 检查清单）。
- **建表方式**：后端启动时通过 `Base.metadata.create_all()` 自动建表，无迁移系统。修改表结构需删除 `backend/easyfix_main.db`（SQLite）或手动重建表（MySQL）。
- **后端路由数量**：`backend/app/main.py:46-60` 注册了 15 个路由。`CLAUDE.md` 写的 11 个已过时，缺少 `learning_report`、`motivation`、`error_type`、`reading`。
- **前端路由数量**：`frontend/src/router/index.js` 定义了 13 条路由。`CLAUDE.md` 写的 8 条已过时，缺少 `/reading`、`/reading-test/:id`、`/learning-reports`、`/motivation`、`/learning-analysis`。
- **软删除**：所有新模型必须包含 `deleted` 字段，禁止硬删除。
- **配置加载**：`backend/.env` 通过 pydantic-settings 加载，详见 `backend/app/config.py`。`backend/config/` 下的 `llm.json` 和 `ocr.json` 通过 `/api/config` 接口运行时覆盖。
- **文件上传路径**：`backend/uploads/images/{year}/{month}/{uuid}_{filename}`。Vite 开发服务器代理 `/uploads`，生产环境由 FastAPI 直接提供静态文件。
- **访问密码**：Settings/Management 页面密码为 `32167`，硬编码在 `backend/app/access_config.py`。
- **MCP 服务**：`.mcp.json` 配置了 MySQL（localhost:3306/easyfix）、browser、playwright。
- **导航菜单**：`frontend/src/App.vue` 顶部水平菜单，包含首页、错题、单词、练习、阅读、统计、学习分析、激励中心、管理、配置。
- **前端 API 层**：`frontend/src/api/` 下有 5 个模块（question、word、learning_report、motivation、learning_analysis），其余 API 直接在组件内调用。

## 新增后端路由步骤

1. 在 `backend/app/routers/<name>.py` 创建路由
2. 在 `backend/app/main.py` 添加 import 并调用 `app.include_router()`
3. 在 `backend/app/routers/__init__.py` 添加导出
4. 在 `backend/app/schemas/` 创建 Pydantic 请求/响应模型
5. 在 `backend/app/models/` 创建或更新 ORM 模型，必须包含 `deleted` 字段

## 新增前端页面步骤

1. 在 `frontend/src/views/<Name>.vue` 创建页面组件
2. 在 `frontend/src/router/index.js` 添加路由配置
3. 在 `frontend/src/App.vue` 顶部菜单添加导航链接
4. API 调用写在 `frontend/src/api/` 下，使用 axios

## 文档归档约定（重要，每次任务必须遵守）

- **任务工作文档不建在项目根目录**，一律放 `docs/tasks/active/{SLUG}.md`（进行中，gitignore）。
- 任务完成后：移到 `docs/tasks/done/{YYYY-MM-DD}-{SLUG}.md`（已完成）或 `docs/tasks/planned/{SLUG}.md`（计划/暂停），并更新 `docs/tasks/README.md` 索引。
- 开始任务前先读 `docs/README.md`（文档地图）与 `docs/CONVENTIONS.md`（完整规则）。
- 根目录禁止新增任何 `.md`（README/AGENTS/CLAUDE/CHANGELOG 除外）。

## 临时文件约定（重要）

- 一次性脚本/测试产物/调试日志/截图一律写 `tools/tmp/`（gitignore），**禁止散落根目录**（`tmp_*`、`_*`、`*.mp3`、`browser_screenshot_*.png`、调试 `.log`）。
- 会话收尾运行 `python tools/cleanup.py` 清空临时区。
- 有复用价值的工具脚本（devserver.py、selftest_* 等）才允许留在 `tools/`。

## 代码规范

- 后端：全部 `snake_case`，函数前写中文文档字符串。
- 前端：Vue 3 Composition API + `<script setup>`，UI 组件用 Element Plus。
- 数据库：只做软删除，查询时必须加 `deleted=False` 过滤。
- 状态管理：Pinia stores 目录为空，实际未使用，状态在组件内本地管理。
- **模块体积上限（硬约束，防止生成大模块）**：后端 `.py` ≤ 400 行，前端 `.vue` ≤ 500 行（含 template/style）。新代码写到接近上限时**必须拆分后再继续**，禁止往超限文件追加：
  - 前端：模板区块 → `frontend/src/components/`，逻辑/请求 → `frontend/src/composables/`（新建目录）。
  - 后端：业务逻辑 → `backend/app/services/`；router 只留路由壳（声明 + 入参校验 + 调 service + 返回），业务规则不进 router。
- 拆分为纯重构：保持行为不变，改完做冒烟/接口验证，不顺手改业务。存量超限文件（如 `PracticeSets.vue`、`practice_set.py`）在下次功能改动时同步拆分。
- **共享常量约束**：多页面/多组件共用的常量（题型配置、分值表、枚举文案等）必须抽到 `frontend/src/constants/` 或 `backend/app/constants.py`，禁止复制进各文件（曾因拆分复制常量导致引用断裂回归）。
- **移动/删除代码前先查引用**：大文件拆分子组件/函数时，先 grep 该符号在**源文件保留区**的全部引用再删定义；移动后两处都要 import。教训：删了 `QUESTION_TYPE_*` 定义但列表/详情仍引用 → 详情弹窗运行时崩溃。

## 搜索纪律（省 token，重要）

QwenPaw 的搜索工具（grep_search / glob_search / ast_search）**不尊重 .gitignore**，会扫到忽略区文件并浪费 token。默认必须缩小范围：

- **grep_search / glob_search 必须先带 `path` 限定**，默认只搜：`backend/app`、`backend/config`、`frontend/src`、`frontend/public`、`docs`、`tools`。
- **禁止全文搜索**（不带 path 的全仓库搜）：`node_modules`、`.venv`、`dist`、`site`、`tools/tmp`、`*.log`、`*.db*`、根目录散落 TODO。
- **目录浏览**：`dir /b` 只看需要的子目录（如 `backend/app/routers`），不列根目录全览。
- **读文件前先想是否必要**：优先 lsp（Python）定位符号、ast_search 查结构；>300 行的大文件用 start_line/end_line 分段读，不整文件读入。
- **大文件定位问题 SOP（省 token，强制）**：
  1. 先描述症状（报错/UI 现象）→ `grep_search` 带 `path` + `context_lines=1~3` 找关键词（错误文本/函数名/路由），**禁止整读 >300 行文件**。
  2. 大文件先跑 `python tools/file_map.py <文件>` 拿结构地图（template 区块注释 / script 顶层符号 / py 函数，含行号），输出仅几十行。
  3. 按地图行号用 `read_file start_line/end_line` 精确读目标段（每次 ≤60 行），不读无关区。
  4. 改完删除/移动定义前，grep 该符号在文件内的全部引用，确认保留区无遗漏（防拆分回归）。
- 每批任务收尾必跑 `python tools/cleanup.py` 清 `tools/tmp/`。
