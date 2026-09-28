from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from fastapi import Path
from sqlalchemy.orm import Session
from app.database import get_db
import os
import uuid
from datetime import datetime
from app.services.motivation import MotivationService
from app.utils.kid_context import get_current_kid_id, get_required_kid_id
from app.schemas.star import (
    StarBalanceResponse, StarRecordResponse, StarActionResponse,
    StarActionCreate, StarActionUpdate,
    StarsAdjustRequest, StarsAdjustResponse,
    IncentiveSettingsRequest
)
from app.schemas.achievement import (
    AchievementResponse, AchievementProgressResponse,
    AchievementCreate, AchievementUpdate
)
from app.schemas.reward import (
    RewardResponse, RewardCreate, RewardUpdate, RedemptionResponse
)
from typing import List

router = APIRouter(prefix="/api", tags=["激励系统"])

DEFAULT_USER_ID = 1


def _kid_or_first(kid_id, db: Session) -> int:
    """读取类接口：未指定孩子时回退到第一个小孩（保证有数据可看）"""
    if kid_id:
        return kid_id
    from app.models.user import User
    kid = db.query(User).filter(User.role == "child", User.enabled == True).order_by(User.id).first()
    return kid.id if kid else DEFAULT_USER_ID


# ============ 积分模块 ============

@router.get("/stars/balance", response_model=StarBalanceResponse)
def get_balance(
    db: Session = Depends(get_db),
    kid_id: int = Depends(get_current_kid_id),
):
    service = MotivationService(db)
    uid = _kid_or_first(kid_id, db)
    balance = service.get_or_create_balance(uid)
    return StarBalanceResponse(balance=balance.balance)


@router.get("/stars/records")
def get_records(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db),
    kid_id: int = Depends(get_current_kid_id),
):
    """获取积分明细列表（分页，按小孩隔离）"""
    from app.models.star import StarRecord
    from sqlalchemy import func

    uid = _kid_or_first(kid_id, db)

    # 查询总数
    total = db.query(func.count(StarRecord.id)).filter(
        StarRecord.user_id == uid,
        StarRecord.deleted == False
    ).scalar()

    # 查询列表
    records = db.query(StarRecord).filter(
        StarRecord.user_id == uid,
        StarRecord.deleted == False
    ).order_by(StarRecord.created_at.desc(), StarRecord.id.desc()).offset(skip).limit(limit).all()

    return {
        "total": total,
        "items": records
    }


@router.post("/stars/adjust")
def adjust_stars(
    data: StarsAdjustRequest,
    db: Session = Depends(get_db),
    kid_id: int = Depends(get_required_kid_id),
):
    """手动调整指定小孩的积分（增加或减少）"""
    from app.models.star import StarRecord, StarBalance

    # 校验
    if data.delta == 0:
        raise HTTPException(status_code=400, detail="积分变动不能为0")
    if not data.reason or len(data.reason.strip()) == 0:
        raise HTTPException(status_code=400, detail="请输入调整原因")
    if len(data.reason) > 200:
        raise HTTPException(status_code=400, detail="调整原因不能超过200字符")

    uid = kid_id

    # 获取或创建余额
    balance = db.query(StarBalance).filter(StarBalance.user_id == uid).first()
    if not balance:
        balance = StarBalance(user_id=uid, balance=0)
        db.add(balance)
        # 不立即commit

    # 检查余额是否足够（减少时）
    if data.delta < 0 and balance.balance + data.delta < 0:
        raise HTTPException(status_code=400, detail="积分不足，无法减少")

    # 计算新余额并创建记录
    new_balance = balance.balance + data.delta
    record = StarRecord(
        user_id=uid,
        action_code="manual_adjustment",
        star_delta=data.delta,
        balance_after=new_balance,
        reason=data.reason.strip()
    )
    db.add(record)

    # 更新余额
    balance.balance = new_balance

    # 统一提交
    db.commit()
    db.refresh(record)

    return {
        "success": True,
        "new_balance": new_balance,
        "delta": data.delta,
        "record_id": record.id,
        "user_id": uid,
    }


@router.get("/stars/actions", response_model=List[StarActionResponse])
def get_actions(db: Session = Depends(get_db)):
    """行为列表（家长覆盖优先，运营默认兜底）——家长端展示，积分值可编辑"""
    service = MotivationService(db)
    return service.get_actions_merged()


# ============ 成就模块 ============

@router.get("/achievements", response_model=List[AchievementResponse])
def get_achievements(db: Session = Depends(get_db)):
    """成就列表（家长覆盖优先，运营默认兜底）——家长端展示，数值可编辑"""
    service = MotivationService(db)
    return service.get_achievements_merged()


@router.put("/incentive-settings")
def save_incentive_settings(data: IncentiveSettingsRequest, db: Session = Depends(get_db)):
    """家长（空间）保存激励自定义：行为积分值 / 成就触发次数 / 成就奖励积分。

    与运营默认（主库差异集，未配置则空间库模板值）比较：
    - 值 == 默认 → ops_override=False（恢复跟随运营默认，运营改默认后自动同步）
    - 值 != 默认 → ops_override=True + 写空间库值（该空间独立生效）
    启停开关（enabled / is_active）不在此接口，始终由运营中心控制。
    """
    from app.models.star import StarAction
    from app.models.achievement import Achievement
    service = MotivationService(db)
    saved = []

    if data.restore_all:
        db.query(StarAction).filter(StarAction.deleted == False).update(
            {StarAction.ops_override: False})
        db.query(Achievement).filter(Achievement.deleted == False).update(
            {Achievement.ops_override: False})
        db.commit()
        return {"ok": True, "saved": [], "restore_all": True}

    for item in data.actions:
        row = db.query(StarAction).filter(
            StarAction.code == item.code, StarAction.deleted == False
        ).first()
        if not row:
            continue
        oa = service._ops_actions.get(item.code)
        default_value = oa.star_value if oa else row.star_value
        if item.star_value == default_value:
            if row.ops_override:
                row.ops_override = False
                saved.append({"code": item.code, "is_default": True})
        else:
            row.star_value = item.star_value
            row.ops_override = True
            saved.append({"code": item.code, "is_default": False})

    for item in data.achievements:
        row = db.query(Achievement).filter(
            Achievement.code == item.code, Achievement.level == item.level,
            Achievement.deleted == False
        ).first()
        if not row:
            continue
        oa = service._ops_achievements.get((item.code, item.level))
        default_trigger = oa.trigger_count if oa else row.trigger_count
        default_reward = oa.reward_stars if oa else row.reward_stars
        if item.trigger_count == default_trigger and item.reward_stars == default_reward:
            if row.ops_override:
                row.ops_override = False
                saved.append({"code": item.code, "level": item.level, "is_default": True})
        else:
            row.trigger_count = item.trigger_count
            row.reward_stars = item.reward_stars
            row.ops_override = True
            saved.append({"code": item.code, "level": item.level, "is_default": False})

    db.commit()
    return {"ok": True, "saved": saved}


@router.get("/achievements/progress", response_model=List[AchievementProgressResponse])
def get_progress(
    db: Session = Depends(get_db),
    kid_id: int = Depends(get_current_kid_id),
):
    from app.models.achievement import Achievement, AchievementProgress

    uid = _kid_or_first(kid_id, db)

    # 获取所有成就进度
    progresses = db.query(AchievementProgress).filter(
        AchievementProgress.user_id == uid
    ).all()

    # 懒初始化：该小孩还没有进度记录的成就，自动补齐
    all_achievements = db.query(Achievement).filter(Achievement.deleted == False).all()
    existing_ids = {p.achievement_id for p in progresses}
    service = MotivationService(db)
    for ach in all_achievements:
        if ach.id in existing_ids:
            continue
        progress = AchievementProgress(
            user_id=uid,
            achievement_id=ach.id,
            current_count=0,
            is_unlocked=False
        )
        db.add(progress)
        progresses.append(progress)
        existing_ids.add(ach.id)
    db.commit()

    # 对于每个成就，计算真实进度（按小孩统计实际行为数据）并同步进度记录
    result = []
    for p in progresses:
        achievement = db.query(Achievement).filter(Achievement.id == p.achievement_id).first()
        if not achievement or achievement.deleted:
            continue
        # 进度计算用覆盖后参数（运营配置优先）
        achievement = service.overlay_achievement(achievement)

        real_count = service._get_achievement_total_count(uid, achievement.trigger_action)
        # 同步进度记录（仅当真实值更大时更新，避免覆盖解锁后的计数）
        if real_count > p.current_count:
            p.current_count = real_count
            if not p.is_unlocked and real_count >= achievement.trigger_count:
                p.is_unlocked = True
                p.unlocked_at = p.unlocked_at or datetime.now()
            db.add(p)
    db.commit()

    result = []
    for p in progresses:
        achievement = db.query(Achievement).filter(Achievement.id == p.achievement_id).first()
        if not achievement or achievement.deleted:
            continue
        achievement = service.overlay_achievement(achievement)
        result.append({
            "id": p.id,
            "achievement_id": p.achievement_id,
            "current_count": p.current_count,
            "is_unlocked": p.is_unlocked,
            "unlocked_at": p.unlocked_at,
            "achievement": achievement
        })

    return result


# ============ 奖励模块 ============

@router.get("/rewards", response_model=List[RewardResponse])
def get_rewards(db: Session = Depends(get_db)):
    from app.models.reward import Reward
    rewards = db.query(Reward).filter(Reward.deleted == False, Reward.is_active == True).all()
    return rewards


@router.post("/rewards", response_model=RewardResponse)
def create_reward(data: RewardCreate, db: Session = Depends(get_db)):
    from app.models.reward import Reward
    reward = Reward(**data.model_dump())
    db.add(reward)
    db.commit()
    db.refresh(reward)
    return reward


@router.put("/rewards/{reward_id}", response_model=RewardResponse)
def update_reward(reward_id: int, data: RewardUpdate, db: Session = Depends(get_db)):
    from app.models.reward import Reward
    reward = db.query(Reward).filter(Reward.id == reward_id).first()
    if not reward:
        raise HTTPException(status_code=404, detail="奖励不存在")
    for key, value in data.model_dump(exclude_unset=True).items():
        setattr(reward, key, value)
    db.commit()
    db.refresh(reward)
    return reward


@router.delete("/rewards/{reward_id}")
def delete_reward(reward_id: int, db: Session = Depends(get_db)):
    from app.models.reward import Reward
    reward = db.query(Reward).filter(Reward.id == reward_id).first()
    if not reward:
        raise HTTPException(status_code=404, detail="奖励不存在")
    reward.deleted = True
    db.commit()
    return {"success": True}


@router.post("/rewards/{reward_id}/redeem")
def redeem_reward(
    reward_id: int,
    db: Session = Depends(get_db),
    kid_id: int = Depends(get_required_kid_id),
):
    service = MotivationService(db)
    try:
        result = service.redeem_reward(reward_id, user_id=kid_id)
        return result
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/rewards/redemptions", response_model=List[RedemptionResponse])
def get_redemptions(
    db: Session = Depends(get_db),
    kid_id: int = Depends(get_current_kid_id),
):
    """获取指定小孩的兑换记录"""
    from app.models.reward import Redemption

    uid = _kid_or_first(kid_id, db)

    redemptions = db.query(Redemption).filter(
        Redemption.user_id == uid
    ).order_by(Redemption.redeemed_at.desc()).limit(50).all()

    return redemptions


# ============ 激励概览 ============

@router.get("/motivation/overview")
def get_overview(
    db: Session = Depends(get_db),
    kid_id: int = Depends(get_current_kid_id),
):
    """获取激励系统概览（按小孩）"""
    from app.models.star import StarAction, StarBalance, StarRecord
    from app.models.achievement import Achievement, AchievementProgress
    from app.models.reward import Reward, Redemption
    from sqlalchemy import func

    uid = _kid_or_first(kid_id, db)
    service = MotivationService(db)

    # 积分余额
    balance = db.query(StarBalance).filter(StarBalance.user_id == uid).first()
    balance_value = balance.balance if balance else 0

    # 成就统计（运营配置优先的启用成就数）
    all_achievements = service.get_achievements_merged()
    all_achievements = [a for a in all_achievements if a.is_active]
    unlocked_count = db.query(AchievementProgress).filter(
        AchievementProgress.user_id == uid,
        AchievementProgress.is_unlocked == True
    ).count()

    # 奖励统计
    active_rewards = db.query(Reward).filter(Reward.deleted == False, Reward.is_active == True).count()

    # 今日积分
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_stars = db.query(func.coalesce(func.sum(StarRecord.star_delta), 0)).filter(
        StarRecord.user_id == uid,
        StarRecord.created_at >= today_start
    ).scalar()

    return {
        "balance": balance_value,
        "achievement_total": len(all_achievements),
        "achievement_unlocked": unlocked_count,
        "rewards_available": active_rewards,
        "today_stars": today_stars
    }


# ============ 内部触发接口（供其他模块调用） ============

@router.post("/motivation/trigger/{action_code}")
def trigger_action(
    action_code: str,
    reason: str = None,
    db: Session = Depends(get_db),
    kid_id: int = Depends(get_required_kid_id),
):
    """触发积分行为（按当前小孩）"""
    service = MotivationService(db)
    result = service.trigger_action(action_code, user_id=kid_id, reason=reason)
    if result is None:
        raise HTTPException(status_code=404, detail="行为不存在或已禁用")
    return result


@router.post("/motivation/trigger/review_word_accuracy")
def trigger_word_accuracy(
    total_count: int,
    correct_count: int,
    reason: str = None,
    db: Session = Depends(get_db),
    kid_id: int = Depends(get_required_kid_id),
):
    """触发单词正确率成就（按当前小孩）"""
    service = MotivationService(db)
    result = service.check_word_accuracy(
        user_id=kid_id,
        total_count=total_count,
        correct_count=correct_count,
        reason=reason
    )
    if result is None:
        return {"unlocked": False, "message": "未达成条件"}
    return {"unlocked": True, **result}


# ============ 每日签到（每日登录积分） ============

@router.post("/motivation/checkin")
def daily_checkin(
    db: Session = Depends(get_db),
    kid_id: int = Depends(get_required_kid_id),
):
    """每日签到：当天首次签到触发 daily_login 积分（按日幂等）"""
    from app.models.star import StarRecord

    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    existed = db.query(StarRecord).filter(
        StarRecord.user_id == kid_id,
        StarRecord.action_code == "daily_login",
        StarRecord.created_at >= today_start
    ).first()

    if existed:
        return {"checked": True, "already": True, "star_delta": 0}

    service = MotivationService(db)
    result = service.trigger_action("daily_login", user_id=kid_id, reason="每日签到")
    if result is None:
        return {"checked": False, "message": "签到行为未配置"}
    return {
        "checked": True,
        "already": False,
        "star_delta": result["star_delta"],
        "new_balance": result["new_balance"],
        "unlocked_achievements": result["unlocked_achievements"],
    }


# ============ 奖励图片上传 ============

@router.post("/rewards/{reward_id}/upload-image")
async def upload_reward_image(reward_id: int, file: UploadFile = File(...), db: Session = Depends(get_db)):
    """上传奖励图片"""
    from app.models.reward import Reward

    reward = db.query(Reward).filter(Reward.id == reward_id).first()
    if not reward:
        raise HTTPException(status_code=404, detail="奖励不存在")

    # 保存文件
    upload_dir = os.path.join("backend", "uploads", "rewards")
    os.makedirs(upload_dir, exist_ok=True)

    ext = os.path.splitext(file.filename)[1] if file.filename else ".png"
    filename = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(upload_dir, filename)

    with open(file_path, "wb") as f:
        content = await file.read()
        f.write(content)

    # 更新数据库
    reward.image_url = f"/uploads/rewards/{filename}"
    db.commit()

    return {"Image_url": reward.image_url}