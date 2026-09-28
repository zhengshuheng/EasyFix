"""练习题目模型（快照）。

练习卷一旦生成，题目即固化为快照——之后修改/删除错题都不会影响历史练习卷和统计，
这是"错题库与练习库隔离但互相可查"的实现基础：
- practice_question.error_question_id → 该练习题目复习的是哪道错题
- error_question.source_practice_question_id → 该错题第一次是在哪道练习题目上错的
"""
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, func, Boolean, CheckConstraint, Index,
)
from sqlalchemy.orm import relationship
from app.database import Base
from app.utils.timeutil import now_local


class PracticeQuestion(Base):
    __tablename__ = "practice_question"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)  # 归属小孩
    subject_id = Column(Integer, ForeignKey("subject.id"), nullable=False)

    # 题目内容（出卷时刻的快照）
    original_text = Column(Text, nullable=True)  # 来源原文（错题复习时复制错题题干）
    original_images = Column(Text, nullable=True)  # JSON 数组（错题带图时复制）
    parsed_question = Column(Text, nullable=True)  # 题干
    answer = Column(Text, nullable=True)
    analysis = Column(Text, nullable=True)
    option_a = Column(Text, nullable=True)
    option_b = Column(Text, nullable=True)
    option_c = Column(Text, nullable=True)
    option_d = Column(Text, nullable=True)

    # 分类信息
    grade = Column(Integer, nullable=True)
    semester = Column(Integer, nullable=True)
    question_type = Column(String(50), nullable=True)
    question_category = Column(String(50), nullable=True)
    knowledge_point = Column(String(200), nullable=True)
    difficulty = Column(Integer, default=3)
    error_type = Column(String(50), nullable=True)

    # 来源：ai=AI 出题；error_review=错题复习组卷；upload=手动录入
    source = Column(String(20), default="ai", nullable=False)
    error_question_id = Column(
        Integer, ForeignKey("error_question.id"), nullable=True,
        comment="该题复习的错题（错题复习卷有值）",
    )
    # 配图场景：结构化 JSON（AI 出题时生成），如 {"type":"group","emoji":"🍪","groups":3,"per_group":5}
    visual = Column(Text, nullable=True, comment="结构化配图场景描述（JSON）")

    deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=now_local, server_default=func.now())

    __table_args__ = (
        CheckConstraint("difficulty >= 1 AND difficulty <= 5", name="check_pquestion_difficulty"),
        Index("ix_practice_question_user", "user_id", "deleted"),
    )

    # Relationships
    attempts = relationship("PracticeAttempt", back_populates="practice_question")
