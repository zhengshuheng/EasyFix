from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

from sqlalchemy.orm import Session
from sqlalchemy import text

from app.database import engine, Base, SessionLocal, get_db
from app.routers import question_router, upload_router, stats_router, similar_router, config_router, error_book_router, subject_router, tag_router, knowledge_point_router, practice_set_router, word_router, word_memory_router, learning_report_router, motivation_router, error_type_router, reading_router, auth_router, users_router, k12_router, textbook_router, grammar_router, phonics_router, zh_router, assessment_router
from app.config import get_settings
from app.models.user import User
from app.models.account import Account
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
from app.trial import router as trial_router, is_trial_key, ensure_template_db, migrate_legacy_registry, ensure_tenant_engine
from app.account_api import router as account_router
from app.subscription_api import router as subscription_router
from app.config_api import router as config_api_router, seed_app_config
from app.routers.ops_data_router import router as ops_data_router
from app.routers.ops_provider_router import router as ops_provider_router
from app.routers.ops_incentive_router import router as ops_incentive_router
from app.routers.ops_grammar_router import router as ops_grammar_router
from app.routers.ops_trial_accounts_router import router as ops_trial_accounts_router
from app.routers.sync_router import router as sync_router
from app.database import set_current_tenant, current_tenant

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
# 专项评测：专项 key（None=综合评测；历史曲线/报告按专项归类）
_ensure_column("assessment_record", "specialty", "specialty VARCHAR(50)")
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
# 全局账号：角色（家长/机构）+ 小孩昵称（家长建空间预填）
_ensure_column("accounts", "role", "role VARCHAR(10) DEFAULT 'parent'")
_ensure_column("accounts", "child_name", "child_name VARCHAR(50) DEFAULT ''")
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
                # UPDATE OR IGNORE：目标小孩已有同 key 数据时保留小孩的，跳过冲突行（幂等，不再每次启动报错）
                conn.execute(text(f"UPDATE OR IGNORE {tbl} SET user_id = :kid WHERE user_id = 1"), {"kid": first_kid_id})
            print(f"[migrate] 激励数据已归属第一个小孩 id={first_kid_id}")
    except Exception as e:
        print(f"[migrate] 跳过激励数据归属迁移: {e}")

# ============================================================
# 迁移必须最先执行：任何业务初始化（init_preset_data 等）都会读取模型上的新列，
# 若旧库缺列会直接 OperationalError（no such column）导致进程启动崩溃。
# 历史事故：init_preset_data 查 star_action.ops_override，而 ensure_ops_override_columns
# 在其之后调用 → 线上容器无限重启、8012 端口从未绑定、公网无法访问。
# ============================================================
from app.db_migrate import ensure_ops_override_columns, ensure_word_seen_column, ensure_account_space_key_column, ensure_assessment_specialty_column, ensure_tenant_schema
# 空间库 schema 整体补齐（治本）：create_all 补缺失表 + 按主库清单补列。
# 必须最先执行——旧模板/旧空间库缺 word_progress 四维列等会导致空间端
# 复习提交/需加强/今日任务 500（2026-09-28 云端"需加强没数据"根因）。
ensure_tenant_schema()
ensure_ops_override_columns()
# word_progress.seen_at（"看过"标记）：必须覆盖空间库，否则空间端 daily-task 500
ensure_word_seen_column()
# accounts.space_key（辅助家长账号绑定空间）：主库 + 模板库补列，官网登录依赖
ensure_account_space_key_column()
# assessment_record.specialty（专项评测 key）：必须覆盖空间库，否则专项评测/练习 500
ensure_assessment_specialty_column()

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
    # 旧试用注册表迁移（tenants 含密码 → spaces + accounts，幂等）
    migrate_legacy_registry(db)
    # 存量辅助家长补官网账号（旧版「添加家长」只写空间库；幂等，官网登录依赖）
    from app.db_migrate import sync_helper_accounts_to_main
    sync_helper_accounts_to_main(db)
    # 运营配置默认值播种（幂等）
    seed_app_config(db)

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


# ===== 试用空间租户中间件：X-Trial-Key → 租户上下文（get_db 按此分发）=====
@app.middleware("http")
async def trial_tenant_middleware(request, call_next):
    key = request.headers.get("x-trial-key")
    if not key:
        return await call_next(request)
    # 无效/已删除空间 key：拒绝访问，避免静默回退正式库（数据泄漏隐患）
    if not is_trial_key(key):
        from fastapi.responses import JSONResponse
        return JSONResponse(
            status_code=403,
            content={"detail": "体验空间不存在或已失效，请重新进入"},
        )
    # 服务重启后进程内引擎为空：从 registry 懒注册，防止静默回退正式库
    ensure_tenant_engine(key)
    token_ctx = set_current_tenant(key)
    try:
        return await call_next(request)
    finally:
        current_tenant.reset(token_ctx)


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
app.include_router(account_router)
app.include_router(subscription_router)
app.include_router(config_api_router)
app.include_router(trial_router)
app.include_router(ops_data_router)
app.include_router(ops_provider_router)
app.include_router(ops_incentive_router)
app.include_router(ops_grammar_router)
app.include_router(ops_trial_accounts_router)
app.include_router(sync_router)

# 确保试用模板库存在（首次启动生成一次 ~10s，之后秒开；注册租户=复制模板，秒级）
# 注意：schema 迁移已在文件上方、业务初始化之前执行（见 ensure_ops_override_columns 处注释）
ensure_template_db()


# 官网静态页（宣传 + 注册入口）：StaticFiles(html=True) 让 /site 直接返回 index.html
# 注意：/ 根路由必须在最前面定义（下方 SITE block 的 site_root），旧 root 已删除——
# 根路径现在由 site_root 处理（官网主页），正式版 SPA 应用入口迁移到 /app。
SITE_DIR = os.path.abspath(
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "frontend", "site")
)
if os.path.isdir(SITE_DIR):
    app.mount("/site", StaticFiles(directory=SITE_DIR, html=True), name="site")

    @app.get("/site")
    @app.get("/")
    def site_root():
        """官网主页（/ 与 /site 均可直达；Mount 不匹配无尾斜杠的路径，需显式路由，否则被 SPA fallback 吞掉）"""
        return FileResponse(os.path.join(SITE_DIR, "index.html"))


# 运营后台 Vue 构建产物（frontend/dist-ops，/ops 直达；必须注册在 trial 通配路由之前）
OPS_DIST = os.path.abspath(
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "frontend", "dist-ops")
)
if os.path.isdir(OPS_DIST):
    app.mount("/ops", StaticFiles(directory=OPS_DIST, html=True), name="ops")


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
        return {"success": True, "token": create_token(admin, persistent=True), "role": admin.role}
    # 用 400 而非 401：401 会被前端 http.js 全局拦截清登录态踢回登录页，
    # 而这里只是"密码不对"的业务校验失败，应留在当前页提示
    raise HTTPException(status_code=400, detail="家长密码错误")


# ===== 前端静态资源（frontend/dist 构建产物，与 API 同源）=====
FRONTEND_DIST = os.path.abspath(
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "frontend", "dist")
)
# 试用版前端构建产物（base='./' + hash 路由，部署在 /{trial_key}/ 下）
TRIAL_FRONTEND_DIST = os.path.abspath(
    os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "frontend", "dist-trial")
)
# 官网静态页目录（StaticFiles 挂载在 app 创建处，见 /site mount）

# ===== 正式版 SPA 静态资源 mount：必须在 /{trial_key}/{full_path:path} 通配路由之前注册，=====
# 否则 /assets/xxx.js 会被 trial_spa 抢先匹配（trial_key="assets"）→ fallback index.html → MIME text/html 白屏
if os.path.isdir(FRONTEND_DIST):
    _assets_dir = os.path.join(FRONTEND_DIST, "assets")
    if os.path.isdir(_assets_dir):
        app.mount("/assets", StaticFiles(directory=_assets_dir), name="assets")
    _icons_dir = os.path.join(FRONTEND_DIST, "icons")
    if os.path.isdir(_icons_dir):
        app.mount("/icons", StaticFiles(directory=_icons_dir), name="icons")

# ===== 正式版 SPA（/app）已移除（2026-09-24 架构统一）=====
# 架构统一后所有用户入口 = 官网 /（site）+ /{key}/ 空间 SPA，/app 无存在意义；
# 无老用户包袱，直接移除不重定向。dist 构建产物与 /assets /icons mount 暂保留（无害，
# 阶段 D 前端合并时统一清理）。


def _trial_index() -> str:
    """试用 SPA 的 index.html（未构建时返回 None）"""
    idx = os.path.join(TRIAL_FRONTEND_DIST, "index.html")
    if os.path.isdir(TRIAL_FRONTEND_DIST) and os.path.isfile(idx):
        return idx
    return None


# ===== 试用空间：/{trial_key}/ 直达独立 db 的 SPA（hash 路由）=====
if _trial_index():

    @app.get("/{trial_key}/assets/{full_path:path}")
    def trial_assets(trial_key: str, full_path: str):
        if not is_trial_key(trial_key):
            raise HTTPException(status_code=404, detail="Not Found")
        candidate = os.path.join(TRIAL_FRONTEND_DIST, "assets", full_path.replace("/", os.sep))
        if full_path and os.path.isfile(candidate):
            return FileResponse(candidate)
        raise HTTPException(status_code=404, detail="Not Found")

    @app.get("/{trial_key}/icons/{full_path:path}")
    def trial_icons(trial_key: str, full_path: str):
        if not is_trial_key(trial_key):
            raise HTTPException(status_code=404, detail="Not Found")
        candidate = os.path.join(TRIAL_FRONTEND_DIST, "icons", full_path.replace("/", os.sep))
        if full_path and os.path.isfile(candidate):
            return FileResponse(candidate)
        raise HTTPException(status_code=404, detail="Not Found")

    @app.get("/{trial_key}")
    @app.get("/{trial_key}/")
    @app.get("/{trial_key}/{full_path:path}")
    def trial_spa(request: Request, trial_key: str, full_path: str = ""):
        """空间入口：/xxx/ 及其子路径（hash 路由，SPA 内部不请求服务器）"""
        if is_trial_key(trial_key):
            if full_path.startswith(("api/", "uploads/")) or full_path in ("api", "uploads"):
                raise HTTPException(status_code=404, detail="Not Found")
            # 无尾斜杠（/easyfix_demo）：301 补斜杠——dist-trial 用相对路径 base='./'，
            # 缺尾斜杠时浏览器把 ./assets 解析成根路径 /assets → 混入正式版 dist JS 白屏
            if not request.url.path.endswith("/"):
                qs = request.url.query
                target = request.url.path + "/" + (("?" + qs) if qs else "")
                return RedirectResponse(target, status_code=301)
            return FileResponse(_trial_index())
        # 非空间 key（/app 与正式 SPA 已退役）：一律 404，回官网用 /
        raise HTTPException(status_code=404, detail="Not Found")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=True,
    )
