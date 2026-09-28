"""Ops 教材数据仓库（主库表）

定位：统一内置/维护各科目·版本·年级·册次的知识点与英语单词，
用户空间只读同步（POST /api/sync/*）。准确性由 Ops 后台统一维护。

表（仅主库 easyfix_main.db）：
  ops_knowledge_point — 科目/版本/年级/册次/知识点（含教学维度）
  ops_word           — 版本/年级/册次/单元/单词（含例句）

修订机制：revision（如 v2026.1）驱动「同步最新」；空间库按
edition_key 全量替换（幂等），避免重复初始化翻倍。
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, UniqueConstraint
from sqlalchemy import func
from app.database import Base
from app.utils.timeutil import now_local


class OpsKnowledgePoint(Base):
    __tablename__ = "ops_knowledge_point"

    id = Column(Integer, primary_key=True, autoincrement=True)
    subject = Column(String(50), nullable=False)   # 学科名：数学/语文/英语
    version = Column(String(100), nullable=False)  # 教材版本：人教版/统编版/人教PEP…
    grade = Column(Integer, nullable=False)        # 年级 1-6
    semester = Column(Integer, nullable=False)     # 学期 1=上册 2=下册
    name = Column(String(200), nullable=False)     # 知识点名称
    chapter = Column(String(200), nullable=True)   # 单元/章节
    description = Column(Text, nullable=True)      # 一句话说明
    requirement = Column(String(50), nullable=True)  # 认知要求：识记/理解/背诵/运用/综合
    tags = Column(Text, nullable=True)             # 教学标签 JSON 数组
    kp_type = Column(String(50), nullable=True)    # 学科内容类型
    revision = Column(String(20), nullable=True)   # 数据修订号
    source_type = Column(String(20), nullable=True, default="ai")  # 来源：ctsf-online/ctsf-local/textbook-online/textbook-local/ai
    ocr_mode = Column(String(20), nullable=True)   # 识别方式：authority(权威在线源)/multimodal(多模态)/local(本地OCR)/llm(AI生成)
    import_batch = Column(String(24), nullable=True)  # 教材任务批次：任务成功后清理同教材旧批次，防重复累积（NULL=手动/AI指令/大纲，永久保留）
    deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=now_local, server_default=func.now())
    updated_at = Column(DateTime, default=now_local, onupdate=now_local)

    __table_args__ = (
        UniqueConstraint("subject", "version", "grade", "semester", "name",
                         name="uq_ops_kp_svgsn"),
    )


class OpsEdition(Base):
    """教材版本实体（主库）：科目 + 版本名，供运营后台管理版本（增删改）。

    知识点/单词按 (subject, version) 挂靠版本；删除版本时连带软删数据。
    """
    __tablename__ = "ops_edition"

    id = Column(Integer, primary_key=True, autoincrement=True)
    subject = Column(String(50), nullable=False)   # 学科名：数学/语文/英语
    name = Column(String(100), nullable=False)     # 教材版本名：人教版/统编版/人教PEP…
    description = Column(Text, nullable=True)      # 说明
    enabled = Column(Boolean, default=True, nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=now_local, server_default=func.now())
    updated_at = Column(DateTime, default=now_local, onupdate=now_local)

    __table_args__ = (
        UniqueConstraint("subject", "name", name="uq_ops_edition_sn"),
    )


class OpsWord(Base):
    __tablename__ = "ops_word"

    id = Column(Integer, primary_key=True, autoincrement=True)
    version = Column(String(100), nullable=False)  # 教材版本：人教PEP/外研版…
    grade = Column(Integer, nullable=False)        # 年级 1-6
    semester = Column(Integer, nullable=False)     # 学期 1=上册 2=下册
    unit = Column(Integer, nullable=True)          # 单元号
    unit_title = Column(String(200), nullable=True)  # 单元英文标题
    english = Column(String(200), nullable=False)
    chinese = Column(Text, nullable=False)
    phonetic = Column(String(100), nullable=True)
    example_sentences = Column(Text, nullable=True)  # 例句 JSON：[{"en","zh"}]
    revision = Column(String(20), nullable=True)   # 数据修订号
    source_type = Column(String(20), nullable=True, default="ai")  # 来源：authority(权威词表)/ai(AI生成)/pdf(教材PDF提取)/manual(人工)
    deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=now_local, server_default=func.now())
    updated_at = Column(DateTime, default=now_local, onupdate=now_local)

    __table_args__ = (
        UniqueConstraint("version", "grade", "semester", "english",
                         name="uq_ops_word_vgse"),
    )


class SpaceSyncState(Base):
    """主库：记录每个空间各数据源的同步状态（edition 对齐 ops 修订号）"""
    __tablename__ = "space_sync_state"

    id = Column(Integer, primary_key=True, autoincrement=True)
    space_key = Column(String(100), nullable=False, index=True)
    data_type = Column(String(30), nullable=False)      # kp / word
    version = Column(String(100), nullable=False)       # 教材版本（人教PEP/人教版/统编版…）
    grade = Column(Integer, nullable=False, default=0)  # 0=整版全册（kp 用）；单词按册
    semester = Column(Integer, nullable=False, default=0)
    edition = Column(String(50), nullable=False)        # 已同步的修订号（如 v1）
    updated_at = Column(DateTime, default=now_local, onupdate=now_local)

    __table_args__ = (
        UniqueConstraint("space_key", "data_type", "version", "grade", "semester",
                         name="uq_space_sync_state_key"),
    )


class OpsAiProvider(Base):
    """AI 模型厂商配置（主库）：多厂商凭证/模型管理。

    学生端按 vendor 选厂商 → 选该厂商模型；LLM 与多模态 OCR 共用同一网关收敛点
    AIGatewayClient(config)。vision_models 留空表示该厂商不支持 OCR（纯文本厂商如 DeepSeek）。
    """
    __tablename__ = "ops_ai_provider"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)          # 厂商显示名：DeepSeek / OpenAI / 阿里云百炼 / 智谱GLM / Anthropic
    vendor = Column(String(50), nullable=False)         # 业务标识：deepseek / openai / dashscope / zhipu / anthropic / …
    protocol = Column(String(20), nullable=False, default="openai")  # openai（兼容协议）/ anthropic
    base_url = Column(String(255), nullable=True)       # 上游 base_url（空=官方默认）
    api_key = Column(Text, nullable=True)               # 上游 Key（列表接口掩码返回）
    models = Column(Text, nullable=True)                # 逗号分隔可用模型
    vision_models = Column(Text, nullable=True)         # 逗号分隔视觉模型（留空=不支持 OCR）
    enabled = Column(Boolean, default=True, nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=now_local, server_default=func.now())
    updated_at = Column(DateTime, default=now_local, onupdate=now_local)

    __table_args__ = (
        UniqueConstraint("vendor", name="uq_ops_ai_provider_vendor"),
    )


class OpsPromptRule(Base):
    """AI 出题规则（主库，运营后台可维护）：scope → rule_text，保障出题质量不依赖改代码。

    scope 命名约定（与 question_prompts / llm 的读取端一致）：
      "general"             通用出题规则段（出题要求/看图列式/年级匹配/难度标注/变式要求）
      "base:数学/语文/英语/默认"   科目基础段（课标导向+语言风格+质量硬性要求）
      "style:数学:小学/初中/高中"   学段真题范例段（该学段真实试卷长什么样）
    读取端优先取 DB 已启用项，未保存的 scope 用代码内置默认（prompt_rules_service.DEFAULT_GENERAL_RULES 与 question_prompts 常量）。
    空 rule_text（或删除记录）= 恢复默认。
    """
    __tablename__ = "ops_prompt_rule"

    id = Column(Integer, primary_key=True, autoincrement=True)
    scope = Column(String(64), nullable=False, unique=True)
    rule_text = Column(Text, nullable=False, default="")
    enabled = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=now_local, server_default=func.now())
    updated_at = Column(DateTime, default=now_local, onupdate=now_local)


class OpsAssessRule(Base):
    """评测规则配置（主库，运营后台可维护）：key → value，评测策略（组卷/排重/坏题校验）可调不依赖改代码。

    默认值与元数据在 assess_rules_service.ASSESS_RULES_META；读取端（assessment.py start 组卷逻辑）
    取 DB 已启用项覆盖内置默认；未配置/配置损坏时用代码内置默认。
    """
    __tablename__ = "ops_assess_rule"

    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String(64), nullable=False, unique=True)
    value = Column(Text, nullable=False, default="")
    enabled = Column(Boolean, default=True, nullable=False)
    created_at = Column(DateTime, default=now_local, server_default=func.now())
    updated_at = Column(DateTime, default=now_local, onupdate=now_local)


def ensure_ops_tables() -> None:
    """主库幂等建表（模板库/空间库不需要 ops 表）"""
    from sqlalchemy import text as sa_text
    from app.database import SessionLocal
    db = SessionLocal()
    try:
        Base.metadata.create_all(bind=db.get_bind())
        # 兜底补列（表结构演进用）
        kp_cols = [r[1] for r in db.execute(sa_text("PRAGMA table_info(ops_knowledge_point)")).fetchall()]
        word_cols = [r[1] for r in db.execute(sa_text("PRAGMA table_info(ops_word)")).fetchall()]
        added = []
        for table, cols, ddl in (
            ("ops_knowledge_point", kp_cols, "ALTER TABLE ops_knowledge_point ADD COLUMN revision VARCHAR(20)"),
            ("ops_knowledge_point", kp_cols, "ALTER TABLE ops_knowledge_point ADD COLUMN source_type VARCHAR(20)"),
            ("ops_knowledge_point", kp_cols, "ALTER TABLE ops_knowledge_point ADD COLUMN ocr_mode VARCHAR(20)"),
            ("ops_knowledge_point", kp_cols, "ALTER TABLE ops_knowledge_point ADD COLUMN import_batch VARCHAR(24)"),
            ("ops_word", word_cols, "ALTER TABLE ops_word ADD COLUMN revision VARCHAR(20)"),
            ("ops_word", word_cols, "ALTER TABLE ops_word ADD COLUMN example_sentences TEXT"),
            ("ops_word", word_cols, "ALTER TABLE ops_word ADD COLUMN source_type VARCHAR(20)"),
        ):
            name = ddl.split("ADD COLUMN ")[1].split(" ")[0]
            if name not in cols and ddl.split(" ")[2] == table:
                db.execute(sa_text(ddl))
                added.append(f"{table}.{name}")
        if added:
            db.commit()
            print(f"[ops] 补列: {', '.join(added)}")
        # 历史数据回填 ocr_mode（按 source_type 推断当时识别方式，幂等）
        if "ocr_mode" in kp_cols:
            db.execute(sa_text(
                "UPDATE ops_knowledge_point SET ocr_mode='authority' "
                "WHERE ocr_mode IS NULL AND source_type IN ('ctsf-online','ctsf-local')"
            ))
            db.execute(sa_text(
                "UPDATE ops_knowledge_point SET ocr_mode='local' "
                "WHERE ocr_mode IS NULL AND source_type IN ('textbook-online','textbook-local')"
            ))
            db.execute(sa_text(
                "UPDATE ops_knowledge_point SET ocr_mode='llm' "
                "WHERE ocr_mode IS NULL AND source_type IN ('ai')"
            ))
            db.commit()
        # 历史数据回填 source_type（word：早期 AI/手动导入统一标 ai，幂等）
        if "source_type" in word_cols:
            db.execute(sa_text(
                "UPDATE ops_word SET source_type='ai' WHERE source_type IS NULL"
            ))
            db.commit()
    finally:
        db.close()
