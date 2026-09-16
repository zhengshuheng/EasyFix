from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional

from app.services import k12_import

router = APIRouter(prefix="/api/k12", tags=["教材知识库"])


class K12ImportRequest(BaseModel):
    grade_band: str  # 小学/初中/高中
    subject: str     # 科目名（对应数据文件）
    confidence_min: Optional[float] = 0.7
    limit: Optional[int] = None  # 测试用：仅导入前 N 条


@router.get("/catalog")
def catalog():
    """获取知识库拆分索引（学段×科目文件清单）"""
    try:
        return k12_import.get_catalog()
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"获取知识库索引失败：{e}")


@router.post("/import")
def import_subject(req: K12ImportRequest):
    """导入指定 学段×科目 的知识点（LLM 自动分配年级学期）"""
    try:
        result = k12_import.import_subject(
            req.grade_band.strip(),
            req.subject.strip(),
            req.confidence_min or 0.7,
            req.limit,
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"导入失败：{e}")
