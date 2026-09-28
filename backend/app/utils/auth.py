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
import re
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

# ---------- 注册安全规则（符合主流互联网应用要求） ----------
# 用户名：4-20 位，字母开头，仅字母/数字/下划线
USERNAME_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_]{3,19}$")
# 密码：8-20 位，至少两类字符（字母/数字/符号取二），不连续 3 相同，不含用户名，弱密码黑名单

WEAK_PASSWORDS = frozenset({
    "12345678", "123456789", "1234567890", "123456789a", "123456789ab",
    "password", "password1", "password123", "passw0rd", "passw0rd1",
    "qwertyui", "qwerty123", "qwertyuiop", "asdfghjk", "asdfghjkl",
    "zxcvbnm1", "abcdefgh", "abc12345", "abc123456", "abcd1234",
    "admin123", "admin888", "admin123456", "root123", "root1234",
    "test1234", "test12345", "iloveyou", "woaini1314", "qq123456",
    "11111111", "00000000", "88888888", "66666666", "a1234567", "a12345678",
})


def validate_username(username: str) -> str:
    """用户名校验；返回错误消息（空串=通过）
    支持两种格式：大陆手机号（11 位，1 开头）或旧式用户名（字母开头 4-20 位，兼容存量账号）"""
    username = (username or "").strip()
    if USERNAME_RE.fullmatch(username):
        return ""
    if re.fullmatch(r"1[3-9]\d{9}", username):
        return ""
    return "用户名需为 11 位手机号（或以字母开头的旧用户名）"


def validate_password(username: str, password: str) -> str:
    """密码校验；返回错误消息（空串=通过）"""
    password = password or ""
    if not 8 <= len(password) <= 20:
        return "密码需 8-20 个字符"
    classes = 0
    if re.search(r"[A-Za-z]", password):
        classes += 1
    if re.search(r"[0-9]", password):
        classes += 1
    if re.search(r"[^A-Za-z0-9]", password):
        classes += 1
    if classes < 2:
        return "密码需同时包含字母和数字（可再含符号）"
    if re.search(r"(.)\1{2,}", password):
        return "密码不能包含连续 3 个相同字符"
    if username and username.lower() in password.lower():
        return "密码不能包含用户名"
    if password.lower() in WEAK_PASSWORDS:
        return "密码过于简单，请更换更复杂的密码"
    return ""


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


def create_token(user, scope: Optional[str] = None, persistent: bool = False) -> str:
    """签发 HMAC token。

    - scope=None（默认）：租户内 User token（租户 API 用，payload 带 role）
    - scope="account"：全局账号 token（/api/auth、/api/trial/spaces 用，payload 无 role）
    - persistent=True：不写 exp（永久有效）——空间登录态用；空间访问门禁靠
      到期校验（/api/trial/status → 前端守卫拦截 /subscribe），不用 token 过期兜底。
      官网全局账号 token 保持默认 30 天（账号入口安全边界）。
    """
    payload = {"uid": user.id}
    if scope:
        payload["scope"] = scope
    elif getattr(user, "role", None):
        payload["role"] = user.role
    if not persistent:
        payload["exp"] = int(time.time()) + TOKEN_TTL
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
        # 无 exp = 永久 token（空间持久登录态）；有 exp 则校验过期
        exp = payload.get("exp")
        if exp is not None and exp < time.time():
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
    """解析当前登录用户；未登录返回 None（不报错）

    注意：scope=account 的全局账号 token 不能用于租户内 API（没有租户 User 身份），
    一律视为未登录；租户 API 的鉴权请使用租户内 User token。
    """
    if not authorization:
        return None
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        return None
    payload = parse_token(token)
    if not payload:
        return None
    if payload.get("scope") == "account":
        return None
    return db.get(User, payload.get("uid"))


def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
) -> User:
    """必须登录；宽松模式下未登录视为默认家长（兼容旧前端）

    注意：请求带了 token 但用户解析不到（无效 token / 用户已被删除）→ 一律 401，
    不做宽松兜底——保证删除家长后其已签发的 token 立即失效，不会因宽松模式
    被放大成默认家长放行。
    """
    has_token = False
    user = None
    if authorization:
        scheme, _, token = authorization.partition(" ")
        if scheme.lower() == "bearer" and token:
            has_token = True
            payload = parse_token(token)
            if payload and payload.get("scope") != "account":
                user = db.get(User, payload.get("uid"))
    if user is None:
        if has_token:
            raise HTTPException(status_code=401, detail="登录已过期或账号已被删除")
        if not is_strict_mode(db):
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


# ---------- 全局账号鉴权（账号/空间分离后 /api/auth、/api/trial/spaces 用）----------

def get_current_account(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
) -> "Account":
    """必须携带 scope=account 的全局账号 token；无效一律 401。

    注意依赖 get_db（默认正式库）：账号 API 不得带 X-Trial-Key。
    """
    from app.models.account import Account  # 局部导入避免循环

    if not authorization:
        raise HTTPException(status_code=401, detail="未登录")
    scheme, _, token = authorization.partition(" ")
    if scheme.lower() != "bearer" or not token:
        raise HTTPException(status_code=401, detail="未登录")
    payload = parse_token(token)
    if not payload or payload.get("scope") != "account":
        raise HTTPException(status_code=401, detail="登录已过期，请重新登录")
    account = db.get(Account, payload.get("uid"))
    if not account:
        raise HTTPException(status_code=401, detail="账号不存在")
    if not account.enabled:
        raise HTTPException(status_code=401, detail="账号已被禁用，请联系管理员")
    return account
