# -*- coding: utf-8 -*-
"""运营配置 API：
- GET /api/config/public        公开配置（官网注册/升级页显示：体验天数、价格）
- GET /api/ops/config           运营后台读全部配置（请求头 X-Ops-Password 口令）
- PUT /api/ops/config           运营后台写配置（请求头 X-Ops-Password 口令）
- POST /api/ops/ai-gateway/test AI 网关连通测试（请求头 X-Ops-Password 口令）
"""
from fastapi import APIRouter, Depends, HTTPException, Header
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.app_config import AppConfig

router = APIRouter(prefix="/api", tags=["运营配置"])

CONFIG_DEFAULTS = {
    "trial_days": "15",
    "online_price": "100",
    "local_price": "50",
    "local_download_url": "",
    "local_guide_url": "",
    "ops_username": "admin",
    "ops_password": "easyfix-ops",
    # AI 网关（订阅制：用户无需配置 Key，凭证由运营统一配置在网关）
    "ai_gateway_provider": "openai",
    "ai_gateway_base_url": "",
    "ai_gateway_api_key": "",
    "ai_gateway_models": "",
    "ai_gateway_default_model": "",
}

PUBLIC_KEYS = ("trial_days", "online_price", "local_price")


def seed_app_config(db: Session) -> None:
    """启动时播种默认配置（幂等，只补缺失键）"""
    for key, value in CONFIG_DEFAULTS.items():
        if not db.query(AppConfig).filter_by(key=key).first():
            db.add(AppConfig(key=key, value=value))
    db.commit()


def get_config_value(db: Session, key: str, default: str = "") -> str:
    row = db.query(AppConfig).filter_by(key=key).first()
    return row.value if row is not None else default


def get_config_map(db: Session) -> dict:
    rows = db.query(AppConfig).all()
    out = dict(CONFIG_DEFAULTS)
    for row in rows:
        out[row.key] = row.value
    return out


def _check_ops_password(db: Session, ops_password: str, ops_username: str = "") -> None:
    """运营鉴权：账号（默认 admin）+ 口令双因子，二者缺一不可"""
    expected_pw = get_config_value(db, "ops_password", CONFIG_DEFAULTS["ops_password"])
    if not ops_password or ops_password != expected_pw:
        raise HTTPException(status_code=401, detail="运营口令错误")
    expected_user = get_config_value(db, "ops_username", CONFIG_DEFAULTS["ops_username"])
    if not ops_username or ops_username != expected_user:
        raise HTTPException(status_code=401, detail="运营账号错误")


class ConfigUpdateRequest(BaseModel):
    values: dict


@router.get("/config/public")
def config_public(db: Session = Depends(get_db)):
    """公开配置：trial_days / online_price / local_price（无需登录）"""
    cfg = get_config_map(db)
    return {k: cfg.get(k, "") for k in PUBLIC_KEYS}


@router.get("/ops/config")
def ops_config_get(x_ops_username: str = Header(default=""), x_ops_password: str = Header(default=""), db: Session = Depends(get_db)):
    _check_ops_password(db, x_ops_password, x_ops_username)
    return {"config": get_config_map(db)}


@router.put("/ops/config")
def ops_config_put(data: ConfigUpdateRequest, x_ops_username: str = Header(default=""), x_ops_password: str = Header(default=""), db: Session = Depends(get_db)):
    _check_ops_password(db, x_ops_password, x_ops_username)
    allowed = set(CONFIG_DEFAULTS.keys())
    changed = []
    for key, value in (data.values or {}).items():
        if key not in allowed:
            continue
        row = db.query(AppConfig).filter_by(key=key).first()
        if not row:
            db.add(AppConfig(key=key, value=str(value)))
        else:
            row.value = str(value)
        changed.append(key)
    db.commit()
    return {"updated": changed, "config": get_config_map(db)}


@router.post("/ops/ai-gateway/test")
def ops_ai_gateway_test(x_ops_username: str = Header(default=""), x_ops_password: str = Header(default=""), db: Session = Depends(get_db)):
    """AI 网关连通测试：用当前配置对默认模型发最小请求（真实调用上游，消耗极少量 token）"""
    _check_ops_password(db, x_ops_password, x_ops_username)
    from app.services.ai_gateway import AIGatewayClient, default_model, get_gateway_config

    try:
        gateway = get_gateway_config()
        if not gateway["api_key"]:
            return {"ok": False, "message": "AI 网关未配置 API Key，请先在运营后台填写"}
        model = gateway["default_model"] or "gpt-4o"
        client = AIGatewayClient()
        resp = client.chat(
            model=model,
            messages=[{"role": "user", "content": "ping"}],
            max_tokens=8,
            timeout=30,
            caller="ops_test",
        )
        text = resp.content[0].text if resp.content else ""
        return {"ok": True, "model": model, "usage": resp.usage, "reply": text[:100]}
    except Exception as e:
        return {"ok": False, "message": str(e)}
