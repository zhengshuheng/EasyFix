"""空间数据同步 API（用户空间内，管理员鉴权）

从主库 Ops 仓库同步教材数据到当前空间库（全量替换、幂等）：
- POST /api/sync/knowledge-points  {subject, version}   → 空间库知识点
- POST /api/sync/words            {version, grade, semester} → 空间库单词
- GET  /api/sync/status                                  → 当前同步状态 + 可更新列表
"""
from typing import Optional

from fastapi import APIRouter, Depends, Header, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import SessionLocal, get_db
from app.models.ops_data import ensure_ops_tables
from app.services import ops_data_service
from app.trial import get_space_by_key
from app.utils.auth import require_admin

router = APIRouter(prefix="/api/sync", tags=["空间数据同步"])


def _space_key(x_trial_key: str) -> str:
    record = get_space_by_key(x_trial_key) if x_trial_key else None
    if not record:
        raise HTTPException(status_code=404, detail="空间不存在或 X-Trial-Key 无效")
    return x_trial_key


class KPSyncRequest(BaseModel):
    subject: str
    version: str


class WordSyncRequest(BaseModel):
    version: str
    grade: int
    semester: int


class WordAllSyncRequest(BaseModel):
    version: str


@router.get("/status")
def sync_status(x_trial_key: str = Header(default="", alias="X-Trial-Key"),
                _admin=Depends(require_admin)):
    key = _space_key(x_trial_key)
    ensure_ops_tables()
    sync = ops_data_service.get_space_sync_status(key)
    catalog = ops_data_service.get_ops_catalog()
    return {"space": key, "synced": sync, "catalog": catalog}


@router.post("/knowledge-points")
def sync_knowledge_points(data: KPSyncRequest,
                          x_trial_key: str = Header(default="", alias="X-Trial-Key"),
                          db: Session = Depends(get_db),
                          _admin=Depends(require_admin)):
    key = _space_key(x_trial_key)
    try:
        result = ops_data_service.sync_knowledge_points(
            db, key, data.subject.strip(), data.version.strip())
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"知识点同步失败：{e}")
    if result.get("reason"):
        raise HTTPException(status_code=404, detail=result["reason"])
    return result


@router.post("/words")
def sync_words(data: WordSyncRequest,
               x_trial_key: str = Header(default="", alias="X-Trial-Key"),
               db: Session = Depends(get_db),
               _admin=Depends(require_admin)):
    key = _space_key(x_trial_key)
    try:
        result = ops_data_service.sync_words(
            db, key, data.version.strip(), data.grade, data.semester)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"单词同步失败：{e}")
    if result.get("reason"):
        raise HTTPException(status_code=404, detail=result["reason"])
    return result


@router.post("/words-all")
def sync_words_all(data: WordAllSyncRequest,
                   x_trial_key: str = Header(default="", alias="X-Trial-Key"),
                   db: Session = Depends(get_db),
                   _admin=Depends(require_admin)):
    """一键同步 1-6 年级全部英语单词（按 ops 仓库存在的册循环替换）"""
    key = _space_key(x_trial_key)
    version = data.version.strip()
    results = []
    total_added = total_removed = 0
    for grade in range(1, 7):
        for semester in (1, 2):
            try:
                r = ops_data_service.sync_words(db, key, version, grade, semester)
            except Exception as e:
                db.rollback()
                continue
            if r.get("reason"):
                continue
            results.append({"grade": grade, "semester": semester, **r})
            total_added += r.get("added", 0)
            total_removed += r.get("removed", 0)
    if not results:
        raise HTTPException(status_code=404, detail=f"ops 仓库无该版本英语单词（{version}）")
    return {"books": results, "added": total_added, "removed": total_removed}
