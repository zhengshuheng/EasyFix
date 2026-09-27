# -*- coding: utf-8 -*-
"""试用体验：账号/空间分离 + 一个空间一个 SQLite db + 一个路由后缀 /{key}/

架构（2026-09 重构，用户拍板方案）：

- **账号**：正式库 `easyfix_main.db` accounts 表（Account 模型），全局身份 + 订阅状态。
  账号 token scope=account（见 utils/auth.get_current_account）。
- **空间**：账号名下的独立数据空间。registry.db `spaces` 表记录 key ↔ account_id ↔ db_path。
- **模板库** `trial_data/template.db`：预置完整表结构 + 基础数据 + 激励预设 +
  语法骨架 + 全局内容（题库/单词/拼读/阅读/知识点/奖品，来自正式库）+ 占位家长(admin, id=1)
  + 1 个演示小孩(child, id=2「体验小朋友」，题库 practice_question.user_id 归它)。
  仅首次启动生成一次；模板收敛逻辑确保恰好 1 个演示小孩（旧库多余小孩自动清理）。
- **创建空间 = 文件复制 + 角色化处理**：shutil.copy(template.db → tenants/{key}.db)，
  再把占位家长的 username/display_name 改成账号名；小孩处理——注册填了 child_name →
  体验小朋友改名为自己的小孩；没填 → 保持「体验小朋友」。秒级完成，不再每次跑建表/初始化。
  （密码不写入空间库：登录验证统一走 accounts 表）
- **体验期**：spaces.trial_end_at = 创建时间 + app_config.trial_days（NULL=正式不限）；升级置 NULL。
- **数据隔离**：middleware 读 X-Trial-Key → current_tenant ContextVar → get_db 分发（见 database.py）。
"""
import os
import secrets
import shutil
import sqlite3
import time
import uuid
from datetime import date, datetime, timedelta

from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.database import (
    Base, engine as default_engine, register_tenant_engine, get_db,
    current_tenant, set_current_tenant, tenant_factory, SessionLocal,
)
from app.utils.auth import hash_password, verify_password, create_token, get_current_account, validate_username, validate_password
from app.utils.timeutil import now_local
from app.models.user import User
from app.models.account import Account

router = APIRouter(prefix="/api/trial", tags=["试用体验"])

# ---- 试用数据目录 ----
TRIAL_DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "trial_data")
TENANTS_DIR = os.path.join(TRIAL_DATA_DIR, "tenants")
TEMPLATE_DB_PATH = os.path.join(TRIAL_DATA_DIR, "template.db")
REGISTRY_DB_PATH = os.path.join(TRIAL_DATA_DIR, "registry.db")

TEMPLATE_KEY = "__template__"            # 模板库的临时租户 key（仅生成阶段使用）
TEMPLATE_OWNER_USERNAME = "__template_owner__"
TEMPLATE_CHILD_USERNAME = "__template_child__"
DEFAULT_ENROLLMENT_DATE = "2025-09-01"   # 演示小孩默认一年级入学

# ---- 全局内容复制清单（A 类/共享内容：试用库开箱即有题库/单词/阅读）----
GLOBAL_CONTENT_TABLES = [
    "word",
    "word_tag",
    "phonics_rule",
    "reading_passage",
    "reading_question",
    "grammar_lesson",
    "knowledge_point",
    "reward",
]


# ==================== 注册表（独立 db registry.db，表 spaces） ====================

def _registry_conn() -> sqlite3.Connection:
    """registry.db 连接（幂等建表 + 旧表结构搬迁）。

    - 新表 `spaces`：key ↔ account_id ↔ username/child_name/db_path。
    - 旧 `tenants` 表存在时：把不含密码的列搬进 spaces（密码在 accounts 表，
      由 migrate_legacy_registry 迁移后才 DROP tenants）。
    """
    os.makedirs(TRIAL_DATA_DIR, exist_ok=True)
    conn = sqlite3.connect(REGISTRY_DB_PATH)
    conn.execute(
        """CREATE TABLE IF NOT EXISTS spaces (
            key          TEXT PRIMARY KEY,
            account_id   INTEGER,
            username     TEXT NOT NULL,
            child_name   TEXT DEFAULT '',
            db_path      TEXT NOT NULL,
            trial_end_at TEXT DEFAULT NULL,
            created_at   TEXT DEFAULT (datetime('now', 'localtime'))
        )"""
    )
    # 旧库补列：trial_end_at（体验期到期时间，NULL=正式不限制）
    cols = [r[1] for r in conn.execute("PRAGMA table_info(spaces)").fetchall()]
    if "trial_end_at" not in cols:
        conn.execute("ALTER TABLE spaces ADD COLUMN trial_end_at TEXT DEFAULT NULL")
    has_tenants = conn.execute(
        "SELECT 1 FROM sqlite_master WHERE type='table' AND name='tenants'"
    ).fetchone()
    if has_tenants:
        cnt = conn.execute("SELECT COUNT(*) FROM spaces").fetchone()[0]
        if cnt == 0:
            conn.execute(
                """INSERT INTO spaces (key, username, child_name, db_path, created_at)
                   SELECT key, username, child_name, db_path, created_at FROM tenants"""
            )
        # 不在此处 DROP tenants：等 migrate_legacy_registry 把密码迁入 accounts
    conn.commit()
    return conn


def migrate_legacy_registry(db: Session) -> int:
    """旧注册表迁移（幂等）：tenants（含 password_hash）→ spaces + accounts。

    在正式库 Session 上执行：逐条把旧租户建为 Account，回填 spaces.account_id，
    最后 DROP tenants。返回迁移条数。
    """
    conn = _registry_conn()
    try:
        has_tenants = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name='tenants'"
        ).fetchone()
        if not has_tenants:
            return 0
        rows = conn.execute(
            "SELECT key, username, password_hash, child_name, db_path, created_at FROM tenants"
        ).fetchall()
        migrated = 0
        for key, username, pw_hash, _child, _dbp, _ct in rows:
            account = db.query(Account).filter_by(username=username).first()
            if not account:
                account = Account(
                    username=username,
                    password_hash=pw_hash or hash_password("__legacy__"),
                    subscription_plan="free",
                )
                db.add(account)
                db.flush()
            conn.execute("UPDATE spaces SET account_id = ? WHERE key = ?", (account.id, key))
            migrated += 1
        db.commit()
        conn.execute("DROP TABLE tenants")
        conn.commit()
        if migrated:
            print(f"[trial] 旧注册表已迁移 {migrated} 个账号 → accounts + spaces")
        return migrated
    finally:
        conn.close()


def get_registered_user(username: str):
    """按用户名查空间记录（兼容旧函数签名），返回 (key, record dict) 或 (None, None)"""
    username = (username or "").strip()
    conn = _registry_conn()
    try:
        row = conn.execute(
            "SELECT key, username, child_name, db_path, created_at, trial_end_at"
            " FROM spaces WHERE username = ?", (username,)
        ).fetchone()
    finally:
        conn.close()
    if not row:
        return None, None
    cols = ("key", "username", "child_name", "db_path", "created_at", "trial_end_at")
    return row[0], dict(zip(cols, row))


def get_space_by_key(key: str) -> dict:
    """按空间 key 查记录；无则返回 None"""
    if not key:
        return None
    conn = _registry_conn()
    try:
        row = conn.execute(
            "SELECT key, username, child_name, db_path, created_at, trial_end_at"
            " FROM spaces WHERE key = ?", (key,)
        ).fetchone()
    finally:
        conn.close()
    if not row:
        return None
    cols = ("key", "username", "child_name", "db_path", "created_at", "trial_end_at")
    d = dict(zip(cols, row))
    d["url"] = f"/{d['key']}/"
    return d


def get_space_by_username(username) -> dict:
    """按账号名查名下空间（username 唯一，避免自增 id 复用/悬空误匹配）；无则返回 None"""
    if not username:
        return None
    conn = _registry_conn()
    try:
        row = conn.execute(
            "SELECT key, username, child_name, db_path, created_at, trial_end_at"
            " FROM spaces WHERE username = ? ORDER BY created_at LIMIT 1", (username,)
        ).fetchone()
    finally:
        conn.close()
    if not row:
        return None
    key, username_, child_name, db_path, created_at, trial_end_at = row
    return {
        "key": key,
        "url": f"/{key}/",
        "username": username_,
        "child_name": child_name,
        "db_path": db_path,
        "created_at": created_at,
        "trial_end_at": trial_end_at,
    }


def get_space_by_account(account_id) -> dict:
    """按账号查名下空间：先经 accounts 表取 username（自增 id 会被复用，悬空 id 不得误匹配空间）；
    辅助家长账号（space_key 非空）直接按绑定空间 key 查；账号记录不存在则返回 None。"""
    if not account_id:
        return None
    from app.models.account import Account
    db = SessionLocal()
    try:
        acct = db.query(Account).filter_by(id=account_id).first()
        if acct and acct.space_key:
            return get_space_by_key(acct.space_key)
        username = acct.username if acct else None
    finally:
        db.close()
    return get_space_by_username(username)


def issue_space_token_for_account(account_id) -> dict | None:
    """官网登录/注册共用：账号 → 名下空间 → 签发空间内对应家长账号 token。

    主账号 = 空间内同 username 的 admin（is_owner，历史行为不变）；
    辅助家长账号 = 家长中心添加的家长，space_key 绑定同一空间，这里按它的
    username 在租户里找到它自己签发（避免辅助账号拿主账号身份进空间）。
    查不到对应 User 时回退第一个 admin（兼容旧数据）。
    """
    record = get_space_by_account(account_id)
    if not record:
        return None
    from app.models.account import Account
    _db = SessionLocal()
    try:
        acct = _db.query(Account).filter_by(id=account_id).first()
        username = acct.username if acct else None
    finally:
        _db.close()
    key = record["key"]
    register_tenant_engine(key, record["db_path"])
    tf = tenant_factory(key)
    with tf() as db:
        user = (
            db.query(User).filter_by(username=username, role="admin").first()
            if username
            else None
        )
        if not user:
            user = db.query(User).filter_by(role="admin").order_by(User.id).first()
    if not user:
        return None
    return {
        "key": key,
        "url": record["url"],
        "token": create_token(user, persistent=True),
        "child_name": record["child_name"],
        "trial_end_at": record["trial_end_at"],
    }


def is_trial_key(key: str) -> bool:
    """判断路由后缀是否是已注册的试用空间 key"""
    if not key:
        return False
    conn = _registry_conn()
    try:
        row = conn.execute("SELECT 1 FROM spaces WHERE key = ?", (key,)).fetchone()
    finally:
        conn.close()
    return row is not None


def ensure_tenant_engine(key: str) -> bool:
    """确保租户引擎已注册（幂等）：从 registry 取 db_path，文件存在则注册。

    服务重启后进程内 _tenant_factories 为空，必须靠它恢复——否则带 X-Trial-Key
    的请求会静默回退正式库（数据泄漏）。middleware 校验后调用。返回是否可用。
    """
    if not key:
        return False
    if tenant_factory(key) is not None:
        return True
    record = get_space_by_key(key)
    if not record:
        return False
    db_path = record.get("db_path")
    if not db_path or not os.path.isfile(db_path):
        return False
    try:
        register_tenant_engine(key, db_path)
        return True
    except Exception as e:
        print(f"[trial] 注册租户引擎 {key} 失败: {e}")
        return False


def _save_space(key: str, account_id: int, username: str, child_name: str, db_path: str, trial_end_at: str = None) -> None:
    conn = _registry_conn()
    try:
        conn.execute(
            "INSERT OR REPLACE INTO spaces (key, account_id, username, child_name, db_path, trial_end_at)"
            " VALUES (?, ?, ?, ?, ?, ?)",
            (key, account_id, username, child_name, db_path, trial_end_at),
        )
        conn.commit()
    finally:
        conn.close()


def upgrade_account_spaces(account_id: int) -> int:
    """升级账号名下所有空间为正式版：trial_end_at=NULL（不再受体验期限制）。返回更新条数。"""
    if not account_id:
        return 0
    conn = _registry_conn()
    try:
        cur = conn.execute(
            "UPDATE spaces SET trial_end_at = NULL WHERE account_id = ?", (account_id,)
        )
        conn.commit()
        return cur.rowcount or 0
    finally:
        conn.close()


def _compute_trial_end_at() -> str:
    """按 app_config.trial_days 计算体验到期时间（本地时间字符串）。

    trial_days<=0 表示不限体验期 → 返回 None（=正式）。
    """
    from app.models.app_config import AppConfig
    days = 15
    try:
        db = SessionLocal()
        try:
            row = db.query(AppConfig).filter_by(key="trial_days").first()
            if row:
                days = int(str(row.value or 15).strip() or 15)
        finally:
            db.close()
    except Exception as e:
        print(f"[trial] 读取 trial_days 失败，用默认 15: {e}")
    if days <= 0:
        return None
    return (now_local() + timedelta(days=days)).strftime("%Y-%m-%d %H:%M:%S")


# ==================== 模板库生成（只跑一次） ====================

def copy_global_content(kid_id: int) -> None:
    """把正式库的共享内容复制到当前租户库（current_tenant 上下文内执行）。

    用 SQLAlchemy text 批量 INSERT，保留主键 id（子表外键引用依赖 id）。
    practice_question 特殊处理：user_id 改写为演示小孩、error_question_id 置 NULL。
    """
    key = current_tenant.get()
    if not key:
        return
    tf = tenant_factory(key)
    if tf is None:
        return

    def _copy_table(src_conn, dst_conn, table: str, rewrite: dict = None) -> int:
        rewrite = rewrite or {}
        cols = [r[1] for r in dst_conn.execute(text(f"PRAGMA table_info({table})")).fetchall()]
        if not cols:
            return 0
        rows = src_conn.execute(text(f"SELECT * FROM {table}")).mappings().all()
        if not rows:
            return 0
        batch = []
        for row in rows:
            row_dict = dict(row)
            data = {c: row_dict[c] for c in cols if c in row_dict}
            for col, val in rewrite.items():
                if col in data:
                    data[col] = val
            batch.append(data)
        if not batch:
            return 0
        placeholders = ", ".join(f":{c}" for c in batch[0])
        col_names = ", ".join(batch[0].keys())
        stmt = text(f"INSERT OR IGNORE INTO {table} ({col_names}) VALUES ({placeholders})")
        for i in range(0, len(batch), 500):
            dst_conn.execute(stmt, batch[i:i + 500])
        return len(batch)

    src = default_engine.connect()
    db = tf()
    try:
        dst_conn = db.connection()
        for table in GLOBAL_CONTENT_TABLES:
            try:
                _copy_table(src, dst_conn, table)
            except Exception as e:
                print(f"[trial] 复制表 {table} 跳过: {e}")
        try:
            _copy_table(src, dst_conn, "practice_question",
                        rewrite={"user_id": kid_id, "error_question_id": None})
        except Exception as e:
            print(f"[trial] 复制表 practice_question 跳过: {e}")
        db.commit()
    finally:
        db.close()
        src.close()


def _seed_demo_child(db: Session, display_name: str) -> User:
    """创建演示小孩（一年级入学，自动建各学科错题本）"""
    from app.routers.users import _ensure_default_error_books
    child = User(
        username=f"kid_{uuid.uuid4().hex[:10]}",
        display_name=(display_name or "体验小朋友").strip() or "体验小朋友",
        role="child",
        enrollment_date=date.fromisoformat(DEFAULT_ENROLLMENT_DATE),
    )
    db.add(child)
    db.commit()
    db.refresh(child)
    _ensure_default_error_books(db, child.id)
    return child


def _ensure_template_demo_children(db_path: str) -> None:
    """模板库幂等收敛：确保恰好 1 个演示小孩「体验小朋友」（id=2，带题库）。

    - 0 个：补插「体验小朋友」并归属全局题库（copy_global_content）
    - 多于 1 个：只保留第一个，删除其余（旧模板的 id=3「新同学」等）及其错题本
    """
    from app import database as db_mod
    try:
        register_tenant_engine(TEMPLATE_KEY, db_path)
    except Exception as e:
        print(f"[trial] 模板库收敛引擎注册失败: {e}")
        return
    try:
        tf = tenant_factory(TEMPLATE_KEY)
        with tf() as db:
            kids = db.query(User).filter_by(role="child").order_by(User.id).all()
            if len(kids) == 0:
                child = _seed_demo_child(db, "体验小朋友")
                copy_global_content(child.id)
                db.commit()
                print("[trial] 模板库已补插体验小朋友")
            elif len(kids) > 1:
                from app.models.error_book import ErrorBook
                for extra in kids[1:]:
                    db.query(ErrorBook).filter_by(user_id=extra.id).delete()
                    db.delete(extra)
                db.commit()
                print(f"[trial] 模板库已收敛演示小孩（保留 {kids[0].display_name}，删除 {len(kids) - 1} 个）")
    finally:
        db_mod._tenant_engines.pop(TEMPLATE_KEY, None)
        db_mod._tenant_factories.pop(TEMPLATE_KEY, None)


def _sync_template_grammar() -> None:
    """模板库语法教程与主库（ops 权威）对齐：ensure_template_db 每次调用时执行，
    保证新建空间复制出的 grammar_lesson 永远是最新教程内容（按 id upsert）。"""
    from app.services.grammar_sync import sync_grammar_sqlite
    if not os.path.isfile(TEMPLATE_DB_PATH):
        return
    try:
        r = sync_grammar_sqlite(TEMPLATE_DB_PATH)
        if r["updated"] or r["created"] or r["removed"]:
            print(f"[trial] 模板库语法教程已同步: {r}")
    except Exception as e:
        print(f"[trial] 模板库语法教程同步失败: {e}")


def ensure_template_db(force: bool = False) -> str:
    """确保模板库存在（幂等）。首次启动生成一次，之后直接复用。

    生成流程：建表 → 基础数据 → 激励预设 → 语法骨架 → 占位家长 + 演示小孩
    → 全局内容复制（题库/单词/阅读…）。耗时主要在 create_all（~10s），只跑一次。
    写临时文件后原子改名，避免并发启动时半成品被当模板用。
    已存在的模板库走幂等收敛：确保恰好 1 个演示小孩（旧库多余小孩自动清理）。
    """
    if os.path.isfile(TEMPLATE_DB_PATH) and not force:
        _ensure_template_demo_children(TEMPLATE_DB_PATH)
        _sync_template_grammar()  # 模板库教程与主库（ops 权威）对齐，新空间创建即带最新内容
        return TEMPLATE_DB_PATH

    # 清理上次可能残留的模板引擎缓存（指向已删除的临时文件）
    from app import database as db_mod
    db_mod._tenant_engines.pop(TEMPLATE_KEY, None)
    db_mod._tenant_factories.pop(TEMPLATE_KEY, None)

    os.makedirs(TRIAL_DATA_DIR, exist_ok=True)
    tmp_path = TEMPLATE_DB_PATH + ".tmp"
    if os.path.isfile(tmp_path):
        os.remove(tmp_path)
    if os.path.isfile(TEMPLATE_DB_PATH):
        os.remove(TEMPLATE_DB_PATH)

    template_engine = register_tenant_engine(TEMPLATE_KEY, tmp_path)
    Base.metadata.create_all(bind=template_engine)

    prev_tenant = current_tenant.get()
    set_current_tenant(TEMPLATE_KEY)
    try:
        from app.services.init_base_data import init_base_data
        from app.services.init_motivation_data import (
            init_preset_data, init_achievement_progress,
            init_achievement_configs, init_star_records_from_existing_data,
        )
        from app.services.grammar_skeleton import ensure_grammar_skeleton
        tf = tenant_factory(TEMPLATE_KEY)
        with tf() as db:
            init_base_data(db)
            init_preset_data(db)
            init_achievement_progress(db)
            init_star_records_from_existing_data(db)
            init_achievement_configs(db)
            ensure_grammar_skeleton(db)

            # 占位家长（id=1）+ 演示小孩（id=2，题库 user_id 归属）
            owner = User(
                username=TEMPLATE_OWNER_USERNAME,
                display_name="模板",
                role="admin",
                password_hash=hash_password("__template__"),
            )
            db.add(owner)
            db.commit()
            db.refresh(owner)
            # 只保留 1 个演示小孩「体验小朋友」（带题库）；不再创建「新同学」
            child = _seed_demo_child(db, "体验小朋友")
            copy_global_content(child.id)
    finally:
        set_current_tenant(prev_tenant)

    # WAL checkpoint 落盘 + 关闭引擎，确保复制出的库数据完整
    with tenant_factory(TEMPLATE_KEY)() as db:
        db.execute(text("PRAGMA wal_checkpoint(TRUNCATE)"))
    template_engine.dispose()
    # 模板已落盘，不再持有模板引擎缓存
    db_mod._tenant_engines.pop(TEMPLATE_KEY, None)
    db_mod._tenant_factories.pop(TEMPLATE_KEY, None)
    os.replace(tmp_path, TEMPLATE_DB_PATH)
    _sync_template_grammar()  # 模板库语法教程与主库对齐（copy_global_content 兜底）
    return TEMPLATE_DB_PATH


# ==================== 创建空间 ====================

def create_space_for_account(account_id: int, username: str, child_name: str = "", role: str = "parent", password_hash: str = "") -> tuple:
    """为账号创建体验空间：复制模板库 + 写入账号名/孩子昵称。返回 (key, record dict)。

    角色处理（模板库含 1 个演示小孩「体验小朋友」带题库）：
    - parent（家长）：注册填了 child_name → 体验小朋友改名为自己的小孩；没填 → 保持「体验小朋友」
    - org（机构）：保持「体验小朋友」
    - 兜底：模板若仍含多余小孩（旧模板复制），收敛为 1 个
    快路径：文件复制（秒级）→ UPDATE 占位家长 → 处理小孩 → registry.db 记录。
    password_hash：官网账号密码哈希（同一 hash_password 算法），写入空间库 admin，
    使「官网账号 = 空间第一个家长」——家长中心用官网账号密码即可登录（不再用模板 __template__ 密码）。
    """
    ensure_template_db()
    key = secrets.token_urlsafe(10)
    os.makedirs(TENANTS_DIR, exist_ok=True)
    db_path = os.path.join(TENANTS_DIR, f"{key}.db")
    shutil.copy(TEMPLATE_DB_PATH, db_path)

    register_tenant_engine(key, db_path)
    tf = tenant_factory(key)
    with tf() as db:
        owner = db.query(User).filter_by(role="admin").order_by(User.id).first()
        owner.username = username
        owner.display_name = username
        owner.is_owner = True  # 主账号 = 官网注册家长，每空间仅 1 个，不可删除
        if password_hash:
            owner.password_hash = password_hash
        kids = db.query(User).filter_by(role="child").order_by(User.id).all()
        if kids:
            # 新模板只含 1 个体验小朋友：改名自己的小孩（注册填了）或保持体验小朋友
            kids[0].display_name = (child_name or "体验小朋友").strip() or "体验小朋友"
            # 兜底：旧模板复制仍带多余小孩时收敛为 1 个（清其错题本）
            if len(kids) > 1:
                from app.models.error_book import ErrorBook
                for extra in kids[1:]:
                    db.query(ErrorBook).filter_by(user_id=extra.id).delete()
                    db.delete(extra)
        db.commit()

    trial_end_at = _compute_trial_end_at()
    _save_space(key, account_id, username, (child_name or "").strip(), db_path, trial_end_at)
    record = {
        "username": username,
        "child_name": (child_name or "").strip(),
        "db_path": db_path,
        "account_id": account_id,
        "trial_end_at": trial_end_at,
    }
    return key, record


def delete_space(key: str) -> None:
    """删除一个体验空间：清理引擎缓存（dispose 释放连接池句柄）+ 删除 db 文件 + 注册表记录"""
    from app import database as db_mod
    conn = _registry_conn()
    try:
        row = conn.execute("SELECT db_path FROM spaces WHERE key = ?", (key,)).fetchone()
        conn.execute("DELETE FROM spaces WHERE key = ?", (key,))
        conn.commit()
    finally:
        conn.close()
    eng = db_mod._tenant_engines.pop(key, None)
    db_mod._tenant_factories.pop(key, None)
    if eng is not None:
        # dispose 关闭连接池底层连接，Windows 下否则文件被句柄占用无法删除
        try:
            eng.dispose()
        except Exception as e:
            print(f"[trial] dispose 引擎 {key} 失败: {e}")
    if row:
        base = row[0]
        failed = []
        for suffix in ("", "-wal", "-shm"):
            target = base + suffix
            if not os.path.isfile(target):
                continue
            # Windows 句柄释放延迟：先重试一次
            try:
                os.remove(target)
            except OSError:
                try:
                    time.sleep(0.5)
                    os.remove(target)
                except OSError as e:
                    failed.append(os.path.basename(target))
                    print(f"[trial] 删除 {target} 失败: {e}")
        if failed:
            raise RuntimeError(f"空间 db 文件删除失败（可能被占用）: {', '.join(failed)}；"
                               f"registry 记录已删除，可稍后手动清理 {os.path.dirname(base) or '.'}")


# ==================== API ====================

class TrialRegisterRequest(BaseModel):
    username: str
    password: str
    child_name: str = ""
    role: str = "parent"  # parent / org


class TrialLoginRequest(BaseModel):
    username: str
    password: str


class TrialSpaceRequest(BaseModel):
    child_name: str = ""


def _trial_user_dict(user: User) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "display_name": user.display_name or user.username,
        "role": user.role,
    }


def _open_tenant_admin(key: str, db_path: str):
    """打开租户引擎并返回家长用户（旧注册/登录共用：返回空间内 User token 兼容旧前端）"""
    register_tenant_engine(key, db_path)
    tf = tenant_factory(key)
    with tf() as db:
        return db.query(User).filter_by(role="admin").order_by(User.id).first()


def _ensure_account(db: Session, username: str, password: str) -> Account:
    """注册/登录共用：按用户名取账号；不存在则创建（注册语义）。密码校验交给调用方。"""
    account = db.query(Account).filter_by(username=username).first()
    if account:
        return account
    account = Account(
        username=username,
        password_hash=hash_password(password),
        subscription_plan="free",
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    return account


@router.post("/register")
def trial_register(data: TrialRegisterRequest, db: Session = Depends(get_db)):
    """【兼容旧版】注册 = 建账号 + 建空间 一步到位。

    返回空间内 User token（旧前端 X-Trial-Key + Bearer 用）；官网新流程请用
    /api/auth/register + /api/trial/spaces（账号/空间分离）。
    """
    username = (data.username or "").strip()
    password = data.password or ""
    err = validate_username(username)
    if err:
        raise HTTPException(status_code=400, detail=err)
    err = validate_password(username, password)
    if err:
        raise HTTPException(status_code=400, detail=err)
    if db.query(Account).filter_by(username=username).first():
        raise HTTPException(status_code=400, detail="该用户名已注册试用，请直接登录")
    account = _ensure_account(db, username, password)
    role = (data.role or "parent").strip().lower()
    if role not in ("parent", "org"):
        role = "parent"
    key, record = create_space_for_account(
        account.id, username, (data.child_name or "").strip(), role,
        password_hash=account.password_hash,
    )
    admin = _open_tenant_admin(key, record["db_path"])
    token = create_token(admin, persistent=True) if admin else None
    return {
        "key": key,
        "url": f"/{key}/",
        "token": token,
        "user": _trial_user_dict(admin) if admin else None,
        "message": "注册成功，开始体验吧！",
    }


@router.post("/login")
def trial_login(data: TrialLoginRequest, db: Session = Depends(get_db)):
    """【兼容旧版】试用登录：账号验证（accounts 表）+ 找回名下空间。

    返回空间内 User token（旧前端）；官网新流程请用 /api/auth/login。
    """
    username = (data.username or "").strip()
    account = db.query(Account).filter_by(username=username).first()
    if not account or not verify_password(data.password or "", account.password_hash):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    key, record = get_registered_user(username)
    if not key or not record:
        raise HTTPException(status_code=404, detail="该账号还没有体验空间，请先注册体验")
    admin = _open_tenant_admin(key, record["db_path"])
    token = create_token(admin, persistent=True) if admin else None
    return {
        "key": key,
        "url": f"/{key}/",
        "token": token,
        "user": _trial_user_dict(admin) if admin else None,
        "message": "登录成功，欢迎回来！",
    }


@router.post("/spaces")
def create_my_space(
    data: TrialSpaceRequest = TrialSpaceRequest(),
    account: Account = Depends(get_current_account),
):
    """当前账号创建体验空间（1 账号 1 空间；已存在则返回已有）"""
    existing = get_space_by_account(account.id)
    if existing:
        return {
            "key": existing["key"],
            "url": existing["url"],
            "child_name": existing["child_name"],
            "space_token": (issue_space_token_for_account(account.id) or {}).get("token"),
            "message": "已有体验空间，直接进入",
        }
    key, record = create_space_for_account(
        account.id, account.username,
        (data.child_name or "").strip() or (account.child_name or "").strip(),
        account.role,
        password_hash=account.password_hash,
    )
    return {
        "key": key,
        "url": f"/{key}/",
        "child_name": record["child_name"],
        "space_token": (issue_space_token_for_account(account.id) or {}).get("token"),
        "message": "体验空间已创建",
    }


@router.post("/spaces/reset")
def reset_my_space(
    data: TrialSpaceRequest = TrialSpaceRequest(),
    account: Account = Depends(get_current_account),
):
    """重置体验空间：删旧库重建（账号保留；原空间数据不可恢复）"""
    existing = get_space_by_account(account.id)
    if existing:
        delete_space(existing["key"])
    key, record = create_space_for_account(
        account.id, account.username,
        (data.child_name or "").strip() or (account.child_name or "").strip(),
        account.role,
        password_hash=account.password_hash,
    )
    return {
        "key": key,
        "url": f"/{key}/",
        "child_name": record["child_name"],
        "message": "体验空间已重置",
    }


@router.get("/status")
def trial_status(
    x_trial_key: str = Header(default="", alias="X-Trial-Key"),
):
    """体验空间状态：剩余天数 / 是否过期 / 是否正式版 + 价格配置。

    空间内前端（dist-trial）顶部倒计时条与到期引导用；X-Trial-Key 由前端自动带。
    trial_end_at=NULL = 正式版（升级后），不受体验期限制。
    注意：不能用 Depends(get_db) 读配置——带 X-Trial-Key 时 get_db 分发到空间库，
    app_config 在**主库**，须用 SessionLocal 直连主库读。
    """
    record = get_space_by_key(x_trial_key) if x_trial_key else None
    if not record:
        raise HTTPException(status_code=404, detail="空间不存在或 X-Trial-Key 无效")

    from app.config_api import get_config_map
    db = SessionLocal()
    try:
        cfg = get_config_map(db)
    finally:
        db.close()
    trial_days = int(str(cfg.get("trial_days") or 0) or 0)

    end = record.get("trial_end_at")
    is_pro = not end
    expired = False
    days_left = None
    if end:
        try:
            end_dt = datetime.strptime(end, "%Y-%m-%d %H:%M:%S")
            now = now_local()
            expired = now > end_dt
            days_left = max(0, (end_dt.date() - now.date()).days)
        except ValueError:
            expired = False

    return {
        "space": {
            "key": record["key"],
            "username": record["username"],
            "child_name": record["child_name"],
            "created_at": record["created_at"],
        },
        "trial": {
            "trial_days": trial_days,
            "expires_at": end,
            "days_left": days_left,
            "expired": expired,
            "is_pro": is_pro,
        },
        "config": {
            "online_price": cfg.get("online_price", ""),
            "local_price": cfg.get("local_price", ""),
            "local_download_url": cfg.get("local_download_url", ""),
            "local_guide_url": cfg.get("local_guide_url", ""),
        },
    }
