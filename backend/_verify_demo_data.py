"""验证 init_demo_data：创建演示小孩 + 1-6年级数据，且幂等"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.database import SessionLocal, Base, engine
from app.models.user import User
from app.models.subject import Subject
from app.models.error_book import ErrorBook
from app.models.question import Question
from app.models.practice_set import PracticeSet, PracticeSetQuestion
from app.models.word import Word, WordReviewLog, WordReview
from app.models.star import StarRecord, StarBalance
from app.services.init_base_data import init_base_data
from app.services.init_demo_data import init_demo_data

Base.metadata.create_all(bind=engine)

with SessionLocal() as db:
    init_base_data(db)
    init_demo_data(db)

    demo = db.query(User).filter(User.username == "demo").first()
    assert demo is not None, "FAIL: demo 用户未创建"
    assert demo.role == "child" and demo.pin == "1234", "FAIL: demo 属性"
    print("demo user:", demo.id, demo.display_name, demo.pin)

    qs = db.query(Question).filter(Question.deleted == False).all()
    grades = sorted(set(q.grade for q in qs))
    print("questions:", len(qs), "grades:", grades)
    assert len(qs) == 18, f"FAIL: 错题数 {len(qs)}"
    assert grades == [1, 2, 3, 4, 5, 6], "FAIL: 未覆盖1-6年级"

    books = db.query(ErrorBook).filter(ErrorBook.deleted == False).all()
    print("error_books:", [b.name for b in books])

    pss = db.query(PracticeSet).filter(PracticeSet.deleted == False).all()
    print("practice_sets:", [(p.name, p.subject_id, p.accuracy) for p in pss])
    assert len(pss) == 2, f"FAIL: 练习集 {len(pss)}"
    psq = db.query(PracticeSetQuestion).count()
    print("practice_set_questions:", psq)
    assert psq > 0, "FAIL: 无练习集题目关联"

    words = db.query(Word).filter(Word.deleted == False).all()
    print("words:", len(words), "word grades:", sorted(set(w.grade for w in words)))
    assert len(words) == 30, f"FAIL: 单词数 {len(words)}"
    logs = db.query(WordReviewLog).count()
    wr = db.query(WordReview).count()
    print("word_review_logs:", logs, "word_review_sessions:", wr)
    assert logs > 0 and wr > 0, "FAIL: 单词复习记录缺失"

    stars = db.query(StarRecord).filter(StarRecord.user_id == demo.id).count()
    balance = db.query(StarBalance).filter(StarBalance.user_id == demo.id).first()
    print("star_records:", stars, "balance:", balance.balance if balance else None)
    assert stars > 0 and balance and balance.balance > 0, "FAIL: 激励数据缺失"

    # 幂等
    before = db.query(Question).count()
    init_demo_data(db)
    after = db.query(Question).count()
    print("idempotent:", before, "->", after)
    assert before == after, "FAIL: 非幂等"
    print("PASS: 全部通过")
