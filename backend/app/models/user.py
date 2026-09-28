from sqlalchemy import Column, Integer, String, Boolean, DateTime, Date, func
from sqlalchemy.orm import relationship
from app.database import Base
from app.utils.timeutil import now_local


class User(Base):
    """本地用户（家长/小孩）"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    display_name = Column(String(50), nullable=True)
    password_hash = Column(String(200), nullable=True)  # 家长密码（PBKDF2）
    pin = Column(String(10), nullable=True)             # 小孩 4 位 PIN
    role = Column(String(10), nullable=False, default="child")  # admin / child
    is_owner = Column(Boolean, nullable=False, default=False)   # 空间主账号=官网注册家长，每空间仅 1 个，不可删除
    avatar = Column(String(200), nullable=True)
    enabled = Column(Boolean, default=True)
    current_grade = Column(Integer, nullable=True, default=1)  # 兼容旧字段：已由 enrollment_date 推断替代
    enrollment_date = Column(Date, nullable=True)  # 一年级入学日期（9月1日开学），据此推断当前年级
    created_at = Column(DateTime, default=now_local, server_default=func.now())

    # 错题本（按小孩隔离）
    error_books = relationship("ErrorBook", back_populates="owner")
