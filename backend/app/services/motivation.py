# backend/app/services/motivation.py
"""
激励系统核心服务
负责：积分触发、成就检查、奖励兑换
"""
from sqlalchemy.orm import Session
from app.models.star import StarAction, StarBalance, StarRecord
from app.models.achievement import Achievement, AchievementProgress, AchievementConfig
from app.models.reward import Reward, Redemption
from typing import Optional, List
from datetime import datetime, timedelta
import copy


# 默认用户ID（单用户场景）
DEFAULT_USER_ID = 1


class MotivationService:
    def __init__(self, db: Session):
        self.db = db
        # 运营权威配置快照（主库差异集）：行为/成就规则统一由运营中心配置，
        # 空间库同名表仅作兜底默认。主库有记录 → 覆盖；无 → 回退空间库。
        self._ops_actions = {}
        self._ops_achievements = {}
        self._ops_word_config = {}
        self._load_ops_snapshot()

    # ================= 运营配置覆盖（主库优先，空间库兜底） =================

    def _load_ops_snapshot(self):
        """读取主库 star_action / achievement / achievement_config（运营权威差异集）"""
        try:
            from app.database import SessionLocal
            with SessionLocal() as db:
                actions = db.query(StarAction).filter(StarAction.deleted == False).all()
                achievements = db.query(Achievement).filter(Achievement.deleted == False).all()
                configs = db.query(AchievementConfig, Achievement.code).join(
                    Achievement, AchievementConfig.achievement_id == Achievement.id
                ).all()
            self._ops_actions = {a.code: a for a in actions}
            self._ops_achievements = {(a.code, a.level): a for a in achievements}
            self._ops_word_config = {code: cfg for cfg, code in configs}
        except Exception as e:
            print(f"[motivation] 主库激励配置读取失败，回退空间库兜底: {e}")
            self._ops_actions = {}
            self._ops_achievements = {}
            self._ops_word_config = {}

    @staticmethod
    def _overlay(sa, oa):
        """以空间库记录为底（保留 id，进度记录稳定关联），用主库配置覆盖参数。
        返回浅拷贝，绝不写库（避免把主库值悄悄同步回空间库表）。"""
        merged = copy.copy(sa)
        for f in ("name", "description", "icon", "trigger_count", "reward_stars", "is_active"):
            setattr(merged, f, getattr(oa, f))
        return merged

    def _merge_achievement(self, sa: Achievement) -> Achievement:
        """单条成就三层合并：家长（空间）覆盖优先 → 主库运营默认 → 空间库模板值。
        未覆盖项用主库默认 overlay（保留空间库 id）；覆盖项数值用家长值，
        但 is_active（启停）始终随主库运营默认。"""
        oa = self._ops_achievements.get((sa.code, sa.level))
        if sa.ops_override:
            if oa is not None:
                m = copy.copy(sa)
                m.is_active = oa.is_active
                return m
            return sa
        if oa:
            return self._overlay(sa, oa)
        return sa

    def _space_achievement(self, code: str, level: int):
        return self.db.query(Achievement).filter(
            Achievement.code == code,
            Achievement.level == level,
            Achievement.deleted == False
        ).first()

    def _action(self, code: str):
        """行为配置：家长（空间）覆盖优先 → 主库运营默认 → 空间库模板值。
        家长覆盖项数值用家长值，但 enabled（启停）始终随主库运营默认。"""
        sa = self.db.query(StarAction).filter(
            StarAction.code == code,
            StarAction.deleted == False
        ).first()
        oa = self._ops_actions.get(code)
        if sa is not None and sa.ops_override:
            if oa is not None:
                m = copy.copy(sa)
                m.enabled = oa.enabled
                return m
            return sa
        if oa:
            if sa is not None:
                m = copy.copy(sa)
                for f in ("name", "star_value", "enabled"):
                    setattr(m, f, getattr(oa, f))
                return m
            return oa
        return sa

    def _achievement(self, code: str, level: int):
        """单条成就：家长（空间）覆盖优先 → 主库运营默认 → 空间库模板值。"""
        sa = self._space_achievement(code, level)
        if sa is not None and sa.ops_override:
            return sa
        oa = self._ops_achievements.get((code, level))
        if oa:
            return self._overlay(sa, oa) if sa is not None else oa
        return sa

    def _achievements_by_action(self, action_code: str) -> List[Achievement]:
        """某触发行为下的全部启用成就：逐条三层合并（家长覆盖 → 主库默认 → 模板）。"""
        space = self.db.query(Achievement).filter(
            Achievement.trigger_action == action_code,
            Achievement.deleted == False
        ).all()
        merged = [self._merge_achievement(sa) for sa in space]
        return [a for a in merged if a.is_active]

    def _achievements_by_code(self, code: str) -> List[Achievement]:
        """某系列（code）下的全部成就：逐条三层合并（家长覆盖 → 主库默认 → 模板）。"""
        space = self.db.query(Achievement).filter(
            Achievement.code == code,
            Achievement.deleted == False
        ).all()
        return [self._merge_achievement(sa) for sa in space]

    def _achievement_by_code_action(self, code: str, action_code: str):
        """按 code + 触发行为定位单条成就（连续学习系列用）。"""
        sa = self.db.query(Achievement).filter(
            Achievement.code == code,
            Achievement.trigger_action == action_code,
            Achievement.deleted == False
        ).first()
        if sa is not None and sa.ops_override:
            return sa
        oa = next((a for a in self._ops_achievements.values()
                   if a.code == code and a.trigger_action == action_code), None)
        if oa:
            return self._overlay(sa, oa) if sa is not None else oa
        return sa

    def _word_config(self, code: str = "word_accuracy"):
        """单词正确率成就配置：主库优先，空间库兜底。"""
        cfg = self._ops_word_config.get(code)
        if cfg:
            return cfg
        ach = self.db.query(Achievement).filter(
            Achievement.code == code,
            Achievement.deleted == False
        ).first()
        if not ach:
            return None
        return self.db.query(AchievementConfig).filter(
            AchievementConfig.achievement_id == ach.id
        ).first()

    def get_actions_merged(self) -> List[StarAction]:
        """合并行为列表（家长端展示）：家长（空间）覆盖优先 → 主库运营默认 → 模板值。"""
        space = self.db.query(StarAction).filter(StarAction.deleted == False).all()
        merged = []
        for sa in space:
            if sa.ops_override:
                oa = self._ops_actions.get(sa.code)
                if oa is not None:
                    m = copy.copy(sa)
                    m.enabled = oa.enabled
                    merged.append(m)
                else:
                    merged.append(sa)
                continue
            oa = self._ops_actions.get(sa.code)
            if oa:
                m = copy.copy(sa)
                for f in ("name", "star_value", "enabled"):
                    setattr(m, f, getattr(oa, f))
                merged.append(m)
            else:
                merged.append(sa)
        space_codes = {sa.code for sa in space}
        for code, oa in self._ops_actions.items():
            if code not in space_codes:
                merged.append(oa)
        return merged

    def get_achievements_merged(self) -> List[Achievement]:
        """合并成就列表：家长（空间）覆盖优先 → 主库运营默认 → 模板值。"""
        space = self.db.query(Achievement).filter(Achievement.deleted == False).all()
        merged = [self._merge_achievement(sa) for sa in space]
        space_keys = {(sa.code, sa.level) for sa in space}
        for key, oa in self._ops_achievements.items():
            if key not in space_keys:
                merged.append(oa)
        return merged

    def overlay_achievement(self, sa: Achievement) -> Achievement:
        """对单条空间库成就应用三层合并（读接口用）。"""
        return self._merge_achievement(sa)

    def get_or_create_balance(self, user_id: int = DEFAULT_USER_ID) -> StarBalance:
        """获取或创建用户积分余额"""
        balance = self.db.query(StarBalance).filter(StarBalance.user_id == user_id).first()
        if not balance:
            balance = StarBalance(user_id=user_id, balance=0)
            self.db.add(balance)
            self.db.commit()
            self.db.refresh(balance)
        return balance

    def trigger_action(self, action_code: str, user_id: int = DEFAULT_USER_ID, reason: str = None) -> Optional[dict]:
        """
        触发积分行为
        返回：积分变动信息和成就解锁信息
        """
        # 查找启用的行为（运营配置优先）
        action = self._action(action_code)
        if not action or not action.enabled:
            return None

        # 获取余额
        balance = self.get_or_create_balance(user_id)

        # 记录积分明细
        new_balance = balance.balance + action.star_value
        record = StarRecord(
            user_id=user_id,
            action_code=action_code,
            star_delta=action.star_value,
            balance_after=new_balance,
            reason=reason or action.name
        )
        self.db.add(record)

        # 更新余额
        balance.balance = new_balance
        self.db.commit()

        # 检查成就
        unlocked_achievements = self._check_achievements(user_id, action_code)

        # 检查连续学习
        self.check_continuous_learning(user_id)

        return {
            "star_delta": action.star_value,
            "new_balance": new_balance,
            "unlocked_achievements": unlocked_achievements
        }

    def _check_achievements(self, user_id: int, action_code: str) -> List[dict]:
        """检查并更新成就进度"""
        unlocked = []

        # 查找所有因该行为触发的成就（运营配置优先）
        achievements = self._achievements_by_action(action_code)

        for achievement in achievements:
            # 计算该用户在该成就系列上的总进度
            total_count = self._get_achievement_total_count(user_id, achievement.trigger_action)

            # 获取或创建进度记录
            progress = self.db.query(AchievementProgress).filter(
                AchievementProgress.user_id == user_id,
                AchievementProgress.achievement_id == achievement.id
            ).first()

            if not progress:
                progress = AchievementProgress(
                    user_id=user_id,
                    achievement_id=achievement.id,
                    current_count=0,
                    is_unlocked=False
                )
                self.db.add(progress)

            # 检查是否达成（需先达成上一级）
            if achievement.level == 1 or self._is_previous_level_unlocked(user_id, achievement.code, achievement.level):
                if total_count >= achievement.trigger_count and not progress.is_unlocked:
                    progress.is_unlocked = True
                    progress.unlocked_at = datetime.now()
                    progress.current_count = total_count

                    # 发放成就奖励积分
                    if achievement.reward_stars > 0:
                        self._add_stars(user_id, achievement.reward_stars, f"成就奖励：{achievement.name} Lv{achievement.level}")

                    unlocked.append({
                        "achievement_id": achievement.id,
                        "name": achievement.name,
                        "level": achievement.level,
                        "reward_stars": achievement.reward_stars
                    })

                    # 自动创建下一级进度记录
                    self._create_next_level_progress(user_id, achievement)
                else:
                    progress.current_count = total_count

        self.db.commit()
        return unlocked

    def _is_previous_level_unlocked(self, user_id: int, code: str, level: int) -> bool:
        """检查上一级是否已解锁"""
        if level <= 1:
            return True

        previous_achievement = self._achievement(code, level - 1)

        if not previous_achievement:
            return True

        previous_progress = self.db.query(AchievementProgress).filter(
            AchievementProgress.user_id == user_id,
            AchievementProgress.achievement_id == previous_achievement.id,
            AchievementProgress.is_unlocked == True
        ).first()

        return previous_progress is not None

    def _create_next_level_progress(self, user_id: int, current_achievement: Achievement):
        """为当前成就的下一级创建进度记录"""
        next_achievement = self._achievement(current_achievement.code, current_achievement.level + 1)

        if next_achievement:
            existing = self.db.query(AchievementProgress).filter(
                AchievementProgress.user_id == user_id,
                AchievementProgress.achievement_id == next_achievement.id
            ).first()

            if not existing:
                progress = AchievementProgress(
                    user_id=user_id,
                    achievement_id=next_achievement.id,
                    current_count=0,
                    is_unlocked=False
                )
                self.db.add(progress)

    def _get_achievement_total_count(self, user_id: int, trigger_action: str) -> int:
        """获取用户已完成该行为的总次数（按小孩隔离统计）"""
        from sqlalchemy import func
        from app.models.word import WordProgress
        from app.models.practice_set import PracticeSet
        from app.models.error_question import ErrorQuestion
        from app.models.similar_question import SimilarQuestion

        # review_word：该小孩累计复习单词次数（WordProgress 按 user_id 隔离）
        if trigger_action == "review_word":
            count = self.db.query(func.coalesce(func.sum(WordProgress.review_count), 0)).filter(
                WordProgress.user_id == user_id
            ).scalar() or 0
            return count

        # review_practice_set：该小孩累计复习练习集次数
        if trigger_action == "review_practice_set":
            count = self.db.query(func.coalesce(func.sum(PracticeSet.review_count), 0)).filter(
                PracticeSet.user_id == user_id,
                PracticeSet.deleted == False
            ).scalar() or 0
            return count

        # upload_question：该小孩手动录入/导入的错题数
        if trigger_action == "upload_question":
            count = self.db.query(func.count(ErrorQuestion.id)).filter(
                ErrorQuestion.user_id == user_id,
                ErrorQuestion.deleted == False
            ).scalar() or 0
            return count

        # generate_similar：该小孩错题生成的相似题数（SimilarQuestion 经 source_question 归属小孩）
        if trigger_action == "generate_similar":
            count = self.db.query(func.count(SimilarQuestion.id)).join(
                ErrorQuestion, SimilarQuestion.source_question_id == ErrorQuestion.id
            ).filter(
                ErrorQuestion.user_id == user_id,
                ErrorQuestion.deleted == False,
                SimilarQuestion.deleted == False
            ).scalar() or 0
            return count

        # 其他行为统计 StarRecord 次数
        count = self.db.query(func.count(StarRecord.id)).filter(
            StarRecord.user_id == user_id,
            StarRecord.action_code == trigger_action
        ).scalar()
        return count or 0

    def _add_stars(self, user_id: int, stars: int, reason: str):
        """手动增加积分"""
        balance = self.get_or_create_balance(user_id)
        new_balance = balance.balance + stars

        record = StarRecord(
            user_id=user_id,
            action_code="reward",
            star_delta=stars,
            balance_after=new_balance,
            reason=reason
        )
        self.db.add(record)
        balance.balance = new_balance
        self.db.commit()

    def _add_star_record(self, user_id: int, action_code: str, star_delta: int, reason: str):
        """内部方法：添加积分记录"""
        balance = self.get_or_create_balance(user_id)
        new_balance = balance.balance + star_delta

        record = StarRecord(
            user_id=user_id,
            action_code=action_code,
            star_delta=star_delta,
            balance_after=new_balance,
            reason=reason
        )
        self.db.add(record)
        balance.balance = new_balance
        self.db.commit()

    def check_continuous_learning(self, user_id: int = None) -> List[dict]:
        """检查并更新连续学习成就"""
        if user_id is None:
            user_id = DEFAULT_USER_ID

        unlocked = []

        # 获取连续学习相关的行为
        continuous_actions = ['continuous_7day', 'continuous_14day', 'continuous_30day']

        # 查询用户的学习日期记录（只统计练习完成）
        records = self.db.query(StarRecord).filter(
            StarRecord.user_id == user_id,
            StarRecord.action_code == 'review_practice_set'
        ).order_by(StarRecord.created_at.desc()).all()

        if not records:
            return unlocked

        # 提取唯一的学习日期
        study_dates = set()
        for r in records:
            date_str = r.created_at.strftime('%Y-%m-%d') if isinstance(r.created_at, datetime) else datetime.strptime(str(r.created_at), '%Y-%m-%d %H:%M:%S').strftime('%Y-%m-%d')
            study_dates.add(date_str)

        study_dates = sorted(study_dates, reverse=True)

        # 检查每个连续学习成就
        for action_code in continuous_actions:
            achievement = self._achievement_by_code_action('continuous_learning', action_code)

            if not achievement:
                continue

            days = achievement.trigger_count

            # 计算连续天数
            consecutive_days = 0
            today = datetime.now().strftime('%Y-%m-%d')

            for i in range(days):
                check_date = (datetime.now() - timedelta(days=i)).strftime('%Y-%m-%d')
                if check_date in study_dates:
                    consecutive_days += 1
                else:
                    break

            # 检查是否解锁
            progress = self.db.query(AchievementProgress).filter(
                AchievementProgress.user_id == user_id,
                AchievementProgress.achievement_id == achievement.id
            ).first()

            if not progress:
                progress = AchievementProgress(
                    user_id=user_id,
                    achievement_id=achievement.id,
                    current_count=0,
                    is_unlocked=False
                )
                self.db.add(progress)

            if consecutive_days >= days and not progress.is_unlocked:
                progress.is_unlocked = True
                progress.unlocked_at = datetime.now()
                progress.current_count = consecutive_days

                # 发放奖励积分
                if achievement.reward_stars > 0:
                    self._add_stars(user_id, achievement.reward_stars, f"成就奖励：{achievement.name} Lv{achievement.level}")

                # 触发该行为记录
                self._add_star_record(user_id, action_code, achievement.reward_stars, f"连续学习成就解锁：{achievement.name}")

                unlocked.append({
                    "achievement_id": achievement.id,
                    "name": achievement.name,
                    "level": achievement.level,
                    "reward_stars": achievement.reward_stars
                })

        self.db.commit()
        return unlocked

    def check_word_accuracy(self, user_id: int, total_count: int, correct_count: int, reason: str = None) -> Optional[dict]:
        """检查单词正确率成就（累计模式）
        每次复习满足条件（≥min_words且正确率≥min_accuracy%）时增加进度
        进度达到trigger_count时解锁对应等级
        """
        # 获取成就配置（运营配置优先）
        config = self._word_config("word_accuracy")

        min_words = config.min_words if config else 10
        min_accuracy = config.min_accuracy if config else 90

        # 计算正确率
        accuracy = (correct_count / total_count * 100) if total_count > 0 else 0

        # 检查是否满足触发条件
        if total_count < min_words or accuracy < min_accuracy:
            return None

        # 获取所有单词正确率成就（按等级排序，运营配置优先）
        achievements = sorted(
            self._achievements_by_code("word_accuracy"),
            key=lambda a: a.level
        )

        if not achievements:
            return None

        unlocked_results = []

        # 找出当前用户已解锁的最高等级
        highest_unlocked_level = 0
        for ach in achievements:
            progress = self.db.query(AchievementProgress).filter(
                AchievementProgress.user_id == user_id,
                AchievementProgress.achievement_id == ach.id,
                AchievementProgress.is_unlocked == True
            ).first()
            if progress:
                highest_unlocked_level = ach.level

        # 确定当前应该增加进度的成就等级
        # 如果全部未解锁，从level 1开始
        # 如果已有解锁的，从下一个未解锁的等级开始
        current_target_level = highest_unlocked_level + 1 if highest_unlocked_level < len(achievements) else None

        if current_target_level is None:
            # 所有等级都已解锁，无需继续
            return None

        # 查找当前目标成就
        target_achievement = None
        for ach in achievements:
            if ach.level == current_target_level:
                target_achievement = ach
                break

        if not target_achievement:
            return None

        # 获取或创建进度记录
        progress = self.db.query(AchievementProgress).filter(
            AchievementProgress.user_id == user_id,
            AchievementProgress.achievement_id == target_achievement.id
        ).first()

        if not progress:
            progress = AchievementProgress(
                user_id=user_id,
                achievement_id=target_achievement.id,
                current_count=0,
                is_unlocked=False
            )
            self.db.add(progress)

        # 增加进度（每次满足条件就+1）
        progress.current_count += 1

        # 检查是否达到解锁条件
        if progress.current_count >= target_achievement.trigger_count:
            progress.is_unlocked = True
            progress.unlocked_at = datetime.now()

            # 发放奖励积分
            if target_achievement.reward_stars > 0:
                self._add_stars(user_id, target_achievement.reward_stars, f"成就奖励：{target_achievement.name} Lv{target_achievement.level}")
                self._add_star_record(user_id, "review_word_accuracy", target_achievement.reward_stars, reason or f"单词正确率成就解锁 Lv{target_achievement.level}")

            unlocked_results.append({
                "achievement_id": target_achievement.id,
                "name": target_achievement.name,
                "level": target_achievement.level,
                "reward_stars": target_achievement.reward_stars,
                "current_count": progress.current_count,
                "trigger_count": target_achievement.trigger_count
            })

        self.db.commit()

        if unlocked_results:
            return {
                "unlocked_achievements": unlocked_results,
                "accuracy": accuracy,
                "total_count": total_count,
                "correct_count": correct_count
            }

        # 条件满足但未解锁，返回当前进度
        return {
            "progress": {
                "level": current_target_level,
                "current_count": progress.current_count,
                "trigger_count": target_achievement.trigger_count
            },
            "accuracy": accuracy,
            "total_count": total_count,
            "correct_count": correct_count
        }

    def redeem_reward(self, reward_id: int, user_id: int = DEFAULT_USER_ID) -> dict:
        """兑换奖励"""
        reward = self.db.query(Reward).filter(
            Reward.id == reward_id,
            Reward.is_active == True,
            Reward.deleted == False
        ).first()

        if not reward:
            raise ValueError("奖励不存在或已下架")

        balance = self.get_or_create_balance(user_id)

        if balance.balance < reward.cost_stars:
            raise ValueError("积分不足")

        if reward.remaining_stock > 0 and reward.remaining_stock < 1:
            raise ValueError("库存不足")

        # 扣除积分
        new_balance = balance.balance - reward.cost_stars
        record = StarRecord(
            user_id=user_id,
            action_code="redeem",
            star_delta=-reward.cost_stars,
            balance_after=new_balance,
            reason=f"兑换：{reward.name}"
        )
        self.db.add(record)
        balance.balance = new_balance

        # 减少库存
        if reward.remaining_stock > 0:
            reward.remaining_stock -= 1

        # 创建兑换记录
        redemption = Redemption(
            user_id=user_id,
            reward_id=reward_id,
            star_cost=reward.cost_stars
        )
        self.db.add(redemption)
        self.db.commit()

        return {
            "success": True,
            "new_balance": new_balance,
            "reward_name": reward.name
        }