"""
阅读理解路由 - 短文库管理、话题列表
"""
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import Optional

from app.database import get_db
from app.models import ReadingPassage, ReadingQuestion
from app.schemas.reading import (
    ReadingPassageCreate,
    ReadingPassageUpdate,
    ReadingPassageResponse,
    ReadingPassageListResponse,
    ReadingQuestionCreate,
    GenerateReadingRequest,
)

router = APIRouter(prefix="/api/readings", tags=["阅读理解"])

# 预设话题列表
TOPICS = [
    "校园生活", "家庭生活", "日常生活", "兴趣爱好",
    "科技发展", "环境保护", "文化艺术", "体育运动",
    "健康与医疗", "旅行与地理", "节日与习俗", "历史人物",
    "未来职业", "人际交往", "饮食文化", "动物与自然",
]


@router.get("/topics", response_model=list)
def get_topics():
    """获取可选话题列表"""
    return TOPICS


@router.post("/generate", status_code=201)
def generate_reading(data: GenerateReadingRequest, db: Session = Depends(get_db)):
    """
    调用LLM生成英语短文 + 配套选择题，保存到数据库
    """
    from app.services.llm import llm_service

    # 1. 生成短文
    passage_result = llm_service.generate_reading_passage(
        grade=data.grade,
        topic=data.topic,
        difficulty=data.difficulty,
    )

    if "error" in passage_result:
        raise HTTPException(status_code=500, detail=f"短文生成失败: {passage_result['error']}")

    if not passage_result.get("content"):
        raise HTTPException(status_code=500, detail="生成了空短文")

    # 2. 生成选择题
    questions_result = llm_service.generate_reading_questions(
        passage_content=passage_result["content"]
    )

    if "error" in questions_result:
        raise HTTPException(status_code=500, detail=f"选择题生成失败: {questions_result['error']}")

    raw_questions = questions_result.get("questions", [])
    if not raw_questions:
        raise HTTPException(status_code=500, detail="未生成选择题")

    # 3. 保存到数据库
    passage = ReadingPassage(
        title=passage_result["title"],
        content=passage_result["content"],
        topic=data.topic,
        grade=data.grade,
        difficulty=data.difficulty,
        word_count=passage_result.get("word_count") or len(passage_result["content"].split()),
        source="generated",
    )
    db.add(passage)
    db.flush()

    for i, q in enumerate(raw_questions[:4]):
        question = ReadingQuestion(
            passage_id=passage.id,
            question_number=q.get("question_number", i + 1),
            question_text=q.get("question_text", ""),
            option_a=q.get("option_a", ""),
            option_b=q.get("option_b", ""),
            option_c=q.get("option_c", ""),
            option_d=q.get("option_d", ""),
            correct_answer=q.get("correct_answer", "A"),
            explanation=q.get("explanation", ""),
        )
        db.add(question)

    db.commit()
    db.refresh(passage)

    return passage


@router.get("", response_model=ReadingPassageListResponse)
def list_readings(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    topic: Optional[str] = None,
    grade: Optional[int] = Query(None, ge=1, le=12),
    difficulty: Optional[int] = Query(None, ge=1, le=5),
    db: Session = Depends(get_db),
):
    """获取短文列表（支持筛选）"""
    query = db.query(ReadingPassage).filter(ReadingPassage.deleted == False).options(
        joinedload(ReadingPassage.questions)
    )

    if topic:
        query = query.filter(ReadingPassage.topic == topic)
    if grade:
        query = query.filter(ReadingPassage.grade == grade)
    if difficulty:
        query = query.filter(ReadingPassage.difficulty == difficulty)

    total = query.count()
    items = query.order_by(ReadingPassage.created_at.desc()).offset(skip).limit(limit).all()

    return {"total": total, "items": items}


@router.get("/{reading_id}", response_model=ReadingPassageResponse)
def get_reading(reading_id: int, db: Session = Depends(get_db)):
    """获取短文详情（含选择题）"""
    passage = db.query(ReadingPassage).options(
        joinedload(ReadingPassage.questions)
    ).filter(
        ReadingPassage.id == reading_id,
        ReadingPassage.deleted == False
    ).first()

    if not passage:
        raise HTTPException(status_code=404, detail="短文不存在")

    return passage


@router.post("", response_model=ReadingPassageResponse, status_code=201)
def create_reading(data: ReadingPassageCreate, db: Session = Depends(get_db)):
    """手动创建短文 + 选择题"""
    passage = ReadingPassage(
        title=data.title,
        content=data.content,
        topic=data.topic,
        grade=data.grade,
        difficulty=data.difficulty,
        word_count=data.word_count or len(data.content.split()),
        source="manual",
    )
    db.add(passage)
    db.flush()

    for q in data.questions:
        question = ReadingQuestion(
            passage_id=passage.id,
            question_number=q.question_number,
            question_text=q.question_text,
            option_a=q.option_a,
            option_b=q.option_b,
            option_c=q.option_c,
            option_d=q.option_d,
            correct_answer=q.correct_answer,
            explanation=q.explanation,
        )
        db.add(question)

    db.commit()
    db.refresh(passage)

    return passage


@router.put("/{reading_id}", response_model=ReadingPassageResponse)
def update_reading(reading_id: int, data: ReadingPassageUpdate, db: Session = Depends(get_db)):
    """更新短文信息（标题、话题、年级、难度）"""
    passage = db.query(ReadingPassage).filter(
        ReadingPassage.id == reading_id,
        ReadingPassage.deleted == False
    ).first()

    if not passage:
        raise HTTPException(status_code=404, detail="短文不存在")

    update_data = data.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(passage, key, value)

    db.commit()
    db.refresh(passage)

    return passage


@router.delete("/{reading_id}", status_code=204)
def delete_reading(reading_id: int, db: Session = Depends(get_db)):
    """软删除短文"""
    passage = db.query(ReadingPassage).filter(
        ReadingPassage.id == reading_id,
        ReadingPassage.deleted == False
    ).first()

    if not passage:
        raise HTTPException(status_code=404, detail="短文不存在")

    passage.deleted = True
    db.commit()
