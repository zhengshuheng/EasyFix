from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime


class QuestionBase(BaseModel):
    error_book_id: Optional[int] = None
    subject_id: int
    grade: Optional[int] = Field(default=None, ge=1, le=12)  # 年级 1-12
    semester: Optional[int] = Field(default=None, ge=1, le=2)  # 学期 1-2
    answer: Optional[str] = None
    analysis: Optional[str] = None
    difficulty: int = Field(default=3, ge=1, le=5)
    error_type: Optional[str] = None
    knowledge_point: Optional[str] = None
    tag_ids: Optional[List[int]] = []


class QuestionCreate(QuestionBase):
    original_text: Optional[str] = None
    parsed_question: Optional[str] = None
    original_image: Optional[str] = None  # 单个图片
    original_images: Optional[List[str]] = None  # 多个图片


class QuestionUpdate(BaseModel):
    subject_id: Optional[int] = None
    original_image: Optional[str] = None
    original_text: Optional[str] = None
    parsed_question: Optional[str] = None
    grade: Optional[int] = Field(default=None, ge=1, le=12)
    semester: Optional[int] = Field(default=None, ge=1, le=2)
    answer: Optional[str] = None
    analysis: Optional[str] = None
    analysis_image: Optional[str] = None
    difficulty: Optional[int] = Field(default=None, ge=1, le=5)
    error_type: Optional[str] = None
    knowledge_point: Optional[str] = None
    tag_ids: Optional[List[int]] = None


# 批量创建错题
class QuestionBatchCreate(BaseModel):
    """批量创建错题（用于OCR后一道图生成多题）"""
    error_book_id: Optional[int] = None
    subject_id: int
    grade: Optional[int] = Field(default=None, ge=1, le=12)
    semester: Optional[int] = Field(default=None, ge=1, le=2)
    images: List[str]  # 关联的图片路径列表
    questions: List[QuestionCreate]  # 多个题目


class TagResponse(BaseModel):
    id: int
    name: str
    color: Optional[str] = None

    class Config:
        from_attributes = True


class SimilarQuestionResponse(BaseModel):
    id: int
    similar_text: str
    similar_answer: Optional[str] = None
    similarity_score: Optional[float] = None
    generated_at: datetime

    class Config:
        from_attributes = True


class QuestionResponse(BaseModel):
    id: int
    error_book_id: Optional[int] = None
    subject_id: int
    original_image: Optional[str] = None  # 单个图片
    original_images: Optional[List[str]] = None  # 多个图片
    original_text: Optional[str] = None
    parsed_question: Optional[str] = None
    visual: Optional[dict] = None  # 原题配图场景（来自 source_practice_question.visual，图例渲染用）
    grade: Optional[int] = None  # 年级 1-12
    semester: Optional[int] = None  # 学期 1-2
    answer: Optional[str] = None
    analysis: Optional[str] = None
    analysis_image: Optional[str] = None
    difficulty: int
    error_type: Optional[str] = None
    knowledge_point: Optional[str] = None
    question_type: Optional[str] = None  # 题型：choice/fill/judge/calc/...
    question_category: Optional[str] = None  # 类型：basic/scene/comprehensive/thinking
    option_a: Optional[str] = None
    option_b: Optional[str] = None
    option_c: Optional[str] = None
    option_d: Optional[str] = None
    correct_count: Optional[int] = 0
    error_count: Optional[int] = 0
    review_count: Optional[int] = 0  # 复习（作答）次数
    accuracy: Optional[float] = None  # 正确率百分比（缓存）
    correct_streak: Optional[int] = 0  # 连续答对次数（>=2 已掌握）
    status: Optional[str] = "active"  # active=在错题本 / mastered=已掌握
    source: Optional[str] = None  # practice=批改判错派生 / upload=手动上传
    created_at: datetime
    updated_at: Optional[datetime] = None
    tags: List[TagResponse] = []
    similar_questions: List[SimilarQuestionResponse] = []

    class Config:
        from_attributes = True


class QuestionListResponse(BaseModel):
    total: int
    items: List[QuestionResponse]


class BatchCreateResponse(BaseModel):
    """批量创建响应"""
    questions: List[QuestionResponse]
    total_count: int
    success_count: int
