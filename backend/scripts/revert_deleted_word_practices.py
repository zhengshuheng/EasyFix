"""清理：已删除的单词练习对应复习日志与单词计数"""
import os
import sys
from datetime import timedelta

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.database import SessionLocal
from app.models import Word, WordReviewLog
from app.models.practice_set import PracticeSet, WordReviewSession


def cleanup(apply_fix=False):
    db = SessionLocal()
    try:
        deleted_ps = (
            db.query(PracticeSet)
            .filter(PracticeSet.deleted == True, PracticeSet.source_type == "word")
            .all()
        )
        print(f"deleted word practices: {len(deleted_ps)}")
        reverted_logs = 0
        reverted_words = 0

        for ps in deleted_ps:
            sessions = (
                db.query(WordReviewSession)
                .filter(WordReviewSession.practice_set_id == ps.id)
                .all()
            )
            for s in sessions:
                # 该场次时间窗内的有效日志
                logs = (
                    db.query(WordReviewLog)
                    .filter(
                        WordReviewLog.deleted == False,
                        WordReviewLog.reviewed_at >= s.reviewed_at - timedelta(minutes=2),
                        WordReviewLog.reviewed_at <= s.reviewed_at + timedelta(hours=3),
                    )
                    .all()
                )
                if not logs:
                    continue
                print(f"  ps={ps.id} session={s.id} at={s.reviewed_at} logs={len(logs)} total_count={s.total_count}")
                if not apply_fix:
                    continue
                # 按日志回滚单词计数
                for log in logs:
                    w = db.query(Word).filter(Word.id == log.word_id).first()
                    if w:
                        w.review_count = max(0, (w.review_count or 0) - 1)
                        if log.is_correct:
                            w.correct_count = max(0, (w.correct_count or 0) - 1)
                        reverted_words += 1
                    log.deleted = True
                    reverted_logs += 1
        if apply_fix:
            db.commit()
            print(f"reverted logs={reverted_logs}, word updates={reverted_words}")
        else:
            print("dry-run only")
    except Exception as e:
        db.rollback()
        print("error", e)
        raise
    finally:
        db.close()


if __name__ == "__main__":
    cleanup(apply_fix="--fix" in sys.argv)
