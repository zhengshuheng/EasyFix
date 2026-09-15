import json
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from app.database import get_db
from app.models import ErrorBook, Subject, User
from app.schemas import ErrorBookCreate, ErrorBookUpdate, ErrorBookResponse, ErrorBookListResponse
from app.services.logger import logger_service
from app.utils.auth import get_current_user

router = APIRouter(prefix="/api/error-books", tags=["错题本"])


def _eb_dict(eb: ErrorBook) -> dict:
    return {
        "id": eb.id,
        "name": eb.name,
        "subject_id": eb.subject_id,
        "user_id": eb.user_id,
        "user_name": eb.owner.display_name or eb.owner.username if eb.owner else None,
        "description": eb.description,
        "cover_image": eb.cover_image,
        "original_images": json.loads(eb.original_images or "[]") if eb.original_images else [],
        "created_at": eb.created_at,
        "updated_at": eb.updated_at,
    }


def _assert_owner(user: User, eb: ErrorBook):
    """小孩只能访问/操作自己的错题本；家长（admin）可访问全部"""
    if user.role != "admin" and eb.user_id != user.id:
        raise HTTPException(status_code=403, detail="无权操作该错题本")


@router.get("", response_model=ErrorBookListResponse)
def list_error_books(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    subject_id: Optional[int] = None,
    user_id: Optional[int] = None,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """获取错题本列表（排除已删除的）；小孩只看自己的，家长可看全部或按小孩筛选"""
    query = db.query(ErrorBook).filter(ErrorBook.deleted == False)

    if user.role == "child":
        # 小孩只能看自己的错题本
        query = query.filter(ErrorBook.user_id == user.id)
    elif user_id is not None:
        query = query.filter(ErrorBook.user_id == user_id)

    if subject_id:
        query = query.filter(ErrorBook.subject_id == subject_id)

    total = query.count()
    items = query.order_by(ErrorBook.created_at.desc()).offset(skip).limit(limit).all()
    result_items = [_eb_dict(item) for item in items]

    return {"total": total, "items": result_items}


@router.get("/{error_book_id}", response_model=ErrorBookResponse)
def get_error_book(
    error_book_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """获取单个错题本"""
    error_book = db.query(ErrorBook).filter(ErrorBook.id == error_book_id, ErrorBook.deleted == False).first()
    if not error_book:
        raise HTTPException(status_code=404, detail="错题本不存在")
    _assert_owner(user, error_book)
    return _eb_dict(error_book)


@router.post("", response_model=ErrorBookResponse, status_code=201)
def create_error_book(
    data: ErrorBookCreate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """创建错题本（小孩自动归属自己；家长可指定所属小孩，不指定则无主）"""
    subject = db.query(Subject).filter(Subject.id == data.subject_id, Subject.deleted == False).first()
    if not subject:
        raise HTTPException(status_code=400, detail="学科不存在")

    owner_id = user.id if user.role == "child" else data.user_id
    if owner_id is not None:
        owner = db.get(User, owner_id)
        if not owner or owner.role != "child":
            raise HTTPException(status_code=400, detail="所属小孩不存在")

    error_book = ErrorBook(
        name=data.name,
        subject_id=data.subject_id,
        user_id=owner_id,
        description=data.description,
        cover_image=data.cover_image,
        original_images=json.dumps(data.original_images or [], ensure_ascii=False) if data.original_images else None,
    )
    db.add(error_book)
    db.commit()
    db.refresh(error_book)

    logger_service.log_error_book(
        operation="create_error_book",
        error_book_id=error_book.id,
        data={"name": data.name, "subject_id": data.subject_id, "user_id": owner_id},
        success=True,
    )

    return _eb_dict(error_book)


@router.put("/{error_book_id}", response_model=ErrorBookResponse)
def update_error_book(
    error_book_id: int,
    data: ErrorBookUpdate,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """更新错题本"""
    error_book = db.query(ErrorBook).filter(ErrorBook.id == error_book_id, ErrorBook.deleted == False).first()
    if not error_book:
        raise HTTPException(status_code=404, detail="错题本不存在")
    _assert_owner(user, error_book)

    update_data = data.model_dump(exclude_unset=True)

    # 处理original_images
    if "original_images" in update_data:
        update_data["original_images"] = json.dumps(update_data["original_images"], ensure_ascii=False)

    for key, value in update_data.items():
        setattr(error_book, key, value)

    db.commit()
    db.refresh(error_book)

    logger_service.log_error_book(
        operation="update_error_book",
        error_book_id=error_book.id,
        data=update_data,
        success=True,
    )

    return _eb_dict(error_book)


@router.delete("/{error_book_id}", status_code=204)
def delete_error_book(
    error_book_id: int,
    db: Session = Depends(get_db),
    user: User = Depends(get_current_user),
):
    """
    软删除错题本（设置deleted=True），而非物理删除
    错题本下的错题不受影响（仍可通过error_book_id关联查询）
    """
    error_book = db.query(ErrorBook).filter(ErrorBook.id == error_book_id, ErrorBook.deleted == False).first()
    if not error_book:
        raise HTTPException(status_code=404, detail="错题本不存在")
    _assert_owner(user, error_book)

    # 软删除：设置deleted标志为True
    error_book.deleted = True
    db.commit()

    logger_service.log_error_book(
        operation="delete_error_book",
        error_book_id=error_book_id,
        data={"soft_delete": True},
        success=True,
    )
