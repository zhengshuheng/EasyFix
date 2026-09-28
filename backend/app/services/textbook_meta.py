# -*- coding: utf-8 -*-
"""教材版本元数据：版本选项清单 + 教材身份（edition_key）生成规则。

edition_key 形如「{学科key}-{版本slug}」（math-rjb / english-wyb3），
用于 knowledge_point（知识点）与 kid_textbook（小孩教材偏好）之间的版本对齐。
无版本时返回 None，表示「通用教材数据」（任何版本都可见）。
"""
import re
from typing import Optional

# 教材版本选项（按学科；与教材目录数据源一致，冷门版本可后续扩充）
TEXTBOOK_VERSIONS = {
    "数学": ["人教版", "北师大版", "苏教版", "冀教版", "西师大版", "青岛版", "北京版"],
    "语文": ["统编版（部编版）"],
    "英语": ["人教版PEP", "外研版（三年级起点）", "外研版（一年级起点）", "冀教版（三年级起点）", "北师大版", "沪教版", "译林版"],
}

_SUBJECT_KEYS = {"数学": "math", "语文": "chinese", "英语": "english"}
_VERSION_SLUGS = {
    "人教版": "rjb", "北师大版": "bsd", "苏教版": "sjb", "冀教版": "jjb", "西师大版": "xsd",
    "青岛版": "qdb", "北京版": "bjb", "统编版（部编版）": "tbb", "人教版PEP": "pep",
    "外研版（三年级起点）": "wyb3", "外研版（一年级起点）": "wyb1", "沪教版": "hjb", "译林版": "ylb",
}


def edition_key_for(subject_name: str, version: Optional[str]) -> Optional[str]:
    """按 学科+版本 生成教材身份（edition_key）；无版本时返回 None（通用教材数据）"""
    if not version:
        return None
    sk = _SUBJECT_KEYS.get(subject_name or "", "")
    vs = _VERSION_SLUGS.get(version) or version
    vs = re.sub(r"[^\w\u4e00-\u9fff-]", "", str(vs))[:40]
    return f"{sk}-{vs}" if sk else vs
