"""一次性迁移：错题/练习分表 + 全链路按小孩隔离（M1 建模阶段）。

背景（用户确认）：
- 现有题目/练习集全部视为脏数据，清空。
- 错题库改为「练习批改判错派生」（error_question 新表），练习题目改为快照表
  （practice_question），作答记录独立成表（practice_attempt）。
- practice_set / practice_set_question / word_review_session 结构变更 → 直接重建。
  重建由后端启动时的 Base.metadata.create_all 完成。

保留（共享或已隔离的数据）：
  subject, knowledge_point, word, achievement*, star_action, error_type, tag, users,
  word_progress, word_review, word_review_log, star_balance, star_record,
  achievement_progress, redemption, error_book（错题本容器）

用法：python tools/migrate_kid_refactor.py
"""
import os
import sqlite3
import sys

DB = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "backend", "easyfix.db")

CLEAR_TABLES = ["question", "question_tag", "similar_question"]          # 只清数据
DROP_TABLES = ["practice_set_question", "practice_set", "word_review_session"]  # 结构变更，重建


def snapshot(con, label):
    print(f"--- {label} ---")
    for t in CLEAR_TABLES + DROP_TABLES:
        try:
            n = con.execute(f"SELECT count(*) FROM {t}").fetchone()[0]
            print(f"  {t:24} {n} 行")
        except sqlite3.OperationalError:
            print(f"  {t:24} (不存在)")


def main():
    if not os.path.exists(DB):
        print(f"数据库不存在: {DB}")
        return 1
    con = sqlite3.connect(DB, timeout=30)
    snapshot(con, "迁移前")
    with con:
        for t in CLEAR_TABLES:
            try:
                con.execute(f"DELETE FROM {t}")
            except sqlite3.OperationalError as e:
                print(f"  清空 {t} 跳过: {e}")
        for t in DROP_TABLES:
            con.execute(f"DROP TABLE IF EXISTS {t}")
    con.execute("VACUUM")  # 需在事务外执行
    print("已清空脏数据并删除待重建表（下次启动自动按新结构建表）")
    snapshot(con, "迁移后")
    con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
