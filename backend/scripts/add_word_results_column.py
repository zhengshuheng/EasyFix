import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from app.database import engine
from sqlalchemy import inspect, text

insp = inspect(engine)
print("dialect", engine.dialect.name)
print("tables", insp.get_table_names())
if "word_review_session" in insp.get_table_names():
    cols = [c["name"] for c in insp.get_columns("word_review_session")]
    print("word_review_session cols", cols)
    if "word_results" not in cols:
        with engine.begin() as conn:
            conn.execute(text("ALTER TABLE word_review_session ADD COLUMN word_results TEXT"))
        print("added word_results")
    else:
        print("word_results already exists")
