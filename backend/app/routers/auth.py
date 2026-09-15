from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional

from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.utils.auth import create_token, get_current_user, verify_password

router = APIRouter(prefix="/api/auth", tags=["认证"])


class LoginRequest(BaseModel):
    username: str
    password: Optional[str] = None
    pin: Optional[str] = None


def user_dict(user: User) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "display_name": user.display_name or user.username,
        "role": user.role,
        "avatar": user.avatar,
    }


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """家长：用户名+密码；小孩：用户名+PIN"""
    user = db.query(User).filter_by(username=data.username.strip()).first()
    if not user:
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    if not user.enabled:
        raise HTTPException(status_code=403, detail="账号已被禁用")

    if user.role == "admin":
        if not data.password or not verify_password(data.password, user.password_hash):
            raise HTTPException(status_code=401, detail="用户名或密码错误")
    # 小孩无需密码：仅校验账号存在且启用（PIN 字段保留兼容，不再作为登录凭据）
    else:
        if data.pin and data.pin.strip() != (user.pin or ""):
            raise HTTPException(status_code=401, detail="PIN 码错误")

    return {
        "token": create_token(user),
        "role": user.role,
        "user": user_dict(user),
    }


@router.get("/me")
def me(user: User = Depends(get_current_user)):
    """当前登录用户信息"""
    return user_dict(user)
