"""验证 init_base_data：全新库建表 → 补种子 → 再跑一遍幂等"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.database import SessionLocal, Base, engine
from app.models.subject import Subject
from app.models.tag import Tag
from app.models.error_type import ErrorType
from app.services.init_base_data import init_base_data

# 0) 建表（等同服务启动）
Base.metadata.create_all(bind=engine)

with SessionLocal() as db:
    # 1) 首次：写入种子
    init_base_data(db)
    subjects = db.query(Subject).filter(Subject.deleted == False).order_by(Subject.id).all()
    tags = db.query(Tag).filter(Tag.deleted == False).order_by(Tag.id).all()
    error_types = db.query(ErrorType).filter(ErrorType.deleted == False).order_by(ErrorType.id).all()
    print("subjects:", [(s.id, s.name) for s in subjects])
    print("tags:", [(t.id, t.name, t.color) for t in tags])
    print("error_types:", [(e.id, e.name, e.subject_id) for e in error_types])
    assert [s.name for s in subjects] == ["数学", "英语"], "FAIL: 学科种子"
    assert len(tags) == 10, f"FAIL: 标签种子 {len(tags)}"
    assert len(error_types) == 6, f"FAIL: 错误类型种子 {len(error_types)}"
    assert all(e.subject_id in (1, 2) for e in error_types), "FAIL: 错误类型未关联学科"
    print("PASS: 全新库首次启动写入种子成功")

    # 2) 再跑一遍：count 不变（幂等）
    before = (len(subjects), len(tags), len(error_types))
    init_base_data(db)
    after = (
        db.query(Subject).filter(Subject.deleted == False).count(),
        db.query(Tag).filter(Tag.deleted == False).count(),
        db.query(ErrorType).filter(ErrorType.deleted == False).count(),
    )
    print("idempotent:", before, "->", after)
    assert before == after, "FAIL: 非幂等"
    print("PASS: 重复启动不重复插入（幂等）")
