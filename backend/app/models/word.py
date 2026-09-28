"""
单词模型 - 存储单词信息及复习记录
"""
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


# 单词-标签关联表
word_tag = Table(
    "word_tag",
    Base.metadata,
    Column("word_id", Integer, ForeignKey("word.id"), primary_key=True),
    Column("tag_id", Integer, ForeignKey("tag.id"), primary_key=True),
)


class Word(Base):
    """单词表"""
    __tablename__ = "word"

    id = Column(Integer, primary_key=True, autoincrement=True)
    english = Column(String(200), nullable=False, index=True)  # 英文单词
    chinese = Column(Text, nullable=False)  # 中文释义
    phonetic = Column(String(100), nullable=True)  # 音标
    grade = Column(Integer, nullable=True)  # 年级 1-12
    semester = Column(Integer, nullable=True)  # 学期 1=上学期, 2=下学期
    unit = Column(Integer, nullable=True)  # 单元号（文本整表导入时识别 Unit N）
    unit_title = Column(String(200), nullable=True)  # 单元英文标题（如 "Meeting new people"）

    # 数据来源标记（ops 同步用；custom=手动/导入，ops=主库教材数据同步）
    source = Column(String(20), nullable=True, default="custom")  # custom/ops
    edition_key = Column(String(50), nullable=True)  # 同步修订标记（如 ops-v1）
    revision = Column(String(20), nullable=True)  # 数据修订号

    # 记忆增强（新增/导入单词时后台自动生成：拼读规则/词根词源/相关词）
    phonetic_rule = Column(Text, nullable=True)  # 拼读规则：按字母组合拆解怎么读（如 "ee → /iː/，ee 组合读长音 iː"）
    mnemonic = Column(Text, nullable=True)  # 联想记忆口诀（中文，帮助记忆）
    word_root = Column(String(500), nullable=True)  # 词根词缀拆解（如 "un-（否定前缀）+ happy → unhappy"）
    related_words = Column(Text, nullable=True)  # 相关词/形近词 JSON 数组：[{"en":"...","cn":"..."}]
    example_sentences = Column(Text, nullable=True)  # 语境例句 JSON 数组：[{"en":"...","zh":"..."}]（单词融入句子，不孤立学）

    # 复习相关（已废弃：自 v1.1 起复习数据按小孩隔离，存 WordProgress 表；以下列仅保留兼容旧库）
    review_count = Column(Integer, default=0)  # 复习次数
    correct_count = Column(Integer, default=0)  # 正确次数
    last_reviewed_at = Column(DateTime, nullable=True)  # 上次复习时间
    next_review_at = Column(DateTime, nullable=True)  # 下次复习时间

    # 记忆曲线参数（艾宾浩斯）（已废弃：见上）
    ease_factor = Column(Integer, default=250)  # 难度因子（单位：分钟）
    interval = Column(Integer, default=1)  # 当前间隔天数
    learning_phase = Column(String(20), default="新学")  # 新学/在途/遗忘点/牢记

    # 软删除
    deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    # 关系
    tags = relationship("Tag", secondary=word_tag, back_populates="words")
    review_logs = relationship("WordReviewLog", back_populates="word")


class WordReviewLog(Base):
    """单词复习记录表"""
    __tablename__ = "word_review_log"

    id = Column(Integer, primary_key=True, autoincrement=True)
    word_id = Column(Integer, ForeignKey("word.id"), nullable=False)
    user_id = Column(Integer, nullable=True, index=True)  # 复习小孩（NULL=旧数据，迁移后归属演示小孩）
    is_correct = Column(Boolean, nullable=False)  # 是否正确
    user_answer = Column(Text, nullable=True)  # 用户答案
    review_type = Column(Integer, nullable=False)  # 复习题型 1=默写, 2=选择
    reviewed_at = Column(DateTime, default=datetime.now, nullable=False)
    deleted = Column(Boolean, default=False, nullable=False)  # 软删除

    # 关系
    word = relationship("Word", back_populates="review_logs")


class PhonicsRule(Base):
    """自然拼读规则库（phonics）：字母组合 → 发音规则 → 示例词

    由家长在单词库「自然拼读」管理中 AI 批量生成或手动维护。
    """
    __tablename__ = "phonics_rule"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pattern = Column(String(100), nullable=False, index=True)  # 字母组合，如 "ee" / "th" / "a_e"
    sound = Column(String(50), nullable=True)  # 发音（音标），如 /iː/ /θ/ /eɪ/
    rule_text = Column(Text, nullable=True)  # 规则说明（孩子能懂的语言）
    example_words = Column(Text, nullable=True)  # 示例词 JSON：[{"en":"bee","cn":"蜜蜂"}, ...]
    grade = Column(Integer, nullable=True)  # 建议年级 1-6
    category = Column(String(50), default="vowel")  # vowel=元音组合 consonant=辅音组合 silent_e=不发音e
    source = Column(String(20), default="ai")  # ai/manual
    deleted = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)


class PhonicsAttempt(Base):
    """自然拼读错题（按小孩隔离）：练习答错的 组合/示例词，进入错题池优先复习

    答对一次即从错题池移除（删除该行）；同一 word 只保留一行（重复答错覆盖时间）。
    """
    __tablename__ = "phonics_attempt"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False, index=True)  # 小孩 id（拼读练习必须登录小孩）
    rule_id = Column(Integer, nullable=True)  # 所属拼读规则 id（规则删除后保留历史）
    word = Column(String(200), nullable=False, index=True)  # 答错的示例词
    pattern = Column(String(100), nullable=True)  # 关联字母组合（快照，规则删除也可用）
    category = Column(String(50), nullable=True)  # 组合类别快照（vowel/consonant/silent_e）
    wrong_count = Column(Integer, default=1)  # 累计答错次数
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)


class WordReview(Base):
    """复习场次表"""
    __tablename__ = "word_review"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=True, index=True)  # 复习小孩（NULL=旧数据，迁移后归属演示小孩）
    total_count = Column(Integer, default=0)  # 总单词数
    correct_count = Column(Integer, default=0)  # 正确数
    error_count = Column(Integer, default=0)  # 错误数
    duration = Column(Integer, default=0)  # 用时（秒）
    reviewed_at = Column(DateTime, default=datetime.now, nullable=False)


class WordProgress(Base):
    """单词复习进度（按小孩隔离）——单词库本身共享，复习情况/正确率每小孩一份

    四维掌握标准：认得(recognize)/听得(listen)/说得(speak)/写得(write)，
    每维独立计数；一个词「记住」= 四维均达标，薄弱维度由今日任务按缺口补练。
    """
    __tablename__ = "word_progress"

    id = Column(Integer, primary_key=True, autoincrement=True)
    word_id = Column(Integer, ForeignKey("word.id"), nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    review_count = Column(Integer, default=0)  # 复习次数（总）
    correct_count = Column(Integer, default=0)  # 正确次数（总）

    # 四维计数（按维度独立统计，练习提交时按题型归类更新）
    recognize_count = Column(Integer, default=0)   # 认得：英→中
    recognize_correct = Column(Integer, default=0)
    listen_count = Column(Integer, default=0)      # 听得：听音选中文
    listen_correct = Column(Integer, default=0)
    speak_count = Column(Integer, default=0)       # 说得：中→英
    speak_correct = Column(Integer, default=0)
    write_count = Column(Integer, default=0)       # 写得：听写/拼写
    write_correct = Column(Integer, default=0)

    last_reviewed_at = Column(DateTime, nullable=True)  # 上次复习时间
    next_review_at = Column(DateTime, nullable=True)  # 下次复习时间

    # 「看过」标记：在今日任务的学词卡阶段翻到过该词（未答题也算）
    # 语义：seen = 孩子已经学/看过，不再出现在新词池；
    #       不参与正确率与记忆曲线计算（那些只由答题提交更新）。
    seen_at = Column(DateTime, nullable=True)

    # 记忆曲线参数（艾宾浩斯）
    ease_factor = Column(Integer, default=250)  # 难度因子（单位：分钟）
    interval = Column(Integer, default=1)  # 当前间隔天数
    learning_phase = Column(String(20), default="新学")  # 新学/在途/遗忘点/牢记

    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)

    __table_args__ = (
        # 每小孩每词只有一条进度
        __import__("sqlalchemy").UniqueConstraint("word_id", "user_id", name="uq_word_progress_word_user"),
    )


class WordAttempt(Base):
    """单词记忆错词池（按小孩隔离）：四维练习任一答错的词

    答对一次即从错词池移除（掌握即出池）；同一 word+dimension 只保留一行（重复答错累计次数）。
    与 phonics_attempt（拼读错词）一起构成「记忆错题」，统一进错题栏目。
    """
    __tablename__ = "word_attempt"

    id = Column(Integer, primary_key=True, autoincrement=True)
    word_id = Column(Integer, nullable=False, index=True)
    user_id = Column(Integer, nullable=False, index=True)
    dimension = Column(String(20), nullable=False)  # recognize/listen/speak/write
    source = Column(String(20), default="review")  # review=单词复习 memory=联想记忆 phonics=拼读
    english = Column(String(200), nullable=False)  # 快照
    chinese = Column(Text, nullable=True)  # 快照
    phonetic = Column(String(100), nullable=True)  # 快照
    wrong_count = Column(Integer, default=1)  # 累计答错次数
    created_at = Column(DateTime, default=datetime.now, nullable=False)
    updated_at = Column(DateTime, default=datetime.now, onupdate=datetime.now, nullable=False)
