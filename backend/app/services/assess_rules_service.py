# -*- coding: utf-8 -*-
"""评测规则配置服务（运营后台可维护，评测策略不依赖改代码）。

表：ops_assess_rule（主库）—— key → value。
读取端（assessment.py 组卷逻辑）优先取 DB 已启用项，未配置/坏值用内置默认；
空 value（或删除记录）= 恢复默认。
"""
import logging

logger = logging.getLogger(__name__)

# 评测规则元数据：key / group / title / tip / value_type / default
ASSESS_RULES_META = [
    # ---- 组卷策略 ----
    {"key": "dedup_days", "group": "组卷策略", "title": "评测排重天数", "value_type": "int", "default": 7,
     "tip": "开始新评测时，排除最近 N 天内该孩子已完成/进行中/放弃评测用过的题（防同题反复出现）。题量不足时自动放宽兜底。"},
    {"key": "variant_count", "group": "组卷策略", "title": "每次举一反三变式数", "value_type": "int", "default": 2,
     "tip": "无论库存是否充足，每次评测都额外生成 N 道同知识点新变式，保证卷子有新面孔。"},
    {"key": "refill_margin", "group": "组卷策略", "title": "缺口补题缓冲数", "value_type": "int", "default": 2,
     "tip": "按档缺口补题时每档多补 N 道缓冲，避免 AI 生成失败导致缺题。"},
    # ---- 补题难度档 ----
    {"key": "gap_diff_basic", "group": "补题难度档", "title": "基础档补题难度", "value_type": "int", "default": 2,
     "tip": "基础档缺口按该难度生成（1-5）。1-2年级 _auto_refill 内自动封顶 4。"},
    {"key": "gap_diff_mid", "group": "补题难度档", "title": "中等档补题难度", "value_type": "int", "default": 3,
     "tip": "中等档缺口按该难度生成（1-5）。"},
    {"key": "gap_diff_hard", "group": "补题难度档", "title": "拔高档补题难度", "value_type": "int", "default": 5,
     "tip": "拔高档缺口按该难度生成（1-5）。"},
    # ---- 变式难度 ----
    {"key": "variant_diff_standard", "group": "变式难度", "title": "标准卷 变式难度", "value_type": "int", "default": 3,
     "tip": "标准卷每次生成变式的目标难度（1-5）。"},
    {"key": "variant_diff_challenge", "group": "变式难度", "title": "挑战卷 变式难度", "value_type": "int", "default": 4,
     "tip": "挑战卷每次生成变式的目标难度（1-5）。"},
    {"key": "variant_diff_explore", "group": "变式难度", "title": "拓展卷 变式难度", "value_type": "int", "default": 5,
     "tip": "拓展卷每次生成变式的目标难度（1-5）。"},
    # ---- 坏题校验 ----
    {"key": "min_choice_options", "group": "坏题校验", "title": "选择题最少有效选项", "value_type": "int", "default": 2,
     "tip": "选择题有效选项少于 N 个判定为坏题，组卷时过滤（含来自题库/模板/导入的题）。"},
    # ---- 配图控制 ----
    {"key": "pictorial_ratio", "group": "配图控制", "title": "配图题占比上限", "value_type": "float", "default": 0.5,
     "tip": "低年级数学卷配图题最多占卷面的比例（0-1，如 0.5 = 最多一半）。"},
    # ---- 卷型难度占比 ----
    {"key": "ratio_standard_basic", "group": "卷型难度占比·标准", "title": "标准卷 基础档占比", "value_type": "float", "default": 0.4,
     "tip": "标准卷难度分布：基础(1-2) / 中等(3) / 拔高(4-5) 占比，三项建议合计 1。"},
    {"key": "ratio_standard_mid", "group": "卷型难度占比·标准", "title": "标准卷 中等档占比", "value_type": "float", "default": 0.4, "tip": ""},
    {"key": "ratio_standard_hard", "group": "卷型难度占比·标准", "title": "标准卷 拔高档占比", "value_type": "float", "default": 0.2, "tip": ""},
    {"key": "ratio_challenge_basic", "group": "卷型难度占比·挑战", "title": "挑战卷 基础档占比", "value_type": "float", "default": 0.2,
     "tip": "挑战卷难度分布，三项建议合计 1。"},
    {"key": "ratio_challenge_mid", "group": "卷型难度占比·挑战", "title": "挑战卷 中等档占比", "value_type": "float", "default": 0.5, "tip": ""},
    {"key": "ratio_challenge_hard", "group": "卷型难度占比·挑战", "title": "挑战卷 拔高档占比", "value_type": "float", "default": 0.3, "tip": ""},
    {"key": "ratio_explore_basic", "group": "卷型难度占比·拓展", "title": "拓展卷 基础档占比", "value_type": "float", "default": 0.1,
     "tip": "拓展卷难度分布，三项建议合计 1。"},
    {"key": "ratio_explore_mid", "group": "卷型难度占比·拓展", "title": "拓展卷 中等档占比", "value_type": "float", "default": 0.4, "tip": ""},
    {"key": "ratio_explore_hard", "group": "卷型难度占比·拓展", "title": "拓展卷 拔高档占比", "value_type": "float", "default": 0.5, "tip": ""},
]

_META_BY_KEY = {m["key"]: m for m in ASSESS_RULES_META}


def load_assess_rules() -> dict:
    """读主库 ops_assess_rule 已启用规则 → {key: 类型转换后的值}。
    未配置/坏值不在返回里（调用方用内置默认）。表不存在/读失败返回空 dict，不影响评测。"""
    try:
        from app.database import SessionLocal
        from app.models.ops_data import OpsAssessRule
        db = SessionLocal()
        try:
            rows = db.query(OpsAssessRule).filter(OpsAssessRule.enabled.is_(True)).all()
            result = {}
            for r in rows:
                meta = _META_BY_KEY.get(r.key)
                if meta is None or not r.value or not str(r.value).strip():
                    continue
                try:
                    if meta["value_type"] == "int":
                        result[r.key] = int(str(r.value).strip())
                    elif meta["value_type"] == "float":
                        result[r.key] = float(str(r.value).strip())
                    else:
                        result[r.key] = str(r.value).strip()
                except (ValueError, TypeError):
                    logger.debug("assess rule 坏值忽略 key=%s value=%r", r.key, r.value)
            return result
        finally:
            db.close()
    except Exception as e:  # 表未建/主库不可用 → 默认规则兜底
        logger.debug("load_assess_rules 失败: %s", e)
        return {}


def get_rule_default(key: str):
    """key 的内置默认值（DB 未保存时前端展示/读取端兜底）。"""
    meta = _META_BY_KEY.get(key)
    return meta["default"] if meta else None
