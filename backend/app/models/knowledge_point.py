from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, func, Boolean, Table
from sqlalchemy.orm import relationship
from app.database import Base


# 知识点-错误类型关联表
kp_error_type = Table(
    "kp_error_type",
    Base.metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("knowledge_point_id", Integer, ForeignKey("knowledge_point.id", ondelete="CASCADE"), nullable=False),
    Column("error_type_id", Integer, ForeignKey("error_type.id", ondelete="CASCADE"), nullable=False),
)


def ensure_kp_dimension_columns() -> None:
    """knowledge_point 表补教学维度列（tags/requirement/kp_type，幂等）"""
    from sqlalchemy import text as sa_text
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        cols = [row[1] for row in db.execute(sa_text("PRAGMA table_info(knowledge_point)")).fetchall()]
        added = []
        for col, ddl in (
            ("tags", "ALTER TABLE knowledge_point ADD COLUMN tags TEXT"),
            ("requirement", "ALTER TABLE knowledge_point ADD COLUMN requirement VARCHAR(50)"),
            ("kp_type", "ALTER TABLE knowledge_point ADD COLUMN kp_type VARCHAR(50)"),
        ):
            if col not in cols:
                db.execute(sa_text(ddl))
                added.append(col)
        if added:
            db.commit()
            print(f"[kp] knowledge_point 表已新增列: {', '.join(added)}")
    finally:
        db.close()


class KnowledgePoint(Base):
    __tablename__ = "knowledge_point"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(200), nullable=False)
    subject_id = Column(Integer, ForeignKey("subject.id"), nullable=False)
    grade = Column(Integer, nullable=True)  # 年级 1-12
    semester = Column(Integer, nullable=True)  # 学期 1-2
    chapter = Column(String(200), nullable=True)  # 教材章节/单元（教材同步导入）
    description = Column(Text, nullable=True)  # 知识点一句话说明（教材同步导入）
    version = Column(String(100), nullable=True)  # 教材版本（教材同步导入，如 人教版/统编版）
    tags = Column(Text, nullable=True)  # 教学标签 JSON 数组，如 ["重点","难点","易错点"]
    requirement = Column(String(50), nullable=True)  # 认知要求：识记/理解/背诵/运用/综合
    kp_type = Column(String(50), nullable=True)  # 学科内容类型：代数/函数/几何/阅读…（按学科自由维护）
    deleted = Column(Boolean, default=False, nullable=False)  # 软删除标记
    created_at = Column(DateTime, server_default=func.now())

    # Relationships
    subject = relationship("Subject", back_populates="knowledge_points")
    error_types = relationship("ErrorType", secondary=kp_error_type, back_populates="knowledge_points")
