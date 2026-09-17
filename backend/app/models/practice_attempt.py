"""作答记录模型。

每次提交做题结果都**追加一行**（不覆盖），这是统计的唯一事实来源：
- 错题的"复习次数/正确率/连续答对"都由这里聚合，或由这里的写入驱动缓存列更新。
- 删除练习集时**保留**作答记录，避免统计凭空丢失。
"""
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, func, Boolean, Float, Index,
)
from sqlalchemy.orm import relationship
from app.database import Base


class PracticeAttempt(Base):
    __tablename__ = "practice_attempt"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)  # 归属小孩
    practice_set_id = Column(Integer, ForeignKey("practice_set.id"), nullable=True, index=True)
    practice_question_id = Column(Integer, ForeignKey("practice_question.id"), nullable=False, index=True)
    error_question_id = Column(
        Integer, ForeignKey("error_question.id"), nullable=True, index=True,
        comment="该次作答对应的错题（用于错题统计聚合）",
    )

    student_answer = Column(Text, nullable=True)
    is_correct = Column(Boolean, nullable=True)  # None=未判（主观题待批改）
    duration_seconds = Column(Integer, nullable=True)  # 用时（秒）
    graded_by = Column(String(20), nullable=True)  # auto=自动判分, manual=人工批改, ai=AI 批改
    accuracy = Column(Float, nullable=True)  # 主观题得分率 0-100

    answered_at = Column(DateTime, server_default=func.now(), index=True)

    # Relationships
    practice_question = relationship("PracticeQuestion", back_populates="attempts")
    error_question = relationship("ErrorQuestion", back_populates="practice_attempts")

    __table_args__ = (
        Index("ix_practice_attempt_user_time", "user_id", "answered_at"),
    )
