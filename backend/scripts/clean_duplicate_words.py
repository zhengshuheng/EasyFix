"""检查并清理单词表中的重复英文词条（合并释义，软删除重复）"""
import sys
import os
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import Word, WordReviewLog


def normalize(en: str) -> str:
    return (en or "").strip().lower()


def score_word(w: Word) -> tuple:
    return (
        w.review_count or 0,
        w.correct_count or 0,
        1 if w.phonetic else 0,
        len(w.chinese or ""),
        w.id,
    )


def merge_chinese(keep_cn: str, drop_cn: str) -> str:
    """合并中英释义，去重分段"""
    if not drop_cn:
        return keep_cn
    if not keep_cn:
        return drop_cn
    if drop_cn.strip() in keep_cn:
        return keep_cn
    # 用分号/逗号拆分后合并唯一片段
    parts = []
    for chunk in (keep_cn + "；" + drop_cn).replace("，", "；").split("；"):
        c = chunk.strip()
        if c and c not in parts:
            parts.append(c)
    return "；".join(parts)


def fix_truncated_phrases(db, apply_fix=False):
    """清理被错误截断成单词根的短语词条（完整短语已存在则软删）"""
    prefix_map = {
        "part in": "take part in",
        "care of": "take care of",
    }
    candidates = db.query(Word).filter(
        Word.deleted == False,
        Word.english == "take",
    ).all()
    fixed = 0
    for w in candidates:
        cn = (w.chinese or "").strip()
        for prefix, full_en in prefix_map.items():
            if cn.startswith(prefix):
                exists = db.query(Word).filter(
                    Word.deleted == False,
                    Word.english == full_en,
                    Word.id != w.id,
                ).first()
                if exists:
                    w.deleted = True
                    fixed += 1
                    print(f"{'DROP' if apply_fix else 'WILL DROP'} truncated id={w.id} take/{cn[:24]!r} (keep {full_en} id={exists.id})")
                else:
                    w.english = full_en
                    w.chinese = cn[len(prefix):].strip() or full_en
                    fixed += 1
                    print(f"{'FIX' if apply_fix else 'WILL'} phrase id={w.id} -> {full_en!r}")
                break
    return fixed


def cleanup(apply_fix=False):
    db = SessionLocal()
    try:
        # 1. 先修短语截断
        fixed_phrases = fix_truncated_phrases(db, apply_fix=apply_fix)
        if apply_fix:
            db.commit()

        # 2. 扫描重复
        words = db.query(Word).filter(Word.deleted == False).all()
        groups = defaultdict(list)
        for w in words:
            key = normalize(w.english)
            if key:
                groups[key].append(w)

        dups = {k: v for k, v in groups.items() if len(v) > 1}
        print(f"\nactive words after phrase fix: {len(words)}")
        print(f"duplicate groups: {len(dups)}")

        dropped = 0
        migrated_logs = 0

        for key in sorted(dups.keys()):
            items = sorted(dups[key], key=score_word, reverse=True)
            keep = items[0]
            for d in items[1:]:
                # 迁移复习日志
                logs = db.query(WordReviewLog).filter(
                    WordReviewLog.word_id == d.id,
                    WordReviewLog.deleted == False
                ).all()
                for log in logs:
                    log.word_id = keep.id
                    migrated_logs += 1

                # 合并标签
                for t in list(d.tags):
                    if t not in keep.tags:
                        keep.tags.append(t)

                # 合并释义
                keep.chinese = merge_chinese(keep.chinese, d.chinese)

                # 累加复习计数
                if d.review_count:
                    keep.review_count = (keep.review_count or 0) + (d.review_count or 0)
                if d.correct_count:
                    keep.correct_count = (keep.correct_count or 0) + (d.correct_count or 0)

                # 补全缺失字段
                if not keep.phonetic and d.phonetic:
                    keep.phonetic = d.phonetic
                if not keep.grade and d.grade:
                    keep.grade = d.grade
                if not keep.semester and d.semester:
                    keep.semester = d.semester

                d.deleted = True
                dropped += 1
                print(f"{'DROP' if apply_fix else 'WILL DROP'} id={d.id} {d.english!r} keep={keep.id}")

        if apply_fix:
            db.commit()
            print(f"\nphrases fixed: {fixed_phrases}")
            print(f"soft-deleted: {dropped}")
            print(f"review logs migrated: {migrated_logs}")
            remaining = db.query(Word).filter(Word.deleted == False).count()
            print(f"remaining active words: {remaining}")
        else:
            print(f"\ndry-run: phrases={fixed_phrases}, would soft-delete {dropped}")
    except Exception as e:
        db.rollback()
        print(f"error: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    apply = "--fix" in sys.argv
    cleanup(apply_fix=apply)
