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

- **建表方式**：后端启动时通过 `Base.metadata.create_all()` 自动建表，无迁移系统。修改表结构需删除 `backend/easyfix.db`（SQLite）或手动重建表（MySQL）。
- **后端路由数量**：`backend/app/main.py:46-60` 注册了 15 个路由。`CLAUDE.md` 写的 11 个已过时，缺少 `learning_report`、`motivation`、`error_type`、`reading`。
- **前端路由数量**：`frontend/src/router/index.js` 定义了 13 条路由。`CLAUDE.md` 写的 8 条已过时，缺少 `/reading`、`/reading-test/:id`、`/learning-reports`、`/motivation`、`/learning-analysis`。
- **软删除**：所有新模型必须包含 `deleted` 字段，禁止硬删除。
- **配置加载**：`backend/.env` 通过 pydantic-settings 加载，详见 `backend/app/config.py`。`backend/config/` 下的 `llm.json` 和 `ocr.json` 通过 `/api/config` 接口运行时覆盖。
- **文件上传路径**：`backend/uploads/images/{year}/{month}/{uuid}_{filename}`。Vite 开发服务器代理 `/uploads`，生产环境由 FastAPI 直接提供静态文件。
- **访问密码**：Settings/Management 页面密码为 `32167`，硬编码在 `backend/app/access_config.py`。
- **MCP 服务**：`.mcp.json` 配置了 MySQL（localhost:3306/easyfix）、browser、playwright。

## 新增后端路由步骤

1. 在 `backend/app/routers/<name>.py` 创建路由
2. 在 `backend/app/main.py` 添加 import 并调用 `app.include_router()`
3. 在 `backend/app/routers/__init__.py` 添加导出
4. 在 `backend/app/schemas/` 创建 Pydantic 请求/响应模型
5. 在 `backend/app/models/` 创建或更新 ORM 模型，必须包含 `deleted` 字段

## 新增前端页面步骤

1. 在 `frontend/src/views/<Name>.vue` 创建页面组件
2. 在 `frontend/src/router/index.js` 添加路由配置
3. 在 `frontend/src/App.vue` 添加侧边栏导航链接
4. API 调用写在 `frontend/src/api/` 下，使用 axios

## 代码规范

- 后端：全部 `snake_case`，函数前写中文文档字符串。
- 前端：Vue 3 Composition API + `<script setup>`，UI 组件用 Element Plus。
- 数据库：只做软删除，查询时必须加 `deleted=False` 过滤。
- 状态管理：Pinia stores 目录为空，实际未使用，状态在组件内本地管理。
