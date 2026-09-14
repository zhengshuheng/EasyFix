"""从 MySQL 迁移到 PostgreSQL，并确保 easyfix 库与表存在"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

PG = {
    "host": "localhost",
    "port": 5432,
    "user": "postgres",
    "password": "lingxi520",
    "dbname": "easyfix",
}


def ensure_database():
    conn = psycopg2.connect(
        host=PG["host"], port=PG["port"], user=PG["user"],
        password=PG["password"], dbname="postgres", connect_timeout=10,
    )
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()
    cur.execute("SELECT 1 FROM pg_database WHERE datname=%s", (PG["dbname"],))
    if not cur.fetchone():
        cur.execute(f'CREATE DATABASE "{PG["dbname"]}" ENCODING \'UTF8\'')
        print(f"created database {PG['dbname']}")
    else:
        print(f"database {PG['dbname']} exists")
    cur.close()
    conn.close()


def ensure_tables():
    # 强制使用 postgres 配置创建表
    os.environ["DB_TYPE"] = "postgres"
    os.environ["DB_HOST"] = PG["host"]
    os.environ["DB_PORT"] = str(PG["port"])
    os.environ["DB_USER"] = PG["user"]
    os.environ["DB_PASSWORD"] = PG["password"]
    os.environ["DB_NAME"] = PG["dbname"]

    # 清掉 settings 缓存
    from app.config import get_settings
    get_settings.cache_clear()

    from app.database import Base, engine
    import app.models  # noqa: F401 注册模型

    Base.metadata.create_all(bind=engine)
    print("tables ensured on", engine.url.render_as_string(hide_password=True))


if __name__ == "__main__":
    ensure_database()
    ensure_tables()
