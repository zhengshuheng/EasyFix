from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os

from sqlalchemy.orm import Session

from app.database import engine, Base, SessionLocal, get_db
from app.routers import question_router, upload_router, stats_router, similar_router, config_router, error_book_router, subject_router, tag_router, knowledge_point_router, practice_set_router, word_router, learning_report_router, motivation_router, error_type_router, reading_router, auth_router, users_router
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

_ensure_column("practice_set_question", "student_answer", "student_answer TEXT")

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

    # 演示小孩与演示学习数据（demo 账号不存在时创建）
    init_demo_data(db)
    init_preset_data(db)
    init_achievement_progress(db)
    init_star_records_from_existing_data(db)
    init_achievement_configs(db)

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
app.include_router(word_router)
app.include_router(learning_report_router)
app.include_router(motivation_router)
app.include_router(reading_router)
app.include_router(auth_router)
app.include_router(users_router)


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
