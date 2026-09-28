"""当前小孩上下文：全链路按小孩隔离的解析工具。

kid_id 解析优先级：
1. 登录用户本身是小孩（role='child'）→ 强制用其自身 id（请求头无法冒充他人）
2. 登录用户是家长（role='admin'）→ 读请求头 X-Kid-Id（前端注入"当前选择的孩子"）
3. 都取不到 → None = 家长未指定孩子
   - 列表/统计类接口：None 表示查看全部孩子（家长视角）
   - 写入类接口：用 get_required_kid_id 强制要求先选孩子
"""
from typing import Optional

from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User
from app.utils.auth import get_optional_user

KID_HEADER = "X-Kid-Id"


def resolve_kid_id(
    current_user: Optional[User],
    x_kid_id: Optional[str],
    db: Session,
    *,
    required: bool = False,
) -> Optional[int]:
    kid_id: Optional[int] = None
    if current_user is not None and current_user.role == "child":
        kid_id = current_user.id
    elif x_kid_id not in (None, "", "null", "undefined", "0"):
        try:
            kid_id = int(x_kid_id)
        except (TypeError, ValueError):
            raise HTTPException(status_code=400, detail="X-Kid-Id 必须是整数")
        target = db.get(User, kid_id)
        if target is None:
            raise HTTPException(status_code=404, detail="指定的孩子不存在")
        if not target.enabled:
            raise HTTPException(status_code=403, detail="指定的孩子已被禁用")
    if kid_id is None and required:
        raise HTTPException(status_code=400, detail="请先在主页选择孩子，再进行操作")
    return kid_id


def get_current_kid_id(
    x_kid_id: Optional[str] = Header(None, alias=KID_HEADER),
    user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db),
) -> Optional[int]:
    """当前小孩 id；None = 家长未指定（查看全部）"""
    return resolve_kid_id(user, x_kid_id, db)


def get_required_kid_id(
    x_kid_id: Optional[str] = Header(None, alias=KID_HEADER),
    user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db),
) -> int:
    """写入类接口：必须有明确的孩子归属"""
    return resolve_kid_id(user, x_kid_id, db, required=True)


def filter_by_kid(query, column, kid_id: Optional[int]):
    """按小孩过滤查询；kid_id 为 None 表示不限（家长未选孩子=全部）"""
    if kid_id is None:
        return query
    return query.filter(column == kid_id)


def kid_scope(kid_id: Optional[int]) -> dict:
    """返回可直接用于 ORM 查询的过滤条件字典（None 时为空字典=不过滤）"""
    return {} if kid_id is None else {"user_id": kid_id}
