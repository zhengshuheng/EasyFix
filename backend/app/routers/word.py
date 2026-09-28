"""
单词路由 - 管理单词的录入、复习、统计等功能
"""
from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from typing import Optional, List
from pydantic import BaseModel
import random
import json
from datetime import datetime, timedelta
from app.database import get_db
from app.models import Word, Tag, WordReviewLog, WordReview, WordAttempt
from app.models.word import WordProgress
from app.models.user import User
from app.utils.auth import require_admin
from app.schemas.word import (
    WordCreate, WordUpdate, WordResponse, WordListResponse,
    WordStatsResponse, ReviewSessionSubmit, ReviewStartResponse, ReviewQuestion,
    MemoryCurveResponse, WordAIGenerateRequest
)
from app.services.textbook_service import _llm_json
import re
import threading
import time

router = APIRouter(prefix="/api/words", tags=["单词"])

# 默认用户ID
DEFAULT_USER_ID = 1


def _dump_json(v) -> str:
    """List/dict → JSON 字符串（空值 → '[]'）"""
    if v is None:
        return '[]'
    try:
        return json.dumps(v, ensure_ascii=False)
    except Exception:
        return '[]'


def _parse_json_list(raw) -> list:
    """JSON 字符串 → list（解析失败返回空列表）"""
    if not raw:
        return []
    try:
        v = json.loads(raw)
        return v if isinstance(v, list) else []
    except Exception:
        return []


def _resolve_user_id(db: Session, user_id: Optional[int]) -> int:
    """未指定小孩时回退到第一个小孩（演示小孩），兼容旧前端"""
    if user_id:
        return user_id
    kid = db.query(User.id).filter(User.role == "child").order_by(User.id).first()
    return kid[0] if kid else DEFAULT_USER_ID


# ===== 四维记忆模型 =====
# 题型 → 记忆维度：1=中-英(说得) 2=英-中(认得) 3=听写(写得) 4=听音选中文(听得) 5=记忆模式(说得)
_DIMENSION_BY_REVIEW_TYPE = {1: "speak", 2: "recognize", 3: "write", 4: "listen", 5: "speak"}
# 维度 → word_progress 计数列名
_DIMENSION_FIELDS = {
    "recognize": ("recognize_count", "recognize_correct"),
    "listen": ("listen_count", "listen_correct"),
    "speak": ("speak_count", "speak_correct"),
    "write": ("write_count", "write_correct"),
}


def _dimension_for_review_type(review_type: int) -> str:
    return _DIMENSION_BY_REVIEW_TYPE.get(review_type, "recognize")


def _upsert_word_attempt(db: Session, word: Word, user_id: int, dimension: str, source: str = "review"):
    """答错 → 词入记忆错题池（同一 word+dimension 覆盖并累计答错次数）"""
    try:
        row = db.query(WordAttempt).filter(
            WordAttempt.word_id == word.id,
            WordAttempt.user_id == user_id,
            WordAttempt.dimension == dimension,
        ).first()
        now = datetime.now()
        if row:
            row.english = word.english
            row.chinese = word.chinese
            row.phonetic = word.phonetic
            row.wrong_count = (row.wrong_count or 1) + 1
            row.updated_at = now
        else:
            db.add(WordAttempt(
                word_id=word.id,
                user_id=user_id,
                dimension=dimension,
                source=source,
                english=word.english,
                chinese=word.chinese,
                phonetic=word.phonetic,
                wrong_count=1,
                created_at=now,
                updated_at=now,
            ))
    except Exception:
        pass  # 错词池异常不影响主流程


def _clear_word_attempt(db: Session, word_id: int, user_id: int, dimension: str):
    """答对 → 移出记忆错题池（掌握即出池）"""
    try:
        rows = db.query(WordAttempt).filter(
            WordAttempt.word_id == word_id,
            WordAttempt.user_id == user_id,
            WordAttempt.dimension == dimension,
        ).all()
        for r in rows:
            db.delete(r)
    except Exception:
        pass


def _get_progress(db: Session, word_id: int, user_id: int) -> WordProgress:
    """获取（必要时创建）某小孩对某词的复习进度"""
    p = db.query(WordProgress).filter(
        WordProgress.word_id == word_id,
        WordProgress.user_id == user_id,
    ).first()
    if not p:
        p = WordProgress(word_id=word_id, user_id=user_id)
        db.add(p)
        db.flush()
    return p


def _get_accuracy_level(review_count: int, correct_count: int) -> str:
    """计算正确率等级

    注意：仅答对 1 次**不算掌握**——必须累计≥3 次且正确率>80% 才判 mastered，
    否则词会在第一次答对后立刻被判为"已掌握"而从今日任务里消失（曾导致
    孩子只练一次就再也见不到这个词）。
    """
    if review_count == 0:
        return "new"  # 新词
    accuracy = (correct_count / review_count * 100) if review_count > 0 else 0
    if accuracy == 0:
        return "weak"  # 需加强
    elif accuracy <= 60:
        return "learning"  # 薄弱
    elif accuracy <= 80 or review_count < 3:
        return "good"  # 一般（含"答对次数还不够"的情况）
    else:
        return "mastered"  # 掌握


def _stable_shuffle(items: list, seed: str) -> list:
    """按 seed 稳定打散（同一天同 seed 结果一致，跨天/换 seed 才变）

    用于「今日新词」抽样：既避免每天固定吐同一批 id，又保证同一天内
    多次刷新看到的是同一组词（孩子中途刷新不会换题）。
    """
    import hashlib
    def _key(it):
        raw = f"{seed}:{getattr(it, 'id', it)}"
        return hashlib.md5(raw.encode("utf-8")).hexdigest()
    return sorted(items, key=_key)


# ---- 科学记忆调度参数 ----
MASTERED_PHASE = "牢记"
# 牢记抽查：随机在这些天数里取一个作为下次抽查间隔（防短期记忆）
MASTERED_REVIEW_INTERVALS = (5, 10, 15)
# 牢记抽查答对后继续拉长（证明长期记忆稳固）
MASTERED_EXTEND_INTERVALS = (20, 30, 60)
# 牢记抽查答错后回落（它曾掌握过，不必从 1 天重来）
MASTERED_RELAPSE_INTERVAL = 3
# 牢记抽查比例：每天从「牢记池」里随机抽 10%
MASTERED_SAMPLE_RATIO = 0.10
MASTERED_SAMPLE_MIN = 1


def _next_mastered_interval(interval: int, correct: bool) -> int:
    """牢记阶段的抽查间隔推进。

    答对：按 5→10→15→20→30→60 阶梯往上走（不再 30 天封顶）。
    答错：回落到 3 天（不是 1 天——它曾掌握过）。
    """
    if not correct:
        return MASTERED_RELAPSE_INTERVAL
    cur = interval or 0
    ladder = MASTERED_REVIEW_INTERVALS + MASTERED_EXTEND_INTERVALS
    for step in ladder:
        if step > cur:
            return step
    return ladder[-1]



def _get_consecutive_correct(word_id: int, user_id: int, db: Session) -> int:
    """获取连续正确次数"""
    logs = db.query(WordReviewLog).filter(
        WordReviewLog.word_id == word_id,
        WordReviewLog.user_id == user_id,
        WordReviewLog.deleted == False
    ).order_by(WordReviewLog.reviewed_at.desc()).limit(10).all()

    consecutive = 0
    for log in reversed(logs):
        if log.is_correct:
            consecutive += 1
        else:
            break
    return consecutive


@router.get("")
def list_words(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=1000),
    user_id: Optional[int] = Query(None, description="小孩ID（复习情况/正确率按该小孩统计；不传则默认第一个小孩）"),
    grade: Optional[int] = Query(None, ge=1, le=12),
    semester: Optional[int] = Query(None, ge=1, le=2),
    tag_ids: Optional[str] = Query(None, description="标签ID，多个用逗号分隔"),
    keyword: Optional[str] = None,
    sort_by: Optional[str] = Query(None, description="排序字段：accuracy, review_count, created_at"),
    sort_order: Optional[str] = Query("desc", description="排序方向：asc, desc"),
    accuracy_min: Optional[float] = Query(None, description="正确率下限"),
    accuracy_max: Optional[float] = Query(None, description="正确率上限"),
    accuracy_level: Optional[str] = Query(None, description="正确率等级：new, weak, learning, good, mastered"),
    db: Session = Depends(get_db),
):
    """获取单词列表（单词库全局共享；复习情况/正确率按 user_id 隔离）"""
    uid = _resolve_user_id(db, user_id)
    query = db.query(Word).filter(Word.deleted == False)

    if grade:
        query = query.filter(Word.grade == grade)
    if semester:
        query = query.filter(Word.semester == semester)
    if keyword:
        query = query.filter(
            (Word.english.contains(keyword))
            | (Word.chinese.contains(keyword))
        )
    if tag_ids:
        tag_list = [int(t.strip()) for t in tag_ids.split(',') if t.strip().isdigit()]
        if tag_list:
            from app.models.word import word_tag
            query = query.join(word_tag).filter(word_tag.c.tag_id.in_(tag_list))

    # 先获取所有匹配的数据用于计算正确率
    all_items = query.all()

    # 批量读取该小孩的复习进度（避免 N+1）
    word_ids = [w.id for w in all_items]
    progress_map = {}
    if word_ids:
        progs = db.query(WordProgress).filter(
            WordProgress.user_id == uid,
            WordProgress.word_id.in_(word_ids),
        ).all()
        progress_map = {p.word_id: p for p in progs}

    # 计算正确率并过滤
    items_with_accuracy = []
    for item in all_items:
        p = progress_map.get(item.id)
        review_count = p.review_count if p else 0
        correct_count = p.correct_count if p else 0
        accuracy = (correct_count / review_count * 100) if review_count and review_count > 0 else (0 if review_count == 0 else None)
        item_accuracy_level = _get_accuracy_level(review_count or 0, correct_count or 0)
        items_with_accuracy.append({
            'item': item,
            'progress': p,
            'accuracy': accuracy,
            'accuracy_level': item_accuracy_level
        })

    # 过滤正确率等级
    if accuracy_level:
        items_with_accuracy = [x for x in items_with_accuracy if x['accuracy_level'] == accuracy_level]

    # 过滤正确率范围
    if accuracy_min is not None:
        items_with_accuracy = [x for x in items_with_accuracy if x['accuracy'] is not None and x['accuracy'] >= accuracy_min]
    if accuracy_max is not None:
        items_with_accuracy = [x for x in items_with_accuracy if x['accuracy'] is not None and x['accuracy'] <= accuracy_max]

    # 排序
    if sort_by == 'accuracy':
        items_with_accuracy.sort(key=lambda x: x['accuracy'] if x['accuracy'] is not None else -1, reverse=(sort_order == 'desc'))
    elif sort_by == 'review_count':
        items_with_accuracy.sort(key=lambda x: (x['progress'].review_count if x['progress'] else 0) or 0, reverse=(sort_order == 'desc'))
    else:
        items_with_accuracy.sort(key=lambda x: x['item'].created_at.timestamp(), reverse=(sort_order == 'desc'))

    total = len(items_with_accuracy)

    # 应用分页
    paginated = items_with_accuracy[skip:skip + limit]

    # 构建返回结果，添加accuracy和accuracy_level字段
    items = []
    for x in paginated:
        item = x['item']
        p = x['progress']
        items.append({
            "id": item.id,
            "english": item.english,
            "chinese": item.chinese,
            "phonetic": item.phonetic,
            "grade": item.grade,
            "semester": item.semester,
            "unit": item.unit,
            "unit_title": item.unit_title,
            "phonetic_rule": item.phonetic_rule,
            "mnemonic": item.mnemonic,
            "word_root": item.word_root,
            "related_words": _parse_json_list(item.related_words),
            "example_sentences": _parse_json_list(item.example_sentences),
            "review_count": (p.review_count if p else 0) or 0,
            "correct_count": (p.correct_count if p else 0) or 0,
            "accuracy": x['accuracy'],
            "accuracy_level": x['accuracy_level'],
            "last_reviewed_at": p.last_reviewed_at if p else None,
            "next_review_at": p.next_review_at if p else None,
            "created_at": item.created_at,
            "tags": item.tags,
        })

    return {
        "total": total,
        "items": items
    }


@router.get("/errors", response_model=WordListResponse)
def get_error_words(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=1000),
    user_id: Optional[int] = Query(None, description="小孩ID（错词按该小孩进度计算；不传则默认第一个小孩）"),
    db: Session = Depends(get_db)
):
    """获取错词列表（该小孩正确率低于60%的单词）"""
    uid = _resolve_user_id(db, user_id)
    query = db.query(Word).filter(
        Word.deleted == False,
        Word.id.in_(
            db.query(WordProgress.word_id).filter(
                WordProgress.user_id == uid,
                WordProgress.review_count > 0,
                WordProgress.correct_count * 1.0 / WordProgress.review_count < 0.6,
            )
        )
    )

    total = query.count()
    items = query.order_by(desc(Word.id)).offset(skip).limit(limit).all()

    # 组装进度字段
    word_ids = [w.id for w in items]
    progress_map = {
        p.word_id: p for p in db.query(WordProgress).filter(
            WordProgress.user_id == uid,
            WordProgress.word_id.in_(word_ids),
        ).all()
    } if word_ids else {}
    result_items = []
    for w in items:
        p = progress_map.get(w.id)
        result_items.append({
            "id": w.id,
            "english": w.english,
            "chinese": w.chinese,
            "phonetic": w.phonetic,
            "grade": w.grade,
            "semester": w.semester,
            "review_count": (p.review_count if p else 0) or 0,
            "correct_count": (p.correct_count if p else 0) or 0,
            "accuracy": round((p.correct_count / p.review_count * 100), 1) if p and p.review_count else 0,
            "accuracy_level": _get_accuracy_level((p.review_count if p else 0) or 0, (p.correct_count if p else 0) or 0),
            "last_reviewed_at": p.last_reviewed_at if p else None,
            "next_review_at": p.next_review_at if p else None,
            "created_at": w.created_at,
            "tags": w.tags,
        })

    return {"total": total, "items": result_items}


@router.get("/{word_id}/memory-curve", response_model=MemoryCurveResponse)
def get_memory_curve(word_id: int, user_id: Optional[int] = Query(None, description="小孩ID，不传则默认第一个小孩"), db: Session = Depends(get_db)):
    """获取单词记忆曲线（按小孩隔离）"""
    uid = _resolve_user_id(db, user_id)
    word = db.query(Word).filter(Word.id == word_id, Word.deleted == False).first()
    if not word:
        # 兜底：该 id 可能被 ops 同步软删（旧版全量替换导致 id 漂移）。
        # 按原行 english 找当前 active 行（同步后的新行）生成音频；词被彻底移除时
        # 用快照 english 现场 TTS，避免旧题目/进度引用的旧 id 直接 404。
        stale = db.query(Word).filter(Word.id == word_id).first()
        if stale and (stale.english or "").strip():
            live = db.query(Word).filter(
                func.lower(Word.english) == stale.english.strip().lower(),
                Word.deleted == False,
            ).first()
            word = live or stale
        else:
            raise HTTPException(status_code=404, detail="单词不存在")

    progress = _get_progress(db, word_id, uid)

    # 获取该小孩的复习历史
    logs = db.query(WordReviewLog).filter(
        WordReviewLog.word_id == word_id,
        WordReviewLog.user_id == uid,
        WordReviewLog.deleted == False
    ).order_by(WordReviewLog.reviewed_at.desc()).all()

    review_history = []
    for log in logs:
        review_history.append({
            "reviewed_at": log.reviewed_at,
            "is_correct": log.is_correct,
            "user_answer": log.user_answer or " - "
        })

    return {
        "word_id": word.id,
        "learning_phase": progress.learning_phase or "新学",
        "interval": progress.interval or 1,
        "next_review_at": progress.next_review_at,
        "review_history": review_history
    }


# ==================== 今日任务（四维记忆调度） ====================

_DIMENSION_NAMES = {"recognize": "认得", "listen": "听得", "speak": "说得", "write": "写得"}


@router.get("/daily-task")
def daily_task(
    user_id: Optional[int] = Query(None, description="小孩ID（不传则默认第一个小孩）"),
    grade: Optional[int] = Query(None, description="按年级筛选"),
    dimensions: Optional[str] = Query(None, description="启用的维度，逗号分隔（默认全部：recognize,listen,speak,write）"),
    new_quota: int = Query(5, ge=0, le=20, description="新学词配额"),
    per_word_dims: int = Query(1, ge=1, le=4, description="每个词每轮最多练几个维度（科学记忆：间隔轮转>集中轰炸，默认1）"),
    category_cap: int = Query(15, ge=1, le=100, description="错题练习/到期复习单类最多词数（控制单次练习量）"),
    db: Session = Depends(get_db),
):
    """今日任务：到期词（记忆曲线）+ 记忆错词池 + 新学词配额

    科学记忆设计：
    - 间隔效应：每个词每轮只练最弱 1 个维度（per_word_dims），四维靠多轮轮转覆盖；
    - 轮转顺序按日期偏移，避免天天练同一维度；
    - 错池维度（in_pool）永远优先（针对性补弱）；
    - 单类词数受 category_cap 限制，避免一次任务过重让孩子失去兴趣。
    """
    uid = _resolve_user_id(db, user_id)
    enabled = [d.strip() for d in (dimensions or "recognize,listen,speak,write").split(",") if d.strip() in _DIMENSION_NAMES]
    if not enabled:
        enabled = list(_DIMENSION_NAMES)

    now = datetime.now()
    # 轮转顺序：按年内天数偏移，让不同天优先练不同维度
    rotation = now.timetuple().tm_yday % len(enabled)
    rotation_order = enabled[rotation:] + enabled[:rotation]

    query = db.query(Word).filter(Word.deleted == False)  # noqa: E712
    if grade:
        query = query.filter(Word.grade == grade)
    words = query.all()

    progress_map = {
        p.word_id: p for p in db.query(WordProgress).filter(
            WordProgress.user_id == uid,
            WordProgress.word_id.in_([w.id for w in words]),
        ).all()
    }
    # 错词池（该小孩）：词级去重（任一维度在池即算记忆错词）
    attempts = db.query(WordAttempt).filter(WordAttempt.user_id == uid).all()
    attempt_map = {}
    for a in attempts:
        attempt_map.setdefault(a.word_id, []).append(a)

    due_words = []       # 到期词（有进度且到期，或低正确率；已在错词池的词归错题练习，不重复计）
    new_words = []       # 新学词（无进度，且未在学词卡里看过）
    mastered_due = []    # 「牢记」到期抽查池（总体不出现，仅限量随机抽查）
    today = now.date()
    for w in words:
        p = progress_map.get(w.id)
        if p is None or (p.review_count or 0) == 0:
            # 复习次数为 0 时，若已「看过」（学词卡翻到过），也不再算新词——
            # 否则孩子看了一遍没答题，下次点开还是这批词，等于白学。
            if p is not None and p.seen_at is not None:
                continue
            new_words.append(w)
            continue
        if attempt_map.get(w.id):
            continue  # 错池词优先归「错题练习」，不重复出现在到期复习

        # 「当天学过的不进当天轮次」：今天已复习过的词，明天再排。
        # 否则"上午答对、下午又出现"，孩子会觉得原地打转。
        if p.last_reviewed_at and p.last_reviewed_at.date() >= today:
            continue

        # 「牢记」的词总体不再出现，只进专属抽查池
        if p.learning_phase == MASTERED_PHASE:
            if p.next_review_at and p.next_review_at <= now:
                mastered_due.append((w, p))
            continue

        due = (p.next_review_at and p.next_review_at <= now) or (
            p.learning_phase in ("遗忘点", "在途")
            and (p.correct_count or 0) < (p.review_count or 0) * 0.6
        )
        if due:
            due_words.append((w, p))

    # 错池词（按词去重，与到期词合并；错池优先；受单类上限控制）
    # 打乱：不再按 Word.id 顺序取，避免孩子靠固定位置蒙对
    wrong_pool = [w for w in words if attempt_map.get(w.id)]
    wrong_words = _stable_shuffle(wrong_pool, f"wrong:{today}")[:category_cap]
    # 打乱：不再按 next_review_at 升序（否则最早就到期的永远排前面，天天同一批）
    due_shuffled = _stable_shuffle([w for w, _ in due_words], f"due:{today}")
    due_words = [(w, progress_map[w.id]) for w in due_shuffled][:category_cap]

    # 牢记抽查：从到期的牢记词里按比例随机抽（每天抽一部分，不一次全上）
    if mastered_due:
        sample_n = max(MASTERED_SAMPLE_MIN,
                       int(round(len(mastered_due) * MASTERED_SAMPLE_RATIO)))
        sample_n = min(sample_n, len(mastered_due), category_cap)
        picked = _stable_shuffle([w for w, _ in mastered_due], f"mastered:{today}")[:sample_n]
        for w in picked:
            due_words.append((w, progress_map[w.id]))

    # 今日任务词 = 错池 ∪ 到期（按优先级排序：错池 > 到期 > 低正确率）
    task_words = []
    seen = set()
    for w in wrong_words:
        if w.id not in seen:
            task_words.append(w)
            seen.add(w.id)
    for w, _p in due_words:
        if w.id not in seen:
            task_words.append(w)
            seen.add(w.id)

    # ===== 例句懒生成（复习题卡）：缺例句的词临时 AI 生成并写回空间库 =====
    # 运营词库 ops_word 无例句，同步后空间库词缺例句；学习时按需补一次，
    # 写回后全部小孩共享（下次任何入口秒开），不阻塞学习（失败降级为无例句）。
    missing_review = [w for w in task_words
                      if not (w.example_sentences and w.example_sentences.strip() and w.example_sentences.strip() != "[]")]
    if missing_review:
        try:
            _res = _fill_sentences_llm(db, missing_review)
            if _res.get("ok_count"):
                db.commit()
        except Exception as _e:
            db.rollback()
            print(f"[words] 复习题卡例句懒生成失败({len(missing_review)}词): {_e}")

    items = []
    for w in task_words:
        p = progress_map.get(w.id)
        dims = {}
        pool_dims = []
        weak_ordered = []
        for d in rotation_order:  # 按轮转顺序评估，保证不同天优先不同维度
            c_field, ok_field = _DIMENSION_FIELDS[d]
            count = getattr(p, c_field, 0) if p else 0
            correct = getattr(p, ok_field, 0) if p else 0
            acc = round(correct * 100.0 / count, 0) if count else 0
            # 薄弱：练过且正确率<60%，或在该维有错池记录
            in_pool = any(a.dimension == d for a in attempt_map.get(w.id, []))
            weak = (count > 0 and acc < 60) or in_pool or count == 0
            dims[d] = {"count": count, "correct": correct, "accuracy": acc, "weak": weak, "in_pool": in_pool}
            if in_pool:
                pool_dims.append(d)
            if weak and d not in pool_dims:
                weak_ordered.append(d)
        # 推荐维度 = 错池维度优先 + 薄弱维度（轮转序），按每词维度数截断
        recommended = (pool_dims + weak_ordered)[:per_word_dims]
        if not recommended:
            recommended = rotation_order[:per_word_dims]  # 全达标也轮转练 1 个保持熟悉
        items.append({
            "word_id": w.id,
            "english": w.english,
            "chinese": w.chinese,
            "phonetic": w.phonetic,
            "mnemonic": w.mnemonic,
            "example_sentences": _parse_json_list(w.example_sentences),
            "learning_phase": p.learning_phase if p else "新学",
            "in_attempt": bool(attempt_map.get(w.id)),
            "dimensions": dims,
            "recommended_dimensions": recommended,
            "wrong_total": sum(a.wrong_count or 1 for a in attempt_map.get(w.id, [])),
        })

    # 新学词配额（取无进度中未在今日任务里的，优先带记忆增强的）
    #
    # 关键：**必须随机打散**，不能按 Word.id 升序取前 quota 个。
    # 旧实现按 id 取头 → 无进度词有几百个时，永远返回同一批（如 [6,7,8,9,10]），
    # 而 review/start 是独立随机池、几乎抽不中这批词 → 那些词的 review_count
    # 永远是 0 → 明天又原样出现，形成"学过的词/显示的新词"两套池永不相交的死锁。
    # 打散 seed 用「日期 + 已练过词数」，既保证同一天内刷新结果稳定，
    # 又能在练过词后自动换一批。
    seed = f"{now.strftime('%Y-%m-%d')}:{len(progress_map)}"
    new_candidates = [w for w in new_words if w.id not in seen]
    # 先在组内稳定打散，再按「是否带口诀」稳定排序：
    # 带记忆增强的词优先，同组内顺序由 seed 决定（同一天刷新结果一致）
    new_candidates = _stable_shuffle(new_candidates, seed)
    new_candidates.sort(key=lambda w: 0 if (w.mnemonic or "").strip() else 1)
    quota = min(new_quota, len(new_candidates))

    # ===== 例句懒生成（今日新词）：缺例句的新词临时 AI 生成并写回空间库 =====
    missing_new = [w for w in new_candidates[:quota]
                   if not (w.example_sentences and w.example_sentences.strip() and w.example_sentences.strip() != "[]")]
    if missing_new:
        try:
            _res = _fill_sentences_llm(db, missing_new)
            if _res.get("ok_count"):
                db.commit()
        except Exception as _e:
            db.rollback()
            print(f"[words] 今日新词例句懒生成失败({len(missing_new)}词): {_e}")

    new_items = []
    for w in new_candidates[:quota]:
        new_items.append({
            "word_id": w.id,
            "english": w.english,
            "chinese": w.chinese,
            "phonetic": w.phonetic,
            "mnemonic": w.mnemonic,
            "example_sentences": _parse_json_list(w.example_sentences),
            "learning_phase": "新学",
            "dimensions": {d: {"count": 0, "correct": 0, "accuracy": 0, "weak": True, "in_pool": False} for d in enabled},
            "recommended_dimensions": [enabled[rotation % len(enabled)]],
        })

    # ---- 已学词明细（供前端展示"哪些单词学过了"）----
    # 取该小孩有进度的词（含 learning_phase / 正确率），按最近复习时间倒序。
    # 这些词不会再出现在 new_words 里（new_words 只取无进度词），
    # 因此前端可以据此明确区分「新学」与「已学」。
    learned_rows = []
    for w in words:
        p = progress_map.get(w.id)
        if p is None:
            continue
        rc = p.review_count or 0
        cc = p.correct_count or 0
        # 只看过没答题（seen）也算"学过"——孩子确实学过了，只是还没测
        if rc == 0 and p.seen_at is None:
            continue
        if rc == 0:
            phase = "已学"
        else:
            phase = p.learning_phase or _get_accuracy_level(rc, cc)
        learned_rows.append({
            "word_id": w.id,
            "english": w.english,
            "chinese": w.chinese,
            "phonetic": w.phonetic,
            "learning_phase": phase,
            "review_count": rc,
            "correct_count": cc,
            "accuracy": round(cc * 100.0 / rc, 1) if rc else 0,
            "last_reviewed_at": p.last_reviewed_at.isoformat() if p.last_reviewed_at else None,
            "next_review_at": p.next_review_at.isoformat() if p.next_review_at else None,
            "seen_at": p.seen_at.isoformat() if p.seen_at else None,
            "in_attempt": bool(attempt_map.get(w.id)),
        })
    learned_rows.sort(key=lambda x: (x["last_reviewed_at"] or x["seen_at"] or ""), reverse=True)
    # learning_phase 文案映射（沿用四维记忆的阶段命名）
    phase_counts = {}
    for r in learned_rows:
        phase_counts[r["learning_phase"]] = phase_counts.get(r["learning_phase"], 0) + 1

    return {
        "date": now.strftime("%Y-%m-%d"),
        "enabled_dimensions": enabled,
        "per_word_dims": per_word_dims,
        "category_cap": category_cap,
        "due_count": len(due_words),
        "wrong_count": len(wrong_words),
        "new_quota": quota,
        "new_count": len(new_items),
        "total": len(items) + len(new_items),
        "task": items,
        "new_words": new_items,
        # 今日新词 id（review/start 可据此消费同一批词，保证"练的=显示的"）
        "new_word_ids": [w["word_id"] for w in new_items],
        # 已学词（含阶段标记，供前端"已学会的词"展示）
        "learned_words": learned_rows,
        "learned_count": len(learned_rows),
        "learned_phase_counts": phase_counts,
    }


@router.get("/{word_id}", response_model=WordResponse)
def get_word(word_id: int, user_id: Optional[int] = Query(None, description="小孩ID，不传则默认第一个小孩"), db: Session = Depends(get_db)):
    """获取单词详情（复习字段按小孩隔离）"""
    uid = _resolve_user_id(db, user_id)
    word = db.query(Word).filter(Word.id == word_id, Word.deleted == False).first()
    if not word:
        # 兜底：该 id 可能被 ops 同步软删（旧版全量替换导致 id 漂移）。
        # 按原行 english 找当前 active 行（同步后的新行）生成音频；词被彻底移除时
        # 用快照 english 现场 TTS，避免旧题目/进度引用的旧 id 直接 404。
        stale = db.query(Word).filter(Word.id == word_id).first()
        if stale and (stale.english or "").strip():
            live = db.query(Word).filter(
                func.lower(Word.english) == stale.english.strip().lower(),
                Word.deleted == False,
            ).first()
            word = live or stale
        else:
            raise HTTPException(status_code=404, detail="单词不存在")
    progress = _get_progress(db, word_id, uid)
    return {
        "id": word.id,
        "english": word.english,
        "chinese": word.chinese,
        "phonetic": word.phonetic,
        "grade": word.grade,
        "semester": word.semester,
        "phonetic_rule": word.phonetic_rule,
        "mnemonic": word.mnemonic,
        "word_root": word.word_root,
        "related_words": _parse_json_list(word.related_words),
        "example_sentences": _parse_json_list(word.example_sentences),
        "review_count": progress.review_count or 0,
        "correct_count": progress.correct_count or 0,
        "last_reviewed_at": progress.last_reviewed_at,
        "next_review_at": progress.next_review_at,
        "tags": word.tags,
        "created_at": word.created_at,
    }


@router.post("", response_model=WordResponse, status_code=201)
def create_word(data: WordCreate, db: Session = Depends(get_db)):
    """创建单词"""
    word = Word(
        english=data.english,
        chinese=data.chinese,
        phonetic=data.phonetic,
        grade=data.grade,
        semester=data.semester,
        unit=data.unit,
        unit_title=data.unit_title,
        phonetic_rule=data.phonetic_rule,
        mnemonic=data.mnemonic,
        word_root=data.word_root,
        related_words=_dump_json(data.related_words),
        example_sentences=_dump_json(data.example_sentences),
    )
    db.add(word)
    db.commit()
    db.refresh(word)

    # 处理标签关联
    if data.tag_ids:
        tags = db.query(Tag).filter(Tag.id.in_(data.tag_ids)).all()
        word.tags = tags
        db.commit()
        db.refresh(word)

    # 自动附带记忆增强（拼读规则/词根词源/相关词）：后台生成，不阻塞创建
    if _needs_enhance(word):
        _schedule_auto_enhance([word.id])

    # 异步预生成音频 + 获取音标
    import threading
    word_id = word.id
    word_english = word.english
    def _generate():
        try:
            from app.services.tts import tts_service
            from app.database import SessionLocal
            tts_service.generate_word_audio(word_english)
            # 从 Free Dictionary API 获取音标
            db2 = SessionLocal()
            w = db2.query(Word).filter(Word.id == word_id).first()
            if w and not w.phonetic:
                info = tts_service.get_word_info(word_english)
                if info and info.get("phonetic"):
                    w.phonetic = info["phonetic"]
                    db2.commit()
            db2.close()
        except Exception:
            pass
    threading.Thread(target=_generate, daemon=True).start()

    return word


class WordBatchCreate(BaseModel):
    """批量创建单词"""
    words: List[dict]  # 每个对象包含 english, chinese, phonetic, grade, semester, tag_ids
    grade: Optional[int] = None
    semester: Optional[int] = None
    tag_ids: Optional[List[int]] = []


@router.post("/extract-from-textbook")
async def extract_from_textbook(
    files: List[UploadFile] = File(...),
    grade: Optional[int] = Form(None),
    semester: Optional[int] = Form(None),
):
    """教材单词表提取（松耦合：独立于教材同步的知识点提取）。

    接收教材单词表页的照片 / PDF（可混合多份）→ 本地 RapidOCR → LLM 按单词表版式
    提取 {english, chinese, phonetic} → 按 english+grade+semester 标记已存在。
    照片/PDF 仅存临时目录，任务结束即删；不写入教材库。
    """
    import os
    import tempfile
    import threading
    from app.services import textbook_service

    tmpdir = tempfile.mkdtemp(prefix="word_extract_")
    try:
        pages = []  # (来源名, 文本)
        for f in files:
            if not f.filename:
                continue
            safe = os.path.basename(f.filename or "upload")
            path = os.path.join(tmpdir, safe)
            with open(path, "wb") as out:
                out.write(await f.read())
            ext = os.path.splitext(safe)[1].lower()
            if ext == ".pdf":
                import fitz
                ocr = textbook_service._get_ocr()
                doc = fitz.open(path)
                for i, page in enumerate(doc):
                    text = textbook_service._page_to_text(ocr, page)
                    if text.strip():
                        pages.append((f"{safe} 第{i + 1}页", text))
                doc.close()
            elif ext in (".jpg", ".jpeg", ".png", ".bmp", ".webp"):
                text = textbook_service.image_to_text(path)
                if text.strip():
                    pages.append((safe, text))
        if not pages:
            return {"words": [], "detail": "未能从图片/PDF 中识别出文字，请确认上传的是教材单词表页"}

        # LLM 按单词表版式提取
        combined = "\n".join(f"【{name}】\n{body}" for name, body in pages)
        if len(combined) > 30000:
            combined = combined[:24000] + "\n……（中略）……\n" + combined[-6000:]
        grade_cn = {1: "一年级", 2: "二年级", 3: "三年级", 4: "四年级", 5: "五年级", 6: "六年级",
                    7: "初一", 8: "初二", 9: "初三", 10: "高一", 11: "高二", 12: "高三"}.get(grade, "")
        sem_cn = {1: "上学期", 2: "下学期"}.get(semester, "")
        prompt = (
            "你是小学英语老师。以下是一本小学英语教材的【单元单词表】OCR 识别文本"
            "（可能含单词、音标、中文释义，扫描件识别可能有少量错字/排版错乱，请自行判断）。\n"
            f"教材年级：{grade_cn or '未知'}；学期：{sem_cn or '未知'}。\n"
            "请提取该单词表里的核心单词：\n"
            "1. 只列单词表中真实出现的词条，宁缺毋滥，不要臆造；\n"
            "2. 跳过页码、标题、装饰性文字、人名地名专有名词（除非是教材要求掌握的词）；\n"
            "3. 音标没有就留空字符串；中文释义从单词表/正文语义判断，一个词条一句话；\n"
            "4. 数量不超过 40 个。\n"
            "只输出 JSON：{\"words\":[{\"en\":\"apple\",\"cn\":\"苹果\",\"phonetic\":\"/ˈæpl/\"}]}\n"
            f"OCR 文本：\n{combined}"
        )
        content = textbook_service._llm_json(prompt, max_tokens=3000)
        data = textbook_service._parse_json(content)
        raw_words = data.get("words", []) if isinstance(data, dict) else []

        # 查重（english + grade + semester 全匹配才算已存在）
        from app.database import SessionLocal
        db = SessionLocal()
        try:
            results = []
            seen = set()
            for w in raw_words:
                en = str(w.get("en", "")).strip()
                cn = str(w.get("cn", "")).strip()
                if not en or en.lower() in seen:
                    continue
                seen.add(en.lower())
                existing = db.query(Word).filter(
                    Word.deleted == False,
                    func.lower(Word.english) == en.lower(),
                )
                if grade is not None:
                    existing = existing.filter(Word.grade == grade)
                if semester is not None:
                    existing = existing.filter(Word.semester == semester)
                exists = existing.first() is not None
                results.append({
                    "english": en,
                    "chinese": cn,
                    "phonetic": str(w.get("phonetic", "") or "").strip(),
                    "grade": grade,
                    "semester": semester,
                    "existing": exists,
                })
        finally:
            db.close()
        return {"words": results, "detail": f"识别到 {len(results)} 个单词（已存在 {sum(1 for r in results if r['existing'])} 个）"}
    finally:
        # 照片/PDF 仅临时使用，即用即删
        def _cleanup():
            import shutil
            shutil.rmtree(tmpdir, ignore_errors=True)
        threading.Thread(target=_cleanup, daemon=True).start()


@router.post("/batch")
def batch_create_words(data: WordBatchCreate, db: Session = Depends(get_db)):
    """批量创建单词"""
    success_count = 0
    fail_count = 0
    results = []
    created_ids = []

    for word_data in data.words:
        try:
            word = Word(
                english=word_data.get('english', ''),
                chinese=word_data.get('chinese', ''),
                phonetic=word_data.get('phonetic'),
                grade=word_data.get('grade') or data.grade,
                semester=word_data.get('semester') or data.semester,
                unit=word_data.get('unit'),
                unit_title=word_data.get('unit_title'),
                phonetic_rule=word_data.get('phonetic_rule'),
                mnemonic=word_data.get('mnemonic'),
                word_root=word_data.get('word_root'),
                related_words=_dump_json(word_data.get('related_words')),
                example_sentences=_dump_json(word_data.get('example_sentences')),
            )
            db.add(word)
            db.commit()
            db.refresh(word)

            # 处理标签
            tag_ids = word_data.get('tag_ids') or data.tag_ids
            if tag_ids:
                tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
                word.tags = tags
                db.commit()

            # 自动附带记忆增强：整批合并后台生成
            if _needs_enhance(word):
                created_ids.append(word.id)

            success_count += 1
            results.append({"english": word.english, "id": word.id, "success": True})
        except Exception as e:
            fail_count += 1
            results.append({"english": word_data.get('english', ''), "success": False, "error": str(e)})

    _schedule_auto_enhance(created_ids)

    # 异步预生成音频缓存
    import threading
    import concurrent.futures
    created_words = [r["english"] for r in results if r.get("success")]
    def _generate(word_text):
        try:
            from app.services.tts import tts_service
            tts_service.generate_word_audio(word_text)
        except Exception:
            pass
    def _batch_generate():
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            executor.map(_generate, created_words)
    threading.Thread(target=_batch_generate, daemon=True).start()

    return {
        "success_count": success_count,
        "fail_count": fail_count,
        "results": results
    }


@router.put("/{word_id}", response_model=WordResponse)
def update_word(word_id: int, data: WordUpdate, db: Session = Depends(get_db)):
    """更新单词"""
    word = db.query(Word).filter(Word.id == word_id, Word.deleted == False).first()
    if not word:
        # 兜底：该 id 可能被 ops 同步软删（旧版全量替换导致 id 漂移）。
        # 按原行 english 找当前 active 行（同步后的新行）生成音频；词被彻底移除时
        # 用快照 english 现场 TTS，避免旧题目/进度引用的旧 id 直接 404。
        stale = db.query(Word).filter(Word.id == word_id).first()
        if stale and (stale.english or "").strip():
            live = db.query(Word).filter(
                func.lower(Word.english) == stale.english.strip().lower(),
                Word.deleted == False,
            ).first()
            word = live or stale
        else:
            raise HTTPException(status_code=404, detail="单词不存在")

    update_data = data.model_dump(exclude_unset=True)
    tag_ids = update_data.pop('tag_ids', None)

    # related_words / example_sentences 是 JSON 文本列：List → 序列化
    if 'related_words' in update_data:
        update_data['related_words'] = _dump_json(update_data['related_words'])
    if 'example_sentences' in update_data:
        update_data['example_sentences'] = _dump_json(update_data['example_sentences'])

    for key, value in update_data.items():
        setattr(word, key, value)

    if tag_ids is not None:
        tags = db.query(Tag).filter(Tag.id.in_(tag_ids)).all()
        word.tags = tags

    db.commit()
    db.refresh(word)
    return word


@router.delete("/{word_id}", status_code=204)
def delete_word(
    word_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(require_admin),
):
    """删除单词（软删除）
    家长认证：学生（child）不能删除单词，必须家长（admin）操作
    """
    word = db.query(Word).filter(Word.id == word_id, Word.deleted == False).first()
    if not word:
        # 兜底：该 id 可能被 ops 同步软删（旧版全量替换导致 id 漂移）。
        # 按原行 english 找当前 active 行（同步后的新行）生成音频；词被彻底移除时
        # 用快照 english 现场 TTS，避免旧题目/进度引用的旧 id 直接 404。
        stale = db.query(Word).filter(Word.id == word_id).first()
        if stale and (stale.english or "").strip():
            live = db.query(Word).filter(
                func.lower(Word.english) == stale.english.strip().lower(),
                Word.deleted == False,
            ).first()
            word = live or stale
        else:
            raise HTTPException(status_code=404, detail="单词不存在")

    word.deleted = True
    db.commit()


@router.get("/{word_id}/audio")
def get_word_audio(word_id: int, db: Session = Depends(get_db)):
    """获取单词发音音频（带缓存）"""
    from fastapi.responses import FileResponse
    from app.services.tts import tts_service

    word = db.query(Word).filter(Word.id == word_id, Word.deleted == False).first()
    if not word:
        # 兜底：该 id 可能被 ops 同步软删（旧版全量替换导致 id 漂移）。
        # 按原行 english 找当前 active 行（同步后的新行）生成音频；词被彻底移除时
        # 用快照 english 现场 TTS，避免旧题目/进度引用的旧 id 直接 404。
        stale = db.query(Word).filter(Word.id == word_id).first()
        if stale and (stale.english or "").strip():
            live = db.query(Word).filter(
                func.lower(Word.english) == stale.english.strip().lower(),
                Word.deleted == False,
            ).first()
            word = live or stale
        else:
            raise HTTPException(status_code=404, detail="单词不存在")

    try:
        audio_path = tts_service.generate_word_audio(word.english)
        media_type = "audio/mpeg" if audio_path.endswith(".mp3") else "audio/wav"
        return FileResponse(audio_path, media_type=media_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"音频生成失败: {str(e)}")


@router.post("/generate-audio")
def generate_audio(grade: Optional[int] = None, db: Session = Depends(get_db)):
    """为所有单词批量预生成音频 + 音标（已缓存的跳过，后台异步执行）"""
    import os
    import threading
    from app.services.tts import tts_service

    query = db.query(Word).filter(Word.deleted == False)
    if grade:
        query = query.filter(Word.grade == grade)
    words = query.all()

    def _generate_all():
        from app.database import SessionLocal
        db2 = SessionLocal()
        words2 = db2.query(Word).filter(Word.deleted == False).all()
        if grade:
            words2 = [w for w in words2 if w.grade == grade]

        results = {"total": len(words2), "generated": 0, "skipped": 0, "failed": 0}
        for word in words2:
            text = word.english
            mp3 = os.path.join(tts_service.audio_dir, f"{text.lower()}.mp3")
            wav = os.path.join(tts_service.audio_dir, f"{text.lower()}.wav")
            if os.path.exists(mp3) or os.path.exists(wav):
                results["skipped"] += 1
            else:
                try:
                    tts_service.generate_word_audio(text)
                    results["generated"] += 1
                except Exception:
                    results["failed"] += 1
            # 补全音标
            if not word.phonetic:
                info = tts_service.get_word_info(text)
                if info and info.get("phonetic"):
                    word.phonetic = info["phonetic"]
        db2.commit()
        db2.close()
        print(f"[TTS] 批量预生成完成: {results}")

    threading.Thread(target=_generate_all, daemon=True).start()

    return {
        "total": len(words),
        "message": f"后台已开始生成，预计需要 {len(words) * 0.5:.0f} 秒"
    }


@router.get("/stats/summary", response_model=WordStatsResponse)
def get_stats(
    user_id: Optional[int] = Query(None, description="小孩ID（复习统计按该小孩；不传则默认第一个小孩）"),
    subject_id: Optional[int] = Query(None, description="按学科过滤（学习空间指定学科时）"),
    grade: Optional[int] = Query(None, ge=1, le=12, description="按年级过滤（学习空间指定年级时）"),
    db: Session = Depends(get_db),
):
    """获取单词统计（单词属于英语学科；指定其他学科时返回全零；复习数据按小孩隔离）"""
    uid = _resolve_user_id(db, user_id)
    # 学科过滤：仅英语学科有单词数据
    if subject_id is not None:
        from app.models.subject import Subject
        sub = db.query(Subject).filter(Subject.id == subject_id).first()
        sub_name = (sub.name or "").lower() if sub else ""
        if "英语" not in sub_name and "english" not in sub_name:
            return {
                "total_words": 0,
                "total_reviews": 0,
                "total_correct": 0,
                "accuracy": 0,
                "mastered_words": 0,
                "learning_words": 0,
                "new_words": 0,
                "grade_distribution": {},
                "review_today": 0,
                "due_words": 0,
                "to_review_count": 0,
            }

    def _wq(q):
        """Word 查询按年级过滤"""
        if grade is not None:
            q = q.filter(Word.grade == grade)
        return q

    def _pq(q):
        """WordProgress 查询按年级过滤（join Word）"""
        if grade is not None:
            q = q.join(Word, Word.id == WordProgress.word_id).filter(Word.deleted == False, Word.grade == grade)
        return q

    def _lq(q):
        """WordReviewLog 查询按小孩 + 年级过滤（join Word）"""
        q = q.filter(WordReviewLog.user_id == uid)
        if grade is not None:
            q = q.join(Word, Word.id == WordReviewLog.word_id).filter(Word.deleted == False, Word.grade == grade)
        return q

    # 总单词数（词库全局共享）
    total_words = _wq(db.query(Word).filter(Word.deleted == False)).count()

    # 总复习次数 = 练习场次数（排除已删除练习集）；指定年级时按该年级单词的复习日志数近似
    from app.models.practice_set import WordReviewSession, PracticeSet
    if grade is not None:
        total_reviews = (
            _lq(db.query(func.count(WordReviewLog.id)).filter(WordReviewLog.deleted == False))
            .scalar() or 0
        )
    else:
        total_reviews = (
            db.query(func.count(WordReviewSession.id))
            .outerjoin(PracticeSet, PracticeSet.id == WordReviewSession.practice_set_id)
            .filter(
                (WordReviewSession.practice_set_id.is_(None))
                | (PracticeSet.deleted == False)
            )
            .scalar() or 0
        )
    total_correct = _lq(db.query(WordReviewLog).filter(WordReviewLog.deleted == False, WordReviewLog.is_correct == True)).count()
    total_logs = _lq(db.query(WordReviewLog).filter(WordReviewLog.deleted == False)).count()

    # 正确率
    accuracy = (total_correct / total_logs * 100) if total_logs > 0 else 0

    # 各状态单词数（按该小孩进度：掌握/学习中/新词）
    mastered_words = _pq(db.query(WordProgress).filter(
        WordProgress.user_id == uid,
        WordProgress.review_count >= 5,
        WordProgress.correct_count / WordProgress.review_count >= 0.9
    )).count()

    # 该小孩复习过的词数（有进度且 review_count>0）
    reviewed_words_count = _pq(db.query(WordProgress).filter(
        WordProgress.user_id == uid,
        WordProgress.review_count > 0
    )).count()

    # 新词 = 词库中该小孩从未复习（或进度为0）的词
    new_words = total_words - reviewed_words_count

    # 学习中 = 复习过但未达掌握
    learning_words = reviewed_words_count - mastered_words

    # 今日复习数（该小孩）
    today = datetime.now().date()
    review_today = _lq(db.query(WordReviewLog).filter(
        WordReviewLog.deleted == False,
        func.date(WordReviewLog.reviewed_at) == today
    )).count()

    # 待复习数（该小孩，超过预定复习时间）
    now = datetime.now()
    due_words = _pq(db.query(WordProgress).filter(
        WordProgress.user_id == uid,
        WordProgress.next_review_at != None,
        WordProgress.next_review_at <= now
    )).count()

    # 待复习数量 = 未复习（新词）+ 曲线到期（该小孩）
    unreviewed_count = total_words - reviewed_words_count
    to_review_count = unreviewed_count + due_words

    # 年级分布（词库全局）
    grade_dist = {}
    words_by_grade = _wq(db.query(Word.grade, func.count(Word.id)).filter(
        Word.deleted == False,
        Word.grade != None
    )).group_by(Word.grade).all()
    for grade, count in words_by_grade:
        grade_dist[str(grade)] = count

    return {
        "total_words": total_words,
        "total_reviews": total_reviews,
        "total_correct": total_correct,
        "accuracy": round(accuracy, 1),
        "mastered_words": mastered_words,
        "learning_words": learning_words,
        "new_words": new_words,
        "grade_distribution": grade_dist,
        "review_today": review_today,
        "due_words": due_words,
        "to_review_count": to_review_count,
    }


def _build_review_questions(selected_words: list, db: Session) -> list:
    """把选中的单词构建成复习题目（选择题带 3 个干扰项）

    干扰项从全库取（不限于本次选中的词），保证 4 选 1 始终成立。
    """
    all_words = db.query(Word).filter(Word.deleted == False).all()  # noqa: E712
    questions = []
    for word in selected_words:
        other_words = [w for w in all_words if w.id != word.id]
        options = None
        if len(other_words) >= 3:
            wrong_options = random.sample(other_words, 3)
            options = [w.chinese for w in wrong_options] + [word.chinese]
            random.shuffle(options)

        questions.append(ReviewQuestion(
            word_id=word.id,
            english=word.english,
            chinese=word.chinese,
            word_length=len(word.english),
            options=options
        ))
    return questions


@router.post("/learn/seen")
def mark_words_seen(
    payload: dict,
    user_id: Optional[int] = Query(None, description="小孩ID（不传则用 payload.user_id 或默认第一个小孩）"),
    db: Session = Depends(get_db),
):
    """标记单词为「已学（看过）」——今日任务学词卡翻到即调用。

    语义：只写 seen_at，**不改** review_count / 正确率 / 记忆曲线
    （那些只由 /review/submit 的答题结果更新）。
    效果：被标记的词立刻离开「新词学习」池，不会出现"看了一遍没答题、
    下次点开又从头开始"。
    """
    uid = _resolve_user_id(db, user_id if user_id is not None else payload.get("user_id"))
    ids = payload.get("word_ids") or []
    if isinstance(ids, (int, str)):
        ids = [ids]
    try:
        ids = [int(i) for i in ids if str(i).strip().isdigit()]
    except Exception:
        ids = []
    if not ids:
        return {"ok": True, "marked": 0}

    now = datetime.now()
    existing = {
        p.word_id: p for p in db.query(WordProgress).filter(
            WordProgress.user_id == uid,
            WordProgress.word_id.in_(ids),
        ).all()
    }
    marked = 0
    for wid in ids:
        p = existing.get(wid)
        if p is None:
            p = WordProgress(user_id=uid, word_id=wid, review_count=0, correct_count=0,
                             learning_phase="已学", seen_at=now)
            db.add(p)
            marked += 1
        elif p.seen_at is None:
            p.seen_at = now
            # 尚未答题的词，阶段显示为「已学」（答题后会由 review/submit 覆盖）
            if (p.review_count or 0) == 0:
                p.learning_phase = "已学"
            marked += 1
    db.commit()
    return {"ok": True, "marked": marked, "user_id": uid}


@router.post("/review/start", response_model=ReviewStartResponse)
def start_review(
    count: int = Query(25, ge=10, le=100, description="复习单词数量"),
    user_id: Optional[int] = Query(None, description="小孩ID（复习进度按该小孩抽样；不传则默认第一个小孩）"),
    grade: Optional[int] = Query(None, description="按年级筛选"),
    word_ids: Optional[str] = Query(None, description="指定单词ID，多个用逗号分隔"),
    category: Optional[str] = Query(None, description="今日任务分类：new=新词学习 / due=到期复习 / wrong=错词复习；"
                                                     "传入时按今日任务池出词，保证「练的=今日任务显示的」"),
    db: Session = Depends(get_db)
):
    """开始复习 - 智能抽取单词，优先抽取该小孩未复习和低正确率的单词"""
    uid = _resolve_user_id(db, user_id)
    query = db.query(Word).filter(Word.deleted == False)

    # 今日任务分类出词：直接消费 daily-task 决定的同一批词。
    # 这是修复「学过的词一直留在今日学习」的关键——旧实现里 review/start 从
    # 全库随机抽、daily-task 按 id 取头，两池互不相交，导致练的词和显示的
    # 新词永远是两批，练完也不影响今日学习列表。
    if category in ("new", "due", "wrong"):
        pool = daily_task(
            user_id=uid, grade=grade, dimensions=None, new_quota=5,
            per_word_dims=1, category_cap=15, db=db,
        )
        if category == "new":
            pool_ids = pool["new_word_ids"]
        else:
            want_wrong = (category == "wrong")
            pool_ids = [t["word_id"] for t in pool["task"]
                        if bool(t["in_attempt"]) == want_wrong]
        if pool_ids:
            words = db.query(Word).filter(
                Word.id.in_(pool_ids), Word.deleted == False
            ).all()
            # 按 pool 顺序输出，并把数量收敛到 count
            order = {wid: i for i, wid in enumerate(pool_ids)}
            words.sort(key=lambda w: order.get(w.id, 1 << 30))
            words = words[:max(count, 1)]
            review_session = WordReview(user_id=uid, total_count=len(words))
            db.add(review_session)
            db.commit()
            db.refresh(review_session)
            return {
                "session_id": review_session.id,
                "questions": _build_review_questions(words, db),
                "total": len(words),
            }

    # 如果指定了单词ID，使用指定的单词（不走智能抽样）
    if word_ids:
        id_list = [int(t.strip()) for t in word_ids.split(',') if t.strip().isdigit()]
        if id_list:
            query = query.filter(Word.id.in_(id_list))

    if grade:
        query = query.filter(Word.grade == grade)

    all_words = query.all()

    if len(all_words) == 0:
        raise HTTPException(status_code=400, detail="没有可复习的单词")

    # 批量读取该小孩进度
    progress_map = {
        p.word_id: p for p in db.query(WordProgress).filter(
            WordProgress.user_id == uid,
            WordProgress.word_id.in_([w.id for w in all_words]),
        ).all()
    }

    # 如果指定了单词ID且数量足够，直接使用；否则使用智能抽样
    if word_ids and len(all_words) <= count:
        selected_words = all_words
    else:
        # 新算法：按优先级抽取（基于该小孩进度）
        pool_unreviewed = []  # 未复习
        pool_due = []         # 曲线到期
        pool_low_acc = []     # 低正确率(<60%)
        pool_other = []       # 其他

        now = datetime.now()
        for w in all_words:
            p = progress_map.get(w.id)
            review_count = p.review_count if p else 0
            correct_count = p.correct_count if p else 0
            next_review_at = p.next_review_at if p else None
            accuracy = (correct_count / review_count * 100) if review_count and review_count > 0 else 0
            if review_count == 0:
                pool_unreviewed.append(w)
            elif next_review_at and next_review_at <= now:
                pool_due.append(w)
            elif accuracy < 60:
                pool_low_acc.append(w)
            else:
                pool_other.append(w)

        selected_words = []
        remaining_count = min(count, len(all_words))

        # 1. 优先从未复习抽取
        a_count = min(len(pool_unreviewed), remaining_count)
        if a_count > 0:
            selected_words.extend(random.sample(pool_unreviewed, a_count))
            remaining_count -= a_count

        # 2. 曲线到期单词
        if remaining_count > 0:
            d_count = min(len(pool_due), remaining_count)
            if d_count > 0:
                selected_words.extend(random.sample(pool_due, d_count))
                remaining_count -= d_count

        # 3. 低正确率
        if remaining_count > 0:
            b_count = min(len(pool_low_acc), remaining_count)
            if b_count > 0:
                selected_words.extend(random.sample(pool_low_acc, b_count))
                remaining_count -= b_count

        # 4. 随机其他
        if remaining_count > 0:
            o_count = min(len(pool_other), remaining_count)
            if o_count > 0:
                selected_words.extend(random.sample(pool_other, o_count))

    # 创建复习场次（按小孩）
    review_session = WordReview(user_id=uid, total_count=len(selected_words))
    db.add(review_session)
    db.commit()
    db.refresh(review_session)

    # 构建题目
    questions = _build_review_questions(selected_words, db)

    return {
        "session_id": review_session.id,
        "questions": questions,
        "total": len(questions)
    }


@router.post("/review/submit")
def submit_review(data: ReviewSessionSubmit, db: Session = Depends(get_db)):
    """提交复习结果（复习进度写入该小孩的 WordProgress；若未指定 user_id 则默认第一个小孩）"""
    from app.models import PracticeSet, WordReviewSession, Subject
    from app.models.tag import Tag

    uid = _resolve_user_id(db, data.user_id)
    correct_count = 0
    error_count = 0
    now = datetime.now()

    # 获取复习的单词列表
    reviewed_words = []
    for result in data.results:
        word = db.query(Word).filter(Word.id == result.word_id, Word.deleted == False).first()
        if not word:
            continue
        reviewed_words.append(word)

        # 记录复习日志（按小孩）
        log = WordReviewLog(
            word_id=result.word_id,
            user_id=uid,
            is_correct=result.is_correct,
            user_answer=result.user_answer,
            review_type=result.review_type,
            reviewed_at=now
        )
        db.add(log)

        # 读取/创建该小孩进度
        progress = _get_progress(db, result.word_id, uid)

        # 增加复习次数（每次复习都要增加）
        progress.review_count = (progress.review_count or 0) + 1

        # 四维记忆：按题型归类更新对应维度计数 + 记忆错词池
        dim = _dimension_for_review_type(result.review_type)
        dim_count, dim_correct = _DIMENSION_FIELDS[dim]
        setattr(progress, dim_count, (getattr(progress, dim_count) or 0) + 1)
        if result.is_correct:
            setattr(progress, dim_correct, (getattr(progress, dim_correct) or 0) + 1)
            _clear_word_attempt(db, result.word_id, uid, dim)  # 答对 → 移出记忆错词池
        else:
            _upsert_word_attempt(db, word, uid, dim, "review")

        # 更新间隔和阶段
        if result.is_correct:
            progress.correct_count = (progress.correct_count or 0) + 1
            correct_count += 1
            # 间隔推进：
            #  - 牢记阶段按 5→10→15→20→30→60 阶梯（防短期记忆，不再 30 天封顶）
            #  - 其余阶段艾宾浩斯加倍，最多 30 天
            if progress.learning_phase == MASTERED_PHASE:
                progress.interval = _next_mastered_interval(progress.interval, True)
            else:
                progress.interval = min((progress.interval or 1) * 2, 30)
            # 更新阶段
            consecutive_correct = _get_consecutive_correct(word.id, uid, db)
            if consecutive_correct >= 3 and progress.interval >= 7:
                progress.learning_phase = MASTERED_PHASE
            elif progress.next_review_at and progress.next_review_at <= datetime.now():
                progress.learning_phase = "遗忘点"
            else:
                progress.learning_phase = "在途"
        else:
            error_count += 1
            if progress.learning_phase == MASTERED_PHASE:
                # 牢记抽查答错：它曾掌握过，不必从 1 天重来
                progress.interval = MASTERED_RELAPSE_INTERVAL
            else:
                progress.interval = 1  # 错误后重置为1天
            progress.learning_phase = "在途"  # 退回在途

        # 计算下次复习时间
        progress.last_reviewed_at = now
        progress.next_review_at = datetime(
            now.year, now.month, now.day
        ) + timedelta(days=progress.interval)

    # 更新复习场次
    review_session = db.query(WordReview).filter(WordReview.id == data.session_id).first()
    if review_session:
        review_session.correct_count = correct_count
        review_session.error_count = error_count
        review_session.duration = data.duration

    # 计算正确率
    accuracy = round(correct_count / len(data.results) * 100, 1) if data.results else 0

    # 触发积分行为和成就检查
    from app.services.motivation import MotivationService
    try:
        service = MotivationService(db)
        # 背单词：每次复习场次 +积分
        service.trigger_action("review_word", user_id=uid, reason="背单词")
        # 单词复习通过练习集完成会计入review_practice_set（需至少10个单词才积分）
        if len(data.results) >= 10:
            service.trigger_action("review_practice_set", user_id=uid, reason="单词练习")

        # 检查单词正确率成就（满足条件时触发）
        if len(data.results) >= 10 and accuracy >= 90:
            service.check_word_accuracy(
                user_id=uid,
                total_count=len(data.results),
                correct_count=correct_count,
                reason=f"单词正确率{accuracy}%"
            )
    except Exception as e:
        pass  # 激励系统不影响主流程

    # 创建练习集记录（单词复习也认为是练习集）
    if reviewed_words:
        # 查找英语学科（单词复习归为英语学科）
        subject = db.query(Subject).filter(Subject.name == "英语", Subject.deleted == False).first()
        subject_id = subject.id if subject else 1  # 默认数学

        # 创建练习集
        practice_set = PracticeSet(
            name=f"单词复习 {now.strftime('%Y-%m-%d %H:%M')}",
            user_id=uid,  # 归属小孩（数据隔离）
            subject_id=subject_id,
            source_type="word",  # 标记为单词来源
            question_type="original",
            total_questions=len(reviewed_words),
            reviewed=True,
            review_count=1,
        )
        db.add(practice_set)
        db.commit()
        db.refresh(practice_set)

        # 创建单词复习场次关联记录
        word_review_session = WordReviewSession(
            practice_set_id=practice_set.id,
            session_id=review_session.id if review_session else 0,
            total_count=len(reviewed_words),
            correct_count=correct_count,
            accuracy=int(accuracy),
            duration=data.duration or 0,
            reviewed_at=now,
            word_results=json.dumps([
                {"word_id": r.word_id, "is_correct": bool(r.is_correct)}
                for r in data.results
            ], ensure_ascii=False),
        )
        db.add(word_review_session)
        db.commit()

    db.commit()

    return {
        "total": len(data.results),
        "correct": correct_count,
        "error": error_count,
        "accuracy": accuracy
    }


@router.post("/print-pdf")
def print_pdf(
    count: int = Query(25, ge=1, le=100),
    grade: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """生成单词默写PDF"""
    from app.services.pdf import generate_word_print_pdf

    query = db.query(Word).filter(Word.deleted == False)
    if grade:
        query = query.filter(Word.grade == grade)

    all_words = query.all()
    selected_words = random.sample(all_words, min(count, len(all_words)))

    # 构建数据
    words_data = [{
        "chinese": w.chinese,
        "english": w.english,
        "length": len(w.english)
    } for w in selected_words]

    pdf_path = generate_word_print_pdf("单词默写", words_data)

    return {"pdf_url": f"/uploads/{pdf_path}"}


# ---------------------------------------------------------------- AI 智能导入

_GRADE_CN = {1: "一年级", 2: "二年级", 3: "三年级", 4: "四年级", 5: "五年级", 6: "六年级",
             7: "初一", 8: "初二", 9: "初三", 10: "高一", 11: "高二", 12: "高三"}
_SEM_CN = {1: "上学期", 2: "下学期"}


def _strip_md_code(text: str) -> str:
    """剥掉 LLM 返回里的 markdown 代码块"""
    m = re.search(r"```[a-zA-Z]*\s*(.*?)```", text, re.DOTALL)
    if m:
        return m.group(1).strip()
    return text.strip()


def parse_llm_words(text: str) -> list:
    """把 LLM 输出的「Unit 标题行 + 英文 中文」文本解析为结构化单词列表（与前端 smartParseWords 同规则）"""
    words = []
    cur_unit = None
    cur_title = ""
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        um = re.match(r"^Unit\s*(\d+)\s*(.*)$", line, re.I)
        if um:
            cur_unit = int(um.group(1))
            cur_title = (um.group(2) or "").strip()
            continue
        idx = re.search(r"[\u4e00-\u9fa5\u3000-\u303f\uff00-\uffef]", line)
        if idx:
            english = line[:idx.start()].strip()
            chinese = line[idx.start():].strip()
            english = re.sub(r"\s*\([^)]*\)\s*$", "", english).strip()
            op = english.rfind("(")
            if op >= 0 and ")" not in english[op:]:
                chinese = english[op:] + chinese
                english = english[:op].strip()
            cm = re.match(r"^(.*\s)([A-Z])$", english)
            if cm and re.match(r"^[\u4e00-\u9fa5]", chinese):
                english = cm.group(1).strip()
                chinese = cm.group(2) + chinese
            if english or chinese:
                words.append({"english": english, "chinese": chinese, "unit": cur_unit, "unit_title": cur_title})
        else:
            words.append({"english": line, "chinese": "", "unit": cur_unit, "unit_title": cur_title})
    return words


@router.post("/ai-generate")
def ai_generate_words(req: WordAIGenerateRequest):
    """AI 智能导入：大模型按教材知识/自然语言指令生成单元单词表"""
    if req.mode == "textbook":
        if not req.subject or not req.version or not req.grade:
            raise HTTPException(status_code=400, detail="教材模式需要选择：学科、版本、年级（册次可选）")
        grade_cn = _GRADE_CN.get(req.grade, "")
        sem_cn = _SEM_CN.get(req.semester, "") if req.semester else ""
        desc = f"{req.subject}《{req.version}》{grade_cn}{sem_cn or '全一册'}"
        task = f"教材：{desc}\n请依据这套教材的真实内容，生成该册全册的单元单词表。"
    else:
        if not req.instruction or not req.instruction.strip():
            raise HTTPException(status_code=400, detail="请先输入导入指令，例如：我要导入沪教版深圳英语三年级上册 全册")
        task = f"用户指令：{req.instruction.strip()}"

    prompt = (
        "你是精通国内各版本中小学教材的英语老师，熟悉各版本各年级教材的单元结构与词汇表。\n"
        f"{task}\n"
        "要求：\n"
        "1. 按单元组织，覆盖该册全部单元；每个单元先输出一行标题，格式：Unit 1 标题（标题用教材里的英文单元名，没有英文标题时用单元主题中文名）\n"
        "2. 标题行之后每行一个单词，格式：英文 中文释义（可把音标放在英文后面，如 apple /ˈæpl/，可选）\n"
        "3. 只列该教材该册要求掌握的核心单词（词汇表为主），宁缺毋滥，不要臆造不在该教材的词；短语整体保留（如 a pair of 一双）\n"
        "4. 中文释义一句话，必要时带括号补充（如 tooth 牙齿(复数teeth)）\n"
        "5. 单词数量以该册实际词汇量为准，一般每单元 8~15 个\n"
        "只输出单词表文本，严禁输出任何解释、提示、markdown 代码块，格式示例：\n"
        "Unit 1 Meeting new people\n"
        "meet 相识；结识\n"
        "new 新的\n"
        "……"
    )
    try:
        raw = _strip_md_code(_llm_json(prompt, system="你只输出单词表文本，不要任何解释。", max_tokens=4000, timeout=180))
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI 生成失败：{e}")

    words = parse_llm_words(raw)
    if not words:
        raise HTTPException(status_code=502, detail="AI 返回内容无法解析为单词，请重试")

    # 查重标记（english + grade + semester 全匹配算已存在）
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        seen = set()
        out = []
        for w in words:
            en = (w.get("english") or "").strip()
            cn = (w.get("chinese") or "").strip()
            key = (en.lower(), cn)
            if not en or key in seen:
                continue
            seen.add(key)
            exists = db.query(Word).filter(
                Word.deleted == False,
                func.lower(Word.english) == en.lower(),
            )
            if req.grade is not None:
                exists = exists.filter(Word.grade == req.grade)
            if req.semester is not None:
                exists = exists.filter(Word.semester == req.semester)
            out.append({
                "english": en,
                "chinese": cn,
                "phonetic": "",
                "unit": w.get("unit"),
                "unit_title": w.get("unit_title") or "",
                "existing": exists.first() is not None,
            })
        db.close()
    finally:
        pass

    return {"words": out, "total": len(out)}





# ============================================================ 记忆专项（P2）
# —— 记忆增强自动附带：新增/导入单词时后台自动生成（拼读规则/词根词源/相关词），
#    不再需要独立操作。`POST /enhance` 保留仅用于历史数据补增强。
_ENHANCE_CHUNK = 20          # 每次 LLM 调用处理的单词数
_ENHANCE_DEBOUNCE = 4.0      # 秒：等待同一批导入全部落库后合并生成，减少 LLM 调用
_enhance_pending: set = set()
_enhance_lock = threading.Lock()
_enhance_worker_running = False


def _needs_enhance(word) -> bool:
    """拼读规则与词根词源都缺失才算待增强；有任一字段视为已人工编辑，不覆盖"""
    return not (word.phonetic_rule and word.word_root)


def _needs_sentences(word) -> bool:
    """例句缺失才算待补（有例句视为已生成/已编辑，不覆盖）"""
    return not _parse_json_list(word.example_sentences)


def _enhance_words_llm(db: Session, words: List[Word]) -> dict:
    """对一组单词调用 LLM 生成记忆增强，就地更新内存对象（由调用方 commit）。

    words 必须已在 db 中；建议单次不超过 _ENHANCE_CHUNK 个。失败抛异常，由调用方决定回滚/包装。
    """
    if not words:
        return {"ok_count": 0, "results": [], "total": 0}
    word_lines = "\n".join(f"- {w.english} / {w.phonetic or ''} / {w.chinese}" for w in words)
    prompt = (
        "你是小学英语特级教师，擅长自然拼读与词根词源。为下列小学英语单词批量生成「记忆增强包」：\n"
        "1. phonetic_rule：拼读规则，按字母组合逐段拆解怎么读，每个字母组合一行（如 apple：a → /æ/，pp → /p/，le → /əl/ 结尾弱化；再如 ee → /iː/，ee 组合读长音 iː）；这是学生见词能读的关键，必须准确；\n"
        "2. word_root：词根词缀拆解（有就写，如 un-（否定）+ happy → unhappy）；若是 apple 这类没有词根的基础词，写词源简史（如 apple ← 古英语 æppel），绝不硬凑词根；\n"
        "3. related_words：相关词/形近词数组（1~3 个，形近或同类，如 [{\"en\":\"see\",\"cn\":\"看见\"}]）；\n"
        "4. example_sentences：语境例句数组（1~2 条，把该单词融入句子里学，不孤立背词）。要求：语法绝对正确、口语自然、贴近低年级孩子生活；句子只用孩子已学的高频词 + 当前单词（新词最多再带 1 个生词），难度恰到好处（i+1）；中文翻译自然通顺。\n"
        "要求：面向一年级小学生，拼读拆解简单准确、中文简单；不写联想口诀、不编顺口溜；例句严禁出现语法错误（如 I like to eat apples. 而不是 I like eat apple）。\n"
        f"单词表：\n{word_lines}\n"
        "只输出 JSON：{\"words\":[{\"english\":\"bee\",\"phonetic_rule\":\"...\","
        "\"word_root\":\"...\",\"related_words\":[{\"en\":\"see\",\"cn\":\"看见\"}],"
        "\"example_sentences\":[{\"en\":\"I like to eat apples.\",\"zh\":\"我喜欢吃苹果。\"}]}]}"
    )
    try:
        content = _llm_json(prompt, system="你只输出JSON，不要任何解释。", max_tokens=4000, timeout=180)
        data_resp = json.loads(_strip_md_code(content)) if isinstance(content, str) else content
    except Exception as e:
        raise Exception(f"AI 生成失败：{e}")

    by_en = {w.english.lower(): w for w in words}
    results, ok_count = [], 0
    for item in data_resp.get("words", []) if isinstance(data_resp, dict) else []:
        en = str(item.get("english", "")).strip().lower()
        word = by_en.get(en)
        if not word:
            continue
        word.phonetic_rule = str(item.get("phonetic_rule", "") or "").strip()
        word.word_root = str(item.get("word_root", "") or "").strip()
        word.related_words = _dump_json(item.get("related_words") or [])
        word.example_sentences = _dump_json(item.get("example_sentences") or [])
        results.append({"id": word.id, "english": word.english, "ok": True})
        ok_count += 1
    return {"ok_count": ok_count, "results": results, "total": len(words)}


def _fill_sentences_llm(db: Session, words: List[Word]) -> dict:
    """只补语境例句（对已有拼读/词根字段、仅缺例句的词）：不覆盖任何已编辑字段"""
    if not words:
        return {"ok_count": 0, "results": [], "total": 0}
    word_lines = "\n".join(f"- {w.english} / {w.phonetic or ''} / {w.chinese}" for w in words)
    prompt = (
        "你是小学英语特级教师。为下列小学英语单词批量生成「语境例句」，把单词融入句子里学，不孤立背词：\n"
        "1. 每个单词 1~2 条例句（example_sentences 数组）；\n"
        "2. 语法绝对正确、口语自然、贴近低年级孩子生活；句子只用孩子已学的高频词 + 当前单词（最多再带 1 个生词），难度恰到好处（i+1）；\n"
        "3. 中文翻译自然通顺；\n"
        "4. 严禁语法错误（如 I like to eat apples. 而不是 I like eat apple）。\n"
        f"单词表：\n{word_lines}\n"
        "只输出 JSON：{\"words\":[{\"english\":\"bee\","
        "\"example_sentences\":[{\"en\":\"The bee is on the flower.\",\"zh\":\"蜜蜂在花上。\"}]}]}"
    )
    try:
        content = _llm_json(prompt, system="你只输出JSON，不要任何解释。", max_tokens=4000, timeout=180)
        data_resp = json.loads(_strip_md_code(content)) if isinstance(content, str) else content
    except Exception as e:
        raise Exception(f"AI 生成失败：{e}")

    by_en = {w.english.lower(): w for w in words}
    results, ok_count = [], 0
    for item in data_resp.get("words", []) if isinstance(data_resp, dict) else []:
        en = str(item.get("english", "")).strip().lower()
        word = by_en.get(en)
        if not word:
            continue
        word.example_sentences = _dump_json(item.get("example_sentences") or [])
        results.append({"id": word.id, "english": word.english, "ok": True})
        ok_count += 1
    return {"ok_count": ok_count, "results": results, "total": len(words)}


def _schedule_auto_enhance(word_ids):
    """新增/导入后登记待增强单词；去抖合并成一批，由后台线程自动生成（静默失败）"""
    if not word_ids:
        return
    global _enhance_worker_running
    with _enhance_lock:
        _enhance_pending.update(word_ids)
        if _enhance_worker_running:
            return
        _enhance_worker_running = True
    threading.Thread(target=_auto_enhance_worker, daemon=True).start()


def _auto_enhance_worker():
    global _enhance_worker_running
    try:
        from app.database import SessionLocal
        while True:
            time.sleep(_ENHANCE_DEBOUNCE)  # 等同一批导入全部落库，合并成一次 LLM 调用
            with _enhance_lock:
                ids = list(_enhance_pending)
                _enhance_pending.clear()
            if not ids:
                break
            db = SessionLocal()
            try:
                words = db.query(Word).filter(Word.id.in_(ids), Word.deleted == False).all()  # noqa: E712
                need = [w for w in words if _needs_enhance(w)]
                need_sent = [w for w in words if not _needs_enhance(w) and _needs_sentences(w)]
                for i in range(0, len(need), _ENHANCE_CHUNK):
                    _enhance_words_llm(db, need[i:i + _ENHANCE_CHUNK])
                    db.commit()
                for i in range(0, len(need_sent), _ENHANCE_CHUNK):
                    _fill_sentences_llm(db, need_sent[i:i + _ENHANCE_CHUNK])
                    db.commit()
            finally:
                db.close()
    except Exception:
        # 记忆增强是增值内容，失败不影响单词本身；打日志便于排查（如 LLM 欠费 402）
        import traceback
        print(f"[word] 自动记忆增强失败: {traceback.format_exc()}")
    finally:
        with _enhance_lock:
            _enhance_worker_running = False
            if _enhance_pending:  # 处理期间又有新词登记 → 立刻再起一轮
                _enhance_worker_running = True
                threading.Thread(target=_auto_enhance_worker, daemon=True).start()


class WordEnhanceRequest(BaseModel):
    """AI 批量生成记忆增强（纯手动触发）：按单词ID列表或年级条件"""
    word_ids: Optional[List[int]] = None
    grade: Optional[int] = None
    semester: Optional[int] = None
    limit: int = 20


class MemoryReviewStartResponse(BaseModel):
    """记忆模式复习开始"""
    total: int
    items: List[dict]  # [{word_id, english, chinese, phonetic, mnemonic, word_root, hint}]


class MemoryReviewSubmitRequest(BaseModel):
    """记忆模式复习提交（逐词或整场）"""
    word_id: int
    correct: bool
    user_id: Optional[int] = None


@router.post("/enhance")
def ai_enhance_words(data: WordEnhanceRequest, db: Session = Depends(get_db)):
    """AI 批量生成记忆增强（拼读规则/词根词源/相关词/语境例句）。

    保留用于历史数据补增强；新增/导入单词已在后台自动生成，无需手动触发。
    已有增强但缺例句的词，自动补例句（不覆盖已编辑字段）。
    """
    query = db.query(Word).filter(Word.deleted == False)  # noqa: E712
    if data.word_ids:
        query = query.filter(Word.id.in_(data.word_ids))
    if data.grade is not None:
        query = query.filter(Word.grade == data.grade)
    if data.semester is not None:
        query = query.filter(Word.semester == data.semester)
    words = query.order_by(Word.grade.asc(), Word.id).limit(max(1, min(data.limit, 50))).all()
    need = [w for w in words if _needs_enhance(w)]
    need_sent = [w for w in words if not _needs_enhance(w) and _needs_sentences(w)]
    if not need and not need_sent:
        return {"results": [], "ok_count": 0, "detail": "没有待增强的单词（可先清空筛选条件或换一批）"}

    results, ok_count = [], 0
    try:
        for i in range(0, len(need), _ENHANCE_CHUNK):
            r = _enhance_words_llm(db, need[i:i + _ENHANCE_CHUNK])
            ok_count += r["ok_count"]
            results.extend(r["results"])
        for i in range(0, len(need_sent), _ENHANCE_CHUNK):
            r = _fill_sentences_llm(db, need_sent[i:i + _ENHANCE_CHUNK])
            ok_count += r["ok_count"]
            results.extend(r["results"])
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=502, detail=str(e))
    return {"results": results, "ok_count": ok_count, "total": len(words), "detail": f"成功增强 {ok_count} 个单词"}


@router.post("/memory-review/submit")
def memory_review_submit(data: MemoryReviewSubmitRequest, db: Session = Depends(get_db)):
    """记忆模式复习提交：按结果更新该小孩 word_progress（艾宾浩斯曲线），并写复习日志"""
    uid = _resolve_user_id(db, data.user_id)
    word = db.query(Word).filter(Word.id == data.word_id, Word.deleted == False).first()
    if not word:
        raise HTTPException(status_code=404, detail="单词不存在")
    progress = _get_progress(db, data.word_id, uid)

    progress.review_count = (progress.review_count or 0) + 1
    if data.correct:
        progress.correct_count = (progress.correct_count or 0) + 1
    now = datetime.now()
    progress.last_reviewed_at = now

    # 艾宾浩斯：正确间隔翻倍、错误重置为1天
    interval = progress.interval or 1
    if data.correct:
        interval = min(interval * 2, 30)
    else:
        interval = 1
    progress.interval = interval
    progress.next_review_at = now + timedelta(days=interval)
    acc = progress.correct_count * 100.0 / progress.review_count
    progress.learning_phase = _get_accuracy_level(progress.review_count, progress.correct_count)

    log = WordReviewLog(
        word_id=word.id,
        user_id=uid,
        is_correct=data.correct,
        review_type=3,  # 3=记忆模式
    )
    db.add(log)
    db.commit()
    return {
        "message": "ok",
        "word_id": word.id,
        "review_count": progress.review_count,
        "correct_count": progress.correct_count,
        "learning_phase": progress.learning_phase,
        "next_review_at": progress.next_review_at,
    }
