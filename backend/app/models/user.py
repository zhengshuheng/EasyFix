from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.database import Base


class User(Base):
    """本地用户（家长/小孩）"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    display_name = Column(String(50), nullable=True)
    password_hash = Column(String(200), nullable=True)  # 家长密码（PBKDF2）
    pin = Column(String(10), nullable=True)             # 小孩 4 位 PIN
    role = Column(String(10), nullable=False, default="child")  # admin / child
    avatar = Column(String(200), nullable=True)
    enabled = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    # 错题本（按小孩隔离）
    error_books = relationship("ErrorBook", back_populates="owner")
