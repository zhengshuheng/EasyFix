#!/usr/bin/env bash
# ==========================================
# EasyFix 远端部署脚本（由 deploy.bat 上传到 /opt/easyfix 后执行）
# 用法: bash deploy/remote_deploy.sh [DOMAIN]
#   DOMAIN 有值 => Caddy 自动申请 HTTPS 证书（语音输入可用）
#   DOMAIN 留空 => 纯 HTTP :80（语音输入不可用）
# ==========================================
set -e

DOMAIN="${1:-}"
REMOTE_DIR="/opt/easyfix"
DATA_DIR="/opt/easyfix-data"
IMAGE_NAME="easyfix"
CONTAINER_NAME="easyfix"
HOST_PORT="8012"      # 对外直连端口（与本地一致，公网 http://IP:8012）
CONTAINER_PORT="8012"

cd "$REMOTE_DIR"

# 解压代码包（包不存在=已解压过，跳过；支持重复部署）
if [ -f deploy_package.tar.gz ]; then
    tar -xzf deploy_package.tar.gz -C "$REMOTE_DIR"
    rm -f deploy_package.tar.gz
fi

# 首次部署：初始化种子数据库（已存在则跳过，防止覆盖服务器数据）
if [ -f backend/easyfix_main.db ] && [ ! -f "$DATA_DIR/easyfix_main.db" ]; then
    cp backend/easyfix_main.db "$DATA_DIR/easyfix_main.db"
    echo ">>> 已初始化种子数据库"
fi
# 主库改名迁移：服务器上仍是旧的 /data/easyfix.db 时自动更名（一次）
if [ -f "$DATA_DIR/easyfix.db" ] && [ ! -f "$DATA_DIR/easyfix_main.db" ]; then
    mv "$DATA_DIR/easyfix.db" "$DATA_DIR/easyfix_main.db"
    echo ">>> 已将旧主库 /data/easyfix.db 迁移为 /data/easyfix_main.db"
fi

# trial_data（空间库/注册表/模板）持久化目录：代码包已 exclude backend/trial_data，
# 容器首次启动时 ensure_template_db / _registry_conn 会自动生成 template.db 与 registry.db
mkdir -p "$DATA_DIR/trial_data"

# ------------------------------------------------------------
# [3.5/5] schema 漂移自动修复（治本）
# 云端主库是持久化的旧库，模型新增列后 create_all 不会 ALTER 既有表，
# 而业务初始化（如 init_preset_data 查 star_action.ops_override）会直接
# OperationalError -> 容器无限重启、端口不绑定、公网不可访问。
# 这里在启动容器前，用当前代码的模型元数据比对主库、自动补缺失列。
# 失败不阻断部署（应用侧 main.py 启动时也有同样的幂等迁移兜底）。
# ------------------------------------------------------------
echo ">>> [3.5/5] 检查云端主库 schema 漂移并自动补列..."
if [ -f "$DATA_DIR/easyfix_main.db" ]; then
    docker run --rm \
        -v "$DATA_DIR:/data" \
        -v "$REMOTE_DIR/backend:/app/backend" \
        -e DB_PATH=/data/easyfix_main.db \
        -w /app/backend \
        "$IMAGE_NAME" \
        python3 -c "
import os, sqlite3
from sqlalchemy import create_engine
from app.database import Base
import app.models  # noqa: F401  触发模型注册
db = os.environ['DB_PATH']
engine = create_engine('sqlite:///' + db)
dialect = engine.dialect
conn = sqlite3.connect(db)
added = 0
for table in Base.metadata.sorted_tables:
    cols = [r[1] for r in conn.execute('PRAGMA table_info(%s)' % table.name)]
    if not cols:
        continue
    for col in table.columns:
        if col.name in cols:
            continue
        ddl = col.type.compile(dialect)
        conn.execute('ALTER TABLE %s ADD COLUMN %s %s' % (table.name, col.name, ddl))
        print('  + %s.%s %s' % (table.name, col.name, ddl))
        added += 1
conn.commit()
conn.close()
print('>>> schema 漂移检查完成，补充 %d 列' % added)
" \
    || echo ">>> 警告：schema 漂移检查失败（不阻断部署；应用启动时会再次尝试幂等迁移）"
else
    echo ">>> 跳过（云端主库尚不存在，将由种子库初始化）"
fi

# 容器网络（幂等）
docker network create easyfix-net >/dev/null 2>&1 || true

# 停止并删除旧容器（兼容旧版 docker run 部署）
echo ">>> [4/5] 停止旧容器..."
docker stop "$CONTAINER_NAME" 2>/dev/null || true
docker rm "$CONTAINER_NAME" 2>/dev/null || true
docker stop caddy 2>/dev/null || true
docker rm caddy 2>/dev/null || true

# 重新构建镜像
echo ">>> 构建新 Docker 镜像..."
docker build -t "$IMAGE_NAME" "$REMOTE_DIR"

# 启动服务容器
echo ">>> [5/5] 启动服务容器..."
docker run -d --name "$CONTAINER_NAME" --network easyfix-net \
    -p "$HOST_PORT:$CONTAINER_PORT" \
    --restart=always \
    -v "$DATA_DIR/uploads:/app/backend/uploads" \
    -v "$DATA_DIR/data:/app/backend/data" \
    -v "$DATA_DIR/trial_data:/app/backend/trial_data" \
    -v "$DATA_DIR:/data" \
    -e DB_PATH=/data/easyfix_main.db \
    -e HOST=0.0.0.0 \
    -e PORT="$CONTAINER_PORT" \
    "$IMAGE_NAME"

# Caddy 反代：有域名自动 HTTPS，无域名纯 HTTP :80
mkdir -p "$DATA_DIR/caddy"
if [ -n "$DOMAIN" ]; then
    echo "$DOMAIN { reverse_proxy $CONTAINER_NAME:$CONTAINER_PORT }" > "$DATA_DIR/caddy/Caddyfile"
    echo ">>> 已启用 HTTPS 反代: $DOMAIN（首次证书申请约 1-2 分钟）"
else
    cp "$REMOTE_DIR/deploy/caddy/Caddyfile.http" "$DATA_DIR/caddy/Caddyfile"
    echo ">>> 已启用 HTTP 反代（无域名，语音输入不可用）"
fi
docker run -d --name caddy --network easyfix-net \
    -p 80:80 -p 443:443 \
    --restart=always \
    -v "$DATA_DIR/caddy/Caddyfile:/etc/caddy/Caddyfile" \
    -v caddy_data:/data \
    -v caddy_config:/config \
    caddy:2

# 清理悬空镜像
docker image prune -f > /dev/null

# 健康检查
sleep 5
if curl -fsS "http://127.0.0.1:$HOST_PORT/health" >/dev/null 2>&1; then
    echo ">>> 健康检查通过"
else
    echo ">>> 警告：健康检查未通过，请运行 docker logs $CONTAINER_NAME 查看日志"
fi

# ops 权威数据同步：本地主库导出的配置表（deploy/ops_data.sql）按 id 幂等 upsert 进云端主库。
# 只更新语法教程/激励规则/成就等配置表，不触碰空间/用户/错题等真实数据；失败仅警告，不阻断部署。
if [ -f deploy/ops_data.sql ] && [ -f "$DATA_DIR/easyfix_main.db" ]; then
    echo ">>> 同步 ops 权威数据（语法教程/激励配置）..."
    cp deploy/ops_data.sql "$DATA_DIR/ops_data.sql"
    cp deploy/ops_data_sync.py "$DATA_DIR/ops_data_sync.py"
    if docker exec "$CONTAINER_NAME" python3 /data/ops_data_sync.py; then
        echo ">>> ops 数据同步完成"
        rm -f "$DATA_DIR/ops_data.sql"
    else
        echo ">>> 警告：ops 数据同步失败（不影响本次部署；可手动重试: docker exec easyfix python3 /data/ops_data_sync.py）"
    fi
else
    echo ">>> 跳过 ops 数据同步（未检测到 deploy/ops_data.sql 或云端主库）"
fi

# 权威词表同步：deploy/words_oxford.json（公开牛津深圳版 12 册）幂等 upsert 进云端主库。
# 策略：同(版本+年级+册次+词)权威覆盖（AI 释义/单元/来源被修正，软删行复活）；
#       AI 独有的词保留并标 ai，运营后台可筛选人工核对。失败仅警告，不阻断部署。
if [ -f deploy/words_oxford.json ] && [ -f "$DATA_DIR/easyfix_main.db" ]; then
    echo ">>> 同步权威词表（牛津深圳版 12 册）..."
    cp deploy/words_oxford.json "$DATA_DIR/words_oxford.json"
    cp deploy/words_sync.py "$DATA_DIR/words_sync.py"
    if docker exec "$CONTAINER_NAME" python3 /data/words_sync.py; then
        echo ">>> 权威词表同步完成"
        rm -f "$DATA_DIR/words_oxford.json"
    else
        echo ">>> 警告：权威词表同步失败（不影响本次部署；可手动重试: docker exec easyfix python3 /data/words_sync.py）"
    fi
else
    echo ">>> 跳过权威词表同步（未检测到 deploy/words_oxford.json 或云端主库）"
fi

echo ">>> 当前运行的容器："
docker ps --filter name="$CONTAINER_NAME" --filter name=caddy
