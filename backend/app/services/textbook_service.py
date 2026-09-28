"""教材同步导入服务

流程：内置目录（backend/data/textbooks/index.json）→ 按需下载 PDF → RapidOCR 提取文本
→ LLM 按单元提取知识点（带 grade/semester/chapter）→ 入库 knowledge_point

下载源（多源容错）：
  - freepep：https://p.20190723.xyz 直链（人教版小学全科，国内可直连）
  - chinatx：GitHub raw → ghproxy 等镜像依次尝试
全部失败 → 降级手动放置（data/textbooks/<版本>/<科目>/<年级><学期>.pdf + 扫描导入）
"""
import json
import os
import re
import threading
import time
import urllib.parse
import uuid

import requests

from app.database import SessionLocal
from app.models import KnowledgePoint, Subject
from app.services.llm import LLMService

BACKEND_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # backend/
DATA_DIR = os.path.join(BACKEND_DIR, "data", "textbooks")
INDEX_PATH = os.path.join(DATA_DIR, "index.json")

# GitHub raw 镜像列表（依次尝试；2026 年常见可用镜像，可在部署机按需增删）
GH_MIRRORS = [
    "https://gh-proxy.com/",
    "https://ghfast.top/",
    "https://ghproxy.net/",
]

# 单元标题正则：第X单元 / 第X章 / Unit N
UNIT_RE = re.compile(r"第\s*[一二三四五六七八九十百0-9]+\s*(?:单元|章)", re.I)
UNIT_RE_EN = re.compile(r"\bunit\s*\d+", re.I)

GRADE_CN = {"一年级": 1, "二年级": 2, "三年级": 3, "四年级": 4, "五年级": 5, "六年级": 6,
            "初一": 7, "初二": 8, "初三": 9, "高一": 10, "高二": 11, "高三": 12}
SEMESTER_CN = {"上册": 1, "下册": 2, "全一册": 1}

UA = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) EasyFix-textbook-importer"}

# ---------------------------------------------------------------- 目录

_INDEX_CACHE = None
_INDEX_LOCK = threading.Lock()


def get_index() -> dict:
    """读取内置教材目录（进程内缓存）"""
    global _INDEX_CACHE
    if _INDEX_CACHE is not None:
        return _INDEX_CACHE
    with _INDEX_LOCK:
        if _INDEX_CACHE is None:
            if not os.path.exists(INDEX_PATH):
                raise RuntimeError("教材目录缺失，请先运行教材目录生成脚本 _build_textbook_index.py 生成 backend/data/textbooks/index.json")
            with open(INDEX_PATH, encoding="utf-8") as f:
                _INDEX_CACHE = json.load(f)
    return _INDEX_CACHE


def _safe_name(name: str, fallback: str = "未分类") -> str:
    """目录名清洗：去掉 Windows 非法字符；空值用兜底名（保证目录能被创建）"""
    name = re.sub(r'[\\/:*?"<>|\r\n\t]', "_", (name or "").strip())
    return name.strip(" .") or fallback


def manual_dir(version: str, subject: str) -> str:
    """手动放置目标文件夹：data/textbooks/<版本>/<科目>"""
    return os.path.join(DATA_DIR, _safe_name(version), _safe_name(subject))


def manual_pdf_path(version: str, subject: str, grade: str = "", semester: str = "") -> str:
    """手动放置目标文件名：<版本>/<科目>/<年级><册次>.pdf（年级册次未知时退回 <版本>/<科目>/手动放置.pdf）"""
    fn = f"{(grade or '').strip()}{(semester or '').strip()}".strip()
    if not fn:
        fn = "手动放置"
    return os.path.join(manual_dir(version, subject), f"{fn}.pdf")


def _open_path(path: str) -> None:
    """在系统文件管理器中打开路径（非 Windows / 失败时静默忽略）"""
    try:
        os.startfile(path)  # Windows
    except Exception:
        pass


def ensure_manual_dir(version: str, subject: str, grade: str = "", semester: str = "",
                      open_explorer: bool = False) -> dict:
    """创建（并可选打开）当前选择对应的手动放置文件夹，返回前后端共用的路径信息"""
    d = manual_dir(version, subject)
    pdf = manual_pdf_path(version, subject, grade, semester)
    if version or subject:  # 未选版本/科目时不建目录，避免产出 未分类/未分类 垃圾文件夹
        os.makedirs(d, exist_ok=True)
        if open_explorer:
            _open_path(d)
    return {
        "dir": d,                                               # 绝对目录
        "dir_rel": os.path.relpath(d, BACKEND_DIR).replace(os.sep, "/"),  # data/textbooks/<版本>/<科目>
        "pdf_path": pdf,                                        # 绝对文件路径
        "pdf_name": os.path.basename(pdf),                      # <年级><册次>.pdf
        "exists": os.path.exists(pdf),                          # 该 PDF 是否已放入
        "opened": bool(open_explorer),
    }


def book_pdf_path(book: dict) -> str:
    return manual_pdf_path(book.get("version"), book.get("subject"),
                           book.get("grade"), book.get("semester"))


def book_txt_path(book: dict) -> str:
    return os.path.splitext(book_pdf_path(book))[0] + ".txt"


def get_catalog() -> dict:
    """返回教材目录（扁平 books 列表 + 本地下载状态）"""
    index = get_index()
    books = []
    for b in index.get("books", []):
        item = {k: b.get(k) for k in ("stage", "subject", "version", "grade", "semester")}
        item["downloads"] = [
            {"source": d.get("source"), "url": d.get("url", ""), "size": d.get("size")}
            for d in b.get("downloads", [])
        ]
        item["local"] = os.path.exists(book_pdf_path(b))
        item["local_only"] = bool(b.get("local_only")) or not item["downloads"]
        books.append(item)
    return {"total": len(books), "generatedAt": index.get("generatedAt"), "books": books}


# ---------------------------------------------------------------- 下载

def _download_with_progress(url: str, dest: str, task: dict, timeout: int = 120) -> None:
    """流式下载到 dest，进度写入 task（progress 0-100 内相对段）"""
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    tmp = dest + ".part"
    with requests.get(url, headers=UA, stream=True, timeout=timeout) as r:
        r.raise_for_status()
        total = int(r.headers.get("content-length") or 0)
        written = 0
        with open(tmp, "wb") as f:
            for chunk in r.iter_content(chunk_size=256 * 1024):
                if chunk:
                    f.write(chunk)
                    written += len(chunk)
                    if total:
                        _set_progress(task, 5 + int(written / total * 30), "downloading",
                                      f"下载中 {written // 1024 // 1024}MB / {total // 1024 // 1024}MB")
    os.replace(tmp, dest)


def download_book(book: dict, task: dict) -> str:
    """按多源顺序下载教材 PDF，返回本地路径"""
    dest = book_pdf_path(book)
    if os.path.exists(dest):
        _set_progress(task, 35, "downloading", "教材已存在，跳过下载")
        return dest
    if book.get("local_only") or not book.get("downloads"):
        os.makedirs(os.path.dirname(dest), exist_ok=True)  # 先把目标文件夹建好，方便用户直接放文件
        raise RuntimeError("该版本暂无在线资源。请手动下载教材 PDF 后放入 " +
                           os.path.dirname(dest) + " 文件夹，再点「扫描本地 PDF」导入")
    errors = []
    for src in book.get("downloads", []):
        source = src.get("source")
        if source == "freepep":
            url = src.get("url")
            try:
                _download_with_progress(url, dest, task)
                _set_progress(task, 35, "downloading", "下载完成")
                return dest
            except Exception as e:
                errors.append(f"freepep: {e}")
                _set_progress(task, 30, "downloading", f"freepep 下载失败，尝试下一源…")
        elif source == "chinatx":
            raw = urllib.parse.quote(src.get("url", ""), safe="/:")
            candidates = [raw] + [m + raw for m in GH_MIRRORS]
            for i, url in enumerate(candidates):
                try:
                    _download_with_progress(url, dest, task, timeout=60)
                    _set_progress(task, 35, "downloading", f"下载完成（{url.split('/')[2]}）")
                    return dest
                except Exception as e:
                    errors.append(f"{url[:60]}: {e}")
    raise RuntimeError("所有下载源均失败：" + "; ".join(errors[-3:]) +
                       "。请手动下载教材 PDF 放到 " + os.path.dirname(dest) + " 后重试")


# ---------------------------------------------------------------- 多模态识别（优先；模型市场视觉厂商）

def _vision_key_valid(cfg: dict) -> bool:
    """检测模型市场厂商 key 有效性：GET {base_url}/models（openai/anthropic 兼容均支持）"""
    base = (cfg.get("base_url") or "").rstrip("/")
    if not base:
        base = "https://api.openai.com/v1" if cfg.get("provider") != "anthropic" else "https://api.anthropic.com/v1"
    url = f"{base}/models"
    headers = {"Authorization": f"Bearer {cfg.get('api_key', '')}"}
    try:
        r = requests.get(url, headers=headers, timeout=10)
        return r.status_code == 200
    except Exception:
        return False


def _resolve_vision_gateway() -> dict:
    """检测模型市场是否配置可用多模态模型（vision_models 非空 + enabled + key 有效）。

    任一厂商通过 → 返回其网关配置（含 vision_models）；
    未配置 / key 均无效 → None（调用方降级本地 OCR）。
    """
    from app.services.ai_gateway import resolve_gateway_config, list_providers
    try:
        for p in list_providers(enabled_only=True):
            if not p.get("vision_models"):
                continue
            cfg = resolve_gateway_config(p.get("vendor"))
            if not cfg or not cfg.get("api_key"):
                continue
            if _vision_key_valid(cfg):
                print(f"[textbook] 多模态识别使用厂商 {p.get('vendor')}（{cfg['vision_models'][0]}）")
                return cfg
            print(f"[textbook] 多模态厂商 {p.get('vendor')} key 无效，尝试下一候选…")
    except Exception as e:
        print(f"[textbook] 多模态检测失败: {e}")
    return None


def _page_to_png_base64(page) -> str:
    """PyMuPDF 页面 → PNG(base64)"""
    import base64 as _b64
    pix = page.get_pixmap(dpi=200)
    return _b64.b64encode(pix.tobytes("png")).decode("ascii")


def _vision_page_text(cfg: dict, page) -> str:
    """单页 → 多模态模型识别页面文字（openai 兼容 / anthropic 两种 content 格式）"""
    from app.services.ai_gateway import AIGatewayClient
    model = cfg["vision_models"][0]
    img_b64 = _page_to_png_base64(page)
    text_prompt = "请识别这一页教材的全部文字，按阅读顺序逐行输出。只输出识别出的文字，不要解释。"
    if cfg.get("provider") == "anthropic":
        content = [
            {"type": "image", "source": {"type": "base64", "media_type": "image/png", "data": img_b64}},
            {"type": "text", "text": text_prompt},
        ]
    else:
        content = [
            {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_b64}"}},
            {"type": "text", "text": text_prompt},
        ]
    client = AIGatewayClient(cfg)
    resp = client.chat(model=model, messages=[{"role": "user", "content": content}],
                       max_tokens=1200, timeout=90, caller="textbook-vision")
    text = resp.content[0].text if hasattr(resp.content[0], "text") else str(resp.content[0])
    return (text or "").strip()


def _mm_txt_path(txt_path: str) -> str:
    """多模态文本缓存：与本地 OCR 文本缓存分开（识别方式不同，避免互相覆盖）"""
    return os.path.splitext(txt_path)[0] + ".mm.txt"


_PAGE_MARK = re.compile(r"^---\s*第\s*(\d+)\s*页\s*---\s*$")


def _split_pages(full_text: str, limit: int = None) -> list:
    """OCR 全文 → [(pdf_page_no, text)]（按「--- 第N页 ---」标记切分；limit 只取前 N 段）"""
    parts = []
    cur_page = None
    cur_lines = []
    for line in full_text.splitlines():
        m = _PAGE_MARK.match(line.strip())
        if m:
            if cur_page is not None:
                parts.append((cur_page, "\n".join(cur_lines)))
            cur_page = int(m.group(1))
            cur_lines = []
            if limit and len(parts) >= limit:
                break
        elif cur_page is not None:
            cur_lines.append(line)
    if cur_page is not None:
        parts.append((cur_page, "\n".join(cur_lines)))
    return parts


def _toc_from_text(full_text: str) -> list:
    """目录页优先定位：取前 6 页文本，LLM 判断是否为目录页并解析单元→PDF页号。

    返回 [{"unit": str, "page": int}]；无目录 / 解析失败 → None（回退正则/全册）。
    兼容 OCR 质量差的目录页（可能没有「目录」二字，靠词条+页码模式判断）。
    """
    pages = _split_pages(full_text, limit=6)
    joined = "\n".join(f"--- 第{p}页 ---\n{t}" for p, t in pages if t.strip())
    if not joined.strip() or len(joined.strip()) < 200:
        return None
    prompt = (
        "以下是小学教材开头几页的识别文本（扫描件 OCR，可能有错字/漏字），每页以「--- 第N页 ---」标记 PDF 物理页号。\n"
        "请判断其中是否有「目录/目」页：目录页特征是若干「词条+页码」列表（如「混合运算 2」、"
        "「Unit 1 Hello 3」；OCR 常把多条目挤成一行，如「目 混合运算 2 观察物体 13 三 加与减 17」）。\n"
        "若存在目录：列出每个单元/章节及其起始页码。目录行写的页码是书本页码，请结合识别文本上下文"
        "换算为 PDF 物理页号（物理页号 = 「--- 第N页 ---」标记的页号，通常比书本页码大 0~5）。\n"
        "若不存在目录：输出空数组。\n"
        "只输出 JSON：{\"units\":[{\"unit\":\"第一单元 混合运算\",\"page\":3}]}\n"
        f"识别文本：\n{joined}"
    )
    try:
        content = _llm_json(prompt, max_tokens=1500)
        data = _parse_json(content)
        entries = data.get("units", []) if isinstance(data, dict) else []
        result = []
        for e in entries:
            if not isinstance(e, dict):
                continue
            unit = str(e.get("unit") or e.get("title") or "").strip()
            try:
                page = int(e.get("page") or 0)
            except (TypeError, ValueError):
                page = 0
            if unit and page > 0:
                result.append({"unit": unit, "page": page})
        if not result:
            print("[textbook] 目录解析无有效条目")
            return None
        return result
    except Exception as e:
        print(f"[textbook] 目录定位失败: {e}")
        return None


def split_units_from_toc(full_text: str, toc: list) -> list:
    """按目录页码清单切分 OCR 文本（多模态/本地均可），返回 [(chapter, body)]"""
    page_idx = {}
    for i, line in enumerate(full_text.splitlines()):
        m = _PAGE_MARK.match(line.strip())
        if m:
            page_idx[int(m.group(1))] = i
    if not page_idx:
        return []
    entries = sorted(toc, key=lambda e: e["page"])
    units = []
    for j, e in enumerate(entries):
        start_i = page_idx.get(e["page"])
        if start_i is None:
            print(f"[textbook] 目录页号 {e['page']} 不在 OCR 文本中，跳过「{e['unit']}」")
            continue
        end_i = None
        for p, i in sorted(page_idx.items()):
            if i > start_i:
                if j + 1 < len(entries):
                    if p >= entries[j + 1]["page"]:
                        end_i = i
                        break
                else:
                    end_i = i
                    break
        if end_i is None:
            end_i = len(full_text.splitlines())
        body = "\n".join(full_text.splitlines()[start_i + 1:end_i]).strip()
        if body:
            units.append((e["unit"], body))
    return units


def _infer_units_llm(text: str) -> list:
    """本地 OCR 无单元标题行时，LLM 推断单元标题清单（兜底）"""
    sample = text[:6000] + "\n……（中略）……\n" + text[-2000:]
    prompt = (
        "以下是一本小学数学教材的 OCR 识别文本（可能有少量错字/缺漏）。"
        "请按单元/章节结构列出本书全部单元的标题（如「第一单元 混合运算」「五 周长」「总复习」），"
        "保持教材原文的叫法，按先后顺序输出。\n"
        "只输出 JSON：{\"units\":[\"第一单元 时、分、秒\",\"Unit 1 Hello!\", ...]}\n"
        f"文本样本：\n{sample}"
    )
    try:
        content = _llm_json(prompt, max_tokens=1500)
        data = _parse_json(content)
        units = data.get("units", []) if isinstance(data, dict) else []
        return [str(u).strip() for u in units if str(u).strip()]
    except Exception as e:
        print(f"[textbook] LLM 推断单元失败: {e}")
        return []


def _match_unit_line(lines: list, title: str) -> int:
    """在 OCR 行中定位单元标题行（模糊：去空白后前 4 字开头或包含；跳过页码/页脚短行）"""
    t = re.sub(r"\s+", "", title)
    t4 = t[:4]
    for i, line in enumerate(lines):
        l = re.sub(r"\s+", "", line)
        if not l:
            continue
        # 页码/纯符号行跳过（OCR 常见页脚噪音）
        if re.fullmatch(r"[\d\s\-—–.:：·、%xX×]+", l):
            continue
        if len(t4) >= 2 and l.startswith(t4) and len(l) < 100:
            return i
        if len(t) >= 4 and t in l and len(l) < 100:
            return i
    return -1


# ---------------------------------------------------------------- OCR

_ocr_instance = None
_ocr_lock = threading.Lock()


def _get_ocr():
    global _ocr_instance
    if _ocr_instance is None:
        with _ocr_lock:
            if _ocr_instance is None:
                from rapidocr_onnxruntime import RapidOCR
                _ocr_instance = RapidOCR()
    return _ocr_instance


def _page_to_text(ocr, page) -> str:
    """PyMuPDF 渲染页面 → RapidOCR 识别 → 按行拼接文本"""
    import numpy as np
    pix = page.get_pixmap(dpi=200)
    img = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.width, pix.n)
    if pix.n == 4:
        img = img[:, :, :3]
    result, _ = ocr(img)
    if not result:
        return ""
    # 按 y 坐标分桶排序，近似阅读顺序
    lines = {}
    for box, text, score in result:
        y = int(round(box[0][1]))
        key = y // 12  # 12px 容差分桶
        lines.setdefault(key, []).append((box[0][0], text))
    ordered = []
    for key in sorted(lines):
        for x, text in sorted(lines[key], key=lambda t: t[0]):
            ordered.append(text)
    return " ".join(ordered)


def image_to_text(img_path: str) -> str:
    """单张图片 → RapidOCR → 按行拼接文本（公共 OCR 基础设施，供单词提取等复用）"""
    import numpy as np
    from PIL import Image
    ocr = _get_ocr()
    img = np.array(Image.open(img_path).convert("RGB"))
    result, _ = ocr(img)
    if not result:
        return ""
    lines = {}
    for box, text, score in result:
        y = int(round(box[0][1]))
        key = y // 12  # 12px 容差分桶
        lines.setdefault(key, []).append((box[0][0], text))
    ordered = []
    for key in sorted(lines):
        for x, text in sorted(lines[key], key=lambda t: t[0]):
            ordered.append(text)
    return " ".join(ordered)


def extract_text(pdf_path: str, txt_path: str, task: dict, vision_cfg: dict = None) -> str:
    """PDF → 文本，缓存到 txt_path，返回全文。

    vision_cfg 提供时走多模态逐页识别（缓存 .mm.txt，与本地 OCR 分开）；
    否则本地 RapidOCR 逐页识别。
    """
    if vision_cfg:
        mm_path = _mm_txt_path(txt_path)
        if os.path.exists(mm_path):
            _set_progress(task, 75, "ocr", "多模态识别文本已存在，跳过识别")
            with open(mm_path, encoding="utf-8") as f:
                return f.read()
        import fitz
        doc = fitz.open(pdf_path)
        total = doc.page_count
        parts = []
        for i, page in enumerate(doc):
            try:
                text = _vision_page_text(vision_cfg, page)
            except Exception as e:
                text = ""
                print(f"[textbook] 第{i + 1}页多模态识别失败: {e}")
            parts.append(f"--- 第{i + 1}页 ---\n{text}")
            if (i + 1) % 5 == 0 or i == total - 1:
                _set_progress(task, 35 + int((i + 1) / total * 40), "ocr",
                              f"多模态识别中 {i + 1}/{total} 页")
        doc.close()
        full = "\n".join(parts)
        os.makedirs(os.path.dirname(mm_path), exist_ok=True)
        with open(mm_path, "w", encoding="utf-8") as f:
            f.write(full)
        _set_progress(task, 75, "ocr", f"多模态识别完成，共 {total} 页")
        return full
    if os.path.exists(txt_path):
        _set_progress(task, 75, "ocr", "OCR 文本已存在，跳过识别")
        with open(txt_path, encoding="utf-8") as f:
            return f.read()
    import fitz
    ocr = _get_ocr()
    doc = fitz.open(pdf_path)
    total = doc.page_count
    parts = []
    for i, page in enumerate(doc):
        try:
            text = _page_to_text(ocr, page)
        except Exception as e:
            text = ""
            print(f"[textbook] 第{i + 1}页 OCR 失败: {e}")
        parts.append(f"--- 第{i + 1}页 ---\n{text}")
        if (i + 1) % 5 == 0 or i == total - 1:
            _set_progress(task, 35 + int((i + 1) / total * 40), "ocr",
                          f"识别中 {i + 1}/{total} 页")
    doc.close()
    full = "\n".join(parts)
    os.makedirs(os.path.dirname(txt_path), exist_ok=True)
    with open(txt_path, "w", encoding="utf-8") as f:
        f.write(full)
    _set_progress(task, 75, "ocr", f"OCR 完成，共 {total} 页")
    return full


# ---------------------------------------------------------------- LLM 提取

def _llm_json(prompt: str, system: str = "你只输出JSON，不要输出任何解释。", max_tokens: int = 2500, timeout: int = 60) -> str:
    """调用 LLM（关闭思考），返回原始文本"""
    llm = LLMService()
    resp = llm._retry_on_rate_limit(
        llm._call_messages_create,
        model=llm._get_config("model", "claude-sonnet-4-20250514"),
        max_tokens=max_tokens,
        temperature=0,
        timeout=timeout,
        # DeepSeek-flash 等推理模型默认深度思考会耗尽 max_tokens 导致空输出；
        # 通过 extra_body 关闭思考（OpenAI 兼容接口透传，anthropic 接口忽略）
        extra_body={"thinking": {"type": "disabled"}},
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    content = resp.content[0].text if hasattr(resp.content[0], "text") else str(resp.content[0])
    if not content or not content.strip():
        raise RuntimeError("LLM 返回内容为空")
    return content.strip()


def _parse_json(text: str):
    """容错解析 LLM 返回的 JSON"""
    m = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if m:
        text = m.group(1)
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        start = text.find("{")
        end = text.rfind("}") + 1
        if start != -1 and end != 0:
            try:
                return json.loads(text[start:end])
            except json.JSONDecodeError:
                pass
    raise RuntimeError("LLM 返回内容无法解析为 JSON")


def split_units(text: str) -> list:
    """按单元标题切分 OCR 全文，返回 [(chapter, body)]。

    正则优先（第X单元/第X章/Unit N）；无匹配时 LLM 推断单元标题兜底；
    推断也无法定位 → 整本作为「全册」一个章节。
    """
    lines = text.splitlines()
    # 记录单元标题行索引
    markers = []
    for i, line in enumerate(lines):
        if UNIT_RE.search(line) or UNIT_RE_EN.search(line):
            title = re.sub(r"[-—–:：\s]+", " ", line).strip()[:80]
            markers.append((i, title))
    if not markers:
        # 无单元标题：LLM 推断单元边界（本地 OCR 无目录/目录定位失败时兜底）
        inferred = _infer_units_llm(text)
        for title in inferred:
            idx = _match_unit_line(lines, title)
            if idx >= 0:
                markers.append((idx, title))
        markers.sort(key=lambda m: m[0])
        # 去重相邻
        dedup = []
        for m in markers:
            if not dedup or dedup[-1][0] != m[0]:
                dedup.append(m)
        markers = dedup
    if not markers:
        # 仍无单元标题：整本作为一个章节
        body = "\n".join(lines)
        return [("全册", body)] if body.strip() else []
    units = []
    for j, (idx, title) in enumerate(markers):
        end = markers[j + 1][0] if j + 1 < len(markers) else len(lines)
        body = "\n".join(lines[idx + 1:end]).strip()
        if body:
            units.append((title, body))
    return units


def extract_unit_points(subject: str, book_meta: str, chapter: str, body: str, task: dict) -> list:
    """LLM 提取单个单元的知识点，返回 [(name, desc)]"""
    # 超长保护：保留首尾
    if len(body) > 12000:
        body = body[:9000] + "\n……（中略）……\n" + body[-3000:]
    prompt = (
        f"你是中国小学{subject}教师。以下是一本《{book_meta}》中章节「{chapter}」的 OCR 识别文本"
        f"（扫描件识别，可能有少量错字/顺序乱，请自行判断）。\n"
        f"请提取该章节的核心知识点清单，供学生按知识点复习使用：\n"
        f"1. 每个知识点一句话说清是什么/怎么用；数学类可含公式、法则、典型结论；英语类可含词汇主题、句型、语法点。\n"
        f"2. 数量 8~20 个，宁缺毋滥，只列教材中确实出现的知识点，不要臆造。\n"
        f"3. 不要输出章节标题（由调用方提供）。\n"
        f"只输出 JSON：{{\"points\":[{{\"name\":\"知识点名\",\"desc\":\"一句话说明\"}}]}}\n"
        f"章节 OCR 文本：\n{body}"
    )
    content = _llm_json(prompt)
    data = _parse_json(content)
    points = data.get("points", [])
    result = []
    if not isinstance(points, list):
        return result
    for p in points:
        name = str(p.get("name", "")).strip()
        desc = str(p.get("desc", "")).strip()
        if name:
            result.append((name, desc))
    return result


# ---------------------------------------------------------------- 入库

def ensure_chapter_column() -> None:
    """knowledge_point 表加 chapter 列（幂等）"""
    from sqlalchemy import text as sa_text
    db = SessionLocal()
    try:
        cols = [row[1] for row in db.execute(sa_text("PRAGMA table_info(knowledge_point)")).fetchall()]
        if "chapter" not in cols:
            db.execute(sa_text("ALTER TABLE knowledge_point ADD COLUMN chapter VARCHAR(200)"))
            db.commit()
            print("[textbook] knowledge_point 表已新增 chapter 列")
    finally:
        db.close()


def get_or_create_subject(db, name: str) -> Subject:
    subj = db.query(Subject).filter(Subject.name == name, Subject.deleted == False).first()
    if not subj:
        subj = Subject(name=name)
        db.add(subj)
        db.commit()
        db.refresh(subj)
    return subj


def import_points(subject_name: str, grade_cn: str, semester_cn: str, chapter: str,
                  points: list, task: dict) -> dict:
    """知识点入库（同 subject_id+name 去重；已存在但缺 grade/semester/chapter 则补全）"""
    db = SessionLocal()
    try:
        subj = get_or_create_subject(db, subject_name)
        grade = GRADE_CN.get(grade_cn)
        semester = SEMESTER_CN.get(semester_cn)
        existing = {row.name: row for row in db.query(KnowledgePoint).filter(
            KnowledgePoint.subject_id == subj.id, KnowledgePoint.deleted == False).all()}
        imported = skipped = updated = 0
        seen = set()
        rows = []
        for name, desc in points:
            name = name.strip()
            if not name or name in seen:
                continue
            seen.add(name)
            if name in existing:
                row = existing[name]
                changed = False
                if row.grade is None and grade:
                    row.grade = grade
                    changed = True
                if row.semester is None and semester:
                    row.semester = semester
                    changed = True
                if not row.chapter and chapter:
                    row.chapter = chapter
                    changed = True
                updated += 1 if changed else 0
                if not changed:
                    skipped += 1
                continue
            rows.append(KnowledgePoint(name=name, subject_id=subj.id,
                                       grade=grade, semester=semester, chapter=chapter))
            imported += 1
        if rows:
            db.add_all(rows)
        db.commit()
        return {"imported": imported, "skipped": skipped, "updated": updated,
                "subject_id": subj.id, "subject_name": subj.name}
    finally:
        db.close()


# ---------------------------------------------------------------- 任务管理

_tasks: dict = {}
_tasks_lock = threading.Lock()
_import_lock = threading.Lock()  # 同一时间只允许一个导入任务


def _set_progress(task: dict, progress: int, stage: str, message: str) -> None:
    with _tasks_lock:
        task["progress"] = max(0, min(100, progress))
        task["stage"] = stage
        task["message"] = message
        task["updated_at"] = time.strftime("%H:%M:%S")


def get_task(task_id: str) -> dict:
    with _tasks_lock:
        t = _tasks.get(task_id)
        return dict(t) if t else None


def list_tasks() -> list:
    with _tasks_lock:
        items = sorted(_tasks.values(), key=lambda t: t.get("created_at", ""), reverse=True)
        return [dict(t) for t in items[:20]]


def _extract_and_save(task: dict, subject: str, grade: str, semester: str,
                      book_meta: str, full_text: str) -> None:
    """共用收尾：按单元切分全文 → LLM 提取知识点 → 入库 → 置 done"""
    units = split_units(full_text)
    if not units:
        raise RuntimeError("未从教材中识别出单元标题，请确认内容完整（应包含「第X单元/Unit X」）")
    _set_progress(task, 76, "extracting", f"共 {len(units)} 个单元，开始提取知识点")
    all_points = []
    for i, (chapter, body) in enumerate(units, start=1):
        _set_progress(task, 76 + int(i / len(units) * 19), "extracting",
                      f"提取知识点 {i}/{len(units)}（{chapter[:20]}…）")
        try:
            pts = extract_unit_points(subject, book_meta, chapter, body, task)
            for name, desc in pts:
                all_points.append((name, desc, chapter))
            print(f"[textbook] 单元「{chapter}」提取 {len(pts)} 个知识点")
        except Exception as e:
            print(f"[textbook] 单元「{chapter}」提取失败: {e}")
            _set_progress(task, 76 + int(i / len(units) * 19), "extracting",
                          f"单元 {i} 提取失败，跳过")
    if not all_points:
        raise RuntimeError("所有单元均未提取到知识点")
    # 入库
    _set_progress(task, 95, "importing", f"写入 {len(all_points)} 个知识点")
    ensure_chapter_column()
    result = {"points_total": len(all_points)}
    by_chapter = {}
    for name, desc, chapter in all_points:
        by_chapter.setdefault(chapter, []).append((name, desc))
    for chapter, pts in by_chapter.items():
        r = import_points(subject, grade, semester, chapter, pts, task)
        for k, v in r.items():
            if k in ("imported", "skipped", "updated"):
                result[k] = result.get(k, 0) + v
    result["units"] = len(units)
    result["chapters"] = list(by_chapter.keys())
    with _tasks_lock:
        task["result"] = result
    _set_progress(task, 100, "done", f"完成：新增 {result.get('imported', 0)}，补全 {result.get('updated', 0)}，跳过 {result.get('skipped', 0)}")
    with _tasks_lock:
        task["status"] = "done"
        task["finished_at"] = time.strftime("%H:%M:%S")


def _run_import(task: dict, book: dict, local_pdf: str = None) -> None:
    try:
        _set_progress(task, 0, "downloading", "开始导入")
        # 1. 下载 / 本地 PDF
        if local_pdf:
            pdf_path = local_pdf
            _set_progress(task, 5, "downloading", "使用本地教材")
        else:
            pdf_path = download_book(book, task)
        # 2. OCR
        txt_path = book_txt_path(book) if not local_pdf else local_pdf[:-4] + ".txt"
        full_text = extract_text(pdf_path, txt_path, task)
        # 3. 切单元 + LLM 提取 + 入库
        book_meta = f"{book.get('version', '')}{book.get('subject', '')}{book.get('grade', '')}{book.get('semester', '')}"
        _extract_and_save(task, book.get("subject", ""), book.get("grade", ""), book.get("semester", ""),
                          book_meta, full_text)
    except Exception as e:
        print(f"[textbook] 导入失败: {e}")
        with _tasks_lock:
            task["status"] = "failed"
            task["error"] = str(e)
            task["finished_at"] = time.strftime("%H:%M:%S")
        _set_progress(task, 0, "failed", str(e)[:200])


def start_import(book: dict, local_pdf: str = None) -> dict:
    """创建并启动导入任务（后台线程）。已有一个运行中任务则抛 RuntimeError"""
    if not _import_lock.acquire(blocking=False):
        raise RuntimeError("已有导入任务正在进行，请等待完成")
    task = {
        "id": uuid.uuid4().hex[:12],
        "status": "pending",
        "stage": "pending",
        "progress": 0,
        "message": "排队中",
        "book": {k: book.get(k) for k in ("stage", "subject", "version", "grade", "semester")},
        "local_pdf": bool(local_pdf),
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": "",
        "finished_at": None,
        "error": None,
        "result": None,
    }
    with _tasks_lock:
        _tasks[task["id"]] = task
        # 内存任务表只保留最近 50 个
        if len(_tasks) > 50:
            for k in sorted(_tasks, key=lambda x: _tasks[x]["created_at"])[: len(_tasks) - 50]:
                _tasks.pop(k, None)

    def _worker():
        try:
            _run_import(task, book, local_pdf)
        finally:
            _import_lock.release()

    threading.Thread(target=_worker, daemon=True).start()
    return task


# ---------------------------------------------------------------- 手动放置兜底

def scan_local(version: str = "", subject: str = "") -> list:
    """扫描 data/textbooks 下的 PDF，解析 版本/科目/年级册次.pdf 结构。

    指定 version/subject 时只扫该教材目录（data/textbooks/<版本>/<科目>），
    未指定时扫全树；目录不存在会先创建，避免首次扫描空手而归。
    """
    found = []
    if version or subject:
        root = manual_dir(version, subject)
    else:
        root = DATA_DIR
    os.makedirs(root, exist_ok=True)
    for root, dirs, files in os.walk(root):
        for fn in files:
            if not fn.lower().endswith(".pdf") or fn.endswith(".part"):
                continue
            path = os.path.join(root, fn)
            rel = os.path.relpath(path, DATA_DIR)
            parts = rel.split(os.sep)
            m = re.match(r"(.+?)\s*(\d+)\.pdf$", fn)
            entry = {
                "path": path,
                "rel": rel,
                "version": parts[0] if len(parts) > 1 else "未分类",
                "subject": parts[1] if len(parts) > 2 else "未分类",
                "grade": "",
                "semester": "",
                "size": os.path.getsize(path),
            }
            gm = re.search(r"([一二三四五六七八九十]+)年级(上|下)册", fn)
            if gm:
                entry["grade"] = gm.group(1) + "年级"
                entry["semester"] = "上册" if gm.group(2) == "上" else "下册"
            found.append(entry)
    found.sort(key=lambda x: (x["version"], x["subject"], x["grade"], x["semester"]))
    return found


def open_data_folder() -> str:
    """打开教材数据目录（返回路径）"""
    os.makedirs(DATA_DIR, exist_ok=True)
    _open_path(DATA_DIR)
    return DATA_DIR


# ---------------------------------------------------------------- 教材知识库（本地预览）

_PAGE_CACHE = {}  # (pdf_path, page) -> base64 png


def _resolve_local_book(version: str, subject: str, grade: str, semester: str) -> str:
    """按 版本/科目/年级册次 定位本地 PDF 路径（不存在返回空）"""
    if not version or not subject:
        return ""
    pdf = os.path.join(DATA_DIR, version, subject, f"{grade}{semester}.pdf")
    if os.path.exists(pdf):
        return pdf
    # 兜底：模糊匹配（手动放置可能文件名略有差异）
    d = os.path.join(DATA_DIR, version, subject)
    if os.path.isdir(d):
        for fn in os.listdir(d):
            if fn.lower().endswith(".pdf") and grade and semester and grade in fn and semester in fn:
                return os.path.join(d, fn)
    return ""


def _txt_path_for(version: str, subject: str, grade: str, semester: str) -> str:
    return os.path.join(DATA_DIR, version, subject, f"{grade}{semester}.txt")


def _parse_page_marks(text: str):
    """解析 OCR 文本的页码标记 → [(page_no, start_offset)]"""
    marks = []
    for m in re.finditer(r"^---\s*第\s*(\d+)\s*页\s*---", text, re.M):
        marks.append((int(m.group(1)), m.start()))
    return marks


def _page_of_offset(text: str, offset: int, marks: list) -> int:
    """由文本偏移量反查所在页号"""
    page = 1
    for pno, start in marks:
        if offset < start:
            break
        page = pno
    return page


def library_catalog() -> dict:
    """教材知识库：扫描本地已下载 PDF，返回书目列表"""
    books = []
    for entry in scan_local():
        books.append({
            "version": entry["version"], "subject": entry["subject"],
            "grade": entry["grade"], "semester": entry["semester"],
            "size": entry["size"],
            "ocr": os.path.exists(_txt_path_for(entry["version"], entry["subject"],
                                                entry["grade"], entry["semester"])),
        })
    return {"total": len(books), "books": books}


def preview_page(version: str, subject: str, grade: str, semester: str, page: int) -> dict:
    """渲染教材 PDF 指定页 → base64 PNG；page<=0 时返回第 1 页"""
    pdf = _resolve_local_book(version, subject, grade, semester)
    if not pdf:
        raise RuntimeError(f"本地未找到教材 {version}/{subject}/{grade}{semester}.pdf")
    if page < 1:
        page = 1
    cache_key = (pdf, page)
    if cache_key in _PAGE_CACHE:
        img_b64 = _PAGE_CACHE[cache_key]
        total = _PAGE_CACHE.get(("__total__", pdf), 0)
        if total:
            return {"page": page, "total_pages": total, "image": img_b64}
    import base64
    import fitz
    doc = fitz.open(pdf)
    total = doc.page_count
    _PAGE_CACHE[("__total__", pdf)] = total
    if page > total:
        page = total
    cache_key = (pdf, page)
    if cache_key in _PAGE_CACHE:
        img_b64 = _PAGE_CACHE[cache_key]
    else:
        pix = doc[page - 1].get_pixmap(dpi=140)
        img_b64 = base64.b64encode(pix.tobytes("png")).decode("ascii")
        if len(_PAGE_CACHE) > 120:
            _PAGE_CACHE.clear()
            _PAGE_CACHE[("__total__", pdf)] = total
        _PAGE_CACHE[cache_key] = img_b64
    doc.close()
    return {"page": page, "total_pages": total, "image": img_b64}


def book_units(version: str, subject: str, grade: str, semester: str) -> list:
    """从 OCR 文本提取单元标题 + 起始页码（未 OCR 返回空）"""
    txt = _txt_path_for(version, subject, grade, semester)
    if not os.path.exists(txt):
        return []
    with open(txt, encoding="utf-8") as f:
        text = f.read()
    marks = _parse_page_marks(text)
    lines = text.splitlines(keepends=True)
    offsets = []
    for i, line in enumerate(lines):
        if UNIT_RE.search(line) or UNIT_RE_EN.search(line):
            offsets.append((sum(len(x) for x in lines[:i]), line.strip()))
    units = []
    for off, line in offsets:
        title = re.sub(r"[-—–:：\s]+", " ", line).strip()[:80]
        units.append({"title": title, "page": _page_of_offset(text, off, marks)})
    return units


def locate_keyword(version: str, subject: str, grade: str, semester: str, keyword: str) -> list:
    """在 OCR 文本中搜索关键词（支持逗号分隔多词，取并集），返回命中页码（去重）。
    无 OCR 文本时尝试 PDF 内嵌文本层（若 PDF 带文本）。"""
    if not keyword or not keyword.strip():
        return []
    marks = []
    text = ""
    txt = _txt_path_for(version, subject, grade, semester)
    if os.path.exists(txt):
        with open(txt, encoding="utf-8") as f:
            text = f.read()
        marks = _parse_page_marks(text)
    else:
        pdf = _resolve_local_book(version, subject, grade, semester)
        if pdf:
            text, marks = _pdf_text_with_marks(pdf)
    if not text:
        return []
    pages = []
    for kw in keyword.split(","):
        kw = kw.strip()
        if not kw:
            continue
        for m in re.finditer(re.escape(kw), text):
            p = _page_of_offset(text, m.start(), marks)
            if p not in pages:
                pages.append(p)
    return pages[:20]


_PDF_TEXT_CACHE = {}  # pdf_path -> (text, marks)


def _pdf_text_with_marks(pdf: str):
    """提取 PDF 内嵌文本层（带页码标记），带缓存"""
    key = (pdf, os.path.getmtime(pdf))
    if key in _PDF_TEXT_CACHE:
        return _PDF_TEXT_CACHE[key]
    import fitz
    doc = fitz.open(pdf)
    parts = []
    marks = []
    for i, p in enumerate(doc):
        marks.append((i + 1, len("\n".join(parts)) + (1 if parts else 0)))
        t = p.get_text().strip().replace("\n", " ")
        parts.append(f"--- 第{i + 1}页 ---\n{t}")
    doc.close()
    text = "\n".join(parts)
    if len(_PDF_TEXT_CACHE) > 20:
        _PDF_TEXT_CACHE.clear()
    _PDF_TEXT_CACHE[key] = (text, marks)
    return text, marks


def book_knowledge_points(version: str, subject: str, grade: str, semester: str) -> dict:
    """该教材已导入的知识点（按章节分组），并定位每章在教材中的页码。
    无 version 匹配时退化为 学科+年级+册次 匹配（单版本场景）。"""
    db = SessionLocal()
    try:
        subj = db.query(Subject).filter(Subject.name == subject, Subject.deleted == False).first()
        if not subj:
            return {"chapters": [], "total": 0}
        q = db.query(KnowledgePoint).filter(
            KnowledgePoint.subject_id == subj.id,
            KnowledgePoint.deleted == False)
        if grade:
            gno = {"一年级": 1, "二年级": 2, "三年级": 3, "四年级": 4, "五年级": 5,
                   "六年级": 6, "初一": 7, "初二": 8, "初三": 9, "高一": 10, "高二": 11, "高三": 12}.get(grade)
            if gno:
                q = q.filter(KnowledgePoint.grade == gno)
        if semester:
            q = q.filter(KnowledgePoint.semester == (1 if semester == "上册" else 2))
        if version:
            rows = q.filter(KnowledgePoint.version == version).all()
            if not rows:
                rows = q.all()  # 退化为无版本匹配（该学科年级册次唯一导入场景）
        else:
            rows = q.all()
        by_chapter = {}
        for r in rows:
            ch = r.chapter or "其他"
            by_chapter.setdefault(ch, []).append(r)
        chapters = []
        for ch, pts in by_chapter.items():
            page = 0
            loc = [p for p in locate_keyword(version, subject, grade, semester, ch) if p >= 7]
            if not loc:
                # 简化关键词重试：取章节名中长度>=2的中文片段（去括号/破折号/数字）
                core = re.sub(r"[^\u4e00-\u9fa5]", "", ch)
                core = core[2:] if len(core) > 6 else core
                if len(core) >= 2:
                    loc = [p for p in locate_keyword(version, subject, grade, semester, core) if p >= 7]
            if loc:
                page = loc[0]
            chapters.append({
                "chapter": ch,
                "page": page or 1,
                "points": [{"name": p.name, "desc": p.description or ""} for p in pts],
            })
        chapters.sort(key=lambda c: c["page"])
        return {"chapters": chapters, "total": sum(len(c["points"]) for c in chapters)}
    finally:
        db.close()


# ---------------------------------------------------------------- 导入入口配置

IMPORT_CONFIG_PATH = os.path.join(BACKEND_DIR, "textbook_import_config.json")
DEFAULT_IMPORT_CONFIG = {
    "enable_online_ctsf": True,   # 「在线知识大纲」入口（在线导入；仅知识点元数据，默认开）
    "enable_online_pdf": False,   # 「教材 PDF 提取」下载入口（内置第三方下载源，默认关；关闭时前端显示「自行通过合法渠道获取」引导）
    "enable_photo": True,         # 「拍照教材同步」入口（用户上传自己的纸质教材照片）
    "enable_user_pdf": True,      # 「自备教材 PDF」入口（用户上传自己持有的电子教材 PDF）
}


def get_import_config() -> dict:
    """读取 backend/textbook_import_config.json；缺失时自动创建并返回默认（全开）。

    对外推广时把 enable_online_ctsf / enable_online_pdf 改为 false，
    前端隐藏对应入口，后端对应接口也会返回 403。
    """
    cfg = dict(DEFAULT_IMPORT_CONFIG)
    try:
        with open(IMPORT_CONFIG_PATH, encoding="utf-8") as f:
            data = json.load(f)
        if isinstance(data, dict):
            for k in cfg:
                if k in data:
                    cfg[k] = bool(data[k])
    except FileNotFoundError:
        try:
            with open(IMPORT_CONFIG_PATH, "w", encoding="utf-8") as f:
                json.dump(DEFAULT_IMPORT_CONFIG, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"[textbook] 创建配置文件失败: {e}")
    except Exception as e:
        print(f"[textbook] 读取导入配置失败，使用默认: {e}")
    return cfg


# ---------------------------------------------------------------- 拍照教材同步

def photo_upload_dir() -> str:
    """拍照导入的临时照片目录（任务结束后删除，不长期保存用户教材影像）"""
    d = os.path.join(BACKEND_DIR, "data", "photo_upload")
    os.makedirs(d, exist_ok=True)
    return d


def _image_to_text(ocr, img_path: str) -> str:
    """单张照片 → RapidOCR → 按阅读顺序拼接文本"""
    result, _ = ocr(img_path)
    if not result:
        return ""
    lines = {}
    for box, text, score in result:
        y = int(round(box[0][1]))
        key = y // 12  # 12px 容差分桶
        lines.setdefault(key, []).append((box[0][0], text))
    ordered = []
    for key in sorted(lines):
        for x, text in sorted(lines[key], key=lambda t: t[0]):
            ordered.append(text)
    return " ".join(ordered)


def extract_photo_text(image_paths: list, task: dict) -> str:
    """多张教材照片 → OCR 文本（带页码标记），供后续切单元/提取"""
    ocr = _get_ocr()
    total = len(image_paths)
    parts = []
    for i, path in enumerate(image_paths, start=1):
        try:
            text = _image_to_text(ocr, path)
        except Exception as e:
            text = ""
            print(f"[textbook] 第{i}张照片 OCR 失败: {e}")
        parts.append(f"--- 第{i}页 ---\n{text}")
        _set_progress(task, 35 + int(i / total * 40), "ocr", f"识别照片 {i}/{total}")
    full = "\n".join(parts)
    _set_progress(task, 75, "ocr", f"OCR 完成，共 {total} 张")
    return full


def _run_photo_import(task: dict, meta: dict, image_paths: list) -> None:
    try:
        _set_progress(task, 0, "photo", "开始识别照片")
        if not image_paths:
            raise RuntimeError("没有可识别的照片")
        full_text = extract_photo_text(image_paths, task)
        if not full_text.strip():
            raise RuntimeError("照片中未识别到文字，请确认拍到了教材页面（光线充足、页面平整、对准文字）")
        book_meta = f"{meta.get('version', '')}{meta.get('subject', '')}{meta.get('grade', '')}{meta.get('semester', '')}"
        _extract_and_save(task, meta.get("subject", ""), meta.get("grade", ""),
                          meta.get("semester", ""), book_meta, full_text)
    except Exception as e:
        print(f"[textbook] 照片导入失败: {e}")
        with _tasks_lock:
            task["status"] = "failed"
            task["error"] = str(e)
            task["finished_at"] = time.strftime("%H:%M:%S")
        _set_progress(task, 0, "failed", str(e)[:200])


def start_photo_import(meta: dict, image_paths: list) -> dict:
    """创建并启动拍照教材导入任务（后台线程）。已有运行中任务则抛 RuntimeError"""
    if not _import_lock.acquire(blocking=False):
        raise RuntimeError("已有导入任务正在进行，请等待完成")
    task = {
        "id": uuid.uuid4().hex[:12],
        "status": "pending",
        "stage": "pending",
        "progress": 0,
        "message": "排队中",
        "source": "photo",
        "book": {k: meta.get(k) for k in ("subject", "version", "grade", "semester")},
        "local_pdf": False,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": "",
        "finished_at": None,
        "error": None,
        "result": None,
    }
    with _tasks_lock:
        _tasks[task["id"]] = task
        if len(_tasks) > 50:
            for k in sorted(_tasks, key=lambda x: _tasks[x]["created_at"])[: len(_tasks) - 50]:
                _tasks.pop(k, None)

    def _worker():
        try:
            _run_photo_import(task, meta, image_paths)
        finally:
            # 隐私：任务结束后删除本次上传的照片（只保留入库的知识点文本）
            try:
                if image_paths:
                    import shutil
                    d = os.path.dirname(os.path.abspath(image_paths[0]))
                    if os.path.isdir(d) and os.path.basename(d).startswith("upload_"):
                        shutil.rmtree(d, ignore_errors=True)
            except Exception:
                pass
            _import_lock.release()

    threading.Thread(target=_worker, daemon=True).start()
    return task


# ---------------------------------------------------------------- 自备教材 PDF 同步

def user_pdf_upload_dir() -> str:
    """自备 PDF 导入的临时目录（任务结束后删除，不长期保存用户教材文件）"""
    d = os.path.join(BACKEND_DIR, "data", "pdf_upload")
    os.makedirs(d, exist_ok=True)
    return d


def start_user_pdf_import(meta: dict, pdf_path: str) -> dict:
    """创建并启动「自备教材 PDF」导入任务。

    上传的 PDF 会移入本地教材库（data/textbooks/<版本>/<科目>/<年级><册次>.pdf），
    **长期保留在用户本地**，供教材库预览/关键词定位/知识点对照使用；
    仅清理临时上传目录本身。OCR 缓存 txt 同样保留在教材库目录。
    """
    if not _import_lock.acquire(blocking=False):
        raise RuntimeError("已有导入任务正在进行，请等待完成")
    book = {
        "subject": meta.get("subject", ""),
        "version": meta.get("version") or "自备教材",
        "grade": meta.get("grade", ""),
        "semester": meta.get("semester", ""),
    }
    task = {
        "id": uuid.uuid4().hex[:12],
        "status": "pending",
        "stage": "pending",
        "progress": 0,
        "message": "排队中",
        "source": "user_pdf",
        "book": {k: book.get(k) for k in ("subject", "version", "grade", "semester")},
        "local_pdf": True,
        "created_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "updated_at": "",
        "finished_at": None,
        "error": None,
        "result": None,
    }
    with _tasks_lock:
        _tasks[task["id"]] = task
        if len(_tasks) > 50:
            for k in sorted(_tasks, key=lambda x: _tasks[x]["created_at"])[: len(_tasks) - 50]:
                _tasks.pop(k, None)

    def _worker():
        try:
            final_pdf = book_pdf_path(book)
            os.makedirs(os.path.dirname(final_pdf), exist_ok=True)
            # 重新导入同一册时：覆盖旧 PDF，并删除旧 OCR 缓存强制重新识别
            txt = final_pdf[:-4] + ".txt"
            if os.path.exists(txt):
                os.remove(txt)
            if os.path.abspath(pdf_path) != os.path.abspath(final_pdf):
                os.replace(pdf_path, final_pdf)
            _run_import(task, book, local_pdf=final_pdf)
        finally:
            # 只清理临时上传目录；教材库里的 PDF/txt 保留在用户本地
            try:
                import shutil
                d = os.path.dirname(os.path.abspath(pdf_path))
                if os.path.isdir(d) and os.path.basename(d).startswith("upload_"):
                    shutil.rmtree(d, ignore_errors=True)
            except Exception:
                pass
            _import_lock.release()

    threading.Thread(target=_worker, daemon=True).start()
    return task
