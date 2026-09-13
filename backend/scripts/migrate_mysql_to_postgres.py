"""MySQL -> PostgreSQL 数据迁移（全表拷贝）"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text, inspect

MYSQL_URL = "mysql+pymysql://root:lingxi520@localhost:3306/easyfix?charset=utf8mb4"
PG_URL = "postgresql+psycopg2://postgres:lingxi520@localhost:5432/easyfix"

# 优先迁移顺序（有外键依赖）
TABLE_ORDER = [
    "subject",
    "error_book",
    "tag",
    "error_type",
    "knowledge_point",
    "question",
    "question_tag",
    "similar_question",
    "reading_passage",
    "reading_question",
    "practice_set",
    "practice_set_question",
    "word",
    "word_tag",
    "word_review",
    "word_review_log",
    "word_review_session",
    "achievement",
    "achievement_config",
    "achievement_progress",
    "star_action",
    "star_balance",
    "star_record",
    "reward",
    "redemption",
    "learning_report",
    "operation_log",
]


def normalize_value(col_name, v, bool_cols=None):
    if v is None:
        return None
    if bool_cols and col_name in bool_cols and isinstance(v, (int, bool)):
        return bool(v)
    return v


def migrate():
    src = create_engine(MYSQL_URL, pool_pre_ping=True)
    dst = create_engine(PG_URL, pool_pre_ping=True)
    src_insp = inspect(src)
    dst_insp = inspect(dst)
    src_tables = set(src_insp.get_table_names())
    dst_tables = set(dst_insp.get_table_names())

    tables = [t for t in TABLE_ORDER if t in src_tables and t in dst_tables]
    for t in sorted(src_tables):
        if (
            t not in tables
            and t in dst_tables
            and not t.startswith("star_balance_backup")
            and not t.startswith("star_record_backup")
        ):
            tables.append(t)

    print("migrate tables:", tables)

    with src.connect() as sc, dst.connect() as dc:
        for table in reversed(tables):
            dc.execute(text(f'TRUNCATE TABLE "{table}" RESTART IDENTITY CASCADE'))
        dc.commit()

        for table in tables:
            scol = {c["name"] for c in src_insp.get_columns(table)}
            dcols = dst_insp.get_columns(table)
            bool_cols = {c["name"] for c in dcols if str(c["type"]).lower().startswith("boolean")}
            cols = [c["name"] for c in dcols if c["name"] in scol]
            if not cols:
                print(f"skip {table}: no common columns")
                continue

            rows = sc.execute(text(f"SELECT {', '.join(f'`{c}`' for c in cols)} FROM `{table}`")).fetchall()
            if not rows:
                print(f"{table}: 0 rows")
                continue

            placeholders = ", ".join([f":{c}" for c in cols])
            col_sql = ", ".join([f'"{c}"' for c in cols])
            insert_sql = text(f'INSERT INTO "{table}" ({col_sql}) VALUES ({placeholders})')

            batch = []
            for r in rows:
                data = {c: normalize_value(c, r[i], bool_cols) for i, c in enumerate(cols)}
                if table == "practice_set" and data.get("passage_id") is not None:
                    exists = dc.execute(
                        text("SELECT 1 FROM reading_passage WHERE id=:id"),
                        {"id": data["passage_id"]},
                    ).first()
                    if not exists:
                        data["passage_id"] = None
                batch.append(data)
                if len(batch) >= 200:
                    dc.execute(insert_sql, batch)
                    batch = []
            if batch:
                dc.execute(insert_sql, batch)
            dc.commit()
            print(f"{table}: {len(rows)} rows")

    print("migration done")


if __name__ == "__main__":
    migrate()
