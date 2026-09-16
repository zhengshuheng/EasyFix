from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.services import textbook_service, ctsf_import

router = APIRouter(prefix="/api/textbook", tags=["教材同步"])


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
def scan_local():
    """扫描本地教材文件夹（手动放置兜底）"""
    try:
        return {"files": textbook_service.scan_local(), "dir": textbook_service.DATA_DIR}
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


# ---------------------------------------------------------------- ChinaStudyFree 在线大纲

@router.get("/ctsf/catalog")
def ctsf_catalog():
    """在线知识大纲目录（ChinaStudyFree，MIT）：数学人教版/语文统编/英语PEP/科学教科版 44 本"""
    try:
        return ctsf_import.get_catalog()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"获取在线大纲目录失败：{e}")


@router.post("/ctsf/import")
def ctsf_import_book(req: CtsfImportRequest):
    """从在线知识大纲导入指定教材的知识点（免下载/免OCR），返回 task_id"""
    try:
        task = ctsf_import.start_ctsf_import(
            req.subject.strip(), req.version.strip(), req.grade.strip(), req.semester.strip())
        return {"task_id": task["id"], "status": task["status"], "source": "ctsf-online"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"启动导入失败：{e}")


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
