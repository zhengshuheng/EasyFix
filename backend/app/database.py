import contextvars
import os

from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.config import get_settings

settings = get_settings()

connect_args = {}
if settings.DB_TYPE == "sqlite":
    connect_args = {"check_same_thread": False}
elif settings.DB_TYPE == "mysql":
    connect_args = {"charset": "utf8mb4", "init_command": "SET NAMES utf8mb4"}
elif settings.DB_TYPE in ("postgres", "postgresql"):
    connect_args = {"connect_timeout": 10}

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_recycle=3600,
    echo=False,
    connect_args=connect_args
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# ============ 试用租户机制（每用户独立 SQLite）============
# 试用空间 = 一个租户 key ↔ 一个独立 db 文件。请求带 X-Trial-Key 时，
# get_db() 返回该租户的 SessionLocal，业务路由（Depends(get_db)）零改动即隔离。
# 无租户上下文 → 默认库（正式空间），完全向后兼容。
current_tenant = contextvars.ContextVar("trial_tenant", default=None)

# 租户注册表：key -> (engine, sessionmaker)。注册时登记，get_db 惰性取用。
_tenant_engines = {}
_tenant_factories = {}


def register_tenant_engine(key: str, db_path: str):
    """登记一个租户引擎（注册试用账号时调用；重复登记直接返回已有 engine）。

    db_path 建议绝对路径（SQLite 路径相对 cwd 的坑，见 AI_CONTEXT）。
    """
    key = str(key)
    if key in _tenant_factories:
        return _tenant_engines[key]
    abs_path = os.path.abspath(db_path)
    te = create_engine(
        f"sqlite:///{abs_path}",
        pool_pre_ping=True,
        pool_recycle=3600,
        connect_args={"check_same_thread": False},
    )

    # SQLite 性能优化：WAL 并发读写 + 降低每次提交的 fsync 开销。
    # 注册时 create_all 建 80+ 张表，逐表 DDL 提交是主要耗时（实测 ~10s），
    # 设置后建表+初始化可降到 1-2s。
    @event.listens_for(te, "connect")
    def _set_sqlite_pragmas(dbapi_conn, connection_record):
        cur = dbapi_conn.cursor()
        try:
            cur.execute("PRAGMA journal_mode=WAL")
            cur.execute("PRAGMA synchronous=NORMAL")
        except Exception:
            pass
        finally:
            cur.close()

    tf = sessionmaker(autocommit=False, autoflush=False, bind=te)
    _tenant_engines[key] = te
    _tenant_factories[key] = tf
    return te


def tenant_factory(key: str):
    """返回租户 sessionmaker（未登记返回 None）"""
    return _tenant_factories.get(str(key))


def set_current_tenant(key):
    """设置当前请求的租户上下文；返回 reset token（中间件 finally 里 reset）。"""
    return current_tenant.set(str(key) if key else None)


def get_db():
    """数据库会话依赖：按当前租户上下文分发（无租户 → 默认库）。

    同步生成器依赖在 FastAPI 线程池执行，anyio 会拷贝 contextvars，
    中间件里 set_current_tenant 的值在线程中可读。
    """
    key = current_tenant.get()
    factory = tenant_factory(key) if key else None
    if factory is not None:
        db = factory()
        try:
            yield db
        finally:
            db.close()
        return
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
