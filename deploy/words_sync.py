# -*- coding: utf-8 -*-
"""云端权威词表同步：把 deploy/words_oxford.json 幂等 upsert 进云端主库 ops_word。

策略（修复旧 AI 数据）：
  - 同 (version, grade, semester, english) 权威覆盖：chinese/unit/unit_title/source_type=authority，软删行复活
  - AI 独有的词（权威源没有的）保留，source_type='ai'，运营后台可筛选人工核对（不误删）
用法: docker exec easyfix python3 /data/words_sync.py
失败仅警告，不阻断部署（与 ops_data_sync.py 一致）。
"""
import json
import os
import sys

sys.path.insert(0, "/app/backend")
os.environ.setdefault("DB_PATH", "/data/easyfix_main.db")

from app.database import SessionLocal
from app.models.ops_data import OpsWord, ensure_ops_tables
from sqlalchemy import func


def main():
    path = os.environ.get("WORDS_JSON", "/data/words_oxford.json")
    if not os.path.exists(path):
        print(">>> 未找到 /data/words_oxford.json，跳过权威词表同步")
        return
    with open(path, encoding="utf-8") as f:
        data = json.load(f)
    rows = data.get("rows") or []
    print(f">>> 权威词表同步：{len(rows)} 条（{data.get('source_version')}）")
    ensure_ops_tables()
    imported = updated = 0
    seen = set()
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
                    row.deleted = False
                    changed = True
                if row.source_type != "authority":
                    row.source_type = "authority"
                    changed = True
                updated += 1 if changed else 0
            else:
                db.add(OpsWord(version=r["version"], grade=r["grade"], semester=r["semester"],
                               unit=r.get("unit"), unit_title=r.get("unit_title"),
                               english=en, chinese=cn, source_type="authority", revision="v1"))
                imported += 1
        db.commit()
        ai_left = db.query(OpsWord).filter(OpsWord.source_type == "ai", OpsWord.version == "牛津深圳版",
                                           OpsWord.deleted == False).count()
        total = db.query(OpsWord).filter(OpsWord.version == "牛津深圳版", OpsWord.deleted == False).count()
        print(f">>> 完成：新增 {imported}，权威覆盖 {updated}；牛津深圳版现存 {total} 条，其中 AI 独有 {ai_left} 条（可筛选核对）")
    except Exception as e:
        db.rollback()
        print(">>> 同步失败:", e)
        sys.exit(1)
    finally:
        db.close()


if __name__ == "__main__":
    main()
