"""ChinaStudyFree 在线知识大纲导入

数据源：https://github.com/wuwangzhang1216/ChinaTextbookStudyFree（MIT 协议）
覆盖：数学(人教版1-6) / 语文(统编版1-6) / 英语(人教版PEP 3-6) / 科学(教科版1-6)，共 44 本
数据：output/{subject}/outlines/{教材}.json
      {"textbook": "三年级上册", "units": [{"unit_number":1, "title":"时、分、秒",
        "knowledge_points":[{"name":..., "description":..., "difficulty":..., "question_types":[...]}]}]}

导入流程：GitHub raw 拉 outline JSON → 解析 → 入库 knowledge_point（grade/semester/chapter/description）
无需下载教材 PDF、无需 OCR、无需 LLM。
"""
import json
import os
import re
import threading
import time
import uuid

import requests

from app.database import SessionLocal
from app.models import KnowledgePoint, Subject
from app.services.textbook_service import GH_MIRRORS, get_or_create_subject, _set_progress, _tasks, _tasks_lock

RAW_BASE = "https://raw.githubusercontent.com/wuwangzhang1216/ChinaTextbookStudyFree/main/output"
UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) EasyFix-ctsf-importer"}

GRADE_CN = {"一年级": 1, "二年级": 2, "三年级": 3, "四年级": 4, "五年级": 5, "六年级": 6}
SEMESTER_CN = {"上册": 1, "下册": 2}

# 44 本教材 outline 文件名（source 目录 → (学科, 版本, 文件名)）
OUTLINES = [
    # 数学 人教版 12 册（注意上册文件名带 " · "）
    ("math", "数学", "人教版", "义务教育教科书 · 数学一年级上册.json"),
    ("math", "数学", "人教版", "义务教育教科书 · 数学二年级上册.json"),
    ("math", "数学", "人教版", "义务教育教科书 · 数学三年级上册.json"),
    ("math", "数学", "人教版", "义务教育教科书 · 数学四年级上册.json"),
    ("math", "数学", "人教版", "义务教育教科书 · 数学五年级上册.json"),
    ("math", "数学", "人教版", "义务教育教科书 · 数学六年级上册.json"),
    ("math", "数学", "人教版", "义务教育教科书·数学一年级下册.json"),
    ("math", "数学", "人教版", "义务教育教科书·数学二年级下册.json"),
    ("math", "数学", "人教版", "义务教育教科书·数学三年级下册.json"),
    ("math", "数学", "人教版", "义务教育教科书·数学四年级下册.json"),
    ("math", "数学", "人教版", "义务教育教科书·数学五年级下册.json"),
    ("math", "数学", "人教版", "义务教育教科书·数学六年级下册.json"),
    # 语文 统编版 12 册
    ("chinese", "语文", "统编版", "义务教育教科书·语文一年级上册.json"),
    ("chinese", "语文", "统编版", "义务教育教科书·语文二年级上册.json"),
    ("chinese", "语文", "统编版", "义务教育教科书·语文三年级上册.json"),
    ("chinese", "语文", "统编版", "义务教育教科书·语文四年级上册.json"),
    ("chinese", "语文", "统编版", "义务教育教科书·语文五年级上册.json"),
    ("chinese", "语文", "统编版", "义务教育教科书·语文六年级上册.json"),
    ("chinese", "语文", "统编版", "义务教育教科书·语文一年级下册.json"),
    ("chinese", "语文", "统编版", "义务教育教科书·语文二年级下册.json"),
    ("chinese", "语文", "统编版", "义务教育教科书·语文三年级下册.json"),
    ("chinese", "语文", "统编版", "义务教育教科书·语文四年级下册.json"),
    ("chinese", "语文", "统编版", "义务教育教科书·语文五年级下册.json"),
    ("chinese", "语文", "统编版", "义务教育教科书·语文六年级下册.json"),
    # 英语 人教版PEP 8 册（上册带（PEP）后缀，下册不带）
    ("english", "英语", "人教版PEP", "义务教育教科书·英语（PEP）（三年级起点）三年级上册.json"),
    ("english", "英语", "人教版PEP", "义务教育教科书·英语（PEP）（三年级起点）四年级上册.json"),
    ("english", "英语", "人教版PEP", "义务教育教科书·英语（PEP）（三年级起点）五年级上册.json"),
    ("english", "英语", "人教版PEP", "义务教育教科书·英语（PEP）（三年级起点）六年级上册.json"),
    ("english", "英语", "人教版PEP", "义务教育教科书·英语（三年级起点）三年级下册.json"),
    ("english", "英语", "人教版PEP", "义务教育教科书·英语（三年级起点）四年级下册.json"),
    ("english", "英语", "人教版PEP", "义务教育教科书·英语（三年级起点）五年级下册.json"),
    ("english", "英语", "人教版PEP", "义务教育教科书·英语（三年级起点）六年级下册.json"),
    # 科学 教科版 12 册
    ("science", "科学", "教科版", "义务教育教科书·科学一年级上册.json"),
    ("science", "科学", "教科版", "义务教育教科书·科学二年级上册.json"),
    ("science", "科学", "教科版", "义务教育教科书·科学三年级上册.json"),
    ("science", "科学", "教科版", "义务教育教科书·科学四年级上册.json"),
    ("science", "科学", "教科版", "义务教育教科书·科学五年级上册.json"),
    ("science", "科学", "教科版", "义务教育教科书·科学六年级上册.json"),
    ("science", "科学", "教科版", "义务教育教科书·科学一年级下册.json"),
    ("science", "科学", "教科版", "义务教育教科书·科学二年级下册.json"),
    ("science", "科学", "教科版", "义务教育教科书·科学三年级下册.json"),
    ("science", "科学", "教科版", "义务教育教科书·科学四年级下册.json"),
    ("science", "科学", "教科版", "义务教育教科书·科学五年级下册.json"),
    ("science", "科学", "教科版", "义务教育教科书·科学六年级下册.json"),
]

_GRADE_RE = re.compile(r"([一二三四五六])年级(上|下)册")


def parse_book_meta(filename: str) -> dict:
    """从 outline 文件名解析 年级/学期"""
    m = _GRADE_RE.search(filename)
    if not m:
        return {}
    return {"grade": GRADE_CN[m.group(1) + "年级"], "semester": SEMESTER_CN[m.group(2) + "册"]}


def get_catalog() -> dict:
    """44 本在线大纲目录（含本地是否已导入）"""
    db = SessionLocal()
    try:
        books = []
        for source, subject, version, fn in OUTLINES:
            meta = parse_book_meta(fn)
            grade_cn = next((g for g, n in GRADE_CN.items() if n == meta.get("grade")), "")
            sem_cn = next((s for s, n in SEMESTER_CN.items() if n == meta.get("semester")), "")
            subj = db.query(Subject).filter(Subject.name == subject, Subject.deleted == False).first()
            existing = 0
            if subj and meta.get("grade"):
                existing = db.query(KnowledgePoint).filter(
                    KnowledgePoint.subject_id == subj.id,
                    KnowledgePoint.grade == meta.get("grade"),
                    KnowledgePoint.semester == meta.get("semester"),
                    KnowledgePoint.deleted == False,
                ).count()
            books.append({
                "source": source, "subject": subject, "version": version,
                "grade": grade_cn, "semester": sem_cn,
                "file": fn, "imported": existing,
            })
        return {"total": len(books), "books": books}
    finally:
        db.close()


def fetch_outline(source: str, fn: str) -> dict:
    """拉取 outline JSON（raw → ghproxy 镜像容错）"""
    url = f"{RAW_BASE}/{source}/outlines/{fn}"
    errors = []
    for u in [url] + [m + url for m in GH_MIRRORS]:
        try:
            r = requests.get(u, headers=UA, timeout=60)
            r.raise_for_status()
            return r.json()
        except Exception as e:
            errors.append(f"{u.split('/')[2]}: {e}")
    raise RuntimeError("下载知识大纲失败：" + "; ".join(errors[-3:]))


def ensure_description_column() -> None:
    """knowledge_point 表加 description 列（幂等）"""
    from sqlalchemy import text as sa_text
    db = SessionLocal()
    try:
        cols = [row[1] for row in db.execute(sa_text("PRAGMA table_info(knowledge_point)")).fetchall()]
        if "description" not in cols:
            db.execute(sa_text("ALTER TABLE knowledge_point ADD COLUMN description TEXT"))
            db.commit()
            print("[ctsf] knowledge_point 表已新增 description 列")
    finally:
        db.close()


def ensure_version_column() -> None:
    """knowledge_point 表加 version 列（幂等）"""
    from sqlalchemy import text as sa_text
    db = SessionLocal()
    try:
        cols = [row[1] for row in db.execute(sa_text("PRAGMA table_info(knowledge_point)")).fetchall()]
        if "version" not in cols:
            db.execute(sa_text("ALTER TABLE knowledge_point ADD COLUMN version VARCHAR(100)"))
            db.commit()
            print("[ctsf] knowledge_point 表已新增 version 列")
    finally:
        db.close()


def import_outline(subject: str, version: str, grade: int, semester: int, outline: dict, task: dict) -> dict:
    """单本大纲入库，返回 {imported, skipped, updated, units}"""
    from app.services.textbook_service import GRADE_CN as G_CN  # 需要中文年级名
    grade_cn = next((g for g, n in G_CN.items() if n == grade), "")
    sem_cn = next((s for s, n in SEMESTER_CN.items() if n == semester), "")
    db = SessionLocal()
    try:
        subj = get_or_create_subject(db, subject)
        existing = {row.name: row for row in db.query(KnowledgePoint).filter(
            KnowledgePoint.subject_id == subj.id, KnowledgePoint.deleted == False).all()}
        imported = skipped = updated = 0
        rows = []
        seen = set()
        units = outline.get("units", [])
        for unit in units:
            chapter = str(unit.get("title", "")).strip() or f"第{unit.get('unit_number', '')}单元"
            for kp in unit.get("knowledge_points", []):
                name = str(kp.get("name", "")).strip()
                if not name or name in seen:
                    continue
                seen.add(name)
                desc = str(kp.get("description", "")).strip()
                if name in existing:
                    row = existing[name]
                    changed = False
                    if row.grade is None and grade:
                        row.grade = grade
                        changed = True
                    if row.semester is None and semester:
                        row.semester = semester
                        changed = True
                    if not row.chapter and chapter:
                        row.chapter = chapter
                        changed = True
                    if not row.description and desc:
                        row.description = desc
                        changed = True
                    updated += 1 if changed else 0
                    if not changed:
                        skipped += 1
                    continue
                rows.append(KnowledgePoint(name=name, subject_id=subj.id,
                                           grade=grade, semester=semester,
                                           chapter=chapter, description=desc or None,
                                           version=version))
                imported += 1
        if rows:
            db.add_all(rows)
        db.commit()
        return {"imported": imported, "skipped": skipped, "updated": updated, "units": len(units)}
    finally:
        db.close()


# ---------------------------------------------------------------- 任务

def start_ctsf_import(subject: str, version: str, grade: str, semester: str) -> dict:
    """创建在线大纲导入任务（可导入整科或指定单本）"""
    target = None
    for source, subj, ver, fn in OUTLINES:
        meta = parse_book_meta(fn)
        grade_cn = next((g for g, n in GRADE_CN.items() if n == meta.get("grade")), "")
        sem_cn = next((s for s, n in SEMESTER_CN.items() if n == meta.get("semester")), "")
        if subj == subject and ver == version and grade_cn == grade and sem_cn == semester:
            target = (source, subj, ver, fn, meta["grade"], meta["semester"])
            break
    if not target:
        raise RuntimeError(f"在线大纲未找到 {subject}/{version}/{grade}{semester}")

    task = {
        "id": uuid.uuid4().hex[:12],
        "status": "pending",
        "stage": "ctsf",
        "progress": 0,
        "message": "排队中",
        "book": {"subject": subject, "version": version, "grade": grade, "semester": semester},
        "local_pdf": False,
        "source": "ctsf-online",
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": "",
        "finished_at": None,
        "error": None,
        "result": None,
    }
    with _tasks_lock:
        _tasks[task["id"]] = task
        if len(_tasks) > 50:
            for k in sorted(_tasks, key=lambda x: _tasks[x]["created_at"])[: len(_tasks) - 50]:
                _tasks.pop(k, None)

    def _worker():
        try:
            source, subj, ver, fn, grade_n, sem_n = target
            _set_progress(task, 5, "ctsf", f"下载大纲 {fn[:30]}…")
            outline = fetch_outline(source, fn)
            _set_progress(task, 30, "ctsf", "解析知识大纲…")
            ensure_description_column()
            from app.services.textbook_service import ensure_chapter_column
            ensure_chapter_column()
            ensure_version_column()
            _set_progress(task, 60, "ctsf", "写入知识点…")
            r = import_outline(subj, ver, grade_n, sem_n, outline, task)
            with _tasks_lock:
                task["result"] = r
                task["status"] = "done"
                task["finished_at"] = time.strftime("%H:%M:%S")
            _set_progress(task, 100, "done",
                          f"完成：新增 {r['imported']}，补全 {r['updated']}，跳过 {r['skipped']}，共 {r['units']} 个单元")
        except Exception as e:
            print(f"[ctsf] 导入失败: {e}")
            with _tasks_lock:
                task["status"] = "failed"
                task["error"] = str(e)
                task["finished_at"] = time.strftime("%H:%M:%S")
            _set_progress(task, 0, "failed", str(e)[:200])

    threading.Thread(target=_worker, daemon=True).start()
    return task
