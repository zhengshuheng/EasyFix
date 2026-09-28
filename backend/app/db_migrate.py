# -*- coding: utf-8 -*-
"""幂等 schema 迁移：为主库 / 模板库 / 各空间库补新增列。

背景：模型新增列后，create_all 只建缺失表、不改已有表；而模板库（trial_data/template.db）、
各空间库（trial_data/tenants/*.db）、主库（easyfix_main.db）都是既有库，需要逐个 ALTER 补列。

注意：主库的迁移不能只靠 main.py 里针对 engine 的 _ensure_column——
空间库是**独立文件**，不会跟着主库一起改，漏掉会出现
"no such column" 导致接口 500。
"""
import os
import re
import sqlite3

from sqlalchemy import create_engine


def _add_column_if_missing(db_path: str, table: str, column: str, ddl: str) -> bool:
    if not os.path.isfile(db_path):
        return False
    conn = sqlite3.connect(db_path)
    try:
        has_table = conn.execute(
            "SELECT 1 FROM sqlite_master WHERE type='table' AND name=?", (table,)
        ).fetchone()
        if not has_table:
            # 空间库没有 accounts 表等场景：跳过而不是 ALTER 报错刷屏
            return False
        cols = [r[1] for r in conn.execute(f"PRAGMA table_info({table})").fetchall()]
        if column in cols:
            return False
        conn.execute(f"ALTER TABLE {table} ADD COLUMN {column} {ddl}")
        conn.commit()
        print(f"[migrate] {os.path.basename(db_path)} {table}.{column} 已补充")
        return True
    except Exception as e:
        print(f"[migrate] {db_path} {table}.{column} ALTER 失败: {e}")
        return False
    finally:
        conn.close()


def _all_db_targets() -> list:
    """主库 + 模板库 + 全部空间库（去重）"""
    from app.config import get_settings
    from app.trial import TEMPLATE_DB_PATH, TENANTS_DIR

    targets = []
    url = get_settings().DATABASE_URL
    m = re.match(r"sqlite:///(.+)", url)
    if m:
        targets.append(os.path.abspath(m.group(1)))
    targets.append(TEMPLATE_DB_PATH)
    if os.path.isdir(TENANTS_DIR):
        targets += [
            os.path.join(TENANTS_DIR, f)
            for f in os.listdir(TENANTS_DIR)
            if f.endswith(".db")
        ]
    # 去重且保序
    seen = set()
    out = []
    for p in targets:
        rp = os.path.abspath(p)
        if rp not in seen:
            seen.add(rp)
            out.append(rp)
    return out


def ensure_ops_override_columns() -> None:
    """对主库 + 模板库 + 全部空间库幂等补 ops_override 列（布尔默认 0=跟随运营默认）。"""
    for p in _all_db_targets():
        _add_column_if_missing(p, "star_action", "ops_override", "BOOLEAN DEFAULT 0")
        _add_column_if_missing(p, "achievement", "ops_override", "BOOLEAN DEFAULT 0")


def ensure_word_seen_column() -> None:
    """对主库 + 模板库 + 全部空间库幂等补 word_progress.seen_at。

    seen_at = 今日任务学词卡翻到即标记的「看过」时间（含未答题）。
    用于把已看过的词移出新词池，避免"看了一遍没答题、下次点开又从头开始"。
    """
    for p in _all_db_targets():
        _add_column_if_missing(p, "word_progress", "seen_at", "DATETIME")


def ensure_account_space_key_column() -> None:
    """对主库 + 模板库幂等补 accounts.space_key（辅助家长账号绑定空间的 key）。

    空间库（tenants/*.db）没有 accounts 表，_add_column_if_missing 会安全跳过。
    主账号该列为空（按 username 查名下空间），辅助账号=家长中心添加的家长（绑定当前空间）。
    """
    for p in _all_db_targets():
        _add_column_if_missing(p, "accounts", "space_key", "VARCHAR(100)")


def ensure_assessment_specialty_column() -> None:
    """对主库 + 模板库 + 全部空间库幂等补 assessment_record.specialty（专项评测 key）。

    专项评测（/assessment/special/*）组卷时会向 assessment_record 写入 specialty，
    空间库是独立文件不会跟主库一起改——漏掉会 "no such column: assessment_record.specialty"
    导致专项评测/专项练习接口 500（2026-09-28 部署验证翻车）。
    """
    for p in _all_db_targets():
        _add_column_if_missing(p, "assessment_record", "specialty", "VARCHAR(50)")


# =====================================================================
# 空间库 schema 整体补齐（治本）：create_all 补缺失表 + 按主库清单补列
#
# 背景（2026-09-28 云端需加强无数据根因）：模板库/空间库是早期版本生成后
# 持久化复用的（remote_deploy.sh 挂载 trial_data 数据卷），新模型表/列
# （word_progress 四维列、word.mnemonic、users.enrollment_date、question 选项列…）
# 只在主库由 main.py _ensure_column / create_all 补齐，空间库只补过零星几列
# （seen_at/specialty/ops_override）。空间库 word_progress 缺列 → 复习提交/需加强/
# 今日任务接口 SELECT 全列 → OperationalError no such column → 500 → 列表空。
# 本地模板是新代码生成的所以正常，云端旧模板因此"本地正常、云端需加强没数据"。
# =====================================================================

# 与 main.py 主库 _ensure_column 清单保持一致；缺表时 _add_column_if_missing 安全跳过。
# （seen_at / specialty / ops_override / accounts.space_key 已有专门 ensure，不重复列出）
_COLUMN_MIGRATIONS = [
    # 练习/报告/错题
    ("practice_set_question", "student_answer", "student_answer TEXT"),
    ("error_book", "user_id", "user_id INTEGER"),
    ("learning_report", "user_id", "user_id INTEGER"),
    ("assessment_record", "questions", "questions TEXT"),
    ("assessment_record", "specialty", "specialty VARCHAR(50)"),
    ("practice_set", "user_id", "user_id INTEGER"),
    ("practice_set_question", "practice_question_id", "practice_question_id INTEGER"),
    ("word_review_session", "user_id", "user_id INTEGER"),
    ("word_review_log", "user_id", "user_id INTEGER"),
    ("word_review", "user_id", "user_id INTEGER"),
    ("practice_set", "show_score", "show_score BOOLEAN DEFAULT 1"),
    ("practice_set", "score_mode", "score_mode VARCHAR(20) DEFAULT 'default'"),
    ("practice_set", "show_ai_author", "show_ai_author BOOLEAN DEFAULT 0"),
    ("practice_set", "grammar_lesson_id", "grammar_lesson_id INTEGER"),
    ("practice_question", "visual", "visual TEXT"),
    # 单词：单元归属 / 记忆辅助 / 语境例句
    ("word", "unit", "unit INTEGER"),
    ("word", "unit_title", "unit_title VARCHAR(200)"),
    ("word", "phonetic_rule", "phonetic_rule TEXT"),
    ("word", "mnemonic", "mnemonic TEXT"),
    ("word", "word_root", "word_root VARCHAR(500)"),
    ("word", "related_words", "related_words TEXT"),
    ("word", "example_sentences", "example_sentences TEXT"),
    # 四维记忆模型：word_progress 分维度计数（认得/听得/说得/写得）
    ("word_progress", "recognize_count", "recognize_count INTEGER DEFAULT 0"),
    ("word_progress", "recognize_correct", "recognize_correct INTEGER DEFAULT 0"),
    ("word_progress", "listen_count", "listen_count INTEGER DEFAULT 0"),
    ("word_progress", "listen_correct", "listen_correct INTEGER DEFAULT 0"),
    ("word_progress", "speak_count", "speak_count INTEGER DEFAULT 0"),
    ("word_progress", "speak_correct", "speak_correct INTEGER DEFAULT 0"),
    ("word_progress", "write_count", "write_count INTEGER DEFAULT 0"),
    ("word_progress", "write_correct", "write_correct INTEGER DEFAULT 0"),
    # 小孩年级 / 入学日期
    ("users", "current_grade", "current_grade INTEGER DEFAULT 1"),
    ("users", "enrollment_date", "enrollment_date DATE"),
    # 题库选项结构（旧库 option_a..d 可能缺失）
    ("question", "question_type", "question_type VARCHAR(50)"),
    ("question", "question_category", "question_category VARCHAR(50)"),
    ("question", "option_a", "option_a TEXT"),
    ("question", "option_b", "option_b TEXT"),
    ("question", "option_c", "option_c TEXT"),
    ("question", "option_d", "option_d TEXT"),
    ("question", "source", "source VARCHAR(20)"),
    # 官网登录账号（空间库无 accounts 表时安全跳过；避免误判为"空间库不需要"）
    ("accounts", "role", "role VARCHAR(10) DEFAULT 'parent'"),
    ("accounts", "child_name", "child_name VARCHAR(50) DEFAULT ''"),
]


def ensure_tenant_schema() -> None:
    """对模板库 + 全部空间库幂等补齐 schema（治本，2026-09-28 云端需加强无数据修复）。

    两步，缺表/缺列都覆盖：
    1. Base.metadata.create_all —— 只建缺失表（word_progress / WordAttempt / 新表…），
       已有表不动、不碰数据；
    2. 按 _COLUMN_MIGRATIONS 补列 —— 与主库 main.py _ensure_column 清单一致。
    """
    from app.database import Base
    targets = _all_db_targets()

    # 1) 补缺失表
    for p in targets:
        if not os.path.isfile(p):
            continue
        try:
            engine = create_engine("sqlite:///" + p.replace("\\", "/"))
            Base.metadata.create_all(bind=engine)
            engine.dispose()
        except Exception as e:
            print(f"[migrate] {os.path.basename(p)} create_all 补表失败: {e}")

    # 2) 补缺失列
    for p in targets:
        for table, column, ddl in _COLUMN_MIGRATIONS:
            _add_column_if_missing(p, table, column, ddl)


def sync_helper_accounts_to_main(db) -> int:
    """幂等：把各空间库的存量「辅助家长」账号补齐到主库 accounts（官网登录依赖）。

    背景：家长中心「添加家长」旧版本只写空间库 users（role=admin、非主账号），
    官网登录查主库 accounts 查不到 → 登录不上。新版创建时已同步主库（users.py
    写 Account + space_key），但存量账号必须在这里启动时补录。

    判定：role='admin' 且 username != 该空间 registry 主账号名
    （兼容没有 is_owner 列的旧库；主账号按 registry spaces.username 识别）。
    幂等：主库已有同名账号则跳过（含与官网已注册账号重名的冲突账号）。
    返回补录数。
    """
    from app.models.account import Account
    from app.trial import TENANTS_DIR, REGISTRY_DB_PATH

    # registry：空间 key -> 主账号 username
    owner_by_key = {}
    if os.path.isfile(REGISTRY_DB_PATH):
        conn = sqlite3.connect(REGISTRY_DB_PATH)
        try:
            for key, username in conn.execute(
                "SELECT key, username FROM spaces"
            ).fetchall():
                owner_by_key[key] = username
        finally:
            conn.close()

    pending = []  # (space_key, username, password_hash)
    if os.path.isdir(TENANTS_DIR):
        for f in sorted(os.listdir(TENANTS_DIR)):
            if not f.endswith(".db"):
                continue
            key = f[:-3]
            owner = owner_by_key.get(key)
            if owner is None:
                continue
            conn = sqlite3.connect(os.path.join(TENANTS_DIR, f))
            try:
                try:
                    rows = conn.execute(
                        "SELECT username, password_hash FROM users WHERE role='admin'"
                    ).fetchall()
                except sqlite3.OperationalError:
                    rows = []
            finally:
                conn.close()
            for username, pw_hash in rows:
                if username == owner:
                    continue  # 主账号（registry 主账号名）
                if pw_hash:
                    pending.append((key, username, pw_hash))

    added = 0
    for key, username, pw_hash in pending:
        if db.query(Account).filter_by(username=username).first():
            continue  # 已存在（含冲突），跳过
        db.add(Account(
            username=username,
            password_hash=pw_hash,
            subscription_plan="free",
            role="parent",
            space_key=key,
        ))
        added += 1
    if added:
        db.commit()
        print(f"[migrate] 已补录 {added} 个存量辅助家长账号到官网登录（accounts）")
    return added

