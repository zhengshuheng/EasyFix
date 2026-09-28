"""Ops 数据服务：主库 ops 仓库 → 用户空间库同步

- ops 数据统一存主库（ops_knowledge_point / ops_word），由 Ops 后台维护准确性。
- 用户空间只读同步：按 (版本, 年级, 册次) 全量替换空间库对应数据（edition_key 标记），
  幂等、可重复、不会与旧导入叠加翻倍。
- 同步状态记录在主库 space_sync_state（空间库无 app_config 表）。
"""
from typing import List, Optional

from sqlalchemy import func

from app.database import SessionLocal
from app.models import KnowledgePoint, OpsKnowledgePoint, OpsWord, SpaceSyncState, Subject, Word
from app.models.ops_data import OpsEdition, ensure_ops_tables
from app.services.textbook_service import get_or_create_subject


# ---------------------------------------------------------------- 目录/计数

def get_ops_catalog() -> dict:
    """ops 仓库目录：科目 → 版本 → 年级×册次 → {kp, words} 计数"""
    ensure_ops_tables()
    db = SessionLocal()
    try:
        kp_rows = db.query(
            OpsKnowledgePoint.subject, OpsKnowledgePoint.version,
            OpsKnowledgePoint.grade, OpsKnowledgePoint.semester,
            func.count(OpsKnowledgePoint.id),
        ).filter(OpsKnowledgePoint.deleted == False).group_by(
            OpsKnowledgePoint.subject, OpsKnowledgePoint.version,
            OpsKnowledgePoint.grade, OpsKnowledgePoint.semester,
        ).all()
        word_rows = db.query(
            OpsWord.version, OpsWord.grade, OpsWord.semester,
            func.count(OpsWord.id),
        ).filter(OpsWord.deleted == False).group_by(
            OpsWord.version, OpsWord.grade, OpsWord.semester,
        ).all()
        subjects: dict = {}
        for subject, version, grade, semester, cnt in kp_rows:
            s = subjects.setdefault(subject, {})
            v = s.setdefault(version, {})
            v[f"{grade}-{semester}"] = {"kp": cnt, "words": 0}
        # 单词按版本合并进科目目录（版本名与知识点一致时自然并入；新版本补进英语）
        word_versions: dict = {}
        for version, grade, semester, cnt in word_rows:
            word_versions.setdefault(version, {})[f"{grade}-{semester}"] = cnt
        existing_versions = {ver for s in subjects.values() for ver in s}
        for version, books in word_versions.items():
            if version in existing_versions:
                for subject, s in subjects.items():
                    if version in s:
                        for k, cnt in books.items():
                            s[version][k] = {"kp": s[version].get(k, {}).get("kp", 0),
                                             "words": cnt}
            else:
                s = subjects.setdefault("英语", {})
                s[version] = {k: {"kp": 0, "words": cnt} for k, cnt in books.items()}
        # 教材版本表（ops_edition）融合：未删未禁的版本并入目录（无数据时 books 为空，
        # 保证「先建版本、后导数据」时版本出现在下拉）
        for e in db.query(OpsEdition).filter(
                OpsEdition.deleted == False, OpsEdition.enabled == True).all():
            s = subjects.setdefault(e.subject, {})
            s.setdefault(e.name, {})
        return {"subjects": subjects}
    finally:
        db.close()


def get_ops_editions() -> list:
    """版本列表 + 每版本统计（册数/知识点数/单词数），按学科、名称排序"""
    ensure_ops_tables()
    db = SessionLocal()
    try:
        rows = db.query(OpsEdition).filter(OpsEdition.deleted == False).order_by(
            OpsEdition.subject, OpsEdition.name).all()
        kp_cnt = {}
        for r in db.query(
                OpsKnowledgePoint.subject, OpsKnowledgePoint.version,
                func.count(OpsKnowledgePoint.id),
        ).filter(OpsKnowledgePoint.deleted == False).group_by(
                OpsKnowledgePoint.subject, OpsKnowledgePoint.version).all():
            kp_cnt[(r[0], r[1])] = r[2]
        word_cnt = {}
        for r in db.query(
                OpsWord.version, func.count(OpsWord.id),
        ).filter(OpsWord.deleted == False).group_by(OpsWord.version).all():
            word_cnt[r[0]] = r[1]
        books_cnt = {}
        for r in db.query(
                OpsKnowledgePoint.subject, OpsKnowledgePoint.version,
                func.count(func.distinct(OpsKnowledgePoint.grade * 10 + OpsKnowledgePoint.semester)),
        ).filter(OpsKnowledgePoint.deleted == False).group_by(
                OpsKnowledgePoint.subject, OpsKnowledgePoint.version).all():
            books_cnt[(r[0], r[1])] = r[2]
        registered = {(r.subject, r.name) for r in rows}
        out = [{
            "id": r.id, "subject": r.subject, "name": r.name,
            "description": r.description or "", "enabled": bool(r.enabled),
            "registered": True,
            "books": books_cnt.get((r.subject, r.name), 0),
            "kp": kp_cnt.get((r.subject, r.name), 0),
            "words": word_cnt.get(r.name, 0),
        } for r in rows]
        # 融合数据中实际存在但未登记到版本表的 学科+版本（历史导入产生），
        # 让版本页成为全量权威视图：可一键登记或删除（连带删数据）
        data_versions = set(kp_cnt.keys())
        for version in word_cnt:
            data_versions.add(("英语", version))
        for subject, name in sorted(data_versions - registered):
            out.append({
                "id": None, "subject": subject, "name": name,
                "description": "", "enabled": True,
                "registered": False,
                "books": books_cnt.get((subject, name), 0),
                "kp": kp_cnt.get((subject, name), 0),
                "words": word_cnt.get(name, 0),
            })
        return out
    finally:
        db.close()


def register_ops_edition(subject: str, name: str, description: Optional[str] = None) -> dict:
    """把数据中已存在的 学科+版本 登记进版本表（幂等），返回登记记录"""
    ensure_ops_tables()
    db = SessionLocal()
    try:
        row = db.query(OpsEdition).filter(
            OpsEdition.subject == subject, OpsEdition.name == name,
            OpsEdition.deleted == False).first()
        if row is None:
            row = OpsEdition(subject=subject, name=name,
                             description=description or "（登记自历史数据）", enabled=True)
            db.add(row)
            db.commit()
            db.refresh(row)
        return {"id": row.id, "subject": row.subject, "name": row.name}
    finally:
        db.close()


def delete_ops_edition_data(subject: str, name: str) -> dict:
    """删除 学科+版本 下全部数据（知识点+单词），软删；版本表记录不受影响"""
    ensure_ops_tables()
    db = SessionLocal()
    try:
        kp = db.query(OpsKnowledgePoint).filter(
            OpsKnowledgePoint.subject == subject,
            OpsKnowledgePoint.version == name,
            OpsKnowledgePoint.deleted == False).all()
        for r in kp:
            r.deleted = True
        words = db.query(OpsWord).filter(
            OpsWord.version == name, OpsWord.deleted == False).all()
        for r in words:
            r.deleted = True
        db.commit()
        return {"kp": len(kp), "words": len(words)}
    finally:
        db.close()


def get_ops_kp(subject: str, version: str, grade: Optional[int] = None,
               semester: Optional[int] = None) -> List[OpsKnowledgePoint]:
    db = SessionLocal()
    try:
        q = db.query(OpsKnowledgePoint).filter(
            OpsKnowledgePoint.deleted == False,
            OpsKnowledgePoint.subject == subject,
            OpsKnowledgePoint.version == version,
        )
        if grade is not None:
            q = q.filter(OpsKnowledgePoint.grade == grade)
        if semester is not None:
            q = q.filter(OpsKnowledgePoint.semester == semester)
        return q.order_by(OpsKnowledgePoint.grade, OpsKnowledgePoint.semester,
                          OpsKnowledgePoint.chapter, OpsKnowledgePoint.id).all()
    finally:
        db.close()


def get_ops_words(version: str, grade: Optional[int] = None,
                  semester: Optional[int] = None) -> List[OpsWord]:
    db = SessionLocal()
    try:
        q = db.query(OpsWord).filter(
            OpsWord.deleted == False,
            OpsWord.version == version,
        )
        if grade is not None:
            q = q.filter(OpsWord.grade == grade)
        if semester is not None:
            q = q.filter(OpsWord.semester == semester)
        return q.order_by(OpsWord.grade, OpsWord.semester, OpsWord.unit,
                          OpsWord.id).all()
    finally:
        db.close()


# ---------------------------------------------------------------- 空间库同步

def _current_edition(db, space_key, data_type, version, grade=0, semester=0) -> Optional[str]:
    row = db.query(SpaceSyncState).filter(
        SpaceSyncState.space_key == space_key,
        SpaceSyncState.data_type == data_type,
        SpaceSyncState.version == version,
        SpaceSyncState.grade == grade,
        SpaceSyncState.semester == semester,
    ).first()
    return row.edition if row else None


def _upsert_sync_state(db, space_key, data_type, version, grade, semester, edition) -> None:
    row = db.query(SpaceSyncState).filter(
        SpaceSyncState.space_key == space_key,
        SpaceSyncState.data_type == data_type,
        SpaceSyncState.version == version,
        SpaceSyncState.grade == grade,
        SpaceSyncState.semester == semester,
    ).first()
    if row:
        row.edition = edition
    else:
        db.add(SpaceSyncState(space_key=space_key, data_type=data_type, version=version,
                              grade=grade, semester=semester, edition=edition))
    db.commit()


def sync_knowledge_points(space_db, space_key: str, subject: str, version: str) -> dict:
    """空间库全量替换 某科目某版本 的知识点；返回 {added, removed, edition}"""
    ops_rows = get_ops_kp(subject, version)
    if not ops_rows:
        return {"added": 0, "removed": 0, "edition": None, "reason": "ops 仓库无该版本知识点"}
    edition = ops_rows[0].revision or "v1"

    subj = get_or_create_subject(space_db, subject)
    # 全量替换：旧版本数据先软删（含历史 edition 残留）
    old = space_db.query(KnowledgePoint).filter(
        KnowledgePoint.subject_id == subj.id,
        KnowledgePoint.version == version,
        KnowledgePoint.deleted == False,
    ).all()
    removed = 0
    for row in old:
        row.deleted = True
        row.edition_key = None
        removed += 1
    for kp in ops_rows:
        space_db.add(KnowledgePoint(
            name=kp.name, subject_id=subj.id, grade=kp.grade, semester=kp.semester,
            chapter=kp.chapter, description=kp.description, version=version,
            source="ops", edition_key=f"ops-{edition}",
            revision=kp.revision, tags=kp.tags, requirement=kp.requirement,
            kp_type=kp.kp_type,
        ))
    space_db.commit()
    # 主库记录同步状态（grade=0 表示整版）
    db = SessionLocal()
    try:
        _upsert_sync_state(db, space_key, "kp", version, 0, 0, edition)
    finally:
        db.close()
    return {"added": len(ops_rows), "removed": removed, "edition": edition}


def _ensure_word_package_columns(db) -> None:
    """空间库 word 表补 source/edition_key/revision 列（幂等）"""
    from sqlalchemy import text as sa_text
    cols = [r[1] for r in db.execute(sa_text("PRAGMA table_info(word)")).fetchall()]
    for col, ddl in (
        ("source", "ALTER TABLE word ADD COLUMN source VARCHAR(20) DEFAULT 'custom'"),
        ("edition_key", "ALTER TABLE word ADD COLUMN edition_key VARCHAR(50)"),
        ("revision", "ALTER TABLE word ADD COLUMN revision VARCHAR(20)"),
    ):
        if col not in cols:
            db.execute(sa_text(ddl))
    db.commit()


def sync_words(space_db, space_key: str, version: str, grade: int, semester: int) -> dict:
    """空间库全量替换 某册单词（word 表无版本列，按年级册次替换）；返回 {added, removed, edition}

    v2（id 稳定，2026-09）：按 english upsert，不再「旧词全软删+重插」——
    - 已存在的英文单词复用原行：保留 id、deleted 恢复 False、更新内容字段
      → WordProgress/WordError/WordReview/word_tag 等引用 word_id 的存量数据同步后仍然有效，
      旧题目/旧列表引用的旧 id 不会 404。
    - 真正新增的词才 INSERT（added）。
    - 该册旧 ops 词不再出现才软删（removed）；家长自定义词（source='custom'）不碰，
      不再被同步误删（旧版会把整册 custom 词一起软删）。
    幂等：重复同步同一册，同 english 行复用，added/removed 都趋 0。
    """
    _ensure_word_package_columns(space_db)
    ops_rows = get_ops_words(version, grade, semester)
    if not ops_rows:
        return {"added": 0, "removed": 0, "edition": None, "reason": "ops 仓库无该册单词"}
    edition = ops_rows[0].revision or "v1"

    # 例句兜底映射：ops_word 例句为空时，从主库内置词库（word 表）按 english 抄例句。
    # 原因：ops 运营词库曾无 example_sentences，直接覆盖会把空间库已有例句清空（custom 词
    # 也受影响），导致「有些单词有中文例句、有些没有」。此映射保证同步永远不丢例句。
    ops_english = {(w.english or "").strip().lower() for w in ops_rows}
    main_ex_map: dict = {}
    if ops_english:
        _db = SessionLocal()
        try:
            _rows = _db.query(Word).filter(
                Word.deleted == False,
                Word.example_sentences.isnot(None),
                Word.example_sentences != "",
                Word.example_sentences != "[]",
                Word.english.in_(list(ops_english)),
            ).all()
            main_ex_map = {(r.english or "").strip().lower(): r.example_sentences for r in _rows}
        finally:
            _db.close()

    def _effective_example(english: str, ops_ex: Optional[str]) -> Optional[str]:
        """同步用例句：ops 有则用 ops；ops 空则抄主库内置词库；都没有返回 None"""
        if ops_ex and ops_ex.strip() and ops_ex.strip() != "[]":
            return ops_ex
        return main_ex_map.get((english or "").strip().lower())

    # 该册现有词（含软删行），按 english 小写索引——软删行也参与复用，id 不漂移
    existing_rows = space_db.query(Word).filter(
        Word.grade == grade,
        Word.semester == semester,
    ).all()
    by_english: dict = {}
    for row in existing_rows:
        key = (row.english or "").strip().lower()
        prev = by_english.get(key)
        if prev is None or (row.deleted == False and prev.deleted == True) or (
            row.deleted == prev.deleted and row.id > prev.id
        ):
            by_english[key] = row

    added = 0
    removed = 0
    touched_ids = set()
    for w in ops_rows:
        key = (w.english or "").strip().lower()
        existing = by_english.get(key)
        if existing is not None:
            # 复用原行：保留 id，恢复 deleted=False，更新内容
            existing.deleted = False
            existing.chinese = w.chinese
            existing.phonetic = w.phonetic
            existing.unit = w.unit
            existing.unit_title = w.unit_title
            # 例句保护：ops 有例句才覆盖；ops 空则抄主库内置词库；都空则保留原值（不丢例句）
            ex = _effective_example(w.english, w.example_sentences)
            if ex:
                existing.example_sentences = ex
            existing.source = "ops"
            existing.edition_key = f"ops-{edition}"
            existing.revision = w.revision
            touched_ids.add(existing.id)
        else:
            space_db.add(Word(
                english=w.english, chinese=w.chinese, phonetic=w.phonetic,
                grade=grade, semester=semester, unit=w.unit, unit_title=w.unit_title,
                example_sentences=_effective_example(w.english, w.example_sentences),
                source="ops", edition_key=f"ops-{edition}", revision=w.revision,
            ))
            added += 1
    # 该册旧 ops 词未出现在新册 → 软删（custom 词不属于同步范围，保留）
    for row in existing_rows:
        if row.source == "ops" and not row.deleted and row.id not in touched_ids:
            row.deleted = True
            row.edition_key = None
            removed += 1
    space_db.commit()
    db = SessionLocal()
    try:
        _upsert_sync_state(db, space_key, "word", version, grade, semester, edition)
    finally:
        db.close()
    return {"added": added, "removed": removed, "edition": edition}


def get_space_sync_status(space_key: str) -> dict:
    """某空间当前同步状态：kp 按版本（整版）、word 按版本+册"""
    db = SessionLocal()
    try:
        rows = db.query(SpaceSyncState).filter(SpaceSyncState.space_key == space_key).all()
        kp = {}
        words = {}
        for r in rows:
            if r.data_type == "kp":
                kp.setdefault(r.version, {"edition": r.edition, "grade": r.grade, "semester": r.semester})
            else:
                key = (r.version, r.grade, r.semester)
                words[key] = {"edition": r.edition}
        return {"kp": kp, "words": {f"{v}-{g}-{s}": e for (v, g, s), e in words.items()}}
    finally:
        db.close()
