# -*- coding: utf-8 -*-
"""小学英语课标语法骨架：板块 + 语法点清单（内置，免调 LLM）。

语法专项管理页首次打开前由 main.py 播种（空表才播种，幂等）；
家长可在管理界面增删语法点、AI 重新生成骨架或逐点生成教程。
"""
from app.models.subject import Subject
from app.models.grammar import GrammarLesson

# (板块, 语法点标题, 适用年级[可空=通用])
PRIMARY_GRAMMAR_SKELETON = [
    # ---- 词法·名词 ----
    ("词法·名词", "名词的分类（可数与不可数）", 3),
    ("词法·名词", "名词复数规则（s/es/特殊变化）", 3),
    ("词法·名词", "名词所有格（'s 与 of）", 4),
    # ---- 词法·代词 ----
    ("词法·代词", "人称代词（主格与宾格）", 3),
    ("词法·代词", "物主代词（my/your/his/her 与 mine/yours）", 4),
    ("词法·代词", "指示代词（this/that/these/those）", 3),
    ("词法·代词", "疑问代词（what/who/whose/which）", 4),
    # ---- 词法·动词 ----
    ("词法·动词", "be 动词（am/is/are）的用法", 3),
    ("词法·动词", "一般现在时与动词三单", 4),
    ("词法·动词", "现在进行时（be + doing）", 4),
    ("词法·动词", "一般过去时（规则与不规则过去式）", 5),
    ("词法·动词", "一般将来时（will 与 be going to）", 5),
    ("词法·动词", "情态动词 can", 3),
    # ---- 词法·形副 ----
    ("词法·形副", "形容词的用法", 3),
    ("词法·形副", "副词的用法（修饰动词）", 4),
    ("词法·形副", "形容词比较级（er / more）", 5),
    ("词法·形副", "形容词最高级（est / most）", 6),
    # ---- 词法·其他 ----
    ("词法·其他", "冠词（a/an/the）", 3),
    ("词法·其他", "介词（时间 in/on/at 与地点 in/on/under）", 4),
    ("词法·其他", "连词（and/but/or）", 3),
    ("词法·其他", "数词（基数词与序数词）", 3),
    # ---- 句法 ----
    ("句法", "句子成分（主语/谓语/宾语）", 4),
    ("句法", "英语五大基本句型", 5),
    ("句法", "一般疑问句（Do/Does/Is... 与回答）", 3),
    ("句法", "特殊疑问句（what/where/when/who/how）", 4),
    ("句法", "祈使句", 3),
    ("句法", "there be 句型", 4),
    ("句法", "感叹句入门（What / How）", 6),
    ("句法", "并列句入门（and/but/or 连接）", 6),
]


def ensure_grammar_skeleton(db) -> int:
    """空表时播种内置骨架；返回新建条数（幂等，已存在则跳过）。"""
    if db.query(GrammarLesson).filter(GrammarLesson.source == "skeleton").count() > 0:
        return 0
    subject = db.query(Subject).filter(Subject.name == "英语").first()
    if subject is None:
        subject = Subject(name="英语")
        db.add(subject)
        db.commit()
        db.refresh(subject)
    created = 0
    for idx, (category, title, grade) in enumerate(PRIMARY_GRAMMAR_SKELETON):
        exists = db.query(GrammarLesson).filter(
            GrammarLesson.category == category,
            GrammarLesson.title == title,
            GrammarLesson.deleted == False,  # noqa: E712
        ).first()
        if exists:
            continue
        db.add(GrammarLesson(
            subject_id=subject.id,
            grade=grade,
            category=category,
            title=title,
            summary="",  # 待 AI 生成教程时填充
            content_md="",
            examples="[]",
            common_mistakes="[]",
            mnemonic="",
            order_index=idx,
            source="skeleton",
        ))
        created += 1
    if created:
        db.commit()
        print(f"[grammar] 语法骨架播种完成: {created} 条")
    return created
