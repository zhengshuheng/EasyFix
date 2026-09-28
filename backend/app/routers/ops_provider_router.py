# -*- coding: utf-8 -*-
"""AI 模型厂商管理（运营后台·AI 模型市场）

多厂商凭证/模型维护：学生端按 vendor 选厂商 → 选模型，LLM 与多模态 OCR
共用同一网关收敛点 AIGatewayClient(config)。旧单厂商 ai_gateway_* 配置兜底。
"""
from fastapi import APIRouter, Header, HTTPException
from pydantic import BaseModel
from sqlalchemy import func

from app.config_api import _check_ops_password
from app.database import SessionLocal
from app.models.ops_data import OpsAiProvider, ensure_ops_tables
from app.services.ai_gateway import (
    AIGatewayClient,
    provider_to_dict,
    resolve_gateway_config,
)

router = APIRouter(prefix="/api/ops/providers", tags=["Ops AI 模型厂商"])


class ProviderIn(BaseModel):
    name: str
    vendor: str
    protocol: str = "openai"   # openai（兼容协议）/ anthropic
    base_url: str = ""
    api_key: str = ""
    models: str = ""           # 逗号分隔
    vision_models: str = ""    # 逗号分隔视觉模型（留空=不支持 OCR）
    enabled: bool = True
    is_default: bool = False


def _ops_check(x_ops_username: str, x_ops_password: str) -> None:
    db = SessionLocal()
    try:
        _check_ops_password(db, x_ops_password, x_ops_username)
    finally:
        db.close()


def _validate(payload: ProviderIn) -> None:
    if not payload.name.strip():
        raise HTTPException(status_code=400, detail="厂商名称不能为空")
    if not payload.vendor.strip():
        raise HTTPException(status_code=400, detail="厂商标识（vendor）不能为空")
    protocol = payload.protocol.strip().lower()
    if protocol not in ("openai", "anthropic"):
        raise HTTPException(status_code=400, detail="protocol 仅支持 openai / anthropic")
    if not payload.models.strip():
        raise HTTPException(status_code=400, detail="请至少配置一个模型")


@router.get("")
def ops_provider_list(x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    """厂商列表（api_key 掩码返回）"""
    _ops_check(x_ops_username, x_ops_password)
    ensure_ops_tables()
    db = SessionLocal()
    try:
        rows = db.query(OpsAiProvider).order_by(OpsAiProvider.id.asc()).all()
        return {"items": [provider_to_dict(p, masked=True) for p in rows], "total": len(rows)}
    finally:
        db.close()


@router.post("")
def ops_provider_create(payload: ProviderIn,
                        x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    """新增厂商"""
    _ops_check(x_ops_username, x_ops_password)
    _validate(payload)
    ensure_ops_tables()
    db = SessionLocal()
    try:
        exists = db.query(OpsAiProvider).filter(
            func.lower(OpsAiProvider.vendor) == payload.vendor.strip().lower()
        ).first()
        if exists:
            raise HTTPException(status_code=400, detail=f"厂商标识 {payload.vendor.strip()} 已存在")
        if payload.is_default:
            db.query(OpsAiProvider).filter(OpsAiProvider.is_default == True).update(  # noqa: E712
                {OpsAiProvider.is_default: False})
        p = OpsAiProvider(
            name=payload.name.strip(),
            vendor=payload.vendor.strip(),
            protocol=payload.protocol.strip().lower(),
            base_url=payload.base_url.strip() or None,
            api_key=payload.api_key or None,
            models=payload.models.strip(),
            vision_models=payload.vision_models.strip() or None,
            enabled=payload.enabled,
            is_default=payload.is_default,
        )
        db.add(p)
        db.commit()
        db.refresh(p)
        return provider_to_dict(p, masked=True)
    finally:
        db.close()


@router.put("/{pid}")
def ops_provider_update(pid: int, payload: ProviderIn,
                        x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    """更新厂商"""
    _ops_check(x_ops_username, x_ops_password)
    _validate(payload)
    ensure_ops_tables()
    db = SessionLocal()
    try:
        p = db.query(OpsAiProvider).filter(OpsAiProvider.id == pid).first()
        if not p:
            raise HTTPException(status_code=404, detail="厂商不存在")
        dup = db.query(OpsAiProvider).filter(
            func.lower(OpsAiProvider.vendor) == payload.vendor.strip().lower(),
            OpsAiProvider.id != pid,
        ).first()
        if dup:
            raise HTTPException(status_code=400, detail=f"厂商标识 {payload.vendor.strip()} 已存在")
        if payload.is_default:
            db.query(OpsAiProvider).filter(OpsAiProvider.is_default == True).update(  # noqa: E712
                {OpsAiProvider.is_default: False})
        p.name = payload.name.strip()
        p.vendor = payload.vendor.strip()
        p.protocol = payload.protocol.strip().lower()
        p.base_url = payload.base_url.strip() or None
        # api_key 留空表示不修改（列表接口掩码返回，前端编辑不重复填）
        if payload.api_key:
            p.api_key = payload.api_key
        p.models = payload.models.strip()
        p.vision_models = payload.vision_models.strip() or None
        p.enabled = payload.enabled
        p.is_default = payload.is_default
        db.commit()
        db.refresh(p)
        return provider_to_dict(p, masked=True)
    finally:
        db.close()


@router.delete("/{pid}")
def ops_provider_delete(pid: int,
                        x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    """删除厂商"""
    _ops_check(x_ops_username, x_ops_password)
    ensure_ops_tables()
    db = SessionLocal()
    try:
        p = db.query(OpsAiProvider).filter(OpsAiProvider.id == pid).first()
        if not p:
            raise HTTPException(status_code=404, detail="厂商不存在")
        db.delete(p)
        db.commit()
        return {"deleted": pid}
    finally:
        db.close()


@router.post("/{pid}/test")
def ops_provider_test(pid: int,
                      x_ops_username: str = Header(default=""), x_ops_password: str = Header(default="")):
    """厂商连通测试：用该厂商默认模型发最小请求（真实调用上游，消耗极少量 token）"""
    _ops_check(x_ops_username, x_ops_password)
    ensure_ops_tables()
    db = SessionLocal()
    try:
        p = db.query(OpsAiProvider).filter(OpsAiProvider.id == pid).first()
    finally:
        db.close()
    if not p:
        raise HTTPException(status_code=404, detail="厂商不存在")
    if not p.api_key:
        return {"ok": False, "message": "该厂商未配置 API Key"}
    cfg = resolve_gateway_config(p.vendor)
    if not cfg.get("api_key"):
        return {"ok": False, "message": "AI 网关未配置 API Key"}
    model = (cfg.get("models") or ["unknown"])[0]
    try:
        client = AIGatewayClient(cfg)
        resp = client.chat(
            model=model,
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=16,
            timeout=30,
        )
        return {"ok": True, "model": model, "reply": getattr(resp.content[0], "text", "")[:80]}
    except Exception as e:
        return {"ok": False, "message": str(e)[:300]}
