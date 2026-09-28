from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class StarActionBase(BaseModel):
    code: str
    name: str
    star_value: int = 0
    icon: Optional[str] = None
    enabled: bool = True


class StarActionCreate(StarActionBase):
    pass


class StarActionUpdate(BaseModel):
    name: Optional[str] = None
    star_value: Optional[int] = None
    icon: Optional[str] = None
    enabled: Optional[bool] = None


class StarActionResponse(StarActionBase):
    id: int
    is_custom: bool
    ops_override: bool  # 家长（空间）自定义标记
    created_at: datetime

    class Config:
        from_attributes = True


class StarBalanceResponse(BaseModel):
    balance: int

    class Config:
        from_attributes = True


class StarRecordResponse(BaseModel):
    id: int
    action_code: str
    star_delta: int
    balance_after: int
    reason: Optional[str]
    created_at: datetime

    class Config:
        from_attributes = True


class StarsAdjustRequest(BaseModel):
    """积分调整请求"""
    delta: int
    reason: str

    class Config:
        from_attributes = True


class StarsAdjustResponse(BaseModel):
    """积分调整响应"""
    success: bool
    new_balance: int
    delta: int
    record_id: int


class IncentiveActionSetting(BaseModel):
    """家长（空间）激励自定义：行为项"""
    code: str
    star_value: int


class IncentiveAchievementSetting(BaseModel):
    """家长（空间）激励自定义：成就项"""
    code: str
    level: int
    trigger_count: int
    reward_stars: int = 0


class IncentiveSettingsRequest(BaseModel):
    """家长（空间）保存激励自定义：提交完整列表，与运营默认比较自动标记 ops_override；
    restore_all=True 时忽略列表，把本空间全部规则恢复为跟随运营默认"""
    actions: List[IncentiveActionSetting] = []
    achievements: List[IncentiveAchievementSetting] = []
    restore_all: bool = False