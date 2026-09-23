from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import engine, Base, SessionLocal, get_db
from app.routers import question_router, upload_router, stats_router, similar_router, config_router, error_book_router, subject_router, tag_router, knowledge_point_router, practice_set_router, word_router, word_memory_router, learning_report_router, motivation_router, error_type_router, reading_router, auth_router, users_router, k12_router, textbook_router, grammar_router, phonics_router, zh_router, assessment_router
from app.config import get_settings
from app.models.user import User
from app.utils.auth import (
    DEFAULT_ADMIN_USERNAME,
    DEFAULT_ADMIN_PASSWORD,
    verify_password as check_password,
    hash_password,
    create_token,
    require_admin,
)
from app.services.init_motivation_data import init_preset_data, init_achievement_progress, init_star_records_from_existing_data, init_achievement_configs
from app.services.init_base_data import init_base_data
from app.services.init_demo_data import init_demo_data
from app.services.grammar_skeleton import ensure_grammar_skeleton

settings = get_settings()

# 创建数据库表
Base.metadata.create_all(bind=engine)

# 轻量迁移：为旧库补充新增列（SQLite 支持 ALTER TABLE ADD COLUMN）
def _ensure_column(table: str, column: str, ddl: str):
    try:
        from sqlalchemy import inspect as sa_inspect, text
        insp = sa_inspect(engine)
        cols = [c["name"] for c in insp.get_columns(table)]
        if column not in cols:
            with engine.begin() as conn:
                conn.execute(text(f"ALTER TABLE {table} ADD COLUMN {ddl}"))
            print(f"[migrate] {table} 增加列 {column}")
    except Exception as e:
        print(f"[migrate] 跳过 {table}.{column}: {e}")


def _backfill_user_enrollment_date():
    """一次性迁移：旧库只有 current_grade（手工年级），反推为 enrollment_date 保留用户意图；
    已有 enrollment_date 或非 child 用户不动。"""
    try:
        from sqlalchemy import text
        from datetime import date
        from app.utils.timeutil import enrollment_date_from_grade
        with engine.connect() as conn:
            rows = conn.execute(text(
                "SELECT id, current_grade, enrollment_date FROM users WHERE role='child'"
            )).fetchall()
        changed = 0
        today = date.today()
        for uid, grade, enr in rows:
            if enr is None and grade is not None:
                enr_date = enrollment_date_from_grade(grade, today)
                with engine.begin() as conn:
                    conn.execute(
                        text("UPDATE users SET enrollment_date = :d WHERE id = :id"),
                        {"d": enr_date.isoformat(), "id": uid},
                    )
                changed += 1
        if changed:
            print(f"[migrate] 已按当前年级反推 {changed} 个小孩的入学日期")
    except Exception as e:
        print(f"[migrate] 反推入学日期跳过: {e}")


_ensure_column("practice_set_question", "student_answer", "student_answer TEXT")
_ensure_column("error_book", "user_id", "user_id INTEGER")
_ensure_column("learning_report", "user_id", "user_id INTEGER")
# 能力评测集管理：评测集题目快照（start 时写入，供历史/重测/恢复）
_ensure_column("assessment_record", "questions", "questions TEXT")
# 错题/练习分表 + 按小孩隔离（新表由 create_all 建，这里补结构变更列）
_ensure_column("practice_set", "user_id", "user_id INTEGER")
_ensure_column("practice_set_question", "practice_question_id", "practice_question_id INTEGER")
_ensure_column("word_review_session", "user_id", "user_id INTEGER")
# 卷面分值：是否显示分数 / 计分方式（hundred=百分制100分，default=题型默认分值）
# 旧库默认 'default'，与已生成的老 PDF 分值口径保持一致
_ensure_column("practice_set", "show_score", "show_score BOOLEAN DEFAULT 1")
_ensure_column("practice_set", "score_mode", "score_mode VARCHAR(20) DEFAULT 'default'")
# 卷面「出题人」是否署名「AI 出题助手」（默认 0 = 留空白手填）
_ensure_column("practice_set", "show_ai_author", "show_ai_author BOOLEAN DEFAULT 0")
# 单词单元归属（文本整表导入时识别 Unit N，unit=单元号，unit_title=单元英文标题）
_ensure_column("word", "unit", "unit INTEGER")
_ensure_column("word", "unit_title", "unit_title VARCHAR(200)")
# 单词记忆增强（新增/导入单词时后台自动生成）
_ensure_column("word", "phonetic_rule", "phonetic_rule TEXT")
_ensure_column("word", "mnemonic", "mnemonic TEXT")
_ensure_column("word", "word_root", "word_root VARCHAR(500)")
_ensure_column("word", "related_words", "related_words TEXT")
# 语境例句（单词融入句子学习）：JSON 数组 [{"en":"...","zh":"..."}]
_ensure_column("word", "example_sentences", "example_sentences TEXT")
# 四维记忆模型：word_progress 分维度计数（认得/听得/说得/写得）
_ensure_column("word_progress", "recognize_count", "recognize_count INTEGER DEFAULT 0")
_ensure_column("word_progress", "recognize_correct", "recognize_correct INTEGER DEFAULT 0")
_ensure_column("word_progress", "listen_count", "listen_count INTEGER DEFAULT 0")
_ensure_column("word_progress", "listen_correct", "listen_correct INTEGER DEFAULT 0")
_ensure_column("word_progress", "speak_count", "speak_count INTEGER DEFAULT 0")
_ensure_column("word_progress", "speak_correct", "speak_correct INTEGER DEFAULT 0")
_ensure_column("word_progress", "write_count", "write_count INTEGER DEFAULT 0")
_ensure_column("word_progress", "write_correct", "write_correct INTEGER DEFAULT 0")
# 小孩当前年级（默认年级按小孩）
_ensure_column("users", "current_grade", "current_grade INTEGER DEFAULT 1")
# 入学日期（据此推断年级，替代手工配置年级）
_ensure_column("users", "enrollment_date", "enrollment_date DATE")
_backfill_user_enrollment_date()
# 语法专项练习卷：关联语法点
_ensure_column("practice_set", "grammar_lesson_id", "grammar_lesson_id INTEGER")
# AI 出题配图场景（结构化 JSON：count/group/shape）
_ensure_column("practice_question", "visual", "visual TEXT")
# AI 出题维度：题型（choice/fill/judge/calc/...）/ 类型（basic/scene/comprehensive/thinking）
_ensure_column("question", "question_type", "question_type VARCHAR(50)")
_ensure_column("question", "question_category", "question_category VARCHAR(50)")
# 选择题独立选项（AI 出题的选择题不再把选项塞进题干）
_ensure_column("question", "option_a", "option_a TEXT")
_ensure_column("question", "option_b", "option_b TEXT")
_ensure_column("question", "option_c", "option_c TEXT")
_ensure_column("question", "option_d", "option_d TEXT")
# 题目来源：'ai'=AI 出题生成的练习题（不属于错题，不出现在错题列表）
_ensure_column("question", "source", "source VARCHAR(20)")
# 注：question 表已废弃（错题 → error_question，练习题目 → practice_question），无需 AI 题目来源回填
# 旧无主错题本自动归属第一个小孩（幂等：仅当该小孩不存在错题本归属时才执行）
with engine.begin() as conn:
    try:
        conn.execute(
            text(
                "UPDATE error_book SET user_id = "
                "(SELECT id FROM users WHERE role='child' ORDER BY id LIMIT 1) "
                "WHERE user_id IS NULL"
            )
        )
    except Exception as e:
        print(f"[migrate] 跳过 error_book 旧数据归属: {e}")

# ===== 单词复习按小孩隔离迁移 =====
_ensure_column("word_review_log", "user_id", "user_id INTEGER")
_ensure_column("word_review", "user_id", "user_id INTEGER")
with engine.begin() as conn:
    # 旧复习日志/场次归属第一个小孩（演示小孩）；仅处理 NULL 记录，幂等
    try:
        conn.execute(
            text(
                "UPDATE word_review_log SET user_id = "
                "(SELECT id FROM users WHERE role='child' ORDER BY id LIMIT 1) "
                "WHERE user_id IS NULL"
            )
        )
        conn.execute(
            text(
                "UPDATE word_review SET user_id = "
                "(SELECT id FROM users WHERE role='child' ORDER BY id LIMIT 1) "
                "WHERE user_id IS NULL"
            )
        )
        # 旧 Word 表复习数据迁入 WordProgress（仅当该词该小孩尚无进度时，幂等）
        conn.execute(
            text(
                "INSERT OR IGNORE INTO word_progress "
                "(word_id, user_id, review_count, correct_count, last_reviewed_at, next_review_at, "
                " ease_factor, interval, learning_phase, updated_at) "
                "SELECT w.id, (SELECT id FROM users WHERE role='child' ORDER BY id LIMIT 1), "
                " w.review_count, w.correct_count, w.last_reviewed_at, w.next_review_at, "
                " w.ease_factor, w.interval, w.learning_phase, COALESCE(w.updated_at, CURRENT_TIMESTAMP) "
                "FROM word w "
                "WHERE w.review_count > 0"
            )
        )
    except Exception as e:
        print(f"[migrate] 跳过单词复习按小孩迁移: {e}")

# ===== 激励数据按小孩迁移 =====
# 旧激励数据（积分余额/明细/成就进度/兑换记录）挂在家长账号 user_id=1 上，
# 归给第一个小孩（幂等：执行一次后 user_id=1 无记录，再跑无效果）
with engine.begin() as conn:
    try:
        first_kid_id = conn.execute(
            text("SELECT id FROM users WHERE role='child' AND enabled=1 ORDER BY id LIMIT 1")
        ).scalar()
        if first_kid_id and first_kid_id != 1:
            for tbl in ("star_balance", "star_record", "achievement_progress", "redemption"):
                conn.execute(text(f"UPDATE {tbl} SET user_id = :kid WHERE user_id = 1"), {"kid": first_kid_id})
            print(f"[migrate] 激励数据已归属第一个小孩 id={first_kid_id}")
    except Exception as e:
        print(f"[migrate] 跳过激励数据归属迁移: {e}")

# 初始化基础数据（学科/标签/错误类型）+ 默认家长账号 + 演示数据 + 激励系统预设数据
with SessionLocal() as db:
    init_base_data(db)

    # 无家长账号时先创建默认家长（确保 admin 为 id=1，兼容旧版激励统计 DEFAULT_USER_ID=1）
    if not db.query(User).filter_by(role="admin").first():
        db.add(User(
            username=DEFAULT_ADMIN_USERNAME,
            display_name="家长",
            role="admin",
            password_hash=hash_password(DEFAULT_ADMIN_PASSWORD),
        ))
        db.commit()

    # 演示数据初始化已停用：旧演示数据基于 question/practice_set 旧模型，
    # 已随「错题派生 + 按小孩隔离」重构清空（见 tools/migrate_kid_refactor.py）。
    # 待按新架构重建演示数据后再恢复；当前数据由真实使用流程产生。
    # init_demo_data(db)
    init_preset_data(db)
    init_achievement_progress(db)
    init_star_records_from_existing_data(db)
    init_achievement_configs(db)
    # 英语语法专项骨架（空表才播种，幂等；家长可在管理界面增删/重新生成）
    ensure_grammar_skeleton(db)

app = FastAPI(
    title="EasyFix API",
    description="错题整理系统后端API",
    version="1.0.0",
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境应限制
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件服务（上传的图片）
uploads_path = os.path.abspath(settings.UPLOAD_DIR)
os.makedirs(uploads_path, exist_ok=True)
app.mount("/uploads", StaticFiles(directory=uploads_path), name="uploads")

# 注册路由
app.include_router(question_router)
app.include_router(upload_router)
app.include_router(stats_router)
app.include_router(similar_router)
# 配置管理接口：仅家长（admin）可访问；宽松模式下未登录仍兼容旧前端
app.include_router(config_router, dependencies=[Depends(require_admin)])
app.include_router(error_book_router)
app.include_router(subject_router)
app.include_router(tag_router)
app.include_router(knowledge_point_router)
app.include_router(error_type_router)
app.include_router(practice_set_router)
app.include_router(word_memory_router)  # /words/memory-review 静态路径必须先于 word_router 的 /{word_id}
app.include_router(word_router)
app.include_router(learning_report_router)
app.include_router(motivation_router)
app.include_router(reading_router)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(k12_router)
app.include_router(textbook_router)
app.include_router(grammar_router)
app.include_router(phonics_router)
app.include_router(zh_router)
app.include_router(assessment_router)


@app.get("/")
def root():
    # 前端构建产物存在时，根路径直接返回前端页面
    index_file = os.path.join(FRONTEND_DIST, "index.html")
    if os.path.isdir(FRONTEND_DIST) and os.path.isfile(index_file):
        return FileResponse(index_file)
    return {"message": "EasyFix API", "version": "1.0.0"}


@app.get("/health")
def health_check():
    return {"status": "ok"}


class PasswordVerifyRequest(BaseModel):
    password: str


@app.post("/api/auth/verify-password")
def verify_password(data: PasswordVerifyRequest, db: Session = Depends(get_db)):
    """验证访问密码（旧前端兼容）：校验默认家长账号密码"""
    admin = db.query(User).filter_by(username=DEFAULT_ADMIN_USERNAME).first()
    if admin and check_password(data.password, admin.password_hash):
        return {"success": True, "token": create_token(admin), "role": admin.role}
    raise HTTPException(status_code=401, detail="密码错误")


# ===== 前端静态资源（frontend/dist 构建产物，与 API 同源）=====
FRONTEND_DIST = os.path.abspath(
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "frontend", "dist")
)

if os.path.isdir(FRONTEND_DIST):
    assets_dir = os.path.join(FRONTEND_DIST, "assets")
    icons_dir = os.path.join(FRONTEND_DIST, "icons")
    if os.path.isdir(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
    if os.path.isdir(icons_dir):
        app.mount("/icons", StaticFiles(directory=icons_dir), name="icons")

    @app.get("/{full_path:path}")
    def spa_fallback(full_path: str):
        """SPA 前端入口：非 API 路径回退到 index.html（支持 history 路由）"""
        if full_path.startswith(("api/", "uploads/")) or full_path in ("api", "uploads"):
            raise HTTPException(status_code=404, detail="Not Found")
        candidate = os.path.join(FRONTEND_DIST, full_path.replace("/", os.sep))
        if full_path and os.path.isfile(candidate):
            return FileResponse(candidate)
        return FileResponse(os.path.join(FRONTEND_DIST, "index.html"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
    )
