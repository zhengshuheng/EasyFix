"""K12 教材知识点导入服务

数据源：https://github.com/mmlong818/k12-knowledge-points
（K12全学段知识点数据集，33,765 个知识点，覆盖 17 科目、347 本教材，按 学段×科目 拆分）

流程：
1. 从本地缓存 backend/data/k12/ 读取拆分数据（不存在则尝试从 GitHub 下载）
2. 过滤低置信度条目
3. LLM 分批为每条知识点判断 年级(1-12) + 学期(1/2)（数据集本身只有学段，无年级学期）
4. 按 (subject_id, name) 去重后批量写入 knowledge_point 表
"""
import json
import os
import threading
from typing import List, Optional

import requests

from app.database import SessionLocal
from app.models import KnowledgePoint, Subject
from app.services.llm import LLMService

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "data", "k12")
# 开发/离线机可配置代理（可选）
K12_PROXY = os.environ.get("K12_PROXY", "")  # 例如 socks5h://10.0.200.184:1080
BASE_URL = "https://raw.githubusercontent.com/mmlong818/k12-knowledge-points/main/split"

# 并发保护：导入期间避免重复触发
_import_lock = threading.Lock()

_INDEX_CACHE = None
_INDEX_CACHE_LOCK = threading.Lock()


def _ensure_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def _proxies() -> Optional[dict]:
    if K12_PROXY:
        return {"http": K12_PROXY, "https": K12_PROXY}
    return None


def _download(url: str, dest: str) -> None:
    """下载到本地缓存；直连失败 + 配置了代理则走代理"""
    _ensure_dir()
    headers = {"User-Agent": "Mozilla/5.0 (EasyFix-k12-importer)"}
    last_err = None
    try:
        r = requests.get(url, headers=headers, timeout=60)
        r.raise_for_status()
        with open(dest, "wb") as f:
            f.write(r.content)
        return
    except Exception as e:
        last_err = e
    if _proxies():
        try:
            r = requests.get(url, headers=headers, timeout=120, proxies=_proxies())
            r.raise_for_status()
            with open(dest, "wb") as f:
                f.write(r.content)
            return
        except Exception as e:
            last_err = e
    raise RuntimeError(f"下载失败：{last_err}。请手动下载 {url} 放到 {dest}")


def get_catalog() -> dict:
    """返回拆分索引（文件清单 + 计数）"""
    global _INDEX_CACHE
    with _INDEX_CACHE_LOCK:
        if _INDEX_CACHE is not None:
            return _INDEX_CACHE
    _ensure_dir()
    index_path = os.path.join(DATA_DIR, "index.json")
    if not os.path.exists(index_path):
        _download(f"{BASE_URL}/index.json", index_path)
    with open(index_path, encoding="utf-8") as f:
        idx = json.load(f)
    with _INDEX_CACHE_LOCK:
        _INDEX_CACHE = idx
    return idx


def get_subject_data(grade_band: str, subject: str) -> dict:
    """读取（或下载）某一学段×科目的数据文件"""
    _ensure_dir()
    band_dir = os.path.join(DATA_DIR, grade_band)
    os.makedirs(band_dir, exist_ok=True)
    path = os.path.join(band_dir, f"{subject}.json")
    if not os.path.exists(path):
        _download(f"{BASE_URL}/{grade_band}/{subject}.json", path)
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def assign_grades_llm(items: List[dict], subject_name: str, grade_band: str, batch_size: int = 60) -> dict:
    """LLM 分批为知识点分配 年级/学期。

    返回: {"grades": {原始序号: {"grade": int|None, "semester": int|None}},
           "failed": 数量}
    """
    llm = LLMService()
    grades: dict = {}
    failed = 0
    for start in range(0, len(items), batch_size):
        batch = items[start:start + batch_size]
        lines = []
        for i, it in enumerate(batch, start=1):
            name = it.get("canonical_name") or it.get("title") or ""
            aliases = it.get("aliases") or ""
            if aliases:
                try:
                    alias_list = json.loads(aliases)
                    if isinstance(alias_list, list) and alias_list:
                        name += "（别名：" + "、".join(str(a) for a in alias_list[:3]) + "）"
                except Exception:
                    pass
            lines.append(f"{i}. {name}")
        prompt = (
            f"你是中国K12教材专家（人教版/统编版）。下面是{subject_name}（{grade_band}阶段）的"
            f"{len(batch)}个知识点，来自真实教材抽取。\n"
            "请为每个知识点判断：它在人教版/统编版教材中首次系统讲授的年级（小学1-6，初中7-9，高中10-12）"
            "和学期（1=上学期，2=下学期；无法确定写0）。\n"
            "只输出一个JSON对象，不要任何解释：\n"
            '{"items":[{"i":1,"grade":3,"semester":1},...]} \n'
            "其中 i 对应下面的编号，grade/semester 均为整数，semester 0 表示不确定。\n"
            "知识点列表：\n" + "\n".join(lines)
        )
        try:
            resp = llm._retry_on_rate_limit(
                llm._call_messages_create,
                model=llm._get_config("model", "claude-sonnet-4-20250514"),
                max_tokens=2000,
                temperature=0,
                system="你只输出JSON，不输出其他内容。",
                messages=[{"role": "user", "content": prompt}],
            )
            content = resp.content[0].text if hasattr(resp.content[0], "text") else str(resp.content[0])
            parsed = _parse_grade_json(content)
            if not parsed:
                failed += len(batch)
                print(f"[k12] LLM 批 {start//batch_size + 1} 返回无法解析，跳过该批")
                continue
            for it in parsed:
                idx = it.get("i")
                if not isinstance(idx, int) or not (1 <= idx <= len(batch)):
                    continue
                g = it.get("grade")
                s = it.get("semester")
                if not isinstance(g, int) or not (1 <= g <= 12):
                    continue
                if not isinstance(s, int) or s not in (0, 1, 2):
                    s = 0
                grades[start + idx - 1] = {"grade": g, "semester": s if s else None}
        except Exception as e:
            failed += len(batch)
            print(f"[k12] LLM 分配失败（批 {start//batch_size + 1}）: {e}")
    return {"grades": grades, "failed": failed}


def _parse_grade_json(content: str) -> list:
    import re
    m = re.search(r"\{.*\}", content, re.S)
    if not m:
        return []
    try:
        data = json.loads(m.group(0))
        items = data.get("items", [])
        return items if isinstance(items, list) else []
    except Exception:
        return []


def import_subject(grade_band: str, subject: str, confidence_min: float = 0.7, limit: Optional[int] = None) -> dict:
    """执行导入，返回 {total, imported, skipped, failed, llm_failed}"""
    with _import_lock:
        return _import_subject_locked(grade_band, subject, confidence_min, limit)


def _import_subject_locked(grade_band: str, subject: str, confidence_min: float, limit: Optional[int]) -> dict:
    # 科目映射（学段不同同名科目可能映射到不同学科记录）
    subject_aliases = {
        "小学": {"语文": "语文", "数学": "数学", "英语": "英语", "思政": "道德与法治", "音乐": "音乐", "美术": "美术", "体育": "体育"},
        "初中": {"语文": "语文", "数学": "数学", "英语": "英语", "物理": "物理", "化学": "化学", "生物": "生物",
                 "地理": "地理", "历史": "历史", "思政": "道德与法治", "音乐": "音乐", "美术": "美术", "体育": "体育"},
        "高中": {"语文": "语文", "数学": "数学", "英语": "英语", "物理": "物理", "化学": "化学", "生物": "生物",
                 "地理": "地理", "历史": "历史", "思政": "思想政治", "科学": "科学", "音乐": "音乐", "美术": "美术", "体育": "体育"},
    }
    db = SessionLocal()
    try:
        # 定位学科
        target_name = subject_aliases.get(grade_band, {}).get(subject, subject)
        subj = db.query(Subject).filter(Subject.name == target_name, Subject.deleted == False).first()
        if not subj:
            # 尝试按原始名
            subj = db.query(Subject).filter(Subject.name == subject, Subject.deleted == False).first()
        if not subj:
            # 找不到就自动创建该学科
            subj = Subject(name=target_name if target_name else subject)
            db.add(subj)
            db.commit()
            db.refresh(subj)

        data = get_subject_data(grade_band, subject)
        kps = data.get("knowledge_points", [])
        total = len(kps)
        if not kps:
            return {"total": 0, "imported": 0, "skipped": 0, "failed": 0, "llm_failed": 0}

        # 置信度过滤
        filtered = [k for k in kps if (k.get("confidence") or 0) >= confidence_min]
        if limit and limit > 0:
            filtered = filtered[:limit]

        # LLM 分配年级/学期
        result = assign_grades_llm(filtered, subj.name, grade_band)
        grades = result["grades"]
        llm_failed = result["failed"]

        # 已存在的 (name) 集合（该学科下）
        existing_names = {
            row.name for row in db.query(KnowledgePoint.name).filter(
                KnowledgePoint.subject_id == subj.id, KnowledgePoint.deleted == False
            ).all()
        }

        imported = 0
        skipped = 0
        failed = 0
        batch_rows = []
        seen = set()
        for idx, it in enumerate(filtered):
            name = (it.get("canonical_name") or it.get("title") or "").strip()
            if not name:
                failed += 1
                continue
            if name in existing_names or name in seen:
                skipped += 1
                continue
            g = grades.get(idx, {}).get("grade") if idx in grades else None
            s = grades.get(idx, {}).get("semester") if idx in grades else None
            # grade 必须在学段内，否则归 null
            if grade_band == "小学" and g is not None and not (1 <= g <= 6):
                g = None
            if grade_band == "初中" and g is not None and not (7 <= g <= 9):
                g = None
            if grade_band == "高中" and g is not None and not (10 <= g <= 12):
                g = None
            row = KnowledgePoint(name=name, subject_id=subj.id, grade=g, semester=s if g else None)
            batch_rows.append(row)
            seen.add(name)
            imported += 1

        if batch_rows:
            db.add_all(batch_rows)
            db.commit()

        return {
            "total": total,
            "filtered": len(filtered),
            "imported": imported,
            "skipped": skipped,
            "failed": failed,
            "llm_failed": llm_failed,
            "subject_id": subj.id,
            "subject_name": subj.name,
        }
    finally:
        db.close()
