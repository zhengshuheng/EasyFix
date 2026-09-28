# -*- coding: utf-8 -*-
"""AI 网关：订阅制下用户无需配置模型 Key，所有 LLM 调用统一经此转发上游。

- 网关凭证（上游 provider/base_url/api_key + 可用模型列表 + 默认模型）由运营在
  ops 后台配置，存主库 app_config（键 ai_gateway_*，X-Ops-Password 保护）。
- 唯一上游入口 `AIGatewayClient.chat()`：返回兼容响应对象（content blocks 列表）
  并附归一化 usage —— 为后续「消耗/价格」计算预留，计费点只需在 chat() 内加。
- anthropic/openai 的 RateLimitError 原样冒泡（上游 `_retry_on_rate_limit`
  依赖捕获这两个异常类型做指数退避）。
"""
import os
from types import SimpleNamespace

from app.config import get_settings

settings = get_settings()

GATEWAY_KEYS = (
    "ai_gateway_provider",
    "ai_gateway_base_url",
    "ai_gateway_api_key",
    "ai_gateway_models",
    "ai_gateway_default_model",
)


def _read_gateway_rows() -> dict:
    """读主库 app_config 的 ai_gateway_* 键。

    注意：不能用 Depends(get_db)——带 X-Trial-Key 时 get_db 分发到空间库，
    app_config 在**主库**，必须 SessionLocal 直连主库（见 AI_CONTEXT 1.6 坑）。
    """
    try:
        from app.database import SessionLocal
        from app.models.app_config import AppConfig

        db = SessionLocal()
        try:
            rows = db.query(AppConfig).filter(AppConfig.key.in_(GATEWAY_KEYS)).all()
            return {r.key: (r.value or "").strip() for r in rows}
        finally:
            db.close()
    except Exception as e:
        print(f"[ai-gateway] 读网关配置失败: {e}")
        return {}


def parse_models(raw: str) -> list:
    """逗号分隔模型列表 → list[str]（去空白去空）"""
    if not raw:
        return []
    return [m.strip() for m in raw.split(",") if m.strip()]


def get_gateway_config() -> dict:
    """网关配置（每次读取实时生效）。未配置时 fallback Settings 遗留值，保证本地零配置可跑。"""
    kv = _read_gateway_rows()
    provider = (kv.get("ai_gateway_provider") or "openai").strip().lower()
    if provider not in ("openai", "anthropic"):
        provider = "openai"
    base_url = kv.get("ai_gateway_base_url") or ""
    api_key = kv.get("ai_gateway_api_key") or settings.OPENAI_API_KEY
    models = parse_models(kv.get("ai_gateway_models") or "")
    default_model = (kv.get("ai_gateway_default_model") or "").strip()
    if not default_model:
        default_model = models[0] if models else settings.LLM_MODEL
    return {
        "provider": provider,
        "base_url": base_url,
        "api_key": api_key,
        "models": models,
        "default_model": default_model,
    }


def list_available_models() -> list:
    """可用模型列表（用户只选模型名）。ops 未配置时给 Settings.LLM_MODEL 兜底。"""
    cfg = get_gateway_config()
    return cfg["models"] or [settings.LLM_MODEL]


def default_model() -> str:
    """默认模型（用户未选择时兜底）"""
    return get_gateway_config()["default_model"] or settings.LLM_MODEL


def gateway_configured() -> bool:
    """网关是否已配置上游 Key（供前端提示用）"""
    return bool(get_gateway_config()["api_key"])


# ---------- AI 模型厂商（多厂商市场） ----------

def _read_providers(enabled_only: bool = True) -> list:
    """读主库 ops_ai_provider 厂商配置（enabled_only=True 只取启用项）"""
    try:
        from app.database import SessionLocal
        from app.models.ops_data import OpsAiProvider

        db = SessionLocal()
        try:
            q = db.query(OpsAiProvider)
            if enabled_only:
                q = q.filter(OpsAiProvider.enabled == True)  # noqa: E712
            return q.order_by(OpsAiProvider.id.asc()).all()
        finally:
            db.close()
    except Exception as e:
        print(f"[ai-gateway] 读厂商配置失败: {e}")
        return []


def _mask_key(key: str) -> str:
    if not key:
        return ""
    if len(key) <= 8:
        return "****"
    return f"{key[:4]}****{key[-4:]}"


def provider_to_dict(p, masked: bool = True) -> dict:
    """OpsAiProvider 对象 → 前端字典（掩码 key）"""
    return {
        "id": p.id,
        "name": p.name,
        "vendor": p.vendor,
        "protocol": p.protocol,
        "base_url": p.base_url or "",
        "api_key": _mask_key(p.api_key or "") if masked else (p.api_key or ""),
        "models": parse_models(p.models or ""),
        "vision_models": parse_models(p.vision_models or ""),
        "enabled": bool(p.enabled),
        "is_default": bool(p.is_default),
        "created_at": p.created_at.isoformat() if p.created_at else "",
    }


def list_providers(enabled_only: bool = True) -> list:
    """可用厂商列表（学生端下拉用：只含启用项）"""
    return [provider_to_dict(p) for p in _read_providers(enabled_only)]


def get_provider(vendor: str = None) -> dict:
    """按 vendor 取厂商配置；未指定 → 默认厂商（is_default）。无匹配返回 None。"""
    for p in _read_providers(enabled_only=True):
        if vendor:
            if (p.vendor or "").strip().lower() == vendor.strip().lower():
                return provider_to_dict(p, masked=False)
        elif p.is_default:
            return provider_to_dict(p, masked=False)
    return None


def resolve_gateway_config(vendor: str = None) -> dict:
    """解析网关配置：厂商市场存在 → 用厂商配置；否则回退旧 ai_gateway_* 单配置。"""
    p = get_provider(vendor)
    if p:
        protocol = (p["protocol"] or "openai").strip().lower()
        if protocol not in ("openai", "anthropic"):
            protocol = "openai"
        models = p["models"]
        default_model = p["models"][0] if p["models"] else (settings.LLM_MODEL if vendor else "")
        return {
            "provider": protocol,
            "base_url": p["base_url"],
            "api_key": p["api_key"],
            "models": models,
            "default_model": default_model,
            "vendor": p["vendor"],
            "vision_models": p["vision_models"],
        }
    return get_gateway_config()


class AIGatewayClient:
    """AI 网关客户端：每次调用重读配置重建 client，配置改立即可用。

    chat() 是**唯一**上游调用入口；返回值与旧 LLMService 客户端响应兼容
    （content 为块列表，text 在 block.text），另附 usage（归一化 token 用量）。
    """

    def __init__(self, config: dict = None):
        self._cfg = config or get_gateway_config()
        self._openai_compat = self._is_openai_compat()
        self._client = None
        self._init_client()

    def _is_openai_compat(self) -> bool:
        """provider=anthropic → Anthropic Messages 协议；其余（含默认 openai）→ OpenAI 兼容协议"""
        return self._cfg["provider"] != "anthropic"

    def _init_client(self):
        api_key = self._cfg["api_key"]
        base_url = self._cfg["base_url"]
        if self._openai_compat:
            import openai

            self._client = openai.OpenAI(
                api_key=api_key,
                base_url=base_url or "https://api.openai.com/v1",
            )
        else:
            import anthropic

            if base_url:
                self._client = anthropic.Anthropic(api_key=api_key, base_url=base_url)
            else:
                self._client = anthropic.Anthropic(api_key=api_key)

    def has_key(self) -> bool:
        return bool(self._cfg["api_key"])

    def chat(
        self,
        model: str,
        messages: list,
        system: str = "",
        max_tokens: int = 2000,
        temperature: float = None,
        timeout: int = 60,
        extra_body: dict = None,
        caller: str = "",
    ) -> SimpleNamespace:
        """统一网关调用。返回 SimpleNamespace(content=[{type,text}], usage={...}, model=str)。

        RateLimitError（anthropic/openai）原样冒泡给调用方重试；
        其余异常统一格式化（附带当前配置的 model/base_url/key 掩码，401 附排查提示）。
        """
        kwargs = {
            "model": model,
            "max_tokens": max_tokens,
            "messages": messages,
            "timeout": timeout,
        }
        if temperature is not None:
            kwargs["temperature"] = temperature
        if system:
            kwargs["system"] = system
        if extra_body:
            kwargs["extra_body"] = extra_body

        try:
            if self._openai_compat:
                resp = self._call_openai_compat(**kwargs)
            else:
                resp = self._call_anthropic(**kwargs)
        except Exception as e:
            # anthropic.RateLimitError / openai.RateLimitError 必须原样冒泡，
            # 上游 _retry_on_rate_limit 依赖捕获这两个类型做指数退避重试。
            import anthropic
            import openai

            if isinstance(e, (anthropic.RateLimitError, openai.RateLimitError)):
                raise
            raise Exception(self._format_llm_error(e, kwargs)) from e

        text = ""
        for block in resp.content:
            if getattr(block, "type", None) == "text" and getattr(block, "text", None):
                text = block.text
                break

        usage = self._normalize_usage(getattr(resp, "usage", None))
        if usage:
            print(f"[ai-gateway] caller={caller or '-'} model={model} usage={usage}")
        return SimpleNamespace(
            content=[SimpleNamespace(type="text", text=text)],
            usage=usage,
            model=model,
        )

    def _call_anthropic(self, **kwargs):
        """Anthropic Messages 协议（兼容不支持 thinking 参数的模型降级重试）"""
        import anthropic

        kwargs.pop("extra_body", None)  # anthropic 协议无此参数
        try:
            return self._client.messages.create(**kwargs)
        except TypeError as e:
            if "thinking" in str(e):
                kwargs.pop("thinking", None)
                return self._client.messages.create(**kwargs)
            raise
        except anthropic.RateLimitError:
            raise

    def _call_openai_compat(self, **kwargs):
        """OpenAI 兼容协议：转换 anthropic 风格参数为 chat.completions 格式。

        返回 SimpleNamespace(content=[{type:'text',text}], usage=usage)，下游无需改动。
        """
        params: dict = {}
        for key in ("model", "max_tokens", "temperature", "timeout"):
            if key in kwargs:
                params[key] = kwargs[key]
        # 透传 extra_body（如 DeepSeek 关闭思考 thinking={"type":"disabled"}）
        if kwargs.get("extra_body"):
            params["extra_body"] = kwargs["extra_body"]

        messages: list = []
        if kwargs.get("system"):
            messages.append({"role": "system", "content": kwargs["system"]})
        for m in kwargs.get("messages", []):
            content = m.get("content")
            if isinstance(content, list):
                # anthropic 内容块列表 → 拼接纯文本
                parts = []
                for b in content:
                    if isinstance(b, dict):
                        parts.append(b.get("text", ""))
                    else:
                        parts.append(getattr(b, "text", str(b)))
                content = "\n".join(parts)
            messages.append({"role": m.get("role", "user"), "content": content})
        params["messages"] = messages

        import openai

        response = self._client.chat.completions.create(**params)
        text = ""
        if response.choices:
            text = response.choices[0].message.content or ""
            if not text:
                # DeepSeek 等推理模型偶发 content 为空（思考在 reasoning_content），兜底取思考内容
                text = getattr(response.choices[0].message, "reasoning_content", None) or ""
        return SimpleNamespace(
            content=[SimpleNamespace(type="text", text=text)],
            usage=getattr(response, "usage", None),
        )

    @staticmethod
    def _normalize_usage(usage) -> dict:
        """归一化 token 用量：openai(usage) / anthropic(usage) → {prompt_tokens, completion_tokens, total_tokens}"""
        if usage is None:
            return {}
        u = {}
        for k in ("prompt_tokens", "completion_tokens", "total_tokens"):
            v = getattr(usage, k, None)
            if v is not None:
                u[k] = v
        input_tokens = getattr(usage, "input_tokens", None)
        output_tokens = getattr(usage, "output_tokens", None)
        if input_tokens is not None:
            u["prompt_tokens"] = input_tokens
        if output_tokens is not None:
            u["completion_tokens"] = output_tokens
        if "total_tokens" not in u and ("prompt_tokens" in u or "completion_tokens" in u):
            u["total_tokens"] = u.get("prompt_tokens", 0) + u.get("completion_tokens", 0)
        return u

    def _format_llm_error(self, e: Exception, kwargs: dict) -> str:
        """格式化 LLM 错误：附带当前网关配置（model/base_url/key掩码），401 附排查提示"""
        model = kwargs.get("model") or self._cfg.get("default_model") or "未配置"
        base_url = self._cfg.get("base_url") or "https://api.openai.com/v1（默认）"
        api_key = self._cfg.get("api_key") or ""
        if len(api_key) > 8:
            masked = f"{api_key[:4]}****{api_key[-4:]}"
        else:
            masked = "未配置或过短"

        msg = str(e)
        if "401" in msg or "invalid_key" in msg or "Invalid API Key" in msg:
            msg += "｜排查：① 复制 API Key 时是否带入多余空格/换行 ② Key 是否与 base_url 对应的是同一服务商（不同服务商 Key 不通用）③ Key 是否过期或未开通模型访问权限"

        return f"{msg}（当前AI网关配置：provider={self._cfg.get('provider')}，model={model}，base_url={base_url}，api_key={masked}）"
