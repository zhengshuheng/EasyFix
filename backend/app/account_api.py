# -*- coding: utf-8 -*-
"""全局账号 API（账号/空间分离）：
- 账号 = 身份（正式库 accounts 表，订阅状态挂这里）
- 空间 = 账号名下的体验数据空间（registry.db spaces 表，见 trial.py）

注意：账号 API 统一用 /api/account/* 前缀（/api/auth/* 已被正式空间家长登录占用，
见 routers/auth.py）。账号 token scope=account；空间内 API 仍用租户内 User token。
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.account import Account
from app.utils.auth import (
    hash_password,
    verify_password,
    create_token,
    get_current_account,
    validate_username,
    validate_password,
)
from app.trial import get_space_by_account, create_space_for_account, issue_space_token_for_account

router = APIRouter(prefix="/api/account", tags=["账号"])


class RegisterRequest(BaseModel):
    username: str
    password: str
    role: str = "parent"   # parent（家长：体验小孩+自己的小孩）/ org（机构：仅体验小孩）
    child_name: str = ""   # 家长注册时填的小孩昵称（建空间预填）


class LoginRequest(BaseModel):
    username: str
    password: str


def _account_dict(account: Account) -> dict:
    return {
        "id": account.id,
        "username": account.username,
        "subscription_plan": account.subscription_plan,
        "role": account.role,
        "child_name": account.child_name,
    }


@router.post("/register")
def register(data: RegisterRequest, db: Session = Depends(get_db)):
    """注册全局账号 + 自动创建体验空间（架构统一：账号即空间，注册完即可进入）。

    复用 create_space_for_account（复制模板库秒级创建），官网前端 app.js 已按
    返回 space 自适应显示「进入体验空间」（未建空间的老账号仍走 /api/trial/spaces 手动创建）。
    """
    username = (data.username or "").strip()
    password = data.password or ""
    err = validate_username(username)
    if err:
        raise HTTPException(status_code=400, detail=err)
    err = validate_password(username, password)
    if err:
        raise HTTPException(status_code=400, detail=err)
    if db.query(Account).filter_by(username=username).first():
        raise HTTPException(status_code=400, detail="该用户名已注册，请直接登录")
    role = (data.role or "parent").strip().lower()
    if role not in ("parent", "org"):
        raise HTTPException(status_code=400, detail="role 必须是 parent 或 org")
    child_name = (data.child_name or "").strip()
    if role == "parent" and len(child_name) > 30:
        raise HTTPException(status_code=400, detail="小孩昵称过长（最多 30 字）")
    account = Account(
        username=username,
        password_hash=hash_password(password),
        subscription_plan="free",
        role=role,
        child_name=child_name,
    )
    db.add(account)
    db.commit()
    db.refresh(account)
    # 注册即建空间（复制模板库 + 写账号名/小孩昵称 + registry 登记；秒级）
    key, record = create_space_for_account(
        account.id, account.username,
        (account.child_name or "").strip(),
        account.role,
        password_hash=account.password_hash,
    )
    space_token_payload = issue_space_token_for_account(account.id)
    return {
        "token": create_token(account, scope="account", persistent=True),
        "space_token": (space_token_payload or {}).get("token"),
        "user": _account_dict(account),
        "space": {
            "key": key,
            "url": f"/{key}/",
            "child_name": record["child_name"],
            "trial_end_at": record["trial_end_at"],
        },
        "message": "注册成功",
    }


@router.post("/login")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    """账号登录：返回账号 token + 名下空间信息"""
    username = (data.username or "").strip()
    account = db.query(Account).filter_by(username=username).first()
    if not account or not verify_password(data.password or "", account.password_hash):
        raise HTTPException(status_code=401, detail="用户名或密码错误")
    if not account.enabled:
        raise HTTPException(status_code=401, detail="账号已被禁用，请联系管理员")
    space = get_space_by_account(account.id)
    space_token_payload = issue_space_token_for_account(account.id)
    return {
        "token": create_token(account, scope="account", persistent=True),
        "space_token": (space_token_payload or {}).get("token"),
        "user": _account_dict(account),
        "space": space,
        "message": "登录成功",
    }


@router.get("/me")
def me(account: Account = Depends(get_current_account)):
    """当前账号 + 名下空间（官网/我的空间面板用）；有空间则附带 space_token 供前端同步登录态"""
    space = get_space_by_account(account.id)
    return {
        "user": _account_dict(account),
        "space": space,
        "space_token": (issue_space_token_for_account(account.id) or {}).get("token") if space else None,
    }
