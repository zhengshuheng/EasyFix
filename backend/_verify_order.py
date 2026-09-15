"""验证初始化顺序：admin=1、demo=2（内存库模拟全新部署）"""
import os
import sys

os.environ["DB_PATH"] = ":memory:"
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from app.database import SessionLocal, Base, engine
from app.models.user import User
from app.models.subject import Subject
from app.models.tag import Tag
from app.models.error_type import ErrorType
from app.services.init_base_data import init_base_data
from app.services.init_demo_data import init_demo_data

Base.metadata.create_all(bind=engine)

with SessionLocal() as db:
    init_base_data(db)
    db.add(User(
        username="admin",
        display_name="家长",
        role="admin",
        password_hash="x",
    ))
    db.commit()
    init_demo_data(db)

    users = db.query(User).order_by(User.id).all()
    print("users:", [(u.id, u.username, u.role) for u in users])
    assert users[0].username == "admin" and users[0].id == 1, "FAIL: admin 应为 id=1"
    assert users[1].username == "demo" and users[1].id == 2, "FAIL: demo 应为 id=2"
    assert db.query(Subject).filter(Subject.deleted == False).count() == 2
    assert db.query(Tag).filter(Tag.deleted == False).count() == 10
    assert db.query(ErrorType).filter(ErrorType.deleted == False).count() == 6
    print("PASS: admin=1 demo=2，基础种子正常")
