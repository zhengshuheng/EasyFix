"""统一时间口径：本项目为本地单机运行，所有入库时间都用**本地时间**。

背景：SQLite 的 CURRENT_TIMESTAMP（即 server_default=func.now()）返回 UTC，
导致出题/作答等记录时间比北京时间少 8 小时。因此模型统一改为
`default=now_local`（Python 端本地时间），数据库层默认值仅作为兜底保留。
"""
from datetime import datetime, date


def now_local() -> datetime:
    """本地当前时间（naive，和 datetime.now() 一致，便于与既有数据比较）"""
    return datetime.now()


def infer_grade(enrollment_date, today=None) -> int:
    """根据一年级入学日期推断当前年级（学年按 9 月 1 日分界）。

    例：2023-09-01 入学一年级 →
        2023-09~2024-08 一年级、2024-09~2025-08 二年级、…2026-09 起四年级。
    未设置入学日期返回 1（默认一年级）；超出小学范围（>12）按 12 封顶。
    """
    if not enrollment_date:
        return 1
    if isinstance(enrollment_date, str):
        try:
            enrollment_date = date.fromisoformat(str(enrollment_date)[:10])
        except ValueError:
            return 1
    today = today or date.today()
    # 入学学年起始年（9 月起算；1~8 月录入的日期也按同年 9 月入学处理）
    start_year = enrollment_date.year
    # 当前学年起始年：9 月及以后属于新学年
    cur_start = today.year if today.month >= 9 else today.year - 1
    grade = cur_start - start_year + 1
    if grade < 1:
        grade = 1
    return min(grade, 12)


def enrollment_date_from_grade(grade, today=None) -> date:
    """由年级反推入学日期（仅用于旧数据迁移：保留用户已设的年级意图）"""
    today = today or date.today()
    cur_start = today.year if today.month >= 9 else today.year - 1
    year = cur_start - (int(grade or 1) - 1)
    return date(year, 9, 1)

