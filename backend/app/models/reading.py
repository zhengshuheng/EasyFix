from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class ReadingPassage(Base):
    """英语阅读理解短文库"""
    __tablename__ = "reading_passage"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(200), nullable=False, comment="短文标题")
    content = Column(Text, nullable=False, comment="英文短文内容")
    topic = Column(String(100), nullable=False, comment="话题主题")
    grade = Column(Integer, nullable=False, comment="适用年级 1-12")
    difficulty = Column(Integer, nullable=False, default=3, comment="难度 1-5")
    word_count = Column(Integer, nullable=True, comment="词数")
    source = Column(String(50), default="generated", comment="来源：generated/manual")
    deleted = Column(Boolean, default=False, nullable=False, comment="软删除标记")
    created_at = Column(DateTime, server_default=func.now())
    updated_at = Column(DateTime, onupdate=func.now(), nullable=True)

    # Relationships
    questions = relationship("ReadingQuestion", back_populates="passage", cascade="all, delete-orphan")


class ReadingQuestion(Base):
    """阅读理解选择题"""
    __tablename__ = "reading_question"

    id = Column(Integer, primary_key=True, autoincrement=True)
    passage_id = Column(Integer, ForeignKey("reading_passage.id"), nullable=False, comment="关联短文ID")
    question_number = Column(Integer, nullable=False, comment="题号 1-4")
    question_text = Column(Text, nullable=False, comment="英文题目")
    option_a = Column(String(500), nullable=False, comment="选项A")
    option_b = Column(String(500), nullable=False, comment="选项B")
    option_c = Column(String(500), nullable=False, comment="选项C")
    option_d = Column(String(500), nullable=False, comment="选项D")
    correct_answer = Column(String(1), nullable=False, comment="正确答案 A/B/C/D")
    explanation = Column(Text, nullable=True, comment="解析")
    deleted = Column(Boolean, default=False, nullable=False, comment="软删除标记")
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    passage = relationship("ReadingPassage", back_populates="questions")
