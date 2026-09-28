"""
能力评测路由 - 家长可评测小孩的学习程度与能力
组卷：按学科+年级从题库抽题，覆盖不同知识点，输出等级与知识点掌握情况
数据隔离：孩子身份一律从 X-Kid-Id 请求头解析（见 app/utils/kid_context.py），
          评测记录按孩子隔离；写入类接口（start/submit）要求必须先选孩子。
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import desc, case
from typing import Optional
from datetime import datetime, timedelta
from pydantic import BaseModel
import random
import json
import re
from app.database import get_db
from app.models import PracticeQuestion, AssessmentRecord, Subject
from app.utils.kid_context import get_current_kid_id, get_required_kid_id, filter_by_kid

router = APIRouter(prefix="/api/assessment", tags=["评测"])

# 等级阈值：答对比例
_LEVELS = [
    (0.8, "优秀"),
    (0.5, "良好"),
    (0.0, "待提升"),
]

# 卷型难度占比（基础=difficulty1-2 / 中等=3 / 拓展=4-5）
# 教育理念（docs/ASSESSMENT_DESIGN.md）：拔高=本年级深度变式（跳一跳够得着），不是超纲题；
# 拓展=可选轻探（摸上限，不强制）。默认标准卷=检验课内掌握。
PAPER_RATIOS = {
    "standard": {"basic": 0.4, "mid": 0.4, "hard": 0.2},
    "challenge": {"basic": 0.2, "mid": 0.5, "hard": 0.3},
    "explore": {"basic": 0.1, "mid": 0.4, "hard": 0.5},
}
PAPER_TYPE_NAMES = {"standard": "标准卷", "challenge": "拔高卷", "explore": "拓展卷"}


def _difficulty_tier(d) -> str:
    """难度 1-5 → 档位（basic/mid/hard）。缺失按中等处理。"""
    d = d or 3
    if d <= 2:
        return "basic"
    if d == 3:
        return "mid"
    return "hard"


def _mastery_level(tier_stats: dict) -> dict:
    """本年级内掌握等级定位（教育理念：不跨年级判"该学几年级"，只在本年级内分层）。
    - 基础<60%                → pending   待巩固（先打牢基础，不急着上难度）
    - 基础≥60% 且 中等<60%     → foundation 基础掌握（中等还欠火候，建议专项巩固）
    - 中等≥60% 且 拓展<60%     → solid     掌握良好（可挑战拔高/深度变式）
    - 拓展≥60%                → advanced  学有余力（可深度拓展，仍在本年级深度内）
    返回 {level, label, advice, strengths[], weaknesses[]}
    """
    def rate(t):
        s = tier_stats.get(t) or {"total": 0, "correct": 0.0}
        return (s["correct"] / s["total"]) if s["total"] else None

    b, m, h = rate("basic"), rate("mid"), rate("hard")
    if b is None and m is None and h is None:
        return {"level": "pending", "label": "待巩固", "advice": "本次作答题目不足，暂无法定位，建议再做一次完整评测", "strengths": [], "weaknesses": []}
    if b is not None and b < 0.6:
        level, label, advice = "pending", "待巩固", "基础题还没有完全拿稳，先回到课内把基础打牢，再挑战更灵活的题"
    elif m is not None and m < 0.6:
        level, label, advice = "foundation", "基础掌握", "基础已过关，中等题还欠火候，建议针对弱项知识点做专项巩固"
    elif h is not None and h < 0.6:
        level, label, advice = "solid", "掌握良好", "课内知识掌握得不错，可以挑战拔高卷——跳一跳够得着的深度变式题"
    else:
        level, label, advice = "advanced", "学有余力", "这份卷子已经难不倒你，可以挑战更灵活的拓展题，把同一个知识点玩出更多花样"

    # 强项/弱项知识点（按正确率；total>=1 才参与）
    def rate_of(item):
        return (item["correct"] / item["total"]) if item["total"] else None

    knowledge = tier_stats.get("knowledge", [])
    strengths = sorted(
        [{"name": k["name"], "rate": rate_of(k)} for k in knowledge if rate_of(k) is not None and rate_of(k) >= 0.8],
        key=lambda x: -x["rate"],
    )[:3]
    weaknesses = sorted(
        [{"name": k["name"], "rate": rate_of(k)} for k in knowledge if rate_of(k) is not None and rate_of(k) < 0.6],
        key=lambda x: x["rate"],
    )[:3]
    return {"level": level, "label": label, "advice": advice, "strengths": strengths, "weaknesses": weaknesses}


def _build_tier_stats(detail: list, knowledge: list) -> dict:
    """从判分明细构建难度维度统计（基础/中等/拓展 正确率）。
    旧记录 detail 无 difficulty → 按中等(3)兜底，不影响统计。"""
    stats = {"basic": {"total": 0, "correct": 0.0}, "mid": {"total": 0, "correct": 0.0}, "hard": {"total": 0, "correct": 0.0}}
    for d in detail:
        t = _difficulty_tier(d.get("difficulty"))
        stats[t]["total"] += 1
        stats[t]["correct"] += float(d.get("correct", 0) or 0)
    stats["knowledge"] = knowledge
    return stats

ASSESS_QUESTION_COUNT = 10  # 每次评测题数（可调）

# 评测排重窗口（天）：开始新评测时，排除最近 N 天内该孩子同学科同年级已完成评测用过的题，
# 避免同一套题反复出现，反馈真实能力。题量不足时自动放宽（近期题兜底）。
RECENT_EXCLUDE_DAYS = 7

# 学科题型白名单（组卷用）：None=不限题型。
# 应用题/计算题是数学题型，英语/语文学科不允许混入（否则会出现"英语化的数学卷"，如 qid 72）
_SUBJECT_ALLOW_TYPES = {
    1: None,                      # 数学：全部题型
    2: {"choice", "fill", "judge", "sentence", "reading", "writing"},  # 英语：无应用题
    3: {"choice", "fill", "judge", "sentence", "reading", "writing"},  # 语文：无应用题
}

# ==================== 图示算式题（低年级 1-2 数学，模板引擎生成） ====================
# 与 AI 出题不同：visual 的 count-split 是"题目本身"，图与算式严格一致，
# 对应课标第一学段"利用画图、实物操作等方法表达情境中的数量关系"（看图列式/求未知数/乘法意义）。


def _ensure_pictorial_questions(db: Session, subject_id: int, grade: int, uid: int, want: int) -> int:
    """保证低年级数学题库里有足量的图示算式题（不足时用模板引擎生成入库，确定性、秒级）
    返回当前图示题总量（题库中已有的 + 本次新增的）
    """
    if subject_id != 1 or grade not in (1, 2):
        return 0
    try:
        from app.services.pictorial_math import generate_pictorial_questions
        from app.services.practice_flow import create_practice_question
        import json as _json
    except Exception:
        return 0
    # 统计当前图示题（visual 含 count-split 的数学低年级题）
    existing = db.query(PracticeQuestion).filter(
        PracticeQuestion.subject_id == subject_id,
        PracticeQuestion.grade == grade,
        PracticeQuestion.deleted == False,  # noqa: E712
        PracticeQuestion.visual.isnot(None),
    ).all()
    have = 0
    for qq in existing:
        try:
            v = json.loads(qq.visual) if isinstance(qq.visual, str) else qq.visual
        except Exception:
            v = None
        if isinstance(v, dict) and v.get("type") == "count-split":
            have += 1
    if have >= want:
        return have
    # 生成补齐（每次多生成几道，留余量；避免重复可随机性自然覆盖）
    need = want - have + 3
    try:
        items = generate_pictorial_questions(grade, need)
    except Exception:
        return have
    for item in items:
        try:
            # 入库前自检（模板引擎绕过 AI sanitize，必须在这兜住）：
            # 1) "看图列式"题干必须自带数量数字（无图也能作答，历史教训：id=717 无数字坏题）
            # 2) 图示题必须带有效 visual（count-split/group 等），否则前端无图、题面残缺
            q = item.get("question") or ""
            if "看图列式" in q and not re.search(r"\d", q.replace("（　）", "").replace("()", "")):
                continue
            v = item.get("visual")
            if not (isinstance(v, dict) and v.get("type") in ("count-split", "group", "count", "shape")):
                continue
            create_practice_question(
                db,
                user_id=uid,
                subject_id=subject_id,
                source="template",
                grade=grade,
                parsed_question=item.get("question"),
                answer=item.get("answer"),
                analysis=item.get("explanation", ""),
                options=[],
                question_type=item.get("question_type"),
                question_category=item.get("question_category"),
                knowledge_point=item.get("knowledge_point"),
                difficulty=item.get("difficulty", 2),
                error_type="",
                original_text=item.get("question"),
                visual=_json.dumps(item.get("visual"), ensure_ascii=False),
            )
        except Exception:
            continue
    db.commit()
    return have + (len(items) if items else 0)


# ==================== 自动补齐：学科×年级知识点清单 ====================
# 从教材目录与已有题库提炼；评测题库不足时按此清单让 AI 生成新题入库
_REFILL_KPS = {
    # 数学
    (1, 1): ["10以内加减法", "20以内进位加法（凑十法）", "11~20各数的认识", "比多少", "认识图形", "位置（上、下、前、后）"],
    (1, 2): ["100以内进位加法", "100以内退位减法", "表内乘法（2-5的乘法口诀）", "平均分", "长度单位：厘米和米", "图形认识：三角形/正方形/长方形"],
    (1, 3): ["万以内加法", "万以内减法", "多位数乘一位数", "长方形和正方形的周长", "分数的初步认识", "质量单位：千克和克", "时间的认识与计算"],
    # 英语
    (2, 1): ["26个英文字母的认读与书写", "问候语（Hello/Goodbye/Good morning）", "自我介绍（My name is...）", "数字1-10", "颜色词汇（red/blue/yellow/green）", "文具词汇（book/pen/pencil/ruler）", "动物词汇（cat/dog/bird/fish）", "水果词汇（apple/banana/orange）"],
    (2, 2): ["家庭成员（father/mother/brother/sister）", "数字11-20", "身体部位（head/hand/eye/ear）", "食物词汇（rice/bread/milk/egg）", "动物词汇（elephant/monkey/panda/tiger）", "常用句型（I like.../How old are you?）", "方位词（in/on/under）", "情态动词can的用法"],
    (2, 3): ["be动词am/is/are的用法", "不定冠词a/an的用法", "一般现在时助动词do/does", "一般疑问句Do/Does...", "一般现在时主谓一致", "in表示上午/下午/晚上"],
    # 语文
    (3, 1): ["汉语拼音：声母", "汉语拼音：韵母", "整体认读音节", "简单汉字笔画笔顺", "简单反义词", "量词搭配", "看图识词"],
    (3, 2): ["读拼音写词语", "形近字组词", "反义词与近义词", "词语搭配（的/地/得）", "把字句与被字句", "标点符号", "古诗积累（咏鹅/静夜思）", "看图写话基础"],
    (3, 3): ["多音字辨析", "成语积累（含动物成语）", "修改病句", "关联词", "古诗默写（望庐山瀑布/绝句）", "比喻句与拟人句", "阅读理解（短文中找信息）", "作文开头"],
}
# 学科名映射（LLM 出题用）
_SUBJECT_NAME = {1: "数学", 2: "英语", 3: "语文"}
# 学科默认题型池（LLM 出题用）
_SUBJECT_TYPES = {
    1: ["calc", "fill", "choice", "application"],
    2: ["choice", "fill", "judge", "sentence"],
    3: ["fill", "choice", "judge", "reading"],
}

# ==================== 专项评测（按义务教育课程标准设计） ====================
# 专项 = 学科内知识模块（知识点分组）。kp_pool 为知识点关键词池（子串匹配），
# 用于组卷收窄题目池 + AI 补题限定知识点。词条风格与 _REFILL_KPS / AI 生成题
# 的 knowledge_point 命名一致。min_grade/max_grade 为课标适用学段（前端按年级提示）。
SPECIALTIES = {
    1: [  # 数学
        {"key": "math_calc", "name": "数与运算", "desc": "口算/笔算/估算，检验计算功底",
         "pool": ["加减法", "乘法", "除法", "计算", "口算", "估算", "数的认识", "数的分解", "分数", "小数", "运算", "混合", "比多少", "平均分", "时间", "质量", "长度", "人民币", "进位", "退位"],
         "types": ["calc", "fill", "choice"], "min_grade": 1, "max_grade": 6},
        {"key": "math_word", "name": "解决问题", "desc": "数量关系与应用题，学会用数学解决实际问题",
         "pool": ["应用题", "问题", "购物", "相差", "倍数", "平均分", "比多少", "行程", "工程", "浓度", "利润"],
         "types": ["application", "fill", "choice"], "min_grade": 1, "max_grade": 9},
        {"key": "math_geom", "name": "图形与几何", "desc": "认识图形、周长面积体积、角度与位置",
         "pool": ["图形", "周长", "面积", "体积", "角", "位置", "方向", "长度", "立体", "对称"],
         "types": ["choice", "fill", "judge"], "min_grade": 1, "max_grade": 9},
        {"key": "math_algebra", "name": "代数与方程", "desc": "有理数、代数式、方程不等式、函数",
         "pool": ["有理数", "代数式", "方程", "不等式", "函数", "整式", "分式", "根式"],
         "types": ["fill", "choice"], "min_grade": 7, "max_grade": 9},
        {"key": "math_stat", "name": "统计与概率", "desc": "数据收集整理、平均数、可能性",
         "pool": ["统计", "概率", "平均数", "数据", "可能性", "中位数", "众数", "方差"],
         "types": ["choice", "fill"], "min_grade": 3, "max_grade": 9},
        {"key": "math_reason", "name": "综合实践与说理", "desc": "开放题、多解、讲题说理，锻炼深度思维",
         "pool": ["说理", "开放", "多解", "综合", "推理", "逻辑", "规律", "探究"],
         "types": ["fill", "choice", "application"], "min_grade": 1, "max_grade": 9},
    ],
    2: [  # 英语
        {"key": "eng_phonics", "name": "自然拼读与语音", "desc": "字母发音、字母组合、拼读规则",
         "pool": ["拼读", "发音", "字母", "语音", "音标", "phonics"],
         "types": ["choice", "fill"], "min_grade": 1, "max_grade": 6},
        {"key": "eng_words", "name": "词汇认读与拼写", "desc": "单词词义、拼写、词类",
         "pool": ["单词", "词汇", "拼写", "词义", "词类"],
         "types": ["choice", "fill"], "min_grade": 1, "max_grade": 9},
        {"key": "eng_sentence", "name": "句型与语法", "desc": "时态、句式、be动词、there be",
         "pool": ["句型", "语法", "时态", "句式", "be动词", "there be", "疑问句", "否定句"],
         "types": ["choice", "fill", "judge", "sentence"], "min_grade": 3, "max_grade": 9},
        {"key": "eng_reading", "name": "阅读理解", "desc": "短篇理解、信息查找、主旨大意",
         "pool": ["阅读", "短文", "理解", "主旨", "信息"],
         "types": ["choice", "reading"], "min_grade": 3, "max_grade": 9},
    ],
    3: [  # 语文
        {"key": "chn_pinyin", "name": "拼音与识字", "desc": "声母韵母、拼读、字形字音",
         "pool": ["拼音", "声母", "韵母", "音节", "认读", "字形", "字音", "多音字", "识字"],
         "types": ["choice", "fill"], "min_grade": 1, "max_grade": 2},
        {"key": "chn_words", "name": "词语积累与运用", "desc": "近反义词、成语、词语搭配、语境选词",
         "pool": ["词语", "成语", "近义词", "反义词", "搭配", "形近字", "关联词", "标点"],
         "types": ["choice", "fill"], "min_grade": 1, "max_grade": 9},
        {"key": "chn_poetry", "name": "古诗文积累与理解", "desc": "课标必背古诗、文言短文、默写与理解",
         "pool": ["古诗", "诗", "文言", "默写", "绝句", "律诗", "词"],
         "types": ["fill", "choice"], "min_grade": 1, "max_grade": 9},
        {"key": "chn_reading", "name": "阅读理解", "desc": "短文概括、词句理解、主旨情感、赏析",
         "pool": ["阅读", "理解", "短文", "概括", "赏析", "主旨", "情感", "修辞"],
         "types": ["choice", "fill", "reading"], "min_grade": 1, "max_grade": 9},
    ],
}


def _kp_in_pool(kp, pool) -> bool:
    """知识点是否属于专项池（子串匹配，兼容题库/生成题命名差异）"""
    if not kp:
        return False
    return any(p and p in kp for p in pool)


def _get_specialty(subject_id: int, key: str):
    """按 key 查专项配置（不存在或不属于学科 → None）"""
    for s in SPECIALTIES.get(subject_id, []):
        if s["key"] == key:
            return s
    return None


def _specialty_name(subject_id: int, key: str):
    """专项 key → 展示名（None/未知 key → 原样）"""
    if not key:
        return None
    sp = _get_specialty(subject_id, key)
    return sp["name"] if sp else key


def _auto_refill(db: Session, subject_id: int, grade: int, needed: int, uid: int, difficulty: int = None, avoid_stems: set = None, knowledge_points: list = None) -> int:
    """题库不足时自动调 AI 生成题目并入库（归属当前小孩），返回实际生成数。
    difficulty：目标难度（1-5），None 时按年级默认（1-2年级=2，3年级=3）。
    avoid_stems：近期已展示过的题干集合，传给 LLM 避免撞题（举一反三：生成同知识点新变式而非原题）。
    knowledge_points：限定知识点池（专项评测补题用；None 时按学科×年级默认清单）。
    LLM 按目标难度出题并在每题标注 difficulty；漏标/越界时以目标难度兜底并夹到 1-5
    （1-2年级封顶 4，不超纲——教育理念：宁可简单不超纲）。"""
    try:
        from app.services.llm import llm_service
        from app.services.practice_flow import snapshot_from_ai_item
    except Exception:
        return 0
    kps = knowledge_points or (_REFILL_KPS.get((subject_id, grade)) or [f"{_SUBJECT_NAME.get(subject_id, '')}基础知识"])
    subject_name = _SUBJECT_NAME.get(subject_id, "")
    types = _SUBJECT_TYPES.get(subject_id, ["fill", "choice"])
    target = difficulty if difficulty is not None else (2 if grade <= 2 else 3)
    if grade <= 2:
        target = min(target, 4)
    # 一次生成 needed 道（LLM 可能少出，多要一些兜底）
    result = llm_service.generate_questions_by_knowledge(
        knowledge_points=kps,
        subject=subject_name,
        grade=grade,
        count=max(needed, 4),
        difficulty=target,
        question_types=types,
        avoid_stems=avoid_stems,
    )
    if result.get("error"):
        return 0
    created = 0
    for item in result.get("questions", []):
        try:
            # LLM 漏标/越界难度 → 目标难度兜底并夹取；1-2年级封顶 4
            d = item.get("difficulty")
            if not isinstance(d, int) or not (1 <= d <= 5):
                d = target
            elif grade <= 2 and d > 4:
                d = 4
            item["difficulty"] = d
            pq = snapshot_from_ai_item(
                db, item,
                user_id=uid,
                subject_id=subject_id,
                grade=grade,
                question_types=types,
                default_knowledge_point=kps[0],
            )
            if pq is not None:  # 自检拒绝的不合格题（如无数量空位题）不计入
                created += 1
        except Exception:
            continue
    db.commit()
    return created


def _level_for(rate: float) -> str:
    for threshold, name in _LEVELS:
        if rate >= threshold:
            return name
    return "待提升"


def _recent_done_question_ids(db: Session, uid: int, subject_id: int, grade: int, days: int = RECENT_EXCLUDE_DAYS) -> tuple:
    """最近 N 天该孩子该学科该年级用过的题目 (id 集合, 题干集合)（新评测组卷排重用）。
    含 done/in_progress/quit：只要题面展示过（含连续切卷后被放弃的卷子），7 天内不重复出，
    保证连续切换不同级别卷子时题目不雷同、每次卷子都有新面孔。
    题干排重兜住 AI 变式撞题（同一题干新生成题 id 不同，仅按 id 防不住）。
    题量不足时调用方会自动放宽（近期题兜底），所以这里只收集、不做决策。"""
    since = datetime.now() - timedelta(days=days)
    ids = set()
    stems = set()
    recs = db.query(AssessmentRecord).filter(
        AssessmentRecord.user_id == uid,
        AssessmentRecord.subject_id == subject_id,
        AssessmentRecord.grade == grade,
        AssessmentRecord.status.in_(["done", "in_progress", "quit"]),
        AssessmentRecord.created_at >= since,
    ).all()
    for r in recs:
        for field in (r.detail, r.questions):
            if not field:
                continue
            try:
                for d in json.loads(field):
                    qid = d.get("question_id")
                    if qid:
                        ids.add(int(qid))
                    s = (d.get("stem") or d.get("parsed_question") or d.get("question") or "").strip()
                    if s:
                        stems.add(s)
            except Exception:
                continue
    return ids, stems


def _sync_error_questions(db: Session, uid: int, detail: list) -> None:
    """评测结果同步到统一错题集：
    - 答错（correct<1，含 0.5 半对）→ 自动入库（source='assessment'，同题幂等复用一条）
    - 答对（correct==1）→ 该题在错题集的 active 记录置 mastered（从错题本自动排除）
    错题本查询只过滤 deleted/status/source!='ai'，评测错题与练习错题同池可见可复习。
    """
    from app.models import ErrorQuestion
    from app.services.practice_flow import upsert_error_question_from_practice_question

    for d in detail:
        qid = d.get("question_id")
        if not qid:
            continue
        # 未作答（空答案）的题不进错题集：只有输入了答案且判错的才算错题
        if not (d.get("user_answer") or "").strip():
            continue
        pq = db.query(PracticeQuestion).get(qid)
        if not pq:
            continue
        correct = d.get("correct", 0)
        if correct < 1:
            eq = upsert_error_question_from_practice_question(db, pq, user_id=uid, source="assessment")
            # 缓存列口径：至少统计"被评测错过一次"（评测不写 practice_attempt）
            eq.review_count = (eq.review_count or 0) + 1
            eq.wrong_count = (eq.wrong_count or 0) + 1
            eq.correct_streak = 0
            eq.last_wrong_at = datetime.now()
            eq.status = "active"  # 重新犯错 → 回到错题本
            eq.accuracy = round(eq.correct_count / eq.review_count * 100, 1) if eq.review_count else None
        else:
            # 评测答对 → 从错题本排除（与"连续答对已掌握移出"口径一致）
            eqs = db.query(ErrorQuestion).filter(
                ErrorQuestion.source_practice_question_id == pq.id,
                ErrorQuestion.user_id == uid,
                ErrorQuestion.deleted == False,  # noqa: E712
                ErrorQuestion.status == "active",
            ).all()
            for eq in eqs:
                eq.status = "mastered"
                eq.correct_streak = max(eq.correct_streak or 0, 1)


def _normalize_answer(s: str) -> str:
    """答案归一化：去空白、全角转半角、统一分隔符，提升判分宽容度"""
    if not s:
        return ""
    s = s.replace("，", ",").replace("；", ";").replace("．", ".").replace("。", ".")
    s = "".join(s.split()).lower()
    s = s.replace("（", "(").replace("）", ")")
    # 去尾部量词短语："12个" / "12个水果" / "12元" → "12"（量词前必须是数字/空，不剥"苹果"这类物品名词首）
    import re
    for _ in range(2):
        m = re.search(r"([\u4e00-\u9fa5]{0,6})([个只本支颗朵块条张匹头串双把盒袋包排群辆架棵根枝片页元角分米厘米名位岁层间艘列节道件副双沓叠堆筐篮箱株])([\u4e00-\u9fa5]{0,4})$", s)
        if m and m.group(1) == "":
            s = s[: m.start()]
        else:
            break
    # 判断题符号归一：√/对/t/yes → 1；×/错/f/no → 0
    mapping = {"√": "1", "对": "1", "正确": "1", "t": "1", "true": "1", "yes": "1",
               "×": "0", "x": "0", "错": "0", "错误": "0", "f": "0", "false": "0", "no": "0"}
    return mapping.get(s, s)


def _check_decompose(q_answer: str, u_answer: str) -> bool:
    """数的分解题判分：用户答案里任意两个数相加等于标准答案中的 N 即算对。
    接受形式：'3和4'、'3,4'、'3+4'、'7=3+4'、'3 4' 等。
    """
    import re
    if not u_answer:
        return False
    # 从标准答案提取 N（如 '7=?+?' → 7）
    m = re.search(r"(\d+)", q_answer or "")
    if not m:
        return False
    target = int(m.group(1))
    # 从用户答案提取所有数字
    nums = [int(x) for x in re.findall(r"\d+", u_answer)]
    if not nums:
        return False
    # 任意两个不同数字和为 target；也接受用户直接写 target（视为理解题意）
    if target in nums:
        return True
    for i, a in enumerate(nums):
        for b in nums[i + 1:]:
            if a + b == target:
                return True
    # 单个数字也可能构成分解（如 target=7 时用户答 '7'）上面已覆盖
    return False


def _extract_unit(s: str) -> str:
    """从标准/用户答案中提取单位词：优先括号内（本/个…），其次数字后紧跟的单位词。
    无单位返回空串。如 '8 + 7 = 15（本）' → '本'；'15个水果' → '个水果'（只取 1~4 个汉字）。
    """
    import re
    if not s:
        return ""
    m = re.search(r"[（(]([\u4e00-\u9fa5]{1,4})[)）]", s)
    if m:
        return m.group(1)
    m = re.search(r"\d+\s*([\u4e00-\u9fa5]{1,4})\s*$", s)
    if m:
        return m.group(1)
    return ""


def _grade_fill_answer(q_answer: str, u_answer: str, ignore_unit: bool = False) -> float:
    """填空/解答题三态判分（教学逻辑：算式对了只缺单位 → 打钩减半，不判 0 分）：
      - 1.0  全对：数值结果对，且单位齐全（标准答案无单位时数值对即满分）
      - 0.5  半对：数值/算式对，但标准答案带单位而孩子缺单位或单位写错
      - 0.0  错：数值结果不对（或空白）
    数值判定采用“末位数字 = 标准答案结果”的宽容策略，列式过程不拘泥。
    ignore_unit=True（低年级数学）：数值对即满分，不比较单位（一年级不会打字记单位）。
    """
    import re
    if not q_answer or not u_answer:
        return 0.0
    qn = re.findall(r"\d+", _normalize_answer(q_answer))
    un = re.findall(r"\d+", _normalize_answer(u_answer))
    if not qn or not un:
        # 判断题/无数字答案：退回严格比较（符号归一由 _normalize_answer 处理）
        return 1.0 if _normalize_answer(u_answer) == _normalize_answer(q_answer) else 0.0
    if qn[-1] != un[-1]:
        return 0.0
    if ignore_unit:
        return 1.0  # 低年级：数值对即满分，忽略单位
    q_unit = _extract_unit(q_answer)
    u_unit = _extract_unit(u_answer)
    if q_unit and u_unit != q_unit:
        return 0.5
    return 1.0


class AssessmentStartRequest(BaseModel):
    subject_id: int
    grade: Optional[int] = None
    count: Optional[int] = None
    paper_type: Optional[str] = None  # standard/challenge/explore（默认 standard）


class AssessmentSubmitRequest(BaseModel):
    grade: Optional[int] = None  # 评测时选择的年级（start 时同值）
    answers: list = []  # [{question_id, user_answer}]
    duration: Optional[int] = 0


def _to_question_dict(q: PracticeQuestion):
    """题目 → 前端渲染数据（含答案用于即时判分反馈）"""
    options = []
    answer = (q.answer or "").strip()
    if q.question_type == "choice" and (q.option_a or q.option_b):
        for opt in (q.option_a, q.option_b, q.option_c, q.option_d):
            if opt:
                options.append(opt)
        # 选项题答案给字母（A/B/C/D），前端也按文本显示答案选项
        letters = ["A", "B", "C", "D"]
        ans_upper = answer.upper()
        if ans_upper in letters:
            answer = letters[letters.index(ans_upper)]
    # 配图场景：优先题目自带 visual（经合法性校验）→ 规则识别
    scene = _resolve_scene(q)
    # 数的分解题答案是一组集合，前端展示友好文本
    if (q.question_type or "") == "fill" and (q.knowledge_point or "") == "数的分解":
        answer = "任意两个数相加等于该数即可"
    return {
        "id": q.id,
        "question_id": q.id,
        "stem": q.parsed_question or q.original_text or "",
        "options": options,
        "answer": answer,
        "type": q.question_type or "fill",
        "knowledge": q.knowledge_point or "其他",
        "grade": q.grade or 0,
        "difficulty": q.difficulty or 3,
        "scene": scene,
    }


# ==================== 场景识别（B：现有题自动配图） ====================
# 物品词 → emoji 映射（低年级数学常见物品）
_ITEM_EMOJI = {
    "苹果": "🍎", "梨": "🍐", "桃": "🍑", "草莓": "🍓", "香蕉": "🍌", "葡萄": "🍇", "西瓜": "🍉",
    "饼干": "🍪", "蛋糕": "🍰", "面包": "🍞", "糖果": "🍬", "糖": "🍬", "棒棒糖": "🍭", "冰激凌": "🍦", "冰淇淋": "🍦",
    "鸡蛋": "🥚", "牛奶": "🥛", "胡萝卜": "🥕", "白菜": "🥬", "花": "🌸", "气球": "🎈",
    "汽车": "🚗", "小汽车": "🚗", "自行车": "🚲", "飞机": "✈️", "船": "⛵",
    "书": "📚", "笔": "✏️", "铅笔": "✏️", "尺子": "📏",
    "球": "⚽", "足球": "⚽", "篮球": "🏀", "皮球": "⚽", "积木": "🧱", "玩具": "🧸",
    "帽子": "🧢", "袜子": "🧦", "鞋": "👟", "裤子": "👖", "衣服": "👕",
    "小鸟": "🐦", "小鸡": "🐤", "小鸭": "🦆", "兔子": "🐰", "小兔": "🐰", "小猫": "🐱", "小狗": "🐶",
    "猴子": "🐵", "小猴": "🐵", "大象": "🐘", "老虎": "🐯", "熊猫": "🐼", "金鱼": "🐟", "鱼": "🐟",
    "星星": "⭐", "月亮": "🌙", "太阳": "☀️", "树": "🌳", "小树": "🌳", "花盆": "🪴",
    "人": "🧑", "小朋友": "🧒", "学生": "🧑🎓", "同学": "🧑🎓", "纸鹤": "🕊️", "千纸鹤": "🕊️",
    "圆": "🔴", "三角形": "🔺", "正方形": "🟥", "长方形": "🟧", "正方体": "🧊", "立方体": "🧊", "长方体": "🧱", "球体": "⚪",
}

# 几何图形：数量无关，用 SVG 更好——前端 scene 类型 shape 直接画
_SHAPE_WORDS = ["三角形", "正方形", "长方形", "圆", "正方体", "长方体", "圆柱", "球", "五角星", "梯形", "平行四边形"]


def _extract_number(text: str) -> int | None:
    """提取文本中的第一个数字（含中文数字 一二三四五六七八九十）"""
    cn = {"一": 1, "二": 2, "两": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}
    import re
    m = re.search(r"(\d+)", text)
    if m:
        return int(m.group(1))
    for w, n in cn.items():
        if w in text:
            return n
    return None


def _extract_numbers(text: str) -> list[int]:
    """提取文本中出现的所有数字（阿拉伯 + 中文一~十），按出现顺序返回。
    忽略序数（"第一/第二天"）与班级号（"三(1)班"）等非数量数字。"""
    import re
    # 剔除班级号："三(1)班/三（1）班/3年级1班" 等
    text = re.sub(r"[一二两三四五六七八九十\d]+[年级]?\s*[（(]\s*\d+\s*[)）]\s*班", "", text)
    text = re.sub(r"[一二两三四五六七八九十\d]+[年级]?\s*\d+\s*班", "", text)
    # 剔除序数："第一/第二天/第1次" 等，避免把序数当数量
    text = re.sub(r"第[一二两三四五六七八九十\d]+[天次轮组个本道位名排]?", "", text)
    found: list[tuple[int, int]] = []
    for m in re.finditer(r"\d+", text):
        found.append((m.start(), int(m.group())))
    cn = {"一": 1, "两": 2, "二": 2, "三": 3, "四": 4, "五": 5, "六": 6, "七": 7, "八": 8, "九": 9, "十": 10}
    for w, n in cn.items():
        idx = text.find(w)
        while idx >= 0:
            # 中文数字 + 量词（"一本书/一只鸟/一根棒"）中的"一"是泛指，不算数量
            if w == "一":
                after = text[idx + 1: idx + 2]
                if after and (after in "个只本条根支棵朵颗块把袋盒包群排束辆架张匹头串双副件层圈层" or after in "些边旁半共起样直会定"):
                    idx = text.find(w, idx + 1)
                    continue
            found.append((idx, n))
            idx = text.find(w, idx + 1)
    found.sort()
    return [n for _, n in found]


# 环境词（容器/地点）：出现时不作为主体物品配图，避免"树上有10只小鸟"画出树而不是鸟
_ENV_WORDS = ["树", "小树", "盒子", "袋子", "盘子", "篮子", "筐", "书架", "花盆", "桌子", "地上", "枝头"]
# 人物泛称：出现在"两人/小明有3个小朋友"语境，不是可配图的物品
_PERSON_WORDS = ["人", "小朋友", "学生", "同学", "孩子", "儿童"]
# 人物/动物角色词：题干主语（小明/小红/小猴/小兔），不是被数的物品（桃子/苹果才是）
_ROLE_WORDS = ["小明", "小红", "小刚", "小华", "小丽", "小军", "小强", "小英", "小方", "小文",
               "小猴", "小兔", "小猫", "小狗", "小鸭", "小鸡", "小熊猫", "小松鼠", "小刺猬",
               "小熊", "小鹿", "小马", "小猪", "小羊", "老师", "妈妈", "爸爸", "弟弟", "妹妹",
               "哥哥", "姐姐", "爷爷", "奶奶", "阿姨", "叔叔"]


def _find_item_emoji(text: str) -> list[tuple[str, str]]:
    """找出题干中出现的所有物品词 → (名称, emoji)，按出现次数降序、出现位置升序。
    环境词（容器/地点）排最后；同物品多次出现优先（主体物品）。"""
    hits = []
    for w, e in _ITEM_EMOJI.items():
        if w in _PERSON_WORDS or w in _ROLE_WORDS:
            continue  # 人物/角色词不作为配图物品（"小猴摘14个桃子"画桃子而不是小猴）
        idx = text.find(w)
        cnt = 0
        while idx >= 0:
            cnt += 1
            idx = text.find(w, idx + 1)
        if cnt:
            hits.append((text.find(w), w, e, cnt, 1 if w in _ENV_WORDS else 0))
    hits.sort(key=lambda t: (-t[3], t[4], t[0]))  # 次数多 → 非环境词 → 先出现
    return [(w, e) for _, w, e, _, _ in hits]


def detect_scene(q) -> dict | None:
    """从题干自动识别可配图场景，返回结构化描述（无则 None）"""
    stem = (q.parsed_question or q.original_text or "").strip()
    if not stem or q.subject_id != 1:  # 目前只给数学配图
        return None
    # 题型过滤：纯计算/判断题不配图（图例无助于考察读题建模能力）
    qt = q.question_type or ""
    if qt in ("calc", "judge"):
        return None
    # 年级阶梯：三年级及以上只保留几何图形 shape（文字情景为主，图例降频）
    grade = getattr(q, "grade", None) or 0
    grade_only_shape = grade >= 3
    # 几何图形题：只有"认识/辨认/下面哪个是"这类才算 shape 场景（"画X个圆"不是认图形）
    # 周长/面积/边长等测量计算题不配图（"正方形边长6厘米周长"不是认图形）
    if any(w in stem for w in ("周长", "面积", "边长", "厘米", "毫米", "平方", "体积", "容积")):
        pass
    else:
        shape_trigger = ["认识", "哪个是", "下面", "下列", "图形", "数一数", "每种", "有几个", "是（"]
        for w in _SHAPE_WORDS:
            if w in stem and any(t in stem for t in shape_trigger):
                return {"type": "shape", "shape": w, "count": 1}
    # 找物品词
    item = None
    emoji = None
    for w, e in _ITEM_EMOJI.items():
        if w in _PERSON_WORDS:
            continue  # 人物泛称不作为配图物品
        if w in stem:
            item = w
            emoji = e
            break
    if not item:
        return None
    # 场景1：X个(物品)，每(个/盒/袋/盘)Y → group 场景（"3个袋子，每袋5块饼干" / "每个袋子装5块，有3个"）
    import re
    m = re.search(r"每\s*([个盒袋包盘筐束排串把捆群组支条块棵朵张])\s*(?:[子里中])?\s*\w{0,4}?\s*([一二两三四五六七八九十\d]+)", stem)
    if m and not grade_only_shape:
        per = int(m.group(2)) if m.group(2).isdigit() else _extract_number(m.group(2)) or 1
        groups = None
        # 找组数：题干里"每"之前最靠近它的数量词（"有3袋饼干，每袋5块" → 3；"每束花有5朵，4束花" → 4）
        head = stem[: m.start()]
        for cand in _extract_numbers(head)[::-1]:
            groups = cand
            break
        if not groups:
            nums = _extract_numbers(stem)
            # 取不是 per 的那一个（通常是第一个）
            for cand in nums:
                if cand != per:
                    groups = cand
                    break
        if not groups:
            groups = 1
        if groups * per <= 24:  # 画得下才配图（超过24个emoji太拥挤）
            return {
                "type": "group",
                "emoji": emoji,
                "groups": groups,
                "per_group": per,
                "label": item,
            }
        # 乘积太大：退化为 count 示意
        return {"type": "count", "emoji": emoji, "count": min(groups, 8), "label": item}
    # 场景1.5：两数加减题 → count-split（图即题：两堆数量都画出，修复"只画第一个数字"问题）
    # 例如"图书角有9本故事书，又新买了7本…一共有多少" → 左9 右7 = ？
    # 触发词保证只命中"加减关系"，不会把"第1天/三(1)班"等序数误当数量
    nums = _extract_numbers(stem)
    if len(nums) >= 2 and emoji and not grade_only_shape:
        # 金额/长度/重量等计量单位不画两堆实物图（"6元+4元/长3米宽1米"不是"数实物"）
        if re.search(r"\d+[元角分]|长\d+米|宽\d+米|周长|厘米|毫米|千米|公斤|千克|克|吨|升|毫升", stem):
            pass
        elif re.search(r"(每[个盒袋包盘筐条支只][^，。]*?(装|分|放|捆|摆|串))|(平均|分成|分给|装了|可以装|可以分)", stem):
            pass  # 除法语义不配两数图（"每2个装一袋/分成3组/平均分"）：画面会误导
        else:
            add_words = ["一共", "总共", "合起来", "共有", "加起来", "现在有", "再买", "新买", "又买",
                         "买来", "运来", "送来", "捡到", "增加", "又来", "又放", "又种", "又养"]
            sub_words = ["还剩", "剩下", "减去", "去掉", "拿走", "吃掉", "飞走", "卖出", "借走",
                         "用了", "花了", "吃了", "减少", "用去", "又走", "又飞", "又借",
                         "给了", "送给", "送出", "分给", "拿走"]
            a, b = nums[0], nums[1]
            # 含"（　）"未知数（"左边有6只，右边有（　）只，一共有14只"）不是确定的两数结构，不配 count-split
            # 两步混合运算（"给了…又添上/先吃…又送"）不是简单两数加减，不配 count-split
            is_add = any(w in stem for w in add_words)
            is_sub = any(w in stem for w in sub_words)
            multi_step = re.search(r"(给了|送给|送出|分了|吃了|用了|飞走).{0,12}?(又|再).{0,8}?(添|加|买|放|来|送|吃|飞)", stem) or \
                         re.search(r"先.{0,12}?(又|再)", stem) or \
                         (is_add and is_sub)
            if "（" in stem and "）" in stem:
                pass
            elif multi_step:
                pass
            else:
                total = a + b if is_add else a
                if is_add and total <= 24:
                    items = _find_item_emoji(stem)
                    # main = 第一个非环境物品（角色已排除："小猴摘14个桃子"→桃子；"苹果…梨"→苹果）
                    non_env = [x for x in items if x[0] not in _ENV_WORDS]
                    main = non_env[0] if non_env else (item, emoji)
                    second = main
                    for w, e in items[1:]:
                        if w not in _ENV_WORDS:
                            second = (w, e)
                            break
                    return {
                        "type": "count-split",
                        "left_emoji": main[1], "left_count": a,
                        "right_emoji": second[1], "right_count": b,
                        "operator": "+", "unknown": "sum",
                        "label": main[0], "max_count": total,
                    }
                if is_sub and b <= a <= 24:
                    items = _find_item_emoji(stem)
                    non_env = [x for x in items if x[0] not in _ENV_WORDS]
                    main = non_env[0] if non_env else (item, emoji)
                    second = main
                    for w, e in items[1:]:
                        if w not in _ENV_WORDS:
                            second = (w, e)
                            break
                    return {
                        "type": "count-split",
                        "left_emoji": main[1], "left_count": a,
                        "right_emoji": second[1], "right_count": b,
                        "operator": "-", "unknown": "remainder",
                        "label": main[0], "max_count": a,
                    }
    # 场景2：单纯数一数（"有X个苹果"）→ count 场景（>12 截断为示意）
    # 三年级及以上不配 count 单数示意图（图例降频，由组卷占比再控制总量）
    if grade_only_shape:
        return None
    # 两步混合运算（"给了2颗又添上5颗/飞走5只又飞来2只"）不配单数示意图
    if re.search(r"(给了|送给|送出|分了|吃了|用了|飞走|借出|搬走|卖出|拿走).{0,12}?(又|再).{0,8}?(添|加|买|放|来|送|吃|飞|还|搬)", stem):
        return None
    # 金额/长度/重量等计量题、除法语义题、含未知数填空的题不配图（避免误导）
    if re.search(r"\d+[元角分]|长\d+米|宽\d+米|周长|厘米|毫米|千米|公斤|千克|克|吨|升|毫升|面积|平方", stem):
        return None
    if re.search(r"(平均|分成|分给|可以装|可以分|每人|每[个盒袋包盘筐条支只][^，。]*?(装|分|放|捆|摆|串))", stem):
        return None
    if "（" in stem and "）" in stem:
        return None
    num = _extract_number(stem)
    if num:
        return {"type": "count", "emoji": emoji, "count": min(num, 12), "label": item}
    return None


def _validate_scene(scene, q) -> dict | None:
    """校验 LLM 自带 visual 是否合法可展示；非法返回 None（回退规则识别或无图）。
    治理目标：带单位测量题 / 除法 / 乘法结构 / 未知数填空 / 数字对不上 一律不画图，
    避免"3根小棒×15厘米"被画成"3个🔺+1个🔺"这类误导图。
    """
    import re
    if not isinstance(scene, dict):
        return None
    t = scene.get("type")
    if t not in ("count", "count-split", "group", "shape"):
        return None
    stem = (q.parsed_question or q.original_text or "").strip()
    qt = q.question_type or ""
    grade = getattr(q, "grade", None) or 0
    # 纯计算/判断题不配图
    if qt in ("calc", "judge"):
        return None
    # 三年级及以上：仅几何图形 shape 配图（文字情景为主，图例会削弱读题能力考察）
    if grade >= 3 and t != "shape":
        return None
    # 计量单位题不画实物堆（"6元+4元/每根15厘米/长3米" 数字是测量值不是实物数量）
    if re.search(r"\d+[元角分]|长\d+米|宽\d+米|周长|厘米|毫米|千米|公斤|千克|克|吨|升|毫升|面积|平方|分钟|小时|秒钟|每秒|每天|每小时", stem):
        return None
    if t == "shape":
        if not any(w in stem for w in _SHAPE_WORDS):
            return None
        return scene
    # 除法语义不配两数图
    if re.search(r"(平均|分成|分给|可以装|可以分|每人|每[个盒袋包盘筐条支只][^，。]*?(装|分|放|捆|摆|串))", stem) and t in ("count-split", "count"):
        return None
    # 含"（　）"未知数填空（"右边有（　）只，一共有14只"）不配确定两数图
    if "（" in stem and "）" in stem:
        return None
    nums = _extract_numbers(stem)
    if t == "count-split":
        add_words = ["一共", "总共", "合起来", "共有", "加起来", "现在有", "再买", "新买", "又买",
                     "买来", "运来", "送来", "捡到", "增加", "又来", "又放", "又种", "又养"]
        sub_words = ["还剩", "剩下", "减去", "去掉", "拿走", "吃掉", "飞走", "卖出", "借走",
                     "用了", "花了", "吃了", "减少", "用去", "又走", "又飞", "又借",
                     "给了", "送给", "送出", "分给", "拿走"]
        if not (any(w in stem for w in add_words) or any(w in stem for w in sub_words)):
            return None
        # 乘法结构（"每X"）不是两数加减图
        if re.search(r"每[个盒袋包盘筐束排串把捆群组支条块棵朵张]", stem):
            return None
        lc, rc = scene.get("left_count"), scene.get("right_count")
        if not isinstance(lc, int) or not isinstance(rc, int) or lc < 1 or rc < 1:
            return None
        # 数字一致性：左右数必须都是题干出现的数量
        if nums and lc not in nums:
            return None
        if nums and rc not in nums:
            return None
        if (scene.get("operator") == "+" and lc + rc > 24) or lc > 24 or rc > 24:
            return None
        return scene
    if t == "count":
        cnt = scene.get("count")
        if not isinstance(cnt, int) or cnt < 1 or cnt > 24:
            return None
        if nums and cnt not in nums and not (len(nums) >= 2 and cnt == nums[0] + nums[1]):
            return None
        return scene
    if t == "group":
        g, p = scene.get("groups"), scene.get("per_group")
        if not isinstance(g, int) or not isinstance(p, int) or g < 1 or p < 1 or g * p > 24:
            return None
        if nums and g not in nums:
            return None
        if nums and p not in nums:
            return None
        return scene
    return None


def _resolve_scene(q) -> dict | None:
    """题目最终配图：自带 visual（经合法性校验）→ 规则识别。统一入口供展示与组卷占比使用。"""
    scene = None
    if getattr(q, "visual", None):
        try:
            scene = json.loads(q.visual)
        except Exception:
            scene = None
        scene = _validate_scene(scene, q)
    if not scene:
        scene = detect_scene(q)
    return scene

@router.get("/history")
def assessment_history(
    subject_id: Optional[int] = None,
    kid_id: Optional[int] = Depends(get_current_kid_id),
    db: Session = Depends(get_db),
):
    """评测记录列表（按当前选中的小孩隔离；家长未选孩子时查看全部）
    - subject_id 可选：按学科过滤（评测页跟随右上角空间，避免数学页混入英语记录）
    - 返回 done + in_progress（未完成优先展示），quit 不显示
    """
    query = db.query(AssessmentRecord).filter(AssessmentRecord.status.in_(["done", "in_progress"]))
    if subject_id:
        query = query.filter(AssessmentRecord.subject_id == subject_id)
    query = filter_by_kid(query, AssessmentRecord.user_id, kid_id)
    records = query.order_by(
        # 未完成排前面（可继续/重新评测），已完成按时间倒序
        case((AssessmentRecord.status == "in_progress", 0), else_=1),
        desc(AssessmentRecord.created_at),
    ).limit(50).all()
    result = []
    for r in records:
        subject = db.query(Subject).get(r.subject_id)
        result.append({
            "id": r.id,
            "subject_id": r.subject_id,
            "subject_name": subject.name if subject else "学科",
            "grade": r.grade,
            "total": r.total,
            "score": r.score,
            "level": r.level,
            "status": r.status,
            "specialty": r.specialty,
            "specialty_name": _specialty_name(r.subject_id, r.specialty),
            "created_at": r.created_at.isoformat() if r.created_at else None,
        })
    return result


@router.post("/{record_id}/quit")
def assessment_quit(record_id: int, kid_id: int = Depends(get_required_kid_id), db: Session = Depends(get_db)):
    """放弃/退出当前评测：进行中的评测集置 quit（历史里不再显示为未完成）
    孩子身份从 X-Kid-Id 头解析（必须先选孩子）。"""
    record = db.query(AssessmentRecord).get(record_id)
    if not record:
        raise HTTPException(status_code=404, detail="评测集不存在")
    if record.user_id != kid_id:
        raise HTTPException(status_code=404, detail="评测集不存在")
    if record.status == "in_progress":
        record.status = "quit"
        db.commit()
    return {"ok": True}


@router.get("/{record_id}")
def assessment_detail(record_id: int, kid_id: Optional[int] = Depends(get_current_kid_id), db: Session = Depends(get_db)):
    """评测详情（归属校验：未选孩子=家长视角可看全部）"""
    r = db.query(AssessmentRecord).get(record_id)
    if not r:
        raise HTTPException(status_code=404, detail="评测记录不存在")
    if kid_id is not None and r.user_id != kid_id:
        raise HTTPException(status_code=404, detail="评测记录不存在")
    subject = db.query(Subject).get(r.subject_id)
    knowledge = json.loads(r.knowledge) if r.knowledge else []
    detail = json.loads(r.detail) if r.detail else []
    tier_stats = _build_tier_stats(detail, knowledge)
    mastery = _mastery_level(tier_stats)
    return {
        "id": r.id,
        "subject_id": r.subject_id,
        "subject_name": subject.name if subject else "学科",
        "grade": r.grade,
        "total": r.total,
        "score": r.score,
        "level": r.level,
        "specialty": r.specialty,
        "specialty_name": _specialty_name(r.subject_id, r.specialty),
        "knowledge": knowledge,
        "detail": detail,
        "tier_stats": tier_stats,
        "mastery": mastery,
        "created_at": r.created_at.isoformat() if r.created_at else None,
    }


def _compose_paper(db: Session, kid_id: int, req, specialty: Optional[dict] = None, mode: str = "assessment") -> dict:
    """组卷核心（综合/专项评测共用）：按学科+年级（+专项）抽题组卷。
    题库不足时自动调 AI 生成新题入库补齐，首次稍慢（约10-30秒），之后秒开。
    孩子身份从 X-Kid-Id 头解析（必须先选孩子）。
    specialty：专项配置 dict（None=综合全学科均衡）；专项时题目池与补题知识点限定在专项池内。
    mode："assessment"=建评测记录并废弃旧进行中记录；"practice"=练习模式（不建记录、不动旧记录）。
    """
    uid = kid_id
    count = req.count or ASSESS_QUESTION_COUNT

    # 评测规则配置（运营后台可维护）：组卷/排重/坏题校验参数，未配置用内置默认
    from app.services.assess_rules_service import load_assess_rules
    _rules = load_assess_rules()

    # 低年级数学：先用模板引擎保证图示算式题足量（确定性生成，秒级，不依赖 LLM）
    if req.subject_id == 1 and req.grade in (1, 2):
        _ensure_pictorial_questions(db, req.subject_id, req.grade, uid, want=max(count // 2, 6))

    def _load_questions():
        q = db.query(PracticeQuestion).filter(
            PracticeQuestion.subject_id == req.subject_id,
        )
        # 学科题型白名单：应用题（application）是数学题型，
        # 英语/语文若混入"英语化的数学应用题"会显得像数学卷（历史教训：qid 72 'I have three red apples'）
        allow = _SUBJECT_ALLOW_TYPES.get(req.subject_id)
        if allow is not None:
            q = q.filter(PracticeQuestion.question_type.in_(allow))
        if req.grade:
            q = q.filter(PracticeQuestion.grade == req.grade).all()
        else:
            q = q.all()
        # 专项评测：题目池收窄到专项知识点池（子串匹配）
        if specialty:
            q = [x for x in q if _kp_in_pool(x.knowledge_point, specialty["pool"])]
        return q

    questions = _load_questions()
    # 评测排重：排除最近 N 天内已完成评测用过的题（同一孩子同学科同年级；N 由运营后台配置，默认 7）
    excluded_ids, recent_stems = _recent_done_question_ids(
        db, uid, req.subject_id, req.grade or 0, days=_rules.get("dedup_days", RECENT_EXCLUDE_DAYS))
    # 出题依据之一是孩子的错题本：错题知识点优先出现（但不是只出错题，知识点+评测要求才是主线）
    weak_kps = set()
    try:
        from app.models import ErrorQuestion
        weak_kps = {k[0] for k in db.query(ErrorQuestion.knowledge_point).filter(
            ErrorQuestion.user_id == uid,
            ErrorQuestion.subject_id == req.subject_id,
            ErrorQuestion.status != "mastered",
            ErrorQuestion.knowledge_point.isnot(None),
        ).all() if k[0]}
    except Exception:
        weak_kps = set()
    # 未入库但可用的题量（去重后）
    usable = set()
    for qq in questions:
        stem = (qq.parsed_question or qq.original_text or "").strip()
        usable.add(stem)
    shortage = count - len(usable)
    generated = 0
    generated_msg = ""
    # 分档缺口检测（不只看总量）：按卷型各档需要量 vs 各档可用题数，不足的档按对应难度补题。
    # 否则拔高/拓展卷 hard 档（diff4-5）库存不足会被迫借简单题，分级差异被稀释、卷子观感雷同。
    if shortage > 0:
        _paper = req.paper_type or "standard"
        _ratios = {}
        for _tier in ("basic", "mid", "hard"):
            _ratios[_tier] = _rules.get(f"ratio_{_paper}_{_tier}",
                                         PAPER_RATIOS.get(_paper, PAPER_RATIOS["standard"])[_tier])
        tier_needs = {}
        for _tier, _ratio in _ratios.items():
            tier_needs[_tier] = int(round(count * _ratio))
        _filled = sum(tier_needs.values())
        if _filled < count:
            tier_needs["basic"] += count - _filled
        elif _filled > count:
            tier_needs["hard"] = max(0, tier_needs["hard"] - (_filled - count))
            _filled = sum(tier_needs.values())
            if _filled > count:
                tier_needs["basic"] = max(0, tier_needs["basic"] - (_filled - count))
        tier_avail = {"basic": 0, "mid": 0, "hard": 0}
        for qq in questions:
            if qq.id in excluded_ids:
                continue  # 已被排重的题（近期展示过）不算可用 → 缺口才准确，避免组卷兜底抽已考题
            tier_avail[_difficulty_tier(qq.difficulty)] += 1
        tier_gap = {}
        for _tier in ("basic", "mid", "hard"):
            _gap = tier_needs[_tier] - tier_avail[_tier]
            if _gap > 0:
                tier_gap[_tier] = _gap
        # 按档难度补题：基础/中等/拔高难度由运营后台配置（1-2年级 _auto_refill 内自动封顶4）
        tier_diff = {
            "basic": _rules.get("gap_diff_basic", 2),
            "mid": _rules.get("gap_diff_mid", 3),
            "hard": _rules.get("gap_diff_hard", 5),
        }
        for _tier, _gap in tier_gap.items():
            generated += _auto_refill(db, req.subject_id, req.grade or 1, _gap + _rules.get("refill_margin", 2),
                                      uid, difficulty=tier_diff[_tier], avoid_stems=recent_stems,
                                      knowledge_points=(specialty["pool"][:6] if specialty else None))
        if generated:
            generated_msg = f"题库按难度补题，已自动生成 {generated} 道新题"
            questions = _load_questions()
        else:
            generated_msg = "题库不足，自动生成失败，本次题目较少"

    # 举一反三：评测卷不以库存直出——库存只作参考，无论库存是否充足，
    # 都按卷型目标难度生成少量同知识点新变式，保证每次卷子都有新面孔、能真实反映水平。
    # 分档补题已生成过则不再重复生成；AI 生成题都会过 sanitize 自检（单位/数量/配图一致性）。
    VARIANT_COUNT = _rules.get("variant_count", 2)
    extra = max(0, VARIANT_COUNT - generated)
    if extra > 0:
        _variant_diff = _rules.get("variant_diff_" + (req.paper_type or "standard"),
                                   {"standard": 3, "challenge": 4, "explore": 5}.get(req.paper_type or "standard", 3))
        extra_gen = _auto_refill(db, req.subject_id, req.grade or 1, extra, uid, difficulty=_variant_diff, avoid_stems=recent_stems,
                                 knowledge_points=(specialty["pool"][:6] if specialty else None))
        if extra_gen:
            generated += extra_gen
            questions = _load_questions()
    if generated:
        generated_msg = f"本次已按知识点举一反三，自动生成 {generated} 道新题"

    if not questions:
        return {"questions": [], "record_id": None, "message": "该年级题库暂无题目，正在尝试生成，请稍后重试"}

    # 2. 分层组卷：按卷型难度占比抽题（标准=检验课内 / 拔高=本年级深度变式 / 拓展=摸上限可选轻探）
    # 每档内保持原优先级：图示算式题 → 情景题 → 近期未考过的题 → 题型优先级 → 随机
    paper_type = req.paper_type or "standard"
    if paper_type not in PAPER_RATIOS:
        paper_type = "standard"
    ratios = PAPER_RATIOS[paper_type]
    TYPE_ORDER = {"application": 1, "fill": 2, "choice": 3, "judge": 4, "calc": 5, "operation": 6, "sentence": 7, "reading": 8, "writing": 9}
    # 同一知识点最多抽 2 题（保证覆盖面）
    sampled = []
    seen_kp = {}
    seen_stems = set()
    # 情景题（scene 类型）优先：先排 scene，再按题型优先级，再随机打乱
    _scene_cache = {}

    def _scene_of(x):
        """题目最终配图（带缓存，避免组卷多次重复解析）"""
        if id(x) not in _scene_cache:
            _scene_cache[id(x)] = _resolve_scene(x)
        return _scene_cache[id(x)]

    def _is_pictorial(x):
        """图示算式题（visual 是 count-split，图即题，出卷最优先）"""
        s = _scene_of(x)
        return isinstance(s, dict) and s.get("type") == "count-split"

    def _has_scene(x):
        """任何配图（count-split/count/group/shape）——占比控制用，防题题有图"""
        return isinstance(_scene_of(x), dict)

    def _pool_key(x):
        # 低年级数学：图示算式题最优先 → scene 情景题 → 近期未考过的题 → 错题本知识点（出题依据之一是错题，但不是唯一）
        # → 按题型优先级 → 随机（近期已考过的题排最后，仅当新题量不足时兜底被抽到）
        return (
            0 if _is_pictorial(x) else 1,
            0 if (x.question_category or "") == "scene" else 1,
            0 if x.id not in excluded_ids else 1,
            0 if (x.knowledge_point or "") in weak_kps else 1,
            TYPE_ORDER.get(x.question_type or "", 99),
            random.random(),
        )
    # 先打乱输入再稳定排序：同优先级内完全随机 → 连续切换卷型时第一题/题序不雷同
    shuffled_in = random.sample(questions, len(questions))
    pool = sorted(shuffled_in, key=_pool_key)
    # 配图题占比限制：最多一半（低年级数学卷图文并茂，不全图也不全文字；比例由运营后台配置，默认 0.5）
    pictorial_total = sum(1 for x in pool if _has_scene(x))
    pictorial_budget = max(min(pictorial_total, int(count * _rules.get("pictorial_ratio", 0.5))), 0) if pictorial_total else 0
    pictorial_taken = 0
    # 按难度档分桶（桶内保持 pool 顺序：图题/情景/未考/题型）
    buckets = {"basic": [], "mid": [], "hard": []}
    for x in pool:
        buckets[_difficulty_tier(x.difficulty)].append(x)
    # 各档配额（round 取整；尾差进基础档保证总量；超出从拓展档扣减）
    quota = {tier: int(round(count * ratio)) for tier, ratio in ratios.items()}
    filled = sum(quota.values())
    if filled < count:
        quota["basic"] += count - filled
    elif filled > count:
        quota["hard"] = max(0, quota["hard"] - (filled - count))
        # 仍超出（拓展档被扣为0）时从基础档扣
        filled = sum(quota.values())
        if filled > count:
            quota["basic"] = max(0, quota["basic"] - (filled - count))

    def _is_bad_question(qq):
        """组卷时校验题库里的题是否为坏题——即使来自题库/存量/模板也过滤（用户明确要求）。
        AI 生成题入库前有 _sanitize_math_item 自检，但模板题/存量题/导入题可能绕过，这里在抽题时兜底：
        1. 题干为空 → 孩子无法作答
        2. 答案为空 → 无法判分
        3. 选择题无有效选项（<2 个）→ 无法作答
        4. '看图列式'题干无数量数字且无有效配图（count-split）→ 没图没数字，孩子无法作答
        """
        stem = (qq.parsed_question or qq.original_text or "").strip()
        if not stem:
            return True
        ans = (qq.answer or "").strip()
        if not ans:
            return True
        qtype = (qq.question_type or "").strip()
        if qtype == "choice":
            opts = [o for o in (qq.option_a, qq.option_b, qq.option_c, qq.option_d) if o and str(o).strip()]
            if len(opts) < _rules.get("min_choice_options", 2):
                return True
        if "看图列式" in stem and not re.search(r"\d", stem.replace("（　）", "").replace("()", "")) and not _is_pictorial(qq):
            return True
        return False

    def _take(qq):
        nonlocal pictorial_taken
        kp = qq.knowledge_point or "其他"
        if seen_kp.get(kp, 0) >= 2:
            return False
        # 坏题过滤（通用校验：题干/答案/选项/看图列式无数量无图）
        if _is_bad_question(qq):
            return False
        # 跳过题干重复的题（题库里有完全相同的 fill 题）
        stem = (qq.parsed_question or qq.original_text or "").strip()
        if stem and stem in seen_stems:
            return False
        # 近期卷子已展示过的题干不重复出（AI 变式可能生成同题干新 id，仅按 id 排重防不住）
        if stem and stem in recent_stems:
            return False
        if _has_scene(qq) and pictorial_taken >= pictorial_budget:
            return False
        sampled.append(qq)
        seen_stems.add(stem)
        seen_kp[kp] = seen_kp.get(kp, 0) + 1
        if _has_scene(qq):
            pictorial_taken += 1
        return True

    for tier in ("basic", "mid", "hard"):
        need = quota.get(tier, 0)
        if need <= 0:
            continue
        for qq in buckets[tier]:
            if need <= 0:
                break
            if _take(qq):
                need -= 1
    # 覆盖不够时放宽知识点限制补足（按整体 pool 顺序：优先补配额缺的档，其余按优先级）
    if len(sampled) < count:
        for qq in pool:
            if len(sampled) >= count:
                break
            if qq in sampled:
                continue
            # 兜底阶段也过滤坏题（题库/存量/模板的坏题同样不抽）
            if _is_bad_question(qq):
                continue
            stem = (qq.parsed_question or qq.original_text or "").strip()
            if stem and stem in seen_stems:
                continue
            # 兜底阶段也遵守近期题干排重（宁缺毋滥，避免切卷雷同）
            if stem and stem in recent_stems:
                continue
            # 补足阶段同样遵守图题占比（防止全图卷）
            if _has_scene(qq) and pictorial_taken >= pictorial_budget:
                continue
            sampled.append(qq)
            seen_stems.add(stem)
            if _has_scene(qq):
                pictorial_taken += 1

    # 3. 返回题目（含场景描述用于前端配图）
    # 卷内题序打乱：按难度分档抽完后 shuffle，保证每次卷子第一题/顺序都不一样（体验友好）
    random.shuffle(sampled)
    questions_data = []
    for qq in sampled:
        data = _to_question_dict(qq)
        data["question_id"] = qq.id
        questions_data.append(data)

    shortage = len(questions_data) < count

    # 4. 评测集管理：生成题目快照，建 in_progress 评测集记录
    # 同一孩子同学科同年级只保留一条进行中记录（旧的未完成自动废弃，历史里可重新评测）
    # 练习模式（mode="practice"）不建记录、不动旧记录（练习不打断进行中的评测）
    record = None
    if mode == "assessment":
        db.query(AssessmentRecord).filter(
            AssessmentRecord.user_id == uid,
            AssessmentRecord.subject_id == req.subject_id,
            AssessmentRecord.grade == (req.grade or (questions_data[0].get("grade", 0) if questions_data else 0)),
            AssessmentRecord.status == "in_progress",
        ).update({"status": "quit"}, synchronize_session=False)
        record = AssessmentRecord(
            user_id=uid,
            subject_id=req.subject_id,
            grade=req.grade or (questions_data[0].get("grade", 0) if questions_data else 0),
            total=len(questions_data),
            status="in_progress",
            questions=json.dumps(questions_data, ensure_ascii=False),
            specialty=specialty["key"] if specialty else None,
        )
        db.add(record)
        db.commit()
        db.refresh(record)

    return {
        "questions": questions_data,
        "record_id": record.id if record else None,
        "shortage": shortage,
        "generated": generated,
        "paper_type": paper_type,
        "specialty": specialty["key"] if specialty else None,
        "specialty_name": specialty["name"] if specialty else None,
        "message": (
            generated_msg if generated_msg else (
                f"当前{req.grade}年级题库题量较少，本次评测共出 {len(questions_data)} 道题"
                if shortage else ""
            )
        ),
    }


# ==================== 专项评测接口 ====================


class SpecialStartRequest(BaseModel):
    subject_id: int
    specialty: str  # 专项 key（见 SPECIALTIES）
    grade: Optional[int] = None
    count: Optional[int] = None
    paper_type: Optional[str] = None  # standard/challenge/explore（默认 standard）


@router.post("/start")
def assessment_start(req: AssessmentStartRequest, db: Session = Depends(get_db), kid_id: int = Depends(get_required_kid_id)):
    """开始评测（综合）：按学科+年级抽题组卷，全学科知识点均衡。
    题库不足时自动调 AI 生成新题入库补齐，首次稍慢（约10-30秒），之后秒开。"""
    return _compose_paper(db, kid_id, req, specialty=None)


@router.get("/special/list")
def special_list(subject_id: int, db: Session = Depends(get_db), kid_id: int = Depends(get_current_kid_id)):
    """专项评测：返回某学科的全部专项（含适用年级，前端按年级过滤显示）"""
    return {"items": SPECIALTIES.get(subject_id, [])}


@router.post("/special/start")
def special_assessment_start(req: SpecialStartRequest, db: Session = Depends(get_db), kid_id: int = Depends(get_required_kid_id)):
    """开始专项评测：专项内知识点均衡组卷（复用综合组卷引擎，题目池/补题知识点限定在专项池内）"""
    sp = _get_specialty(req.subject_id, req.specialty)
    if not sp:
        raise HTTPException(status_code=404, detail="专项不存在或不属于该学科")
    return _compose_paper(db, kid_id, req, specialty=sp)


@router.get("/special/history")
def special_history(subject_id: int, grade: int, specialty: str, db: Session = Depends(get_db), kid_id: int = Depends(get_current_kid_id)):
    """专项评测历史（按小孩）：某专项的历次完成记录（专项进步曲线数据源）"""
    recs = db.query(AssessmentRecord).filter(
        AssessmentRecord.user_id == kid_id,
        AssessmentRecord.subject_id == subject_id,
        AssessmentRecord.grade == grade,
        AssessmentRecord.specialty == specialty,
        AssessmentRecord.status == "done",
    ).order_by(AssessmentRecord.created_at).all()
    items = []
    for r in recs:
        items.append({
            "record_id": r.id,
            "date": r.created_at.strftime("%Y-%m-%d") if r.created_at else "",
            "score": int(r.score or 0),
            "total": int(r.total or 0),
            "rate": round((r.score or 0) / r.total, 2) if r.total else 0,
            "level": r.level or "",
        })
    return {"items": items}


@router.post("/special/practice/start")
def special_practice_start(req: SpecialStartRequest, db: Session = Depends(get_db), kid_id: int = Depends(get_required_kid_id)):
    """专项练习模式（非评测，不入评测历史）：专项组卷直接出题，基础+中等为主，
    答完只同步错题本、不给等级评级；不打断进行中的评测记录。"""
    sp = _get_specialty(req.subject_id, req.specialty)
    if not sp:
        raise HTTPException(status_code=404, detail="专项不存在或不属于该学科")
    res = _compose_paper(db, kid_id, req, specialty=sp, mode="practice")
    res["practice"] = True
    return res


@router.post("/special/practice/submit")
def special_practice_submit(req: AssessmentSubmitRequest, db: Session = Depends(get_db), kid_id: int = Depends(get_required_kid_id)):
    """专项练习提交：判分 + 错题同步（答错入错题本、答对排除），不建评测记录、不给等级评级。"""
    uid = kid_id
    if not req.answers:
        raise HTTPException(status_code=400, detail="没有作答内容，无法生成练习小结")
    detail, correct, total, knowledge, tier_stats, mastery = _grade_answers(db, req, uid)
    _sync_error_questions(db, uid, detail)
    db.commit()
    return {
        "score": correct,
        "total": total,
        "rate": round(correct / total, 2) if total else 0,
        "knowledge": knowledge,
        "detail": detail,
        "tier_stats": tier_stats,
        "mastery": mastery,
        "practice": True,
    }


def _grade_answers(db: Session, req, uid: int) -> tuple:
    """公共判分：从 answers 反查题目逐题判分（支持 0.5 半对/数的分解/低年级忽略单位）。
    返回 (detail, correct, total, knowledge, tier_stats, mastery)。
    评测 submit 与专项练习 submit 共用，保证判分口径一致。"""
    detail = []
    correct = 0
    knowledge_map = {}  # name -> {total, correct}

    for ans in req.answers:
        q = db.query(PracticeQuestion).get(ans.get("question_id"))
        if not q:
            continue
        q_answer = (q.answer or "").strip()
        u_answer = (ans.get("user_answer") or "").strip()
        if q.question_type == "choice" and (q.option_a or q.option_b):
            # 选项题：选项文本 → 字母（A/B/C/D）比对，容忍前端提交文本或字母
            letters = ["A", "B", "C", "D"]
            option_texts = [o for o in (q.option_a, q.option_b, q.option_c, q.option_d) if o]
            is_correct = False
            if u_answer in letters and u_answer.upper() == q_answer.upper():
                is_correct = True
            elif u_answer:
                u_idx = option_texts.index(u_answer) if u_answer in option_texts else -1
                if u_idx >= 0 and letters[u_idx].upper() == q_answer.upper():
                    is_correct = True
        else:
            # 填空/解答题：三态判分（1 全对 / 0.5 算式对缺单位 / 0 错）
            # 数的分解题（？+？=N）：任意两个数相加等于 N 都算对
            if q.question_type == "fill" and (q.knowledge_point or "") == "数的分解":
                is_correct = 1.0 if _check_decompose(q_answer, u_answer) else 0.0
            else:
                # 低年级（1-2）数学：数值对即满分，忽略单位（一年级不会打字记单位）
                _grade = req.grade or q.grade or 0
                _ignore_unit = (_grade <= 2) and (q.subject_id or 0) == 1
                is_correct = _grade_fill_answer(q_answer, u_answer, ignore_unit=_ignore_unit)
        correct += is_correct  # 支持 0.5 半对
        kn = q.knowledge_point or "其他"
        km = knowledge_map.setdefault(kn, {"total": 0, "correct": 0})
        km["total"] += 1
        km["correct"] += is_correct
        detail.append({
            "question_id": q.id,
            "stem": q.parsed_question or q.original_text or "",
            "answer": q_answer,
            "user_answer": u_answer,
            "correct": is_correct,
            "knowledge": kn,
            "difficulty": q.difficulty or 3,
        })
    # 实际判分条数（题目缺失的 answer 不计入 total，避免出现 0/1 这类空报告）
    total = len(detail)
    knowledge = [
        {"name": k, "total": v["total"], "correct": v["correct"]}
        for k, v in knowledge_map.items()
    ]
    # 难度维度统计 + 本年级内掌握等级定位（教育理念：不跨年级判级）
    tier_stats = _build_tier_stats(detail, knowledge)
    mastery = _mastery_level(tier_stats)
    return detail, correct, total, knowledge, tier_stats, mastery


@router.post("/{record_id}/submit")
def assessment_submit(record_id: int, req: AssessmentSubmitRequest, db: Session = Depends(get_db), kid_id: int = Depends(get_required_kid_id)):
    """提交评测并生成报告（record_id 为 0 时新建记录）
    孩子身份从 X-Kid-Id 头解析（必须先选孩子）。
    """
    uid = kid_id

    # 没有作答内容（一题未做）→ 不生成报告
    if not req.answers:
        raise HTTPException(status_code=400, detail="没有作答内容，无法生成评测报告")

    # 公共判分（与专项练习同口径）
    detail, correct, total, knowledge, tier_stats, mastery = _grade_answers(db, req, uid)
    rate = (correct / total) if total else 0
    level = _level_for(rate)

    record = None
    if record_id and record_id > 0:
        record = db.query(AssessmentRecord).get(record_id)
        if not record:
            raise HTTPException(status_code=404, detail="评测集不存在")
        if record.user_id != uid:
            raise HTTPException(status_code=404, detail="评测集不存在")
        if record.status == "quit":
            raise HTTPException(status_code=400, detail="该评测集已废弃，请重新开始评测")

    if record:
        record.score = correct
        record.total = total
        record.level = level
        record.knowledge = json.dumps(knowledge, ensure_ascii=False)
        record.detail = json.dumps(detail, ensure_ascii=False)
        record.status = "done"
    else:
        # 兼容：record_id=0（异常/旧流程未拿到评测集）→ 按第一道题反查学科/年级新建
        first_q = db.query(PracticeQuestion).get(req.answers[0]["question_id"]) if req.answers else None
        record = AssessmentRecord(
            user_id=uid,
            subject_id=first_q.subject_id if first_q else 0,
            grade=req.grade or (first_q.grade if first_q else 0),
            total=total,
            score=correct,
            level=level,
            knowledge=json.dumps(knowledge, ensure_ascii=False),
            detail=json.dumps(detail, ensure_ascii=False),
            status="done",
        )
        db.add(record)

    # 错题同步：答错自动进统一错题集，答对自动从错题集排除
    _sync_error_questions(db, uid, detail)

    db.commit()
    db.refresh(record)

    # 专项报告增强（阶段 B）：返回专项名供前端报告头部展示
    sp_name = None
    if record and record.specialty:
        _sp = _get_specialty(record.subject_id, record.specialty)
        sp_name = _sp["name"] if _sp else record.specialty

    return {
        "record_id": record.id,
        "score": correct,
        "total": total,
        "rate": round(rate, 2),
        "level": level,
        "knowledge": knowledge,
        "detail": detail,
        "tier_stats": tier_stats,
        "mastery": mastery,
        "specialty": record.specialty if record else None,
        "specialty_name": sp_name,
    }
