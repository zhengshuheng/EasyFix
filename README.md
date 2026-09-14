# EasyFix 错题整理学习软件

> 面向中小学生的本地错题整理与学习软件：拍照上传错题、OCR 自动识别、AI 生成相似题、错题统计分析、单词记忆、练习卷 PDF 生成，一站式学习助手。

**当前版本**: v1.0.8 · 前端 Vue 3 + 后端 FastAPI · 本地运行，数据自持

---

## ✨ 功能特性

| 模块 | 说明 |
|------|------|
| 📷 错题录入 | 拍照/图片上传，OCR 自动识别题目文字（支持 PaddleOCR 本地识别 / 云 API / 多模态大模型） |
| 🗂 错题管理 | 按学科、年级、知识点、错误类型、标签归档整理，支持错题本 |
| 📊 学习分析 | 错题统计 Dashboard、知识点错误排行、错误类型饼图、日历热力图、掌握率环形图、LLM 深度分析 |
| 🤖 相似题推荐 | 基于 LLM 生成同类型练习题，举一反三 |
| 📄 练习卷 PDF | 一键从错题生成练习集，导出 PDF（难度星级彩色标注） |
| 📚 单词学习 | 单词管理 + 艾宾浩斯记忆曲线复习（新学/在途/遗忘点/牢记四阶段） |
| 📖 阅读理解 | 阅读材料管理 + 阅读测试 |
| 📈 学习报告 | 周期学习报告生成（LLM 结构化总结） |
| 🎯 激励系统 | 成就、星星奖励、奖励商城，激发学习动力 |
| 🗣 语音朗读 | TTS 朗读（单词/阅读） |

---

## 🛠 技术栈

| 层级 | 技术选型 |
|------|---------|
| 前端 | Vue 3 + Element Plus + ECharts（构建产物位于 `frontend/dist`） |
| 后端 | Python FastAPI + SQLAlchemy + Uvicorn |
| 数据库 | SQLite（默认，零配置）/ MySQL 8.0 / PostgreSQL |
| OCR | PaddleOCR（本地）/ Baidu / Tencent / Multimodal（Claude·Qwen·GPT-4o 视觉） |
| LLM | Anthropic Claude API / OpenAI 兼容接口 |

---

## 🚀 快速开始（一键启动）

> 已配置好项目虚拟环境 `.venv`，无需手动安装依赖。

1. **双击运行** 项目根目录的 **`一键启动.bat`**
2. 弹出的黑色窗口保持开启（这是服务窗口，关闭即停止服务）
3. 等待提示「服务已启动」，浏览器自动打开 **http://localhost:8010/**
4. 局域网内其它设备可访问 **http://<本机IP>:8010/**

> 默认访问密码：`32167`（可在 `backend/app/access_config.py` 修改）

### 首次从零部署（换机器/换环境时）

```bat
:: 1. 创建项目虚拟环境并安装依赖（需先安装 uv 或 Python 3.12）
uv venv .venv --python 3.12
uv pip install -r backend\requirements.txt

:: 2. 一键启动
一键启动.bat
```

---

## ⚙️ 配置说明

### 服务配置（`backend/.env`）— 端口配置化

所有运行参数集中在 `backend/.env`，修改后重新运行 `一键启动.bat` 生效：

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| `HOST` | `0.0.0.0` | 监听地址；`0.0.0.0`=局域网可访问，`127.0.0.1`=仅本机 |
| `PORT` | `8010` | 服务端口（前端页面与后端 API 共用），按需修改 |
| `DB_TYPE` | `sqlite` | 数据库类型：`sqlite` / `mysql` / `postgres` |
| `DB_PATH` | `easyfix.db` | SQLite 数据库文件路径 |
| `DB_HOST` / `DB_PORT` / `DB_USER` / `DB_PASSWORD` / `DB_NAME` | - | MySQL / PostgreSQL 连接参数 |

### 业务配置（`backend/config/`）

| 文件 | 说明 |
|------|------|
| `app.json` | 默认年级、学期 |
| `llm.json` | LLM 服务配置（API Key、模型、供应商） |
| `ocr.json` | OCR 服务配置（Provider：paddleocr / tesseract / baidu / tencent / multimodal） |

### OCR / LLM 密钥（`backend/.env` 或对应 config 文件）

- `OPENAI_API_KEY` / `OPENAI_BASE_URL` / `LLM_MODEL`
- `ANTHROPIC_API_KEY` / `CLAUDE_VISION_MODEL`
- `QWEN_API_KEY` / `QWEN_VISION_MODEL`
- `BAIDU_API_KEY` / `BAIDU_SECRET_KEY`、`TENCENT_*`

> 未配置密钥时，OCR/LLM 相关功能会返回错误提示，不影响错题录入等核心功能。

---

## 📁 目录结构

```
EasyFix-main/
├── 一键启动.bat            # 一键启动脚本（读 .env 端口配置）
├── backend/
│   ├── .env                # 运行配置（端口/数据库/密钥）⚠️ 勿提交
│   ├── requirements.txt    # Python 依赖
│   ├── app/
│   │   ├── main.py         # FastAPI 入口（含前端静态托管）
│   │   ├── config.py       # 配置管理（pydantic-settings）
│   │   ├── access_config.py# 访问密码
│   │   ├── models/         # ORM 模型（错题/单词/练习集/成就…）
│   │   ├── routers/        # API 路由（16 个模块）
│   │   ├── schemas/        # Pydantic 校验模型
│   │   └── services/       # 业务逻辑（OCR/LLM/PDF/TTS/激励…）
│   ├── uploads/            # 上传图片（运行时生成）
│   └── migrations/         # SQL 迁移脚本
├── frontend/
│   └── dist/               # 前端构建产物（Vue3 SPA，由后端托管）
├── docs/SPEC.md            # 产品需求文档
└── CHANGELOG.md            # 变更记录
```

---

## 🔧 开发指南

### 后端开发

```bat
cd backend
..\.venv\Scripts\python.exe -m uvicorn app.main:app --host 0.0.0.0 --port 8010 --reload
```

- 访问交互式 API 文档：`http://localhost:8010/docs`
- 健康检查：`http://localhost:8010/health`

### 前端开发（需前端源码仓库）

前端为 Vue 3 项目，构建产物已托管在 `frontend/dist`。修改前端后执行构建命令将产物输出到 `frontend/dist`，刷新页面即可生效（后端自动托管同源 `/api`，无需跨域配置）。

---

## ❓ 常见问题

| 问题 | 解决 |
|------|------|
| 双击脚本窗口一闪而过 | 确认使用根目录最新 `一键启动.bat`（GBK/CRLF 版本），在 cmd 中运行可看到报错 |
| 提示端口被占用 | 修改 `backend/.env` 的 `PORT`（如 8010）后重新启动 |
| 本机能访问、局域网打不开 | Windows 防火墙放行：`netsh advfirewall firewall add rule name="EasyFix" dir=in action=allow protocol=TCP localport=8010` |
| 访问密码是什么 / 怎么改 | 默认 `32167`，改 `backend/app/access_config.py` 的 `ACCESS_PASSWORD` |
| OCR 报错 | 检查 `backend/config/ocr.json` Provider 与对应 API 密钥；未配置时走 Multimodal 会报错，可切回 PaddleOCR 或关闭 |
| 数据库想用 MySQL | 修改 `.env`：`DB_TYPE=mysql`，配置 `DB_HOST/PORT/USER/PASSWORD/NAME` |
| 更换电脑如何迁移 | 拷贝整个项目目录（含 `.venv`、`backend/easyfix.db`、`backend/uploads/`）即可 |

---

## 📜 变更记录

详见 [CHANGELOG.md](CHANGELOG.md) 与 [docs/SPEC.md](docs/SPEC.md)
