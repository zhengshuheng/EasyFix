from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Optional, List
from datetime import date

from sqlalchemy.orm import Session
from app.database import get_db, SessionLocal, current_tenant
from app.models.user import User
from app.models.subject import Subject
from app.models.error_book import ErrorBook
from app.models.kid_textbook import KidTextbook
from app.models.account import Account
from app.services.textbook_meta import edition_key_for
from app.utils.auth import hash_password, require_admin
from app.utils.timeutil import infer_grade
from app.trial import get_space_by_key

router = APIRouter(prefix="/api/users", tags=["用户管理"])

MAX_ADMIN = 2
MAX_CHILD = 5


def _parse_date(v):
    """YYYY-MM-DD 字符串 → date（空/非法返回 None）"""
    if not v:
        return None
    try:
        return date.fromisoformat(str(v)[:10])
    except ValueError:
        return None


class KidTextbookIn(BaseModel):
    subject_id: int
    edition_key: Optional[str] = None  # 可选：缺省由后端按版本规则自动生成（edition_key_for）
    version_name: str = ""
    source: str = "package"  # package=下载包 / local=本地AI提取兜底


class KidTextbookBatchRequest(BaseModel):
    textbooks: List[KidTextbookIn] = []


class CreateUserRequest(BaseModel):
    username: str
    role: str = "child"  # admin / child
    display_name: Optional[str] = None
    password: Optional[str] = None  # 家长必填
    pin: Optional[str] = None       # 小孩必填（4位数字）
    avatar: Optional[str] = None
    enrollment_date: Optional[str] = None  # 小孩一年级入学日期（YYYY-MM-DD），据此推断当前年级
    textbooks: Optional[List[KidTextbookIn]] = None  # 小孩教材版本偏好（按学科）


class UpdateUserRequest(BaseModel):
    display_name: Optional[str] = None
    avatar: Optional[str] = None
    enabled: Optional[bool] = None
    enrollment_date: Optional[str] = None  # 入学日期（null=不改）


class UpdatePasswordRequest(BaseModel):
    password: Optional[str] = None  # 家长改密码
    pin: Optional[str] = None       # 小孩改 PIN


def _kid_textbook_dict(db: Session, kid_id: int) -> list:
    rows = db.query(KidTextbook).filter(KidTextbook.kid_id == kid_id).all()
    return [
        {
            "subject_id": r.subject_id,
            "edition_key": r.edition_key,
            "version_name": r.version_name,
            "source": r.source,
        }
        for r in rows
    ]


def _save_kid_textbooks(db: Session, kid_id: int, textbooks: list) -> None:
    """全量保存小孩教材版本偏好（按 kid_id+subject_id upsert；空列表=清空）。
    前端只需传 subject_id + version_name，edition_key 由后端按版本规则兜底生成。"""
    db.query(KidTextbook).filter(KidTextbook.kid_id == kid_id).delete()
    subj_map = {s.id: s.name for s in db.query(Subject).all()}
    for t in textbooks or []:
        subject_id = t.get("subject_id")
        version_name = (t.get("version_name") or "").strip()
        if not subject_id or not version_name:
            continue
        edition_key = (t.get("edition_key") or "").strip() or edition_key_for(
            subj_map.get(subject_id, ""), version_name
        )
        if not edition_key:
            continue
        db.add(KidTextbook(
            kid_id=kid_id,
            subject_id=subject_id,
            edition_key=edition_key,
            version_name=version_name,
            source=t.get("source") or "package",
        ))
    db.commit()


def user_dict(user: User, db: Session = None) -> dict:
    d = {
        "id": user.id,
        "username": user.username,
        "display_name": user.display_name or user.username,
        "role": user.role,
        "is_owner": user.is_owner,
        "avatar": user.avatar,
        "enabled": user.enabled,
        "enrollment_date": user.enrollment_date.isoformat() if user.enrollment_date else None,
        "current_grade": infer_grade(user.enrollment_date),
        "created_at": user.created_at.isoformat() if user.created_at else None,
    }
    if db is not None and user.role == "child":
        d["textbooks"] = _kid_textbook_dict(db, user.id)
    return d


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
                "enrollment_date": k.enrollment_date.isoformat() if k.enrollment_date else None,
                "current_grade": infer_grade(k.enrollment_date),
                "textbooks": _kid_textbook_dict(db, k.id),
            }
            for k in kids
        ]
    }


@router.get("")
def list_users(db: Session = Depends(get_db), admin: User = Depends(require_admin)):
    """用户列表（家长可见）"""
    users = db.query(User).order_by(User.id).all()
    return {"users": [user_dict(u, db) for u in users]}


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
        # 辅助家长要能在官网登录：用户名必须全局唯一（不占用官网已注册账号名）
        main_db = SessionLocal()
        try:
            if main_db.query(Account).filter_by(username=username).first():
                raise HTTPException(status_code=400, detail="该用户名已被官网账号占用，请换一个用户名")
        finally:
            main_db.close()
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
            enrollment_date=_parse_date(data.enrollment_date),
        )

    db.add(user)
    db.commit()
    db.refresh(user)

    # 辅助家长官网登录：同步创建全局账号（绑定当前空间 key，同一密码）
    if data.role == "admin":
        key = current_tenant.get()
        main_db = SessionLocal()
        try:
            acct = Account(
                username=username,
                password_hash=user.password_hash,
                subscription_plan="free",
                role="parent",
                space_key=key,
            )
            main_db.add(acct)
            main_db.commit()
        except Exception:
            main_db.rollback()
            # 官网账号创建失败则撤销空间用户，避免"空间里有账号但官网登不上"
            db.delete(user)
            db.commit()
            raise HTTPException(status_code=400, detail="创建官网登录账号失败，请重试")
        finally:
            main_db.close()

    # 小孩创建成功后：自动为该小孩创建各学科错题本 + 保存教材版本偏好
    if data.role == "child":
        _ensure_default_error_books(db, user.id)
        if data.textbooks:
            _save_kid_textbooks(db, user.id, [t.model_dump() for t in data.textbooks])

    return {"message": "创建成功", "user": user_dict(user, db)}


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
    # 入学日期：显式传 null 表示清空；未传该字段则不修改
    if "enrollment_date" in data.model_fields_set and user.role == "child":
        user.enrollment_date = _parse_date(data.enrollment_date)
    db.commit()
    db.refresh(user)
    return {"message": "更新成功", "user": user_dict(user, db)}


@router.get("/{user_id}/textbooks")
def get_kid_textbooks(
    user_id: int,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """小孩教材版本偏好列表"""
    user = db.get(User, user_id)
    if not user or user.role != "child":
        raise HTTPException(status_code=404, detail="小孩不存在")
    return {"textbooks": _kid_textbook_dict(db, user_id)}


@router.put("/{user_id}/textbooks")
def put_kid_textbooks(
    user_id: int,
    data: KidTextbookBatchRequest,
    db: Session = Depends(get_db),
    admin: User = Depends(require_admin),
):
    """保存小孩教材版本偏好（全量替换；空数组=清空）"""
    user = db.get(User, user_id)
    if not user or user.role != "child":
        raise HTTPException(status_code=404, detail="小孩不存在")
    _save_kid_textbooks(db, user_id, [t.model_dump() for t in data.textbooks])
    return {"message": "已保存", "textbooks": _kid_textbook_dict(db, user_id)}


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
        # 官网登录同步：改空间内家长密码时同步更新全局账号密码（否则官网登录仍是旧密码）
        main_db = SessionLocal()
        try:
            acct = main_db.query(Account).filter_by(username=user.username).first()
            if acct:
                acct.password_hash = user.password_hash
                main_db.commit()
        finally:
            main_db.close()
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
    """删除用户；保护：不能删自己、不能删最后一个家长、不能删主账号（官网注册家长）"""
    if user_id == admin.id:
        raise HTTPException(status_code=400, detail="不能删除当前登录账号")
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    if user.role == "admin" and _count_by_role(db, "admin") <= 1:
        raise HTTPException(status_code=400, detail="至少保留一个家长账号")
    # 主账号（官网注册家长）不可删除：显式 is_owner 标识；registry username 兜底
    key = current_tenant.get()
    record = get_space_by_key(key) if key else None
    if user.is_owner or (record and user.username == (record.get("username") or "")):
        raise HTTPException(status_code=400, detail="主账号（官网注册账号）不可删除")
    # 删除小孩时软删其错题本（避免孤儿数据残留）
    if user.role == "child":
        db.query(ErrorBook).filter(ErrorBook.user_id == user.id).update({ErrorBook.deleted: True})
    db.delete(user)
    db.commit()
    # 删除家长 → 同时禁用其官网账号（同 username），官网登录立即失效
    if user.role == "admin":
        try:
            main_db = SessionLocal()
            try:
                acct = main_db.query(Account).filter_by(username=user.username).first()
                if acct:
                    acct.enabled = False
                    main_db.commit()
            finally:
                main_db.close()
        except Exception:
            pass  # 主库账号禁用失败不影响空间内删除
    return {"message": "删除成功"}
