"""认证与授权工具：PBKDF2 密码哈希 + HMAC 签名 Token + FastAPI 依赖

零第三方依赖，仅使用标准库。

宽松/严格模式：
- 宽松模式（系统中只有默认家长账号）：未登录请求视为 admin，兼容旧前端（旧前端不传 token）
- 严格模式（已创建第二个用户）：所有接口必须登录，管理接口必须 admin 角色
"""
import base64
import hashlib
import hmac
import json
import os
import secrets
import time
from typing import Optional

from fastapi import Depends, Header, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.user import User

# Token 密钥：优先读环境变量，便于部署时更换
TOKEN_SECRET = os.environ.get("EASYFIX_TOKEN_SECRET", "easyfix-local-secret-change-me")
TOKEN_TTL = 60 * 60 * 24 * 30  # 30 天

PBKDF2_ITERATIONS = 120_000

# 默认家长账号（首次启动自动创建；密码迁移自 access_config.ACCESS_PASSWORD）
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_PASSWORD = "32167"


# ---------- 密码哈希 ----------

def hash_password(password: str) -> str:
    salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac(
        "sha256", password.encode("utf-8"), salt, PBKDF2_ITERATIONS
    )
    return "pbkdf2${}${}${}".format(
        PBKDF2_ITERATIONS, salt.hex(), digest.hex()
    )


def verify_password(password: str, stored: Optional[str]) -> bool:
    if not stored:
        return False
    try:
        scheme, iterations, salt_hex, digest_hex = stored.split("$", 3)
        if scheme != "pbkdf2":
            return False
        digest = hashlib.pbkdf2_hmac(
            "sha256",
            password.encode("utf-8"),
            bytes.fromhex(salt_hex),
            int(iterations),
        )
        return hmac.compare_digest(digest.hex(), digest_hex)
    except Exception:
        return False


# ---------- Token ----------

def _b64e(data: bytes) -> str:
    return base64.urlsafe_b64encode(data).rstrip(b"=").decode("ascii")


def _b64d(data: str) -> bytes:
    return base64.urlsafe_b64decode(data + "=" * (-len(data) % 4))


def create_token(user: User) -> str:
    payload = {
        "uid": user.id,
        "role": user.role,
        "exp": int(time.time()) + TOKEN_TTL,
    }
    body = _b64e(json.dumps(payload, separators=(",", ":")).encode("utf-8"))
    sig = hmac.new(TOKEN_SECRET.encode("utf-8"), body.encode("ascii"), hashlib.sha256).digest()
    return body + "." + _b64e(sig)


def parse_token(token: str) -> Optional[dict]:
    try:
        body, sig = token.split(".", 1)
        expect = hmac.new(
            TOKEN_SECRET.encode("utf-8"), body.encode("ascii"), hashlib.sha256
        ).digest()
        if not hmac.compare_digest(expect, _b64d(sig)):
            return None
        payload = json.loads(_b64d(body))
        if payload.get("exp", 0) < time.time():
            return None
        return payload
    except Exception:
        return None


# ---------- 模式判定 ----------

def is_strict_mode(db: Session) -> bool:
    """严格模式：用户数 > 1（创建过第二个用户）"""
    return db.query(User).count() > 1


# ---------- FastAPI 依赖 ----------

def get_optional_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
) -> Optional[User]:
    """解析当前登录用户；未登录返回 None（不报错）"""
    if not authorization:
        return None
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        return None
    payload = parse_token(token)
    if not payload:
        return None
    return db.get(User, payload.get("uid"))


def get_current_user(
    user: Optional[User] = Depends(get_optional_user),
    db: Session = Depends(get_db),
) -> User:
    """必须登录；宽松模式下未登录视为默认家长（兼容旧前端）"""
    if user is None and not is_strict_mode(db):
        user = db.query(User).filter_by(username=DEFAULT_ADMIN_USERNAME).first()
    if user is None:
        raise HTTPException(status_code=401, detail="未登录或登录已过期")
    if not user.enabled:
        raise HTTPException(status_code=403, detail="账号已被禁用")
    return user


def require_admin(
    user: User = Depends(get_current_user),
) -> User:
    """管理接口：必须 admin 角色"""
    if user.role != "admin":
        raise HTTPException(status_code=403, detail="需要家长（管理员）权限")
    return user
