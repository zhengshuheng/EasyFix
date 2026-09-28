"""
记忆模式复习路由（独立文件避免与 /words/{word_id} 路由冲突）

prefix=/api/words，须在 word_router 之前注册：
  GET  /api/words/memory-review       待复习词（有口诀，按小孩进度排序）
  POST /api/words/memory-review/submit 提交结果 → word_progress 艾宾浩斯更新
"""
import json
from datetime import datetime, timedelta
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy import func
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.database import get_db
from app.models import Word, WordReviewLog
from app.models.word import WordProgress
from app.models.user import User
from app.routers.word import _resolve_user_id, _get_progress, _get_accuracy_level

router = APIRouter(prefix="/api/words", tags=["单词记忆专项"])


def _parse_json_list(raw) -> list:
    if not raw:
        return []
    try:
        v = json.loads(raw)
        return v if isinstance(v, list) else []
    except Exception:
        return []


class MemoryReviewStartResponse(BaseModel):
    total: int
    items: List[dict]


class MemoryReviewSubmitRequest(BaseModel):
    word_id: int
    correct: bool
    user_id: Optional[int] = None


@router.get("/audio")
def word_audio_by_english(
    english: str,
    lang: str = Query("en-US", description="语言：en-US（默认）/ zh-CN；句子/中文走 edge-tts"),
    db: Session = Depends(get_db),
):
    """按英文单词直接取发音音频（拼读规则示例词用；词库没有时现场 TTS 生成，不再 404）。

    单词（无空格）→ 有道/Free Dictionary/edge 三级 fallback（generate_word_audio）。
    句子/中文（含空格、超长或 lang=zh-CN）→ edge-tts（浏览器 speechSynthesis 降级场景）。
    """
    import re
    from fastapi.responses import FileResponse
    from app.services.tts import tts_service
    text = english.strip()
    if not text:
        raise HTTPException(status_code=400, detail="english 不能为空")

    # 中文朗读降级（speakZh 用）：直接 edge-tts
    if lang.lower().startswith("zh"):
        try:
            audio_path = tts_service.generate_sentence_audio(text, lang="zh-CN")
            media_type = "audio/mpeg" if audio_path.endswith(".mp3") else "audio/wav"
            return FileResponse(audio_path, media_type=media_type)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"中文语音生成失败: {e}")

    # 英文句子/短语（含空格或超长）→ edge-tts；有道/Free Dictionary 只支持单词
    if " " in text or len(text) > 30:
        try:
            audio_path = tts_service.generate_sentence_audio(text, lang="en-US")
            media_type = "audio/mpeg" if audio_path.endswith(".mp3") else "audio/wav"
            return FileResponse(audio_path, media_type=media_type)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"句子语音生成失败: {e}")

    word = db.query(Word).filter(
        Word.deleted == False,  # noqa: E712
        func.lower(Word.english) == text.lower(),
    ).first()
    try:
        audio_path = tts_service.generate_word_audio(word.english if word else text)
    except Exception:
        # 组合类文本（如 a_e）词典/有道查不到，拆成字母名逐个朗读（a_e → "a e"），
        # 让孩子听出组合由哪些字母构成，同时避免落到未配置有效的 mimo 兜底
        letters = re.sub(r"[^a-zA-Z]", " ", text).strip()
        letters = re.sub(r"\s+", " ", letters)
        if letters and letters != text:
            audio_path = tts_service.generate_word_audio(letters)
        else:
            raise
    try:
        media_type = "audio/mpeg" if audio_path.endswith(".mp3") else "audio/wav"
        return FileResponse(audio_path, media_type=media_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"音频生成失败: {str(e)}")


@router.get("/memory-review", response_model=MemoryReviewStartResponse)
def memory_review(
    user_id: Optional[int] = Query(None, description="小孩ID，不传则默认第一个小孩"),
    limit: int = Query(20, ge=1, le=100),
    db: Session = Depends(get_db),
):
    """记忆模式复习：取该小孩「已生成口诀」的单词（优先待复习/最近错词），口诀做提示猜词"""
    uid = _resolve_user_id(db, user_id)
    words = db.query(Word).filter(
        Word.deleted == False,  # noqa: E712
        Word.mnemonic.isnot(None),
        Word.mnemonic != "",
    ).all()
    if not words:
        return {"total": 0, "items": []}

    ids = [w.id for w in words]
    progress_map = {p.word_id: p for p in db.query(WordProgress).filter(
        WordProgress.user_id == uid, WordProgress.word_id.in_(ids)).all()}

    def sort_key(w):
        p = progress_map.get(w.id)
        due = 0 if p is None or p.next_review_at is None or p.next_review_at <= datetime.now() else 1
        acc = 100
        if p and p.review_count:
            acc = p.correct_count * 100.0 / p.review_count
        return (due, acc, w.id)

    words.sort(key=sort_key)
    picked = words[:limit]
    items = [{
        "word_id": w.id,
        "english": w.english,
        "chinese": w.chinese,
        "phonetic": w.phonetic,
        "mnemonic": w.mnemonic,
        "word_root": w.word_root,
        "related_words": _parse_json_list(w.related_words),
        "example_sentences": _parse_json_list(w.example_sentences),
        "hint": f"{w.english[0]}{'_' * (len(w.english) - 1)}（{len(w.english)} 个字母）",
    } for w in picked]
    return {"total": len(picked), "items": items}


@router.post("/memory-review/submit")
def memory_review_submit(data: MemoryReviewSubmitRequest, db: Session = Depends(get_db)):
    """记忆模式复习提交：更新该小孩 word_progress（艾宾浩斯曲线）并写复习日志"""
    uid = _resolve_user_id(db, data.user_id)
    word = db.query(Word).filter(Word.id == data.word_id, Word.deleted == False).first()  # noqa: E712
    if not word:
        raise HTTPException(status_code=404, detail="单词不存在")
    progress = _get_progress(db, data.word_id, uid)

    progress.review_count = (progress.review_count or 0) + 1
    if data.correct:
        progress.correct_count = (progress.correct_count or 0) + 1
    now = datetime.now()
    progress.last_reviewed_at = now

    interval = progress.interval or 1
    interval = min(interval * 2, 30) if data.correct else 1
    progress.interval = interval
    progress.next_review_at = now + timedelta(days=interval)
    progress.learning_phase = _get_accuracy_level(progress.review_count, progress.correct_count)

    log = WordReviewLog(
        word_id=word.id,
        user_id=uid,
        is_correct=data.correct,
        review_type=3,  # 3=记忆模式
    )
    db.add(log)

    # 四维记忆：记忆模式=「说得」（口诀猜英文，输出单词）；答错入错词池，答对移出
    progress.speak_count = (progress.speak_count or 0) + 1
    if data.correct:
        progress.speak_correct = (progress.speak_correct or 0) + 1
        try:
            from app.models import WordAttempt
            rows = db.query(WordAttempt).filter(
                WordAttempt.word_id == word.id,
                WordAttempt.user_id == uid,
                WordAttempt.dimension == "speak",
            ).all()
            for r in rows:
                db.delete(r)
        except Exception:
            pass
    else:
        try:
            from app.models import WordAttempt
            row = db.query(WordAttempt).filter(
                WordAttempt.word_id == word.id,
                WordAttempt.user_id == uid,
                WordAttempt.dimension == "speak",
            ).first()
            if row:
                row.wrong_count = (row.wrong_count or 1) + 1
                row.updated_at = now
            else:
                db.add(WordAttempt(
                    word_id=word.id,
                    user_id=uid,
                    dimension="speak",
                    source="memory",
                    english=word.english,
                    chinese=word.chinese,
                    phonetic=word.phonetic,
                    wrong_count=1,
                    created_at=now,
                    updated_at=now,
                ))
        except Exception:
            pass

    db.commit()
    return {
        "message": "ok",
        "word_id": word.id,
        "review_count": progress.review_count,
        "correct_count": progress.correct_count,
        "learning_phase": progress.learning_phase,
        "next_review_at": progress.next_review_at,
    }
