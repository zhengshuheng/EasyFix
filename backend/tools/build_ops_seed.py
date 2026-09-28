"""Ops 种子数据生成：ctsf 在线大纲 → ops_knowledge_point

用法：cd backend && ..\.venv\Scripts\python.exe tools/build_ops_seed.py [--subjects 数学 英语]
默认科目：数学 / 语文 / 英语（用户定位三科；科学暂不内置）
数据源：ChinaStudyFree 大纲（MIT）→ 知识点文本（不含教材原文）
幂等：按 (subject, version, grade, semester, name) upsert，重复运行不翻倍。
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import OpsKnowledgePoint
from app.models.ops_data import ensure_ops_tables
from app.services.ctsf_import import OUTLINES, fetch_outline, parse_book_meta, GRADE_CN, SEMESTER_CN

DEFAULT_SUBJECTS = ["数学", "语文", "英语"]
REVISION = "v1"


def upsert_book(db, source, subject, version, grade_n, sem_n, outline) -> dict:
    units = outline.get("units", [])
    imported = updated = skipped = 0
    seen = set()
    for unit in units:
        chapter = str(unit.get("title", "")).strip() or f"第{unit.get('unit_number', '')}单元"
        for kp in unit.get("knowledge_points", []):
            name = str(kp.get("name", "")).strip()
            if not name or name in seen:
                continue
            seen.add(name)
            desc = str(kp.get("description", "")).strip()
            q_types = kp.get("question_types") or []
            tags = [str(q) for q in q_types] if isinstance(q_types, list) else []
            row = db.query(OpsKnowledgePoint).filter(
                OpsKnowledgePoint.subject == subject,
                OpsKnowledgePoint.version == version,
                OpsKnowledgePoint.grade == grade_n,
                OpsKnowledgePoint.semester == sem_n,
                OpsKnowledgePoint.name == name,
            ).first()
            if row:
                changed = False
                for attr, val in (("chapter", chapter), ("description", desc or None)):
                    if not getattr(row, attr) and val:
                        setattr(row, attr, val)
                        changed = True
                if row.deleted:
                    row.deleted = False
                    changed = True
                if changed:
                    updated += 1
                else:
                    skipped += 1
                continue
            db.add(OpsKnowledgePoint(
                subject=subject, version=version, grade=grade_n, semester=sem_n,
                name=name, chapter=chapter, description=desc or None,
                tags=("[\"%s\"]" % '","'.join(tags)) if tags else None,
                revision=REVISION,
            ))
            imported += 1
    return {"imported": imported, "updated": updated, "skipped": skipped, "units": len(units)}


def main(subjects=None):
    subjects = subjects or DEFAULT_SUBJECTS
    ensure_ops_tables()
    db = SessionLocal()
    try:
        total = {"imported": 0, "updated": 0, "skipped": 0, "units": 0, "books": 0}
        for source, subject, version, fn in OUTLINES:
            if subject not in subjects:
                continue
            meta = parse_book_meta(fn)
            grade_cn = next((g for g, n in GRADE_CN.items() if n == meta.get("grade")), "")
            sem_cn = next((s for s, n in SEMESTER_CN.items() if n == meta.get("semester")), "")
            if not meta.get("grade") or not meta.get("semester"):
                continue
            try:
                outline = fetch_outline(source, fn)
            except Exception as e:
                print(f"  [skip] {subject}/{version} {grade_cn}{sem_cn}: {e}")
                continue
            r = upsert_book(db, source, subject, version, meta["grade"], meta["semester"], outline)
            db.commit()
            total["books"] += 1
            for k in ("imported", "updated", "skipped", "units"):
                total[k] += r[k]
            print(f"  [ok] {subject}/{version} {grade_cn}{sem_cn}: 新增{r['imported']} 更新{r['updated']} 跳过{r['skipped']} 单元{r['units']}")
        print(f"\n== 完成：{total['books']} 本，新增 {total['imported']}，更新 {total['updated']}，跳过 {total['skipped']}，单元 {total['units']}")
    finally:
        db.close()


if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    main(args or None)
