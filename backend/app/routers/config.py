from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import json
import os
from app.config import get_settings

router = APIRouter(prefix="/api/config", tags=["配置"])
settings = get_settings()


class OCRConfig(BaseModel):
    provider: str
    baidu_api_key: Optional[str] = ""
    baidu_secret_key: Optional[str] = ""
    tencent_app_id: Optional[str] = ""
    tencent_secret_id: Optional[str] = ""
    tencent_secret_key: Optional[str] = ""
    tencent_bucket: Optional[str] = ""
    # 多模态OCR：订阅制只保存用户选择的模型名（凭据由平台 AI 网关统一提供）
    multimodal_model: Optional[str] = ""
    # AI 模型市场：选择的厂商（vendor）；空=网关默认厂商
    vendor: Optional[str] = ""


class LLMConfig(BaseModel):
    model: str = ""
    # AI 模型市场：选择的厂商（vendor）；空=网关默认厂商
    vendor: str = ""


class CustomOCRConfig(BaseModel):
    api_url: str
    method: str = "POST"
    headers: str = ""
    body_template: str = ""
    response_parser: str = ""


class AppConfig(BaseModel):
    """应用级默认配置（如默认年级）"""
    default_grade: Optional[int] = None
    default_semester: Optional[int] = None


def _providers_public() -> list:
    """厂商公开信息（学生端下拉用）：只含启用厂商，不含 Key"""
    from app.services.ai_gateway import list_providers

    out = []
    for p in list_providers(enabled_only=True):
        out.append({
            "vendor": p["vendor"],
            "name": p["name"],
            "models": p["models"],
            "vision_models": p["vision_models"],
            "is_default": p["is_default"],
        })
    return out


@router.get("/ocr")
def get_ocr_config():
    """获取OCR配置（订阅制：多模态OCR不再暴露 Key/提供商，只返回可选模型名；凭据由平台 AI 网关统一提供）"""
    from app.services.ai_gateway import list_available_models, get_gateway_config

    gateway = get_gateway_config()
    config_file = "config/ocr.json"
    if os.path.exists(config_file):
        with open(config_file) as f:
            data = json.load(f)
    else:
        data = {
            "provider": settings.OCR_PROVIDER,
            "baidu_api_key": settings.BAIDU_API_KEY,
            "baidu_secret_key": settings.BAIDU_SECRET_KEY,
            "tencent_app_id": settings.TENCENT_APP_ID,
            "tencent_secret_id": settings.TENCENT_SECRET_ID,
            "tencent_secret_key": settings.TENCENT_SECRET_KEY,
            "tencent_bucket": settings.TENCENT_BUCKET,
        }
    # 剔除订阅制改造前的遗留多模态字段（含旧 Key，不得回传前端）
    for legacy in (
        "multimodal_provider",
        "openai_api_key",
        "openai_vision_model",
        "anthropic_api_key",
        "claude_vision_model",
        "qwen_api_key",
        "qwen_vision_model",
    ):
        data.pop(legacy, None)
    # 注入网关模型列表供前端下拉（用户只选模型名，Key 在运营后台）
    data["multimodal_models"] = list_available_models()
    data["multimodal_default_model"] = gateway["default_model"]
    data["gateway_configured"] = bool(gateway["api_key"])
    # AI 模型市场：视觉厂商列表（vision_models 非空）+ 用户已选 vendor
    data["multimodal_providers"] = [p for p in _providers_public() if p["vision_models"]]
    data["multimodal_vendor"] = str(data.get("vendor", ""))
    data["vendor"] = str(data.get("vendor", ""))
    return data


@router.post("/ocr")
def save_ocr_config(config: OCRConfig):
    """保存OCR配置"""
    os.makedirs("config", exist_ok=True)
    config_file = "config/ocr.json"
    with open(config_file, 'w') as f:
        json.dump(config.model_dump(), f, indent=2)
    return {"message": "OCR配置已保存"}


@router.get("/llm")
def get_llm_config():
    """获取LLM配置：模型列表 + 当前选择（订阅制，不暴露任何 Key/BaseURL）"""
    from app.services.ai_gateway import list_available_models, get_gateway_config

    gateway = get_gateway_config()
    current = ""
    vendor = ""
    if os.path.exists("config/llm.json"):
        with open("config/llm.json") as f:
            cfg = json.load(f)
            current = cfg.get("model", "")
            vendor = cfg.get("vendor", "")
    return {
        "model": current,
        "vendor": vendor,
        "models": list_available_models(),
        "default_model": gateway["default_model"],
        "gateway_configured": bool(gateway["api_key"]),
        "providers": _providers_public(),
    }


@router.post("/llm")
def save_llm_config(config: LLMConfig):
    """保存LLM配置：只保存用户选择的厂商+模型名（Key/BaseURL 由平台 AI 网关统一提供）"""
    from app.services.ai_gateway import list_available_models, resolve_gateway_config

    model = (config.model or "").strip()
    vendor = (config.vendor or "").strip()
    if vendor:
        cfg = resolve_gateway_config(vendor)
        models = cfg.get("models") or list_available_models()
    else:
        models = list_available_models()
    if model and models and model not in models:
        raise HTTPException(status_code=400, detail=f"未知模型：{model}，可选：{'、'.join(models)}")
    os.makedirs("config", exist_ok=True)
    config_file = "config/llm.json"
    with open(config_file, 'w') as f:
        json.dump({"model": model, "vendor": vendor}, f, indent=2)
    return {"message": "LLM配置已保存", "model": model, "vendor": vendor}


@router.get("/models")
def get_llm_models():
    """获取可用模型列表（订阅制：用户只需选模型名，无需配置 Key；含多厂商下拉数据）"""
    from app.services.ai_gateway import list_available_models, get_gateway_config

    gateway = get_gateway_config()
    providers = _providers_public()
    default_vendor = ""
    if providers:
        default_vendor = next((p["vendor"] for p in providers if p["is_default"]), providers[0]["vendor"])
    return {
        "models": list_available_models(),
        "default_model": gateway["default_model"],
        "providers": providers,
        "default_vendor": default_vendor,
    }


@router.get("/custom-ocr")
def get_custom_ocr_config():
    """获取自定义OCR配置"""
    config_file = "config/custom_ocr.json"
    if os.path.exists(config_file):
        with open(config_file) as f:
            return json.load(f)
    return {
        "api_url": "",
        "method": "POST",
        "headers": "{}",
        "body_template": '{"image": "${base64_image}"}',
        "response_parser": "response.text || response.data",
    }


@router.post("/custom-ocr")
def save_custom_ocr_config(config: CustomOCRConfig):
    """保存自定义OCR配置"""
    os.makedirs("config", exist_ok=True)
    config_file = "config/custom_ocr.json"
    with open(config_file, 'w') as f:
        json.dump(config.model_dump(), f, indent=2)
    return {"message": "自定义OCR配置已保存"}


@router.get("/app")
def get_app_config():
    """获取应用配置（默认年级/学期）"""
    config_file = "config/app.json"
    if os.path.exists(config_file):
        with open(config_file) as f:
            return json.load(f)
    return {"default_grade": None, "default_semester": None}


@router.post("/app")
def save_app_config(config: AppConfig):
    """保存应用配置（默认年级/学期）"""
    os.makedirs("config", exist_ok=True)
    config_file = "config/app.json"
    with open(config_file, 'w') as f:
        json.dump(config.model_dump(), f, indent=2)
    return {"message": "应用配置已保存", "data": config.model_dump()}
