# -*- coding: utf-8 -*-
"""体验账号管理（运营后台）

列表 / 延长体验 / 删除：体验账号 = accounts（主库，全局身份）+ registry.spaces
（空间 key ↔ account_id ↔ db_path，trial_end_at 到期时间）+ 空间库（小孩数量）。

- 延长体验：spaces.trial_end_at += N 天；trial_end_at=NULL（正式版）拒绝延长。
- 删除账号：delete_space（引擎缓存 + db 文件 + registry 行）+ 删除 accounts 行。
  提示：正式版账号同样可删（连带空间数据），运营自行确认。
"""
from datetime import datetime, timedelta

from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel

from app.config_api import _check_ops_password
from app.database import SessionLocal
from app.models.account import Account
from app.trial import get_space_by_username, delete_space, _registry_conn

router = APIRouter(prefix="/api/ops/trial-accounts", tags=["Ops 体验账号管理"])


class ExtendIn(BaseModel):
    days: int = 7


def _ops_check(x_ops_username: str, x_ops_password: str) -> None:
    db = SessionLocal()
    try:
        _check_ops_password(db, x_ops_password, x_ops_username)
    finally:
        db.close()


def _count_children(db_path: str) -> int:
    """打开空间库统计小孩数（role='child'）；文件缺失/损坏按 0 处理"""
    import os
    import sqlite3
    if not db_path or not os.path.isfile(db_path):
        return 0
    try:
        conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
        try:
            n = conn.execute("SELECT COUNT(*) FROM users WHERE role='child'").fetchone()[0]
            return int(n)
        finally:
            conn.close()
    except Exception as e:
        print(f"[trial-accounts] 统计小孩数失败 {db_path}: {e}")
        return 0


def _status_of(trial_end_at):
    """体验状态：pro=正式版 / expired=已过期 / ok=体验中"""
    if not trial_end_at:
        return "pro"
    try:
        end = datetime.strptime(trial_end_at, "%Y-%m-%d %H:%M:%S")
        if end < datetime.now():
            return "expired"
    except ValueError:
        pass
    return "ok"


@router.get("")
def trial_accounts_list(
    x_ops_username: str = Header(default=""),
    x_ops_password: str = Header(default=""),
):
    """体验账号列表：账号 + 小孩数量 + 创建时间 + 到期时间 + 状态 + 订阅计划"""
    _ops_check(x_ops_username, x_ops_password)
    conn = _registry_conn()
    try:
        rows = conn.execute(
            "SELECT key, account_id, username, child_name, db_path, created_at, trial_end_at"
            " FROM spaces ORDER BY created_at DESC"
        ).fetchall()
    finally:
        conn.close()

    db = SessionLocal()
    try:
        items = []
        for key, account_id, username, child_name, db_path, created_at, trial_end_at in rows:
            account = db.query(Account).filter_by(id=account_id).first() if account_id else None
            items.append({
                "account_id": account_id,
                "username": username,
                "subscription_plan": account.subscription_plan if account else None,
                "child_name": child_name or "",
                "space_key": key,
                "children_count": _count_children(db_path),
                "created_at": created_at,
                "trial_end_at": trial_end_at,
                "status": _status_of(trial_end_at),
            })
    finally:
        db.close()
    return {"items": items, "total": len(items)}


@router.post("/{account_id}/extend")
def trial_account_extend(
    account_id: int,
    data: ExtendIn,
    x_ops_username: str = Header(default=""),
    x_ops_password: str = Header(default=""),
):
    """延长体验时间：trial_end_at += days（正式版拒绝延长）"""
    _ops_check(x_ops_username, x_ops_password)
    days = data.days
    if not isinstance(days, int) or days <= 0 or days > 3650:
        raise HTTPException(status_code=400, detail="延长时间需为 1~3650 天的整数")
    record = get_space_by_account(account_id)
    if not record:
        raise HTTPException(status_code=404, detail="该账号名下没有空间")
    if not record.get("trial_end_at"):
        raise HTTPException(status_code=400, detail="该账号已是正式版（不限体验期），无需延长")

    try:
        end = datetime.strptime(record["trial_end_at"], "%Y-%m-%d %H:%M:%S")
        new_end = end + timedelta(days=days)
        new_end_str = new_end.strftime("%Y-%m-%d %H:%M:%S")
    except ValueError:
        raise HTTPException(status_code=400, detail=f"到期时间格式异常：{record['trial_end_at']}")

    conn = _registry_conn()
    try:
        conn.execute(
            "UPDATE spaces SET trial_end_at = ? WHERE key = ?",
            (new_end_str, record["key"]),
        )
        conn.commit()
    finally:
        conn.close()
    return {
        "account_id": account_id,
        "username": record["username"],
        "old_trial_end_at": record["trial_end_at"],
        "trial_end_at": new_end_str,
        "extended_days": days,
    }


@router.delete("/{account_id}")
def trial_account_delete(
    account_id: int,
    x_ops_username: str = Header(default=""),
    x_ops_password: str = Header(default=""),
):
    """删除体验账号：删除名下空间（引擎缓存 + db 文件 + registry 记录）+ 账号本身"""
    _ops_check(x_ops_username, x_ops_password)
    db = SessionLocal()
    try:
        account = db.query(Account).filter_by(id=account_id).first()
        if not account:
            raise HTTPException(status_code=404, detail="账号不存在")
        # 按 username 精确匹配空间（自增 account_id 会被复用，悬空 id 会误删别的空间）
        record = get_space_by_username(account.username)
        if record:
            try:
                delete_space(record["key"])
            except RuntimeError as e:
                # 文件可能被占用：账号/注册记录已删除，文件残留，明确告知运营
                raise HTTPException(status_code=500, detail=str(e))
        username = account.username
        db.delete(account)
        db.commit()
        return {
            "ok": True,
            "username": username,
            "space_deleted": bool(record),
            "space_key": record["key"] if record else None,
        }
    finally:
        db.close()
