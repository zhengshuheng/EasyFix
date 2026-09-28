from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, UniqueConstraint
from app.database import Base
from app.utils.timeutil import now_local


class KidTextbook(Base):
    """小孩教材版本偏好（按学科绑定；知识点本体仍为全家共享一份）"""
    __tablename__ = "kid_textbook"
    __table_args__ = (UniqueConstraint("kid_id", "subject_id", name="uq_kid_textbook_kid_subject"),)

    id = Column(Integer, primary_key=True, autoincrement=True)
    kid_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)  # 小孩
    subject_id = Column(Integer, ForeignKey("subject.id"), nullable=False)       # 学科
    edition_key = Column(String(50), nullable=False)  # 教材身份（如 math-rj-2022）
    version_name = Column(String(100), nullable=False)  # 版本显示名（如 人教版数学（2022课标版））
    source = Column(String(20), default="package", nullable=False)  # package=下载包 / local=本地AI提取兜底
    created_at = Column(DateTime, default=now_local, server_default=func.now())
    updated_at = Column(DateTime, default=now_local, onupdate=now_local)
