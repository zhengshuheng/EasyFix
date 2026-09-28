# -*- coding: utf-8 -*-
"""语法教程同步：主库（ops 权威）→ 空间库 / 模板库。

定位：语法知识点与教程内容由运营中心统一维护（主库 grammar_lesson = 权威）。
- 空间创建：模板库从主库复制 grammar_lesson（copy_global_content 保留主键 id）→ 新空间自动带最新教程；
- 更新逻辑：本模块按 id upsert（含内容字段），主库移除的点在目标库软删，保证全空间列表与内容一致；
- 固化：空间端写接口已禁用（routers/grammar.py 返回 403），家长只读。

提供两个入口：
- sync_grammar_from_main(target_db)：SQLAlchemy session 版（空间端 /api/grammar/sync-tutorials 用）；
- sync_grammar_sqlite(db_path)：sqlite3 直写版（ops 批量推送全部空间/模板库用）。
"""
import sqlite3
from typing import List, Optional

from app.database import SessionLocal
from app.models.grammar import GrammarLesson
from app.models.subject import Subject

# 同步的字段（id 为匹配锚，不更新）
_SYNC_FIELDS = [
    "category", "title", "grade", "semester", "summary", "content_md",
    "examples", "common_mistakes", "mnemonic", "order_index", "source",
]


def _main_rows(db) -> List[GrammarLesson]:
    return (
        db.query(GrammarLesson)
        .filter(GrammarLesson.deleted == False)  # noqa: E712
        .order_by(GrammarLesson.id)
        .all()
    )


def _load_main_rows(main_rows: Optional[List[GrammarLesson]]) -> List[GrammarLesson]:
    if main_rows is not None:
        return main_rows
    db = SessionLocal()
    try:
        return _main_rows(db)
    finally:
        db.close()


def sync_grammar_from_main(target_db, main_rows: Optional[List[GrammarLesson]] = None) -> dict:
    """SQLAlchemy 版：把主库教程同步进目标租户库（按 id upsert + 软删多余点）。

    保留主键 id（grammar_progress / practice_set.grammar_lesson_id 引用不失效）；
    subject_id 用目标库「英语」学科 id，避免跨库 id 不一致。
    """
    rows = _load_main_rows(main_rows)
    if not rows:
        return {"created": 0, "updated": 0, "removed": 0}

    eng = target_db.query(Subject).filter(Subject.name == "英语").first()
    subject_id = eng.id if eng else rows[0].subject_id

    target_map = {l.id: l for l in target_db.query(GrammarLesson).all()}
    created = updated = 0
    for mr in rows:
        t = target_map.get(mr.id)
        if t is None:
            t = GrammarLesson(id=mr.id, subject_id=subject_id)
            target_db.add(t)
            created += 1
        for f in _SYNC_FIELDS:
            setattr(t, f, getattr(mr, f))
        t.subject_id = subject_id
        t.deleted = False
        updated += 1

    main_ids = {mr.id for mr in rows}
    removed = 0
    for tid, t in target_map.items():
        if tid not in main_ids and not t.deleted:
            t.deleted = True
            removed += 1

    target_db.commit()
    return {"created": created, "updated": updated, "removed": removed}


def sync_grammar_sqlite(db_path: str, main_rows: Optional[List[GrammarLesson]] = None) -> dict:
    """sqlite3 直写版：ops 批量推送 / 模板库收敛用（目标库可能正被引擎使用，WAL 并发安全）。"""
    rows = _load_main_rows(main_rows)
    if not rows:
        return {"created": 0, "updated": 0, "removed": 0}

    conn = sqlite3.connect(db_path)
    try:
        cur = conn.cursor()
        eng = cur.execute("select id from subject where name='英语' limit 1").fetchone()
        subject_id = eng[0] if eng else rows[0].subject_id
        existing = {r[0]: r[1] for r in cur.execute("select id, deleted from grammar_lesson").fetchall()}

        created = updated = 0
        for mr in rows:
            vals = (
                mr.category, mr.title, mr.grade, mr.semester, mr.summary,
                mr.content_md, mr.examples, mr.common_mistakes, mr.mnemonic,
                mr.order_index, mr.source, subject_id,
            )
            if mr.id in existing:
                cur.execute(
                    "update grammar_lesson set category=?, title=?, grade=?, semester=?, "
                    "summary=?, content_md=?, examples=?, common_mistakes=?, mnemonic=?, "
                    "order_index=?, source=?, subject_id=?, deleted=0 where id=?",
                    vals + (mr.id,),
                )
                updated += 1
            else:
                cur.execute(
                    "insert into grammar_lesson (id, subject_id, category, title, grade, semester, "
                    "summary, content_md, examples, common_mistakes, mnemonic, order_index, source, deleted) "
                    "values (?,?,?,?,?,?,?,?,?,?,?,?,?,0)",
                    (mr.id, subject_id, mr.category, mr.title, mr.grade, mr.semester,
                     mr.summary, mr.content_md, mr.examples, mr.common_mistakes,
                     mr.mnemonic, mr.order_index, mr.source),
                )
                created += 1

        main_ids = {mr.id for mr in rows}
        removed = 0
        for tid, tdel in existing.items():
            if tid not in main_ids and not tdel:
                cur.execute("update grammar_lesson set deleted=1 where id=?", (tid,))
                removed += 1

        conn.commit()
        return {"created": created, "updated": updated, "removed": removed}
    finally:
        conn.close()
