"""Ops 教材数据管理 API（运营后台，X-Ops-Password 鉴权，主库读写）

定位：统一内置/维护 语文/数学/英语 各版本教材的知识点与英语单词；
数据最终发布给用户空间（POST /api/sync/* 只读同步）。
"""
from typing import List, Optional
import json
import threading

from fastapi import APIRouter, Depends, File, Header, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy import func, or_

from app.config_api import _check_ops_password
from app.database import SessionLocal
from app.models import OpsKnowledgePoint, OpsWord
from app.models.ops_data import OpsEdition, OpsPromptRule, OpsAssessRule, ensure_ops_tables
from app.services import ops_data_service
from app.services.prompt_rules_service import SCOPE_META, get_scope_default_text
from app.services.assess_rules_service import ASSESS_RULES_META, get_rule_default

router = APIRouter(prefix="/api/ops", tags=["Ops 教材数据"])


def _db():
    ensure_ops_tables()
    return SessionLocal()


def _ops_check(x_ops_username: str, x_ops_password: str) -> None:
    db = SessionLocal()
    try:
        _check_ops_password(db, x_ops_password, x_ops_username)
    finally:
        db.close()


# ---------------------------------------------------------------- 目录

@router.get("/catalog")
def ops_catalog(x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    _ops_check(x_ops_username, x_ops_password)
    return ops_data_service.get_ops_catalog()


# ---------------------------------------------------------------- 教材版本管理

class EditionCreateRequest(BaseModel):
    subject: str
    name: str
    description: Optional[str] = None


class EditionUpdateRequest(BaseModel):
    subject: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    enabled: Optional[bool] = None


@router.get("/editions")
def ops_edition_list(x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    _ops_check(x_ops_username, x_ops_password)
    return {"items": ops_data_service.get_ops_editions()}


@router.post("/editions")
def ops_edition_create(data: EditionCreateRequest,
                       x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    _ops_check(x_ops_username, x_ops_password)
    db = _db()
    try:
        subject = (data.subject or "").strip()
        name = (data.name or "").strip()
        if not subject or not name:
            raise HTTPException(status_code=400, detail="学科与版本名必填")
        dup = db.query(OpsEdition).filter(
            OpsEdition.subject == subject, OpsEdition.name == name).first()
        if dup:
            if dup.deleted:
                dup.deleted = False
            else:
                raise HTTPException(status_code=409, detail=f"版本「{subject} {name}」已存在")
            dup.description = data.description
            dup.enabled = True
        else:
            db.add(OpsEdition(subject=subject, name=name, description=data.description))
        db.commit()
        return {"id": dup.id if dup else None}
    finally:
        db.close()


@router.put("/editions/{edition_id}")
def ops_edition_update(edition_id: int, data: EditionUpdateRequest,
                       x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    """编辑版本：改名/改学科时联动更新该版本下全部知识点与单词（保持数据一致）"""
    _ops_check(x_ops_username, x_ops_password)
    db = _db()
    try:
        row = db.get(OpsEdition, edition_id)
        if not row or row.deleted:
            raise HTTPException(status_code=404, detail="版本不存在")
        new_subject = (data.subject or row.subject).strip()
        new_name = (data.name or row.name).strip()
        if not new_subject or not new_name:
            raise HTTPException(status_code=400, detail="学科与版本名不能为空")
        if (new_subject, new_name) != (row.subject, row.name):
            dup = db.query(OpsEdition).filter(
                OpsEdition.subject == new_subject, OpsEdition.name == new_name,
                OpsEdition.id != edition_id, OpsEdition.deleted == False).first()
            if dup:
                raise HTTPException(status_code=409, detail=f"版本「{new_subject} {new_name}」已存在")
            # 联动数据（同 subject+version 的知识点；版本名相同的单词——单词无学科列，按版本名联动）
            kp_rows = db.query(OpsKnowledgePoint).filter(
                OpsKnowledgePoint.deleted == False,
                OpsKnowledgePoint.subject == row.subject,
                OpsKnowledgePoint.version == row.name).all()
            for k in kp_rows:
                k.subject = new_subject
                k.version = new_name
            word_rows = db.query(OpsWord).filter(
                OpsWord.deleted == False, OpsWord.version == row.name).all()
            for w in word_rows:
                w.version = new_name
            row.subject = new_subject
            row.name = new_name
        if data.description is not None:
            row.description = data.description
        if data.enabled is not None:
            row.enabled = data.enabled
        db.commit()
        return {"id": edition_id}
    finally:
        db.close()


@router.delete("/editions/by-name")
def ops_edition_delete_by_name(subject: str, name: str,
                               x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    """删除数据中存在的未登记版本（连带软删该 学科+版本 的知识点与单词），版本表记录不受影响"""
    _ops_check(x_ops_username, x_ops_password)
    return ops_data_service.delete_ops_edition_data(subject.strip(), name.strip())


@router.delete("/editions/{edition_id}")
def ops_edition_delete(edition_id: int,
                       x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    """删除版本：软删版本记录 + 连带软删该 学科+版本 的知识点与单词"""
    _ops_check(x_ops_username, x_ops_password)
    db = _db()
    try:
        row = db.get(OpsEdition, edition_id)
        if not row or row.deleted:
            raise HTTPException(status_code=404, detail="版本不存在")
        row.deleted = True
        kp_cnt = db.query(OpsKnowledgePoint).filter(
            OpsKnowledgePoint.deleted == False,
            OpsKnowledgePoint.subject == row.subject,
            OpsKnowledgePoint.version == row.name).update(
                {OpsKnowledgePoint.deleted: True})
        word_cnt = db.query(OpsWord).filter(
            OpsWord.deleted == False, OpsWord.version == row.name).update(
                {OpsWord.deleted: True})
        db.commit()
        return {"id": edition_id, "kp_deleted": kp_cnt, "words_deleted": word_cnt}
    finally:
        db.close()


@router.post("/editions/register")
def ops_edition_register(data: EditionCreateRequest,
                         x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    """登记历史数据中已存在、但未写入版本表的 学科+版本（幂等）"""
    _ops_check(x_ops_username, x_ops_password)
    subject = (data.subject or "").strip()
    name = (data.name or "").strip()
    if not subject or not name:
        raise HTTPException(status_code=400, detail="学科与版本名不能为空")
    return ops_data_service.register_ops_edition(subject, name, data.description)


# ---------------------------------------------------------------- 知识点

class KPCreateRequest(BaseModel):
    subject: str
    version: str
    grade: int
    semester: int
    name: str
    chapter: Optional[str] = None
    description: Optional[str] = None
    requirement: Optional[str] = None
    tags: Optional[list] = None
    kp_type: Optional[str] = None
    revision: Optional[str] = None


class KPUpdateRequest(KPCreateRequest):
    pass


@router.get("/knowledge-points")
def ops_kp_list(subject: str, version: str,
                grade: Optional[int] = None, semester: Optional[int] = None,
                q: str = "", page: int = 1, page_size: int = 200,
                x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    _ops_check(x_ops_username, x_ops_password)
    db = _db()
    try:
        query = db.query(OpsKnowledgePoint).filter(
            OpsKnowledgePoint.deleted == False,
            OpsKnowledgePoint.subject == subject,
            OpsKnowledgePoint.version == version,
        )
        if grade is not None:
            query = query.filter(OpsKnowledgePoint.grade == grade)
        if semester is not None:
            query = query.filter(OpsKnowledgePoint.semester == semester)
        if q.strip():
            like = f"%{q.strip()}%"
            query = query.filter(OpsKnowledgePoint.name.like(like) |
                                 OpsKnowledgePoint.chapter.like(like) |
                                 OpsKnowledgePoint.description.like(like))
        total = query.count()
        rows = query.order_by(OpsKnowledgePoint.grade, OpsKnowledgePoint.semester,
                              OpsKnowledgePoint.chapter, OpsKnowledgePoint.id) \
            .offset((page - 1) * page_size).limit(page_size).all()
        return {"total": total, "items": [
            {"id": r.id, "subject": r.subject, "version": r.version, "grade": r.grade,
             "semester": r.semester, "name": r.name, "chapter": r.chapter,
             "description": r.description, "requirement": r.requirement,
             "tags": r.tags, "kp_type": r.kp_type, "revision": r.revision} for r in rows]}
    finally:
        db.close()


@router.post("/knowledge-points")
def ops_kp_create(data: KPCreateRequest, x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    _ops_check(x_ops_username, x_ops_password)
    db = _db()
    try:
        name = (data.name or "").strip()
        if not data.subject or not data.version or not name:
            raise HTTPException(status_code=400, detail="学科/版本/知识点名称必填")
        dup = db.query(OpsKnowledgePoint).filter(
            OpsKnowledgePoint.subject == data.subject,
            OpsKnowledgePoint.version == data.version,
            OpsKnowledgePoint.grade == data.grade,
            OpsKnowledgePoint.semester == data.semester,
            OpsKnowledgePoint.name == name,
        ).first()
        if dup:
            if dup.deleted:
                dup.deleted = False
            else:
                raise HTTPException(status_code=409, detail="同名知识点已存在")
        row = dup or OpsKnowledgePoint(
            subject=data.subject, version=data.version, grade=data.grade,
            semester=data.semester, name=name,
        )
        row.chapter = data.chapter
        row.description = data.description
        row.requirement = data.requirement
        row.tags = _dump_tags(data.tags)
        row.kp_type = data.kp_type
        row.revision = data.revision or row.revision or "v1"
        db.add(row)
        db.commit()
        return {"id": row.id}
    finally:
        db.close()


@router.put("/knowledge-points/{kp_id}")
def ops_kp_update(kp_id: int, data: KPUpdateRequest, x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    _ops_check(x_ops_username, x_ops_password)
    db = _db()
    try:
        row = db.get(OpsKnowledgePoint, kp_id)
        if not row or row.deleted:
            raise HTTPException(status_code=404, detail="知识点不存在")
        row.subject = data.subject
        row.version = data.version
        row.grade = data.grade
        row.semester = data.semester
        row.name = (data.name or "").strip() or row.name
        row.chapter = data.chapter
        row.description = data.description
        row.requirement = data.requirement
        row.tags = _dump_tags(data.tags)
        row.kp_type = data.kp_type
        row.revision = data.revision or row.revision
        db.commit()
        return {"id": row.id}
    finally:
        db.close()


@router.delete("/knowledge-points/{kp_id}")
def ops_kp_delete(kp_id: int, x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    _ops_check(x_ops_username, x_ops_password)
    db = _db()
    try:
        row = db.get(OpsKnowledgePoint, kp_id)
        if not row:
            raise HTTPException(status_code=404, detail="知识点不存在")
        row.deleted = True
        db.commit()
        return {"id": kp_id}
    finally:
        db.close()


# ---------------------------------------------------------------- 单词

class WordCreateRequest(BaseModel):
    version: str
    grade: int
    semester: int
    english: str
    chinese: str
    phonetic: Optional[str] = None
    unit: Optional[int] = None
    unit_title: Optional[str] = None
    example_sentences: Optional[list] = None
    revision: Optional[str] = None


@router.get("/words")
def ops_word_list(version: str, grade: Optional[int] = None, semester: Optional[int] = None,
                  q: str = "", page: int = 1, page_size: int = 200,
                  x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    _ops_check(x_ops_username, x_ops_password)
    db = _db()
    try:
        query = db.query(OpsWord).filter(
            OpsWord.deleted == False,
            OpsWord.version == version,
        )
        if grade is not None:
            query = query.filter(OpsWord.grade == grade)
        if semester is not None:
            query = query.filter(OpsWord.semester == semester)
        if q.strip():
            like = f"%{q.strip()}%"
            query = query.filter(OpsWord.english.like(like) | OpsWord.chinese.like(like))
        total = query.count()
        rows = query.order_by(OpsWord.grade, OpsWord.semester, OpsWord.unit,
                              OpsWord.id).offset((page - 1) * page_size).limit(page_size).all()
        return {"total": total, "items": [
            {"id": r.id, "version": r.version, "grade": r.grade, "semester": r.semester,
             "english": r.english, "chinese": r.chinese, "phonetic": r.phonetic,
             "unit": r.unit, "unit_title": r.unit_title,
             "example_sentences": r.example_sentences, "revision": r.revision} for r in rows]}
    finally:
        db.close()


@router.post("/words")
def ops_word_create(data: WordCreateRequest, x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    _ops_check(x_ops_username, x_ops_password)
    db = _db()
    try:
        en = (data.english or "").strip()
        cn = (data.chinese or "").strip()
        if not en or not cn:
            raise HTTPException(status_code=400, detail="英文与中文释义必填")
        dup = db.query(OpsWord).filter(
            OpsWord.version == data.version,
            OpsWord.grade == data.grade,
            OpsWord.semester == data.semester,
            OpsWord.english == en,
        ).first()
        if dup:
            if dup.deleted:
                dup.deleted = False
            else:
                raise HTTPException(status_code=409, detail="同名单词已存在")
        row = dup or OpsWord(version=data.version, grade=data.grade,
                             semester=data.semester, english=en)
        row.chinese = cn
        row.phonetic = data.phonetic
        row.unit = data.unit
        row.unit_title = data.unit_title
        row.example_sentences = _dump_tags(data.example_sentences)
        row.revision = data.revision or row.revision or "v1"
        db.add(row)
        db.commit()
        return {"id": row.id}
    finally:
        db.close()


@router.put("/words/{word_id}")
def ops_word_update(word_id: int, data: WordCreateRequest, x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    _ops_check(x_ops_username, x_ops_password)
    db = _db()
    try:
        row = db.get(OpsWord, word_id)
        if not row or row.deleted:
            raise HTTPException(status_code=404, detail="单词不存在")
        row.version = data.version
        row.grade = data.grade
        row.semester = data.semester
        row.english = (data.english or "").strip() or row.english
        row.chinese = (data.chinese or "").strip() or row.chinese
        row.phonetic = data.phonetic
        row.unit = data.unit
        row.unit_title = data.unit_title
        row.example_sentences = _dump_tags(data.example_sentences)
        row.revision = data.revision or row.revision
        db.commit()
        return {"id": row.id}
    finally:
        db.close()


@router.delete("/words/{word_id}")
def ops_word_delete(word_id: int, x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    _ops_check(x_ops_username, x_ops_password)
    db = _db()
    try:
        row = db.get(OpsWord, word_id)
        if not row:
            raise HTTPException(status_code=404, detail="单词不存在")
        row.deleted = True
        db.commit()
        return {"id": word_id}
    finally:
        db.close()


# ---------------------------------------------------------------- 单词

class WordAiGenerateRequest(BaseModel):
    mode: str = "textbook"  # textbook / custom
    version: Optional[str] = None
    grade: Optional[int] = None
    semester: Optional[int] = None
    instruction: Optional[str] = None


@router.post("/words/ai-generate")
def ops_word_ai_generate(req: WordAiGenerateRequest,
                         x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    """AI 智能导入预览：教材模式（版本/年级/册次）或自定义指令 → 生成单词清单（含查重），不直接写入主库"""
    _ops_check(x_ops_username, x_ops_password)
    from app.routers.word import _llm_json, parse_llm_words, _strip_md_code
    if req.mode == "textbook":
        if not req.version or not req.grade:
            raise HTTPException(status_code=400, detail="教材模式需要选择：版本、年级（册次可选）")
        grade_cn = f"{req.grade}年级"
        sem_cn = "上册" if req.semester == 1 else ("下册" if req.semester == 2 else "")
        task = (f"教材：英语《{req.version}》{grade_cn}{sem_cn or '全一册'}\n"
                "请依据这套教材的真实内容，生成该册全册的单元单词表。"
                "注意：只列本册新学词汇（含该册单元复习词），不同年级/册次的词汇表必须有明显区分；"
                "像 hello/hi/bye 等基础问候语仅在其首次出现的册次保留，不要把其他册次已学的基础词大量重复列进来。")
    else:
        if not req.instruction or not req.instruction.strip():
            raise HTTPException(status_code=400, detail="请先输入导入指令，例如：我要导入沪教版深圳英语三年级上册 全册")
        task = f"用户指令：{req.instruction.strip()}"
    prompt = (
        "你是精通国内各版本中小学教材的英语老师，熟悉各版本各年级教材的单元结构与词汇表。\n"
        f"{task}\n"
        "要求：\n"
        "1. 按单元组织，覆盖该册全部单元；每个单元先输出一行标题，格式：Unit 1 标题（标题用教材里的英文单元名，没有英文标题时用单元主题中文名）\n"
        "2. 标题行之后每行一个单词，格式：英文 中文释义（可把音标放在英文后面，如 apple /ˈæpl/，可选）\n"
        "3. 只列该教材该册要求掌握的核心单词（词汇表为主），宁缺毋滥，不要臆造不在该教材的词；短语整体保留（如 a pair of 一双）\n"
        "4. 中文释义一句话，必要时带括号补充（如 tooth 牙齿(复数teeth)）\n"
        "5. 单词数量以该册实际词汇量为准，一般每单元 8~15 个\n"
        "只输出单词表文本，严禁输出任何解释、提示、markdown 代码块，格式示例：\n"
        "Unit 1 Meeting new people\n"
        "meet 相识；结识\n"
        "new 新的\n"
        "……"
    )
    try:
        raw = _strip_md_code(_llm_json(prompt, system="你只输出单词表文本，不要任何解释。",
                                       max_tokens=4000, timeout=180))
        words = parse_llm_words(raw)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI 生成失败：{e}")
    if not words:
        raise HTTPException(status_code=502, detail="AI 返回内容无法解析为单词，请重试")

    # 查重标记（english + version + grade + semester 全匹配算已存在）
    db = _db()
    try:
        seen = set()
        out = []
        for w in words:
            en = (w.get("english") or "").strip()
            cn = (w.get("chinese") or "").strip()
            key = (en.lower(), cn)
            if not en or key in seen:
                continue
            seen.add(key)
            q = db.query(OpsWord).filter(
                OpsWord.deleted == False,
                func.lower(OpsWord.english) == en.lower(),
            )
            if req.version:
                q = q.filter(OpsWord.version == req.version)
            # 跨册查重：同版本任意年级/册次已存在 → 标记 existing（前端提示"已存在·更新"，用户可不勾选避免跨册重复导入）
            existing_rows = q.all()
            out.append({
                "english": en,
                "chinese": cn,
                "phonetic": (w.get("phonetic") or "").strip() or "",
                "unit": w.get("unit"),
                "unit_title": w.get("unit_title") or "",
                "existing": bool(existing_rows),
                "exist_grades": sorted({f"{r.grade}年级{'上' if r.semester == 1 else '下'}" for r in existing_rows}),
            })
        db.close()
    finally:
        pass

    return {"words": out, "total": len(out), "version": req.version or "",
            "grade": req.grade, "semester": req.semester}


class WordImportRequest(BaseModel):
    words: list  # [{english, chinese, phonetic, unit, unit_title}]
    version: str
    grade: Optional[int] = None
    semester: Optional[int] = None
    revision: Optional[str] = None


@router.post("/words/import")
def ops_word_import(req: WordImportRequest,
                    x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    """勾选导入单词到运营主库：english+version+grade+semester 已存在则更新，否则新增（幂等 upsert）"""
    _ops_check(x_ops_username, x_ops_password)
    if req.grade is None or req.semester is None:
        raise HTTPException(status_code=400, detail="导入单词必须选择年级和册次（grade/semester 不能为空）")
    db = _db()
    try:
        ok = 0
        skip = 0
        seen = set()  # 同请求去重（Session autoflush=False，重复词第二次 SELECT 看不到 pending 新词 → 同批 flush 撞 UNIQUE 500）
        for w in req.words:
            en = (w.get("english") or "").strip()
            cn = (w.get("chinese") or "").strip()
            if not en or not cn:
                skip += 1
                continue
            key = (req.version, req.grade, req.semester, en.lower())
            if key in seen:
                skip += 1
                continue
            seen.add(key)
            row = db.query(OpsWord).filter(
                func.lower(OpsWord.english) == en.lower(),
                OpsWord.version == req.version,
            )
            if req.grade is not None:
                row = row.filter(OpsWord.grade == req.grade)
            if req.semester is not None:
                row = row.filter(OpsWord.semester == req.semester)
            row = row.order_by(OpsWord.deleted.asc()).first()  # 优先 active 行；软删行命中则复活
            if row:
                if row.deleted:
                    row.deleted = False  # 复活软删词，避免 UNIQUE(version,grade,semester,english) 冲突 500
                row.chinese = cn
                if w.get("phonetic"):
                    row.phonetic = str(w["phonetic"]).strip() or None
                if w.get("unit") is not None:
                    row.unit = w["unit"]
                if w.get("unit_title"):
                    row.unit_title = str(w["unit_title"]).strip()
                if req.revision:
                    row.revision = req.revision
            else:
                db.add(OpsWord(
                    version=req.version, grade=req.grade, semester=req.semester,
                    unit=w.get("unit"), unit_title=(w.get("unit_title") or "").strip() or None,
                    english=en, chinese=cn,
                    phonetic=(str(w.get("phonetic") or "").strip()) or None,
                    revision=req.revision or "v1",
                ))
            ok += 1
        db.commit()
        # 新导入词自动补例句：登记范围内缺例句词，后台线程 AI 生成写回 ops_word（租户同步即得）
        if ok:
            q = db.query(OpsWord).filter(
                OpsWord.deleted == False,
                or_(OpsWord.example_sentences.is_(None),
                    OpsWord.example_sentences == "",
                    OpsWord.example_sentences == "[]"),
            )
            if req.version:
                q = q.filter(OpsWord.version == req.version)
            if req.grade is not None:
                q = q.filter(OpsWord.grade == req.grade)
            if req.semester is not None:
                q = q.filter(OpsWord.semester == req.semester)
            _ids = [r[0] for r in q.with_entities(OpsWord.id).limit(5000).all()]
            if _ids:
                _schedule_ops_fill_sentences(_ids)
        return {"imported": ok, "skipped": skip}
    finally:
        db.close()


# ---------------------------------------------------------------- 例句 AI 补全（运营侧）

class WordFillSentencesRequest(BaseModel):
    version: Optional[str] = None
    grade: Optional[int] = None
    semester: Optional[int] = None


_ops_fill_lock = threading.Lock()
_ops_fill_running = False
_ops_fill_pending_ids: set = set()


def _schedule_ops_fill_sentences(word_ids) -> None:
    """登记缺例句词 → 后台线程分批 AI 生成写回 ops_word（静默失败，幂等）"""
    if not word_ids:
        return
    global _ops_fill_running
    with _ops_fill_lock:
        _ops_fill_pending_ids.update(word_ids)
        if _ops_fill_running:
            return
        _ops_fill_running = True
    threading.Thread(target=_ops_fill_worker, daemon=True).start()


def _ops_fill_worker():
    """分批（20/批）补例句：ops_word 在主库，后台线程用主库 SessionLocal 安全"""
    global _ops_fill_running
    from app.routers.word import _fill_sentences_llm
    try:
        while True:
            with _ops_fill_lock:
                ids = list(_ops_fill_pending_ids)[:20]
                if ids:
                    _ops_fill_pending_ids.difference_update(ids)
            if not ids:
                break
            db = _db()
            try:
                words = db.query(OpsWord).filter(
                    OpsWord.id.in_(ids),
                    OpsWord.deleted == False,
                    or_(OpsWord.example_sentences.is_(None),
                        OpsWord.example_sentences == "",
                        OpsWord.example_sentences == "[]"),
                ).all()
                if words:
                    _fill_sentences_llm(db, words)
                    db.commit()
            except Exception as e:
                db.rollback()
                print(f"[ops] 例句补全失败: {e}")
            finally:
                db.close()
    finally:
        with _ops_fill_lock:
            _ops_fill_running = False


@router.post("/words/fill-sentences")
def ops_word_fill_sentences(req: WordFillSentencesRequest,
                            x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    """AI 批量补全例句：对范围内缺例句的运营单词生成语境例句并写回 ops_word（后台异步，幂等）"""
    _ops_check(x_ops_username, x_ops_password)
    db = _db()
    try:
        q = db.query(OpsWord).filter(
            OpsWord.deleted == False,
            or_(OpsWord.example_sentences.is_(None),
                OpsWord.example_sentences == "",
                OpsWord.example_sentences == "[]"),
        )
        if req.version:
            q = q.filter(OpsWord.version == req.version)
        if req.grade is not None:
            q = q.filter(OpsWord.grade == req.grade)
        if req.semester is not None:
            q = q.filter(OpsWord.semester == req.semester)
        ids = [r[0] for r in q.with_entities(OpsWord.id).limit(5000).all()]
    finally:
        db.close()
    _schedule_ops_fill_sentences(ids)
    if ids:
        return {"queued": len(ids),
                "message": f"已提交 {len(ids)} 个单词例句生成，后台分批自动完成（约 {len(ids) // 20 + 1} 批，每批十几秒），稍后刷新可见"}
    return {"queued": 0, "message": "当前范围内没有缺例句的单词"}


class WordTextImportRequest(BaseModel):
    text: str
    version: str
    grade: Optional[int] = None
    semester: Optional[int] = None
    revision: Optional[str] = None


@router.post("/words/extract-textbook")
async def ops_word_extract_textbook(
    files: List[UploadFile] = File(...),
    x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    """图片/PDF 教材单词表提取（复用平台 OCR/多模态服务）：识别后按单元格式解析出单词，预览后再由 /words/import 导入"""
    _ops_check(x_ops_username, x_ops_password)
    from app.routers.word import parse_llm_words
    import os
    import shutil
    import tempfile
    from app.services import textbook_service

    tmpdir = tempfile.mkdtemp(prefix="ops_word_extract_")
    try:
        pages = []  # (来源名, 文本)
        for f in files:
            if not f.filename:
                continue
            safe = os.path.basename(f.filename or "upload")
            path = os.path.join(tmpdir, safe)
            with open(path, "wb") as out:
                out.write(await f.read())
            ext = os.path.splitext(safe)[1].lower()
            if ext == ".pdf":
                import fitz
                ocr = textbook_service._get_ocr()
                doc = fitz.open(path)
                try:
                    for i, page in enumerate(doc):
                        text = textbook_service._page_to_text(ocr, page)
                        if text.strip():
                            pages.append((f"{safe} 第{i + 1}页", text))
                finally:
                    doc.close()
            elif ext in (".jpg", ".jpeg", ".png", ".bmp", ".webp"):
                text = textbook_service.image_to_text(path)
                if text.strip():
                    pages.append((safe, text))
        if not pages:
            return {"words": [], "total": 0,
                    "detail": "未能从图片/PDF 中识别出文字，请确认上传的是教材单词表页"}

        joined = "\n".join([f"【{name}】\n{text}" for name, text in pages])
        words = parse_llm_words(joined)
        seen = set()
        out = []
        for w in words:
            en = (w.get("english") or "").strip()
            cn = (w.get("chinese") or "").strip()
            key = (en.lower(), cn)
            if not en or key in seen:
                continue
            seen.add(key)
            out.append({
                "english": en,
                "chinese": cn,
                "phonetic": (w.get("phonetic") or "").strip() or "",
                "unit": w.get("unit"),
                "unit_title": w.get("unit_title") or "",
                "existing": False,
            })
        return {"words": out, "total": len(out), "detail": ""}
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)


@router.post("/words/batch-text")
def ops_word_batch_text(req: WordTextImportRequest,
                        x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    """文本粘贴批量导入单词：格式同 AI 输出（Unit N 标题行 + 每行 英文 中文），幂等 upsert"""
    _ops_check(x_ops_username, x_ops_password)
    from app.routers.word import parse_llm_words
    words = parse_llm_words(req.text or "")
    if not words:
        raise HTTPException(status_code=400, detail="未能解析出任何单词，请检查格式（每行：英文 中文，可带 Unit 标题行）")
    return ops_word_import(WordImportRequest(
        words=words, version=req.version, grade=req.grade,
        semester=req.semester, revision=req.revision,
    ), x_ops_username, x_ops_password)


# ---------------------------------------------------------------- 知识点：AI 生成预览 / 勾选导入 / 文本批量

class KPAiGenerateRequest(BaseModel):
    mode: str = "textbook"  # textbook / custom
    subject: Optional[str] = None
    version: Optional[str] = None
    grade: Optional[int] = None
    semester: Optional[int] = None
    instruction: Optional[str] = None


_GRADE_CN_OPS = {1: "一年级", 2: "二年级", 3: "三年级", 4: "四年级", 5: "五年级", 6: "六年级"}
_SEM_CN_OPS = {1: "上册", 2: "下册"}


def _parse_json_ops(content: str) -> dict:
    """从 LLM 输出提取 JSON 对象（容忍 markdown 代码块/前后噪音）"""
    import re as _re
    if not content:
        return {}
    text = content.strip()
    if text.startswith("```"):
        text = _re.sub(r"^```[a-zA-Z]*\s*", "", text)
        text = _re.sub(r"\s*```$", "", text)
    text = text.strip()
    try:
        return json.loads(text)
    except Exception:
        m = _re.search(r"\{.*\}", text, _re.S)
        if m:
            try:
                return json.loads(m.group(0))
            except Exception:
                return {}
        return {}


@router.post("/knowledge-points/ai-generate")
def ops_kp_ai_generate(req: KPAiGenerateRequest,
                       x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    """AI 生成知识点清单（教材模式/自定义指令，含查重），预览后由 /knowledge-points/import 导入"""
    _ops_check(x_ops_username, x_ops_password)
    from app.routers.word import _llm_json
    if req.mode == "textbook":
        if not req.subject or not req.grade:
            raise HTTPException(status_code=400, detail="教材模式需要选择：学科、年级（版本/册次可选）")
        grade_cn = _GRADE_CN_OPS.get(req.grade, f"{req.grade}年级")
        sem_cn = _SEM_CN_OPS.get(req.semester) if req.semester else ""
        desc = f"{req.subject}《{req.version or '通用教材'}》{grade_cn}{sem_cn or '全一册'}"
        task = f"教材：{desc}\n请依据这套教材的真实内容，生成该册全部单元的知识点清单。"
    else:
        if not req.instruction or not req.instruction.strip():
            raise HTTPException(status_code=400, detail="请先输入导入指令，例如：生成人教版小学数学三年级上册的全部知识点")
        task = f"用户指令：{req.instruction.strip()}"

    prompt = (
        "你是熟悉国内各版本中小学教材的名师，精通各学段各学科的单元结构与知识点体系。\n"
        f"{task}\n"
        "要求：\n"
        "1. 按单元组织，每个单元一章；chapter 用教材里的单元名（如：第一单元 时、分、秒；Unit 1 Hello!）\n"
        "2. 每单元列出本单元要求掌握的核心知识点 3~8 条，覆盖该单元主要教学内容\n"
        "3. 每条知识点字段：\n"
        "   - name：知识点名称（简短，如 认识秒 / be动词am/is/are的用法）\n"
        "   - description：一句话说明该知识点要掌握什么\n"
        "   - requirement：识记/理解/背诵/运用/综合（按课标认知层次选一个）\n"
        "   - tags：教学标签数组，从 重点/难点/易错点 中选（可多个或空）\n"
        "   - kp_type：学科内容类型（数学：数与代数/图形与几何/统计与概率/综合与实践；语文：识字写字/阅读/习作/口语交际；英语：语音/词汇/句型/语法/话题/阅读/写作；其他学科自定合理类型）\n"
        "4. 宁缺毋滥，只列该教材该册真实要求掌握的内容，不要臆造教材没有的知识点\n"
        "只输出 JSON，不要任何解释，不要 markdown 代码块：\n"
        "{\"chapters\":[{\"chapter\":\"第一单元 时、分、秒\",\"points\":[{\"name\":\"认识秒\",\"description\":\"知道秒是比分更小的时间单位，会认秒针\",\"requirement\":\"理解\",\"tags\":[\"重点\"],\"kp_type\":\"数与代数\"}]}]}"
    )
    try:
        content = _llm_json(prompt, system="你只输出JSON，不要输出任何解释。", max_tokens=4000, timeout=180)
        data = _parse_json_ops(content)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI 生成失败：{e}")

    chapters = data.get("chapters", []) if isinstance(data, dict) else []
    items = []
    seen = set()
    for ch in chapters:
        chapter = str(ch.get("chapter", "")).strip() if isinstance(ch, dict) else ""
        for p in (ch.get("points", []) if isinstance(ch, dict) else []):
            if not isinstance(p, dict):
                continue
            name = str(p.get("name", "")).strip()
            if not name:
                continue
            key = name.lower()
            if key in seen:
                continue
            seen.add(key)
            items.append({
                "chapter": chapter,
                "name": name,
                "description": str(p.get("description", "")).strip(),
                "requirement": str(p.get("requirement", "")).strip() or "",
                "tags": [str(t).strip() for t in (p.get("tags") or []) if str(t).strip()],
                "kp_type": str(p.get("kp_type", "")).strip() or "",
                "existing": False,
            })

    if not items:
        raise HTTPException(status_code=502, detail="AI 返回内容无法解析为知识点，请重试")

    # 查重：subject+version+grade+semester+name 全匹配算已存在
    db = _db()
    try:
        for it in items:
            q = db.query(OpsKnowledgePoint).filter(
                OpsKnowledgePoint.deleted == False,
                func.lower(OpsKnowledgePoint.name) == it["name"].lower(),
            )
            if req.subject:
                q = q.filter(OpsKnowledgePoint.subject == req.subject)
            if req.version:
                q = q.filter(OpsKnowledgePoint.version == req.version)
            if req.grade is not None:
                q = q.filter(OpsKnowledgePoint.grade == req.grade)
            if req.semester is not None:
                q = q.filter(OpsKnowledgePoint.semester == req.semester)
            it["existing"] = q.first() is not None
        db.close()
    finally:
        pass

    return {"items": items, "total": len(items), "subject": req.subject or "",
            "version": req.version or "", "grade": req.grade, "semester": req.semester}


class KPImportRequest(BaseModel):
    items: list  # [{name, chapter, description, requirement, tags, kp_type}]
    subject: str
    version: str
    grade: int
    semester: int
    revision: Optional[str] = None


def _kp_upsert(db, name, chapter, description, requirement, tags, kp_type,
               subject, version, grade, semester, revision, source_type="ai",
               ocr_mode: str = None, import_batch: str = None) -> bool:
    """主库知识点 upsert：subject+version+grade+semester+name 已存在则更新，否则新增

    source_type：ctsf-online/ctsf-local/textbook-online/textbook-local/ai
    ocr_mode 识别方式：authority(权威在线源)/multimodal(多模态)/local(本地OCR)/llm(AI生成)
    import_batch 教材任务批次：教材提取任务完成后清理同教材旧批次防重复；手动/AI指令/大纲不传
    """
    name = (name or "").strip()
    if not name:
        return False
    # autoflush=False：先把本 session 已 pending 的行写库，
    # 避免同批导入跨单元提取到同名知识点时二次 INSERT 撞 UNIQUE
    db.flush()
    row = db.query(OpsKnowledgePoint).filter(
        func.lower(OpsKnowledgePoint.name) == name.lower(),
        OpsKnowledgePoint.subject == subject,
        OpsKnowledgePoint.version == version,
        OpsKnowledgePoint.grade == grade,
        OpsKnowledgePoint.semester == semester,
    ).first()
    if row:
        row.deleted = False  # 软删行复活（唯一约束按 name 占位，软删不释放名字）
        if chapter:
            row.chapter = chapter
        if description:
            row.description = description
        if requirement:
            row.requirement = requirement
        if tags:
            row.tags = _dump_tags(tags)
        if kp_type:
            row.kp_type = kp_type
        if revision:
            row.revision = revision
        row.source_type = source_type
        if ocr_mode:
            row.ocr_mode = ocr_mode
        if import_batch is not None:
            row.import_batch = import_batch
    else:
        db.add(OpsKnowledgePoint(
            subject=subject, version=version, grade=grade, semester=semester,
            name=name, chapter=chapter or None, description=description or None,
            requirement=requirement or None,
            tags=_dump_tags(tags) if tags else None,
            kp_type=kp_type or None, revision=revision or "v1",
            source_type=source_type, ocr_mode=ocr_mode, import_batch=import_batch,
        ))
    return True


def _clean_old_kp_batches(db, subject, version, grade, semester, batch_id: str) -> int:
    """教材任务成功后清理同教材旧批次知识点（防重复累积）。

    清理对象（软删）：
      1) 教材来源（textbook-online/textbook-local）且无批次或非本次批次（含历史遗留行）
      2) 带批次且非本次批次的其余来源（如教材任务失败时的 AI 兜底行）
    保留：本次批次行、无批次的手动新增 / AI 指令生成 / 权威大纲行。
    """
    n = 0
    q1 = db.query(OpsKnowledgePoint).filter(
        OpsKnowledgePoint.subject == subject,
        OpsKnowledgePoint.version == version,
        OpsKnowledgePoint.grade == grade,
        OpsKnowledgePoint.semester == semester,
        OpsKnowledgePoint.source_type.in_(["textbook-online", "textbook-local"]),
        or_(OpsKnowledgePoint.import_batch.is_(None), OpsKnowledgePoint.import_batch != batch_id),
    )
    n += q1.update({OpsKnowledgePoint.deleted: True}, synchronize_session=False)
    q2 = db.query(OpsKnowledgePoint).filter(
        OpsKnowledgePoint.subject == subject,
        OpsKnowledgePoint.version == version,
        OpsKnowledgePoint.grade == grade,
        OpsKnowledgePoint.semester == semester,
        OpsKnowledgePoint.import_batch.isnot(None),
        OpsKnowledgePoint.import_batch != batch_id,
    )
    n += q2.update({OpsKnowledgePoint.deleted: True}, synchronize_session=False)
    return n


@router.post("/knowledge-points/import")
def ops_kp_import(req: KPImportRequest,
                  x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    """勾选导入知识点到运营主库：同名同教材同册已存在则更新，否则新增（幂等 upsert）"""
    _ops_check(x_ops_username, x_ops_password)
    db = _db()
    try:
        ok = 0
        for it in req.items:
            if _kp_upsert(db, it.get("name"), it.get("chapter"), it.get("description"),
                          it.get("requirement"), it.get("tags"), it.get("kp_type"),
                          req.subject, req.version, req.grade, req.semester, req.revision,
                          "ai", ocr_mode="llm"):
                ok += 1
        db.commit()
        return {"imported": ok}
    finally:
        db.close()


class KPTextImportRequest(BaseModel):
    text: str
    subject: str
    version: str
    grade: int
    semester: int
    revision: Optional[str] = None


@router.post("/knowledge-points/batch-text")
def ops_kp_batch_text(req: KPTextImportRequest,
                      x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    """文本粘贴批量导入知识点：每行 名称|章节|说明|要求（| 分隔，后三项可选），幂等 upsert"""
    _ops_check(x_ops_username, x_ops_password)
    items = []
    for line in (req.text or "").splitlines():
        line = line.strip()
        if not line:
            continue
        parts = [p.strip() for p in line.split("|")]
        name = parts[0]
        if not name:
            continue
        items.append({
            "name": name,
            "chapter": parts[1] if len(parts) > 1 else "",
            "description": parts[2] if len(parts) > 2 else "",
            "requirement": parts[3] if len(parts) > 3 else "",
            "tags": [],
            "kp_type": "",
        })
    if not items:
        raise HTTPException(status_code=400, detail="未能解析出任何知识点，请检查格式（每行：名称|章节|说明|要求）")
    return ops_kp_import(KPImportRequest(
        items=items, subject=req.subject, version=req.version,
        grade=req.grade, semester=req.semester, revision=req.revision,
    ), x_ops_username, x_ops_password)


def _dump_tags(tags) -> Optional[str]:
    if tags is None:
        return None
    if isinstance(tags, list):
        return "[\"%s\"]" % '","'.join(str(t) for t in tags)
    return str(tags)


# ---------------------------------------------------------------- 智能导入三步（在线知识点 → 在线教材 → AI）

class KPSmartCheckRequest(BaseModel):
    subject: str
    version: str
    grade: int
    semester: int


def _match_index_book_strict(subject: str, version: str, grade_cn: str, sem_cn: str) -> Optional[dict]:
    """在线教材 index.json 严格匹配：精确版本 → token 包含；默认回退一律不匹配（避免误导下载错教材）"""
    from app.services.textbook_service import get_index
    import re as _re
    index = get_index()
    cands = [b for b in index.get("books", [])
             if b.get("subject") == subject
             and b.get("grade") == grade_cn
             and b.get("semester") == sem_cn]
    exact = next((b for b in cands if b.get("version") == version), None)
    if not exact:
        tokens = [t for t in _re.findall(r"[\u4e00-\u9fa5]+|[A-Za-z]+", version) if len(t) >= 2]
        scored = [(sum(1 for tok in tokens if tok in b.get("version", "")), b) for b in cands]
        scored = [(s, b) for s, b in scored if s > 0]
        if scored:
            scored.sort(key=lambda x: (-x[0], len(x[1].get("version", ""))))
            exact = scored[0][1]
    return exact


@router.post("/knowledge-points/smart-check")
def ops_kp_smart_check(req: KPSmartCheckRequest,
                       x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    """探测智能导入资源：①ctsf 在线知识大纲（秒级导入）②index.json 在线教材（PDF 可下载提取）③AI 兜底"""
    _ops_check(x_ops_username, x_ops_password)
    from app.services import ctsf_import
    from app.services.textbook_service import GRADE_CN as _G_CN, SEMESTER_CN as _S_CN
    grade_cn = next((g for g, n in _G_CN.items() if n == req.grade), "")
    sem_cn = next((s for s, n in _S_CN.items() if n == req.semester), "")

    ctsf = None
    for source, subj, ver, fn in ctsf_import.OUTLINES:
        meta = ctsf_import.parse_book_meta(fn)
        if subj == req.subject and ver == req.version and meta.get("grade") == req.grade \
                and meta.get("semester") == req.semester:
            ctsf = {"source": source, "subject": subj, "version": ver,
                    "grade": req.grade, "semester": req.semester, "file": fn}
            break

    pdf = None
    try:
        exact = _match_index_book_strict(req.subject, req.version, grade_cn, sem_cn)
        if exact:
            downloads = exact.get("downloads") or []
            pdf = {
                "subject": exact.get("subject", req.subject),
                "version": exact.get("version", req.version),
                "grade": req.grade, "semester": req.semester,
                "grade_cn": grade_cn, "sem_cn": sem_cn,
                "local_only": bool(exact.get("local_only")) or not downloads,
                "downloads": len(downloads),
            }
    except Exception:
        pass

    return {"subject": req.subject, "version": req.version, "grade": req.grade,
            "semester": req.semester, "ctsf": ctsf, "pdf": pdf, "ai": True}


class KPCtsfImportRequest(BaseModel):
    subject: str
    version: str
    grade: int
    semester: int


def _sync_import_outline(outline: dict, subject: str, version: str, grade: int,
                         semester: int, source_type: str) -> dict:
    """outline JSON → 运营主库 upsert（同步，秒级）"""
    db = _db()
    try:
        ok = skipped = 0
        seen = set()
        units = outline.get("units", [])
        for unit in units:
            chapter = str(unit.get("title", "")).strip() or f"第{unit.get('unit_number', '')}单元"
            for kp in unit.get("knowledge_points", []):
                name = str(kp.get("name", "")).strip()
                if not name or name in seen:
                    skipped += 1
                    continue
                seen.add(name)
                if _kp_upsert(db, name, chapter, str(kp.get("description", "")).strip() or None,
                              None, None, None, subject, version, grade, semester, "v1",
                              source_type, ocr_mode="authority"):
                    ok += 1
        db.commit()
        return {"imported": ok, "skipped": skipped, "units": len(units)}
    finally:
        db.close()


@router.post("/knowledge-points/ctsf-import")
def ops_kp_ctsf_import(req: KPCtsfImportRequest,
                       x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    """在线知识大纲（ChinaStudyFree）秒级导入运营主库：拉 outline JSON → 解析 → upsert"""
    _ops_check(x_ops_username, x_ops_password)
    from app.services import ctsf_import
    target = None
    for source, subj, ver, fn in ctsf_import.OUTLINES:
        meta = ctsf_import.parse_book_meta(fn)
        if subj == req.subject and ver == req.version and meta.get("grade") == req.grade \
                and meta.get("semester") == req.semester:
            target = (source, subj, ver, fn)
            break
    if not target:
        raise HTTPException(status_code=404,
                            detail="在线知识大纲未收录该教材（可改用教材 PDF 提取或 AI 生成）")
    source, subj, ver, fn = target
    outline = ctsf_import.fetch_outline(source, fn)
    r = _sync_import_outline(outline, req.subject, req.version, req.grade, req.semester, "ctsf-online")
    return {**r, "source": "ctsf-online"}


class KPPdfImportRequest(BaseModel):
    subject: str
    version: str
    grade: int
    semester: int


def _start_ops_pdf_task(req, book: dict, download: bool, source_type: str) -> dict:
    """教材 PDF 提取知识点 → 运营主库（异步任务）。

    download=True 走在线下载（book 为 index.json 条目）；download=False 用本地 PDF
    （book 仅含 subject/version/grade/semester，download_book 检测到本地已存在会跳过下载）。
    失败自动降级：任务内转 AI 生成，保证「系统内部完成决策」。
    """
    from app.services import textbook_service
    from app.services.textbook_service import GRADE_CN as _G_CN, SEMESTER_CN as _S_CN
    import os as _os
    import threading
    import time
    import uuid
    grade_cn = next((g for g, n in _G_CN.items() if n == req.grade), "")
    sem_cn = next((s for s, n in _S_CN.items() if n == req.semester), "")
    stage_label = "textbook-online" if download else "textbook-local"
    batch_id = "tb" + time.strftime("%Y%m%d%H%M%S")  # 教材任务批次：成功后清理同教材旧批次防重复
    task = {
        "id": uuid.uuid4().hex[:12],
        "status": "pending", "stage": stage_label, "progress": 0,
        "message": "排队中",
        "book": {"subject": req.subject, "version": req.version,
                 "grade": req.grade, "semester": req.semester},
        "source": stage_label,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": "", "finished_at": None, "error": None, "result": None,
    }
    with textbook_service._tasks_lock:
        textbook_service._tasks[task["id"]] = task

    def _finish(method, result, message):
        with textbook_service._tasks_lock:
            task["result"] = result
            task["status"] = "done"
            task["finished_at"] = time.strftime("%H:%M:%S")
        textbook_service._set_progress(task, 100, "done", f"{message}（来源：{method}）")

    def _worker():
        try:
            # 识别方式：优先模型市场多模态（vision 厂商 + key 有效），否则本地 OCR
            vision_cfg = textbook_service._resolve_vision_gateway()
            ocr_mode = "multimodal" if vision_cfg else "local"
            if download:
                textbook_service._set_progress(task, 5, stage_label, "下载教材 PDF…")
            else:
                textbook_service._set_progress(task, 5, stage_label, "读取本地教材 PDF…")
            pdf_path = textbook_service.download_book(book, task)
            txt_path = _os.path.splitext(pdf_path)[0] + ".txt"
            textbook_service._set_progress(task, 45, stage_label, "识别教材文字…")
            full_text = textbook_service.extract_text(pdf_path, txt_path, task, vision_cfg=vision_cfg)
            # 内容识别：先识别目录页定位单元页码 → 按页范围切分；失败回退正则/全册
            units = None
            toc = textbook_service._toc_from_text(full_text)
            if toc:
                textbook_service._set_progress(task, 50, stage_label,
                                               f"目录定位 {len(toc)} 个单元，按页提取…")
                units = textbook_service.split_units_from_toc(full_text, toc)
            if units is None or not units:
                units = textbook_service.split_units(full_text)
            if not units:
                raise RuntimeError("未从教材中识别出单元，请确认内容完整（应包含「第X单元/Unit X」）")
            book_meta = f"{req.subject}《{req.version}》{grade_cn}{sem_cn}"
            db = _db()
            try:
                ok = 0
                for i, (chapter, body) in enumerate(units):
                    textbook_service._set_progress(
                        task, 50 + int(i / max(len(units), 1) * 40), stage_label,
                        f"AI 提取第 {i + 1}/{len(units)} 单元…")
                    pts = textbook_service.extract_unit_points(req.subject, book_meta,
                                                               chapter, body, task)
                    for name, desc in pts:
                        if _kp_upsert(db, name, chapter, desc or None, None, None, None,
                                      req.subject, req.version, req.grade, req.semester,
                                      "v1", source_type, ocr_mode=ocr_mode, import_batch=batch_id):
                            ok += 1
                cleaned = _clean_old_kp_batches(db, req.subject, req.version,
                                                 req.grade, req.semester, batch_id)
                db.commit()
            finally:
                db.close()
            _finish(source_type, {"imported": ok, "units": len(units), "cleaned": cleaned},
                    f"完成：共 {ok} 条知识点（清理旧批次 {cleaned} 条）")
        except Exception as e:
            print(f"[ops {stage_label}] 失败，降级 AI: {e}")
            # 自动降级：AI 生成兜底（系统内部完成决策）
            try:
                textbook_service._set_progress(task, 60, stage_label, "教材处理失败，自动转 AI 生成…")
                items = _ai_gen_kp_items(req.subject, req.version, req.grade, req.semester, None)
                db = _db()
                try:
                    ok = 0
                    for it in items:
                        if _kp_upsert(db, it["name"], it.get("chapter"), it.get("description"),
                                      it.get("requirement"), it.get("tags"), it.get("kp_type"),
                                      req.subject, req.version, req.grade, req.semester, "v1", "ai",
                                      ocr_mode="llm", import_batch=batch_id):
                            ok += 1
                    db.commit()
                finally:
                    db.close()
                _finish("ai", {"imported": ok, "units": len({it.get("chapter", "") for it in items})},
                        f"教材处理失败已转 AI 生成：共 {ok} 条知识点")
            except Exception as e2:
                print(f"[ops {stage_label}] AI 兜底也失败: {e2}")
                with textbook_service._tasks_lock:
                    task["status"] = "failed"
                    task["error"] = str(e2)[:300]
                    task["finished_at"] = time.strftime("%H:%M:%S")
                textbook_service._set_progress(task, 0, "failed", str(e2)[:200])

    threading.Thread(target=_worker, daemon=True).start()
    return task


@router.post("/knowledge-points/pdf-import")
def ops_kp_pdf_import(req: KPPdfImportRequest,
                      x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    """在线教材 PDF 提取知识点 → 运营主库（异步任务，复用 textbook_service 下载/OCR/LLM 链路）"""
    _ops_check(x_ops_username, x_ops_password)
    from app.services.textbook_service import GRADE_CN as _G_CN, SEMESTER_CN as _S_CN
    grade_cn = next((g for g, n in _G_CN.items() if n == req.grade), "")
    sem_cn = next((s for s, n in _S_CN.items() if n == req.semester), "")
    book = _match_index_book_strict(req.subject, req.version, grade_cn, sem_cn)
    if not book:
        raise HTTPException(status_code=404, detail="在线教材目录中未找到该教材")
    if not book.get("downloads"):
        raise HTTPException(status_code=400,
                            detail="该教材无在线下载资源，需手动放置 PDF（本运营端暂不支持）")
    task = _start_ops_pdf_task(req, book, download=True, source_type="textbook-online")
    return {"task_id": task["id"], "status": "pending"}


@router.get("/tasks/{task_id}")
def ops_task_get(task_id: str,
                 x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    """运营端异步任务进度查询（教材 PDF 提取等）"""
    _ops_check(x_ops_username, x_ops_password)
    from app.services import textbook_service
    task = textbook_service._tasks.get(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return {k: task.get(k) for k in ("id", "status", "stage", "progress", "message",
                                     "result", "error", "created_at", "finished_at")}


class KPSmartImportRequest(BaseModel):
    subject: str
    version: str
    grade: int
    semester: int
    skip_online_textbook: bool = False  # 跳过在线教材下载（在线 PDF 较大较慢；走本地教材或 AI 兜底）


def _ai_gen_kp_items(subject: str, version: str, grade: int, semester: int, instruction: str = None) -> list:
    """AI 生成知识点清单（教材模式/自定义指令），供异步任务直接 upsert"""
    from app.routers.word import _llm_json
    if instruction:
        task = f"用户指令：{instruction.strip()}"
    else:
        grade_cn = _GRADE_CN_OPS.get(grade, f"{grade}年级")
        sem_cn = _SEM_CN_OPS.get(semester) if semester else ""
        desc = f"{subject}《{version or '通用教材'}》{grade_cn}{sem_cn or '全一册'}"
        task = f"教材：{desc}\n请依据这套教材的真实内容，生成该册全部单元的知识点清单。"

    prompt = (
        "你是熟悉国内各版本中小学教材的名师，精通各学段各学科的单元结构与知识点体系。\n"
        f"{task}\n"
        "要求：\n"
        "1. 按单元组织，每个单元一章；chapter 用教材里的单元名（如：第一单元 时、分、秒；Unit 1 Hello!）\n"
        "2. 每单元列出本单元要求掌握的核心知识点 3~8 条，覆盖该单元主要教学内容\n"
        "3. 每条知识点字段：\n"
        "   - name：知识点名称（简短，如 认识秒 / be动词am/is/are的用法）\n"
        "   - description：一句话说明该知识点要掌握什么\n"
        "   - requirement：识记/理解/背诵/运用/综合（按课标认知层次选一个）\n"
        "   - tags：教学标签数组，从 重点/难点/易错点 中选（可多个或空）\n"
        "   - kp_type：学科内容类型（数学：数与代数/图形与几何/统计与概率/综合与实践；语文：识字写字/阅读/习作/口语交际；英语：语音/词汇/句型/语法/话题/阅读/写作；其他学科自定合理类型）\n"
        "4. 宁缺毋滥，只列该教材该册真实要求掌握的内容，不要臆造教材没有的知识点\n"
        "只输出 JSON，不要任何解释，不要 markdown 代码块：\n"
        "{\"chapters\":[{\"chapter\":\"第一单元 时、分、秒\",\"points\":[{\"name\":\"认识秒\",\"description\":\"知道秒是比分更小的时间单位，会认秒针\",\"requirement\":\"理解\",\"tags\":[\"重点\"],\"kp_type\":\"数与代数\"}]}]}"
    )
    content = _llm_json(prompt, system="你只输出JSON，不要输出任何解释。", max_tokens=4000, timeout=180)
    data = _parse_json_ops(content)
    chapters = data.get("chapters", []) if isinstance(data, dict) else []
    items = []
    seen = set()
    for ch in chapters:
        chapter = str(ch.get("chapter", "")).strip() if isinstance(ch, dict) else ""
        for p in (ch.get("points", []) if isinstance(ch, dict) else []):
            if not isinstance(p, dict):
                continue
            name = str(p.get("name", "")).strip()
            if not name or name.lower() in seen:
                continue
            seen.add(name.lower())
            items.append({
                "chapter": chapter,
                "name": name,
                "description": str(p.get("description", "")).strip(),
                "requirement": str(p.get("requirement", "")).strip() or "",
                "tags": [str(t).strip() for t in (p.get("tags") or []) if str(t).strip()],
                "kp_type": str(p.get("kp_type", "")).strip() or "",
            })
    if not items:
        raise RuntimeError("AI 返回内容无法解析为知识点")
    return items


def _start_ops_ai_task(req) -> dict:
    """AI 生成知识点 → 运营主库（异步任务）"""
    from app.services import textbook_service
    import threading
    import time
    import uuid
    task = {
        "id": uuid.uuid4().hex[:12],
        "status": "pending", "stage": "ai-ops", "progress": 0,
        "message": "排队中",
        "book": {"subject": req.subject, "version": req.version,
                 "grade": req.grade, "semester": req.semester},
        "source": "ai-ops",
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": "", "finished_at": None, "error": None, "result": None,
    }
    with textbook_service._tasks_lock:
        textbook_service._tasks[task["id"]] = task

    def _worker():
        try:
            textbook_service._set_progress(task, 5, "ai-ops", "AI 生成知识点中（约 1~3 分钟）…")
            items = _ai_gen_kp_items(req.subject, req.version, req.grade, req.semester)
            textbook_service._set_progress(task, 80, "ai-ops", "写入知识点…")
            db = _db()
            try:
                ok = 0
                for it in items:
                    if _kp_upsert(db, it["name"], it.get("chapter"), it.get("description"),
                                  it.get("requirement"), it.get("tags"), it.get("kp_type"),
                                  req.subject, req.version, req.grade, req.semester, "v1", "ai",
                                  ocr_mode="llm"):
                        ok += 1
                db.commit()
            finally:
                db.close()
            with textbook_service._tasks_lock:
                task["result"] = {"imported": ok, "units": len({it.get("chapter", "") for it in items})}
                task["status"] = "done"
                task["finished_at"] = time.strftime("%H:%M:%S")
            textbook_service._set_progress(task, 100, "done", f"完成：共 {ok} 条知识点（来源：AI 指令生成）")
        except Exception as e:
            print(f"[ops ai] 失败: {e}")
            with textbook_service._tasks_lock:
                task["status"] = "failed"
                task["error"] = str(e)[:300]
                task["finished_at"] = time.strftime("%H:%M:%S")
            textbook_service._set_progress(task, 0, "failed", str(e)[:200])

    threading.Thread(target=_worker, daemon=True).start()
    return task


@router.post("/knowledge-points/smart-import")
def ops_kp_smart_import(req: KPSmartImportRequest,
                        x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    """智能导入自动决策（系统自动选择最佳方式，用户无需理解）：
    ①权威在线知识源（官网/教育部公开大纲优先，其次 GitHub 教材大纲；命中即用、不做教材 OCR）→
    ②本地权威大纲缓存（之前已下载过的权威大纲，秒级导入、准确性高）→
    ③本地教材 PDF（教材库中已放置的 PDF，优先于在线下载；识别优先多模态模型，key 无效自动降级本地 OCR；
       先识别目录页定位单元页码，再按页范围提取）→
    ④在线教材资源（index.json 可下载，同③识别流程；req.skip_online_textbook=True 时跳过此步直接 AI 兜底）→
    ⑤AI 生成兜底
    """
    _ops_check(x_ops_username, x_ops_password)
    from app.services import ctsf_import
    from app.services.textbook_service import GRADE_CN as _G_CN, SEMESTER_CN as _S_CN
    from app.services.textbook_service import book_pdf_path
    import os as _os
    grade_cn = next((g for g, n in _G_CN.items() if n == req.grade), "")
    sem_cn = next((s for s, n in _S_CN.items() if n == req.semester), "")

    # 定位 ctsf OUTLINES 条目（①③ 共用）
    target = None
    for source, subj, ver, fn in ctsf_import.OUTLINES:
        meta = ctsf_import.parse_book_meta(fn)
        if subj == req.subject and ver == req.version and meta.get("grade") == req.grade \
                and meta.get("semester") == req.semester:
            target = (source, subj, ver, fn)
            break

    # ① 在线知识大纲（纯在线，不读缓存；成功自动写缓存）
    if target:
        try:
            outline = ctsf_import.fetch_outline(target[0], target[3], use_cache=False)
            r = _sync_import_outline(outline, req.subject, req.version,
                                     req.grade, req.semester, "ctsf-online")
            return {"method": "ctsf-online", "done": True, **r}
        except Exception:
            pass  # 在线失败 → 降级

    # ② 本地权威大纲缓存（优先于在线教材：已下载过的权威大纲准确性高、秒级导入）
    if target and ctsf_import.local_outline_exists(target[0], target[3]):
        outline = ctsf_import.load_local_outline(target[0], target[3])
        r = _sync_import_outline(outline, req.subject, req.version,
                                 req.grade, req.semester, "ctsf-local")
        return {"method": "ctsf-local", "done": True, **r}

    # ③ 本地教材 PDF（教材库中已放置的 PDF，优先于在线下载：无需下载、内容可控）
    local_book = {"subject": req.subject, "version": req.version,
                  "grade": grade_cn, "semester": sem_cn}
    if _os.path.exists(book_pdf_path(local_book)):
        task = _start_ops_pdf_task(req, local_book, download=False, source_type="textbook-local")
        return {"method": "textbook-local", "done": False, "task_id": task["id"]}

    # ④ 在线教材资源（index.json 有下载源；skip_online_textbook=True 时跳过）
    book = None
    if not req.skip_online_textbook:
        book = _match_index_book_strict(req.subject, req.version, grade_cn, sem_cn)
    if book and book.get("downloads"):
        task = _start_ops_pdf_task(req, book, download=True, source_type="textbook-online")
        return {"method": "textbook-online", "done": False, "task_id": task["id"]}

    # ⑤ AI 生成
    task = _start_ops_ai_task(req)
    return {"method": "ai", "done": False, "task_id": task["id"]}


# ---------------------------------------------------------------- 分组列表（按单元分组，保序）

def _load_tags_ops(tags) -> list:
    import json as _json
    if not tags:
        return []
    try:
        return _json.loads(tags) if isinstance(tags, str) else list(tags)
    except Exception:
        return []


@router.get("/knowledge-points/grouped")
def ops_kp_grouped(subject: str, version: str,
                   grade: Optional[int] = None, semester: Optional[int] = None,
                   x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    """知识点按单元分组列表（单元按首次出现顺序，单元内按导入顺序）"""
    _ops_check(x_ops_username, x_ops_password)
    db = _db()
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
        rows = q.order_by(OpsKnowledgePoint.id).all()
        groups = []
        idx = {}
        for row in rows:
            ch = row.chapter or "未分组"
            if ch not in idx:
                idx[ch] = len(groups)
                groups.append({"chapter": ch, "items": []})
            groups[idx[ch]]["items"].append({
                "id": row.id, "name": row.name, "chapter": ch,
                "description": row.description or "", "requirement": row.requirement or "",
                "tags": _load_tags_ops(row.tags), "kp_type": row.kp_type or "",
                "source_type": row.source_type or "", "revision": row.revision or "",
                "ocr_mode": row.ocr_mode or "",
            })
        return {"groups": groups, "total": len(rows)}
    finally:
        db.close()


# ---------------------------------------------------------------- AI 出题规则（prompt 维护）

@router.get("/prompt-rules")
def ops_prompt_rules_list(x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    """出题规则清单：内置全部 scope + 运营已保存覆盖（未保存显示默认规则文本）。"""
    _ops_check(x_ops_username, x_ops_password)
    db = _db()
    try:
        rows = {r.scope: r for r in db.query(OpsPromptRule).all()}
        items = []
        for meta in SCOPE_META:
            row = rows.get(meta["scope"])
            saved = bool(row and row.rule_text and row.rule_text.strip())
            rule_text = row.rule_text if saved else get_scope_default_text(meta["scope"])
            items.append({
                "scope": meta["scope"],
                "group": meta["group"],
                "title": meta["title"],
                "tip": meta["tip"],
                "rule_text": rule_text,
                "enabled": row.enabled if row else True,
                "is_default": not saved,
            })
        return {"items": items}
    finally:
        db.close()


class PromptRuleItem(BaseModel):
    scope: str = ""
    rule_text: str = ""


class PromptRulesSaveRequest(BaseModel):
    rules: List[PromptRuleItem] = []


@router.put("/prompt-rules")
def ops_prompt_rules_save(data: PromptRulesSaveRequest,
                          x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    """批量保存出题规则：非空文本 upsert 启用；空文本=删除记录恢复默认。"""
    _ops_check(x_ops_username, x_ops_password)
    db = _db()
    try:
        valid_scopes = {m["scope"] for m in SCOPE_META}
        saved = []
        for item in data.rules:
            scope = (item.scope or "").strip()
            if scope not in valid_scopes:
                continue
            text = (item.rule_text or "").strip()
            row = db.query(OpsPromptRule).filter(OpsPromptRule.scope == scope).first()
            default_text = get_scope_default_text(scope)
            if not text or (default_text and text == default_text):
                # 空文本 或 与内置默认一致 → 恢复默认（删除记录）
                if row is not None:
                    db.delete(row)
                saved.append({"scope": scope, "is_default": True})
                continue
            if row is None:
                row = OpsPromptRule(scope=scope, rule_text=text, enabled=True)
                db.add(row)
            else:
                row.rule_text = text
                row.enabled = True
            saved.append({"scope": scope, "is_default": False})
        db.commit()
        return {"ok": True, "saved": saved}
    finally:
        db.close()


# ---------------------------------------------------------------- 评测规则（组卷/排重/坏题校验参数）

@router.get("/assess-rules")
def ops_assess_rules_list(x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    """评测规则清单：全部配置项 + 运营已保存覆盖（未保存显示内置默认值）。"""
    _ops_check(x_ops_username, x_ops_password)
    db = _db()
    try:
        rows = {r.key: r for r in db.query(OpsAssessRule).all()}
        items = []
        for meta in ASSESS_RULES_META:
            row = rows.get(meta["key"])
            saved = bool(row and row.value and str(row.value).strip())
            value = row.value if saved else meta["default"]
            items.append({
                "key": meta["key"],
                "group": meta["group"],
                "title": meta["title"],
                "tip": meta["tip"],
                "value_type": meta["value_type"],
                "default": meta["default"],
                "value": value,
                "is_default": not saved,
            })
        return {"items": items}
    finally:
        db.close()


class AssessRuleItem(BaseModel):
    key: str = ""
    value: str = ""


class AssessRulesSaveRequest(BaseModel):
    rules: List[AssessRuleItem] = []


@router.put("/assess-rules")
def ops_assess_rules_save(data: AssessRulesSaveRequest,
                          x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    """批量保存评测规则：非空文本 upsert 启用；空文本=删除记录恢复默认。"""
    _ops_check(x_ops_username, x_ops_password)
    db = _db()
    try:
        valid_keys = {m["key"] for m in ASSESS_RULES_META}
        saved = []
        for item in data.rules:
            key = (item.key or "").strip()
            if key not in valid_keys:
                continue
            text = (item.value or "").strip()
            row = db.query(OpsAssessRule).filter(OpsAssessRule.key == key).first()
            default = get_rule_default(key)
            # 空 或 与内置默认一致 → 恢复默认（删除记录）
            if not text or (default is not None and str(text) == str(default)):
                if row is not None:
                    db.delete(row)
                saved.append({"key": key, "is_default": True})
                continue
            if row is None:
                row = OpsAssessRule(key=key, value=text, enabled=True)
                db.add(row)
            else:
                row.value = text
                row.enabled = True
            saved.append({"key": key, "is_default": False})
        db.commit()
        return {"ok": True, "saved": saved}
    finally:
        db.close()

