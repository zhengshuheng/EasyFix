#!/usr/bin/env bash
# EasyFix 服务器一键安装（Ubuntu 20.04+，root 或 sudo 运行）
# 用法: bash install.sh [域名] [证书通知邮箱]
set -euo pipefail

APP_DIR=/opt/easyfix
APP_USER=easyfix
DOMAIN="${1:-}"
EMAIL="${2:-}"

echo "==> [1/7] 系统依赖"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq python3-venv python3-pip nginx certbot python3-certbot-nginx fonts-noto-cjk >/dev/null

echo "==> [2/7] 应用用户与目录"
if ! id -u "$APP_USER" >/dev/null 2>&1; then
    useradd --system --home-dir "$APP_DIR" --shell /usr/sbin/nologin "$APP_USER"
fi
mkdir -p "$APP_DIR"
chown -R "$APP_USER":"$APP_USER" "$APP_DIR"

echo "==> [3/7] Python 虚拟环境 + 依赖"
if [ ! -x "$APP_DIR/.venv/bin/python" ]; then
    python3 -m venv "$APP_DIR/.venv"
fi
"$APP_DIR/.venv/bin/pip" install -q --upgrade pip
"$APP_DIR/.venv/bin/pip" install -q -r "$APP_DIR/backend/requirements.txt"

echo "==> [4/7] 配置 backend/.env（固定监听 127.0.0.1:8012，保留你的 API keys）"
ENV_FILE="$APP_DIR/backend/.env"
if [ ! -f "$ENV_FILE" ]; then
    cp "$APP_DIR/backend/.env.example" "$ENV_FILE"
fi
# Windows 编辑的 .env 可能是 CRLF，统一转 LF 再按行修改
sed -i 's/\r$//' "$ENV_FILE"
# 幂等固定监听：Nginx 反代，不对外直连
sed -i 's/^HOST=.*/HOST=127.0.0.1/; s/^PORT=.*/PORT=8012/' "$ENV_FILE"
grep -q '^HOST=' "$ENV_FILE" || echo 'HOST=127.0.0.1' >> "$ENV_FILE"
grep -q '^PORT=' "$ENV_FILE" || echo 'PORT=8012' >> "$ENV_FILE"

# PDF 中文字体：优先使用随包上传的 simhei.ttf
if [ -f "$APP_DIR/backend/fonts/simhei.ttf" ]; then
    grep -q '^EASYFIX_FONT=' "$ENV_FILE" || echo 'EASYFIX_FONT='$(realpath "$APP_DIR/backend/fonts/simhei.ttf') >> "$ENV_FILE"
    sed -i "s|^EASYFIX_FONT=.*|EASYFIX_FONT=$(realpath "$APP_DIR/backend/fonts/simhei.ttf")|" "$ENV_FILE"
    echo "  使用随包字体 backend/fonts/simhei.ttf"
fi

echo "==> [5/7] swap 兜底（2GB）"
if [ ! -f /swapfile ]; then
    fallocate -l 2G /swapfile && chmod 600 /swapfile && mkswap /swapfile >/dev/null && swapon /swapfile
    grep -q '/swapfile' /etc/fstab || echo '/swapfile none swap sw 0 0' >> /etc/fstab
    echo "  已创建 2G swap"
else
    echo "  swap 已存在，跳过"
fi

echo "==> [6/7] systemd 服务"
cp "$APP_DIR/deploy/easyfix.service" /etc/systemd/system/easyfix.service
systemctl daemon-reload
systemctl enable --now easyfix
sleep 2

echo "==> [7/7] Nginx 反代 + HTTPS"
# 替换 server_name 与证书域名占位
sed "s/__DOMAIN__/${DOMAIN:-_}/g" "$APP_DIR/deploy/nginx-easyfix.conf" > /etc/nginx/sites-available/easyfix
ln -sf /etc/nginx/sites-available/easyfix /etc/nginx/sites-enabled/easyfix
nginx -t >/dev/null && systemctl reload nginx

if [ -n "$DOMAIN" ]; then
    if [ -z "$EMAIL" ]; then
        echo "  [提示] 未提供 -Email，certbot 使用 --register-unsafely-without-email"
    fi
    certbot --nginx -d "$DOMAIN" --redirect --non-interactive --agree-tos \
        ${EMAIL:+--email "$EMAIL"} --register-unsafely-without-email >/dev/null || \
        echo "  [警告] 证书申请失败：确认域名已解析到本机、安全组放行 80/443"
else
    echo "  [提示] 未提供域名：80 端口直连。语音输入（webkitSpeechRecognition）在非 HTTPS 下不可用。"
fi

echo "==> 自检"
sleep 1
if curl -fsS http://127.0.0.1:8012/api/subjects >/dev/null; then
    echo "  本机 API OK (http://127.0.0.1:8012/api/subjects)"
else
    echo "  [错误] 本机 API 未就绪，查看: journalctl -u easyfix -n 50"
    exit 1
fi
if [ -n "$DOMAIN" ]; then
    curl -fsS "https://$DOMAIN/api/subjects" >/dev/null && echo "  公网 HTTPS OK (https://$DOMAIN)" || echo "  [警告] 公网访问失败，检查安全组"
fi

echo "==> 每日备份 cron"
cp "$APP_DIR/deploy/backup.sh" /etc/cron.daily/easyfix-backup
chmod +x /etc/cron.daily/easyfix-backup
mkdir -p /opt/easyfix-backups

echo ""
echo "✅ 安装完成！"
echo "   本机: http://127.0.0.1:8012"
[ -n "$DOMAIN" ] && echo "   公网: https://$DOMAIN"
echo "   备份: /opt/easyfix-backups/（每日，保留 7 天）"
echo "   下一步: 阿里云安全组放行 8012（有域名时再放行 80/443）；浏览器打开后进「家长设置」改家长密码。"
