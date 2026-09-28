"""Ops 单词种子生成：LLM 按教材生成 → ops_word

用法：cd backend && ..\.venv\Scripts\python.exe tools/build_ops_words_seed.py [--grades 3 4 5 6] [--version 人教PEP]
默认：人教PEP 三年级起点 3-6 年级（8 册），逐册调用 LLM 生成全册单元单词表。
幂等：按 (version, grade, semester, english) upsert。
提示：每册约 1~3 分钟；可加 --grades 3 限制先跑部分验证。
"""
import sys
import os
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import OpsWord
from app.models.ops_data import ensure_ops_tables
from app.routers.word import _llm_json, parse_llm_words, _strip_md_code

REVISION = "v1"
SEM_CN = {1: "上册", 2: "下册"}

PROMPT_TPL = (
    "你是精通国内各版本中小学教材的英语老师，熟悉各版本各年级教材的单元结构与词汇表。\n"
    "教材：英语《{version}》{grade_cn}{sem_cn}\n"
    "请依据这套教材的真实内容，生成该册全册的单元单词表。\n"
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


def generate_book(db, version, grade, semester) -> dict:
    grade_cn = f"{grade}年级"
    sem_cn = SEM_CN[semester]
    raw = _llm_json(
        PROMPT_TPL.format(version=version, grade_cn=grade_cn, sem_cn=sem_cn),
        system="你只输出单词表文本，不要任何解释。", max_tokens=4000, timeout=180,
    )
    words = parse_llm_words(_strip_md_code(raw))
    # 权威重灌：真删该册旧数据（含 LLM 重复/乱序残留），避免 UNIQUE 冲突
    db.query(OpsWord).filter(
        OpsWord.version == version,
        OpsWord.grade == grade,
        OpsWord.semester == semester,
    ).delete()
    db.flush()
    imported = 0
    seen = set()
    for w in words:
        en = (w.get("english") or "").strip()
        cn = (w.get("chinese") or "").strip()
        if not en or not cn or en.lower() in seen:
            continue
        seen.add(en.lower())
        db.add(OpsWord(
            version=version, grade=grade, semester=semester,
            unit=w.get("unit"), unit_title=w.get("unit_title") or "",
            english=en, chinese=cn,
            phonetic=(w.get("phonetic") or "").strip() or None,
            revision=REVISION,
        ))
        imported += 1
    db.commit()
    return {"imported": imported, "skipped": 0, "words": len(words)}


def main():
    args = sys.argv[1:]
    version = "人教版PEP"
    grades = [3, 4, 5, 6]
    if "--version" in args:
        version = args[args.index("--version") + 1]
    if "--grades" in args:
        grades = [int(g) for g in args[args.index("--grades") + 1].split()]
    ensure_ops_tables()
    db = SessionLocal()
    try:
        total = {"imported": 0, "skipped": 0, "words": 0, "books": 0}
        for grade in grades:
            for semester in (1, 2):
                t0 = time.time()
                try:
                    r = generate_book(db, version, grade, semester)
                except Exception as e:
                    print(f"  [fail] {version} {grade}年级{SEM_CN[semester]}: {e}")
                    db.rollback()
                    continue
                total["books"] += 1
                for k in ("imported", "skipped", "words"):
                    total[k] += r[k]
                print(f"  [ok] {version} {grade}年级{SEM_CN[semester]}: 新增{r['imported']} 跳过{r['skipped']} 共{r['words']} 耗时{int(time.time()-t0)}s")
        print(f"\n== 完成：{total['books']} 册，新增 {total['imported']}，跳过 {total['skipped']}")
    finally:
        db.close()


if __name__ == "__main__":
    main()
