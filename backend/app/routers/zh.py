"""低年级辅助：中文拼音转换接口（pypinyin 本地转换，带内存缓存）"""
from fastapi import APIRouter, Query
from pypinyin import pinyin, Style

router = APIRouter(prefix="/api/zh", tags=["zh"])

# 简单内存缓存：text -> 拼音串（文本短、量小，会话级缓存足够）
_pinyin_cache = {}


def _convert(text: str) -> str:
    cached = _pinyin_cache.get(text)
    if cached is not None:
        return cached
    # TONE 风格：带声调；多音字按常见读音（heteronym=False）
    parts = [p[0] for p in pinyin(text, style=Style.TONE, heteronym=False)]
    result = " ".join(parts)
    if len(_pinyin_cache) > 2000:
        _pinyin_cache.clear()
    _pinyin_cache[text] = result
    return result


@router.get("/pinyin")
def get_pinyin(
    texts: str = Query(..., description="要注音的文本，多个用英文逗号分隔（如：老师,书包,猫）"),
):
    """批量中文 → 拼音（带声调）。非中文部分原样保留。"""
    items = [t.strip() for t in texts.split(",") if t.strip()]
    result = {}
    for t in items:
        result[t] = _convert(t)
    return {"texts": result}
