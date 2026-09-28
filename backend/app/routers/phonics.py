"""
自然拼读规则库路由（phonics）：规则列表 / CRUD / AI 生成 / 拼读错题（按小孩隔离）
"""
import json
import re
from datetime import datetime
from typing import Optional, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from pydantic import BaseModel, Field
from app.database import get_db
from app.models.word import PhonicsRule, PhonicsAttempt, Word
from app.utils.kid_context import get_current_kid_id, get_required_kid_id
from app.services.textbook_service import _llm_json

router = APIRouter(prefix="/api/phonics", tags=["自然拼读"])

_GRADE_CN = {1: "一年级", 2: "二年级", 3: "三年级", 4: "四年级", 5: "五年级", 6: "六年级"}

# ==================== 词库覆盖（从单词表按学段提取 → 按规则归类） ====================

_STAGE_GRADES = {"primary": (1, 6), "junior": (7, 9)}  # 小学 1-6 / 初中 7-9


def _stage_grade_range(stage: Optional[str]) -> tuple:
    """学段 → 年级范围（缺省小学）"""
    if stage == "junior":
        return 7, 9
    return 1, 6


def _match_pattern(pattern: str, word: str) -> bool:
    """判断单词是否命中拼读规则 pattern（支持 a_e 这类带下划线的规则）"""
    p = (pattern or "").strip().lower()
    w = (word or "").strip().lower()
    if not p or not w:
        return False
    if "_" in p:
        # a_e → a 后跟一个字母再 e（CVCe）；i_e / o_e / u_e 同理
        parts = p.split("_")
        if len(parts) != 2 or not parts[0] or not parts[1]:
            return False
        return re.search(re.escape(parts[0]) + r"[a-z]" + re.escape(parts[1]), w) is not None
    return p in w


def _load_stage_lexicon(db: Session, stage: Optional[str]) -> List[Word]:
    """按学段提取单词表（去重，按年级排序）"""
    lo, hi = _stage_grade_range(stage)
    words = db.query(Word).filter(
        Word.deleted == False,  # noqa: E712
        Word.grade >= lo,
        Word.grade <= hi,
    ).order_by(Word.grade.asc(), Word.english.asc()).all()
    seen = set()
    result = []
    for w in words:
        key = (w.english or "").strip().lower()
        if not key or key in seen:
            continue
        seen.add(key)
        result.append(w)
    return result

def _attach_lexicon(db: Session, rules: List[PhonicsRule], stage: Optional[str]) -> List[dict]:
    """给规则附加词库覆盖（lexicon_count / lexicon_words / lexicon_total），stage 为空则跳过"""
    if not stage:
        return [_to_dict(r) for r in rules]
    lexicon = _load_stage_lexicon(db, stage)
    # 过滤多词短语（climb trees / a pair of 等），拼读分类只统计单个单词
    lexicon = [w for w in lexicon if (w.english or "").strip() and " " not in w.english.strip().lower()]
    out = []
    for r in rules:
        d = _to_dict(r)
        matched = [w for w in lexicon if _match_pattern(r.pattern, w.english)]
        d["lexicon_total"] = len(lexicon)
        d["lexicon_count"] = len(matched)
        d["lexicon_words"] = [
            {"en": w.english, "cn": w.chinese or "", "grade": w.grade}
            for w in matched[:80]
        ]
        out.append(d)
    return out


def _dump_json(v) -> str:
    if v is None:
        return "[]"
    try:
        return json.dumps(v, ensure_ascii=False)
    except Exception:
        return "[]"


def _parse_json_list(raw) -> list:
    if not raw:
        return []
    try:
        v = json.loads(raw)
        return v if isinstance(v, list) else []
    except Exception:
        return []


class PhonicsRuleResponse(BaseModel):
    id: int
    pattern: str
    sound: Optional[str] = None
    rule_text: Optional[str] = None
    example_words: List = []
    grade: Optional[int] = None
    category: Optional[str] = None
    source: Optional[str] = None

    class Config:
        from_attributes = True


class PhonicsRuleCreate(BaseModel):
    pattern: str = Field(..., max_length=100)
    sound: Optional[str] = Field(None, max_length=50)
    rule_text: Optional[str] = None
    example_words: Optional[List] = None
    grade: Optional[int] = Field(None, ge=1, le=12)
    category: str = "vowel"


class PhonicsRuleUpdate(BaseModel):
    pattern: Optional[str] = None
    sound: Optional[str] = None
    rule_text: Optional[str] = None
    example_words: Optional[List] = None
    grade: Optional[int] = None
    category: Optional[str] = None


class PhonicsAIGenerateRequest(BaseModel):
    """AI 生成自然拼读规则（按类别批量）"""
    category: str = Field("vowel", description="vowel=元音组合 consonant=辅音组合 silent_e=不发音e")
    grade: Optional[int] = Field(None, ge=1, le=6)
    instruction: Optional[str] = Field(None, max_length=500)


def _to_dict(r: PhonicsRule) -> dict:
    return {
        "id": r.id,
        "pattern": r.pattern,
        "sound": r.sound,
        "rule_text": r.rule_text,
        "example_words": _parse_json_list(r.example_words),
        "grade": r.grade,
        "category": r.category or "vowel",
        "source": r.source,
    }


@router.get("")
def list_rules(
    category: Optional[str] = None,
    grade: Optional[int] = None,
    keyword: Optional[str] = None,
    stage: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """规则列表；传 stage（primary/junior）时附加上该学段词库覆盖（从单词表提取归类）"""
    q = db.query(PhonicsRule).filter(PhonicsRule.deleted == False)  # noqa: E712
    if category:
        q = q.filter(PhonicsRule.category == category)
    if grade:
        q = q.filter(PhonicsRule.grade == grade)
    if keyword:
        q = q.filter(PhonicsRule.pattern.contains(keyword))
    rules = q.order_by(PhonicsRule.category, PhonicsRule.grade.asc().nulls_last(), PhonicsRule.id).all()
    return _attach_lexicon(db, rules, stage)


@router.get("/lexicon-stats")
def lexicon_stats(
    stage: Optional[str] = None,
    db: Session = Depends(get_db),
):
    """学段词库覆盖统计：词库总词数 / 命中规则词数 / 规则覆盖数（词库从单词表按学段提取）"""
    lexicon = _load_stage_lexicon(db, stage)
    lexicon = [w for w in lexicon if (w.english or "").strip() and " " not in w.english.strip().lower()]
    rules = db.query(PhonicsRule).filter(PhonicsRule.deleted == False).all()  # noqa: E712
    covered_word_ids = set()
    covered_rule_ids = set()
    rule_word_count = {}
    for r in rules:
        matched = [w for w in lexicon if _match_pattern(r.pattern, w.english)]
        n = len(matched)
        rule_word_count[r.id] = n
        if n > 0:
            covered_rule_ids.add(r.id)
            covered_word_ids.update(w.id for w in matched)
    lo, hi = _stage_grade_range(stage)
    return {
        "stage": stage or "primary",
        "grade_range": [lo, hi],
        "total_words": len(lexicon),
        "covered_words": len(covered_word_ids),
        "covered_rate": round(len(covered_word_ids) / len(lexicon), 4) if lexicon else 0,
        "rule_count": len(rules),
        "covered_rules": len(covered_rule_ids),
        "rule_word_count": {str(k): v for k, v in rule_word_count.items()},
    }


@router.post("", status_code=201)
def create_rule(data: PhonicsRuleCreate, db: Session = Depends(get_db)):
    rule = PhonicsRule(
        pattern=data.pattern.strip(),
        sound=data.sound,
        rule_text=data.rule_text,
        example_words=_dump_json(data.example_words),
        grade=data.grade,
        category=data.category,
        source="manual",
    )
    db.add(rule)
    db.commit()
    db.refresh(rule)
    return _to_dict(rule)


@router.put("/{rule_id}")
def update_rule(rule_id: int, data: PhonicsRuleUpdate, db: Session = Depends(get_db)):
    rule = db.query(PhonicsRule).filter(PhonicsRule.id == rule_id, PhonicsRule.deleted == False).first()  # noqa: E712
    if not rule:
        raise HTTPException(status_code=404, detail="规则不存在")
    if data.pattern is not None:
        rule.pattern = data.pattern.strip()
    if data.sound is not None:
        rule.sound = data.sound
    if data.rule_text is not None:
        rule.rule_text = data.rule_text
    if data.example_words is not None:
        rule.example_words = _dump_json(data.example_words)
    if data.grade is not None:
        rule.grade = data.grade
    if data.category is not None:
        rule.category = data.category
    rule.source = "manual"
    db.commit()
    db.refresh(rule)
    return _to_dict(rule)


@router.delete("/{rule_id}", status_code=204)
def delete_rule(rule_id: int, db: Session = Depends(get_db)):
    rule = db.query(PhonicsRule).filter(PhonicsRule.id == rule_id, PhonicsRule.deleted == False).first()  # noqa: E712
    if not rule:
        raise HTTPException(status_code=404, detail="规则不存在")
    rule.deleted = True
    db.commit()


@router.post("/ai-generate")
def ai_generate_rules(req: PhonicsAIGenerateRequest, db: Session = Depends(get_db)):
    """AI 批量生成自然拼读规则（整类生成，查重按 pattern+category）"""
    cat_cn = {"vowel": "元音字母组合（如 ee, oo, ai, ay, ea, ou, ow, ar, or, er, ir, ur, a_e, i_e 等）",
              "consonant": "辅音字母组合（如 th, sh, ch, ph, wh, ck, ng, qu, bl, br, cl, cr, dr, fl, fr, gl, gr, pl, pr, sl, sm, sn, sp, st, sw, tr, tw 等）",
              "silent_e": "不发音 e 规则（如 a_e, i_e, o_e, u_e，元音读字母音）"}.get(
        req.category, req.category)
    grade_cn = _GRADE_CN.get(req.grade, "")
    task = f"类别：{cat_cn}；建议年级：{grade_cn or '小学'}。"
    if req.instruction and req.instruction.strip():
        task += f"\n额外要求：{req.instruction.strip()}"

    prompt = (
        "你是小学英语自然拼读老师，精通英语字母组合的发音规律。\n"
        f"{task}\n"
        "请生成该类别下小学阶段需要掌握的全部自然拼读规则（10~18 条），每条：\n"
        "   - pattern：字母组合（如 ee / th / a_e）\n"
        "   - sound：发音音标（如 /iː/ /θ/ /eɪ/）\n"
        "   - rule_text：规则说明（用孩子能懂的中文，如「两个 e 手拉手，一起读长音 iː」）\n"
        "   - example_words：2~4 个示例词 [{\"en\":\"bee\",\"cn\":\"蜜蜂\"}, ...]，必须真实拼读符合该规则\n"
        "   - grade：建议起始年级（1~6）\n"
        "要求：规则准确、示例词是本单词库常见小学词汇。\n"
        "只输出 JSON，不要任何解释，不要 markdown 代码块：\n"
        '{"rules":[{"pattern":"ee","sound":"/iː/","rule_text":"...","example_words":[{"en":"bee","cn":"蜜蜂"}],"grade":1}]}'
    )
    try:
        content = _llm_json(prompt, system="你只输出JSON，不要任何解释。", max_tokens=3500, timeout=180)
        data = json.loads(content) if isinstance(content, str) else content
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"AI 生成失败：{e}")

    rules = data.get("rules", []) if isinstance(data, dict) else []
    items = []
    seen = set()
    for r in rules:
        if not isinstance(r, dict):
            continue
        pattern = str(r.get("pattern", "")).strip().lower()
        if not pattern or pattern in seen:
            continue
        seen.add(pattern)
        exists = db.query(PhonicsRule).filter(
            PhonicsRule.deleted == False,  # noqa: E712
            PhonicsRule.category == req.category,
            PhonicsRule.pattern == pattern,
        ).first()
        grade = r.get("grade")
        try:
            grade = int(grade) if grade is not None else None
        except Exception:
            grade = None
        items.append({
            "pattern": pattern,
            "sound": str(r.get("sound", "") or "").strip(),
            "rule_text": str(r.get("rule_text", "") or "").strip(),
            "example_words": r.get("example_words") or [],
            "grade": grade if grade and 1 <= grade <= 6 else None,
            "existing": exists is not None,
        })
    if not items:
        raise HTTPException(status_code=502, detail="AI 返回内容无法解析，请重试")
    return {"items": items, "total": len(items), "category": req.category}


@router.post("/ai-import")
def ai_import_rules(req: PhonicsAIGenerateRequest, db: Session = Depends(get_db)):
    """AI 生成并直接导入整类规则（跳过已存在）"""
    gen = ai_generate_rules(req, db)
    created = 0
    for it in gen["items"]:
        if it["existing"]:
            continue
        db.add(PhonicsRule(
            pattern=it["pattern"],
            sound=it["sound"],
            rule_text=it["rule_text"],
            example_words=_dump_json(it["example_words"]),
            grade=it["grade"],
            category=req.category,
            source="ai",
        ))
        created += 1
    db.commit()
    return {"created": created, "total": gen["total"]}


# ==================== 拼读练习错题（按小孩隔离） ====================

class PhonicsWrongItem(BaseModel):
    rule_id: Optional[int] = None
    word: str = Field(..., max_length=200)
    pattern: Optional[str] = Field(None, max_length=100)
    category: Optional[str] = Field(None, max_length=50)


class PhonicsWrongsRequest(BaseModel):
    items: List[PhonicsWrongItem] = Field(default_factory=list, max_length=200)


class PhonicsWrongsClearRequest(BaseModel):
    words: List[str] = Field(default_factory=list, max_length=200)


def _wrong_to_dict(a: PhonicsAttempt) -> dict:
    return {
        "id": a.id,
        "rule_id": a.rule_id,
        "word": a.word,
        "pattern": a.pattern,
        "category": a.category,
        "wrong_count": a.wrong_count,
        "updated_at": a.updated_at.isoformat() if a.updated_at else None,
    }


@router.get("/wrong-words")
def list_wrong_words(
    category: Optional[str] = None,
    db: Session = Depends(get_db),
    kid_id: Optional[int] = Depends(get_current_kid_id),
):
    """拼读错题池（当前小孩）：练习答错的组合/示例词，供优先复习"""
    q = db.query(PhonicsAttempt).filter(PhonicsAttempt.user_id == kid_id)
    if category:
        q = q.filter(PhonicsAttempt.category == category)
    rows = q.order_by(PhonicsAttempt.updated_at.desc()).all()
    return [_wrong_to_dict(a) for a in rows]


@router.get("/wrong-count")
def wrong_count(
    db: Session = Depends(get_db),
    kid_id: Optional[int] = Depends(get_current_kid_id),
):
    """拼读错题数（按小孩）"""
    n = db.query(PhonicsAttempt).filter(PhonicsAttempt.user_id == kid_id).count()
    return {"count": n}


@router.post("/wrong-words", status_code=201)
def save_wrong_words(
    req: PhonicsWrongsRequest,
    db: Session = Depends(get_db),
    kid_id: int = Depends(get_required_kid_id),
):
    """练习结束后保存本轮错题（同一 word 覆盖并累计答错次数）"""
    saved = 0
    now = datetime.now()
    for it in req.items:
        word = (it.word or "").strip()
        if not word:
            continue
        row = db.query(PhonicsAttempt).filter(
            PhonicsAttempt.user_id == kid_id,
            PhonicsAttempt.word == word,
        ).first()
        if row:
            row.rule_id = it.rule_id or row.rule_id
            row.pattern = it.pattern or row.pattern
            row.category = it.category or row.category
            row.wrong_count = (row.wrong_count or 1) + 1
            row.updated_at = now
        else:
            db.add(PhonicsAttempt(
                user_id=kid_id,
                rule_id=it.rule_id,
                word=word,
                pattern=it.pattern,
                category=it.category,
                wrong_count=1,
                created_at=now,
                updated_at=now,
            ))
        saved += 1
    db.commit()
    return {"saved": saved}


@router.post("/wrong-words/clear")
def clear_wrong_words(
    req: PhonicsWrongsClearRequest,
    db: Session = Depends(get_db),
    kid_id: int = Depends(get_required_kid_id),
):
    """练习中答对的历史错题 → 移出错题池（掌握即移除）"""
    words = [w.strip() for w in req.words if w and w.strip()]
    if not words:
        return {"cleared": 0}
    rows = db.query(PhonicsAttempt).filter(
        PhonicsAttempt.user_id == kid_id,
        PhonicsAttempt.word.in_(words),
    ).all()
    for r in rows:
        db.delete(r)
    db.commit()
    return {"cleared": len(rows)}
