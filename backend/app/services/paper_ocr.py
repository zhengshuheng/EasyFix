"""线下做题：从试卷照片中识别学生手写作答，并按卷面题号映射回题目。

关键点：打印出来的 PDF 是按题型分大题、题号从 1 连续编号的，顺序与数据库里的
题目顺序**不一致**（见 pdf.PracticeSetPDF.generate）。这里复现同一套分组顺序，
保证「卷面题号 → practice_question」的映射和打印出来的卷子完全一致。
"""
import json
import re
from typing import Any, Dict, List, Optional

from app.services.pdf import PracticeSetPDF
from app.services.multimodal_ocr import multimodal_ocr_service

TYPE_ORDER = PracticeSetPDF.TYPE_ORDER
TYPE_NAMES = PracticeSetPDF.TYPE_NAMES


def printed_order(questions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """返回卷面顺序的题目列表（与 PDF 打印的题号一一对应，索引 i 对应卷面题号 i+1）。"""
    groups: Dict[str, List[Dict[str, Any]]] = {}
    for q in questions:
        groups.setdefault(str(q.get("question_type") or ""), []).append(q)
    ordered = sorted(
        groups.items(),
        key=lambda kv: TYPE_ORDER.get(kv[0], 99) if kv[0] else 99,
    )
    out: List[Dict[str, Any]] = []
    for _type_key, items in ordered:
        out.extend(items)
    return out


def _option_line(q: Dict[str, Any]) -> str:
    opts = []
    for letter, key in (("A", "option_a"), ("B", "option_b"), ("C", "option_c"), ("D", "option_d")):
        val = (q.get(key) or "").strip()
        if val:
            opts.append(f"{letter}. {val}")
    return " ".join(opts)


ANSWER_PROMPT_HEAD = """你是一名批改助手。下面是一份试卷的题目清单（**题号与学生卷面上的题号完全一致**）。
请仔细查看这张试卷照片，读出**学生在卷面上手写的作答**，逐题输出结果。

题目清单：
"""

ANSWER_PROMPT_TAIL = """
输出要求：只输出一个 JSON 对象，不要任何解释文字、不要 markdown 代码块。格式：
{"answers":[{"no":3,"answer":"am","confidence":"high"}],
 "empty":[1,2],
 "notes":"识别备注"}

规则：
- no：卷面题号（整数，必须与上面清单里的题号一致）；
- answer：学生在卷面上写下的内容原文。选择题只写所选字母（如 A）；判断题写 √ 或 ×；
  填空题写横线上的内容；计算题/应用题/操作题/写话题写学生写下的算式和最终答案
  （保留关键步骤，用「，」分隔，例如「3+2=5，5个」）；
- confidence：high / medium / low，表示对该题识别的把握程度；
- empty：学生**空着没写**的题号列表；
- 没写就是没写，**不要臆造答案**，也不要抄写题目本身；
- 题干里的空白看起来像有字但划掉了，按最终保留的内容识别，并在 notes 里说明。
"""


def build_answer_prompt(questions: List[Dict[str, Any]]) -> str:
    """按卷面顺序构造结构化抽取提示词。"""
    ordered = printed_order(questions)
    lines: List[str] = []
    last_type: Optional[str] = None
    section_idx = 0
    for idx, q in enumerate(ordered, 1):
        type_key = str(q.get("question_type") or "")
        if type_key != last_type:
            section_idx += 1
            cn = "一二三四五六七八九十"
            prefix = f"{cn[section_idx - 1]}、" if section_idx <= len(cn) else f"{section_idx}、"
            name = TYPE_NAMES.get(type_key, "题目") if type_key else "题目"
            lines.append(f"{prefix}{name}")
            last_type = type_key
        text = (q.get("parsed_question") or q.get("original_text") or "").strip().replace("\n", " ")
        if len(text) > 160:
            text = text[:160] + "…"
        opt = _option_line(q)
        lines.append(f"{idx}. {text}" + (f"（{opt}）" if opt else ""))
    return ANSWER_PROMPT_HEAD + "\n".join(lines) + "\n" + ANSWER_PROMPT_TAIL


def _extract_json(text: str) -> Optional[dict]:
    """从模型输出里抠出 JSON 对象（容忍 ```json 包裹与前后说明文字）。"""
    if not text:
        return None
    raw = text.strip()
    fence = re.search(r"```(?:json)?\s*(.+?)```", raw, re.S)
    if fence:
        raw = fence.group(1).strip()
    try:
        return json.loads(raw)
    except Exception:
        pass
    start = raw.find("{")
    end = raw.rfind("}")
    if start >= 0 and end > start:
        snippet = raw[start:end + 1]
        try:
            return json.loads(snippet)
        except Exception:
            snippet = snippet.replace("，", ",").replace("：", ":")
            try:
                return json.loads(snippet)
            except Exception:
                return None
    return None


def _norm_no(value: Any) -> Optional[int]:
    try:
        return int(str(value).strip().strip("．.、"))
    except Exception:
        return None


def _compress(text: str) -> str:
    """去掉空白，用于判断模型是否只是把题目抄了回来。"""
    return re.sub(r"\s+", "", text or "")


def normalize_image(path: str, max_side: int = 2000, quality: int = 92) -> str:
    """把手机/摄像头拍的照片整理成「方向正确、体积可控」的图，再送视觉模型。

    两个真实坑：
      1. 手机竖拍的照片方向信息在 EXIF 里，不应用就会被当成横躺着的卷子识别；
      2. 动辄 4000+ 像素、几 MB 的照片可能超出视觉模型/接口限制。
    处理失败时退回原图，不影响主流程。
    """
    try:
        from PIL import Image, ImageOps

        img = Image.open(path)
        img = ImageOps.exif_transpose(img)
        if img.mode not in ("RGB", "L"):
            img = img.convert("RGB")
        long_side = max(img.size)
        if long_side > max_side:
            ratio = max_side / long_side
            img = img.resize(
                (max(1, int(img.width * ratio)), max(1, int(img.height * ratio))),
                Image.LANCZOS,
            )
        img.save(path, "JPEG", quality=quality)
        return path
    except Exception:
        return path


def recognize_answers(
    image_paths: List[str],
    questions: List[Dict[str, Any]],
    subject: str = "",
) -> Dict[str, Any]:
    """识别多张试卷照片中的手写作答。

    Args:
        image_paths: 本地图片绝对路径列表（按页顺序）
        questions: 题目列表，每项含 id/parsed_question/original_text/question_type/option_a~d

    Returns:
        {
          "answers": [{"question_id","no","answer","confidence","page"}],
          "empty": [题号...],
          "pages": [{"index","ok","count","error","notes"}],
          "notes": [...],
          "provider": str, "model": str,
          "error": str  # 仅在整体失败时
        }
    """
    ordered = printed_order(questions)
    if not ordered:
        return {"answers": [], "empty": [], "pages": [], "error": "练习集没有题目"}
    if not image_paths:
        return {"answers": [], "empty": [], "pages": [], "error": "没有上传照片"}

    prompt = build_answer_prompt(questions)
    if subject:
        prompt = f"（科目：{subject}）\n" + prompt

    merged: Dict[int, Dict[str, Any]] = {}
    empty_nos: set = set()
    pages: List[Dict[str, Any]] = []
    notes: List[str] = []
    provider = ""
    model = ""

    for page_index, path in enumerate(image_paths, 1):
        path = normalize_image(path)  # EXIF 方向 + 控体积
        res = multimodal_ocr_service.recognize(path, prompt=prompt)
        provider = res.get("provider") or provider
        model = res.get("model") or model
        if res.get("error"):
            pages.append({"index": page_index, "ok": False, "count": 0,
                          "error": str(res.get("error"))})
            continue
        text = res.get("full_text") or ""
        data = _extract_json(text)
        if data is None:
            pages.append({"index": page_index, "ok": False, "count": 0,
                          "error": "识别结果不是 JSON", "raw": text[:300]})
            continue

        got = 0
        for item in (data.get("answers") or []):
            if not isinstance(item, dict):
                continue
            no = _norm_no(item.get("no"))
            if no is None or no < 1 or no > len(ordered):
                continue
            answer = str(item.get("answer") or "").strip()
            if not answer:
                continue
            # 模型把题干抄回来的情况：与题干高度重合则丢弃
            stem = _compress(ordered[no - 1].get("parsed_question") or "")
            if stem and _compress(answer) and _compress(answer) in stem and len(_compress(answer)) > 8:
                continue
            confidence = str(item.get("confidence") or "").strip().lower() or "medium"
            prev = merged.get(no)
            rank = {"high": 3, "medium": 2, "low": 1}
            if prev is None or rank.get(confidence, 0) > rank.get(prev["confidence"], 0):
                merged[no] = {
                    "question_id": ordered[no - 1].get("id"),
                    "no": no,
                    "answer": answer,
                    "confidence": confidence if confidence in rank else "medium",
                    "page": page_index,
                }
            got += 1
        for no in (data.get("empty") or []):
            n = _norm_no(no)
            if n is not None and 1 <= n <= len(ordered):
                empty_nos.add(n)
        note = (data.get("notes") or "").strip()
        if note:
            notes.append(f"第{page_index}页：{note}")
        pages.append({"index": page_index, "ok": True, "count": got,
                      "matched": len(data.get("answers") or [])})

    answers = [merged[no] for no in sorted(merged.keys())]
    return {
        "answers": answers,
        "empty": sorted(n for n in empty_nos if n not in merged),
        "pages": pages,
        "notes": notes,
        "provider": provider,
        "model": model,
        "total_questions": len(ordered),
    }
