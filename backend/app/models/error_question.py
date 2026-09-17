"""错题库模型。

设计要点：
- 错题是**练习批改结果的派生数据**：做题判错时自动进错题库（source='practice'），
  也可手动上传（source='upload'，保留来源，不依赖练习）。
- 复习次数 / 正确率 / 错误次数用**缓存列**，在每次批改时同事务更新（事实来源是
  practice_attempt 作答记录，可随时全量重算）。
- 连续答对 2 次即判定掌握（status='mastered'），从错题本移出。
"""
from sqlalchemy import (
    Column, Integer, String, Text, DateTime, ForeignKey, func, Boolean, Float,
    CheckConstraint, Index,
)
from sqlalchemy.orm import relationship
from app.database import Base


class ErrorQuestion(Base):
    __tablename__ = "error_question"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)  # 归属小孩
    error_book_id = Column(Integer, ForeignKey("error_book.id"), nullable=True, comment="所属错题本（同小孩同学科）")
    subject_id = Column(Integer, ForeignKey("subject.id"), nullable=False)

    # 题目本体（手动上传时有 original_images/original_text；来自练习时由练习题目快照复制）
    original_image = Column(String(500), nullable=True)
    original_images = Column(Text, nullable=True)  # JSON 数组
    original_text = Column(Text, nullable=True)
    parsed_question = Column(Text, nullable=True)
    answer = Column(Text, nullable=True)
    analysis = Column(Text, nullable=True)
    analysis_image = Column(String(500), nullable=True)
    option_a = Column(Text, nullable=True)
    option_b = Column(Text, nullable=True)
    option_c = Column(Text, nullable=True)
    option_d = Column(Text, nullable=True)

    # 分类信息
    grade = Column(Integer, nullable=True)
    semester = Column(Integer, nullable=True)
    question_type = Column(String(50), nullable=True)  # choice/fill/judge/calc/application/operation/reading/writing/sentence
    question_category = Column(String(50), nullable=True)  # basic/scene/comprehensive/thinking
    knowledge_point = Column(String(200), nullable=True)
    difficulty = Column(Integer, default=3)
    error_type = Column(String(50), nullable=True)  # 计算/概念/审题/其他

    # 来源：practice=练习批改判错自动入库；upload=手动上传/拍照录入
    source = Column(String(20), default="practice", nullable=False)
    source_practice_question_id = Column(
        Integer, ForeignKey("practice_question.id"), nullable=True,
        comment="首次出错的那道练习题（手动上传时为空）",
    )

    # 统计缓存列（每次批改同事务更新；可由 practice_attempt 全量重算）
    review_count = Column(Integer, default=0, nullable=False)  # 复习次数（该题被练习的总次数）
    correct_count = Column(Integer, default=0, nullable=False)  # 答对次数
    wrong_count = Column(Integer, default=0, nullable=False)  # 答错次数
    accuracy = Column(Float, nullable=True)  # 正确率百分比（缓存）
    correct_streak = Column(Integer, default=0, nullable=False)  # 连续答对次数（>=2 判定掌握）

    status = Column(String(20), default="active", nullable=False)  # active=在错题本；mastered=已掌握（移出）
    first_wrong_at = Column(DateTime, nullable=True)
    last_wrong_at = Column(DateTime, nullable=True)

    deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), nullable=True)

    __table_args__ = (
        CheckConstraint("difficulty >= 1 AND difficulty <= 5", name="check_equestion_difficulty"),
        Index("ix_error_question_user_active", "user_id", "status", "deleted"),
    )

    # Relationships
    error_book = relationship("ErrorBook")
    practice_attempts = relationship("PracticeAttempt", back_populates="error_question")
