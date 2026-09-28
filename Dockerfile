# ==========================================
# EasyFix — Dockerfile（单阶段构建）
#   前端在 Windows 本地构建（frontend/dist 随包上传，见 deploy.ps1），
#   服务器只做后端运行环境：python:3.12-slim + uv 装依赖 + 拷贝代码与 dist
#
# 构建：docker build -t easyfix .
# 一键部署：deploy.bat（本地 npm run build 前端 → 打包上传 → 服务器构建并启动）
# ==========================================

# ---------- 后端运行时 ----------
# python:3.12 —— 依赖锁定的 pydantic-core 2.16.2 只有 cp312 以下 wheel，
# 3.13/3.14 会触发源码编译卡死；3.12 全 wheel 零编译，后期加包也兼容
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_INDEX_URL=https://mirrors.aliyun.com/pypi/simple \
    UV_INDEX_URL=https://mirrors.aliyun.com/pypi/simple \
    UV_DEFAULT_INDEX=https://mirrors.aliyun.com/pypi/simple \
    UV_NO_CACHE=1 \
    EASYFIX_FONT=/app/backend/fonts/simhei.ttf

WORKDIR /app

# 中文字体：随包上传的 simhei.ttf（Windows 黑体，与本地 PDF 输出一致），
# 不装 fonts-noto-cjk —— 省掉 apt-get update + 56MB 下载，构建快、镜像小

# Python 依赖（独立层，代码改动时可命中缓存）
# uv = Rust 写的包管理器，比 pip 快 10-100 倍；--system 装进镜像系统环境
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir uv \
    && uv pip install --system -r /app/backend/requirements.txt

# 后端代码（含 backend/.env 配置与 easyfix_main.db 种子库）
COPY backend/ /app/backend/

# 前端构建产物（本地 npm run build 生成，随包上传；FastAPI 同源托管）
COPY frontend/dist /app/frontend/dist

# 试用版前端构建产物（本地 npm run build:trial 生成；FastAPI 同源托管于 /{trial_key}/）
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
