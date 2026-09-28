"""Ops 激励规则管理 API（运营后台，X-Ops-Password 鉴权，主库读写）

定位：行为/成就规则统一由运营中心集中配置（主库 star_action / achievement 为权威差异集）。
服务层（services/motivation.py）读取时主库优先、空间库兜底；家长中心不再提供行为/成就配置。
本接口只允许调整参数（积分值/启用/触发次数/奖励积分），不允许新增/删除触发点——
行为代码是程序触发点，新增必须改代码，运营界面不暴露 code。
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel

from app.config_api import _check_ops_password
from app.database import SessionLocal
from app.models.star import StarAction
from app.models.achievement import Achievement
from app.services.init_motivation_data import PRESET_ACTIONS, PRESET_ACHIEVEMENTS

router = APIRouter(prefix="/api/ops", tags=["Ops 激励规则"])

# 业务触发点（排除内部行为 manual_adjustment —— 家长手动调整不走 trigger_action）
ACTION_DEFAULTS = {a["code"]: a for a in PRESET_ACTIONS if a["code"] != "manual_adjustment"}
ACH_DEFAULTS = {(a["code"], a["level"]): a for a in PRESET_ACHIEVEMENTS}


def _ops_check(x_ops_username: str, x_ops_password: str) -> None:
    db = SessionLocal()
    try:
        _check_ops_password(db, x_ops_password, x_ops_username)
    finally:
        db.close()


# ---------------------------------------------------------------- 激励规则

@router.get("/incentive-rules")
def ops_incentive_rules_list(x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    """激励规则清单：全部配置项 + 运营已保存覆盖（未保存显示内置默认值）。"""
    _ops_check(x_ops_username, x_ops_password)
    db = SessionLocal()
    try:
        rows_a = {r.code: r for r in db.query(StarAction).all()}
        rows_ach = {(r.code, r.level): r for r in db.query(Achievement).all()}

        actions = []
        for code, d in ACTION_DEFAULTS.items():
            row = rows_a.get(code)
            changed = row and (row.star_value != d["star_value"] or bool(row.enabled) != bool(d.get("enabled", True)))
            value = row if changed else d
            actions.append({
                "code": code,
                "name": value["name"] if isinstance(value, dict) else value.name,
                "star_value": value["star_value"] if isinstance(value, dict) else value.star_value,
                "enabled": bool(value.get("enabled", True)) if isinstance(value, dict) else bool(value.enabled),
                "is_default": not changed,
            })

        achievements = []
        for (code, level), d in ACH_DEFAULTS.items():
            row = rows_ach.get((code, level))
            changed = row and (
                row.trigger_count != d["trigger_count"]
                or row.reward_stars != d["reward_stars"]
                or bool(row.is_active) != bool(d.get("is_active", True))
            )
            value = row if changed else d
            achievements.append({
                "code": code,
                "name": value["name"] if isinstance(value, dict) else value.name,
                "level": level,
                "trigger_action": value["trigger_action"] if isinstance(value, dict) else value.trigger_action,
                "trigger_count": value["trigger_count"] if isinstance(value, dict) else value.trigger_count,
                "reward_stars": value["reward_stars"] if isinstance(value, dict) else value.reward_stars,
                "is_active": bool(value.get("is_active", True)) if isinstance(value, dict) else bool(value.is_active),
                "is_default": not changed,
            })

        return {"actions": actions, "achievements": achievements}
    finally:
        db.close()


class IncentiveActionItem(BaseModel):
    code: str
    star_value: int
    enabled: bool = True


class IncentiveAchievementItem(BaseModel):
    code: str
    level: int
    trigger_count: int
    reward_stars: int = 0
    is_active: bool = True


class IncentiveRulesSaveRequest(BaseModel):
    restore_all: bool = False
    actions: List[IncentiveActionItem] = []
    achievements: List[IncentiveAchievementItem] = []


@router.put("/incentive-rules")
def ops_incentive_rules_save(data: IncentiveRulesSaveRequest,
                             x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    """批量保存激励规则：
    参数与内置默认一致 → 删除主库记录（恢复默认）；有差异 → upsert；
    restore_all=True → 清空主库差异集，全部恢复内置默认。
    """
    _ops_check(x_ops_username, x_ops_password)
    db = SessionLocal()
    try:
        if data.restore_all:
            db.query(StarAction).delete()
            db.query(Achievement).delete()
            db.commit()
            return {"ok": True, "restored_all": True, "saved": []}

        saved = []

        # ---- 行为 ----
        for item in data.actions:
            d = ACTION_DEFAULTS.get(item.code)
            if not d:
                continue
            is_default = (item.star_value == d["star_value"] and item.enabled == bool(d.get("enabled", True)))
            row = db.query(StarAction).filter(StarAction.code == item.code).first()
            if is_default:
                if row is not None:
                    db.delete(row)
                saved.append({"code": item.code, "is_default": True})
                continue
            if row is None:
                row = StarAction(code=item.code, name=d["name"], star_value=item.star_value,
                                 enabled=item.enabled, is_custom=False)
                db.add(row)
            else:
                row.star_value = item.star_value
                row.enabled = item.enabled
            saved.append({"code": item.code, "is_default": False})

        # ---- 成就 ----
        for item in data.achievements:
            d = ACH_DEFAULTS.get((item.code, item.level))
            if not d:
                continue
            is_default = (item.trigger_count == d["trigger_count"]
                          and item.reward_stars == d["reward_stars"]
                          and item.is_active == bool(d.get("is_active", True)))
            row = db.query(Achievement).filter(
                Achievement.code == item.code, Achievement.level == item.level
            ).first()
            if is_default:
                if row is not None:
                    db.delete(row)
                saved.append({"code": item.code, "level": item.level, "is_default": True})
                continue
            if row is None:
                row = Achievement(code=item.code, name=d["name"], level=item.level,
                                  description=d.get("description"), trigger_action=d["trigger_action"],
                                  trigger_count=item.trigger_count, reward_stars=item.reward_stars,
                                  is_active=item.is_active, is_preset=True)
                db.add(row)
            else:
                row.trigger_count = item.trigger_count
                row.reward_stars = item.reward_stars
                row.is_active = item.is_active
            saved.append({"code": item.code, "level": item.level, "is_default": False})

        db.commit()
        return {"ok": True, "restored_all": False, "saved": saved}
    finally:
        db.close()
