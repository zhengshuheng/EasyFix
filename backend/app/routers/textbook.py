import os
import uuid

from fastapi import APIRouter, File, Form, HTTPException, UploadFile
from pydantic import BaseModel
from typing import List, Optional

from app.services import textbook_service, ctsf_import

router = APIRouter(prefix="/api/textbook", tags=["教材同步"])


def _require_online(flag: str):
    """在线导入入口门禁：backend/textbook_import_config.json 中对应开关关闭时拒绝"""
    cfg = textbook_service.get_import_config()
    if not cfg.get(flag, True):
        raise HTTPException(status_code=403,
                            detail="该在线导入入口已关闭（backend/textbook_import_config.json）")


class ImportRequest(BaseModel):
    subject: str
    version: str
    grade: str
    semester: str
    local_pdf: Optional[str] = None  # 手动放置的 PDF 路径（scan_local 返回的 path）


class CtsfImportRequest(BaseModel):
    subject: str
    version: str
    grade: str
    semester: str


@router.get("/catalog")
def catalog():
    """内置教材目录（学段/学科/版本/年级/册次 + 下载源 + 本地状态）"""
    try:
        return textbook_service.get_catalog()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"教材目录不可用：{e}")


@router.post("/import")
def import_book(req: ImportRequest):
    """下载并导入指定教材（或导入本地 PDF），后台执行，返回 task_id"""
    _require_online("enable_online_pdf")
    try:
        book = None
        if not req.local_pdf:
            catalog = textbook_service.get_catalog()
            for b in catalog["books"]:
                if (b["subject"] == req.subject and b["version"] == req.version
                        and b["grade"] == req.grade and b["semester"] == req.semester):
                    book = b
                    break
            if not book:
                raise HTTPException(status_code=404, detail="目录中未找到该教材")
        else:
            if not req.local_pdf.lower().endswith(".pdf"):
                raise HTTPException(status_code=400, detail="本地教材必须是 PDF 文件")
            if not __import__("os").path.exists(req.local_pdf):
                raise HTTPException(status_code=400, detail="本地 PDF 不存在")
            book = {"subject": req.subject, "version": req.version or "手动放置",
                    "grade": req.grade, "semester": req.semester}
        task = textbook_service.start_import(book, local_pdf=req.local_pdf)
        return {"task_id": task["id"], "status": task["status"]}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"启动导入失败：{e}")


@router.get("/task/{task_id}")
def task_status(task_id: str):
    """查询导入任务进度"""
    task = textbook_service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="任务不存在")
    return task


@router.get("/tasks")
def tasks():
    """最近任务列表"""
    return {"tasks": textbook_service.list_tasks()}


@router.get("/scan")
def scan_local(version: str = "", subject: str = ""):
    """扫描本地教材文件夹（手动放置兜底）。

    指定 版本/科目 时只扫该教材目录，未指定则扫全树；
    返回被扫描的目录 dir 与 scoped 标记，方便前端提示放置位置。
    """
    try:
        scoped = bool(version or subject)
        files = textbook_service.scan_local(version=version, subject=subject)
        scan_dir = textbook_service.manual_dir(version, subject) if scoped else textbook_service.DATA_DIR
        return {"files": files, "dir": scan_dir, "scoped": scoped}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"扫描失败：{e}")


@router.get("/open-folder")
def open_folder():
    """打开本地教材文件夹"""
    try:
        path = textbook_service.open_data_folder()
        return {"ok": True, "dir": path}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"打开文件夹失败：{e}")


@router.get("/manual-dir")
def manual_dir(version: str = "", subject: str = "", grade: str = "", semester: str = "",
               open: bool = False):
    """按当前选择返回「手动放置」目标文件夹与目标 PDF 文件名；文件夹不存在时自动创建。
    open=true 时同时在资源管理器中打开该文件夹。
    """
    try:
        return textbook_service.ensure_manual_dir(version, subject, grade, semester,
                                                  open_explorer=bool(open))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"创建教材文件夹失败：{e}")


# ---------------------------------------------------------------- ChinaStudyFree 在线大纲

@router.get("/ctsf/catalog")
def ctsf_catalog():
    """在线知识大纲目录（ChinaStudyFree，MIT）：数学人教版/语文统编/英语PEP/科学教科版 44 本"""
    _require_online("enable_online_ctsf")
    try:
        return ctsf_import.get_catalog()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取在线大纲目录失败：{e}")


@router.post("/ctsf/import")
def ctsf_import_book(req: CtsfImportRequest):
    """从在线知识大纲导入指定教材的知识点（免下载/免OCR），返回 task_id"""
    _require_online("enable_online_ctsf")
    try:
        task = ctsf_import.start_ctsf_import(
            req.subject.strip(), req.version.strip(), req.grade.strip(), req.semester.strip())
        return {"task_id": task["id"], "status": task["status"], "source": "ctsf-online"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"启动导入失败：{e}")


@router.get("/import-config")
def import_config():
    """导入入口配置：enable_online_ctsf / enable_online_pdf / enable_photo（前端据此显隐 tab）"""
    try:
        return textbook_service.get_import_config()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"读取导入配置失败：{e}")


@router.post("/photo-import")
async def photo_import(subject: str = Form(...), grade: str = Form(...), semester: str = Form(...),
                       version: str = Form(""), files: List[UploadFile] = File(...)):
    """拍照教材同步：上传纸质教材照片（可多张）→ OCR → AI 提取知识点 → 入库。

    照片仅存临时目录、任务结束后删除；知识点文本入库后可按 学科/年级/册次 使用。
    """
    cfg = textbook_service.get_import_config()
    if not cfg.get("enable_photo", True):
        raise HTTPException(status_code=403, detail="拍照教材同步已关闭（backend/textbook_import_config.json）")
    if not subject or not grade or not semester:
        raise HTTPException(status_code=400, detail="请选择 学科/年级/册次")
    if not files:
        raise HTTPException(status_code=400, detail="请至少上传一张教材照片")
    task_id = None
    upload_dir = os.path.join(textbook_service.photo_upload_dir(), f"upload_{uuid.uuid4().hex[:8]}")
    saved = []
    try:
        os.makedirs(upload_dir, exist_ok=True)
        for i, f in enumerate(files):
            if not f.filename:
                continue
            ext = os.path.splitext(f.filename)[1].lower()
            if ext not in (".jpg", ".jpeg", ".png", ".webp", ".bmp"):
                raise HTTPException(status_code=400, detail=f"不支持的图片格式：{f.filename}")
            path = os.path.join(upload_dir, f"page_{i + 1}{ext}")
            with open(path, "wb") as out:
                out.write(await f.read())
            saved.append(path)
        if not saved:
            raise HTTPException(status_code=400, detail="没有收到有效图片")
        meta = {"subject": subject.strip(), "grade": grade.strip(), "semester": semester.strip(),
                "version": version.strip()}
        task = textbook_service.start_photo_import(meta, saved)
        task_id = task["id"]
        return {"task_id": task["id"], "status": task["status"], "photos": len(saved), "source": "photo"}
    except HTTPException:
        import shutil
        shutil.rmtree(upload_dir, ignore_errors=True)
        raise
    except Exception as e:
        import shutil
        shutil.rmtree(upload_dir, ignore_errors=True)
        raise HTTPException(status_code=500, detail=f"启动拍照导入失败：{e}")


@router.post("/user-pdf-import")
async def user_pdf_import(subject: str = Form(...), grade: str = Form(...), semester: str = Form(...),
                          version: str = Form(""), file: UploadFile = File(...)):
    """自备教材 PDF 同步：用户上传自己持有的电子教材 PDF → OCR → AI 提取知识点 → 入库。

    不依赖任何在线目录/下载源；上传的 PDF 会保存到用户本地教材库
    （data/textbooks/<版本>/<科目>/<年级><册次>.pdf，连同 OCR 缓存 txt），
    供教材库预览与知识点对照使用，仅限个人学习、不得传播。
    """
    cfg = textbook_service.get_import_config()
    if not cfg.get("enable_user_pdf", True):
        raise HTTPException(status_code=403, detail="自备教材 PDF 同步已关闭（backend/textbook_import_config.json）")
    if not subject or not grade or not semester:
        raise HTTPException(status_code=400, detail="请选择 学科/年级/册次")
    if not file or not file.filename:
        raise HTTPException(status_code=400, detail="请选择要上传的教材 PDF 文件")
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="仅支持 PDF 文件")
    task_id = None
    upload_dir = os.path.join(textbook_service.user_pdf_upload_dir(), f"upload_{uuid.uuid4().hex[:8]}")
    try:
        os.makedirs(upload_dir, exist_ok=True)
        safe_name = "textbook.pdf"
        path = os.path.join(upload_dir, safe_name)
        with open(path, "wb") as out:
            out.write(await file.read())
        meta = {"subject": subject.strip(), "grade": grade.strip(), "semester": semester.strip(),
                "version": version.strip()}
        task = textbook_service.start_user_pdf_import(meta, path)
        task_id = task["id"]
        return {"task_id": task["id"], "status": task["status"], "source": "user_pdf"}
    except HTTPException:
        import shutil
        shutil.rmtree(upload_dir, ignore_errors=True)
        raise
    except Exception as e:
        import shutil
        shutil.rmtree(upload_dir, ignore_errors=True)
        raise HTTPException(status_code=500, detail=f"启动自备 PDF 导入失败：{e}")


# ---------------------------------------------------------------- 教材知识库（本地预览）

@router.get("/library")
def library():
    """教材知识库：列出本地已下载的教材 PDF"""
    try:
        return textbook_service.library_catalog()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取教材知识库失败：{e}")


@router.get("/library/preview")
def library_preview(version: str, subject: str, grade: str = "", semester: str = "", page: int = 1):
    """在线预览教材 PDF 指定页（返回 base64 PNG + 总页数）"""
    try:
        return textbook_service.preview_page(version, subject, grade, semester, page)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.get("/library/units")
def library_units(version: str, subject: str, grade: str = "", semester: str = ""):
    """从 OCR 文本提取单元目录（标题 + 起始页码）"""
    try:
        return {"units": textbook_service.book_units(version, subject, grade, semester)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/library/locate")
def library_locate(version: str, subject: str, grade: str = "", semester: str = "", keyword: str = ""):
    """按关键词在教材文本（OCR txt 或 PDF 文本层）中定位页码"""
    try:
        return {"pages": textbook_service.locate_keyword(version, subject, grade, semester, keyword)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/library/knowledge-points")
def library_knowledge_points(version: str = "", subject: str = "", grade: str = "", semester: str = ""):
    """该教材已导入的知识点（按章节分组 + 定位页码），供左侧知识点导航"""
    try:
        return textbook_service.book_knowledge_points(version, subject, grade, semester)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
