# ==========================================
# EasyFix — Dockerfile（单阶段构建）
#   前端在 Windows 本地构建（frontend/dist-trial + dist-ops + site 随包上传，见 deploy.ps1），
#   服务器只做后端运行环境：python:3.12-slim + uv 装依赖 + 拷贝代码与前端产物
#
# 构建：docker build -t easyfix .
# 一键部署：deploy.bat（本地 npm run build:trial + build:ops 前端 → 打包上传 → 服务器构建并启动）
# 架构原则（2026-09-29）：正式版/试用版共用 dist-trial 一套空间前端（/{key}/），
#   正式/试用只是后端账号属性（spaces.trial_end_at=NULL=正式版）；dist 正式版已废弃不打包。
# ==========================================

# ---------- 后端运行时 ----------
# python:3.12 —— 依赖锁定的 pydantic-core 2.16.2 只有 cp312 以下 wheel，
# 3.13/3.14 会触发源码编译卡死；3.12 全 wheel 零编译，后期加包也兼容
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_INDEX_URL=https://pypi.tuna.tsinghua.edu.cn/simple \
    EASYFIX_FONT=/app/backend/fonts/simhei.ttf

WORKDIR /app

# 中文字体：随包上传的 simhei.ttf（Windows 黑体，与本地 PDF 输出一致），
# 不装 fonts-noto-cjk —— 省掉 apt-get update + 56MB 下载，构建快、镜像小

# Python 依赖（独立层，代码改动时可命中缓存）
# 2026-09-29 改：弃用 uv —— ECS 上 uv 二进制(20.4MB)从 aliyun 镜像下载时无重试、易长时间卡死；
# pip 自带 --timeout/--retries，网络抖动自动重试，构建更稳（代价：串行下载稍慢，一次性成本，RUN 层会缓存）
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir --timeout 60 --retries 5 -r /app/backend/requirements.txt

# 后端代码（含 backend/.env 配置与 easyfix_main.db 种子库）
COPY backend/ /app/backend/

# 试用版/正式版共用空间前端构建产物（本地 npm run build:trial 生成；FastAPI 同源托管于 /{trial_key}/）
# 正式版 = spaces.trial_end_at NULL（账号属性），前端同一套，不再构建 dist
COPY frontend/dist-trial /app/frontend/dist-trial

# 运营后台 Vue 构建产物（本地 npm run build:ops 生成；vite outDir ../dist-ops 输出到 frontend/dist-ops；/ops 直达，见 main.py OPS_DIST mount）
COPY frontend/dist-ops /app/frontend/dist-ops

# 官网静态页（宣传 + 注册入口，main.py SITE_DIR=/app/frontend/site；漏掉则 / 会退化成 SPA fallback 进旧界面）
COPY frontend/site /app/frontend/site

WORKDIR /app/backend

EXPOSE 8012

# SQLite 路径相对 cwd，必须保持 WORKDIR=/app/backend；
# 生产建议用 -e DB_PATH=/data/easyfix_main.db 挂载数据卷（deploy.bat 已处理）
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8012"]
