"""
练习集路由 - 管理练习集的创建、打印、复习等功能
"""
import json
from fastapi import APIRouter, Depends, HTTPException, Form, Body, Query, File, UploadFile
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import func
from typing import List, Optional, Union
from datetime import datetime
from pydantic import BaseModel

from app.database import get_db
from app.models import (
    PracticeSet, PracticeSetQuestion, Question, SimilarQuestion, Subject,
    WordReviewSession, PracticeQuestion, PracticeAttempt, ErrorQuestion,
)
from app.models.word import WordReview, WordReviewLog, Word
from app.models.reading import ReadingPassage, ReadingQuestion
from app.models.user import User
from app.services.pdf import generate_practice_set_pdf
from app.services.scoring import (
    compute_question_scores, normalize_score_mode, DEFAULT_SCORE_MODE,
)
from app.services.logger import logger_service
from app.services import practice_flow
from app.services import paper_ocr
from app.utils.auth import require_admin
from app.utils.kid_context import get_current_kid_id, get_required_kid_id, filter_by_kid

router = APIRouter(prefix="/api/practice-sets", tags=["练习集"])


# ============ Pydantic Schemas ============

class PracticeSetCreate(BaseModel):
    name: str
    question_ids: List[int]
    source_type: str = "question"  # question=来自错题, word=来自单词复习
    question_type: str = "original"  # original=原题, similar=相似题
    show_score: bool = True  # 卷面是否显示分值
    score_mode: str = "hundred"  # hundred=百分制100分 / default=题型默认分值


class GenerateFromQuestionsRequest(BaseModel):
    """根据条件生成练习集请求"""
    subject_id: int
    grade: Optional[int] = None
    count: int = 5
    show_score: bool = True  # 卷面是否显示分值
    score_mode: str = "hundred"  # hundred=百分制100分 / default=题型默认分值

    class Config:
        json_schema_extra = {
            "example": {
                "subject_id": 1,
                "grade": 1,
                "count": 5
            }
        }


class GenerateFromReadingRequest(BaseModel):
    """从短文生成练习集请求"""
    passage_id: int
    name: Optional[str] = None


class PracticeSetQuestionResponse(BaseModel):
    id: int
    question_id: int
    similar_question_id: Optional[int] = None
    display_order: int
    question_text: Optional[str] = None
    answer: Optional[str] = None
    phonetic: Optional[str] = None
    difficulty: Optional[int] = None
    knowledge_point: Optional[str] = None
    error_type: Optional[str] = None
    review_count: Optional[int] = 0
    is_correct: Optional[bool] = None
    user_answer: Optional[str] = None
    tags: Optional[List[dict]] = None
    # 新增：原题信息
    original_question_text: Optional[str] = None
    original_answer: Optional[str] = None
    original_image: Optional[str] = None
    student_answer: Optional[str] = None  # 学生作答（做题环节提交）
    question_type: Optional[str] = None  # 题型：choice/fill/judge/calc/application/operation/reading/writing/sentence
    # 阅读理解额外字段
    option_a: Optional[str] = None
    option_b: Optional[str] = None
    option_c: Optional[str] = None
    option_d: Optional[str] = None
    explanation: Optional[str] = None
    is_reading_question: Optional[bool] = None
    scene: Optional[dict] = None  # 图文场景（数学题自动配图，与评测端一致）
    score: Optional[int] = None  # 本题分值（按练习集计分方式算出）

    class Config:
        from_attributes = True


class PracticeSetResponse(BaseModel):
    id: int
    name: str
    notes: Optional[str] = None
    subject_id: int
    subject_name: Optional[str] = None
    source_type: str = "question"  # question=来自错题, word=来自单词复习
    question_type: str
    pdf_path: Optional[str] = None
    total_questions: int
    reviewed: bool
    review_count: int
    accuracy: Optional[float] = None  # 整体正确率
    last_reviewed_at: Optional[datetime] = None
    review_images: Optional[List[str]] = None  # 复习图片列表
    created_at: datetime
    questions: List[PracticeSetQuestionResponse] = []
    word_review_stats: Optional[dict] = None  # 单词复习统计
    pdf_url: Optional[str] = None  # PDF下载URL
    student_answered_count: Optional[int] = 0  # 学生已作答题数
    show_score: Optional[bool] = True  # 卷面是否显示分值
    score_mode: Optional[str] = "hundred"  # hundred=百分制100分 / default=题型默认分值
    total_score: Optional[int] = None  # 卷面总分（按计分方式算出）
    show_ai_author: Optional[bool] = False  # 卷面「出题人」是否署名「AI 出题助手」
    grammar_lesson_id: Optional[int] = None  # 语法专项练习集关联的语法点ID
    passage_id: Optional[int] = None  # 阅读理解练习集关联的短文ID
    grade: Optional[int] = None  # 练习集题目年级（取第一道题快照，做题端低年级数学判定用）

    class Config:
        from_attributes = True


class PracticeSetListResponse(BaseModel):
    total: int
    items: List[PracticeSetResponse]


class BatchSimilarRequest(BaseModel):
    question_ids: List[int]


class BatchSimilarResponse(BaseModel):
    success_count: int
    failed_count: int
    results: List[dict]


# ============ 辅助函数 ============

def load_practice_questions(db: Session, practice_set_id: int):
    """练习集内的题目快照（按显示顺序），返回 [(PracticeSetQuestion, PracticeQuestion)]"""
    psqs = db.query(PracticeSetQuestion).filter(
        PracticeSetQuestion.practice_set_id == practice_set_id
    ).order_by(PracticeSetQuestion.display_order).all()
    ids = [psq.practice_question_id for psq in psqs if psq.practice_question_id]
    qmap = {}
    if ids:
        qmap = {q.id: q for q in db.query(PracticeQuestion).filter(PracticeQuestion.id.in_(ids)).all()}
    return [(psq, qmap[psq.practice_question_id]) for psq in psqs if psq.practice_question_id in qmap]


def save_student_answers(db: Session, practice_set_id: int, user_id: int, pairs, answer_map: dict) -> int:
    """写作答记录（已提交未批改的作答复用同一条：一次作答 = 一条 practice_attempt）"""
    pending = {
        a.practice_question_id: a for a in db.query(PracticeAttempt).filter(
            PracticeAttempt.practice_set_id == practice_set_id,
            PracticeAttempt.is_correct.is_(None),
        ).order_by(PracticeAttempt.id.asc()).all()
    }
    saved = 0
    for psq, pq in pairs:
        if pq.id in answer_map:
            text = (answer_map[pq.id] or "").strip() or None
            att = pending.get(pq.id)
            if att:
                att.student_answer = text
            else:
                db.add(PracticeAttempt(
                    user_id=user_id,
                    practice_set_id=practice_set_id,
                    practice_question_id=pq.id,
                    error_question_id=pq.error_question_id,
                    student_answer=text,
                    is_correct=None,
                ))
            saved += 1
    db.flush()  # autoflush=False：提交前要让后续查询能看到刚写入的作答
    return saved


def apply_question_results(db: Session, ps: PracticeSet, pairs, results_list,
                           graded_by: str = "manual", is_all_correct: bool = None):
    """逐题批改落库：写作答记录 → 判错派生错题 → 同步错题缓存列。

    Returns: (correct_count, graded_count)
    """
    pending = {
        a.practice_question_id: a for a in db.query(PracticeAttempt).filter(
            PracticeAttempt.practice_set_id == ps.id,
            PracticeAttempt.is_correct.is_(None),
        ).order_by(PracticeAttempt.id.asc()).all()
    }

    correct_count = 0
    graded = 0
    for psq, question in pairs:
        if is_all_correct is True:
            mark = True
        else:
            result = next((r for r in results_list if r.get('question_id') == question.id), None)
            if result is None:
                continue  # 该题本次未批改
            mark = result.get('is_correct')

        attempt = pending.get(question.id)
        if attempt is not None:
            attempt.is_correct = mark if mark is None else bool(mark)
            attempt.graded_by = graded_by
            eq = db.get(ErrorQuestion, attempt.error_question_id) if attempt.error_question_id else None
            if eq is None and attempt.is_correct is False:
                eq = practice_flow.upsert_error_question_from_practice_question(db, question, ps.user_id)
                attempt.error_question_id = eq.id
                question.error_question_id = eq.id  # 回填：该练习题已对应错题
            if eq is not None and attempt.is_correct is not None:
                practice_flow.apply_review_result(eq, bool(attempt.is_correct))
        else:
            attempt = practice_flow.record_attempt(
                db,
                practice_set_id=ps.id,
                practice_question=question,
                is_correct=(mark if mark is None else bool(mark)),
                user_id=ps.user_id,
                graded_by=graded_by,
            )
        graded += 1
        if attempt.is_correct:
            correct_count += 1

    return correct_count, graded


# ============ 路由实现 ============

@router.post("/generate-from-questions", response_model=PracticeSetResponse, status_code=201)
def generate_practice_from_questions(
    data: GenerateFromQuestionsRequest,
    db: Session = Depends(get_db),
    kid_id: Optional[int] = Depends(get_required_kid_id),
):
    """
    从错题库组卷（错题复习）

    选择逻辑（优先级）：
    1. 未复习（review_count = 0）
    2. 需巩固（最近答错且未连续答对 / 正确率 < 60%）
    3. 其他（正确率 >= 60%）
    已掌握（连续答对 MASTERED_STREAK 次）的错题不再被抽到。
    """
    import random

    # 错题组卷：只从该孩子的错题池抽题（已掌握/已删除的不抽）
    query = db.query(ErrorQuestion).filter(
        ErrorQuestion.subject_id == data.subject_id,
        ErrorQuestion.user_id == kid_id,
        ErrorQuestion.deleted == False,  # noqa: E712
        ErrorQuestion.status == "active",
    )
    if data.grade:
        query = query.filter(ErrorQuestion.grade == data.grade)

    all_questions = query.all()

    # 分类到3个优先级池
    pool_unvisited = []    # 优先级1：未复习
    pool_need_review = []  # 优先级2：需巩固
    pool_other = []        # 优先级3：其他

    for q in all_questions:
        if (q.review_count or 0) == 0:
            pool_unvisited.append(q)
        elif (q.wrong_count or 0) > 0 and (q.correct_streak or 0) == 0:
            pool_need_review.append(q)
        elif (q.accuracy or 0) < 60:
            pool_need_review.append(q)
        else:
            pool_other.append(q)

    # 按优先级依次抽取
    selected_ids = []
    remaining = data.count

    for pool in [pool_unvisited, pool_need_review, pool_other]:
        if remaining <= 0:
            break
        if pool:
            count = min(len(pool), remaining)
            selected = random.sample(pool, count)
            selected_ids.extend([q.id for q in selected])
            remaining -= count

    # 实际取出的数量
    actual_count = len(selected_ids)
    if actual_count == 0:
        raise HTTPException(status_code=400, detail="没有符合条件的题目")

    # 取出错题对象（保持优先级顺序）
    eq_map = {q.id: q for q in all_questions}
    ordered_errors = [eq_map[qid] for qid in selected_ids if qid in eq_map]

    # 学科名称 + 知识点（用于卷名：数学三年级·错题重练卷·两位数乘一位数·5题）
    subject_obj = db.query(Subject).filter(Subject.id == data.subject_id).first() if data.subject_id else None
    subject_name = subject_obj.name if subject_obj else ""
    kps = []
    for eq in ordered_errors:
        kp = (eq.knowledge_point or "").strip()
        if kp and kp not in kps:
            kps.append(kp)

    # 创建练习集（归属该孩子）
    practice_set = PracticeSet(
        name=build_pool_practice_name(subject_name, data.grade, actual_count, kps),
        subject_id=data.subject_id,
        user_id=kid_id,
        source_type="question",
        question_type="original",
        total_questions=actual_count,
        show_score=data.show_score,
        score_mode=data.score_mode,
    )
    db.add(practice_set)
    db.flush()

    # 错题 → 练习题目快照 + 关联（内容各自独立，之后改错题不影响历史卷）
    ordered_questions = []
    for idx, eq in enumerate(ordered_errors):
        pq = practice_flow.snapshot_from_error_question(db, eq, user_id=kid_id)
        ordered_questions.append(pq)
        db.add(PracticeSetQuestion(
            practice_set_id=practice_set.id,
            practice_question_id=pq.id,
            display_order=idx,
        ))

    db.commit()
    db.refresh(practice_set)

    # 构建题目数据用于生成PDF
    questions_data = []
    for question in ordered_questions:
        questions_data.append({
            "question_text": question.parsed_question or question.original_text or "",
            "difficulty": question.difficulty or 3,
            "id": question.id,
            "knowledge_point": question.knowledge_point or "",
            "error_type": question.error_type or "",
            "question_type": question.question_type or "",
            "option_a": question.option_a,
            "option_b": question.option_b,
            "option_c": question.option_c,
            "option_d": question.option_d,
        })

    # 生成PDF
    pdf_url = None
    if questions_data:
        try:
            pdf_path = generate_practice_set_pdf(
                practice_set.name, questions_data,
                show_score=practice_set.show_score,
                score_mode=practice_set.score_mode,
                created_at=practice_set.created_at,
                subject_name=subject_name,
                grade_label=AI_GRADE_LABELS.get(data.grade) if data.grade else None,
                show_ai_author=bool(practice_set.show_ai_author),
            )
            practice_set.pdf_path = pdf_path
            db.commit()
            pdf_url = f"/uploads/{pdf_path}"
        except Exception as e:
            print(f"PDF生成失败: {e}")

    return {
        "id": practice_set.id,
        "name": practice_set.name,
        "subject_id": practice_set.subject_id,
        "subject_name": subject_name,
        "source_type": "question",
        "question_type": "original",
        "total_questions": actual_count,
        "reviewed": False,
        "review_count": 0,
        "pdf_path": practice_set.pdf_path,
        "created_at": practice_set.created_at,
        "questions": [],
        "pdf_url": pdf_url,
        "show_score": bool(practice_set.show_score),
        "score_mode": practice_set.score_mode or "hundred",
        "total_score": sum(compute_question_scores(
            [{"question_type": q.get("question_type") or ""} for q in questions_data],
            practice_set.score_mode or "hundred")),
        "show_ai_author": bool(practice_set.show_ai_author),
        "grammar_lesson_id": practice_set.grammar_lesson_id,
    }


AI_GRADE_LABELS = {
    1: "一年级", 2: "二年级", 3: "三年级", 4: "四年级", 5: "五年级", 6: "六年级",
    7: "七年级", 8: "八年级", 9: "九年级", 10: "高一", 11: "高二", 12: "高三",
}
AI_TYPE_LABELS = {
    "choice": "选择题", "fill": "填空题", "judge": "判断题", "calc": "计算题",
    "application": "应用题", "operation": "操作题", "reading": "阅读理解",
    "writing": "写作", "sentence": "连词成句",
}
# 难度标签（与前端出题表单一致：1 简单 ~ 5 困难）
AI_DIFFICULTY_LABELS = {1: "简单", 2: "基础", 3: "中等", 4: "偏难", 5: "困难"}


def difficulty_label_text(difficulty) -> str:
    """卷名里的难度写法：简单难度 / 基础难度 / 中等难度 / 偏难 / 困难"""
    label = AI_DIFFICULTY_LABELS.get(difficulty) if difficulty else ""
    if not label:
        return ""
    return f"{label}难度" if label in ("简单", "基础", "中等") else label


def build_ai_practice_name(subject_name, grade, knowledge_points, count,
                           question_types=None, preset_name=None, difficulty=None):
    """AI 练习集名称：年级学科 · 知识点 · 卷型/题型（难度） · 题数

    例如：三年级数学·两位数乘一位数·基础卷（中等难度）·4题
    没选卷型时按题型命名（计算题专项）；都没选则「综合练习」。
    （原来的 AI练习_20260917231714 对家长没有意义）
    """
    question_types = question_types or []
    parts = []
    grade_label = AI_GRADE_LABELS.get(grade) if grade else ""
    head = f"{grade_label}{subject_name or ''}"
    if head:
        parts.append(head)
    if knowledge_points:
        if len(knowledge_points) == 1:
            parts.append(knowledge_points[0])
        else:
            parts.append(f"{knowledge_points[0]}等{len(knowledge_points)}个知识点")
    # 卷型/题型：卷型优先，其次单题型专项，最后「综合练习」
    if preset_name:
        paper_part = preset_name
    elif len(question_types) == 1:
        paper_part = f"{AI_TYPE_LABELS.get(question_types[0], question_types[0])}专项"
    elif not knowledge_points:
        paper_part = "综合练习"
    else:
        paper_part = ""
    difficulty_label = difficulty_label_text(difficulty)
    if paper_part and difficulty_label:
        paper_part = f"{paper_part}（{difficulty_label}）"
    if paper_part:
        parts.append(paper_part)
    if count:
        parts.append(f"{count}题")
    name = "·".join(parts)[:120]
    return name or f"AI练习_{datetime.now().strftime('%Y%m%d%H%M%S')}"


def build_pool_practice_name(subject_name, grade, count, knowledge_points=None):
    """错题重练卷名称：年级学科 · 错题重练卷 · 知识点 · 题数

    例如：三年级数学·错题重练卷·两位数乘一位数·5题
    """
    parts = []
    grade_label = AI_GRADE_LABELS.get(grade) if grade else ""
    head = f"{grade_label}{subject_name or ''}"
    if head:
        parts.append(head)
    parts.append("错题重练卷")
    if knowledge_points:
        if len(knowledge_points) == 1:
            parts.append(knowledge_points[0])
        else:
            parts.append(f"{knowledge_points[0]}等{len(knowledge_points)}个知识点")
    if count:
        parts.append(f"{count}题")
    return "·".join(parts)[:120] or f"错题重练卷_{datetime.now().strftime('%Y%m%d%H%M%S')}"


class GenerateAIRequest(BaseModel):
    """AI结合知识点出题请求"""
    subject_id: int
    grade: Optional[int] = None  # 年级 1-6
    knowledge_points: List[str] = []  # 手动指定知识点；为空则自动统计薄弱知识点
    count: int = 5  # 题数
    difficulty: Optional[int] = None  # 难度 1-5
    question_types: List[str] = []  # 题型：choice/fill/judge/calc/application/operation/reading/writing/sentence；空=混合
    question_categories: List[str] = []  # 类型：basic/scene/comprehensive/thinking；空=混合
    preset_name: Optional[str] = None  # 试卷结构名（基础卷/标准卷/拓展卷），只用于命名
    show_score: bool = True  # 卷面是否显示分值
    score_mode: str = "hundred"  # hundred=百分制100分 / default=题型默认分值
    show_ai_author: bool = False  # 卷头「出题人」是否署名「AI 出题助手」（默认留空白）


@router.post("/generate-ai", response_model=PracticeSetResponse, status_code=201)
def generate_practice_from_ai(
    data: GenerateAIRequest,
    db: Session = Depends(get_db),
    kid_id: Optional[int] = Depends(get_required_kid_id),
):
    """AI结合知识点出题：自动统计薄弱知识点（或手动指定）→ LLM 生成 → 入库 → 组卷 → PDF"""
    import random

    subject = db.query(Subject).filter(Subject.id == data.subject_id).first()
    if not subject:
        raise HTTPException(status_code=404, detail="学科不存在")

    if data.count < 1 or data.count > 20:
        raise HTTPException(status_code=400, detail="题数需在 1-20 之间")
    if data.difficulty is not None and (data.difficulty < 1 or data.difficulty > 5):
        raise HTTPException(status_code=400, detail="难度需在 1-5 之间")

    # 题型/类型白名单校验
    VALID_TYPES = {"choice", "fill", "judge", "calc", "application", "operation", "reading", "writing", "sentence"}
    VALID_CATEGORIES = {"basic", "scene", "comprehensive", "thinking"}
    question_types = [t for t in data.question_types if t in VALID_TYPES]
    question_categories = [c for c in data.question_categories if c in VALID_CATEGORIES]

    # 1. 确定知识点：手动指定 > 自动统计该孩子的薄弱知识点（取错题答错次数最多的）
    knowledge_points = [kp.strip() for kp in data.knowledge_points if kp and kp.strip()]
    if not knowledge_points:
        rows = db.query(
            ErrorQuestion.knowledge_point,
            func.sum(ErrorQuestion.wrong_count).label("total_error"),
        ).filter(
            ErrorQuestion.subject_id == data.subject_id,
            ErrorQuestion.user_id == kid_id,
            ErrorQuestion.deleted == False,  # noqa: E712
            ErrorQuestion.knowledge_point.isnot(None),
            ErrorQuestion.knowledge_point != "",
        ).group_by(ErrorQuestion.knowledge_point).order_by(
            func.sum(ErrorQuestion.wrong_count).desc()
        ).limit(3).all()
        knowledge_points = [r[0] for r in rows]

    if not knowledge_points:
        raise HTTPException(
            status_code=400,
            detail="当前学科还没有错题知识点数据，请手动输入知识点（如：分数加减法、乘法分配律）",
        )

    # 2. LLM 出题
    from app.services.llm import llm_service
    result = llm_service.generate_questions_by_knowledge(
        knowledge_points=knowledge_points,
        subject=subject.name,
        grade=data.grade,
        count=data.count,
        difficulty=data.difficulty,
        question_types=question_types,
        question_categories=question_categories,
    )
    if result.get("error"):
        raise HTTPException(status_code=502, detail=result["error"])
    ai_questions = result.get("questions", [])
    if not ai_questions:
        raise HTTPException(status_code=502, detail="AI 没有生成可用题目")

    # 2.1 生成后校验：用户明确指定的题型必须出现；缺失时补一轮只生成缺失题型
    if question_types:
        def _type_satisfied(t: str) -> bool:
            for q in ai_questions:
                if (q.get("question_type") or "") != t:
                    continue
                # 选择题必须真的带 ≥2 个选项才算数（避免"标了 choice 其实是填空题"）
                if t == "choice" and len(q.get("options") or []) < 2:
                    continue
                return True
            return False

        missing_types = [t for t in question_types if not _type_satisfied(t)]
        if missing_types and data.count < 20:
            try:
                fill_count = max(len(ai_questions) // 2, 1)  # 补题量不超过现有的一半
                result2 = llm_service.generate_questions_by_knowledge(
                    knowledge_points=knowledge_points,
                    subject=subject.name,
                    grade=data.grade,
                    count=fill_count,
                    difficulty=data.difficulty,
                    question_types=missing_types,
                    question_categories=question_categories,
                )
                extra = result2.get("questions", [])
                # 只接收缺失题型的题目，且不重复
                seen_q = {q["question"] for q in ai_questions}
                for q in extra:
                    if q["question"] in seen_q:
                        continue
                    qt = q.get("question_type") or ""
                    if qt not in missing_types:
                        continue
                    if qt == "choice" and len(q.get("options") or []) < 2:
                        continue  # 补出来的"选择题"没有选项，不收
                    ai_questions.append(q)
                    seen_q.add(q["question"])
                # 严格截断到请求题数（主流程已截断；补题型后不得超量）
                ai_questions = ai_questions[: data.count]
            except Exception as e:
                print(f"AI出题 缺失题型补生成失败: {e}")

    # 2.2 按试卷大题顺序排序（选择→填空→判断→计算→应用→操作→阅读→写作）
    TYPE_ORDER = {"choice": 1, "fill": 2, "judge": 3, "calc": 4, "application": 5,
                  "operation": 6, "reading": 7, "writing": 8, "sentence": 9}
    ai_questions.sort(key=lambda q: TYPE_ORDER.get(q.get("question_type") or "", 99))

    # 3. 题目入库（练习题目快照表；AI 练习题不属于错题，只有做错时才派生错题）
    new_questions = []
    for item in ai_questions:
        pq = practice_flow.snapshot_from_ai_item(
            db, item,
            user_id=kid_id,
            subject_id=data.subject_id,
            grade=data.grade,
            question_types=question_types,
            question_categories=question_categories,
            default_knowledge_point=knowledge_points[0] if knowledge_points else None,
        )
        if pq is not None:  # 自检拒绝的不合格题不入库
            new_questions.append(pq)

    # 4. 创建练习集
    practice_set = PracticeSet(
        name=build_ai_practice_name(
            subject.name, data.grade, knowledge_points, len(new_questions),
            question_types, data.preset_name, data.difficulty,
        ),
        subject_id=data.subject_id,
        user_id=kid_id,
        source_type="ai",
        question_type="original",
        total_questions=len(new_questions),
        show_score=data.show_score,
        score_mode=data.score_mode,
        show_ai_author=data.show_ai_author,
    )
    db.add(practice_set)
    db.flush()

    for idx, question in enumerate(new_questions):
        db.add(PracticeSetQuestion(
            practice_set_id=practice_set.id,
            practice_question_id=question.id,
            display_order=idx,
        ))

    # 5. 生成 PDF（按题型分组，试卷式排版 + 分值）
    pdf_url = None
    try:
        questions_data = [{
            "question_text": q.parsed_question or q.original_text or "",
            "difficulty": q.difficulty or 3,
            "id": q.id,
            "knowledge_point": q.knowledge_point or "",
            "error_type": q.error_type or "",
            "question_type": q.question_type or "",
        } for q in new_questions]
        pdf_path = generate_practice_set_pdf(
            practice_set.name, questions_data,
            show_score=practice_set.show_score,
            score_mode=practice_set.score_mode,
            created_at=practice_set.created_at,
            subject_name=subject.name,
            grade_label=AI_GRADE_LABELS.get(data.grade) if data.grade else None,
            show_ai_author=bool(practice_set.show_ai_author),
        )
        practice_set.pdf_path = pdf_path
        pdf_url = f"/uploads/{pdf_path}"
    except Exception as e:
        print(f"AI出题 PDF生成失败: {e}")

    db.commit()
    db.refresh(practice_set)

    return {
        "id": practice_set.id,
        "name": practice_set.name,
        "subject_id": practice_set.subject_id,
        "subject_name": subject.name,
        "source_type": "ai",
        "question_type": "original",
        "total_questions": len(new_questions),
        "reviewed": False,
        "review_count": 0,
        "pdf_path": practice_set.pdf_path,
        "created_at": practice_set.created_at,
        "questions": [],
        "pdf_url": pdf_url,
        "show_score": bool(practice_set.show_score),
        "score_mode": practice_set.score_mode or "hundred",
        "total_score": sum(compute_question_scores(
            [{"question_type": q.get("question_type") or ""} for q in questions_data],
            practice_set.score_mode or "hundred")),
        "show_ai_author": bool(practice_set.show_ai_author),
        "grammar_lesson_id": practice_set.grammar_lesson_id,
    }


@router.post("/generate-from-reading", response_model=PracticeSetResponse, status_code=201)
def generate_practice_from_reading(
    data: GenerateFromReadingRequest,
    db: Session = Depends(get_db),
    kid_id: Optional[int] = Depends(get_required_kid_id),
):
    """
    从短文生成阅读理解练习集

    创建 source_type=reading 的练习集，关联短文
    """
    from app.models.reading import ReadingPassage, ReadingQuestion

    # 验证短文存在
    passage = db.query(ReadingPassage).options(
        joinedload(ReadingPassage.questions)
    ).filter(
        ReadingPassage.id == data.passage_id,
        ReadingPassage.deleted == False
    ).first()

    if not passage:
        raise HTTPException(status_code=404, detail="短文不存在")

    if not passage.questions:
        raise HTTPException(status_code=400, detail="该短文没有选择题")

    # 创建练习集（reading 类型不创建 PracticeSetQuestion 记录，
    # 题目来自 ReadingQuestion 表，通过 passage_id 关联）
    practice_set = PracticeSet(
        name=data.name or f"阅读理解-{passage.title}"[:200],
        subject_id=_get_english_subject_id(db),
        user_id=kid_id,  # 归属当前孩子（practice_set.user_id NOT NULL）
        source_type="reading",
        question_type="original",
        total_questions=len(passage.questions),
        passage_id=passage.id,
    )
    db.add(practice_set)
    db.commit()
    db.refresh(practice_set)

    subject_name = db.query(Subject).filter(Subject.id == practice_set.subject_id).first().name if practice_set.subject_id else ""

    return {
        "id": practice_set.id,
        "name": practice_set.name,
        "subject_id": practice_set.subject_id,
        "subject_name": subject_name,
        "source_type": "reading",
        "question_type": "original",
        "pdf_path": practice_set.pdf_path,
        "total_questions": len(passage.questions),
        "reviewed": False,
        "review_count": 0,
        "created_at": practice_set.created_at,
        "questions": [],
    }


def _get_english_subject_id(db: Session) -> int:
    """获取英语学科ID，如果不存在则创建"""
    from app.models.subject import Subject
    subject = db.query(Subject).filter(Subject.name == "英语").first()
    if subject:
        return subject.id
    # 创建英语学科
    subject = Subject(name="英语")
    db.add(subject)
    db.commit()
    db.refresh(subject)
    return subject.id


@router.post("", response_model=PracticeSetResponse, status_code=201)
def create_practice_set(data: PracticeSetCreate, db: Session = Depends(get_db)):
    """
    创建练习集

    1. 验证所有题目存在且未删除
    2. 如果是similar类型，自动为每道题生成相似题
    3. 创建练习集和关联记录
    """
    # 验证题目（手动组卷的题目来自错题库）
    error_questions = db.query(ErrorQuestion).filter(
        ErrorQuestion.id.in_(data.question_ids),
        ErrorQuestion.deleted == False  # noqa: E712
    ).all()

    if len(error_questions) != len(data.question_ids):
        raise HTTPException(status_code=400, detail="部分错题不存在或已删除")

    if not error_questions:
        raise HTTPException(status_code=400, detail="题目列表为空")

    eq_by_id = {q.id: q for q in error_questions}
    ordered_errors = [eq_by_id[qid] for qid in data.question_ids if qid in eq_by_id]

    # 获取学科ID、归属孩子（使用第一道题的）
    subject_id = ordered_errors[0].subject_id
    kid_id = ordered_errors[0].user_id

    subject_obj = db.query(Subject).filter(Subject.id == subject_id).first()
    subject_name = subject_obj.name if subject_obj else ""

    # 如果是相似题类型，先行为每道错题生成相似题
    similar_question_ids = []
    if data.question_type == "similar":
        from app.services.llm import llm_service

        for eq in ordered_errors:
            # 检查是否已有相似题
            existing = db.query(SimilarQuestion).filter(
                SimilarQuestion.source_question_id == eq.id,
                SimilarQuestion.deleted == False
            ).first()

            if existing:
                similar_question_ids.append((eq.id, existing.id))
            else:
                # 调用LLM生成相似题
                try:
                    result = llm_service.generate_similar_question(
                        question=eq.parsed_question or eq.original_text,
                        answer=eq.answer or "",
                        subject=subject_name,
                        knowledge_point=eq.knowledge_point or "",
                    )

                    if result.get("error"):
                        continue

                    # 保存相似题（source_question_id 关联错题 id）
                    similar = SimilarQuestion(
                        source_question_id=eq.id,
                        similar_text=result.get("similar_question", ""),
                        similar_answer=result.get("similar_answer", ""),
                        similarity_score=0.85,
                    )
                    db.add(similar)
                    db.commit()
                    db.refresh(similar)
                    similar_question_ids.append((eq.id, similar.id))
                except Exception:
                    continue

    # 创建练习集（归属该孩子）
    practice_set = PracticeSet(
        name=data.name,
        subject_id=subject_id,
        user_id=kid_id,
        source_type=data.source_type,
        question_type=data.question_type,
        total_questions=len(data.question_ids),
        show_score=data.show_score,
        score_mode=data.score_mode,
    )
    db.add(practice_set)
    db.flush()

    # 错题 → 练习题目快照 + 关联记录
    for idx, eq in enumerate(ordered_errors):
        similar_q_id = None
        if data.question_type == "similar" and similar_question_ids:
            for q_id, sq_id in similar_question_ids:
                if q_id == eq.id:
                    similar_q_id = sq_id
                    break

        pq = practice_flow.snapshot_from_error_question(db, eq, user_id=kid_id)
        psq = PracticeSetQuestion(
            practice_set_id=practice_set.id,
            practice_question_id=pq.id,
            similar_question_id=similar_q_id,
            display_order=idx,
        )
        db.add(psq)

    db.commit()
    db.refresh(practice_set)

    # 触发积分行为（创建练习集）
    from app.services.motivation import MotivationService
    try:
        service = MotivationService(db)
        service.trigger_action("create_practice_set", user_id=kid_id, reason=f"创建练习集：{practice_set.name}")
    except Exception:
        pass  # 激励系统不影响主流程

    # 返回结果

    return {
        "id": practice_set.id,
        "name": practice_set.name,
        "subject_id": practice_set.subject_id,
        "subject_name": subject_name,
        "source_type": practice_set.source_type or "question",
        "question_type": practice_set.question_type,
        "pdf_path": practice_set.pdf_path,
        "total_questions": practice_set.total_questions,
        "reviewed": practice_set.reviewed,
        "review_count": practice_set.review_count,
        "created_at": practice_set.created_at,
        "questions": [],
    }


@router.get("", response_model=PracticeSetListResponse)
def list_practice_sets(
    skip: int = 0,
    limit: int = 20,
    subject_id: Optional[int] = None,
    grade: Optional[int] = Query(None, ge=1, le=12, description="按年级过滤（练习集内题目年级）"),
    reviewed: Optional[bool] = None,
    source_type: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    db: Session = Depends(get_db),
    kid_id: Optional[int] = Depends(get_current_kid_id),
):
    """获取练习集列表（按孩子隔离；家长未选孩子时返回全部）"""
    query = db.query(PracticeSet).filter(PracticeSet.deleted == False)  # noqa: E712

    if kid_id is not None:
        query = query.filter(PracticeSet.user_id == kid_id)
    if subject_id:
        query = query.filter(PracticeSet.subject_id == subject_id)
    if grade is not None:
        # 练习集无年级字段：按练习集内题目年级过滤（题目快照表）
        query = query.filter(
            db.query(PracticeSetQuestion.id)
            .join(PracticeQuestion, PracticeQuestion.id == PracticeSetQuestion.practice_question_id)
            .filter(
                PracticeSetQuestion.practice_set_id == PracticeSet.id,
                PracticeQuestion.deleted == False,
                PracticeQuestion.grade == grade,
            )
            .exists()
        )
    if reviewed is not None:
        query = query.filter(PracticeSet.reviewed == reviewed)
    if source_type:
        query = query.filter(PracticeSet.source_type == source_type)
    if start_date:
        query = query.filter(PracticeSet.created_at >= start_date)
    if end_date:
        query = query.filter(PracticeSet.created_at <= f"{end_date} 23:59:59")

    total = query.count()
    items = query.order_by(PracticeSet.created_at.desc()).offset(skip).limit(limit).all()

    result = []
    for ps in items:
        subject_name = db.query(Subject).filter(Subject.id == ps.subject_id).first().name if ps.subject_id else ""

        # 学生已作答题数（作答记录里提交过答案的题）
        student_answered_count = db.query(
            func.count(func.distinct(PracticeAttempt.practice_question_id))
        ).filter(
            PracticeAttempt.practice_set_id == ps.id,
            PracticeAttempt.student_answer.isnot(None),
            PracticeAttempt.student_answer != "",
        ).scalar() or 0

        # 获取单词复习统计
        word_review_stats = None
        if ps.source_type == "word":
            print(f"[DEBUG] Processing word practice set id={ps.id}, name={ps.name}")
            sessions = db.query(WordReviewSession).filter(
                WordReviewSession.practice_set_id == ps.id
            ).order_by(WordReviewSession.reviewed_at.desc()).all()
            print(f"[DEBUG] Found {len(sessions)} sessions for practice_set_id={ps.id}")

            if sessions:
                total_count = sum(s.total_count for s in sessions)
                total_correct = sum(s.correct_count for s in sessions)
                total_duration = sum(getattr(s, 'duration', 0) or 0 for s in sessions)

                # 获取复习类型（从最近的复习日志中获取）
                review_type = 1  # 默认默写
                latest_session = sessions[0]  # 最近的复习场次
                if latest_session.session_id:
                    from app.models.word import WordReview
                    word_review = db.query(WordReview).filter(WordReview.id == latest_session.session_id).first()
                    if word_review:
                        # 查找该场次的复习日志
                        log = db.query(WordReviewLog).filter(
                            WordReviewLog.reviewed_at >= word_review.reviewed_at,
                            WordReviewLog.deleted == False
                        ).order_by(WordReviewLog.reviewed_at.desc()).first()
                        if log:
                            review_type = log.review_type

                word_review_stats = {
                    "total_count": total_count,
                    "correct_count": total_correct,
                    "accuracy": round(total_correct / total_count * 100, 1) if total_count > 0 else 0,
                    "duration": total_duration,
                    "review_type": review_type,
                }
                print(f"[DEBUG] word_review_stats = {word_review_stats}")

        result.append({
            "id": ps.id,
            "name": ps.name,
            "subject_id": ps.subject_id,
            "subject_name": subject_name,
            "source_type": ps.source_type or "question",
            "question_type": ps.question_type,
            "pdf_path": ps.pdf_path,
            "total_questions": ps.total_questions,
            "reviewed": ps.reviewed or False,
            "review_count": ps.review_count or 0,
            "accuracy": ps.accuracy,
            "student_answered_count": student_answered_count,
            "created_at": ps.created_at,
            "questions": [],
            "word_review_stats": word_review_stats,
            "grammar_lesson_id": ps.grammar_lesson_id,
        })

    return {"total": total, "items": result}


@router.get("/{practice_set_id}", response_model=PracticeSetResponse)
def get_practice_set(practice_set_id: int, db: Session = Depends(get_db)):
    """获取练习集详情（含题目列表）"""
    ps = db.query(PracticeSet).filter(
        PracticeSet.id == practice_set_id,
        PracticeSet.deleted == False
    ).first()

    if not ps:
        raise HTTPException(status_code=404, detail="练习集不存在")

    subject_name = db.query(Subject).filter(Subject.id == ps.subject_id).first().name if ps.subject_id else ""

    # 解析复习图片
    review_images = None
    if ps.review_images:
        try:
            import json
            review_images = json.loads(ps.review_images)
        except:
            review_images = [ps.review_images] if ps.review_images else None

    # 获取关联的题目
    questions = []
    word_review_stats = None
    pairs = []  # 错题/AI 练习集题目快照（grade 推导用；word/reading 分支不涉及）

    if ps.source_type == "word":
        # 单词练习集：获取复习统计和单词题目
        sessions = db.query(WordReviewSession).filter(
            WordReviewSession.practice_set_id == practice_set_id
        ).order_by(WordReviewSession.reviewed_at.desc()).all()

        if sessions:
            total_count = sum(s.total_count for s in sessions)
            total_correct = sum(s.correct_count for s in sessions)
            total_duration = sum(getattr(s, 'duration', 0) or 0 for s in sessions)

            # 获取复习类型（从最近的复习日志中获取）
            review_type = 1  # 默认默写
            latest_session = sessions[0]  # 最近的复习场次
            if latest_session.session_id:
                from app.models.word import WordReview
                word_review = db.query(WordReview).filter(WordReview.id == latest_session.session_id).first()
                if word_review:
                    log = db.query(WordReviewLog).filter(
                        WordReviewLog.reviewed_at >= word_review.reviewed_at,
                        WordReviewLog.deleted == False
                    ).order_by(WordReviewLog.reviewed_at.desc()).first()
                    if log:
                        review_type = log.review_type

            word_review_stats = {
                "total_count": total_count,
                "correct_count": total_correct,
                "accuracy": round(total_correct / total_count * 100, 1) if total_count > 0 else 0,
                "duration": total_duration,
                "reviewed_at": sessions[0].reviewed_at if sessions else None,
                "review_type": review_type,
            }

            # 获取单词题目（从 WordReviewLog 中获取，通过 reviewed_at 时间匹配）
            for idx, session in enumerate(sessions):
                review_logs = db.query(WordReviewLog).filter(
                    WordReviewLog.reviewed_at == session.reviewed_at
                ).order_by(WordReviewLog.id).all()

                for log in review_logs:
                    word = db.query(Word).filter(Word.id == log.word_id).first()
                    if not word:
                        continue
                    # 获取单词标签
                    tags = [{"id": t.id, "name": t.name} for t in word.tags] if word.tags else []
                    questions.append({
                        "id": log.id,
                        "question_id": word.id,
                        "similar_question_id": None,
                        "display_order": len(questions),
                        "question_text": word.english,
                        "answer": word.chinese,
                        "phonetic": word.phonetic,
                        "difficulty": None,
                        "is_correct": log.is_correct,
                        "user_answer": log.user_answer,
                        "tags": tags,
                    })

    if ps.source_type == "reading" and ps.passage_id:
        from app.models.reading import ReadingPassage, ReadingQuestion
        passage = db.query(ReadingPassage).options(
            joinedload(ReadingPassage.questions)
        ).filter(ReadingPassage.id == ps.passage_id).first()

        if passage:
            for idx, q in enumerate(passage.questions):
                questions.append({
                    "id": q.id,
                    "question_id": q.id,
                    "similar_question_id": None,
                    "display_order": idx,
                    "question_text": q.question_text,
                    "answer": q.correct_answer,
                    "difficulty": passage.difficulty,
                    "knowledge_point": f"阅读理解-{passage.topic}",
                    "is_correct": None,
                    "tags": [],
                    "original_question_text": q.question_text,
                    "original_answer": q.correct_answer,
                    "original_image": None,
                    # 阅读理解额外字段
                    "option_a": q.option_a,
                    "option_b": q.option_b,
                    "option_c": q.option_c,
                    "option_d": q.option_d,
                    "explanation": q.explanation,
                    "is_reading_question": True,
                })
    else:
        # 错题/AI 练习集：从练习题目快照读取，作答结果取最新一次 practice_attempt
        latest = practice_flow.latest_attempt_map(db, practice_set_id)
        pairs = load_practice_questions(db, practice_set_id)
        eq_ids = [q.error_question_id for _, q in pairs if q.error_question_id]
        eq_map = {e.id: e for e in db.query(ErrorQuestion).filter(ErrorQuestion.id.in_(eq_ids)).all()} if eq_ids else {}

        for psq, question in pairs:
            question_text = question.parsed_question or question.original_text or ""
            answer = question.answer or ""

            # 旧数据兜底：早期 AI 题把选项塞在题干里、或把填空题错标成 choice
            q_type = question.question_type or ""
            opt_a, opt_b, opt_c, opt_d = question.option_a, question.option_b, question.option_c, question.option_d
            if q_type == "choice" and not opt_a:
                from app.services.llm import extract_inline_options, infer_question_type
                cleaned, inline_opts = extract_inline_options(question_text)
                if len(inline_opts) >= 2:
                    question_text = cleaned
                    opt_a = inline_opts[0]
                    opt_b = inline_opts[1] if len(inline_opts) > 1 else None
                    opt_c = inline_opts[2] if len(inline_opts) > 2 else None
                    opt_d = inline_opts[3] if len(inline_opts) > 3 else None
                else:
                    # 根本没有选项 → 不是选择题，按内容纠正（仅影响展示）
                    q_type = infer_question_type(question_text, answer, subject_name, allow_choice=False)

            attempt = latest.get(question.id)
            eq = eq_map.get(question.error_question_id) if question.error_question_id else None
            # 图文场景（数学题自动配图，与评测端一致：孩子看 emoji 图更好理解）
            scene = None
            if ps.subject_id == 1:
                try:
                    from app.routers.assessment import _resolve_scene
                    scene = _resolve_scene(question)
                except Exception:
                    scene = None
            questions.append({
                "id": psq.id,
                "question_id": question.id,
                "similar_question_id": psq.similar_question_id,
                "display_order": psq.display_order,
                "question_text": question_text,
                "answer": answer,
                "difficulty": question.difficulty,
                "knowledge_point": question.knowledge_point or "",
                "error_type": question.error_type or "",
                "review_count": (eq.review_count or 0) if eq else 0,
                "is_correct": attempt.is_correct if attempt else None,
                "original_question_text": question_text,
                "original_answer": question.answer or "",
                "original_image": question.original_images or None,
                "student_answer": (attempt.student_answer if attempt else "") or "",
                "question_type": q_type,
                # 选择题选项（AI 出题时独立存储；旧数据在读取时从题干切分）
                "option_a": opt_a or None,
                "option_b": opt_b or None,
                "option_c": opt_c or None,
                "option_d": opt_d or None,
                "explanation": question.analysis or None,
                "is_reading_question": False,
                "scene": scene,
                "error_question_id": question.error_question_id,
                "source": question.source,
            })

    # 每题分值：与 PDF 用同一套算法，保证屏幕上的卷子和打印出来的一致
    score_mode = normalize_score_mode(getattr(ps, "score_mode", None) or DEFAULT_SCORE_MODE)
    question_scores = compute_question_scores(
        [{"question_type": (q.get("question_type") or ("reading" if q.get("is_reading_question") else ""))}
         for q in questions],
        score_mode,
    )
    for q, qs_score in zip(questions, question_scores):
        q["score"] = qs_score

    # 练习集题目年级：取第一道题快照的非空年级（做题端低年级数学判定用）
    ps_grade = next((q.grade for _, q in pairs if q.grade), None)

    return {
        "id": ps.id,
        "name": ps.name,
        "notes": ps.notes,
        "subject_id": ps.subject_id,
        "subject_name": subject_name,
        "source_type": ps.source_type or "question",
        "question_type": ps.question_type,
        "pdf_path": ps.pdf_path,
        "total_questions": ps.total_questions,
        "reviewed": ps.reviewed,
        "review_count": ps.review_count,
        "accuracy": ps.accuracy,
        "last_reviewed_at": ps.last_reviewed_at,
        "review_images": review_images,
        "created_at": ps.created_at,
        "questions": questions,
        "word_review_stats": word_review_stats,
        "grammar_lesson_id": ps.grammar_lesson_id,
        # 阅读理解练习集：ReadingTest 页面据此拉短文与题目（曾漏返回 → 测试页只显示标题）
        "passage_id": ps.passage_id,
        "show_score": True if ps.show_score is None else bool(ps.show_score),
        "score_mode": score_mode,
        "total_score": sum(question_scores),
        "show_ai_author": bool(ps.show_ai_author),
        "grade": ps_grade,
    }


class PracticeSetUpdateRequest(BaseModel):
    """更新练习集请求"""
    name: Optional[str] = None
    notes: Optional[str] = None


class ReviewImagesUpdateRequest(BaseModel):
    """更新复习图片请求"""
    images: Optional[List[str]] = None  # 新的图片路径列表


@router.put("/{practice_set_id}")
def update_practice_set(practice_set_id: int, data: PracticeSetUpdateRequest, db: Session = Depends(get_db)):
    """更新练习集名称和备注"""
    ps = db.query(PracticeSet).filter(
        PracticeSet.id == practice_set_id,
        PracticeSet.deleted == False
    ).first()

    if not ps:
        raise HTTPException(status_code=404, detail="练习集不存在")

    if data.name is not None:
        ps.name = data.name
    if data.notes is not None:
        ps.notes = data.notes

    db.commit()

    return {"message": "更新成功"}


@router.put("/{practice_set_id}/review-images")
def update_review_images(
    practice_set_id: int,
    data: ReviewImagesUpdateRequest,
    db: Session = Depends(get_db)
):
    """更新练习集的复习图片"""
    ps = db.query(PracticeSet).filter(
        PracticeSet.id == practice_set_id,
        PracticeSet.deleted == False
    ).first()

    if not ps:
        raise HTTPException(status_code=404, detail="练习集不存在")

    if data.images is not None:
        import json
        ps.review_images = json.dumps(data.images, ensure_ascii=False)

    db.commit()

    return {"message": "更新成功", "review_images": data.images}


@router.post("/{practice_set_id}/generate-pdf")
def generate_pdf(practice_set_id: int, db: Session = Depends(get_db)):
    """为练习集生成PDF"""
    ps = db.query(PracticeSet).filter(
        PracticeSet.id == practice_set_id,
        PracticeSet.deleted == False
    ).first()

    if not ps:
        raise HTTPException(status_code=404, detail="练习集不存在")

    questions_data = []

    # 阅读理解类型：从ReadingPassage和ReadingQuestion获取题目
    if ps.source_type == "reading" and ps.passage_id:
        passage = db.query(ReadingPassage).filter(
            ReadingPassage.id == ps.passage_id,
            ReadingPassage.deleted == False
        ).first()
        if passage:
            reading_questions = db.query(ReadingQuestion).filter(
                ReadingQuestion.passage_id == ps.passage_id,
                ReadingQuestion.deleted == False
            ).order_by(ReadingQuestion.question_number).all()

            for rq in reading_questions:
                questions_data.append({
                    "question_text": f"{rq.question_number}. {rq.question_text}",
                    "option_a": rq.option_a,
                    "option_b": rq.option_b,
                    "option_c": rq.option_c,
                    "option_d": rq.option_d,
                    "is_reading_question": True,
                    "id": rq.id,
                })
            # 保存短文标题供PDF使用
            if questions_data:
                questions_data[0]["_passage_title"] = passage.title
                questions_data[0]["_passage_content"] = passage.content
    else:
        # 普通练习集：从练习题目快照获取题目
        for psq, question in load_practice_questions(db, practice_set_id):
            question_text = None
            if ps.question_type == "similar" and psq.similar_question_id:
                similar = db.query(SimilarQuestion).filter(SimilarQuestion.id == psq.similar_question_id).first()
                question_text = similar.similar_text if similar else None
            if not question_text:
                question_text = question.parsed_question or question.original_text or ""

            questions_data.append({
                "question_text": question_text,
                "difficulty": question.difficulty or 3,
                "id": question.id,
                "knowledge_point": question.knowledge_point or "",
                "error_type": question.error_type or "",
                "review_count": 0,
                "question_type": question.question_type or "",
                "option_a": question.option_a,
                "option_b": question.option_b,
                "option_c": question.option_c,
                "option_d": question.option_d,
            })

    if not questions_data:
        raise HTTPException(status_code=400, detail="练习集没有题目")

    # 生成PDF
    try:
        # 确保name是Unicode字符串
        ps_name = str(ps.name) if ps.name else "练习集"
        pdf_subject = db.query(Subject).filter(Subject.id == ps.subject_id).first() if ps.subject_id else None
        pdf_path = generate_practice_set_pdf(
            ps_name, questions_data,
            show_score=True if ps.show_score is None else bool(ps.show_score),
            score_mode=ps.score_mode or "default",
            created_at=ps.created_at,
            subject_name=pdf_subject.name if pdf_subject else None,
            show_ai_author=bool(ps.show_ai_author),
        )
        ps.pdf_path = pdf_path
        db.commit()

        logger_service.log_operation(
            operation_type="generate_pdf",
            target_type="practice_set",
            target_id=ps.id,
            data={"pdf_path": pdf_path},
            success=True,
        )

        return {"pdf_url": f"/uploads/{pdf_path}"}
    except Exception as e:
        logger_service.log_operation(
            operation_type="generate_pdf",
            target_type="practice_set",
            target_id=ps.id,
            data={},
            success=False,
            error=str(e),
        )
        raise HTTPException(status_code=500, detail=f"PDF生成失败: {str(e)}")


class SubmitAnswersItem(BaseModel):
    """做题提交：单题作答"""
    question_id: int
    answer: str


class SubmitAnswersRequest(BaseModel):
    """做题提交请求"""
    answers: List[SubmitAnswersItem]


@router.post("/{practice_set_id}/submit-answers")
def submit_practice_answers(
    practice_set_id: int,
    data: SubmitAnswersRequest,
    db: Session = Depends(get_db)
):
    """学生做题提交：保存每道题的学生作答（供家长批改）"""
    ps = db.query(PracticeSet).filter(
        PracticeSet.id == practice_set_id,
        PracticeSet.deleted == False
    ).first()

    if not ps:
        raise HTTPException(status_code=404, detail="练习集不存在")

    answer_map = {a.question_id: a.answer for a in data.answers}
    if not answer_map:
        raise HTTPException(status_code=400, detail="作答内容为空")

    pairs = load_practice_questions(db, practice_set_id)
    if not pairs:
        raise HTTPException(status_code=400, detail="练习集没有题目")

    # 已提交未批改的作答复用同一条记录（一次作答 = 一条 practice_attempt）
    saved = save_student_answers(db, practice_set_id, ps.user_id, pairs, answer_map)

    db.commit()
    return {"message": "作答已保存", "saved": saved, "total": len(pairs)}


@router.post("/{practice_set_id}/ai-grade")
def ai_grade_practice_set(
    practice_set_id: int,
    db: Session = Depends(get_db)
):
    """大模型一键批改：读取学生已提交的作答，LLM 逐题判断对错并给出错因（图片题自动跳过，提示人工批改）"""
    ps = db.query(PracticeSet).filter(
        PracticeSet.id == practice_set_id,
        PracticeSet.deleted == False
    ).first()

    if not ps:
        raise HTTPException(status_code=404, detail="练习集不存在")

    pairs = load_practice_questions(db, practice_set_id)
    if not pairs:
        raise HTTPException(status_code=400, detail="练习集没有题目")

    latest = practice_flow.latest_attempt_map(db, practice_set_id)
    items = []
    unsupported = []
    for psq, question in pairs:
        qid = question.id
        question_text = question.parsed_question or question.original_text or ""
        answer = question.answer or ""
        is_image_only = (not question_text) and bool(question.original_images)
        attempt = latest.get(qid)
        student_answer = (attempt.student_answer if attempt else "") or ""

        if not question_text or is_image_only:
            unsupported.append({"question_id": qid, "reason": "图片题暂不支持AI批改，请人工批改"})
            continue

        items.append({
            "question_id": qid,
            "question": question_text,
            "answer": answer,
            "student_answer": student_answer.strip() or "（未作答）",
        })

    if not items:
        return {"results": [], "unsupported": unsupported, "message": "本练习集暂无可AI批改的题目"}

    from app.services.llm import llm_service
    subject = db.query(Subject).filter(Subject.id == ps.subject_id).first()
    result = llm_service.grade_answers(items, subject=subject.name if subject else "")

    if result.get("error"):
        raise HTTPException(status_code=502, detail=result["error"])

    return {"results": result.get("results", []), "unsupported": unsupported}


class PhotoSubmitAnswer(BaseModel):
    question_id: int
    answer: str = ""


class PhotoSubmitRequest(BaseModel):
    """线下做题拍照交卷"""
    answers: List[PhotoSubmitAnswer] = []
    images: List[str] = []              # 卷子照片相对路径（/recognize-paper 返回，存为复习图片）
    auto_grade: bool = True             # True=紧接着调 LLM 批改；False=只存作答等人工批改
    question_results: Optional[List[dict]] = None  # 人工核对后的对错（给了就不再调 AI）


def _question_dicts(pairs) -> List[dict]:
    """转成 paper_ocr 需要的题目结构（题号顺序由 paper_ocr 复现 PDF 分组）"""
    out = []
    for _psq, q in pairs:
        out.append({
            "id": q.id,
            "parsed_question": q.parsed_question,
            "original_text": q.original_text,
            "question_type": q.question_type,
            "option_a": q.option_a,
            "option_b": q.option_b,
            "option_c": q.option_c,
            "option_d": q.option_d,
        })
    return out


@router.post("/{practice_set_id}/recognize-paper")
async def recognize_paper(
    practice_set_id: int,
    files: List[UploadFile] = File(...),
    db: Session = Depends(get_db),
):
    """线下做题：上传卷子照片，自动识别学生手写作答（只识别不落库，供核对后交卷）"""
    ps = db.query(PracticeSet).filter(
        PracticeSet.id == practice_set_id,
        PracticeSet.deleted == False,
    ).first()
    if not ps:
        raise HTTPException(status_code=404, detail="练习集不存在")

    pairs = load_practice_questions(db, practice_set_id)
    if not pairs:
        raise HTTPException(status_code=400, detail="练习集没有题目")
    if not files:
        raise HTTPException(status_code=400, detail="请先拍照或选择照片")

    from app.routers.upload import _save_image
    saved_paths = []
    abs_paths = []
    for f in files:
        info = await _save_image(f)
        if info.get("error"):
            raise HTTPException(status_code=400, detail=info["error"])
        saved_paths.append(info["image_path"])
        abs_paths.append(info["absolute_path"])

    subject = db.query(Subject).filter(Subject.id == ps.subject_id).first()
    try:
        result = paper_ocr.recognize_answers(
            abs_paths, _question_dicts(pairs), subject=subject.name if subject else ""
        )
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"识别失败：{e}")

    if result.get("error"):
        raise HTTPException(status_code=502, detail=result["error"])

    ordered = paper_ocr.printed_order(_question_dicts(pairs))
    latest = practice_flow.latest_attempt_map(db, practice_set_id)
    by_qid = {item["question_id"]: item for item in result.get("answers", [])}

    questions_out = []
    for idx, q in enumerate(ordered, 1):
        hit = by_qid.get(q["id"])
        attempt = latest.get(q["id"])
        questions_out.append({
            "no": idx,
            "question_id": q["id"],
            "question_type": q["question_type"],
            "question_text": (q["parsed_question"] or q["original_text"] or "").strip(),
            "recognized_answer": hit["answer"] if hit else "",
            "confidence": hit["confidence"] if hit else "",
            "page": hit["page"] if hit else None,
            "existing_answer": (attempt.student_answer if attempt else "") or "",
        })

    recognized = len([q for q in questions_out if q["recognized_answer"]])
    return {
        "images": saved_paths,
        "questions": questions_out,
        "total": len(questions_out),
        "recognized_count": recognized,
        "missing_count": len(questions_out) - recognized,
        "empty_nos": [q["no"] for q in questions_out if not q["recognized_answer"]],
        "pages": result.get("pages", []),
        "notes": result.get("notes", []),
        "provider": result.get("provider", ""),
        "model": result.get("model", ""),
        "message": f"共 {len(questions_out)} 题，识别到手写作答 {recognized} 题"
                   + (f"，{len(questions_out) - recognized} 题未识别到（可手动补充）" if recognized < len(questions_out) else ""),
    }


@router.post("/{practice_set_id}/photo-submit")
def photo_submit(
    practice_set_id: int,
    data: PhotoSubmitRequest,
    db: Session = Depends(get_db),
):
    """线下做题拍照交卷：保存手写作答 → （默认）AI 自动批改 → 判错派生错题、更新正确率"""
    ps = db.query(PracticeSet).filter(
        PracticeSet.id == practice_set_id,
        PracticeSet.deleted == False,
    ).first()
    if not ps:
        raise HTTPException(status_code=404, detail="练习集不存在")

    pairs = load_practice_questions(db, practice_set_id)
    if not pairs:
        raise HTTPException(status_code=400, detail="练习集没有题目")

    answer_map = {a.question_id: a.answer for a in data.answers if (a.answer or "").strip()}
    saved = save_student_answers(db, practice_set_id, ps.user_id, pairs, answer_map) if answer_map else 0

    ps.reviewed = True
    ps.review_count += 1
    ps.last_reviewed_at = datetime.now()
    if data.images:
        ps.review_images = json.dumps(data.images, ensure_ascii=False)

    subject = db.query(Subject).filter(Subject.id == ps.subject_id).first()

    graded_by = "manual"
    results_list: List[dict] = []
    unsupported: List[dict] = []

    if data.question_results:
        results_list = data.question_results
    elif data.auto_grade:
        latest = practice_flow.latest_attempt_map(db, practice_set_id)
        items = []
        for _psq, question in pairs:
            qid = question.id
            question_text = question.parsed_question or question.original_text or ""
            is_image_only = (not question_text) and bool(question.original_images)
            if not question_text or is_image_only:
                unsupported.append({"question_id": qid, "reason": "图片题暂不支持AI批改，请人工批改"})
                continue
            attempt = latest.get(qid)
            student_answer = (attempt.student_answer if attempt else "") or answer_map.get(qid, "")
            items.append({
                "question_id": qid,
                "question": question_text,
                "answer": question.answer or "",
                "student_answer": (student_answer or "").strip() or "（未作答）",
            })
        if items:
            from app.services.llm import llm_service
            graded = llm_service.grade_answers(items, subject=subject.name if subject else "")
            if graded.get("error"):
                db.rollback()
                raise HTTPException(status_code=502, detail=graded["error"])
            results_list = graded.get("results", [])
            # 兜底：模型若返回的是位置序号导致一个都对不上，按提交顺序映射回真实题号
            valid_ids = {q.id for _psq, q in pairs}
            if results_list and not any(r.get("question_id") in valid_ids for r in results_list):
                results_list = [
                    dict(r, question_id=items[pos]["question_id"] if pos < len(items) else None)
                    for pos, r in enumerate(results_list)
                ]
            graded_by = "ai"

    correct_count, graded_count = apply_question_results(
        db, ps, pairs, results_list, graded_by=graded_by
    )
    ps.accuracy = round(correct_count / graded_count * 100, 1) if graded_count else None

    db.commit()

    from app.services.motivation import MotivationService
    try:
        service = MotivationService(db)
        service.trigger_action("review_practice_set", user_id=ps.user_id, reason="线下做题拍照交卷")
    except Exception:
        pass  # 激励系统不影响主流程

    wrong_ids = [r.get("question_id") for r in results_list if r.get("is_correct") is False]
    return {
        "message": "交卷完成",
        "saved_answers": saved,
        "graded": graded_count,
        "total": len(pairs),
        "correct": correct_count,
        "wrong": len(wrong_ids),
        "accuracy": ps.accuracy,
        "results": results_list,
        "unsupported": unsupported,
        "wrong_question_ids": wrong_ids,
        "graded_by": graded_by,
    }


@router.post("/{practice_set_id}/mark-reviewed")
def mark_reviewed(
    practice_set_id: int,
    images: Optional[str] = Form(None),
    is_all_correct: Optional[bool] = Form(None),
    question_results: Optional[str] = Body(None),
    db: Session = Depends(get_db)
):
    """标记练习集为已复习，支持整体批改或逐题批改"""
    ps = db.query(PracticeSet).filter(
        PracticeSet.id == practice_set_id,
        PracticeSet.deleted == False
    ).first()

    if not ps:
        raise HTTPException(status_code=404, detail="练习集不存在")

    now = datetime.now()

    # 解析题目结果
    results_list = []
    if question_results:
        import json
        results_list = json.loads(question_results)

    # 更新练习集
    ps.reviewed = True
    ps.review_count += 1
    ps.last_reviewed_at = now
    if images:
        ps.review_images = images

    if ps.source_type == "reading":
        # reading 类型：直接从 question_results 计算正确率
        correct_count = sum(1 for r in results_list if r.get('is_correct'))
        total_count = len(results_list)
        if total_count > 0:
            ps.accuracy = round(correct_count / total_count * 100, 1)
        else:
            ps.accuracy = None
    else:
        # 逐题批改：写作答记录 → 判错派生错题 → 同步错题缓存列
        pairs = load_practice_questions(db, practice_set_id)
        correct_count, graded = apply_question_results(
            db, ps, pairs, results_list, graded_by="manual", is_all_correct=is_all_correct
        )

        # 计算并保存整体正确率（分母为本次实际批改的题数）
        ps.accuracy = round(correct_count / graded * 100, 1) if graded else None

    db.commit()

    # 触发积分行为
    from app.services.motivation import MotivationService
    try:
        service = MotivationService(db)
        service.trigger_action("review_practice_set", user_id=ps.user_id, reason="复习练习集")
    except Exception:
        pass  # 激励系统不影响主流程

    return {"message": "已标记为复习", "review_count": ps.review_count, "accuracy": ps.accuracy}


class BatchDeleteRequest(BaseModel):
    """批量删除请求"""
    ids: List[int]


@router.post("/batch-delete")
def batch_delete_practice_sets(
    data: BatchDeleteRequest,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin),
):
    """批量删除练习集
    家长认证：学生（child）不能删除练习，必须家长（admin）操作
    """
    if not data.ids:
        raise HTTPException(status_code=400, detail="ID列表为空")

    deleted_count = db.query(PracticeSet).filter(
        PracticeSet.id.in_(data.ids),
        PracticeSet.deleted == False
    ).update({"deleted": True}, synchronize_session=False)

    db.commit()

    return {
        "success": True,
        "deleted_count": deleted_count,
        "total": len(data.ids)
    }


@router.post("/batch-download-pdf")
def batch_download_pdf(data: BatchDeleteRequest, db: Session = Depends(get_db)):
    """批量下载练习集PDF（返回PDF链接列表）"""
    if not data.ids:
        raise HTTPException(status_code=400, detail="ID列表为空")

    results = []
    for ps_id in data.ids:
        ps = db.query(PracticeSet).filter(
            PracticeSet.id == ps_id,
            PracticeSet.deleted == False
        ).first()

        if ps and ps.pdf_path:
            results.append({
                "id": ps.id,
                "name": ps.name,
                "pdf_url": f"/uploads/{ps.pdf_path}"
            })
        elif ps:
            results.append({
                "id": ps.id,
                "name": ps.name,
                "pdf_url": None,
                "error": "PDF未生成"
            })
        else:
            results.append({
                "id": ps_id,
                "pdf_url": None,
                "error": "练习集不存在"
            })

    return {"results": results}


@router.delete("/{practice_set_id}", status_code=204)
def delete_practice_set(
    practice_set_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin),
):
    """删除练习集（软删除）；单词练习会回滚对应单词的复习计数
    家长认证：学生（child）不能删除练习，必须家长（admin）操作
    """
    ps = db.query(PracticeSet).filter(
        PracticeSet.id == practice_set_id,
        PracticeSet.deleted == False
    ).first()

    if not ps:
        raise HTTPException(status_code=404, detail="练习集不存在")

    # 单词练习：回滚单词复习计数，避免已删除练习继续计入复习统计
    if ps.source_type == "word":
        _revert_word_review_for_practice(ps, db)

    # 练习题目快照随卷软删除；作答记录（practice_attempt）**保留**，统计不因删卷丢失
    pq_ids = [
        row.practice_question_id
        for row in db.query(PracticeSetQuestion.practice_question_id)
        .filter(PracticeSetQuestion.practice_set_id == ps.id)
        .all()
        if row.practice_question_id
    ]
    if pq_ids:
        db.query(PracticeQuestion).filter(
            PracticeQuestion.id.in_(pq_ids),
        ).update({"deleted": True}, synchronize_session=False)

    ps.deleted = True
    db.commit()


def _revert_word_review_for_practice(ps, db):
    """根据练习关联的场次记录，回滚单词 review_count/correct_count，并软删除对应日志"""
    import json
    from datetime import timedelta
    from app.models import Word, WordReviewLog

    sessions = (
        db.query(WordReviewSession)
        .filter(WordReviewSession.practice_set_id == ps.id)
        .all()
    )
    for session in sessions:
        results = []
        if session.word_results:
            try:
                results = json.loads(session.word_results)
            except Exception:
                results = []
        # 旧数据无 word_results 时，按时间窗近似回滚
        if not results:
            continue
        for item in results:
            word_id = item.get("word_id")
            is_correct = bool(item.get("is_correct"))
            if not word_id:
                continue
            word = db.query(Word).filter(Word.id == word_id).first()
            if not word:
                continue
            word.review_count = max(0, (word.review_count or 0) - 1)
            if is_correct:
                word.correct_count = max(0, (word.correct_count or 0) - 1)
            # 软删除该场次时间附近的一条匹配日志
            start = session.reviewed_at - timedelta(minutes=2)
            end = session.reviewed_at + timedelta(hours=3)
            log = (
                db.query(WordReviewLog)
                .filter(
                    WordReviewLog.word_id == word_id,
                    WordReviewLog.deleted == False,
                    WordReviewLog.reviewed_at >= start,
                    WordReviewLog.reviewed_at <= end,
                    WordReviewLog.is_correct == is_correct,
                )
                .order_by(WordReviewLog.reviewed_at.desc())
                .first()
            )
            if log:
                log.deleted = True




# ============================================================ 语法专项练习卷
# 教程页「语法专项练习」：按语法点出题 → source_type='grammar' + grammar_lesson_id
class GrammarPracticeRequest(BaseModel):
    lesson_id: int
    count: int = 6
    difficulty: Optional[int] = None
    question_types: List[str] = []  # 语法题适用：choice/fill/judge/sentence；空=混合
    show_score: bool = True
    score_mode: str = "hundred"
    show_ai_author: bool = False


@router.post("/generate-grammar", response_model=PracticeSetResponse, status_code=201)
def generate_practice_from_grammar(
    data: GrammarPracticeRequest,
    db: Session = Depends(get_db),
    kid_id: Optional[int] = Depends(get_required_kid_id),
):
    """语法专项练习：按语法点标题出题组卷，卷名突出「语法·XX·专项练习」"""
    from app.models.grammar import GrammarLesson

    lesson = db.query(GrammarLesson).filter(
        GrammarLesson.id == data.lesson_id,
        GrammarLesson.deleted == False,  # noqa: E712
    ).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="语法点不存在")

    VALID_GRAMMAR_TYPES = {"choice", "fill", "judge", "sentence"}
    question_types = [t for t in data.question_types if t in VALID_GRAMMAR_TYPES]
    if data.count < 1 or data.count > 20:
        raise HTTPException(status_code=400, detail="题数需在 1-20 之间")
    if data.difficulty is not None and (data.difficulty < 1 or data.difficulty > 5):
        raise HTTPException(status_code=400, detail="难度需在 1-5 之间")

    from app.services.llm import llm_service
    result = llm_service.generate_questions_by_knowledge(
        knowledge_points=[lesson.title],
        subject="英语",
        grade=lesson.grade,
        count=data.count,
        difficulty=data.difficulty,
        question_types=question_types,
        question_categories=["basic", "scene"],
    )
    if result.get("error"):
        raise HTTPException(status_code=502, detail=result["error"])
    ai_questions = result.get("questions", [])
    if not ai_questions:
        raise HTTPException(status_code=502, detail="AI 没有生成可用题目")

    TYPE_ORDER = {"choice": 1, "fill": 2, "judge": 3, "sentence": 4}
    ai_questions.sort(key=lambda q: TYPE_ORDER.get(q.get("question_type") or "", 99))

    new_questions = []
    for item in ai_questions:
        pq = practice_flow.snapshot_from_ai_item(
            db, item,
            user_id=kid_id,
            subject_id=lesson.subject_id,
            grade=lesson.grade,
            question_types=question_types,
            question_categories=["basic", "scene"],
            default_knowledge_point=lesson.title,
        )
        if pq is not None:  # 自检拒绝的不合格题不入库
            new_questions.append(pq)

    practice_set = PracticeSet(
        name=f"语法·{lesson.title}·专项练习·{len(new_questions)}题"[:200],
        subject_id=lesson.subject_id,
        user_id=kid_id,
        source_type="grammar",
        question_type="original",
        total_questions=len(new_questions),
        show_score=data.show_score,
        score_mode=data.score_mode,
        show_ai_author=data.show_ai_author,
        grammar_lesson_id=lesson.id,
    )
    db.add(practice_set)
    db.flush()
    for idx, question in enumerate(new_questions):
        db.add(PracticeSetQuestion(
            practice_set_id=practice_set.id,
            practice_question_id=question.id,
            display_order=idx,
        ))

    pdf_url = None
    try:
        questions_data = [{
            "question_text": q.parsed_question or q.original_text or "",
            "difficulty": q.difficulty or 3,
            "id": q.id,
            "knowledge_point": q.knowledge_point or "",
            "error_type": q.error_type or "",
            "question_type": q.question_type or "",
        } for q in new_questions]
        pdf_path = generate_practice_set_pdf(
            practice_set.name, questions_data,
            show_score=practice_set.show_score,
            score_mode=practice_set.score_mode,
            created_at=practice_set.created_at,
            subject_name="英语",
            grade_label=AI_GRADE_LABELS.get(lesson.grade) if lesson.grade else None,
            show_ai_author=bool(practice_set.show_ai_author),
        )
        practice_set.pdf_path = pdf_path
        pdf_url = f"/uploads/{pdf_path}"
    except Exception as e:
        print(f"语法专项 PDF生成失败: {e}")

    db.commit()
    db.refresh(practice_set)

    return {
        "id": practice_set.id,
        "name": practice_set.name,
        "subject_id": practice_set.subject_id,
        "subject_name": "英语",
        "source_type": "grammar",
        "question_type": "original",
        "total_questions": len(new_questions),
        "reviewed": False,
        "review_count": 0,
        "pdf_path": practice_set.pdf_path,
        "created_at": practice_set.created_at,
        "questions": [],
        "pdf_url": pdf_url,
        "show_score": bool(practice_set.show_score),
        "score_mode": practice_set.score_mode or "hundred",
        "total_score": sum(compute_question_scores(
            [{"question_type": q.get("question_type") or ""} for q in questions_data],
            practice_set.score_mode or "hundred")),
        "show_ai_author": bool(practice_set.show_ai_author),
        "grammar_lesson_id": practice_set.grammar_lesson_id,
    }
