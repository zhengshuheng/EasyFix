"""
单词相关 Pydantic Schemas
"""
import json
from pydantic import BaseModel, Field, field_validator
from typing import Optional, List
from datetime import datetime


class WordBase(BaseModel):
    """单词基础字段"""
    english: str = Field(..., min_length=1, max_length=200)
    chinese: str = Field(..., min_length=1)
    phonetic: Optional[str] = Field(None, max_length=100)
    grade: Optional[int] = Field(None, ge=1, le=12)
    semester: Optional[int] = Field(None, ge=1, le=2)
    unit: Optional[int] = Field(None, ge=1, le=99)
    unit_title: Optional[str] = Field(None, max_length=200)
    phonetic_rule: Optional[str] = None  # 拼读规则
    mnemonic: Optional[str] = None  # 联想口诀
    word_root: Optional[str] = None  # 词根词缀
    related_words: Optional[List] = None  # 相关词 [{en,cn}]
    example_sentences: Optional[List] = None  # 语境例句 [{en,zh}]（单词融入句子）


class WordCreate(WordBase):
    """创建单词"""
    tag_ids: Optional[List[int]] = []


class WordUpdate(BaseModel):
    """更新单词"""
    english: Optional[str] = Field(None, min_length=1, max_length=200)
    chinese: Optional[str] = None
    phonetic: Optional[str] = Field(None, max_length=100)
    grade: Optional[int] = Field(None, ge=1, le=12)
    semester: Optional[int] = Field(None, ge=1, le=2)
    unit: Optional[int] = Field(None, ge=1, le=99)
    unit_title: Optional[str] = Field(None, max_length=200)
    phonetic_rule: Optional[str] = None  # 拼读规则
    mnemonic: Optional[str] = None  # 联想口诀
    word_root: Optional[str] = None  # 词根词缀
    related_words: Optional[List] = None  # 相关词 [{en,cn}]
    example_sentences: Optional[List] = None  # 语境例句 [{en,zh}]
    tag_ids: Optional[List[int]] = None


class WordAIGenerateRequest(BaseModel):
    """AI 智能导入：大模型直接生成单词表"""
    mode: str = Field("custom", description="textbook=按教材下拉生成；custom=按自然语言指令生成")
    subject: Optional[str] = Field(None, max_length=50)
    version: Optional[str] = Field(None, max_length=100)
    grade: Optional[int] = Field(None, ge=1, le=12)
    semester: Optional[int] = Field(None, ge=1, le=2)
    instruction: Optional[str] = Field(None, max_length=500)


class TagResponse(BaseModel):
    """标签响应"""
    id: int
    name: str
    color: Optional[str] = None

    class Config:
        from_attributes = True


class WordResponse(WordBase):
    """单词响应"""
    id: int
    review_count: int = 0
    correct_count: int = 0
    last_reviewed_at: Optional[datetime] = None
    next_review_at: Optional[datetime] = None
    tags: List[TagResponse] = []
    created_at: datetime

    @field_validator("related_words", mode="before")
    @classmethod
    def _parse_related_words(cls, v):
        """DB 里 related_words 是 JSON 字符串列；响应时解析成 List，兼容已入库的 '[]'"""
        if isinstance(v, str):
            try:
                parsed = json.loads(v)
                return parsed if isinstance(parsed, list) else []
            except Exception:
                return []
        return v

    @field_validator("example_sentences", mode="before")
    @classmethod
    def _parse_example_sentences(cls, v):
        """DB 里 example_sentences 是 JSON 字符串列；响应时解析成 List"""
        if isinstance(v, str):
            try:
                parsed = json.loads(v)
                return parsed if isinstance(parsed, list) else []
            except Exception:
                return []
        return v

    class Config:
        from_attributes = True


class WordListResponse(BaseModel):
    """单词列表响应"""
    total: int
    items: List[WordResponse]


class ReviewLogResponse(BaseModel):
    """复习记录响应"""
    id: int
    word_id: int
    is_correct: bool
    user_answer: Optional[str] = None
    review_type: int
    reviewed_at: datetime

    class Config:
        from_attributes = True


class WordReviewSubmit(BaseModel):
    """提交复习结果

    注意：is_correct 曾有必填校验——前端未作答题目的 q.correct 为 undefined，
    JSON.stringify 会把该字段整条丢弃，导致 422 且整批学习记录丢失。
    这里给默认值兜底（缺省按错误计），从上游杜绝整批失败。
    """
    word_id: int
    is_correct: bool = False
    user_answer: Optional[str] = None
    review_type: int = Field(1, description="复习题型 1=默写, 2=选择")


class ReviewSessionSubmit(BaseModel):
    """提交复习场次"""
    session_id: int
    results: List[WordReviewSubmit]
    duration: int = Field(0, description="用时秒数")
    user_id: Optional[int] = Field(None, description="小孩ID；不传则默认第一个小孩（兼容旧前端）")


class WordStatsResponse(BaseModel):
    """单词统计响应"""
    total_words: int = 0
    total_reviews: int = 0
    total_correct: int = 0
    accuracy: float = 0.0
    mastered_words: int = 0  # 完全掌握的单词
    learning_words: int = 0  # 学习中
    new_words: int = 0  # 新单词
    grade_distribution: dict = {}  # 各年级分布
    review_today: int = 0  # 今日复习数
    due_words: int = 0  # 待复习数
    to_review_count: int = 0  # 待复习单词数（未复习+曲线到期）


class ReviewQuestion(BaseModel):
    """复习题目"""
    word_id: int
    english: str
    chinese: str
    word_length: int  # 单词长度
    options: Optional[List[str]] = None  # 选择题选项


class ReviewStartResponse(BaseModel):
    """开始复习响应"""
    session_id: int
    questions: List[ReviewQuestion]
    total: int


class MemoryCurveResponse(BaseModel):
    """记忆曲线响应"""
    word_id: int
    learning_phase: str
    interval: int
    next_review_at: Optional[datetime] = None
    review_history: List[dict] = []

    class Config:
        from_attributes = True
