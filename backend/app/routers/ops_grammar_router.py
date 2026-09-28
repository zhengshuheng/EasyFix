# -*- coding: utf-8 -*-
"""Ops 语法教程管理 API（运营后台，X-Ops-Password 鉴权，主库读写）

定位：语法知识点与教程内容统一由运营中心维护（主库 grammar_lesson = 权威）。
- 空间创建时模板库自动携带主库副本（trial.copy_global_content 保留主键 id）；
- 存量空间/模板库通过本接口的「同步」能力按 id upsert 更新，保证全空间一致；
- 空间端语法写接口已禁用（routers/grammar.py 403），家长只读 → 语法点固化。
"""
import json
from typing import List, Optional

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.config_api import _check_ops_password
from app.database import SessionLocal
from app.models.grammar import GrammarLesson
from app.services.grammar_sync import sync_grammar_from_main, sync_grammar_sqlite
from app.services.textbook_service import _llm_json, _parse_json

router = APIRouter(prefix="/api/ops/grammar", tags=["Ops 语法教程"])

_GRADE_CN = {1: "一年级", 2: "二年级", 3: "三年级", 4: "四年级", 5: "五年级", 6: "六年级"}


def _ops_check(x_ops_username: str, x_ops_password: str) -> None:
    db = SessionLocal()
    try:
        _check_ops_password(db, x_ops_password, x_ops_username)
    finally:
        db.close()


def _dump_json(v) -> str:
    return json.dumps(v, ensure_ascii=False) if v else "[]"


def _lesson_out(l: GrammarLesson) -> dict:
    return {
        "id": l.id,
        "category": l.category,
        "title": l.title,
        "grade": l.grade,
        "semester": l.semester,
        "summary": l.summary or "",
        "content_md": l.content_md or "",
        "examples": l.examples or "[]",
        "common_mistakes": l.common_mistakes or "[]",
        "mnemonic": l.mnemonic or "",
        "source": l.source,
        "order_index": l.order_index,
        "has_content": bool(l.content_md and l.content_md.strip()),
        "updated_at": l.updated_at.strftime("%Y-%m-%d %H:%M") if l.updated_at else "",
    }


class GrammarLessonUpdate(BaseModel):
    category: Optional[str] = None
    title: Optional[str] = None
    grade: Optional[int] = None
    semester: Optional[int] = None
    summary: Optional[str] = None
    content_md: Optional[str] = None
    examples: Optional[List] = None
    common_mistakes: Optional[List] = None
    mnemonic: Optional[str] = None
    order_index: Optional[int] = None


class GrammarAiRequest(BaseModel):
    """生成缺失教程：lesson_ids 指定单点/多点；缺省=全部 content 为空的点。"""
    lesson_ids: Optional[List[int]] = None
    category: Optional[str] = None


# ---------------------------------------------------------------- 列表 / 详情

@router.get("/lessons")
def ops_grammar_lessons(
    category: Optional[str] = None,
    has_content: Optional[int] = None,
    x_ops_username: str = Header(default=""),
    x_ops_password: str = Header(default=""),
):
    """语法教程清单（主库）：板块/语法点/年级/内容状态；has_content=1 只看缺内容的。"""
    _ops_check(x_ops_username, x_ops_password)
    db = SessionLocal()
    try:
        q = db.query(GrammarLesson).filter(GrammarLesson.deleted == False)  # noqa: E712
        if category:
            q = q.filter(GrammarLesson.category == category)
        rows = q.order_by(GrammarLesson.category, GrammarLesson.grade.asc().nulls_last(), GrammarLesson.order_index, GrammarLesson.id).all()
        out = [_lesson_out(l) for l in rows]
        if has_content is not None:
            out = [r for r in out if (r["has_content"] if has_content == 1 else not r["has_content"])]
        return {"total": len(out), "items": out}
    finally:
        db.close()


@router.get("/lessons/{lesson_id}")
def ops_grammar_lesson_detail(lesson_id: int, x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    _ops_check(x_ops_username, x_ops_password)
    db = SessionLocal()
    try:
        l = db.query(GrammarLesson).filter(GrammarLesson.id == lesson_id, GrammarLesson.deleted == False).first()  # noqa: E712
        if not l:
            raise HTTPException(status_code=404, detail="语法点不存在")
        return _lesson_out(l)
    finally:
        db.close()


# ---------------------------------------------------------------- 编辑

@router.put("/lessons/{lesson_id}")
def ops_grammar_lesson_update(
    lesson_id: int,
    data: GrammarLessonUpdate,
    x_ops_username: str = Header(default=""),
    x_ops_password: str = Header(default=""),
):
    """编辑语法教程（主库权威）。改完同步模板库，使新建空间即带最新内容；存量空间由「推送同步」更新。"""
    _ops_check(x_ops_username, x_ops_password)
    db = SessionLocal()
    try:
        l = db.query(GrammarLesson).filter(GrammarLesson.id == lesson_id, GrammarLesson.deleted == False).first()  # noqa: E712
        if not l:
            raise HTTPException(status_code=404, detail="语法点不存在")
        if data.category is not None:
            l.category = data.category.strip()
        if data.title is not None:
            l.title = data.title.strip()
        if data.grade is not None:
            l.grade = data.grade
        if data.semester is not None:
            l.semester = data.semester
        if data.summary is not None:
            l.summary = data.summary
        if data.content_md is not None:
            l.content_md = data.content_md
        if data.examples is not None:
            l.examples = _dump_json(data.examples)
        if data.common_mistakes is not None:
            l.common_mistakes = _dump_json(data.common_mistakes)
        if data.mnemonic is not None:
            l.mnemonic = data.mnemonic
        if data.order_index is not None:
            l.order_index = data.order_index
        l.source = "manual"
        db.commit()
        db.refresh(l)
        return _lesson_out(l)
    finally:
        db.close()


# ---------------------------------------------------------------- AI 生成内容

@router.post("/ai-generate")
def ops_grammar_ai_generate(
    req: GrammarAiRequest,
    x_ops_username: str = Header(default=""),
    x_ops_password: str = Header(default=""),
):
    """AI 批量生成缺失教程（主库）。lesson_ids 指定单点/多点；缺省=全部内容为空的点。"""
    _ops_check(x_ops_username, x_ops_password)
    db = SessionLocal()
    try:
        q = db.query(GrammarLesson).filter(GrammarLesson.deleted == False)  # noqa: E712
        if req.lesson_ids:
            q = q.filter(GrammarLesson.id.in_(req.lesson_ids))
        elif req.category:
            q = q.filter(GrammarLesson.category == req.category)
        else:
            q = q.filter(GrammarLesson.content_md.is_(None) | (GrammarLesson.content_md == ""))
        lessons = q.order_by(GrammarLesson.id).all()
        if not lessons:
            return {"results": [], "ok_count": 0, "total": 0, "message": "没有待生成的语法点（可能已全部生成）"}

        results = []
        for lesson in lessons:
            grade_cn = _GRADE_CN.get(lesson.grade, "")
            prompt = (
                "你是小学英语特级教师，擅长把语法规则讲得「清楚、易懂、有趣」，写给 6~12 岁孩子自学。\n"
                f"语法点：{lesson.title}；适用年级：{grade_cn or '小学'}。\n"
                "请生成一份语法教程，要求：\n"
                "1. summary：一句话总结这个语法点（像顺口溜一样好记，孩子一看就懂）；\n"
                "2. content_md：教程正文 Markdown，用「小学老师上课」的口吻，包含：\n"
                "   - 这是啥（用孩子能懂的话解释）\n"
                "   - 怎么用（分 2~4 个要点，每条先讲规则再给一个生活化例句）\n"
                "   - 内容用 Markdown 小标题（##、###）和列表组织，段落短小\n"
                "3. examples：5~8 条例句数组 [{\"en\":\"英文\",\"zh\":\"中文\"}]，覆盖刚才讲的每个要点；\n"
                "4. common_mistakes：3~5 条小学生最常见的错误，数组字符串，如 [\"I am 不能写成 I is\", \"...\"]；\n"
                "5. mnemonic：一句记忆口诀或顺口溜（中文，朗朗上口）。\n"
                "语言要求：中文讲解，例句英文原句 + 中文翻译；低年级（1~3 年级）用词更简单。\n"
                "只输出 JSON，不要任何解释，不要 markdown 代码块：\n"
                '{"summary":"...","content_md":"## 这是啥\\n...","examples":[{"en":"I am a student.","zh":"我是一名学生。"}],"common_mistakes":["..."],"mnemonic":"..."}'
            )
            try:
                content = _llm_json(prompt, system="你只输出JSON，不要输出任何解释。", max_tokens=3500, timeout=180)
                data = _parse_json(content)
            except Exception as e:
                results.append({"id": lesson.id, "title": lesson.title, "ok": False, "error": str(e)})
                continue

            lesson.summary = str(data.get("summary", "")).strip() or lesson.summary
            lesson.content_md = str(data.get("content_md", "")).strip()
            lesson.examples = _dump_json(data.get("examples") or [])
            lesson.common_mistakes = _dump_json(data.get("common_mistakes") or [])
            lesson.mnemonic = str(data.get("mnemonic", "")).strip()
            if lesson.source == "skeleton":
                lesson.source = "ai"
            db.commit()
            results.append({
                "id": lesson.id,
                "title": lesson.title,
                "ok": True,
                "has_content": bool(lesson.content_md),
            })

        ok_count = sum(1 for r in results if r["ok"])
        if not ok_count:
            raise HTTPException(status_code=502, detail="所有语法点生成失败，请重试")
        return {"results": results, "ok_count": ok_count, "total": len(results)}
    finally:
        db.close()


# ---------------------------------------------------------------- 推送同步

@router.post("/sync-tenants")
def ops_grammar_sync_tenants(x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    """推送主库语法教程到全部空间库 + 模板库（按 id upsert + 软删多余点）。

    空间端也可自行调用 /api/grammar/sync-tutorials 即时更新当前空间。
    """
    _ops_check(x_ops_username, x_ops_password)
    import os
    import sqlite3
    from app.trial import TEMPLATE_DB_PATH, _registry_conn

    rows = None  # 惰性：sync_grammar_sqlite 内部加载主库
    targets = []
    # 模板库
    if os.path.isfile(TEMPLATE_DB_PATH):
        targets.append(("template", TEMPLATE_DB_PATH))
    # 全部空间库
    reg = _registry_conn()
    try:
        for key, db_path in reg.execute("select key, db_path from spaces").fetchall():
            if os.path.isfile(db_path):
                targets.append((key, db_path))
    finally:
        reg.close()

    summary = {"template": None, "spaces": {}, "failures": []}
    for key, path in targets:
        try:
            r = sync_grammar_sqlite(path, rows)
            rows = None  # 主库行缓存复用
            if key == "template":
                summary["template"] = r
            else:
                summary["spaces"][key] = r
        except Exception as e:
            summary["failures"].append({"key": key, "error": str(e)})

    return {
        "template": summary["template"],
        "space_count": len(summary["spaces"]),
        "spaces": summary["spaces"],
        "failures": summary["failures"],
    }
