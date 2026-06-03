from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, Integer
from app.database import get_db
from app.models import Question, Subject, ErrorBook, Word, WordReviewLog, PracticeSet, PracticeSetQuestion
from app.schemas import StatsResponse, SubjectStats, GradeStats, SemesterStats, WordStats, AccuracyCurvePoint, TodayStats, LearningOverview
from datetime import datetime, timedelta

router = APIRouter(prefix="/api/stats", tags=["统计"])


@router.get("/summary", response_model=StatsResponse)
def get_stats_summary(db: Session = Depends(get_db)):
    """获取统计概览（只统计未删除的记录）"""
    total_questions = db.query(func.count(Question.id)).filter(Question.deleted == False).scalar()
    to_review_questions = db.query(func.count(Question.id)).filter(
        Question.deleted == False,
        (Question.review_count == 0) | (Question.review_count.is_(None)) |
        ((Question.review_count > 0) & (Question.correct_count == 0))
    ).scalar() or 0
    total_subjects = db.query(func.count(Subject.id)).filter(Subject.deleted == False).scalar()
    total_error_books = db.query(func.count(ErrorBook.id)).filter(ErrorBook.deleted == False).scalar()

    difficulty_query = (
        db.query(Question.difficulty, func.count(Question.id))
        .filter(Question.deleted == False)
        .group_by(Question.difficulty)
        .all()
    )
    difficulty_distribution = {str(k): v for k, v in difficulty_query}

    error_type_query = (
        db.query(Question.error_type)
        .filter(Question.deleted == False, Question.error_type.isnot(None))
        .all()
    )
    error_type_counts = {}
    for (et,) in error_type_query:
        if et:
            for single_et in et.split(','):
                single_et = single_et.strip()
                if single_et:
                    error_type_counts[single_et] = error_type_counts.get(single_et, 0) + 1
    error_type_distribution = error_type_counts

    subject_query = (
        db.query(Subject.id, Subject.name, func.count(Question.id))
        .join(Question, Subject.id == Question.subject_id)
        .filter(Subject.deleted == False, Question.deleted == False)
        .group_by(Subject.id, Subject.name)
        .all()
    )

    by_subject = []
    for subject_id, subject_name, question_count in subject_query:
        error_counts = (
            db.query(Question.error_type, func.count(Question.id))
            .filter(Question.subject_id == subject_id, Question.deleted == False, Question.error_type.isnot(None))
            .group_by(Question.error_type)
            .all()
        )
        error_type_counts = {}
        for (et, count) in error_counts:
            if et:
                for single_et in et.split(','):
                    single_et = single_et.strip()
                    if single_et:
                        error_type_counts[single_et] = error_type_counts.get(single_et, 0) + count

        difficulty_counts = (
            db.query(Question.difficulty, func.count(Question.id))
            .filter(Question.subject_id == subject_id, Question.deleted == False)
            .group_by(Question.difficulty)
            .all()
        )
        difficulty_dist = {str(k): v for k, v in difficulty_counts}

        kp_counts = (
            db.query(Question.knowledge_point, func.count(Question.id))
            .filter(Question.subject_id == subject_id, Question.deleted == False, Question.knowledge_point.isnot(None))
            .group_by(Question.knowledge_point)
            .all()
        )
        knowledge_point_counts = {k: v for k, v in kp_counts if k}

        practice_count = db.query(func.count(PracticeSet.id)).filter(
            PracticeSet.subject_id == subject_id, PracticeSet.deleted == False
        ).scalar() or 0

        by_subject.append(SubjectStats(
            subject_id=subject_id,
            subject_name=subject_name,
            question_count=question_count,
            error_type_counts=error_type_counts,
            difficulty_distribution=difficulty_dist,
            knowledge_point_counts=knowledge_point_counts,
            practice_count=practice_count,
        ))

    grade_query = (
        db.query(Question.grade, func.count(Question.id))
        .filter(Question.deleted == False)
        .group_by(Question.grade)
        .all()
    )
    by_grade = []
    for grade, count in grade_query:
        if grade is not None:
            diff_counts = (
                db.query(Question.difficulty, func.count(Question.id))
                .filter(Question.deleted == False, Question.grade == grade)
                .group_by(Question.difficulty)
                .all()
            )
            by_grade.append(GradeStats(grade=grade, question_count=count, difficulty_distribution={str(k): v for k, v in diff_counts}))

    semester_query = (
        db.query(Question.semester, func.count(Question.id))
        .filter(Question.deleted == False)
        .group_by(Question.semester)
        .all()
    )
    by_semester = []
    for semester, count in semester_query:
        if semester is not None:
            diff_counts = (
                db.query(Question.difficulty, func.count(Question.id))
                .filter(Question.deleted == False, Question.semester == semester)
                .group_by(Question.difficulty)
                .all()
            )
            by_semester.append(SemesterStats(semester=semester, question_count=count, difficulty_distribution={str(k): v for k, v in diff_counts}))

    total_words = db.query(func.count(Word.id)).filter(Word.deleted == False).scalar() or 0
    reviewed_words = db.query(func.count(Word.id)).filter(Word.deleted == False, Word.review_count > 0).scalar() or 0
    total_reviews = db.query(func.sum(Word.review_count)).filter(Word.deleted == False).scalar() or 0
    total_correct = db.query(func.sum(Word.correct_count)).filter(Word.deleted == False).scalar() or 0
    word_accuracy = round(total_correct / total_reviews * 100, 1) if total_reviews > 0 else 0.0
    to_review_count = db.query(func.count(Word.id)).filter(
        Word.deleted == False,
        (Word.next_review_at == None) | (Word.next_review_at <= datetime.now())
    ).scalar() or 0

    word_stats = WordStats(
        total_words=total_words,
        reviewed_words=reviewed_words,
        total_reviews=total_reviews,
        accuracy=word_accuracy,
        to_review_count=to_review_count,
    )

    thirty_days_ago = datetime.now() - timedelta(days=30)
    word_logs = (
        db.query(WordReviewLog.reviewed_at, WordReviewLog.is_correct)
        .filter(WordReviewLog.deleted == False, WordReviewLog.reviewed_at >= thirty_days_ago)
        .order_by(WordReviewLog.reviewed_at)
        .all()
    )
    daily_word = {}
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

    active_days_query = db.query(func.count(func.distinct(func.date(Question.created_at)))).filter(Question.deleted == False).scalar() or 0
    active_days = active_days_query

    return StatsResponse(
        total_questions=total_questions,
        total_subjects=total_subjects,
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
def get_today_stats(db: Session = Depends(get_db)):
    """获取今日学习统计"""
    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)

    from app.models import WordReviewSession
    word_sessions = db.query(WordReviewSession).filter(
        WordReviewSession.reviewed_at >= today_start,
        WordReviewSession.reviewed_at < today_end
    ).all()

    today_word_review_count = sum(s.total_count for s in word_sessions)
    today_word_correct = sum(s.correct_count for s in word_sessions)
    today_word_accuracy = round(today_word_correct / today_word_review_count * 100, 1) if today_word_review_count > 0 else 0.0

    question_sets = db.query(PracticeSet).filter(
        PracticeSet.source_type == 'question',
        PracticeSet.last_reviewed_at >= today_start,
        PracticeSet.last_reviewed_at < today_end,
        PracticeSet.deleted == False
    ).all()

    question_ids_set = set()
    question_correct_count = 0
    for ps in question_sets:
        questions = db.query(PracticeSetQuestion).filter(
            PracticeSetQuestion.practice_set_id == ps.id,
            PracticeSetQuestion.question_id.isnot(None),
            PracticeSetQuestion.is_correct.isnot(None)
        ).all()
        for q in questions:
            question_ids_set.add(q.question_id)
            if q.is_correct:
                question_correct_count += 1

    today_question_review_count = len(question_ids_set)
    today_question_accuracy = round(question_correct_count / today_question_review_count * 100, 1) if today_question_review_count > 0 else 0.0

    return TodayStats(
        today_word_review_count=today_word_review_count,
        today_question_review_count=today_question_review_count,
        today_word_accuracy=today_word_accuracy,
        today_question_accuracy=today_question_accuracy,
    )


def get_date_stats(db, date_start, date_end):
    """获取指定日期范围的统计数据"""
    from app.models import PracticeSet, PracticeSetQuestion, WordReviewSession

    practice_sets = db.query(PracticeSet).filter(
        PracticeSet.deleted == False,
        PracticeSet.created_at >= date_start,
        PracticeSet.created_at < date_end
    ).all()

    word_sessions = db.query(WordReviewSession).filter(
        WordReviewSession.reviewed_at >= date_start,
        WordReviewSession.reviewed_at < date_end
    ).all()

    word_review_count = sum(s.total_count for s in word_sessions)
    word_correct = sum(s.correct_count for s in word_sessions)
    word_accuracy = round(word_correct / word_review_count * 100, 1) if word_review_count > 0 else 0.0

    question_sets = [ps for ps in practice_sets if ps.source_type == 'question']
    question_ids_set = set()
    question_correct_count = 0
    for ps in question_sets:
        questions = db.query(PracticeSetQuestion).filter(
            PracticeSetQuestion.practice_set_id == ps.id,
            PracticeSetQuestion.question_id.isnot(None),
            PracticeSetQuestion.is_correct.isnot(None)
        ).all()
        for q in questions:
            question_ids_set.add(q.question_id)
            if q.is_correct:
                question_correct_count += 1

    question_review_count = len(question_ids_set)
    question_accuracy = round(question_correct_count / question_review_count * 100, 1) if question_review_count > 0 else 0.0

    return {
        'word_review_count': word_review_count,
        'question_review_count': question_review_count,
        'word_accuracy': word_accuracy,
        'question_accuracy': question_accuracy,
    }


@router.get("/overview", response_model=LearningOverview)
def get_learning_overview(db: Session = Depends(get_db)):
    """获取学习概览（昨日 + 今日数据）"""
    from datetime import datetime, timedelta

    today_start = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    today_end = today_start + timedelta(days=1)
    yesterday_start = today_start - timedelta(days=1)
    yesterday_end = today_start

    yesterday = get_date_stats(db, yesterday_start, yesterday_end)
    today = get_date_stats(db, today_start, today_end)

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
def get_knowledge_point_stats(db: Session = Depends(get_db)):
    """获取知识点掌握统计"""
    results = (
        db.query(
            Question.knowledge_point,
            func.count(Question.id).label('total'),
            func.sum(func.cast(Question.review_count > 0, Integer)).label('reviewed'),
            func.sum(Question.correct_count).label('total_correct'),
            func.sum(Question.review_count).label('total_reviews'),
            func.sum(Question.error_count).label('total_errors'),
        )
        .filter(
            Question.deleted == False,
            Question.knowledge_point.isnot(None),
            Question.knowledge_point != '',
        )
        .group_by(Question.knowledge_point)
        .all()
    )
    data = []
    for r in results:
        reviews = int(r.total_reviews or 0)
        correct = int(r.total_correct or 0)
        accuracy = round(correct / reviews * 100, 1) if reviews > 0 else 0
        data.append({
            "name": r.knowledge_point,
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
def get_full_analysis(db: Session = Depends(get_db)):
    """获取完整学习分析数据"""
    service = LearningAnalysisService(db)
    return service.get_full_stats()


@router.post("/analysis/llm")
def get_llm_analysis(db: Session = Depends(get_db)):
    """获取LLM学习分析"""
    try:
        service = LearningAnalysisService(db)
        stats = service.get_full_stats()
        analysis = service.analyze_with_llm(stats)
        return analysis
    except Exception as e:
        return {"error": f"获取LLM分析失败: {str(e)}"}
