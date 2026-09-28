"""练习链路服务：出卷快照 → 作答记录 → 错题派生与缓存统计。

设计（用户拍板）：
- 错题 = 批改判错的**派生结果**，进 error_question；手动上传的错题 source='upload'（保留来源）。
- 错题与练习题目互存对方 id，但内容各存快照，互不影响。
- 作答记录按次留在 practice_attempt，是统计的唯一事实来源（删除练习集也不丢）。
- 错题的复习次数/正确率用 error_question 的**缓存列**，每次批改同事务更新，可用
  recalc_error_question_stats 全量重算兜底。
- 连续答对 MASTERED_STREAK 次 → status='mastered'，移出错题本（组卷不再抽到）。
"""
from datetime import datetime
import re
from typing import Iterable, List, Optional

from sqlalchemy.orm import Session

from app.models.error_book import ErrorBook
from app.models.error_question import ErrorQuestion
from app.models.practice_attempt import PracticeAttempt
from app.models.practice_question import PracticeQuestion
from app.models.subject import Subject

MASTERED_STREAK = 2  # 连续答对 2 次判定已掌握，移出错题本


# ---------------- 出卷：写题目快照 ----------------

def create_practice_question(
    db: Session,
    *,
    user_id: int,
    subject_id: int,
    source: str = "ai",
    grade: Optional[int] = None,
    semester: Optional[int] = None,
    parsed_question: Optional[str] = None,
    answer: Optional[str] = None,
    analysis: Optional[str] = None,
    options: Optional[Iterable[str]] = None,
    question_type: Optional[str] = None,
    question_category: Optional[str] = None,
    knowledge_point: Optional[str] = None,
    difficulty: Optional[int] = None,
    error_type: Optional[str] = None,
    original_text: Optional[str] = None,
    original_images: Optional[str] = None,
    error_question_id: Optional[int] = None,
    visual: Optional[str] = None,
) -> PracticeQuestion:
    """写入一道练习题目的快照"""
    opts = [o for o in (options or [])][:4]
    pq = PracticeQuestion(
        user_id=user_id,
        subject_id=subject_id,
        source=source,
        grade=grade,
        semester=semester,
        parsed_question=parsed_question,
        answer=answer,
        analysis=analysis,
        option_a=opts[0] if len(opts) > 0 else None,
        option_b=opts[1] if len(opts) > 1 else None,
        option_c=opts[2] if len(opts) > 2 else None,
        option_d=opts[3] if len(opts) > 3 else None,
        question_type=question_type,
        question_category=question_category,
        knowledge_point=knowledge_point,
        difficulty=difficulty if difficulty else 3,
        error_type=error_type,
        original_text=original_text if original_text is not None else parsed_question,
        original_images=original_images,
        error_question_id=error_question_id,
        visual=visual,
    )
    db.add(pq)
    db.flush()
    return pq


def snapshot_from_error_question(db: Session, eq: ErrorQuestion, *, user_id: int) -> PracticeQuestion:
    """错题复习组卷：把错题内容复制成练习题目快照（双向关联，内容各自独立）"""
    return create_practice_question(
        db,
        user_id=user_id,
        subject_id=eq.subject_id,
        source="error_review",
        grade=eq.grade,
        semester=eq.semester,
        parsed_question=eq.parsed_question,
        answer=eq.answer,
        analysis=eq.analysis,
        options=[eq.option_a, eq.option_b, eq.option_c, eq.option_d],
        question_type=eq.question_type,
        question_category=eq.question_category,
        knowledge_point=eq.knowledge_point,
        difficulty=eq.difficulty,
        error_type=eq.error_type,
        original_text=eq.original_text,
        original_images=eq.original_images,
        error_question_id=eq.id,
    )


# ---------------- AI 题目后置清洗（按科目规则，防"张冠李戴"） ----------------
# 背景：AI 出题 prompt 按科目分开（question_prompts.py），但 LLM 偶尔仍会
# 在英语"看图数数"题里泄漏答案（"（图中一共有 5 个苹果）"）或"看图"却无图。
# 这里在入库前做规则级兜底，只处理明确模式，避免误删正常情境信息（如"你的名字叫Amy"）。

_EN_ITEM_EMOJI = {
    "apple": "🍎", "apples": "🍎",
    "banana": "🍌", "bananas": "🍌",
    "orange": "🍊", "oranges": "🍊",
    "pear": "🍐", "pears": "🍐",
    "grape": "🍇", "grapes": "🍇",
    "strawberry": "🍓", "strawberries": "🍓",
    "peach": "🍑", "peaches": "🍑",
    "watermelon": "🍉",
    "lemon": "🍋", "lemons": "🍋",
    "pencil": "✏️", "pencils": "✏️",
    "pen": "🖊️", "pens": "🖊️",
    "book": "📚", "books": "📚",
    "crayon": "🖍️", "crayons": "🖍️",
    "ruler": "📏", "rulers": "📏",
    "bag": "🎒", "bags": "🎒",
    "ball": "⚽", "balls": "⚽",
    "kite": "🪁", "kites": "🪁",
    "cake": "🎂", "cakes": "🎂",
    "egg": "🥚", "eggs": "🥚",
    "cookie": "🍪", "cookies": "🍪",
    "star": "⭐", "stars": "⭐",
    "flower": "🌸", "flowers": "🌸",
    "tree": "🌳", "trees": "🌳",
    "car": "🚗", "cars": "🚗",
    "bird": "🐦", "birds": "🐦",
    "cat": "🐱", "cats": "🐱",
    "dog": "🐶", "dogs": "🐶",
    "duck": "🦆", "ducks": "🦆",
    "rabbit": "🐰", "rabbits": "🐰",
    "fish": "🐟", "fishes": "🐟",
}

_CN_DIGITS = {
    "零": 0, "一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5, "六": 6,
    "七": 7, "八": 8, "九": 9, "十": 10, "十一": 11, "十二": 12, "十三": 13,
    "十四": 14, "十五": 15, "十六": 16, "十七": 17, "十八": 18, "十九": 19, "二十": 20,
}
_EN_DIGITS = {
    "zero": 0, "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6,
    "seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11, "twelve": 12,
    "thirteen": 13, "fourteen": 14, "fifteen": 15, "sixteen": 16, "seventeen": 17,
    "eighteen": 18, "nineteen": 19, "twenty": 20,
}


def _answer_number(answer: str) -> Optional[int]:
    """把纯数字/中文数字/英文单词数字的答案解析为 int；复合答案（如 'Amy; seven'）取第一个英文数字；否则 None"""
    a = (answer or "").strip().lower()
    if not a:
        return None
    if a.isdigit():
        return int(a)
    if a in _CN_DIGITS:
        return _CN_DIGITS[a]
    for w, n in _EN_DIGITS.items():
        if a == w or a.startswith(w + ";") or a.startswith(w + ",") or a.startswith(w + " "):
            return n
    return None


def _strip_answer_hint(stem: str, answer: str) -> str:
    """删除题干中暴露答案的括号提示，仅当括号内含数量词且数字=答案数字。
    例："There are ____ apples. （图中一共有 5 个苹果）" → "There are ____ apples. "
    保守策略：不含数量词（一共/共有/总共）的括号不删（如情境设定"你的名字叫Amy"）。"""
    num = _answer_number(answer)
    if num is None:
        return stem
    cn = next((k for k, v in _CN_DIGITS.items() if v == num), None)

    def _drop(m: "re.Match") -> str:
        seg = m.group(0)
        has_qty = ("一共" in seg or "共有" in seg or "总共" in seg)
        has_num = (str(num) in seg or (cn and cn in seg))
        return "" if (has_qty and has_num) else seg

    out = re.sub(r"[（(][^（）()]*?[）)]", _drop, stem)
    return out.rstrip(" 。.，,；;：:") or stem


def _ensure_picture(stem: str, answer: str) -> str:
    """'看图'类题但题干没有任何图（emoji）→ 按物品词+答案数量补 emoji 图（数量 1-12 才补，防拥挤）"""
    low = stem.lower()
    if not any(k in low for k in ("看图", "图中有", "picture", "数一数")):
        return stem
    if re.search(r"[\U0001F300-\U0001FAFF\u2600-\u27BF]", stem):
        return stem  # 已有 emoji 图，不重复补
    num = _answer_number(answer)
    if num is None or not (1 <= num <= 12):
        return stem
    for w, e in _EN_ITEM_EMOJI.items():
        if re.search(rf"\b{re.escape(w)}\b", low):
            return stem.rstrip("。. ") + f" ({e * num})"
    return stem


# 数学物品 → 自然计量单位（与 pictorial_math._ITEMS 一致；修正 AI 题面"只（个）"冗余/单位错误）
_MATH_ITEM_UNITS = {
    "小鸟": "只", "小鸡": "只", "小鸭": "只", "小兔": "只", "小猫": "只",
    "小狗": "只", "小猴": "只", "小熊": "只", "小鱼": "条", "金鱼": "条",
    "苹果": "个", "桃子": "个", "草莓": "颗", "香蕉": "根", "葡萄": "颗",
    "西瓜": "个", "橙子": "个", "樱桃": "颗", "糖果": "颗", "饼干": "块",
    "气球": "个", "花朵": "朵", "星星": "颗", "蘑菇": "个", "胡萝卜": "根",
    "足球": "个", "皮球": "个", "积木": "块", "贝壳": "个", "铅笔": "支",
    "课本": "本", "本子": "本", "橡皮": "块", "尺子": "把", "鸡蛋": "个",
    "橘子": "个", "梨": "个", "面包": "个",
}


def _fix_math_unit(q: str) -> str:
    """把题面"只（个）/（个）"按物品自然单位替换；无匹配物品则去掉冗余"（个）"后缀。"""
    unit = None
    for label, u in _MATH_ITEM_UNITS.items():
        if label in q:
            unit = u
            break
    if unit:
        q = q.replace("只（个）", unit).replace("（个）", unit)
        q = q.replace("（　）" + unit, "（　）" + unit)  # 保持空位格式
    else:
        # 无物品词：去掉"N只（个）""N个（个）"这类冗余后缀（单位保留前者）
        q = re.sub(r"(\d+|（　）)(只|个|条|颗|根|朵|块|支|本|把)（个）", r"\1\2", q)
    return q


def _collect_visual_nums(visual: dict) -> list:
    """收集配图场景里承载数量信息的字段值（max_count 只是上限，不算数量）"""
    nums = []
    for k in ("left_count", "right_count", "count", "groups", "per_group", "num"):
        v = visual.get(k)
        if isinstance(v, int) and v > 0:
            nums.append(v)
    return nums


def _sanitize_math_item(item: dict):
    """数学 AI 出题入库前自检（规则验证，非 LLM 复审，快速可靠）：
    1. 无数量空位题——"看图列式：X一共有（　）只（个）。"且题干没有任何数字
       → 图缺失时孩子无法作答，返回 None 拒绝入库（调用方跳过）。
    2. 单位修正——"只（个）/（个）"冗余或物品单位错误（如"草莓…只"）
       → 按物品自然计量单位替换（动物=只/条，水果=个/颗，胡萝卜=根…）。
    3. visual 数量一致性——配图场景里的每个数量必须都出现在题干数字中
       （图数矛盾会误导孩子）→ 不一致则清除 visual，让 detect_scene 重新兜底。
    直接修改并返回 item；返回 None 表示该题不合格。
    """
    q = item.get("question") or ""
    if not q:
        return item
    # 1. 无数量空位题（去掉空位后仍无数字 → 图缺失时无法作答）
    no_blank = re.sub(r"[（(]\s*[　 ]*\s*[)）]", "", q)
    # "一共有/一共"里的"一"是助词不是数量，先剔除避免误判
    no_check = no_blank.replace("一共有", "").replace("一共", "")
    if "看图列式" in q and not re.search(r"\d+|[一二三四五六七八九十]", no_check):
        return None
    # 2. 单位修正
    new_q = _fix_math_unit(q)
    if new_q != q:
        item["question"] = new_q
        if "original_text" in item:
            item["original_text"] = new_q
    # 3. visual 数量一致性
    visual = item.get("visual")
    if isinstance(visual, dict):
        stem_nums = [int(n) for n in re.findall(r"\d+", new_q)]
        bad = [n for n in _collect_visual_nums(visual) if n not in stem_nums]
        if bad:
            item["visual"] = None
            item.pop("scene", None)
    return item


def sanitize_ai_item(item: dict, subject_id: int) -> dict:
    """AI 出题结果入库前的科目化后置清洗/自检（数学：单位/数量/配图一致性；英语：fill 去答案泄漏 + 看图补图）。
    直接修改并返回 item；数学不合格题返回 None（调用方跳过入库）。"""
    if subject_id == 1:
        return _sanitize_math_item(item)
    if subject_id != 2:
        return item
    qt = item.get("question_type") or ""
    q = item.get("question") or ""
    if qt != "fill" or not q:
        return item
    ans = item.get("answer") or ""
    new_q = _strip_answer_hint(q, ans)
    new_q = _ensure_picture(new_q, ans)
    if new_q != q:
        item["question"] = new_q
        if "original_text" in item:
            item["original_text"] = new_q
    return item


def snapshot_from_ai_item(
    db: Session,
    item: dict,
    *,
    user_id: int,
    subject_id: int,
    grade: Optional[int],
    question_types: Optional[List[str]] = None,
    question_categories: Optional[List[str]] = None,
    default_knowledge_point: Optional[str] = None,
) -> PracticeQuestion:
    """AI 出题结果 → 练习题目快照（数学不合格题（自检拒绝）返回 None，调用方跳过）"""
    if sanitize_ai_item(item, subject_id) is None:  # 科目化后置清洗/自检（数学：单位/数量/配图；英语：去答案泄漏/看图补图）
        return None
    qt = item.get("question_type") or (question_types[0] if question_types and len(question_types) == 1 else None)
    qc = item.get("question_category") or (
        question_categories[0] if question_categories and len(question_categories) == 1 else None
    )
    # 配图场景：LLM 生成的结构化 visual，或由题干规则识别（detect_scene 兜底）
    visual = item.get("visual")
    if not visual and item.get("question") and subject_id == 1:
        try:
            from app.routers.assessment import detect_scene
            from types import SimpleNamespace
            scene = detect_scene(SimpleNamespace(
                parsed_question=item.get("question"),
                original_text=item.get("question"),
                subject_id=subject_id,
            ))
            if scene:
                import json as _json
                visual = _json.dumps(scene, ensure_ascii=False)
        except Exception:
            pass
    return create_practice_question(
        db,
        user_id=user_id,
        subject_id=subject_id,
        source="ai",
        grade=grade,
        parsed_question=item.get("question"),
        answer=item.get("answer"),
        analysis=item.get("explanation", ""),
        options=item.get("options") or [],
        question_type=qt,
        question_category=qc,
        knowledge_point=item.get("knowledge_point") or default_knowledge_point,
        difficulty=item.get("difficulty") or 3,
        error_type="",
        original_text=item.get("question"),
        visual=visual,
    )


# ---------------- 错题本 ----------------

def ensure_error_book(db: Session, user_id: int, subject_id: int) -> ErrorBook:
    """按（孩子, 学科）取错题本，没有就建一个"""
    book = db.query(ErrorBook).filter(
        ErrorBook.user_id == user_id,
        ErrorBook.subject_id == subject_id,
        ErrorBook.deleted == False,  # noqa: E712
    ).first()
    if book:
        return book
    subject = db.get(Subject, subject_id)
    book = ErrorBook(
        name=f"{subject.name}错题本" if subject else "错题本",
        subject_id=subject_id,
        user_id=user_id,
    )
    db.add(book)
    db.flush()
    return book


def upsert_error_question_from_practice_question(
    db: Session, pq: PracticeQuestion, user_id: Optional[int] = None, source: str = "practice"
) -> ErrorQuestion:
    """练习题判错 → 派生错题（同一道练习题只派生一次，幂等）
    source: 来源标识 practice=练习批改 / assessment=评测答错，统一进同一个错题集合。"""
    existing = db.query(ErrorQuestion).filter(
        ErrorQuestion.source_practice_question_id == pq.id,
        ErrorQuestion.deleted == False,  # noqa: E712
    ).first()
    if existing:
        return existing
    kid = user_id if user_id is not None else pq.user_id
    book = ensure_error_book(db, kid, pq.subject_id)
    now = datetime.now()
    eq = ErrorQuestion(
        user_id=kid,
        error_book_id=book.id,
        subject_id=pq.subject_id,
        original_text=pq.original_text,
        original_images=pq.original_images,
        parsed_question=pq.parsed_question,
        answer=pq.answer,
        analysis=pq.analysis,
        option_a=pq.option_a,
        option_b=pq.option_b,
        option_c=pq.option_c,
        option_d=pq.option_d,
        grade=pq.grade,
        semester=pq.semester,
        question_type=pq.question_type,
        question_category=pq.question_category,
        knowledge_point=pq.knowledge_point,
        difficulty=pq.difficulty,
        error_type=pq.error_type,
        source=source,
        source_practice_question_id=pq.id,
        review_count=0,
        correct_count=0,
        wrong_count=0,
        correct_streak=0,
        status="active",
        first_wrong_at=now,
        last_wrong_at=now,
    )
    db.add(eq)
    db.flush()
    return eq


# ---------------- 批改：作答记录 + 缓存列 ----------------

def apply_review_result(eq: ErrorQuestion, is_correct: bool) -> None:
    """按一次作答结果更新错题缓存列（同事务内调用）"""
    eq.review_count = (eq.review_count or 0) + 1
    if is_correct:
        eq.correct_count = (eq.correct_count or 0) + 1
        eq.correct_streak = (eq.correct_streak or 0) + 1
    else:
        eq.wrong_count = (eq.wrong_count or 0) + 1
        eq.correct_streak = 0
        eq.last_wrong_at = datetime.now()
    eq.accuracy = round(eq.correct_count / eq.review_count * 100, 1) if eq.review_count else None
    if (eq.correct_streak or 0) >= MASTERED_STREAK:
        eq.status = "mastered"       # 连续答对 2 次 → 移出错题本
    elif eq.status == "mastered":
        eq.status = "active"         # 掌握后又错了 → 回到错题本


def record_attempt(
    db: Session,
    *,
    practice_set_id: Optional[int],
    practice_question: PracticeQuestion,
    student_answer: Optional[str] = None,
    is_correct: Optional[bool] = None,
    user_id: Optional[int] = None,
    graded_by: Optional[str] = None,
    duration_seconds: Optional[int] = None,
) -> PracticeAttempt:
    """写一行作答记录；判错时派生/关联错题并同步缓存列（幂等不覆盖历史）"""
    kid = user_id if user_id is not None else practice_question.user_id
    eq: Optional[ErrorQuestion] = None
    if practice_question.error_question_id:
        eq = db.get(ErrorQuestion, practice_question.error_question_id)
    elif is_correct is False:
        eq = upsert_error_question_from_practice_question(db, practice_question, kid)
        if eq is not None:
            practice_question.error_question_id = eq.id  # 回填：该练习题已对应错题

    attempt = PracticeAttempt(
        user_id=kid,
        practice_set_id=practice_set_id,
        practice_question_id=practice_question.id,
        error_question_id=eq.id if eq else None,
        student_answer=student_answer,
        is_correct=is_correct,
        graded_by=graded_by,
        duration_seconds=duration_seconds,
    )
    db.add(attempt)
    if eq is not None and is_correct is not None:
        apply_review_result(eq, bool(is_correct))
    return attempt


def latest_attempt_map(db: Session, practice_set_id: int) -> dict:
    """练习集内每道题的最新一次作答结果 {practice_question_id: (student_answer, is_correct)}"""
    rows = db.query(PracticeAttempt).filter(
        PracticeAttempt.practice_set_id == practice_set_id,
    ).order_by(PracticeAttempt.answered_at.asc(), PracticeAttempt.id.asc()).all()
    latest = {}
    for r in rows:
        latest[r.practice_question_id] = r
    return latest


def max_attempt_id(db: Session, practice_set_id: int) -> Optional[int]:
    row = db.query(PracticeAttempt.id).filter(
        PracticeAttempt.practice_set_id == practice_set_id,
    ).order_by(PracticeAttempt.id.desc()).first()
    return row[0] if row else None


# ---------------- 兜底：全量重算 ----------------

def recalc_error_question_stats(db: Session, eq: ErrorQuestion) -> None:
    """从作答记录全量重算缓存列（数据修复/对账用）"""
    rows = db.query(PracticeAttempt).filter(
        PracticeAttempt.error_question_id == eq.id,
    ).order_by(PracticeAttempt.answered_at.asc(), PracticeAttempt.id.asc()).all()
    total = len(rows)
    correct = sum(1 for r in rows if r.is_correct is True)
    wrong = sum(1 for r in rows if r.is_correct is False)
    streak = 0
    for r in reversed(rows):
        if r.is_correct is True:
            streak += 1
        else:
            break
    eq.review_count = total
    eq.correct_count = correct
    eq.wrong_count = wrong
    eq.accuracy = round(correct / total * 100, 1) if total else None
    eq.correct_streak = streak
    eq.status = "mastered" if streak >= MASTERED_STREAK else "active"
