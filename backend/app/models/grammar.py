from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Boolean, func
from sqlalchemy.orm import relationship
from app.database import Base
from app.utils.timeutil import now_local


class GrammarLesson(Base):
    """语法教程（英语专项）：一个语法点一条，内容由 AI 按板块批量生成、家长可编辑。

    板块示例：词法·名词 / 词法·动词 / 词法·代词 / 词法·形副 / 词法·其他 / 句法
    content_md 为教程正文（Markdown），examples/common_mistakes 为 JSON 数组。
    """
    __tablename__ = "grammar_lesson"

    id = Column(Integer, primary_key=True, autoincrement=True)
    subject_id = Column(Integer, ForeignKey("subject.id"), nullable=False)  # 英语学科
    grade = Column(Integer, nullable=True)  # 适用年级 1-12（可空=通用于各年级）
    semester = Column(Integer, nullable=True)  # 学期 1-2
    category = Column(String(100), nullable=False, index=True)  # 板块，如 词法·动词 / 句法
    title = Column(String(200), nullable=False)  # 语法点标题，如 be 动词（am/is/are）
    summary = Column(String(500), nullable=True)  # 一句话总结（易懂易记）
    content_md = Column(Text, nullable=True)  # 教程正文 Markdown
    examples = Column(Text, nullable=True)  # JSON 数组：[{"en": "...", "zh": "..."}, ...]
    common_mistakes = Column(Text, nullable=True)  # JSON 数组：["...", ...] 易错点
    mnemonic = Column(String(500), nullable=True)  # 记忆口诀/顺口溜
    order_index = Column(Integer, default=0)  # 板块内排序
    source = Column(String(20), default="ai")  # ai=AI生成 manual=手写/编辑
    deleted = Column(Boolean, default=False, nullable=False)  # 软删除标记
    created_at = Column(DateTime, default=now_local, server_default=func.now())
    updated_at = Column(DateTime, default=now_local, server_default=func.now(), onupdate=now_local)

    # Relationships
    subject = relationship("Subject")


class GrammarProgress(Base):
    """语法学习进度（按小孩隔离）：学过/练过哪个语法点、最近一次练习情况。"""
    __tablename__ = "grammar_progress"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)  # 归属小孩
    lesson_id = Column(Integer, ForeignKey("grammar_lesson.id"), nullable=False, index=True)
    status = Column(String(20), default="learned")  # learned=已学 practiced=已练 mastered=已掌握
    practice_count = Column(Integer, default=0)  # 练习次数
    correct_count = Column(Integer, default=0)  # 正确题数
    total_count = Column(Integer, default=0)  # 总题数
    last_score = Column(Integer, nullable=True)  # 最近一次得分（0-100）
    first_learned_at = Column(DateTime, default=now_local, server_default=func.now())
    updated_at = Column(DateTime, default=now_local, server_default=func.now(), onupdate=now_local)
