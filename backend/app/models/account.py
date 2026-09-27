from sqlalchemy import Column, Integer, String, DateTime, Boolean, func
from app.database import Base
from app.utils.timeutil import now_local


class Account(Base):
    """全局账号（线上身份）：与具体空间/租户解耦。

    账号 = 身份；体验空间 = 账号名下的独立数据空间（spaces 表在 registry.db）。
    订阅状态存这里（subscription_plan）：free / pro_online（云端正式）/ pro_local（本地正式）。
    role：parent（家长，空间内=体验小孩+自己的小孩） / org（机构，空间内=仅体验小孩）。
    enabled：False = 已禁用（家长在家庭中心被删除时置 False → 官网登录立即失效）。
    """
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    password_hash = Column(String(200), nullable=False)  # PBKDF2
    subscription_plan = Column(String(20), nullable=False, default="free")  # free / pro_online / pro_local
    role = Column(String(10), nullable=False, default="parent")  # parent / org
    child_name = Column(String(50), nullable=False, default="")   # 家长注册时填的小孩昵称（建空间预填）
    enabled = Column(Boolean, nullable=False, default=True)       # 禁用后官网登录失效
    # 辅助家长账号（家长中心「添加家长」创建）绑定的空间 key；主账号为空，按 username 查空间
    space_key = Column(String(100), nullable=True)
    created_at = Column(DateTime, default=now_local, server_default=func.now())
