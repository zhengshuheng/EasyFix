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


def book_pdf_path(book: dict) -> str:
    return os.path.join(DATA_DIR, book.get("version", "未分类"), book.get("subject", "未分类"),
                        f"{book.get('grade', '')}{book.get('semester', '')}.pdf")


def book_txt_path(book: dict) -> str:
    return os.path.join(DATA_DIR, book.get("version", "未分类"), book.get("subject", "未分类"),
                        f"{book.get('grade', '')}{book.get('semester', '')}.txt")


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
            raw = src.get("url", "")
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


def extract_text(pdf_path: str, txt_path: str, task: dict) -> str:
    """PDF → OCR 文本（缓存到 txt_path），返回全文"""
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

def _llm_json(prompt: str, system: str = "你只输出JSON，不要输出任何解释。", max_tokens: int = 2500) -> str:
    """调用 LLM（关闭思考），返回原始文本"""
    llm = LLMService()
    resp = llm._retry_on_rate_limit(
        llm._call_messages_create,
        model=llm._get_config("model", "claude-sonnet-4-20250514"),
        max_tokens=max_tokens,
        temperature=0,
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
    """按单元标题切分 OCR 全文，返回 [(chapter, body)]"""
    lines = text.splitlines()
    # 记录单元标题行索引
    markers = []
    for i, line in enumerate(lines):
        if UNIT_RE.search(line) or UNIT_RE_EN.search(line):
            title = re.sub(r"[-—–:：\s]+", " ", line).strip()[:80]
            markers.append((i, title))
    if not markers:
        # 无单元标题：整本作为一个章节
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
        # 3. 按单元切分 + LLM 提取
        units = split_units(full_text)
        if not units:
            raise RuntimeError("未从教材中识别出单元标题，请确认 PDF 内容完整")
        _set_progress(task, 76, "extracting", f"共 {len(units)} 个单元，开始提取知识点")
        book_meta = f"{book.get('version', '')}{book.get('subject', '')}{book.get('grade', '')}{book.get('semester', '')}"
        all_points = []
        for i, (chapter, body) in enumerate(units, start=1):
            _set_progress(task, 76 + int(i / len(units) * 19), "extracting",
                          f"提取知识点 {i}/{len(units)}（{chapter[:20]}…）")
            try:
                pts = extract_unit_points(book.get("subject", ""), book_meta, chapter, body, task)
                for name, desc in pts:
                    all_points.append((name, desc, chapter))
                print(f"[textbook] 单元「{chapter}」提取 {len(pts)} 个知识点")
            except Exception as e:
                print(f"[textbook] 单元「{chapter}」提取失败: {e}")
                _set_progress(task, 76 + int(i / len(units) * 19), "extracting",
                              f"单元 {i} 提取失败，跳过")
        if not all_points:
            raise RuntimeError("所有单元均未提取到知识点")
        # 4. 入库
        _set_progress(task, 95, "importing", f"写入 {len(all_points)} 个知识点")
        ensure_chapter_column()
        result = {"points_total": len(all_points)}
        by_chapter = {}
        for name, desc, chapter in all_points:
            by_chapter.setdefault(chapter, []).append((name, desc))
        for chapter, pts in by_chapter.items():
            r = import_points(book.get("subject", ""), book.get("grade", ""), book.get("semester", ""),
                              chapter, pts, task)
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

def scan_local() -> list:
    """扫描 data/textbooks 下所有 PDF，解析 版本/科目/年级册次.pdf 结构"""
    found = []
    if not os.path.isdir(DATA_DIR):
        return found
    for root, dirs, files in os.walk(DATA_DIR):
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
    try:
        os.startfile(DATA_DIR)  # Windows
    except Exception:
        pass
    return DATA_DIR
