"""查看/清理英文单词中的标点符号"""
import re
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import Word

# 去掉句末/句首的句子标点；保留缩写点（a.m.）、撇号（What's）、连字符
SENTENCE_PUNCT = re.compile(r"^[\s\"'（(]+|[\s?!?!\"'，。！？；：、）)]+$")


def list_punctuated(apply_fix=False):
    db = SessionLocal()
    try:
        words = db.query(Word).filter(Word.deleted == False).all()
        print(f"total words: {len(words)}")
        changed = []
        for w in words:
            if not w.english:
                continue
            cleaned = SENTENCE_PUNCT.sub("", w.english).strip()
            cleaned = re.sub(r"\s+", " ", cleaned)
            if cleaned != w.english:
                print(f"{'FIX' if apply_fix else 'HIT'}: {w.english!r} -> {cleaned!r} | {w.chinese[:30]}")
                if apply_fix and cleaned:
                    w.english = cleaned
                    changed.append((w.id, cleaned))
        if apply_fix:
            db.commit()
            print(f"\nupdated {len(changed)} words")
        else:
            found = sum(1 for w in words if w.english and SENTENCE_PUNCT.search(w.english))
            print(f"\nfound {found} words needing cleanup")
    finally:
        db.close()


if __name__ == "__main__":
    apply = "--fix" in sys.argv
    list_punctuated(apply_fix=apply)
