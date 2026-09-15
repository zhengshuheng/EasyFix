"""内置演示数据：演示小孩账号 + 小学1-6年级学习数据

仅当演示账号不存在时创建整套数据（幂等）：
- 演示小孩：username=demo / PIN=1234
- 错题本 + 错题（数学1-6年级 + 英语1-6年级，带复习历史）
- 练习集（含批改记录）
- 单词（1-6年级，word 表为空时插入）与复习记录
- 激励星星记录与余额

注意：当前系统数据为本地共享（错题/单词无 user_id 字段），演示数据用于展示各功能如何运作。
"""
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from app.models.user import User
from app.models.subject import Subject
from app.models.error_book import ErrorBook
from app.models.question import Question
from app.models.error_type import ErrorType
from app.models.tag import Tag
from app.models.practice_set import PracticeSet, PracticeSetQuestion
from app.models.word import Word, WordReviewLog, WordReview
from app.models.star import StarRecord, StarBalance
from app.utils.auth import hash_password

DEMO_USERNAME = "demo"
DEMO_PIN = "1234"

# 数学错题：1-6 年级每年级 2 道（题干, 知识点, 错误类型, 难度, 解析, 答案）
MATH_QUESTIONS = [
    # 一年级
    ("计算 9 - 3 + 5 = ?", "20以内加减混合运算", "计算错误", 2, "按从左到右顺序计算：9-3=6，6+5=11。", "11"),
    ("数一数：△△△△ ○○○，一共有几个图形？", "认识图形", "概念错误", 1, "数出三角形4个、圆形3个，4+3=7。", "7"),
    # 二年级
    ("4 × 7 = ?", "表内乘法", "计算错误", 2, "背诵乘法口诀：四七二十八。", "28"),
    ("1 米 = ( ) 厘米", "长度单位", "概念错误", 2, "1米 = 100厘米。", "100"),
    # 三年级
    ("408 ÷ 4 = ?", "三位数除以一位数", "计算错误", 3, "从高位除起：4÷4=1，0÷4=0，8÷4=2，结果是102。", "102"),
    ("3 时 = ( ) 分", "时、分、秒", "概念错误", 2, "1时=60分，3时=180分。", "180"),
    # 四年级
    ("125 × 80 = ?", "三位数乘两位数", "计算错误", 3, "125×8=1000，再乘10：1000×10=10000。", "10000"),
    ("一个角的两条边越长，角就越大，对吗？", "角的认识", "概念错误", 3, "角的大小与边的长短无关，与两边张开的大小有关。", "不对"),
    # 五年级
    ("0.3 × 0.7 = ?", "小数乘法", "计算错误", 3, "先算3×7=21，两个因数各有一位小数，共两位，结果是0.21。", "0.21"),
    ("解方程：x + 5 = 12", "简易方程", "概念错误", 4, "等式两边同时减5：x = 12 - 5 = 7。", "7"),
    # 六年级
    ("3/4 ÷ 2 = ?", "分数除法", "计算错误", 4, "除以一个数等于乘它的倒数：3/4 × 1/2 = 3/8。", "3/8"),
    ("一件商品打八折后是80元，原价是多少？", "百分数应用题", "完全不会", 5, "八折=80%，原价×80%=80，原价=80÷0.8=100元。", "100"),
]

# 英语错题：1-6 年级每年级 1 道（题干, 知识点, 错误类型, 难度, 解析, 答案）
ENGLISH_QUESTIONS = [
    ("拼写单词：苹果 a _ _ l e", "字母与单词拼写", "背诵拼写", 2, "苹果的英文是 apple，注意双写 p。", "apple"),
    ("选词填空：I have two (book / books).", "名词复数", "语法", 2, "two 后面用复数，book 的复数是 books。", "books"),
    ("用 be 动词填空：She ___ a teacher.", "一般现在时（be动词）", "语法", 3, "主语 she 是第三人称单数，be 动词用 is。", "is"),
    ("写出 go 的过去式", "一般过去时（不规则动词）", "语法", 3, "go 的过去式是不规则的 went。", "went"),
    ("填空：This box is ___ (big) than that one.", "形容词比较级", "语法", 4, "big 是重读闭音节，比较级双写 g 加 er：bigger。", "bigger"),
    ("选词填空：I ___ (has/have) been to the museum.", "现在完成时", "语法", 5, "主语 I 用 have，现在完成时结构 have + 过去分词。", "have"),
]

# 练习集：名称, 学科, 复习次数, 正确率, 最近复习天数前
PRACTICE_SETS = [
    ("六年级数学 · 分数与百分数巩固", "数学", 2, 75, 3),
    ("六年级英语 · 时态与语法强化", "英语", 1, 67, 5),
]

# 单词：1-6 年级各 5 个（word 表为空时才插入）
WORDS_BY_GRADE = {
    1: [("apple", "苹果"), ("banana", "香蕉"), ("cat", "猫"), ("dog", "狗"), ("egg", "鸡蛋")],
    2: [("book", "书"), ("pen", "钢笔"), ("desk", "书桌"), ("chair", "椅子"), ("bag", "书包")],
    3: [("teacher", "老师"), ("student", "学生"), ("school", "学校"), ("class", "班级"), ("friend", "朋友")],
    4: [("family", "家庭"), ("mother", "妈妈"), ("father", "爸爸"), ("brother", "兄弟"), ("sister", "姐妹")],
    5: [("breakfast", "早餐"), ("lunch", "午餐"), ("dinner", "晚餐"), ("vegetable", "蔬菜"), ("fruit", "水果")],
    6: [("museum", "博物馆"), ("library", "图书馆"), ("hospital", "医院"), ("cinema", "电影院"), ("science", "科学")],
}


def _days_ago(days: int) -> datetime:
    return datetime.now() - timedelta(days=days)


def _make_question(db, book: ErrorBook, subject: Subject, data, grade, semester):
    text, kp, error_type_name, difficulty, analysis, answer = data
    et = (
        db.query(ErrorType)
        .filter(ErrorType.subject_id == subject.id, ErrorType.name == error_type_name)
        .first()
    )
    review_count = 1 + (grade % 3)  # 1-3 次
    correct_count = max(0, review_count - 1) if grade % 2 == 0 else review_count
    error_count = review_count - correct_count
    q = Question(
        error_book_id=book.id,
        subject_id=subject.id,
        original_text=text,
        parsed_question=text,
        grade=grade,
        semester=semester,
        answer=answer,
        analysis=analysis,
        difficulty=difficulty,
        error_type=et.name if et else error_type_name,
        knowledge_point=kp,
        review_count=review_count,
        correct_count=correct_count,
        error_count=error_count,
        last_reviewed_at=_days_ago(1 + grade % 4),
        created_at=_days_ago(60 + grade * 5),
    )
    db.add(q)
    db.flush()
    return q


def init_demo_data(db: Session) -> None:
    """创建演示小孩与整套演示学习数据（幂等：demo 账号已存在则跳过）"""
    if db.query(User).filter(User.username == DEMO_USERNAME).first():
        return

    demo = User(
        username=DEMO_USERNAME,
        display_name="演示小孩",
        role="child",
        pin=DEMO_PIN,
        enabled=True,
    )
    db.add(demo)
    db.flush()

    subject_map = {s.name: s for s in db.query(Subject).filter(Subject.deleted == False).all()}
    math = subject_map.get("数学")
    english = subject_map.get("英语")

    # ---- 错题本 + 错题 ----
    math_book = None
    english_book = None
    math_questions = []
    english_questions = []

    if math:
        math_book = ErrorBook(name="小学数学错题本", subject_id=math.id, description="一年级到六年级的数学错题（演示数据）")
        db.add(math_book)
        db.flush()
        for grade in range(1, 7):
            for item in MATH_QUESTIONS[(grade - 1) * 2 : grade * 2]:
                math_questions.append(_make_question(db, math_book, math, item, grade, 1 if grade % 2 else 2))
    if english:
        english_book = ErrorBook(name="小学英语错题本", subject_id=english.id, description="一年级到六年级的英语错题（演示数据）")
        db.add(english_book)
        db.flush()
        for grade, item in enumerate(ENGLISH_QUESTIONS, start=1):
            english_questions.append(_make_question(db, english_book, english, item, grade, 1 if grade % 2 else 2))

    # 六年级英语错题打上 Unit 标签（演示标签用法）
    if english_questions:
        unit_tags = {t.name: t for t in db.query(Tag).filter(Tag.deleted == False, Tag.name.like("六上Unit%")).all()}
        for i, q in enumerate(english_questions[-3:]):
            tag = unit_tags.get(f"六上Unit{i + 1}")
            if tag:
                q.tags.append(tag)

    # ---- 练习集 ----
    for name, subject_name, review_count, accuracy, reviewed_days_ago in PRACTICE_SETS:
        subject = subject_map.get(subject_name)
        pool = math_questions if subject_name == "数学" else english_questions
        if not subject or not pool:
            continue
        ps = PracticeSet(
            name=name,
            subject_id=subject.id,
            source_type="question",
            question_type="original",
            total_questions=len(pool),
            reviewed=True,
            review_count=review_count,
            accuracy=accuracy,
            last_reviewed_at=_days_ago(reviewed_days_ago),
            created_at=_days_ago(20 + reviewed_days_ago * 2),
        )
        db.add(ps)
        db.flush()
        for order, q in enumerate(pool):
            db.add(PracticeSetQuestion(
                practice_set_id=ps.id,
                question_id=q.id,
                is_correct=order % 3 != 0,
                display_order=order,
            ))

    # ---- 单词 + 复习记录（仅 word 表为空时，避免混入真实单词库） ----
    word_count = db.query(Word).filter(Word.deleted == False).count()
    if word_count == 0:
        phases = ["牢记", "在途", "新学"]
        words_by_id = {}
        for grade in range(1, 7):
            for idx, (en, zh) in enumerate(WORDS_BY_GRADE[grade]):
                review_count = 2 + (grade + idx) % 3
                correct_count = review_count if (grade + idx) % 2 else max(0, review_count - 1)
                w = Word(
                    english=en,
                    chinese=zh,
                    phonetic="",
                    grade=grade,
                    semester=1 if grade % 2 else 2,
                    review_count=review_count,
                    correct_count=correct_count,
                    last_reviewed_at=_days_ago(1 + (grade + idx) % 5),
                    next_review_at=_days_ago(-(1 + (grade + idx) % 3)),
                    ease_factor=240,
                    interval=1 + (grade + idx) % 3,
                    learning_phase=phases[(grade + idx) % 3],
                    created_at=_days_ago(90 + grade * 8),
                )
                db.add(w)
                db.flush()
                words_by_id[w.id] = w
                # 每个词 1-2 条复习日志
                for li in range(1 + (grade + idx) % 2):
                    db.add(WordReviewLog(
                        word_id=w.id,
                        is_correct=li == 0 or (grade + idx) % 2 == 0,
                        user_answer=en if li == 0 else (en if (grade + idx) % 2 == 0 else ""),
                        review_type=1 if li == 0 else 2,
                        reviewed_at=_days_ago(2 + (grade + idx) % 5 + li),
                    ))
        # 一场单词复习（演示复习场次）
        db.add(WordReview(
            total_count=12,
            correct_count=9,
            error_count=3,
            duration=180,
            reviewed_at=_days_ago(3),
        ))

    # ---- 激励星星记录 + 余额 ----
    records = [
        ("upload_question", 20, "上传错题（演示）"),
        ("create_practice_set", 5, "创建练习集（演示）"),
        ("review_practice_set", 5, "复习练习集（演示）"),
        ("review_word", 2, "背单词（演示）"),
        ("daily_login", 1, "每日登录（演示）"),
        ("daily_login", 1, "每日登录（演示）"),
        ("review_word", 2, "背单词（演示）"),
        ("review_practice_set", 5, "复习练习集（演示）"),
        ("upload_question", 20, "上传错题（演示）"),
    ]
    balance = 0
    for i, (code, delta, reason) in enumerate(records):
        balance += delta
        db.add(StarRecord(
            user_id=demo.id,
            action_code=code,
            star_delta=delta,
            balance_after=balance,
            reason=reason,
            created_at=_days_ago(20 - i * 2),
        ))
    db.add(StarBalance(user_id=demo.id, balance=balance))

    db.commit()
