"""
TTS 服务 - 优先使用有道词典发音，其次 Free Dictionary API，最后 mimo-V2.5-tts
"""
import os
import base64
import requests
from urllib.parse import quote


class TTSService:
    """TTS 语音合成服务"""

    def __init__(self):
        self._mimo_client = None
        self.audio_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
            "uploads", "audio", "words"
        )
        os.makedirs(self.audio_dir, exist_ok=True)

    def _get_mimo_client(self):
        if self._mimo_client is None:
            from openai import OpenAI
            import json
            config_file = os.path.join(
                os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
                "config", "llm.json"
            )
            api_key = ""
            if os.path.exists(config_file):
                with open(config_file) as f:
                    config = json.load(f)
                api_key = config.get("api_key", "")
            self._mimo_client = OpenAI(
                api_key=api_key,
                base_url="https://token-plan-cn.xiaomimimo.com/v1"
            )
        return self._mimo_client

    def get_word_info(self, word: str) -> dict:
        """
        从 Free Dictionary API 获取单词信息

        Returns:
            dict: {"phonetic": str, "audio_url": str} 或 None
        """
        try:
            resp = requests.get(
                f"https://api.dictionaryapi.dev/api/v2/entries/en/{quote(word)}",
                timeout=10
            )
            if resp.status_code != 200:
                return None

            data = resp.json()[0]
            phonetic = data.get("phonetic", "")
            audio_url = ""

            # 优先选 US 发音
            for p in data.get("phonetics", []):
                if p.get("audio") and "us" in p["audio"]:
                    audio_url = p["audio"]
                    break
            if not audio_url:
                for p in data.get("phonetics", []):
                    if p.get("audio"):
                        audio_url = p["audio"]
                        break

            return {
                "phonetic": phonetic or "",
                "audio_url": audio_url or "",
            }
        except Exception:
            return None

    def _get_youdao_audio(self, word: str):
        """
        从有道词典下载美式发音音频（国内稳定，无需 API Key）

        Args:
            word: 英文单词

        Returns:
            bytes: 音频内容 或 None
        """
        try:
            url = f"https://dict.youdao.com/dictvoice?type=1&audio={quote(word)}"
            resp = requests.get(
                url,
                timeout=10,
                headers={"User-Agent": "Mozilla/5.0"}
            )
            ctype = resp.headers.get("content-type", "")
            if resp.status_code == 200 and ctype.startswith("audio") and len(resp.content) > 500:
                return resp.content
            return None
        except Exception:
            return None

    def generate_word_audio(self, word: str) -> str:
        """
        生成单词音频，返回本地文件路径

        优先有道词典，其次 Free Dictionary API，最后用 mimo TTS 生成

        Args:
            word: 英文单词

        Returns:
            str: 音频文件绝对路径
        """
        cache_path = os.path.join(self.audio_dir, f"{word.lower()}.wav")
        if os.path.exists(cache_path):
            return cache_path

        # 方案1: 有道词典下载 MP3（国内稳定）
        try:
            audio_bytes = self._get_youdao_audio(word)
            if audio_bytes:
                mp3_path = os.path.join(self.audio_dir, f"{word.lower()}.mp3")
                with open(mp3_path, "wb") as f:
                    f.write(audio_bytes)
                return mp3_path
        except Exception:
            pass

        # 方案2: Free Dictionary API 下载 MP3
        info = self.get_word_info(word)
        if info and info["audio_url"]:
            try:
                resp = requests.get(info["audio_url"], timeout=15)
                if resp.status_code == 200 and len(resp.content) > 100:
                    # MP3 直接保存为 .mp3
                    mp3_path = os.path.join(self.audio_dir, f"{word.lower()}.mp3")
                    with open(mp3_path, "wb") as f:
                        f.write(resp.content)
                    return mp3_path
            except Exception:
                pass

        # 方案3: mimo TTS fallback
        try:
            client = self._get_mimo_client()
            completion = client.chat.completions.create(
                model="mimo-v2.5-tts",
                messages=[
                    {"role": "user", "content": "Clear, slow, standard American English pronunciation. Neutral tone."},
                    {"role": "assistant", "content": word}
                ],
                audio={"format": "wav", "voice": "Chloe"},
                timeout=30,
            )
            message = completion.choices[0].message
            if not hasattr(message, 'audio') or not message.audio:
                raise Exception("TTS API 未返回音频数据")

            audio_bytes = base64.b64decode(message.audio.data)
            with open(cache_path, "wb") as f:
                f.write(audio_bytes)
            return cache_path
        except Exception as e:
            print(f"[TTS] 生成音频失败 ({word}): {e}")
            raise


# 全局单例
tts_service = TTSService()
