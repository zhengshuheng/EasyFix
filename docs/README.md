# EasyFix 文档地图

> 所有文档的入口。**开始任何任务前先看这里**；规则详见 `CONVENTIONS.md`。

## 📋 快速导航

| 想看什么 | 去哪里 |
|---|---|
| 模型工作上下文速查（判分/组卷/结算/高频坑） | `docs/AI_CONTEXT.md` |
| 文档管理规则（归档约定） | `docs/CONVENTIONS.md` |
| 任务进行中 / 已完成 / 计划 | `docs/tasks/README.md` |
| 产品路线图 | `docs/product/PRODUCT_ROADMAP.md` |
| 知识点打包方案 | `docs/product/KP_PACKAGE_PLAN.md` |
| 规格与开发说明 | `docs/SPEC.md`、`docs/DEVELOPMENT_PLAN.md` |
| 数据隔离架构说明（新增功能必读） | `docs/ARCHITECTURE.md` |
| 教材同步合规协议 | `docs/教材同步使用协议.md` |
| 历史设计稿（superpowers） | `docs/superpowers/{plans,specs}/` |
| 部署（阿里云） | `deploy/README.md` |
| 临时文件一键清理 | `python tools/cleanup.py`（清空 `tools/tmp/`） |
| 架构参考（AI 指令） | `AGENTS.md`、`CLAUDE.md` |
| 版本变更 | `CHANGELOG.md` |
| 项目介绍 | `README.md` |

## 🗂 目录约定

- 根目录只保留 4 个常驻文档：`README.md`、`AGENTS.md`、`CLAUDE.md`、`CHANGELOG.md`
- 任务工作文档一律在 `docs/tasks/`（active 进行中 / done 归档 / planned 计划）
- 产品级长期文档在 `docs/product/`
- 完整规则见 `docs/CONVENTIONS.md`（新增文档必须遵守，禁止再往根目录堆 .md）

## 📦 归档记录

- 2026-09-21：根目录 45 个 `*_TODO.md` 完成首次整理归档 →
  43 个已完成移入 `docs/tasks/done/2026-09-21-*.md`，
  2 个计划（`PHOTO_SUBMIT`、`SPEAKING`）移入 `docs/tasks/planned/`；
  `PRODUCT_ROADMAP.md`、`KP_PACKAGE_PLAN.md` 移入 `docs/product/`。
