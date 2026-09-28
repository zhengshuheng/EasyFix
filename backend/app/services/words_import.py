# -*- coding: utf-8 -*-
"""权威词表导入服务

数据源：GitHub 公开整理的教材词汇表（单词+基本释义为事实性内容）。
  - language-astronauts: https://github.com/flyxl/LanguageAstronauts
      沪教牛津版（六三制一起）（2024）· 深圳用 = 项目内的「牛津深圳版」
      12 册（1A-6B），1091 词，按单元 {en, zh}。
      无音标/例句（导入后由运营补例句任务自动补）。

定位：与 ctsf 大纲同为「权威在线源」（source_type='authority'），
      AI 生成（'ai'）降级为无权威源时的兜底。
"""
import base64
import json
import os
import re
import time
import urllib.request

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) EasyFix-words-importer"}
GH_API = "https://api.github.com/repos/{repo}/contents/{path}"
GH_RAW = "https://raw.githubusercontent.com/{repo}/main/{path}"

# 册次后缀 → 学期：A=上册(1) B=下册(2)；年级由册次首位数字决定
GRADE_SEM = {"A": 1, "B": 2}

WORD_SOURCES = [
    {
        "key": "language-astronauts",
        "label": "沪教牛津深圳版 12 册词表（LanguageAstronauts，公开整理）",
        "repo": "flyxl/LanguageAstronauts",
        "path": "js/data.js",
        "version": "牛津深圳版",
        "raw_fallback": True,
    },
]


def _fetch_github(repo: str, path: str, use_api: bool = True) -> str:
    if use_api:
        url = GH_API.format(repo=repo, path=path)
        req = urllib.request.Request(url, headers=UA)
        with urllib.request.urlopen(req, timeout=60) as r:
            d = json.loads(r.read().decode("utf-8"))
        if d.get("content"):
            return base64.b64decode(d["content"]).decode("utf-8")
    url = GH_RAW.format(repo=repo, path=path)
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=90) as r:
        return r.read().decode("utf-8")


def parse_la_words(src: str) -> list:
    """解析 LanguageAstronauts data.js → [{grade, semester, unit, unit_title, english, chinese}]"""
    rows = []
    # grade 块起点：{ id: "1A", name: "..."
    starts = list(re.finditer(r'\{\s*id:\s*"([1-6][AB])"\s*,\s*name:\s*"([^"]*)"', src))
    for i, m in enumerate(starts):
        gid = m.group(1)
        grade = int(gid[0])
        semester = GRADE_SEM[gid[1]]
        block = src[m.start(): (starts[i + 1].start() if i + 1 < len(starts) else len(src))]
        # unit 块：{ id: "1A-U1", name: "Unit 1 Hello", ... vocab: [ ... ], dialogue: [...] }
        # id 必须是 XX-U\d+（排除 grade 块自身）；vocab 数组内跨行，必须用 [\s\S]*?（.*? 的 . 不匹配换行）
        for um in re.finditer(r'\{\s*id:\s*"([1-6][AB]-U\d+)"\s*,\s*name:\s*"([^"]*)"[\s\S]*?vocab:\s*\[([\s\S]*?)\]', block):
            unit_title = um.group(2).strip()
            um_unit = re.search(r"-U(\d+)", um.group(1))
            unit = int(um_unit.group(1)) if um_unit else 0
            for vm in re.finditer(r'en:\s*"([^"]*)",\s*zh:\s*"([^"]*)"', um.group(3)):
                en = vm.group(1).strip()
                cn = vm.group(2).strip()
                if not en or not cn:
                    continue
                rows.append({"grade": grade, "semester": semester,
                             "unit": unit, "unit_title": unit_title,
                             "english": en, "chinese": cn})
    return rows


def fetch_word_source(source: dict, use_api: bool = True) -> list:
    """下载并解析指定权威词表源 → rows（含 version）"""
    src = _fetch_github(source["repo"], source["path"], use_api=use_api)
    if source["key"] == "language-astronauts":
        rows = parse_la_words(src)
    else:
        raise ValueError(f"未知词表源: {source['key']}")
    for r in rows:
        r["version"] = source["version"]
    return rows


def import_word_rows(rows: list, source_type: str = "authority", batch: str = "") -> dict:
    """把权威词表 rows 写入 ops_word（同版本+年级+册次+词 upsert，AI 词被权威内容覆盖）"""
    from app.database import SessionLocal
    from app.models.ops_data import OpsWord, ensure_ops_tables
    from sqlalchemy import func
    ensure_ops_tables()  # 幂等建表/补列（source_type 等）
    imported = updated = 0
    seen = set()  # autoflush=False 下同批重复词（跨单元同词）防 UNIQUE 撞车
    db = SessionLocal()
    try:
        for r in rows:
            en = (r.get("english") or "").strip()
            cn = (r.get("chinese") or "").strip()
            if not en or not cn:
                continue
            key = (r["version"], r["grade"], r["semester"], en.lower())
            if key in seen:
                continue
            seen.add(key)
            row = db.query(OpsWord).filter(
                func.lower(OpsWord.english) == en.lower(),
                OpsWord.version == r["version"],
                OpsWord.grade == r["grade"],
                OpsWord.semester == r["semester"],
            ).order_by(OpsWord.deleted.asc()).first()
            if row:
                changed = False
                if row.chinese != cn:
                    row.chinese = cn
                    changed = True
                if (r.get("unit") or 0) and (row.unit != r["unit"] or row.unit is None):
                    row.unit = r["unit"]
                    changed = True
                if r.get("unit_title") and row.unit_title != r["unit_title"]:
                    row.unit_title = r["unit_title"]
                    changed = True
                if row.deleted:
                    row.deleted = False  # 权威源导入即复活
                    changed = True
                if row.source_type != source_type:
                    row.source_type = source_type
                    changed = True
                updated += 1 if changed else 0
            else:
                db.add(OpsWord(version=r["version"], grade=r["grade"], semester=r["semester"],
                               unit=r.get("unit"), unit_title=r.get("unit_title"),
                               english=en, chinese=cn,
                               source_type=source_type, revision="v1"))
                imported += 1
        db.commit()
        return {"imported": imported, "updated": updated, "total": len(rows)}
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
