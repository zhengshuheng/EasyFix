# -*- coding: utf-8 -*-
"""导入牛津深圳版权威词表（LanguageAstronauts 12 册）→ ops_word

用法: python tools/import_oxford_words.py [--grade 1] [--semester 1] [--version 牛津深圳版] [--dry-run]
默认全册导入（dry-run 只统计不写库）。
"""
import os
import sys

os.chdir(r"E:\qianwenpaw\EasyFix-main\backend")
sys.path.insert(0, r"E:\qianwenpaw\EasyFix-main\backend")

from app.services.words_import import WORD_SOURCES, fetch_word_source, import_word_rows

dry_run = "--dry-run" in sys.argv
grade_filter = None
sem_filter = None
for i, a in enumerate(sys.argv):
    if a == "--grade" and i + 1 < len(sys.argv):
        grade_filter = int(sys.argv[i + 1])
    if a == "--semester" and i + 1 < len(sys.argv):
        sem_filter = int(sys.argv[i + 1])

src = WORD_SOURCES[0]
print(f"下载词表源: {src['label']} ...")
rows = fetch_word_source(src)
print(f"解析到 {len(rows)} 条词")

if grade_filter is not None:
    rows = [r for r in rows if r["grade"] == grade_filter]
if sem_filter is not None:
    rows = [r for r in rows if r["semester"] == sem_filter]
print(f"过滤后 {len(rows)} 条（grade={grade_filter} semester={sem_filter}）")

if dry_run:
    from collections import Counter
    c = Counter((r["grade"], r["semester"]) for r in rows)
    for k in sorted(c):
        print(f"  牛津深圳版 {k[0]}年级{'上' if k[1]==1 else '下'}: {c[k]} 词")
    print("DRY-RUN 未写库")
else:
    r = import_word_rows(rows)
    print("导入结果:", r)
