# -*- coding: utf-8 -*-
"""导出权威词表 JSON（部署用）：deploy/words_oxford.json
由 deploy.ps1 [1.5/5] 调用，随部署包上传，远端 words_sync.py 幂等 upsert 进云端主库。
"""
import json
import os
import sys

os.chdir(r"E:\qianwenpaw\EasyFix-main\backend")
sys.path.insert(0, r"E:\qianwenpaw\EasyFix-main\backend")

from app.services.words_import import WORD_SOURCES, fetch_word_source

out = os.path.join(os.path.dirname(__file__), "..", "deploy", "words_oxford.json")
rows = []
for src in WORD_SOURCES:
    rows.extend(fetch_word_source(src))
    print(f"  {src['key']}: {len(rows)} 条（含此前源）")
with open(out, "w", encoding="utf-8") as f:
    json.dump({"source_version": "2024-v1", "rows": rows}, f, ensure_ascii=False, indent=1)
print(f"已导出 {len(rows)} 条 → {out}")
