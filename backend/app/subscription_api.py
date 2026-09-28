# -*- coding: utf-8 -*-
"""订阅/升级 API：
- POST /api/subscription/upgrade {plan: 'online'|'local'}（Bearer account token）
  模拟付款完成后调用：账号订阅状态升级 + 名下所有空间转正式（trial_end_at=NULL）。
  云端正式版(pro_online)：直接在线使用；本地版(pro_local)：附下载/指引链接。
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.account import Account
from app.utils.auth import get_current_account
from app.trial import upgrade_account_spaces
from app.config_api import get_config_map

router = APIRouter(prefix="/api/subscription", tags=["订阅升级"])

VALID_PLANS = ("online", "local")


class UpgradeRequest(BaseModel):
    plan: str  # online / local


@router.post("/upgrade")
def upgrade(
    data: UpgradeRequest,
    account: Account = Depends(get_current_account),
    db: Session = Depends(get_db),
):
    plan = (data.plan or "").strip().lower()
    if plan not in VALID_PLANS:
        raise HTTPException(status_code=400, detail="plan 必须是 online 或 local")

    account.subscription_plan = "pro_online" if plan == "online" else "pro_local"
    db.commit()
    upgraded = upgrade_account_spaces(account.id)
    cfg = get_config_map(db)

    result = {
        "subscription_plan": account.subscription_plan,
        "spaces_upgraded": upgraded,
        "message": "升级成功！已转为云端正式版，不再受体验期限制。" if plan == "online"
        else "本地版订阅成功！请下载本地版安装包使用。",
    }
    if plan == "local":
        result["download_url"] = cfg.get("local_download_url", "")
        result["guide_url"] = cfg.get("local_guide_url", "")
    return result
