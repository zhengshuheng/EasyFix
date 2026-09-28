from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from app.utils.timeutil import now_local


class AssessmentRecord(Base):
    """能力评测记录"""
    __tablename__ = "assessment_record"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)  # 归属小孩（数据隔离）
    subject_id = Column(Integer, ForeignKey("subject.id"), nullable=False)  # 学科
    grade = Column(Integer, nullable=False)  # 年级
    total = Column(Integer, default=0)  # 总题数
    score = Column(Integer, default=0)  # 答对题数
    level = Column(String(20), nullable=True)  # 优秀/良好/待提升
    knowledge = Column(Text, nullable=True)  # JSON：知识点掌握 [{name, total, correct}]
    detail = Column(Text, nullable=True)  # JSON：逐题明细 [{question, answer, user_answer, correct, knowledge}]
    questions = Column(Text, nullable=True)  # JSON：评测集题目快照 [{question_id, stem, type, options, answer, knowledge, scene}]（start 时写入，供评测集管理/恢复）
    specialty = Column(String(50), nullable=True, index=True)  # 专项评测 key（None=综合评测；见 routers/assessment.SPECIALTIES）
    status = Column(String(20), default="done")  # in_progress=进行中 done=已完成 quit=已废弃
    created_at = Column(DateTime, default=now_local, server_default=func.now())

    # Relationships
    subject = relationship("Subject")
