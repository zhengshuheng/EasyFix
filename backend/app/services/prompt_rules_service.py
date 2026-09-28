# -*- coding: utf-8 -*-
"""AI 出题规则配置服务（运营后台可维护，保障出题质量不依赖改代码）。

表：ops_prompt_rule（主库）—— scope → rule_text。
读取端（llm.py / question_prompts.py）优先取 DB 已启用项，未保存的 scope 用内置默认：
  - general             → DEFAULT_GENERAL_RULES（本文件）
  - base:科目            → question_prompts.SUBJECT_BASES
  - style:科目:学段       → question_prompts.STAGE_STYLES
空 rule_text（或删除记录）= 恢复默认。
"""
import logging

logger = logging.getLogger(__name__)

# 通用出题规则段（仅放各学科都适用的硬性规则；数学专属的看图列式/计算准确已归入 base:数学）
DEFAULT_GENERAL_RULES = """【难度标注】每道题必须给出 difficulty 字段（1-5 整数，与整体难度要求一致，允许±1浮动）：1=非常基础直接套用、2=基础略有变化、3=中等需两步思考、4=偏难需综合运用、5=困难需灵活综合运用；1-2年级不出难度5
【变式要求】围绕同一知识点的多道题，情境、物品、数据、问法必须各不相同，严禁出现只改数字/只改人名的雷同题；题目之间要有可辨识差异，避免孩子感到重复枯燥"""

# scope 元数据：供运营后台渲染（group 分组 / title 标题 / 提示）
SCOPE_META = [
    {"scope": "general", "group": "通用", "title": "通用出题规则", "tip": "所有学科出题都套用的硬性规则（难度标注 / 变式要求）。数学专属的看图列式/计算准确规则在「数学」tab 的科目基础段里。"},
    {"scope": "base:数学", "group": "数学", "title": "数学 · 科目基础段", "tip": "数学课标导向 + 语言风格 + 质量硬性要求（选择题一正三错、全卷禁止重复算式、情境去重等）。"},
    {"scope": "style:数学:小学", "group": "数学", "title": "数学 · 小学真题样式", "tip": "小学数学试卷长什么样（填空/选择/计算/应用/操作实践示例）。"},
    {"scope": "style:数学:初中", "group": "数学", "title": "数学 · 初中真题样式", "tip": "初中数学试卷长什么样（人教版初中期末/中考模拟示例）。"},
    {"scope": "style:数学:高中", "group": "数学", "title": "数学 · 高中真题样式", "tip": "高中数学试卷长什么样（必修/选择性必修示例）。"},
    {"scope": "base:语文", "group": "语文", "title": "语文 · 科目基础段", "tip": "语文课标导向 + 语言风格 + 质量硬性要求。"},
    {"scope": "style:语文:小学", "group": "语文", "title": "语文 · 小学真题样式", "tip": "小学语文试卷长什么样。"},
    {"scope": "style:语文:初中", "group": "语文", "title": "语文 · 初中真题样式", "tip": "初中语文试卷长什么样。"},
    {"scope": "base:英语", "group": "英语", "title": "英语 · 科目基础段", "tip": "英语课标导向 + 语言风格 + 质量硬性要求。"},
    {"scope": "style:英语:小学", "group": "英语", "title": "英语 · 小学真题样式", "tip": "小学英语试卷长什么样。"},
    {"scope": "style:英语:初中", "group": "英语", "title": "英语 · 初中真题样式", "tip": "初中英语试卷长什么样。"},
    {"scope": "base:默认", "group": "通用", "title": "默认科目基础段", "tip": "未知科目兜底用的通用基础段。"},
]


def load_prompt_rule_map() -> dict:
    """读主库 ops_prompt_rule 已启用规则 → {scope: rule_text}。
    未保存的 scope 不在返回里（调用方用内置默认）。表不存在/读失败返回空 dict，不影响出题。"""
    try:
        from app.database import SessionLocal
        from app.models.ops_data import OpsPromptRule
        db = SessionLocal()
        try:
            rows = db.query(OpsPromptRule).filter(OpsPromptRule.enabled.is_(True)).all()
            return {r.scope: r.rule_text for r in rows if r.rule_text and r.rule_text.strip()}
        finally:
            db.close()
    except Exception as e:  # 表未建/主库不可用 → 默认规则兜底
        logger.debug("load_prompt_rule_map 失败: %s", e)
        return {}


def get_scope_default_text(scope: str) -> str:
    """scope 的内置默认文本（DB 未保存时前端展示/读取端兜底）。"""
    if scope == "general":
        return DEFAULT_GENERAL_RULES
    if scope.startswith("base:"):
        subj = scope[len("base:"):]
        from app.services.question_prompts import SUBJECT_BASES
        return SUBJECT_BASES.get(subj, "")
    if scope.startswith("style:"):
        parts = scope.split(":")
        if len(parts) == 3:
            from app.services.question_prompts import STAGE_STYLES
            return STAGE_STYLES.get((parts[1], parts[2]), "")
    return ""
