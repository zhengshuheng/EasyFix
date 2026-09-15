from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional

from sqlalchemy.orm import Session
from app.database import get_db
from app.models.user import User
from app.models.subject import Subject
from app.models.error_book import ErrorBook
from app.utils.auth import hash_password, require_admin

router = APIRouter(prefix="/api/users", tags=["用户管理"])

MAX_ADMIN = 2
MAX_CHILD = 5


class CreateUserRequest(BaseModel):
    username: str
    role: str = "child"  # admin / child
    display_name: Optional[str] = None
    password: Optional[str] = None  # 家长必填
    pin: Optional[str] = None       # 小孩必填（4位数字）
    avatar: Optional[str] = None


class UpdateUserRequest(BaseModel):
    display_name: Optional[str] = None
    avatar: Optional[str] = None
    enabled: Optional[bool] = None


class UpdatePasswordRequest(BaseModel):
    password: Optional[str] = None  # 家长改密码
    pin: Optional[str] = None       # 小孩改 PIN


def user_dict(user: User) -> dict:
    return {
        "id": user.id,
        "username": user.username,
        "display_name": user.display_name or user.username,
        "role": user.role,
        "avatar": user.avatar,
        "enabled": user.enabled,
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }


def _count_by_role(db: Session, role: str) -> int:
    return db.query(User).filter_by(role=role).count()


@router.get("/kids")
def list_kids(db: Session = Depends(get_db)):
    """公开的小孩列表（选择页用，无需登录；不含家长/敏感信息）"""
    kids = (
        db.query(User)
        .filter_by(role="child")
        .order_by(User.id)
        .all()
    )
    return {
        "kids": [
            {
                "id": k.id,
                "username": k.username,
                "display_name": k.display_name or k.username,
                "avatar": k.avatar,
                "enabled": k.enabled,
            }
            for k in kids
        ]
    }


@router.get("")
def list_users(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    """用户列表（家长可见）"""
    users = db.query(User).order_by(User.id).all()
    return {"users": [user_dict(u) for u in users]}


@router.post("")
def create_user(
    data: CreateUserRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """创建小孩(≤5) / 第二个家长(≤2)"""
    username = data.username.strip()
    if not username:
        raise HTTPException(status_code=400, detail="用户名不能为空")
    if data.role not in ("admin", "child"):
        raise HTTPException(status_code=400, detail="角色必须是 admin 或 child")
    if db.query(User).filter_by(username=username).first():
        raise HTTPException(status_code=400, detail="用户名已存在")

    if data.role == "admin":
        if _count_by_role(db, "admin") >= MAX_ADMIN:
            raise HTTPException(status_code=400, detail=f"家长账号最多 {MAX_ADMIN} 个")
        if not data.password or len(data.password) < 4:
            raise HTTPException(status_code=400, detail="家长密码至少 4 位")
        user = User(
            username=username,
            display_name=data.display_name or username,
            role="admin",
            password_hash=hash_password(data.password),
            avatar=data.avatar,
        )
    else:
        if _count_by_role(db, "child") >= MAX_CHILD:
            raise HTTPException(status_code=400, detail=f"小孩账号最多 {MAX_CHILD} 个")
        # 小孩无需密码：PIN 为可选字段（保留兼容，可为空）
        pin = (data.pin or "").strip()
        user = User(
            username=username,
            display_name=data.display_name or username,
            role="child",
            pin=pin or None,
            avatar=data.avatar,
        )

    db.add(user)
    db.commit()
    db.refresh(user)

    # 小孩创建成功后：自动为该小孩创建各学科错题本（该小孩该学科已有则跳过）
    if data.role == "child":
        _ensure_default_error_books(db, user.id)

    return {"message": "创建成功", "user": user_dict(user)}


def _ensure_default_error_books(db: Session, user_id: int):
    """为指定小孩自动创建各学科错题本（该小孩该学科已有则跳过），无需家长手动添加"""
    subjects = db.query(Subject).filter(Subject.deleted == False).all()
    for s in subjects:
        exists = (
            db.query(ErrorBook)
            .filter(
                ErrorBook.user_id == user_id,
                ErrorBook.subject_id == s.id,
                ErrorBook.deleted == False,
            )
            .first()
        )
        if exists:
            continue
        db.add(ErrorBook(name=f"小学{s.name}错题本" if s.id <= 3 else f"{s.name}错题本", subject_id=s.id, user_id=user_id))
    db.commit()


@router.put("/{user_id}")
def update_user(
    user_id: int,
    data: UpdateUserRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    if data.display_name is not None:
        user.display_name = data.display_name.strip() or user.username
    if data.avatar is not None:
        user.avatar = data.avatar
    if data.enabled is not None:
        user.enabled = data.enabled
    db.commit()
    db.refresh(user)
    return {"message": "更新成功", "user": user_dict(user)}


@router.put("/{user_id}/password")
def update_password(
    user_id: int,
    data: UpdatePasswordRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """家长改密码 / 小孩改 PIN"""
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    if user.role == "admin":
        if not data.password or len(data.password) < 4:
            raise HTTPException(status_code=400, detail="家长密码至少 4 位")
        user.password_hash = hash_password(data.password)
    else:
        pin = (data.pin or "").strip()
        if not pin.isdigit() or len(pin) != 4:
            raise HTTPException(status_code=400, detail="小孩 PIN 码必须是 4 位数字")
        user.pin = pin
    db.commit()
    return {"message": "修改成功"}


@router.delete("/{user_id}")
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """删除用户；保护：不能删自己、不能删最后一个家长"""
    if user_id == admin.id:
        raise HTTPException(status_code=400, detail="不能删除当前登录账号")
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    if user.role == "admin" and _count_by_role(db, "admin") <= 1:
        raise HTTPException(status_code=400, detail="至少保留一个家长账号")
    # 删除小孩时软删其错题本（避免孤儿数据残留）
    if user.role == "child":
        db.query(ErrorBook).filter(ErrorBook.user_id == user.id).update({ErrorBook.deleted: True})
    db.delete(user)
    db.commit()
    return {"message": "删除成功"}
