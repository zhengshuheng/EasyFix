import json
import re
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, or_
from typing import List, Optional
from pydantic import BaseModel, Field
from app.database import get_db
from app.models import KnowledgePoint, Subject, ErrorType
from app.models.knowledge_point import ensure_kp_dimension_columns, ensure_kp_package_columns
from app.services.textbook_meta import TEXTBOOK_VERSIONS, edition_key_for
from app.services.textbook_service import _llm_json, _parse_json

# 启动即建列（幂等），保证旧库可用
ensure_kp_dimension_columns()
ensure_kp_package_columns()

router = APIRouter(prefix="/api/knowledge-points", tags=["知识点"])

TAG_OPTIONS = ["重点", "难点", "易错点"]
REQUIREMENT_OPTIONS = ["识记", "理解", "背诵", "运用", "综合"]

# 单元语义排序支持：中文数字转阿拉伯（支持 一~九十九，如 十/十五/二十一）
_CN_NUM = {"零": 0, "一": 1, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9}


def _cn2num(s: str) -> int:
    if not s:
        return 0
    if s.isdigit():
        return int(s)
    if "十" in s:
        parts = s.split("十")
        tens = _CN_NUM.get(parts[0], 1) if parts[0] else 1
        ones = _CN_NUM.get(parts[1], 0) if len(parts) > 1 and parts[1] else 0
        return tens * 10 + ones
    return _CN_NUM.get(s, 99)


def _unit_num(chapter: Optional[str]):
    """提取单元序号：'第X单元/第X课/第X章'（含中文数字）或 'Unit N'；识别不到返回 None"""
    if not chapter:
        return None
    m = re.search(r"第\s*([零一二三四五六七八九十百\d]+)\s*[课单元章篇]", chapter)
    if m:
        return _cn2num(m.group(1))
    m = re.search(r"(?:unit|lesson|part|module|section)\s*(\d+)", chapter, re.I)
    if m:
        return int(m.group(1))
    return None


# 人教版数学各年级单元顺序（无「第X单元」前缀的历史数据按此排）
_MATH_RJB_UNITS = {
    (1, 1): ["准备课", "位置", "1~5的认识和加减法", "认识图形（一）", "6~10的认识和加减法",
             "11~20各数的认识", "认识钟表", "20以内的进位加法", "总复习"],
    (2, 1): ["长度单位", "100以内的加法和减法（二）", "角的初步认识", "观察物体（一）",
             "表内乘法（一）", "表内乘法（二）", "认识时间", "数学广角——搭配（一）", "总复习"],
    (3, 1): ["时、分、秒", "万以内的加法和减法（一）", "测量", "万以内的加法和减法（二）",
             "倍的认识", "多位数乘一位数", "长方形和正方形", "分数的初步认识", "数学广角——集合", "总复习"],
}


def _kp_sort_key(kp):
    """知识点语义排序：学科 → 年级 → 学期 → 单元序号 → 章节名 → 知识点名"""
    unit = _unit_num(kp.chapter)
    if unit is None:
        rjb = _MATH_RJB_UNITS.get((kp.grade, kp.semester))
        if rjb and (kp.chapter or "").strip() in rjb:
            unit = rjb.index(kp.chapter.strip()) + 1
    return (
        kp.subject_id or 999,
        kp.grade if kp.grade is not None else 999,
        kp.semester if kp.semester is not None else 999,
        0 if unit is not None else 1,   # 带单元序号排前
        unit if unit is not None else 0,
        (kp.chapter or "").lower(),
        (kp.name or "").lower(),
    )


def _parse_tags(raw) -> List[str]:
    if not raw:
        return []
    try:
        v = json.loads(raw)
        return v if isinstance(v, list) else []
    except Exception:
        return []


def _dump_tags(tags) -> Optional[str]:
    if not tags:
        return None
    seen = []
    for t in tags:
        if t and t not in seen:
            seen.append(t)
    return json.dumps(seen, ensure_ascii=False)


class ErrorTypeSimple(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class KnowledgePointResponse(BaseModel):
    id: int
    name: str
    subject_id: int
    subject_name: Optional[str] = None
    grade: Optional[int] = None
    semester: Optional[int] = None
    version: Optional[str] = None
    source: Optional[str] = None
    edition_key: Optional[str] = None
    chapter: Optional[str] = None
    tags: List[str] = []
    requirement: Optional[str] = None
    kp_type: Optional[str] = None
    created_at: Optional[str] = None
    error_types: List[ErrorTypeSimple] = []

    class Config:
        from_attributes = True


class KnowledgePointCreate(BaseModel):
    name: str
    subject_id: int
    grade: Optional[int] = None
    semester: Optional[int] = None
    chapter: Optional[str] = None
    version: Optional[str] = None
    source: Optional[str] = None  # textbook=教材内置 / custom=自定义（缺省 custom）
    edition_key: Optional[str] = None
    description: Optional[str] = None
    tags: Optional[List[str]] = []
    requirement: Optional[str] = None
    kp_type: Optional[str] = None
    error_type_ids: Optional[List[int]] = []


class KnowledgePointAIGenerateRequest(BaseModel):
    """AI 智能导入：大模型按教材知识/自然语言指令生成单元知识点清单"""
    mode: str = Field("custom", description="textbook=按教材下拉生成；custom=按自然语言指令生成")
    subject_id: Optional[int] = None
    version: Optional[str] = Field(None, max_length=100)
    grade: Optional[int] = Field(None, ge=1, le=12)
    semester: Optional[int] = Field(None, ge=1, le=2)
    instruction: Optional[str] = Field(None, max_length=500)


class KnowledgePointUpdate(BaseModel):
    name: Optional[str] = None
    subject_id: Optional[int] = None
    grade: Optional[int] = None
    semester: Optional[int] = None
    chapter: Optional[str] = None
    tags: Optional[List[str]] = None
    requirement: Optional[str] = None
    kp_type: Optional[str] = None
    error_type_ids: Optional[List[int]] = None


@router.get("/options", response_model=dict)
def knowledge_point_options(subject_id: Optional[int] = None, db: Session = Depends(get_db)):
    """过滤选项：标签、要求、内容类型（类型按学科 distinct 收集）"""
    q = db.query(KnowledgePoint).filter(KnowledgePoint.deleted == False)
    if subject_id:
        q = q.filter(KnowledgePoint.subject_id == subject_id)
    type_set = set()
    requirement_set = set()
    tag_set = set()
    for kp in q.all():
        if kp.kp_type:
            type_set.add(kp.kp_type)
        if kp.requirement:
            requirement_set.add(kp.requirement)
        for t in _parse_tags(kp.tags):
            tag_set.add(t)
    return {
        "tags": TAG_OPTIONS,
        "requirements": REQUIREMENT_OPTIONS,
        "kp_types": sorted(type_set),
        "existing_requirements": sorted(requirement_set),
    }


@router.get("/textbook-versions", response_model=dict)
def textbook_versions():
    """教材版本选项（按学科）——建小孩/账号管理选教材版本用"""
    return {"versions": TEXTBOOK_VERSIONS}


@router.get("", response_model=List[KnowledgePointResponse])
def list_knowledge_points(
    subject_id: Optional[int] = None,
    grade: Optional[int] = None,
    semester: Optional[int] = None,
    tag: Optional[str] = None,  # 教学标签，任一命中（可逗号分隔）
    requirement: Optional[str] = None,
    kp_type: Optional[str] = None,
    edition_key: Optional[str] = None,  # 小孩绑定的教材版本：只返回 该版本 + 通用教材 + 自定义
    db: Session = Depends(get_db),
):
    """获取知识点列表（排除已删除的）"""
    query = db.query(KnowledgePoint).filter(KnowledgePoint.deleted == False)

    if subject_id:
        query = query.filter(KnowledgePoint.subject_id == subject_id)
    if grade:
        query = query.filter(KnowledgePoint.grade == grade)
    if semester:
        query = query.filter(KnowledgePoint.semester == semester)
    if requirement:
        query = query.filter(KnowledgePoint.requirement == requirement)
    if kp_type:
        query = query.filter(KnowledgePoint.kp_type == kp_type)
    if tag:
        # tags 存 JSON 数组，任一命中即匹配
        or_clauses = [KnowledgePoint.tags.like(f'%"{t}"%') for t in tag.split(",") if t]
        if or_clauses:
            query = query.filter(or_(*or_clauses))
    if edition_key:
        # 版本过滤：自定义知识点 + 通用教材数据（edition_key 为空）+ 该小孩绑定的版本
        query = query.filter(or_(
            KnowledgePoint.source.is_(None),
            KnowledgePoint.source == "custom",
            KnowledgePoint.edition_key.is_(None),
            KnowledgePoint.edition_key == edition_key,
        ))

    knowledge_points = query.order_by(
        KnowledgePoint.grade.asc().nulls_last(),
        KnowledgePoint.semester.asc().nulls_last(),
        KnowledgePoint.chapter.asc().nulls_last(),
        KnowledgePoint.name.asc(),
    ).all()

    # 获取学科名称
    subjects = db.query(Subject).filter(Subject.deleted == False).all()
    subject_map = {s.id: s.name for s in subjects}

    result = []
    for kp in knowledge_points:
        error_types = []
        for et in kp.error_types:
            if not et.deleted:
                error_types.append(ErrorTypeSimple(id=et.id, name=et.name))
        result.append(KnowledgePointResponse(
            id=kp.id,
            name=kp.name,
            subject_id=kp.subject_id,
            subject_name=subject_map.get(kp.subject_id, ""),
            grade=kp.grade,
            semester=kp.semester,
            version=kp.version,
            source=kp.source,
            edition_key=kp.edition_key,
            chapter=kp.chapter,
            tags=_parse_tags(kp.tags),
            requirement=kp.requirement,
            kp_type=kp.kp_type,
            created_at=kp.created_at.isoformat() if kp.created_at else None,
            error_types=error_types,
        ))

    # 语义排序：学科 → 年级 → 学期 → 单元序号 → 章节名 → 知识点名
    result.sort(key=_kp_sort_key)
    return result


@router.post("", response_model=KnowledgePointResponse, status_code=201)
def create_knowledge_point(data: KnowledgePointCreate, db: Session = Depends(get_db)):
    """创建知识点"""
    subject = db.query(Subject).filter(Subject.id == data.subject_id, Subject.deleted == False).first()
    if not subject:
        raise HTTPException(status_code=400, detail="学科不存在")

    kp = KnowledgePoint(
        name=data.name,
        subject_id=data.subject_id,
        grade=data.grade,
        semester=data.semester,
        chapter=data.chapter,
        version=data.version,
        source=data.source or "custom",
        edition_key=data.edition_key,
        description=data.description,
        tags=_dump_tags(data.tags),
        requirement=data.requirement,
        kp_type=data.kp_type,
    )
    db.add(kp)
    db.flush()

    # 关联错误类型
    if data.error_type_ids:
        for et_id in data.error_type_ids:
            et = db.query(ErrorType).filter(ErrorType.id == et_id, ErrorType.deleted == False).first()
            if et:
                kp.error_types.append(et)

    db.commit()
    db.refresh(kp)

    error_types = []
    for et in kp.error_types:
        if not et.deleted:
            error_types.append(ErrorTypeSimple(id=et.id, name=et.name))

    return KnowledgePointResponse(
        id=kp.id,
        name=kp.name,
        subject_id=kp.subject_id,
        subject_name=subject.name,
        grade=kp.grade,
        semester=kp.semester,
        version=kp.version,
        source=kp.source,
        edition_key=kp.edition_key,
        chapter=kp.chapter,
        tags=_parse_tags(kp.tags),
        requirement=kp.requirement,
        kp_type=kp.kp_type,
        created_at=kp.created_at.isoformat() if kp.created_at else None,
        error_types=error_types,
    )


@router.put("/{kp_id}", response_model=KnowledgePointResponse)
def update_knowledge_point(kp_id: int, data: KnowledgePointUpdate, db: Session = Depends(get_db)):
    """更新知识点（教材内置知识点只读）"""
    kp = db.query(KnowledgePoint).filter(KnowledgePoint.id == kp_id, KnowledgePoint.deleted == False).first()
    if not kp:
        raise HTTPException(status_code=404, detail="知识点不存在")
    if kp.source == "textbook":
        raise HTTPException(status_code=403, detail="教材内置知识点只读，如需修改请在「自定义知识点」中新建")

    if data.subject_id is not None:
        subject = db.query(Subject).filter(Subject.id == data.subject_id, Subject.deleted == False).first()
        if not subject:
            raise HTTPException(status_code=400, detail="学科不存在")
        kp.subject_id = data.subject_id

    if data.name is not None:
        kp.name = data.name
    if data.grade is not None:
        kp.grade = data.grade
    if data.semester is not None:
        kp.semester = data.semester
    if data.chapter is not None:
        kp.chapter = data.chapter
    if data.tags is not None:
        kp.tags = _dump_tags(data.tags)
    if data.requirement is not None:
        kp.requirement = data.requirement
    if data.kp_type is not None:
        kp.kp_type = data.kp_type

    # 更新错误类型关联
    if data.error_type_ids is not None:
        kp.error_types = []
        for et_id in data.error_type_ids:
            et = db.query(ErrorType).filter(ErrorType.id == et_id, ErrorType.deleted == False).first()
            if et:
                kp.error_types.append(et)

    db.commit()
    db.refresh(kp)

    subject = db.query(Subject).filter(Subject.id == kp.subject_id, Subject.deleted == False).first()
    subject_name = subject.name if subject else ""

    error_types = []
    for et in kp.error_types:
        if not et.deleted:
            error_types.append(ErrorTypeSimple(id=et.id, name=et.name))

    return KnowledgePointResponse(
        id=kp.id,
        name=kp.name,
        subject_id=kp.subject_id,
        subject_name=subject_name,
        grade=kp.grade,
        semester=kp.semester,
        version=kp.version,
        chapter=kp.chapter,
        tags=_parse_tags(kp.tags),
        requirement=kp.requirement,
        kp_type=kp.kp_type,
        created_at=kp.created_at.isoformat() if kp.created_at else None,
        error_types=error_types,
    )


@router.delete("/{kp_id}", status_code=204)
def delete_knowledge_point(kp_id: int, db: Session = Depends(get_db)):
    """软删除知识点（教材内置知识点只读）"""
    kp = db.query(KnowledgePoint).filter(KnowledgePoint.id == kp_id, KnowledgePoint.deleted == False).first()
    if not kp:
        raise HTTPException(status_code=404, detail="知识点不存在")
    if kp.source == "textbook":
        raise HTTPException(status_code=403, detail="教材内置知识点只读，不能删除")

    kp.deleted = True
    db.commit()


# ---------------------------------------------------------------- AI 智能生成知识点

_KP_GRADE_CN = {1: "一年级", 2: "二年级", 3: "三年级", 4: "四年级", 5: "五年级", 6: "六年级",
                7: "初一", 8: "初二", 9: "初三", 10: "高一", 11: "高二", 12: "高三"}
_KP_SEM_CN = {1: "上学期", 2: "下学期"}


@router.post("/ai-generate")
def ai_generate_knowledge_points(req: KnowledgePointAIGenerateRequest, db: Session = Depends(get_db)):
    """AI 智能导入：大模型按教材知识/自然语言指令生成单元知识点清单（含查重）"""
    subject_name = ""
    if req.mode == "textbook":
        if not req.subject_id or not req.grade:
            raise HTTPException(status_code=400, detail="教材模式需要选择：学科、年级（版本/册次可选）")
        subj = db.query(Subject).filter(Subject.id == req.subject_id, Subject.deleted == False).first()
        if not subj:
            raise HTTPException(status_code=400, detail="学科不存在")
        subject_name = subj.name
        grade_cn = _KP_GRADE_CN.get(req.grade, "")
        sem_cn = _KP_SEM_CN.get(req.semester, "") if req.semester else ""
        desc = f"{subject_name}《{req.version or '通用教材'}》{grade_cn}{sem_cn or '全一册'}"
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
        data = _parse_json(content)
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
                "requirement": str(p.get("requirement", "")).strip() or None,
                "tags": [str(t).strip() for t in (p.get("tags") or []) if str(t).strip()],
                "kp_type": str(p.get("kp_type", "")).strip() or None,
                "existing": False,
            })

    if not items:
        raise HTTPException(status_code=502, detail="AI 返回内容无法解析为知识点，请重试")

    # 查重：name + subject_id + grade + semester + 版本 全匹配算已存在（同名不同版本不算重复）
    for it in items:
        q = db.query(KnowledgePoint).filter(
            KnowledgePoint.deleted == False,
            func.lower(KnowledgePoint.name) == it["name"].lower(),
        )
        if req.subject_id:
            q = q.filter(KnowledgePoint.subject_id == req.subject_id)
        if req.grade is not None:
            q = q.filter(KnowledgePoint.grade == req.grade)
        if req.semester is not None:
            q = q.filter(KnowledgePoint.semester == req.semester)
        if req.version:
            q = q.filter(KnowledgePoint.version == req.version)
        it["existing"] = q.first() is not None

    return {"items": items, "total": len(items), "subject_name": subject_name}
