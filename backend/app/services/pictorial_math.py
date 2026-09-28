"""
图示算式模板引擎（低年级 1-2 年级）

背景：市面教辅的数学卷在低年级大量使用"图示算式"——用动物/物品图示承载数字信息，
配合算式填空（如 🐤🐤 + 🐤🐤 = ？、1 + ？ = 7、？+？ = 7、3 组 × 每组 4 个 = ？），
帮助儿童从"可数的具体对象"过渡到"抽象符号运算"（课标第一学段：利用画图、实物操作
等方法表达情境中的数量关系，体会几何直观）。

与 AI 出题（llm.py）的区别：
- AI 出的 visual 只是"文字题的示意图"，不承载题目信息（"不要求精确等于题干所有数字"）；
- 本引擎的 visual 是"题目本身"——left_count/right_count 就是算式里的数，图与算式严格一致。

设计原则：
- 确定性生成：不依赖 LLM，数字/物品/句式由模板代码控制，保证不超纲、图数匹配、答案唯一。
- visual 类型 count-split（左右两堆物品 + 运算符 + 未知位置）：
    {"type":"count-split","left_emoji":"🐤","left_count":3,"right_emoji":"🐤","right_count":4,
     "operator":"+","unknown":"sum","label":"小鸟","max_count":7}
  unknown 取值：
    - "sum"          ：两堆全可见，求总数（看图列式：3+4=？，答案7）
    - "addend_left"  ：右堆可见，左堆是问号（？+4=7，答案3）—— 二年级未知加数
    - "addend_right" ：左堆可见，右堆是问号（3+？=7，答案4）—— 二年级未知加数
    - "minuend"      ：总数与右堆可见，左堆是问号（？-4=3，答案7）—— 求被减数（二年级）
    - "subtrahend"   ：总数与左堆可见，右堆是问号（7-？=3，答案4）—— 求减数（二年级）
    - "remainder"    ：两堆全可见，求差（7-4=？，答案3）—— 一年级看图列式（减法）
    - "decompose"    ：两堆都是问号（？+？=7），答案集合（分解训练，二年级）
    - "mul_sum"      ：乘法意义 group（3 组 × 每组 4 个 → 4+4+4=？，答案12，二年级）
"""
from __future__ import annotations

import random
from typing import Any, Dict, List

# 低年级数学常用物品 → emoji + 计量单位（与 assessment.py _ITEM_EMOJI 一致，避免视觉冲突）
# 单位按物品自然计量词：动物=只、条；水果蔬菜=个/颗/根；文具/日用品=支/本/块/把
_ITEMS = [
    ("小鸟", "🐤", "只"), ("小鸡", "🐥", "只"), ("小鸭", "🦆", "只"), ("小兔", "🐰", "只"), ("小猫", "🐱", "只"),
    ("小狗", "🐶", "只"), ("小猴", "🐵", "只"), ("小熊", "🐻", "只"), ("小鱼", "🐟", "条"), ("金鱼", "🐟", "条"),
    ("苹果", "🍎", "个"), ("桃子", "🍑", "个"), ("草莓", "🍓", "颗"), ("香蕉", "🍌", "根"), ("葡萄", "🍇", "颗"),
    ("西瓜", "🍉", "个"), ("橙子", "🍊", "个"), ("樱桃", "🍒", "颗"), ("糖果", "🍬", "颗"), ("饼干", "🍪", "块"),
    ("气球", "🎈", "个"), ("花朵", "🌸", "朵"), ("星星", "⭐", "颗"), ("蘑菇", "🍄", "个"), ("胡萝卜", "🥕", "根"),
    ("足球", "⚽", "个"), ("皮球", "⚽", "个"), ("积木", "🧱", "块"), ("贝壳", "🐚", "个"),
]

# 10 以内加法对（用于一年级看图列式，和 ≤10）
_ADD_PAIRS_10 = [(a, b) for a in range(1, 10) for b in range(1, 10) if a + b <= 10]
# 20 以内不进位加法对（一年级下：和 ≤20，个位不进位或简单进位可控）
_ADD_PAIRS_20 = [(a, b) for a in range(2, 12) for b in range(2, 12) if a + b <= 20]
# 乘法组：组数×每组个数 ≤ 24（二年级表内乘法前段）
_MUL_SETS = [(g, p) for g in range(2, 7) for p in range(2, 6) if g * p <= 24]


def _item() -> tuple[str, str, str]:
    """随机选一个物品（返回 名称, emoji, 单位词）"""
    return random.choice(_ITEMS)


def _cn(n: int) -> str:
    """数字 → 中文（1-20）"""
    digits = ["零", "一", "二", "三", "四", "五", "六", "七", "八", "九", "十",
              "十一", "十二", "十三", "十四", "十五", "十六", "十七", "十八", "十九", "二十"]
    return digits[n] if 0 <= n <= 20 else str(n)


def _fill_stem(label: str, a: int, b: int, op: str, unknown: str, unit: str = "个") -> str:
    """生成题干文本。unknown 决定问号位置。unit 为物品自然计量单位（动物=只/水果=个/草莓=颗…）。
    所有分支题干必须自带数量（数字），不依赖配图——孩子没图也能读题作答（历史教训：id=717 旧版 sum 分支
    生成"看图列式：小鸡一共有（　）只（个）。"无数字无 visual，孩子无法作答）。"""
    if op == "+":
        if unknown == "sum":
            return f"看图列式：左边有{a}{unit}{label}，右边有{b}{unit}，一共有（　）{unit}。"
        if unknown == "addend_left":
            return f"左边有（　）{unit}{label}，右边有{b}{unit}，一共有{a + b}{unit}。左边有多少{unit}？"
        if unknown == "addend_right":
            return f"左边有{a}{unit}{label}，右边有（　）{unit}，一共有{a + b}{unit}。右边有多少{unit}？"
        if unknown == "decompose":
            return f"{a + b}可以分成几和几？（填两个数）"
    else:  # "-"
        if unknown == "remainder":
            return f"看图列式：一共有{a + b}{unit}{label}，去掉{b}{unit}，还剩（　）{unit}。"
        if unknown == "minuend":
            return f"一共（　）{unit}{label}，飞走了{b}{unit}，还剩{a}{unit}。原来一共有多少{unit}？"
        if unknown == "subtrahend":
            return f"一共有{a + b}{unit}{label}，飞走了（　）{unit}，还剩{a}{unit}。飞走了多少{unit}？"
    return ""


def generate_pictorial_questions(grade: int, count: int = 10) -> List[Dict[str, Any]]:
    """生成低年级图示算式题（返回可直接入库的题目 dict，与 AI 出题结构一致）。

    grade=1：看图列式（加法求和 / 减法求剩余），和/被减数 ≤10（上学期）或 ≤20（下学期）。
    grade=2：未知加数 / 求被减数 / 求减数（和 ≤20）、数的分解、乘法意义 group 图（≤24）。
    """
    questions: List[Dict[str, Any]] = []
    if grade == 1:
        # 一年级：看图列式，以 10 以内为主、混合少量 20 以内
        for _ in range(count):
            if random.random() < 0.7:
                a, b = random.choice(_ADD_PAIRS_10)
                op, unknown = "+", "sum"
            else:
                a, b = random.choice(_ADD_PAIRS_20)
                op, unknown = "+", "sum"
            label, emoji, unit = _item()
            questions.append(_build_add_question(a, b, label, emoji, op, unknown, grade=1, unit=unit))
    elif grade == 2:
        for _ in range(count):
            r = random.random()
            if r < 0.35:
                # 未知加数：1+？=7 或 ？+3=7（和 ≤20）
                a, b = random.choice(_ADD_PAIRS_20)
                unknown = random.choice(["addend_left", "addend_right"])
                label, emoji, unit = _item()
                questions.append(_build_add_question(a, b, label, emoji, "+", unknown, grade=2, unit=unit))
            elif r < 0.5:
                # 求被减数/减数：？-4=3、7-？=3
                a, b = random.choice(_ADD_PAIRS_10)
                unknown = random.choice(["minuend", "subtrahend"])
                label, emoji, unit = _item()
                questions.append(_build_add_question(a, b, label, emoji, "-", unknown, grade=2, unit=unit))
            elif r < 0.65:
                # 数的分解：？+？=N（答案集合）
                s = random.randint(3, 10)
                questions.append(_build_decompose_question(s))
            else:
                # 乘法意义 group：3 组 × 每组 4 个 → 4+4+4=？
                g, p = random.choice(_MUL_SETS)
                questions.append(_build_mul_question(g, p))
    return questions


def _build_add_question(a: int, b: int, label: str, emoji: str, op: str, unknown: str, grade: int, unit: str = "个") -> Dict[str, Any]:
    """构造一道加减法图示算式题"""
    total = a + b
    visual: Dict[str, Any] = {
        "type": "count-split",
        "left_emoji": emoji,
        "left_count": a if unknown not in ("addend_left", "minuend") else None,  # None=问号
        "right_emoji": emoji,
        "right_count": b if unknown not in ("addend_right", "subtrahend") else None,
        "operator": op,
        "unknown": unknown,
        "label": label,
        "unit": unit,
        "max_count": total if op == "+" else max(a + b, a),
    }
    if op == "+":
        answer = str(total)
        if unknown == "addend_left":
            answer = str(a)
        elif unknown == "addend_right":
            answer = str(b)
    else:
        if unknown == "remainder":
            answer = str(a)
        elif unknown == "minuend":
            answer = str(a + b)
        else:  # subtrahend
            answer = str(b)
    stem = _fill_stem(label, a, b, op, unknown, unit)
    return {
        "question": stem,
        "options": [],
        "answer": answer,
        "explanation": f"看图数一数，列式计算。{label}的数量和问号合起来就是答案。",
        "knowledge_point": "看图列式" if grade == 1 else ("求未知加数" if unknown in ("addend_left", "addend_right")
                                                          else "加减法各部分关系"),
        "question_type": "fill",
        "question_category": "scene",
        "difficulty": 1 if grade == 1 else 2,
        "visual": visual,
    }


def _build_decompose_question(total: int) -> Dict[str, Any]:
    """？+？=N 分解题（答案接受任意一对和为 N 的数）"""
    visual: Dict[str, Any] = {
        "type": "count-split",
        "left_emoji": "⭐",
        "left_count": None,
        "right_emoji": "⭐",
        "right_count": None,
        "operator": "+",
        "unknown": "decompose",
        "label": "星星",
        "max_count": total,
    }
    return {
        "question": f"{_cn(total)}可以分成几和几？",
        "options": [],
        "answer": f"{total}=?+?",
        "explanation": f"{total}可以分成很多组：如 {total - 1}+1、{total - 2}+2……只要两个数加起来等于{total}都对。",
        "knowledge_point": "数的分解",
        "question_type": "fill",
        "question_category": "thinking",
        "difficulty": 2,
        "visual": visual,
    }


def _build_mul_question(groups: int, per: int) -> Dict[str, Any]:
    """乘法意义：3 组 × 每组 4 个 → 4+4+4=？ 或 3×4=？"""
    label, emoji, unit = _item()
    total = groups * per
    visual: Dict[str, Any] = {
        "type": "count-split",
        "left_emoji": emoji,
        "left_count": per,
        "right_emoji": emoji,
        "right_count": groups,
        "operator": "×",
        "unknown": "mul_sum",
        "label": label,
        "unit": unit,
        "max_count": total,
    }
    return {
        "question": f"看图列式：有{groups}组{label}，每组{per}{unit}，一共有（　）{unit}。",
        "options": [],
        "answer": str(total),
        "explanation": f"{per}+{per}+{per}（共{groups}组）={total}，也就是{groups}×{per}={total}。",
        "knowledge_point": "乘法的意义",
        "question_type": "fill",
        "question_category": "scene",
        "difficulty": 2,
        "visual": visual,
    }


if __name__ == "__main__":
    random.seed(42)
    for g in (1, 2):
        print(f"===== 年级 {g} 示例 =====")
        for q in generate_pictorial_questions(g, 5):
            print(f"  {q['question']}")
            print(f"    答案={q['answer']} 知识点={q['knowledge_point']}")
            print(f"    visual={q['visual']}")
