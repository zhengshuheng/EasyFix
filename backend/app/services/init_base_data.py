"""基础数据种子：学科 / 标签 / 错误类型

首次启动或缺失时自动写入（幂等：按名称/学科逐条检查，缺失才插入）。
"""
from sqlalchemy.orm import Session

from app.models.subject import Subject
from app.models.tag import Tag
from app.models.error_type import ErrorType


DEFAULT_SUBJECTS = ["数学", "英语"]

DEFAULT_TAGS = [
    ("重点", "#f25714"),
    ("粗心", "#409eff"),
    ("重复错误", "#e4b117"),
    ("薄弱", "#409eff"),
    ("六上Unit1", "#409EFF"),
    ("六上Unit2", "#67C23A"),
    ("六上Unit3", "#E6A23C"),
    ("六上Unit4", "#F56C6C"),
    ("六上Unit5", "#909399"),
    ("六上Unit6", "#00c1de"),
]

# 学科 -> 该学科的错误类型（与用户既有数据一致）
DEFAULT_ERROR_TYPES = {
    "数学": ["计算错误", "审题不清", "概念错误", "完全不会"],
    "英语": ["背诵拼写", "语法"],
}


def _ensure_subject(db: Session, name: str) -> Subject:
    """按名称查学科，缺失则创建，返回记录（未 commit，由调用方统一提交）"""
    subject = db.query(Subject).filter(Subject.name == name).first()
    if not subject:
        subject = Subject(name=name)
        db.add(subject)
        db.flush()
    return subject


def _ensure_tag(db: Session, name: str, color: str) -> None:
    if not db.query(Tag).filter(Tag.name == name).first():
        db.add(Tag(name=name, color=color))
        db.flush()


def _ensure_error_type(db: Session, name: str, subject: Subject) -> None:
    exists = (
        db.query(ErrorType)
        .filter(ErrorType.name == name, ErrorType.subject_id == subject.id)
        .first()
    )
    if not exists:
        db.add(ErrorType(name=name, subject_id=subject.id))
        db.flush()


def init_base_data(db: Session) -> None:
    """内置基础数据：学科 → 标签 → 错误类型，全部完成后统一提交"""
    for name in DEFAULT_SUBJECTS:
        _ensure_subject(db, name)

    for name, color in DEFAULT_TAGS:
        _ensure_tag(db, name, color)

    for subject_name, type_names in DEFAULT_ERROR_TYPES.items():
        subject = _ensure_subject(db, subject_name)
        for type_name in type_names:
            _ensure_error_type(db, type_name, subject)

    db.commit()
