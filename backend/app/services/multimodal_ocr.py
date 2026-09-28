import os
import json
import base64
from typing import Optional

# 默认 OCR 提示词：整页文字识别（保持排版）
DEFAULT_OCR_PROMPT = (
    "请识别图片中的所有文字，保持原有格式和排版。"
    "如果图片中有数学公式、符号等，请准确识别并用标准格式表示。"
    "直接输出识别结果，不需要其他说明。"
)


def load_config() -> dict:
    """从config/ocr.json加载配置"""
    config_file = "config/ocr.json"
    if os.path.exists(config_file):
        with open(config_file) as f:
            return json.load(f)
    return {}


class MultimodalOCRService:
    """多模态模型OCR服务（订阅制改造）

    凭据统一走平台 AI 网关（运营后台配置 Key/BaseURL），用户侧只保存模型名
    （config/ocr.json 的 multimodal_model）。网关 provider 决定协议：
      - openai    → OpenAI 兼容协议（chat.completions + image_url data URL），
                    适用于 OpenAI / Qwen-VL（DashScope 兼容模式）等
      - anthropic → Anthropic Messages API（image block）
    """

    def __init__(self):
        self._config = load_config()
        self._available = self._check_available()

    def _gateway(self) -> dict:
        """读取 AI 网关配置（实时生效）：按用户选择的视觉厂商（ocr.json vendor）解析，
        未选厂商时走默认厂商/旧单配置"""
        from app.services.ai_gateway import resolve_gateway_config
        vendor = (self._config.get("vendor") or "").strip()
        return resolve_gateway_config(vendor or None)

    def _check_available(self) -> bool:
        # 网关已配置 Key 即可用（用户不再自行配置 Key）
        return bool(self._gateway().get("api_key"))

    @property
    def is_available(self) -> bool:
        # 每次检查时重新加载配置
        self._config = load_config()
        return self._check_available()

    def recognize(self, image_path: str, prompt: Optional[str] = None) -> dict:
        """
        使用多模态模型识别图片文字

        Args:
            image_path: 本地图片路径
            prompt: 自定义提示词（用于结构化抽取等场景），默认整页文字识别

        Returns:
            dict: {
                "full_text": str,
                "blocks": list,
                "provider": str,
                "model": str,
            }
        """
        # 重新加载配置
        self._config = load_config()
        gateway = self._gateway()

        if not gateway.get("api_key"):
            return {
                "full_text": "",
                "blocks": [],
                "warning": "Multimodal OCR unavailable: AI 网关未配置 Key，请联系运营在后台配置 AI 网关。",
                "provider": "multimodal",
                "model": "",
            }

        # 模型：必须来自该厂商「视觉模型」列表；vision_models 留空 = 厂商不支持 OCR（纯文本厂商如 DeepSeek）
        vision = gateway.get("vision_models") or []
        model = (self._config.get("multimodal_model") or "").strip()
        if not vision:
            return {
                "full_text": "",
                "blocks": [],
                "warning": "当前厂商未配置视觉模型，不支持多模态 OCR。请联系运营在「AI 模型市场」为该厂商填写视觉模型，或改选其他视觉厂商。",
                "provider": "multimodal",
                "model": model,
            }
        if not model:
            model = vision[0]
        elif model not in vision:
            return {
                "full_text": "",
                "blocks": [],
                "warning": f"所选模型「{model}」不在该厂商视觉模型列表（{'、'.join(vision)}），请在家长中心重新选择。",
                "provider": "multimodal",
                "model": model,
            }
        provider = gateway.get("provider", "openai")

        try:
            if provider == "anthropic":
                return self._recognize_anthropic(image_path, prompt, gateway, model)
            return self._recognize_openai_compat(image_path, prompt, gateway, model)
        except Exception as e:
            return {"full_text": "", "blocks": [], "error": str(e), "provider": "multimodal", "model": model}

    def _read_image_base64(self, image_path: str) -> str:
        with open(image_path, 'rb') as f:
            return base64.b64encode(f.read()).decode()

    def _recognize_openai_compat(self, image_path: str, prompt: Optional[str], gateway: dict, model: str) -> dict:
        """OpenAI 兼容协议（OpenAI / Qwen-VL 等）"""
        prompt = prompt or DEFAULT_OCR_PROMPT
        from openai import OpenAI

        client = OpenAI(
            api_key=gateway["api_key"],
            base_url=gateway.get("base_url") or None,
        )

        base64_image = self._read_image_base64(image_path)

        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{base64_image}"
                            }
                        }
                    ]
                }
            ],
            max_tokens=4096,
        )

        full_text = response.choices[0].message.content
        return {
            "full_text": full_text,
            "blocks": [{"text": line.strip()} for line in full_text.split('\n') if line.strip()],
            "provider": "multimodal",
            "model": model,
        }

    def _recognize_anthropic(self, image_path: str, prompt: Optional[str], gateway: dict, model: str) -> dict:
        """Anthropic Messages API（Claude Vision）"""
        prompt = prompt or DEFAULT_OCR_PROMPT
        import anthropic

        client_kwargs = {"api_key": gateway["api_key"]}
        if gateway.get("base_url"):
            client_kwargs["base_url"] = gateway["base_url"]
        client = anthropic.Anthropic(**client_kwargs)

        with open(image_path, 'rb') as f:
            image_data = base64.b64encode(f.read()).decode()

        response = client.messages.create(
            model=model,
            max_tokens=4096,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "image",
                            "source": {
                                "type": "base64",
                                "media_type": "image/jpeg",
                                "data": image_data,
                            }
                        },
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        )

        full_text = response.content[0].text
        return {
            "full_text": full_text,
            "blocks": [{"text": line.strip()} for line in full_text.split('\n') if line.strip()],
            "provider": "multimodal",
            "model": model,
        }


# 全局单例
multimodal_ocr_service = MultimodalOCRService()
