from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session, joinedload
from typing import Optional, List
import json
from datetime import datetime
from app.database import get_db
from app.models import Question, Tag, QuestionTag, ErrorQuestion, SimilarQuestion
from app.models.practice_set import PracticeSetQuestion, PracticeSet
from app.models.practice_question import PracticeQuestion
from app.models.practice_attempt import PracticeAttempt
from app.models.assessment import AssessmentRecord
from app.models.operation_log import OperationType
from app.models.user import User
from app.schemas import QuestionCreate, QuestionUpdate, QuestionResponse, QuestionListResponse, QuestionBatchCreate, BatchCreateResponse
from app.services.logger import logger_service
from app.services import practice_flow
from app.utils.auth import require_admin
from app.utils.html import decode_html
from app.utils.kid_context import get_current_kid_id, get_required_kid_id

router = APIRouter(prefix="/api/questions", tags=["错题"])


def _visual_map_for(db: Session, eqs) -> dict:
    """批量取错题原题的配图场景，返回 {error_question_id: scene_dict}
    优先级：PracticeQuestion.visual（题库落库图例）→ 评测快照 scene（组卷时动态配的图，评测答题渲染用的那版）
    """
    ids = [q.source_practice_question_id for q in eqs if q.source_practice_question_id]
    if not ids:
        return {}
    pqs = db.query(PracticeQuestion).filter(PracticeQuestion.id.in_(ids)).all()
    by_id = {p.id: p for p in pqs}

    # 兜底：评测快照（questions JSON 里该题的 scene）
    snap_scene = {}  # (user_id, practice_question_id) -> scene
    uid_to_ids = {}
    for q in eqs:
        if q.source_practice_question_id and q.user_id:
            uid_to_ids.setdefault(q.user_id, set()).add(q.source_practice_question_id)
    for uid, pq_ids in uid_to_ids.items():
        records = db.query(AssessmentRecord).filter(
            AssessmentRecord.user_id == uid,
            AssessmentRecord.status == "done",
        ).order_by(AssessmentRecord.created_at.desc(), AssessmentRecord.id.desc()).all()
        for rec in records:
            try:
                qs = json.loads(rec.questions or "[]")
            except Exception:
                qs = []
            for item in qs:
                qid = item.get("question_id")
                if qid in pq_ids and item.get("scene"):
                    snap_scene.setdefault((uid, qid), item["scene"])

    out = {}
    for q in eqs:
        p = by_id.get(q.source_practice_question_id)
        scene = None
        if p and p.visual:
            try:
                scene = json.loads(p.visual)
            except Exception:
                scene = None
        if scene is None:
            scene = snap_scene.get((q.user_id, q.source_practice_question_id))
        if scene:
            out[q.id] = scene
    return out


@router.get("", response_model=QuestionListResponse)
def list_questions(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    error_book_id: Optional[int] = None,
    subject_id: Optional[int] = None,
    difficulty: Optional[str] = Query(None, description="难度，多个用逗号分隔"),
    error_type: Optional[str] = None,
    keyword: Optional[str] = None,
    grade: Optional[int] = Query(None, ge=1, le=12),
    semester: Optional[int] = Query(None, ge=1, le=2),
    tag_ids: Optional[str] = Query(None, description="标签ID，多个用逗号分隔（错题暂不支持标签）"),
    knowledge_point: Optional[str] = Query(None, description="知识点搜索"),
    accuracy_range: Optional[str] = Query(None, description="正确率区间筛选，如 '0-30','30-60','60-80','80-100'"),
    status: str = Query("active", description="active=在错题本（默认）, mastered=已掌握, all=全部"),
    source: Optional[str] = Query(None, description="来源：practice=批改判错派生, upload=手动上传"),
    include_ai: bool = Query(False, description="已废弃（错题与练习题已分表），保留仅为兼容"),
    db: Session = Depends(get_db),
    kid_id: Optional[int] = Depends(get_current_kid_id),
):
    """错题列表：数据来自 error_question（练习批改判错自动派生 + 手动上传）"""
    # 过滤已删除的记录
    query = db.query(ErrorQuestion).filter(ErrorQuestion.deleted == False)  # noqa: E712

    # 按小孩隔离：家长未选孩子时返回全部（家长视角）
    if kid_id is not None:
        query = query.filter(ErrorQuestion.user_id == kid_id)

    # 掌握状态：默认只显示仍在错题本的
    if status in ("active", "mastered"):
        query = query.filter(ErrorQuestion.status == status)
    if source:
        query = query.filter(ErrorQuestion.source == source)

    if error_book_id:
        query = query.filter(ErrorQuestion.error_book_id == error_book_id)
    if subject_id:
        query = query.filter(ErrorQuestion.subject_id == subject_id)
    # 难度多选
    if difficulty:
        diff_list = [int(d.strip()) for d in difficulty.split(',') if d.strip().isdigit()]
        if diff_list:
            query = query.filter(ErrorQuestion.difficulty.in_(diff_list))
    if error_type:
        # 错误类型多选
        error_type_list = [e.strip() for e in error_type.split(',') if e.strip()]
        if error_type_list:
            query = query.filter(ErrorQuestion.error_type.in_(error_type_list))
    if grade:
        query = query.filter(ErrorQuestion.grade == grade)
    if semester:
        query = query.filter(ErrorQuestion.semester == semester)
    # 知识点搜索
    if knowledge_point:
        query = query.filter(ErrorQuestion.knowledge_point.contains(knowledge_point))
    if keyword:
        query = query.filter(
            (ErrorQuestion.original_text.contains(keyword))
            | (ErrorQuestion.parsed_question.contains(keyword))
            | (ErrorQuestion.knowledge_point.contains(keyword))
        )
    # 正确率区间筛选（直接用缓存列）
    if accuracy_range:
        if accuracy_range == 'none':
            query = query.filter(
                (ErrorQuestion.review_count == 0) | (ErrorQuestion.review_count.is_(None))
            )
        else:
            try:
                parts = accuracy_range.split('-')
                if len(parts) == 2:
                    min_acc = float(parts[0])
                    max_acc = float(parts[1])
                    query = query.filter(
                        ErrorQuestion.accuracy.isnot(None),
                        ErrorQuestion.accuracy >= min_acc,
                        ErrorQuestion.accuracy <= max_acc,
                    )
            except Exception:
                pass

    total = query.count()
    items = query.order_by(ErrorQuestion.created_at.desc()).offset(skip).limit(limit).all()

    # 相似题（SimilarQuestion.source_question_id 现关联错题 id）
    sim_map = {}
    ids = [q.id for q in items]
    if ids:
        sims = db.query(SimilarQuestion).filter(
            SimilarQuestion.source_question_id.in_(ids),
            SimilarQuestion.deleted == False,  # noqa: E712
        ).all()
        for s in sims:
            sim_map.setdefault(s.source_question_id, []).append(s)

    # 转换items为响应格式
    visual_map = _visual_map_for(db, items)
    result_items = []
    for q in items:
        result_items.append({
            "id": q.id,
            "error_book_id": q.error_book_id,
            "subject_id": q.subject_id,
            "original_image": q.original_image,
            "original_images": json.loads(q.original_images) if q.original_images else None,
            "original_text": q.original_text,
            "parsed_question": q.parsed_question,
            "visual": visual_map.get(q.id),
            "grade": q.grade,
            "semester": q.semester,
            "answer": q.answer,
            "analysis": q.analysis,
            "analysis_image": q.analysis_image,
            "difficulty": q.difficulty,
            "error_type": q.error_type,
            "knowledge_point": q.knowledge_point,
            "question_type": q.question_type,
            "question_category": q.question_category,
            "option_a": q.option_a,
            "option_b": q.option_b,
            "option_c": q.option_c,
            "option_d": q.option_d,
            "correct_count": q.correct_count or 0,
            "error_count": q.wrong_count or 0,
            "review_count": q.review_count or 0,
            "accuracy": q.accuracy,
            "correct_streak": q.correct_streak or 0,
            "status": q.status,
            "source": q.source,
            "created_at": q.created_at,
            "updated_at": q.updated_at,
            "tags": [],
            "similar_questions": sim_map.get(q.id, []),
        })

    return {"total": total, "items": result_items}


@router.get("/filter-options/{subject_id}")
def get_filter_options(
    subject_id: int,
    grade: Optional[int] = Query(None, ge=1, le=12, description="按年级过滤（学习空间指定年级时）"),
    db: Session = Depends(get_db),
    kid_id: Optional[int] = Depends(get_current_kid_id),
):
    """获取指定学科的错误类型和知识点列表（去重；可按年级过滤）"""
    # 获取该孩子该学科下所有去重的错误类型
    error_q = db.query(ErrorQuestion.error_type).filter(
        ErrorQuestion.deleted == False,  # noqa: E712
        ErrorQuestion.subject_id == subject_id,
        ErrorQuestion.error_type.isnot(None),
        ErrorQuestion.error_type != ''
    )
    kp_q = db.query(ErrorQuestion.knowledge_point).filter(
        ErrorQuestion.deleted == False,  # noqa: E712
        ErrorQuestion.subject_id == subject_id,
        ErrorQuestion.knowledge_point.isnot(None),
        ErrorQuestion.knowledge_point != ''
    )
    if kid_id is not None:
        error_q = error_q.filter(ErrorQuestion.user_id == kid_id)
        kp_q = kp_q.filter(ErrorQuestion.user_id == kid_id)
    if grade is not None:
        error_q = error_q.filter(ErrorQuestion.grade == grade)
        kp_q = kp_q.filter(ErrorQuestion.grade == grade)
        kp_q = kp_q.filter(Question.grade == grade)
    error_types = error_q.distinct().all()
    knowledge_points = kp_q.distinct().all()

    # 拆分合并的错误类型（如 "计算错误,审题不清" 拆分为 ["计算错误", "审题不清"]）
    split_error_types = set()
    for (et,) in error_types:
        if et:
            for single_et in et.split(','):
                single_et = single_et.strip()
                if single_et:
                    split_error_types.add(single_et)

    return {
        "error_types": sorted(list(split_error_types)),
        "knowledge_points": sorted([kp for (kp,) in knowledge_points if kp])
    }


@router.get("/{question_id}", response_model=QuestionResponse)
def get_question(
    question_id: int,
    db: Session = Depends(get_db),
    kid_id: Optional[int] = Depends(get_current_kid_id),
):
    # 只获取未删除的记录（数据源：error_question）
    query = db.query(ErrorQuestion).filter(
        ErrorQuestion.id == question_id,
        ErrorQuestion.deleted == False,  # noqa: E712
    )
    if kid_id is not None:
        query = query.filter(ErrorQuestion.user_id == kid_id)
    question = query.first()
    if not question:
        raise HTTPException(status_code=404, detail="错题不存在")
    sims = db.query(SimilarQuestion).filter(
        SimilarQuestion.source_question_id == question.id,
        SimilarQuestion.deleted == False,  # noqa: E712
    ).all()
    visual_map = _visual_map_for(db, [question])
    result = {
        "id": question.id,
        "error_book_id": question.error_book_id,
        "subject_id": question.subject_id,
        "original_image": question.original_image,
        "original_images": json.loads(question.original_images) if question.original_images else None,
        "original_text": question.original_text,
        "parsed_question": question.parsed_question,
        "visual": visual_map.get(question.id),
        "grade": question.grade,
        "semester": question.semester,
        "answer": question.answer,
        "analysis": question.analysis,
        "analysis_image": question.analysis_image,
        "difficulty": question.difficulty,
        "error_type": question.error_type,
        "knowledge_point": question.knowledge_point,
        "question_type": question.question_type,
        "question_category": question.question_category,
        "option_a": question.option_a,
        "option_b": question.option_b,
        "option_c": question.option_c,
        "option_d": question.option_d,
        "correct_count": question.correct_count or 0,
        "error_count": question.wrong_count or 0,
        "review_count": question.review_count or 0,
        "accuracy": question.accuracy,
        "correct_streak": question.correct_streak or 0,
        "status": question.status,
        "source": question.source,
        "created_at": question.created_at,
        "updated_at": question.updated_at,
        "tags": [],
        "similar_questions": sims,
    }
    return result


@router.get("/{question_id}/practice-history")
def get_practice_history(question_id: int, db: Session = Depends(get_db)):
    """获取指定错题的作答历史记录（练习批改 + 评测答错合并，按时间倒序）"""
    question = db.query(ErrorQuestion).filter(
        ErrorQuestion.id == question_id,
        ErrorQuestion.deleted == False,  # noqa: E712
    ).first()
    if not question:
        raise HTTPException(status_code=404, detail="错题不存在")

    records = db.query(PracticeAttempt).filter(
        PracticeAttempt.error_question_id == question_id,
    ).order_by(PracticeAttempt.answered_at.desc(), PracticeAttempt.id.desc()).all()

    ps_ids = [r.practice_set_id for r in records if r.practice_set_id]
    ps_map = {}
    if ps_ids:
        ps_map = {p.id: p for p in db.query(PracticeSet).filter(PracticeSet.id.in_(ps_ids)).all()}

    # 用 (datetime, dict) 收集，最后统一按时间倒序，避免"未知日期"字符串排序错乱
    rows = []
    for r in records:
        ps = ps_map.get(r.practice_set_id)
        when = r.answered_at or (ps.created_at if ps else None)
        rows.append((
            when,
            {
                "practice_set_id": r.practice_set_id,
                "practice_set_name": (ps.name if ps else None) or "练习",
                "is_correct": 1 if r.is_correct else 0,
                "student_answer": r.student_answer or "",
                "source": "practice",
            },
        ))

    # 评测作答补充：该错题来源题（source_practice_question_id）在评测记录中的逐题明细
    pq_id = question.source_practice_question_id
    if pq_id:
        ars = db.query(AssessmentRecord).filter(
            AssessmentRecord.user_id == question.user_id,
            AssessmentRecord.status == "done",
        ).order_by(AssessmentRecord.created_at.desc(), AssessmentRecord.id.desc()).all()
        for ar in ars:
            try:
                detail = json.loads(ar.detail or "[]")
            except Exception:
                detail = []
            for item in detail:
                if item.get("question_id") == pq_id:
                    rows.append((
                        ar.created_at,
                        {
                            "practice_set_id": ar.id,
                            "practice_set_name": f"评测 · {ar.grade}年级",
                            "is_correct": float(item.get("correct") or 0),
                            "student_answer": item.get("user_answer") or "",
                            "source": "assessment",
                        },
                    ))
                    break

    rows.sort(key=lambda x: (x[0] is None, x[0] or datetime.min), reverse=True)
    out = []
    for when, item in rows:
        item["date"] = when.strftime("%Y-%m-%d %H:%M") if when else "未知日期"
        out.append(item)
    return out


@router.post("", response_model=QuestionResponse, status_code=201)
def create_question(
    data: QuestionCreate,
    db: Session = Depends(get_db),
    kid_id: int = Depends(get_required_kid_id),
):
    """手动新增错题（拍照/OCR 录入）：来源标记 source='upload'，保留错题来源"""
    try:
        # 处理多个图片
        original_images_json = None
        if data.original_images:
            original_images_json = json.dumps(data.original_images, ensure_ascii=False)

        # 没指定错题本 → 归到该孩子该学科的错题本
        error_book_id = data.error_book_id
        if not error_book_id:
            error_book_id = practice_flow.ensure_error_book(db, kid_id, data.subject_id).id

        question = ErrorQuestion(
            user_id=kid_id,
            error_book_id=error_book_id,
            subject_id=data.subject_id,
            original_image=data.original_image,
            original_images=original_images_json,
            original_text=data.original_text,
            parsed_question=decode_html(data.parsed_question) if data.parsed_question else None,
            grade=data.grade,
            semester=data.semester,
            answer=decode_html(data.answer) if data.answer else None,
            analysis=decode_html(data.analysis) if data.analysis else None,
            difficulty=data.difficulty,
            error_type=data.error_type,
            knowledge_point=data.knowledge_point,
            source="upload",
            review_count=0,
            correct_count=0,
            wrong_count=0,
            correct_streak=0,
            status="active",
        )
        db.add(question)
        db.commit()
        db.refresh(question)

        # 触发积分行为（上传错题）
        try:
            from app.services.motivation import MotivationService
            service = MotivationService(db)
            service.trigger_action("upload_question", user_id=kid_id, reason="上传错题")
        except Exception:
            pass  # 激励系统不影响主流程

        # 记录日志
        logger_service.log_question(
            operation=OperationType.CREATE_QUESTION,
            question_id=question.id,
            data={
                "error_book_id": error_book_id,
                "subject_id": data.subject_id,
                "original_text": data.original_text[:100] if data.original_text else None,
            },
            success=True,
        )

        # 返回格式化的响应
        return {
            "id": question.id,
            "error_book_id": question.error_book_id,
            "subject_id": question.subject_id,
            "original_image": question.original_image,
            "original_images": json.loads(question.original_images) if question.original_images else None,
            "original_text": question.original_text,
            "parsed_question": question.parsed_question,
            "grade": question.grade,
            "semester": question.semester,
            "answer": question.answer,
            "analysis": question.analysis,
            "analysis_image": question.analysis_image,
            "difficulty": question.difficulty,
            "error_type": question.error_type,
            "knowledge_point": question.knowledge_point,
            "question_type": question.question_type,
            "question_category": question.question_category,
            "option_a": question.option_a,
            "option_b": question.option_b,
            "option_c": question.option_c,
            "option_d": question.option_d,
            "correct_count": question.correct_count or 0,
            "error_count": question.wrong_count or 0,
            "review_count": question.review_count or 0,
            "accuracy": question.accuracy,
            "correct_streak": question.correct_streak or 0,
            "status": question.status,
            "source": question.source,
            "created_at": question.created_at,
            "updated_at": question.updated_at,
            "tags": [],
            "similar_questions": [],
        }
    except Exception as e:
        # 记录错误日志
        logger_service.log_question(
            operation=OperationType.CREATE_QUESTION,
            question_id=-1,
            data={"error_book_id": data.error_book_id, "subject_id": data.subject_id},
            success=False,
            error=str(e),
        )
        raise HTTPException(status_code=500, detail=f"创建错题失败: {str(e)}")


# 临时调试端点
@router.put("/debug/{question_id}")
def debug_update(
    question_id: int,
    request: Request,
):
    body = request.body()
    print(f"[DEBUG PUT /debug/{question_id}] body: {body}")
    return {"received": True}


@router.put("/{question_id}", response_model=QuestionResponse)
def update_question(
    question_id: int,
    data: QuestionUpdate,
    db: Session = Depends(get_db),
    kid_id: Optional[int] = Depends(get_current_kid_id),
):
    try:
        query = db.query(ErrorQuestion).filter(
            ErrorQuestion.id == question_id,
            ErrorQuestion.deleted == False,  # noqa: E712
        )
        if kid_id is not None:
            query = query.filter(ErrorQuestion.user_id == kid_id)
        question = query.first()
        if not question:
            raise HTTPException(status_code=404, detail="错题不存在")

        update_data = data.model_dump(exclude_unset=True)
        tag_ids = update_data.pop("tag_ids", None)

        # 调试日志
        print(f"[DEBUG] update_data: {update_data}")
        print(f"[DEBUG] original_image in update_data: {'original_image' in update_data}")
        print(f"[DEBUG] original_image value: {update_data.get('original_image')}")

        # 解码HTML实体
        for key in ["parsed_question", "answer", "analysis"]:
            if key in update_data and update_data[key]:
                update_data[key] = decode_html(update_data[key])

        if tag_ids is not None:
            update_data.pop("tag_ids", None)  # 错题暂不支持标签

        for key, value in update_data.items():
            setattr(question, key, value)

        db.commit()
        db.refresh(question)

        # 记录日志
        logger_service.log_question(
            operation=OperationType.UPDATE_QUESTION,
            question_id=question_id,
            data=update_data,
            success=True,
        )

        # 返回格式化的响应
        return {
            "id": question.id,
            "error_book_id": question.error_book_id,
            "subject_id": question.subject_id,
            "original_image": question.original_image,
            "original_images": json.loads(question.original_images) if question.original_images else None,
            "original_text": question.original_text,
            "parsed_question": question.parsed_question,
            "grade": question.grade,
            "semester": question.semester,
            "answer": question.answer,
            "analysis": question.analysis,
            "analysis_image": question.analysis_image,
            "difficulty": question.difficulty,
            "error_type": question.error_type,
            "knowledge_point": question.knowledge_point,
            "question_type": question.question_type,
            "question_category": question.question_category,
            "option_a": question.option_a,
            "option_b": question.option_b,
            "option_c": question.option_c,
            "option_d": question.option_d,
            "correct_count": question.correct_count or 0,
            "error_count": question.wrong_count or 0,
            "review_count": question.review_count or 0,
            "accuracy": question.accuracy,
            "correct_streak": question.correct_streak or 0,
            "status": question.status,
            "source": question.source,
            "created_at": question.created_at,
            "updated_at": question.updated_at,
            "tags": [],
            "similar_questions": [],
        }
    except HTTPException:
        raise
    except Exception as e:
        logger_service.log_question(
            operation=OperationType.UPDATE_QUESTION,
            question_id=question_id,
            data={},
            success=False,
            error=str(e),
        )
        raise HTTPException(status_code=500, detail=f"更新错题失败: {str(e)}")


@router.delete("/{question_id}", status_code=204)
def delete_question(
    question_id: int,
    db: Session = Depends(get_db),
    kid_id: Optional[int] = Depends(get_current_kid_id),
    user: User = Depends(require_admin),
):
    """
    软删除错题（设置deleted=True），而非物理删除
    家长认证：学生（child）不能删除错题，必须家长（admin）操作
    """
    try:
        query = db.query(ErrorQuestion).filter(
            ErrorQuestion.id == question_id,
            ErrorQuestion.deleted == False,  # noqa: E712
        )
        if kid_id is not None:
            query = query.filter(ErrorQuestion.user_id == kid_id)
        question = query.first()
        if not question:
            raise HTTPException(status_code=404, detail="错题不存在")

        # 软删除：设置deleted标志为True
        question.deleted = True
        db.commit()

        # 记录日志
        logger_service.log_question(
            operation=OperationType.DELETE_QUESTION,
            question_id=question_id,
            data={"soft_delete": True},
            success=True,
        )
    except HTTPException:
        raise
    except Exception as e:
        logger_service.log_question(
            operation=OperationType.DELETE_QUESTION,
            question_id=question_id,
            data={},
            success=False,
            error=str(e),
        )
        raise HTTPException(status_code=500, detail=f"删除错题失败: {str(e)}")


@router.post("/batch", response_model=BatchCreateResponse)
def create_questions_batch(
    data: QuestionBatchCreate,
    db: Session = Depends(get_db),
    kid_id: int = Depends(get_required_kid_id),
):
    """
    批量创建错题（用于OCR后一道图生成多题）：来源标记 source='upload'
    """
    created_questions = []
    success_count = 0

    error_book_id = data.error_book_id
    if not error_book_id:
        error_book_id = practice_flow.ensure_error_book(db, kid_id, data.subject_id).id

    for q_data in data.questions:
        try:
            question = ErrorQuestion(
                user_id=kid_id,
                error_book_id=error_book_id,
                subject_id=data.subject_id,
                original_images=json.dumps(data.images, ensure_ascii=False),
                original_image=data.images[0] if data.images else None,
                original_text=q_data.original_text,
                parsed_question=decode_html(q_data.parsed_question) if q_data.parsed_question else None,
                grade=data.grade,
                semester=data.semester,
                answer=decode_html(q_data.answer) if q_data.answer else None,
                analysis=decode_html(q_data.analysis) if q_data.analysis else None,
                difficulty=q_data.difficulty,
                error_type=q_data.error_type,
                knowledge_point=q_data.knowledge_point,
                source="upload",
                review_count=0,
                correct_count=0,
                wrong_count=0,
                correct_streak=0,
                status="active",
            )
            db.add(question)
            db.commit()
            db.refresh(question)
            created_questions.append(question)
            success_count += 1

            logger_service.log_question(
                operation=OperationType.CREATE_QUESTION,
                question_id=question.id,
                data={"batch": True, "images": data.images},
                success=True,
            )
        except Exception as e:
            db.rollback()
            logger_service.log_question(
                operation=OperationType.CREATE_QUESTION,
                question_id=-1,
                data={"batch": True},
                success=False,
                error=str(e),
            )

    # 转换响应
    result_questions = []
    for q in created_questions:
        result_questions.append({
            "id": q.id,
            "error_book_id": q.error_book_id,
            "subject_id": q.subject_id,
            "original_image": q.original_image,
            "original_images": json.loads(q.original_images) if q.original_images else None,
            "original_text": q.original_text,
            "parsed_question": q.parsed_question,
            "answer": q.answer,
            "analysis": q.analysis,
            "difficulty": q.difficulty,
            "error_type": q.error_type,
            "knowledge_point": q.knowledge_point,
            "question_type": q.question_type,
            "question_category": q.question_category,
            "option_a": q.option_a,
            "option_b": q.option_b,
            "option_c": q.option_c,
            "option_d": q.option_d,
            "correct_count": q.correct_count or 0,
            "error_count": q.wrong_count or 0,
            "review_count": q.review_count or 0,
            "accuracy": q.accuracy,
            "correct_streak": q.correct_streak or 0,
            "status": q.status,
            "source": q.source,
            "created_at": q.created_at,
            "updated_at": q.updated_at,
            "tags": [],
            "similar_questions": [],
        })

    return {
        "questions": result_questions,
        "total_count": len(data.questions),
        "success_count": success_count,
    }
