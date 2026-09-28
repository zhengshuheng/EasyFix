"""
卷面分值计算 —— 把卷面总分分配到每道题上

两种计分方式（供 PDF 与详情页共用，保证「打印出来的卷子」和「屏幕上看到的卷子」分值一致）：
- hundred：百分制，整卷满分固定 100 分（按题型权重先把总分分给各题型大题，再在大题内均分到每题）
- default：按题型内置分值（选择题 3 分、填空 3 分、应用 6 分……），总分自然累加

分配结果与题目传入顺序无关：内部按题型分组、组内按传入相对顺序，
因此详情接口与 PDF 生成对同一份卷子会算出完全相同的每题分值。
"""
from typing import Any, Dict, List

# 各题型单题默认分值（与 pdf.PracticeSetPDF.TYPE_SCORES 保持一致）
DEFAULT_TYPE_SCORES: Dict[str, int] = {
    "choice": 3, "fill": 3, "judge": 2, "calc": 4, "application": 6,
    "operation": 5, "reading": 4, "writing": 10, "sentence": 2,
}

# 大题排列顺序（选择题 → 填空题 → …… ，与卷面大题序号一致）
TYPE_ORDER: Dict[str, int] = {
    "choice": 1, "fill": 2, "judge": 3, "calc": 4, "application": 5,
    "operation": 6, "reading": 7, "writing": 8, "sentence": 9,
}

SCORE_MODE_HUNDRED = "hundred"
SCORE_MODE_DEFAULT = "default"
SCORE_MODES = (SCORE_MODE_HUNDRED, SCORE_MODE_DEFAULT)
DEFAULT_SCORE_MODE = SCORE_MODE_HUNDRED
HUNDRED_TOTAL = 100


def normalize_score_mode(mode: Any) -> str:
    """归一化计分方式，未知值按百分制处理"""
    value = str(mode or "").strip().lower()
    if value in SCORE_MODES:
        return value
    return DEFAULT_SCORE_MODE


def type_weight(question_type: Any) -> int:
    return DEFAULT_TYPE_SCORES.get(str(question_type or ""), 3)


def _group_order(question_type: str) -> int:
    return TYPE_ORDER.get(question_type, 99) if question_type else 99


def compute_question_scores(
    questions: List[Dict[str, Any]],
    score_mode: Any = DEFAULT_SCORE_MODE,
    total: int = HUNDRED_TOTAL,
) -> List[int]:
    """返回与 questions 等长的每题分值列表

    Args:
        questions: 题目列表，每项至少要有 question_type 字段（可为空字符串）
        score_mode: hundred=百分制（满分 total）/ default=题型默认分值
        total: 百分制的整卷满分
    """
    n = len(questions)
    if n == 0:
        return []

    types = [str(q.get("question_type") or "") for q in questions]

    if normalize_score_mode(score_mode) == SCORE_MODE_DEFAULT:
        return [type_weight(t) for t in types]

    # 按题型分组（组内保持传入相对顺序）
    grouped: Dict[str, List[int]] = {}
    for idx, t in enumerate(types):
        grouped.setdefault(t, []).append(idx)
    keys = sorted(grouped.keys(), key=_group_order)

    # 题数多于满分（极端情况）：每题 1 分
    if n >= total:
        return [1] * n

    weights = [type_weight(k) * len(grouped[k]) for k in keys]
    weight_sum = sum(weights) or len(keys)
    raw = [total * w / weight_sum for w in weights]
    section_totals = [max(1, int(r)) for r in raw]

    diff = total - sum(section_totals)
    # 余数按小数部分从大到小补分（并列时题多的大题优先）
    order = sorted(
        range(len(keys)),
        key=lambda i: (-(raw[i] - int(raw[i])), -len(grouped[keys[i]]), i),
    )
    k = 0
    while diff > 0:
        section_totals[order[k % len(order)]] += 1
        diff -= 1
        k += 1
    while diff < 0:
        for i in sorted(range(len(keys)), key=lambda j: -section_totals[j]):
            if diff == 0:
                break
            if section_totals[i] > 1:
                section_totals[i] -= 1
                diff += 1

    scores = [0] * n
    for key, sec_total in zip(keys, section_totals):
        idxs = grouped[key]
        count = len(idxs)
        base, extra = divmod(sec_total, count)
        if base < 1:
            base, extra = 1, 0
        for j, idx in enumerate(idxs):
            scores[idx] = base + (1 if j < extra else 0)
    return scores


def total_score(questions: List[Dict[str, Any]], score_mode: Any = DEFAULT_SCORE_MODE,
                total: int = HUNDRED_TOTAL) -> int:
    """整卷总分"""
    return sum(compute_question_scores(questions, score_mode, total))
