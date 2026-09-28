# OpenSpec · EasyFix 评测系统

> Spec-Driven Development（规范驱动开发）工作区。任何**需要规划的功能改造**，
> 先在此创建 change（proposal → design → tasks），实现与验证通过后归档。

## 项目概况

- **仓库**：E:\qianwenpaw\EasyFix-main（前端 + 后端 + 官网 + 运营后台单仓库）
- **技术栈**：前端 Vue3 SPA（`frontend/src`，构建产物 `frontend/dist-trial`）+ 官网静态站（`frontend/site`）+ 后端 FastAPI（`backend/app`，SQLite，端口 8012）
- **启动**：`一键重启.bat`（杀旧服务 → `backend/.venv` uvicorn 起 8012）
- **产品宪法**：评测北极星 = 提高孩子学习积极性和学习能力，深度优先于速度（见 `docs/ASSESSMENT_DESIGN.md`）
- **关键约束**：官网静态文件实时读盘（改完即生效）；SPA 改动必须 `npm run build:trial`；`deploy.ps1` 必须 UTF-8 with BOM

## 框架流程

1. **propose**：`openspec/changes/{slug}/proposal.md` —— 为什么做、做什么、影响范围
2. **design**：`design.md` —— 技术方案、接口、数据模型（需要时）
3. **tasks**：`tasks.md` —— 可勾选实现清单（实现中每完成一项立即打勾）
4. **apply**：按 tasks 实现；每批改动后验证（API / 浏览器 / 构建）
5. **verify**：对照 proposal 逐条验收，保留真实工具输出证据
6. **archive**：完成后移入 `openspec/changes/archive/{YYYY-MM-DD}-{slug}/`，并把关键结论沉淀进 `docs/AI_CONTEXT.md`

## 目录

- `changes/`：进行中的变更（每个一个文件夹）
- `changes/archive/`：已归档变更（审计历史）
- `changes/_template/`：新变更模板
