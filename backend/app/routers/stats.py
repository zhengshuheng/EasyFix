from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func, Integer, or_
from typing import Optional
import json
from app.database import get_db
from app.models import ErrorQuestion, Subject, ErrorBook, Word, WordProgress, WordReviewLog, PracticeSet, PracticeSetQuestion
from app.models.practice_attempt import PracticeAttempt
from app.utils.kid_context import get_current_kid_id
from app.schemas import StatsResponse, SubjectStats, GradeStats, SemesterStats, WordStats, AccuracyCurvePoint, TodayStats, LearningOverview
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/stats", tags=["统计"])


def _kid(q, kid_id: Optional[int], model=ErrorQuestion):
    """按当前小孩过滤统计（家长未选小孩时不过滤 = 全部）"""
    return q if kid_id is None else q.filter(model.user_id == kid_id)


def _word_grade_ok(grade: Optional[int]):
    """单词年级过滤：NULL 年级=通用词，任何年级空间都计入。

    词表年级标注经常缺失/不精确，若硬按 `Word.grade == grade` 会把通用词
    全部排除，导致首页/分析的单词进度、正确率、曲线全空。
    """
    if grade is None:
        return None
    return or_(Word.grade == grade, Word.grade.is_(None))


def is_english_subject(db: Session, subject_id: Optional[int]) -> bool:
    """学科是否英语（单词数据只属于英语学科；无学科过滤时视为英语保留）"""
    if subject_id is None:
        return True
    s = db.query(Subject).filter(Subject.id == subject_id).first()
    if not s:
        return False
    name = (s.name or "").lower()
    return "英语" in name or "english" in name


@router.get("/summary", response_model=StatsResponse)
def get_stats_summary(
    grade: Optional[int] = Query(None, ge=1, le=12, description="按年级过滤，不区分学期"),
    subject_id: Optional[int] = Query(None, description="按学科过滤（学习空间指定学科时）"),
    db: Session = Depends(get_db),
    kid_id: Optional[int] = Depends(get_current_kid_id),
):
    """获取统计概览（只统计未删除的记录；不含 AI 出题生成的练习题；按孩子/年级/学科过滤）"""
    q_base = _kid(
        db.query(ErrorQuestion).filter(
            ErrorQuestion.deleted == False,  # noqa: E712
            ErrorQuestion.source != 'ai',
        ),
        kid_id,
    )
    w_base = db.query(Word).filter(Word.deleted == False)
    if grade is not None:
        q_base = q_base.filter(ErrorQuestion.grade == grade)
        w_base = w_base.filter(_word_grade_ok(grade))
    if subject_id is not None:
        q_base = q_base.filter(ErrorQuestion.subject_id == subject_id)
        # 单词无学科字段：仅英语学科保留单词统计，其他学科置空
        if not is_english_subject(db, subject_id):
            w_base = w_base.filter(Word.id == -1)

    total_questions = q_base.count()
    to_review_questions = q_base.filter(
        (ErrorQuestion.review_count == 0) | (ErrorQuestion.review_count.is_(None)) |
        ((ErrorQuestion.review_count > 0) & (ErrorQuestion.correct_count == 0))
    ).count() or 0
    total_subjects = db.query(func.count(Subject.id)).filter(Subject.deleted == False).scalar()
    total_error_books = _kid(db.query(func.count(ErrorBook.id)).filter(ErrorBook.deleted == False), kid_id, ErrorBook).scalar()  # noqa: E712

    difficulty_query = (
        db.query(ErrorQuestion.difficulty, func.count(ErrorQuestion.id))
        .filter(ErrorQuestion.deleted == False, ErrorQuestion.source != 'ai')
    )
    if grade is not None:
        difficulty_query = difficulty_query.filter(ErrorQuestion.grade == grade)
    if subject_id is not None:
        difficulty_query = difficulty_query.filter(ErrorQuestion.subject_id == subject_id)
    difficulty_query = _kid(difficulty_query, kid_id).group_by(ErrorQuestion.difficulty).all()
    difficulty_distribution = {str(k): v for k, v in difficulty_query}

    error_type_query = (
        db.query(ErrorQuestion.error_type)
        .filter(ErrorQuestion.deleted == False, ErrorQuestion.error_type.isnot(None))
    )
    if grade is not None:
        error_type_query = error_type_query.filter(ErrorQuestion.grade == grade)
    if subject_id is not None:
        error_type_query = error_type_query.filter(ErrorQuestion.subject_id == subject_id)
    error_type_counts = {}
    for (et,) in _kid(error_type_query, kid_id).all():
        if et:
            for single_et in et.split(','):
                single_et = single_et.strip()
                if single_et:
                    error_type_counts[single_et] = error_type_counts.get(single_et, 0) + 1
    error_type_distribution = error_type_counts

    subject_query = (
        db.query(Subject.id, Subject.name, func.count(ErrorQuestion.id))
        .join(ErrorQuestion, Subject.id == ErrorQuestion.subject_id)
        .filter(Subject.deleted == False, ErrorQuestion.deleted == False)
    )
    if grade is not None:
        subject_query = subject_query.filter(ErrorQuestion.grade == grade)
    if subject_id is not None:
        subject_query = subject_query.filter(Subject.id == subject_id)
    subject_query = _kid(subject_query, kid_id).group_by(Subject.id, Subject.name).all()

    by_subject = []
    for sid, subject_name, question_count in subject_query:
        error_counts = (
            db.query(ErrorQuestion.error_type, func.count(ErrorQuestion.id))
            .filter(ErrorQuestion.subject_id == sid, ErrorQuestion.deleted == False, ErrorQuestion.error_type.isnot(None))
        )
        if grade is not None:
            error_counts = error_counts.filter(ErrorQuestion.grade == grade)
        error_counts = _kid(error_counts, kid_id).group_by(ErrorQuestion.error_type).all()
        error_type_counts = {}
        for (et, count) in error_counts:
            if et:
                for single_et in et.split(','):
                    single_et = single_et.strip()
                    if single_et:
                        error_type_counts[single_et] = error_type_counts.get(single_et, 0) + count

        difficulty_counts = (
            db.query(ErrorQuestion.difficulty, func.count(ErrorQuestion.id))
            .filter(ErrorQuestion.subject_id == sid, ErrorQuestion.deleted == False)
        )
        if grade is not None:
            difficulty_counts = difficulty_counts.filter(ErrorQuestion.grade == grade)
        difficulty_counts = _kid(difficulty_counts, kid_id).group_by(ErrorQuestion.difficulty).all()
        difficulty_dist = {str(k): v for k, v in difficulty_counts}

        kp_counts = (
            db.query(ErrorQuestion.knowledge_point, func.count(ErrorQuestion.id))
            .filter(ErrorQuestion.subject_id == sid, ErrorQuestion.deleted == False, ErrorQuestion.knowledge_point.isnot(None))
        )
        if grade is not None:
            kp_counts = kp_counts.filter(ErrorQuestion.grade == grade)
        kp_counts = _kid(kp_counts, kid_id).group_by(ErrorQuestion.knowledge_point).all()
        knowledge_point_counts = {k: v for k, v in kp_counts if k}

        practice_count = _kid(db.query(func.count(PracticeSet.id)).filter(
            PracticeSet.subject_id == sid, PracticeSet.deleted == False
        ), kid_id, PracticeSet).scalar() or 0

        by_subject.append(SubjectStats(
            subject_id=sid,
            subject_name=subject_name,
            question_count=question_count,
            error_type_counts=error_type_counts,
            difficulty_distribution=difficulty_dist,
            knowledge_point_counts=knowledge_point_counts,
            practice_count=practice_count,
        ))

    # 单词按年级分布（不区分学期）
    word_grade_query = (
        db.query(Word.grade, func.count(Word.id))
        .filter(Word.deleted == False, Word.grade.isnot(None))
        .group_by(Word.grade)
        .all()
    )
    word_grade_dist = {int(g): int(c) for g, c in word_grade_query}

    grade_query = (
        db.query(ErrorQuestion.grade, func.count(ErrorQuestion.id))
        .filter(ErrorQuestion.deleted == False)
    )
    if subject_id is not None:
        grade_query = grade_query.filter(ErrorQuestion.subject_id == subject_id)
    grade_query = grade_query.group_by(ErrorQuestion.grade).all()
    by_grade = []
    covered_grades = set()
    for g, count in grade_query:
        if g is not None:
            g = int(g)
            covered_grades.add(g)
            diff_counts = (
                db.query(ErrorQuestion.difficulty, func.count(ErrorQuestion.id))
                .filter(ErrorQuestion.deleted == False, ErrorQuestion.grade == g)
            )
            if subject_id is not None:
                diff_counts = diff_counts.filter(ErrorQuestion.subject_id == subject_id)
            diff_counts = _kid(diff_counts, kid_id).group_by(ErrorQuestion.difficulty).all()
            by_grade.append(GradeStats(
                grade=g,
                question_count=count,
                word_count=word_grade_dist.get(g, 0),
                difficulty_distribution={str(k): v for k, v in diff_counts}
            ))
    for g, wc in word_grade_dist.items():
        if g not in covered_grades:
            by_grade.append(GradeStats(grade=g, question_count=0, word_count=wc, difficulty_distribution={}))
    by_grade.sort(key=lambda x: x.grade)

    semester_query = (
        db.query(ErrorQuestion.semester, func.count(ErrorQuestion.id))
        .filter(ErrorQuestion.deleted == False)
    )
    if grade is not None:
        semester_query = semester_query.filter(ErrorQuestion.grade == grade)
    if subject_id is not None:
        semester_query = semester_query.filter(ErrorQuestion.subject_id == subject_id)
    semester_query = _kid(semester_query, kid_id).group_by(ErrorQuestion.semester).all()
    by_semester = []
    for semester, count in semester_query:
        if semester is not None:
            diff_q = (
                db.query(ErrorQuestion.difficulty, func.count(ErrorQuestion.id))
                .filter(ErrorQuestion.deleted == False, ErrorQuestion.semester == semester)
            )
            if grade is not None:
                diff_q = diff_q.filter(ErrorQuestion.grade == grade)
            if subject_id is not None:
                diff_q = diff_q.filter(ErrorQuestion.subject_id == subject_id)
            diff_counts = _kid(diff_q, kid_id).group_by(ErrorQuestion.difficulty).all()
            by_semester.append(SemesterStats(semester=semester, question_count=count, difficulty_distribution={str(k): v for k, v in diff_counts}))

    total_words = w_base.count()
    reviewed_words = w_base.filter(Word.review_count > 0).count()

    include_words = is_english_subject(db, subject_id)

    # 复习次数 = 答题次数（WordReviewLog 每次答题一条，覆盖词库复习/记忆模式/练习集复习）
    total_reviews = 0
    if include_words:
        word_rev_q = db.query(func.count(WordReviewLog.id)).filter(WordReviewLog.deleted == False)
        if grade is not None:
            word_rev_q = word_rev_q.join(Word, Word.id == WordReviewLog.word_id).filter(
                Word.deleted == False, _word_grade_ok(grade)
            )
        total_reviews = _kid(word_rev_q, kid_id, WordReviewLog).scalar() or 0

    # 正确率按复习日志统计（排除已删日志；年级过滤时关联单词表）
    total_log_count = 0
    total_log_correct = 0
    if include_words:
        word_total_logs = db.query(func.count(WordReviewLog.id)).filter(WordReviewLog.deleted == False)
        word_correct_logs = db.query(func.count(WordReviewLog.id)).filter(
            WordReviewLog.deleted == False, WordReviewLog.is_correct == True
        )
        if grade is not None:
            word_total_logs = word_total_logs.join(Word, Word.id == WordReviewLog.word_id).filter(
                Word.deleted == False, _word_grade_ok(grade)
            )
            word_correct_logs = word_correct_logs.join(Word, Word.id == WordReviewLog.word_id).filter(
                Word.deleted == False, _word_grade_ok(grade)
            )
        total_log_count = _kid(word_total_logs, kid_id, WordReviewLog).scalar() or 0
        total_log_correct = _kid(word_correct_logs, kid_id, WordReviewLog).scalar() or 0
    word_accuracy = round(total_log_correct / total_log_count * 100, 1) if total_log_count > 0 else 0.0

    to_review_count = w_base.filter(
        (Word.next_review_at == None) | (Word.next_review_at <= datetime.now())
    ).count() or 0

    # 单词学习过程五维量化（按该小孩 WordProgress 维度进度统计）
    # 口径：跟读=听得维度答对过、认读=认得维度答对过、读词=说得维度练过（开口读过）、
    #       说词=说得维度答对过、听写=写得维度答对过；total=当前空间单词总数
    dim_stats = []
    if include_words:
        wp_base = _kid(db.query(WordProgress), kid_id, WordProgress)
        if grade is not None:
            wp_base = wp_base.join(Word, Word.id == WordProgress.word_id).filter(
                Word.deleted == False, _word_grade_ok(grade)
            )
        dim_defs = [
            ("listen", "跟读", WordProgress.listen_correct),
            ("recognize", "认读", WordProgress.recognize_correct),
            ("read", "读词", WordProgress.speak_count),
            ("speak", "说词", WordProgress.speak_correct),
            ("write", "听写", WordProgress.write_correct),
        ]
        for key, label, col in dim_defs:
            done = wp_base.filter(col > 0).count()
            dim_stats.append({"key": key, "label": label, "done": done, "total": total_words})

    word_stats = WordStats(
        total_words=total_words,
        reviewed_words=reviewed_words,
        total_reviews=total_reviews,
        accuracy=word_accuracy,
        to_review_count=to_review_count,
        grade_distribution={str(k): v for k, v in word_grade_dist.items()},
        dim_stats=dim_stats,
    )

    # 准确率曲线取最近 180 天（前端 halfyear 档可看全；太短会误显示"无数据"）
    curve_start = datetime.now() - timedelta(days=180)
    daily_word = {}
    if include_words:
        word_logs_q = (
            db.query(WordReviewLog.reviewed_at, WordReviewLog.is_correct)
            .filter(WordReviewLog.deleted == False, WordReviewLog.reviewed_at >= curve_start)
        )
        if grade is not None:
            word_logs_q = word_logs_q.join(Word, Word.id == WordReviewLog.word_id).filter(
                Word.deleted == False, _word_grade_ok(grade)
            )
        word_logs = _kid(word_logs_q, kid_id, WordReviewLog).order_by(WordReviewLog.reviewed_at).all()
        for log in word_logs:
            date_str = log.reviewed_at.strftime('%Y-%m-%d')
            if date_str not in daily_word:
                daily_word[date_str] = {'total': 0, 'correct': 0}
            daily_word[date_str]['total'] += 1
            if log.is_correct:
                daily_word[date_str]['correct'] += 1

    word_accuracy_curve = []
    for date_str in sorted(daily_word.keys()):
        d = daily_word[date_str]
        acc = round(d['correct'] / d['total'] * 100, 1) if d['total'] > 0 else 0
        word_accuracy_curve.append(AccuracyCurvePoint(date=date_str, accuracy=acc))

    question_accuracy_curve = []
    qa_logs = (
        db.query(PracticeAttempt.answered_at, PracticeAttempt.is_correct)
        .join(ErrorQuestion, ErrorQuestion.id == PracticeAttempt.error_question_id)
        .filter(
            PracticeAttempt.answered_at >= curve_start,
            PracticeAttempt.is_correct.isnot(None),
        )
    )
    if grade is not None:
        qa_logs = qa_logs.filter(ErrorQuestion.grade == grade)
    if subject_id is not None:
        qa_logs = qa_logs.filter(ErrorQuestion.subject_id == subject_id)
    daily_question = {}
    for log in _kid(qa_logs, kid_id, PracticeAttempt).all():
        date_str = log.answered_at.strftime('%Y-%m-%d')
        if date_str not in daily_question:
            daily_question[date_str] = {'total': 0, 'correct': 0}
        daily_question[date_str]['total'] += 1
        if log.is_correct:
            daily_question[date_str]['correct'] += 1
    for date_str in sorted(daily_question.keys()):
        d = daily_question[date_str]
        acc = round(d['correct'] / d['total'] * 100, 1) if d['total'] > 0 else 0
        question_accuracy_curve.append(AccuracyCurvePoint(date=date_str, accuracy=acc))

    active_days_query = db.query(func.count(func.distinct(func.date(ErrorQuestion.created_at)))).filter(ErrorQuestion.deleted == False)
    if grade is not None:
        active_days_query = active_days_query.filter(ErrorQuestion.grade == grade)
    if subject_id is not None:
        active_days_query = active_days_query.filter(ErrorQuestion.subject_id == subject_id)
    active_days = _kid(active_days_query, kid_id).scalar() or 0

    return StatsResponse(
        total_questions=total_questions,
        total_subjects=total_subjects if subject_id is None else 1,
        total_error_books=total_error_books,
        active_days=active_days,
        to_review_questions=to_review_questions,
        difficulty_distribution=difficulty_distribution,
        error_type_distribution=error_type_distribution,
        by_subject=by_subject,
        by_grade=by_grade,
        by_semester=by_semester,
        word_stats=word_stats,
        word_accuracy_curve=word_accuracy_curve,
        question_accuracy_curve=question_accuracy_curve,
    )


@router.get("/today", response_model=TodayStats)
def get_today_stats(
    db: Session = Depends(get_db),
    kid_id: Optional[int] = Depends(get_current_kid_id),
):
    """获取今日学习统计（按当前小孩）"""
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    today_word_logs = _kid(
        db.query(WordReviewLog).filter(
            WordReviewLog.deleted == False,  # noqa: E712
            WordReviewLog.reviewed_at >= today_start,
            WordReviewLog.reviewed_at < today_end,
        ),
        kid_id,
        WordReviewLog,
    ).all()
    today_word_review_count = len(today_word_logs)
    today_word_correct = sum(1 for l in today_word_logs if l.is_correct)
    today_word_accuracy = round(today_word_correct / today_word_review_count * 100, 1) if today_word_review_count > 0 else 0.0

    # 错题练习统计：以作答记录（practice_attempt）为事实来源
    attempt_rows = _kid(db.query(PracticeAttempt).filter(
        PracticeAttempt.answered_at >= today_start,
        PracticeAttempt.answered_at < today_end,
    ), kid_id, PracticeAttempt).all()
    question_ids_set = {a.error_question_id for a in attempt_rows if a.error_question_id}
    question_correct_count = sum(1 for a in attempt_rows if a.is_correct)

    today_question_review_count = len(question_ids_set) if question_ids_set else len(attempt_rows)
    today_question_accuracy = round(question_correct_count / len(attempt_rows) * 100, 1) if attempt_rows else 0.0

    return TodayStats(
        today_word_review_count=today_word_review_count,
        today_question_review_count=today_question_review_count,
        today_word_accuracy=today_word_accuracy,
        today_question_accuracy=today_question_accuracy,
    )


def get_date_stats(db, date_start, date_end, grade: Optional[int] = None, subject_id: Optional[int] = None, kid_id: Optional[int] = None):
    """获取指定日期范围的统计数据，可按孩子/年级/学科过滤"""
    from app.models import PracticeSet, PracticeSetQuestion

    practice_sets = _kid(db.query(PracticeSet).filter(
        PracticeSet.deleted == False,  # noqa: E712
        PracticeSet.created_at >= date_start,
        PracticeSet.created_at < date_end
    ), kid_id, PracticeSet)
    if subject_id is not None:
        practice_sets = practice_sets.filter(PracticeSet.subject_id == subject_id)
    practice_sets = practice_sets.all()

    # 单词：以 WordReviewLog（每次答题一条）为事实来源，覆盖词库复习/记忆模式/练习集复习
    include_words = is_english_subject(db, subject_id)
    if not include_words:
        word_review_count = 0
        word_correct = 0
    else:
        word_logs_q = (
            db.query(WordReviewLog.is_correct)
            .filter(
                WordReviewLog.deleted == False,  # noqa: E712
                WordReviewLog.reviewed_at >= date_start,
                WordReviewLog.reviewed_at < date_end,
            )
        )
        if grade is not None:
            word_logs_q = word_logs_q.join(Word, Word.id == WordReviewLog.word_id).filter(
                Word.deleted == False,  # noqa: E712
                _word_grade_ok(grade),
            )
        word_logs = _kid(word_logs_q, kid_id, WordReviewLog).all()
        word_review_count = len(word_logs)
        word_correct = sum(1 for (ok,) in word_logs if ok)
    word_accuracy = round(word_correct / word_review_count * 100, 1) if word_review_count > 0 else 0.0

    # 错题练习统计：以作答记录（practice_attempt）为事实来源，可按学科/年级过滤
    attempt_q = (
        db.query(PracticeAttempt)
        .join(ErrorQuestion, ErrorQuestion.id == PracticeAttempt.error_question_id)
        .filter(
            PracticeAttempt.answered_at >= date_start,
            PracticeAttempt.answered_at < date_end,
        )
    )
    if subject_id is not None:
        attempt_q = attempt_q.filter(ErrorQuestion.subject_id == subject_id)
    if grade is not None:
        attempt_q = attempt_q.filter(ErrorQuestion.grade == grade)
    attempt_rows = _kid(attempt_q, kid_id).all()

    question_ids_set = {a.error_question_id for a in attempt_rows if a.error_question_id}
    question_correct_count = sum(1 for a in attempt_rows if a.is_correct)
    question_review_count = len(question_ids_set) if question_ids_set else len(attempt_rows)
    question_accuracy = round(question_correct_count / len(attempt_rows) * 100, 1) if attempt_rows else 0.0

    return {
        'word_review_count': word_review_count,
        'question_review_count': question_review_count,
        'word_accuracy': word_accuracy,
        'question_accuracy': question_accuracy,
    }


@router.get("/overview", response_model=LearningOverview)
def get_learning_overview(
    grade: Optional[int] = Query(None, ge=1, le=12, description="按年级过滤"),
    subject_id: Optional[int] = Query(None, description="按学科过滤（学习空间指定学科时）"),
    db: Session = Depends(get_db),
    kid_id: Optional[int] = Depends(get_current_kid_id),
):
    """获取学习概览（昨日 + 今日数据，按当前小孩）"""
    from datetime import datetime, timedelta

    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)
    yesterday_start = today_start - timedelta(days=1)
    yesterday_end = today_start

    yesterday = get_date_stats(db, yesterday_start, yesterday_end, grade=grade, subject_id=subject_id, kid_id=kid_id)
    today = get_date_stats(db, today_start, today_end, grade=grade, subject_id=subject_id, kid_id=kid_id)

    return LearningOverview(
        yesterday_word_review_count=yesterday['word_review_count'],
        yesterday_question_review_count=yesterday['question_review_count'],
        yesterday_word_accuracy=yesterday['word_accuracy'],
        yesterday_question_accuracy=yesterday['question_accuracy'],
        today_word_review_count=today['word_review_count'],
        today_question_review_count=today['question_review_count'],
        today_word_accuracy=today['word_accuracy'],
        today_question_accuracy=today['question_accuracy'],
    )


@router.get("/knowledge-points")
def get_knowledge_point_stats(
    subject_id: Optional[int] = Query(None, description="按学科过滤（学习空间指定学科时）"),
    grade: Optional[int] = Query(None, ge=1, le=12, description="按年级过滤（学习空间指定年级时）"),
    db: Session = Depends(get_db),
    kid_id: Optional[int] = Depends(get_current_kid_id),
):
    """获取知识点掌握统计（按当前小孩）"""
    base_filters = [
        ErrorQuestion.deleted == False,  # noqa: E712
        ErrorQuestion.knowledge_point.isnot(None),
        ErrorQuestion.knowledge_point != '',
    ]
    if kid_id is not None:
        base_filters.append(ErrorQuestion.user_id == kid_id)
    if subject_id is not None:
        base_filters.append(ErrorQuestion.subject_id == subject_id)
    if grade is not None:
        base_filters.append(ErrorQuestion.grade == grade)
    results = (
        db.query(
            ErrorQuestion.knowledge_point,
            func.count(ErrorQuestion.id).label('total'),
            func.sum(func.cast(ErrorQuestion.review_count > 0, Integer)).label('reviewed'),
            func.sum(ErrorQuestion.correct_count).label('total_correct'),
            func.sum(ErrorQuestion.review_count).label('total_reviews'),
            func.sum(ErrorQuestion.wrong_count).label('total_errors'),
            ErrorQuestion.subject_id,
            Subject.name.label('subject_name'),
        )
        .outerjoin(Subject, Subject.id == ErrorQuestion.subject_id)
        .filter(*base_filters)
        .group_by(ErrorQuestion.knowledge_point, ErrorQuestion.subject_id, Subject.name)
        .all()
    )
    data = []
    for r in results:
        reviews = int(r.total_reviews or 0)
        correct = int(r.total_correct or 0)
        accuracy = round(correct / reviews * 100, 1) if reviews > 0 else 0
        data.append({
            "name": r.knowledge_point,
            "subject_id": r.subject_id,
            "subject_name": r.subject_name or '未分类',
            "total": int(r.total or 0),
            "reviewed": int(r.reviewed or 0),
            "accuracy": accuracy,
            "total_reviews": reviews,
            "total_errors": int(r.total_errors or 0),
        })
    data.sort(key=lambda x: x['total'], reverse=True)
    return data


from app.services.learning_analysis import LearningAnalysisService

@router.get("/analysis/full")
def get_full_analysis(
    subject_id: Optional[int] = Query(None, description="按学科过滤（学习空间指定学科时）"),
    grade: Optional[int] = Query(None, ge=1, le=12, description="按年级过滤（学习空间指定年级时）"),
    db: Session = Depends(get_db),
    kid_id: Optional[int] = Depends(get_current_kid_id),
):
    """获取完整学习分析数据（按当前小孩）"""
    service = LearningAnalysisService(db, subject_id=subject_id, grade=grade, user_id=kid_id)
    return service.get_full_stats()


@router.post("/analysis/llm")
def get_llm_analysis(
    db: Session = Depends(get_db),
    kid_id: Optional[int] = Depends(get_current_kid_id),
):
    """获取LLM学习分析"""
    try:
        service = LearningAnalysisService(db, user_id=kid_id)
        stats = service.get_full_stats()
        analysis = service.analyze_with_llm(stats)
        return analysis
    except Exception as e:
        return {"error": f"获取LLM分析失败: {str(e)}"}
