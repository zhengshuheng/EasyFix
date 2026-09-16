import json
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
from app.database import get_db
from app.models import KnowledgePoint, Subject, ErrorType
from app.models.knowledge_point import ensure_kp_dimension_columns

# 启动即建列（幂等），保证旧库可用
ensure_kp_dimension_columns()

router = APIRouter(prefix="/api/knowledge-points", tags=["知识点"])

TAG_OPTIONS = ["重点", "难点", "易错点"]
REQUIREMENT_OPTIONS = ["识记", "理解", "背诵", "运用", "综合"]


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
    tags: Optional[List[str]] = []
    requirement: Optional[str] = None
    kp_type: Optional[str] = None
    error_type_ids: Optional[List[int]] = []


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


@router.get("", response_model=List[KnowledgePointResponse])
def list_knowledge_points(
    subject_id: Optional[int] = None,
    grade: Optional[int] = None,
    semester: Optional[int] = None,
    tag: Optional[str] = None,  # 教学标签，任一命中（可逗号分隔）
    requirement: Optional[str] = None,
    kp_type: Optional[str] = None,
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
            from sqlalchemy import or_
            query = query.filter(or_(*or_clauses))

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
            chapter=kp.chapter,
            tags=_parse_tags(kp.tags),
            requirement=kp.requirement,
            kp_type=kp.kp_type,
            created_at=kp.created_at.isoformat() if kp.created_at else None,
            error_types=error_types,
        ))

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
        chapter=kp.chapter,
        tags=_parse_tags(kp.tags),
        requirement=kp.requirement,
        kp_type=kp.kp_type,
        created_at=kp.created_at.isoformat() if kp.created_at else None,
        error_types=error_types,
    )


@router.put("/{kp_id}", response_model=KnowledgePointResponse)
def update_knowledge_point(kp_id: int, data: KnowledgePointUpdate, db: Session = Depends(get_db)):
    """更新知识点"""
    kp = db.query(KnowledgePoint).filter(KnowledgePoint.id == kp_id, KnowledgePoint.deleted == False).first()
    if not kp:
        raise HTTPException(status_code=404, detail="知识点不存在")

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
    """软删除知识点"""
    kp = db.query(KnowledgePoint).filter(KnowledgePoint.id == kp_id, KnowledgePoint.deleted == False).first()
    if not kp:
        raise HTTPException(status_code=404, detail="知识点不存在")

    kp.deleted = True
    db.commit()
