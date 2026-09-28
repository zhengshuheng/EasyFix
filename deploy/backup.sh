#!/usr/bin/env bash
# EasyFix 每日备份（cron.daily 调用，保留 7 天）
# 备份内容: SQLite 数据库 + 上传图片/音频 + 语音模型
set -euo pipefail

BACKUP_ROOT=/opt/easyfix-backups
APP_DIR=/opt/easyfix
STAMP=$(date +%Y%m%d_%H%M%S)

mkdir -p "$BACKUP_ROOT"

# 停止写入窗口内快照：SQLite 单文件，直接 tar 冷备即可（个人使用量级安全）
tar -czf "$BACKUP_ROOT/easyfix-$STAMP.tar.gz" \
    -C "$APP_DIR" \
    backend/easyfix_main.db \
    backend/uploads \
    backend/speech_models \
    2>/dev/null || true

# 保留最近 7 天
find "$BACKUP_ROOT" -name 'easyfix-*.tar.gz' -mtime +7 -delete

echo "$(date '+%F %T') EasyFix backup -> $BACKUP_ROOT/easyfix-$STAMP.tar.gz" >> /var/log/easyfix-backup.log
