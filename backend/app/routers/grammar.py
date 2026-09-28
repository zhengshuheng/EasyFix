import json
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from pydantic import BaseModel, Field
from app.database import get_db
from app.models import GrammarLesson, GrammarProgress, Subject
from app.services.textbook_service import _llm_json, _parse_json
from app.services.grammar_sync import sync_grammar_from_main

router = APIRouter(prefix="/api/grammar", tags=["语法专项"])

# 语法教程固化：语法知识点与内容由运营中心统一维护（主库权威），空间端只读。
_READONLY_MSG = "语法教程由运营中心统一管理（语法点固化、全空间一致）；内容有缺请点「同步官方教程」更新。"


def _ensure_readonly():
    raise HTTPException(status_code=403, detail=_READONLY_MSG)

_GRADE_CN = {1: "一年级", 2: "二年级", 3: "三年级", 4: "四年级", 5: "五年级", 6: "六年级"}


def _parse_json_list(raw) -> List:
    if not raw:
        return []
    try:
        v = json.loads(raw)
        return v if isinstance(v, list) else []
    except Exception:
        return []


def _dump_json(v) -> str:
    return json.dumps(v, ensure_ascii=False) if v else "[]"


# ---------------------------------------------------------------- 模型

class GrammarLessonResponse(BaseModel):
    id: int
    category: str
    title: str
    grade: Optional[int] = None
    semester: Optional[int] = None
    summary: Optional[str] = None
    content_md: Optional[str] = None
    examples: List = []
    common_mistakes: List = []
    mnemonic: Optional[str] = None
    source: Optional[str] = None
    # 进度（当前小孩）
    progress_status: Optional[str] = None
    practice_count: int = 0
    last_score: Optional[int] = None

    class Config:
        from_attributes = True


class GrammarCategoryResponse(BaseModel):
    category: str
    count: int
    learned: int  # 当前小孩已学数量


class GrammarLessonCreate(BaseModel):
    category: str
    title: str
    grade: Optional[int] = Field(None, ge=1, le=12)
    semester: Optional[int] = Field(None, ge=1, le=2)
    summary: Optional[str] = None
    content_md: Optional[str] = None
    examples: Optional[List] = None
    common_mistakes: Optional[List] = None
    mnemonic: Optional[str] = None
    order_index: int = 0


class GrammarLessonUpdate(BaseModel):
    category: Optional[str] = None
    title: Optional[str] = None
    grade: Optional[int] = None
    semester: Optional[int] = None
    summary: Optional[str] = None
    content_md: Optional[str] = None
    examples: Optional[List] = None
    common_mistakes: Optional[List] = None
    mnemonic: Optional[str] = None
    order_index: Optional[int] = None


class GrammarAISkeletonRequest(BaseModel):
    """AI 生成语法点骨架清单（板块）"""
    category: str = Field(..., max_length=100)
    grade: Optional[int] = Field(None, ge=1, le=12)
    instruction: Optional[str] = Field(None, max_length=500)


class GrammarAITutorialRequest(BaseModel):
    """AI 生成教程：单点 lesson_id，或按板块整批生成 category"""
    lesson_id: Optional[int] = None
    category: Optional[str] = None
    grade: Optional[int] = Field(None, ge=1, le=12)


class GrammarProgressRequest(BaseModel):
    lesson_id: int
    status: str = Field("learned", pattern="^(learned|practiced|mastered)$")
    score: Optional[int] = Field(None, ge=0, le=100)


def _resolve_user_id(db: Session, user_id: Optional[int]) -> Optional[int]:
    """解析当前小孩：优先显式 user_id；否则取第一个小孩（家长端调试）"""
    if user_id:
        return user_id
    from app.models.user import User
    kid = db.query(User).filter(User.role == "child").order_by(User.id).first()
    return kid.id if kid else None


def _lesson_dict(lesson: GrammarLesson, progress: Optional[GrammarProgress]) -> GrammarLessonResponse:
    return GrammarLessonResponse(
        id=lesson.id,
        category=lesson.category,
        title=lesson.title,
        grade=lesson.grade,
        semester=lesson.semester,
        summary=lesson.summary,
        content_md=lesson.content_md,
        examples=_parse_json_list(lesson.examples),
        common_mistakes=_parse_json_list(lesson.common_mistakes),
        mnemonic=lesson.mnemonic,
        source=lesson.source,
        progress_status=progress.status if progress else None,
        practice_count=progress.practice_count if progress else 0,
        last_score=progress.last_score if progress else None,
    )


# ---------------------------------------------------------------- 列表

@router.get("/categories", response_model=List[GrammarCategoryResponse])
def grammar_categories(user_id: Optional[int] = None, db: Session = Depends(get_db)):
    """板块列表：板块名 + 语法点数 + 当前小孩已学数"""
    uid = _resolve_user_id(db, user_id)
    rows = (db.query(GrammarLesson.category, func.count(GrammarLesson.id))
            .filter(GrammarLesson.deleted == False)  # noqa: E712
            .group_by(GrammarLesson.category)
            .order_by(GrammarLesson.category)
            .all())
    learned_map = {}
    if uid:
        sub = (db.query(GrammarLesson.category, func.count(GrammarProgress.id))
               .join(GrammarProgress, GrammarProgress.lesson_id == GrammarLesson.id)
               .filter(GrammarLesson.deleted == False, GrammarProgress.user_id == uid)  # noqa: E712
               .group_by(GrammarLesson.category).all())
        learned_map = dict(sub)
    return [
        GrammarCategoryResponse(category=cat, count=cnt, learned=learned_map.get(cat, 0))
        for cat, cnt in rows
    ]


@router.get("/lessons", response_model=List[GrammarLessonResponse])
def grammar_lessons(
    category: Optional[str] = None,
    grade: Optional[int] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
):
    """语法点列表（可按板块/年级过滤），带当前小孩进度"""
    q = db.query(GrammarLesson).filter(GrammarLesson.deleted == False)  # noqa: E712
    if category:
        q = q.filter(GrammarLesson.category == category)
    if grade:
        q = q.filter(GrammarLesson.grade == grade)
    lessons = q.order_by(GrammarLesson.category, GrammarLesson.grade.asc().nulls_last(), GrammarLesson.order_index, GrammarLesson.id).all()

    uid = _resolve_user_id(db, user_id)
    progress_map = {}
    if uid:
        ids = [l.id for l in lessons]
        if ids:
            for p in db.query(GrammarProgress).filter(
                GrammarProgress.user_id == uid,
                GrammarProgress.lesson_id.in_(ids),
            ).all():
                progress_map[p.lesson_id] = p
    return [_lesson_dict(l, progress_map.get(l.id)) for l in lessons]


@router.get("/lessons/{lesson_id}", response_model=GrammarLessonResponse)
def grammar_lesson_detail(lesson_id: int, user_id: Optional[int] = None, db: Session = Depends(get_db)):
    lesson = db.query(GrammarLesson).filter(
        GrammarLesson.id == lesson_id, GrammarLesson.deleted == False  # noqa: E712
    ).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="语法点不存在")
    uid = _resolve_user_id(db, user_id)
    progress = None
    if uid:
        progress = db.query(GrammarProgress).filter(
            GrammarProgress.user_id == uid, GrammarProgress.lesson_id == lesson_id
        ).first()
    return _lesson_dict(lesson, progress)


# ---------------------------------------------------------------- 同步（从运营主库更新）

@router.post("/sync-tutorials")
def sync_grammar_tutorials(db: Session = Depends(get_db)):
    """从运营中心（主库）同步语法教程到当前空间：按 id upsert + 软删多余点。

    语法点固化：同步后本空间列表与内容与主库一致；家长不可增删/编辑语法教程。
    """
    try:
        r = sync_grammar_from_main(db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"同步失败：{e}")
    return {"message": "同步完成", "created": r["created"], "updated": r["updated"], "removed": r["removed"]}


# ---------------------------------------------------------------- 管理 CRUD（已固化，只读）

@router.post("/lessons", response_model=GrammarLessonResponse, status_code=201)
def create_grammar_lesson(data: GrammarLessonCreate, db: Session = Depends(get_db)):
    _ensure_readonly()


@router.put("/lessons/{lesson_id}", response_model=GrammarLessonResponse)
def update_grammar_lesson(lesson_id: int, data: GrammarLessonUpdate, db: Session = Depends(get_db)):
    _ensure_readonly()


@router.delete("/lessons/{lesson_id}", status_code=204)
def delete_grammar_lesson(lesson_id: int, db: Session = Depends(get_db)):
    _ensure_readonly()


# ---------------------------------------------------------------- 进度

@router.post("/progress")
def update_grammar_progress(data: GrammarProgressRequest, user_id: Optional[int] = None, db: Session = Depends(get_db)):
    """记录学习/练习进度（按小孩隔离）"""
    uid = _resolve_user_id(db, user_id)
    if uid is None:
        raise HTTPException(status_code=400, detail="请先选择小孩")
    lesson = db.query(GrammarLesson).filter(
        GrammarLesson.id == data.lesson_id, GrammarLesson.deleted == False  # noqa: E712
    ).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="语法点不存在")
    progress = db.query(GrammarProgress).filter(
        GrammarProgress.user_id == uid, GrammarProgress.lesson_id == data.lesson_id
    ).first()
    if not progress:
        progress = GrammarProgress(user_id=uid, lesson_id=data.lesson_id)
        db.add(progress)
    if data.status == "practiced" and data.score is not None:
        progress.practice_count += 1
        progress.total_count += 1
        if data.score >= 60:
            progress.correct_count += 1
        progress.last_score = data.score
        progress.status = "mastered" if data.score >= 80 else "practiced"
    else:
        progress.status = data.status
    db.commit()
    return {"message": "ok", "status": progress.status, "practice_count": progress.practice_count}


# ---------------------------------------------------------------- AI 生成（已固化：由运营中心统一生成）

@router.post("/ai-generate-skeleton")
def ai_generate_skeleton(req: GrammarAISkeletonRequest, db: Session = Depends(get_db)):
    _ensure_readonly()


@router.post("/ai-generate-tutorial")
def ai_generate_tutorial(req: GrammarAITutorialRequest, db: Session = Depends(get_db)):
    _ensure_readonly()
