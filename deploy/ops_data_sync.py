# -*- coding: utf-8 -*-
"""
容器内执行：把 /data/ops_data.sql（本地主库导出的 ops 权威数据）
按 id 幂等 upsert 进云端主库 DB_PATH（挂载卷 /data/easyfix_main.db）。

由 deploy/remote_deploy.sh 在容器启动、健康检查通过后调用：
    docker exec easyfix python3 /data/ops_data_sync.py

只更新配置表（语法教程/激励规则/成就），不触碰空间/用户/错题等真实数据。
"""
import os
import sqlite3
import sys

SQL_FILE = os.environ.get("OPS_SQL_FILE", "/data/ops_data.sql")
DB_PATH = os.environ.get("DB_PATH", "/data/easyfix_main.db")


def main() -> int:
    if not os.path.isfile(SQL_FILE):
        print("!! 未找到 %s，跳过 ops 数据同步" % SQL_FILE, file=sys.stderr)
        return 1
    if not os.path.isfile(DB_PATH):
        print("!! 云端主库不存在 %s，跳过 ops 数据同步" % DB_PATH, file=sys.stderr)
        return 1
    with open(SQL_FILE, "r", encoding="utf-8") as f:
        sql = f.read()
    con = sqlite3.connect(DB_PATH)
    try:
        con.executescript(sql)
        con.commit()
    finally:
        con.close()
    n = sql.count("ON CONFLICT(id)")
    print(">>> ops 数据同步完成：%d 条 upsert 已写入 %s" % (n, DB_PATH))
    return 0


if __name__ == "__main__":
    sys.exit(main())
