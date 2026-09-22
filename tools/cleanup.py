#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""一键清理项目临时区 tools/tmp/（含子目录全部内容）。
约定见 docs/CONVENTIONS.md「临时文件约定」。
- 一次性脚本、测试产物、调试日志、截图等临时文件一律写 tools/tmp/；
- 会话收尾运行本脚本清空；也可手动删除目录内容。
本脚本只删除 tools/tmp/ 内的内容，不碰项目任何其他文件。
"""
import os
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TMP = os.path.join(ROOT, "tools", "tmp")


def main():
    if not os.path.isdir(TMP):
        print("[cleanup] tools/tmp/ 不存在，无需清理")
        return
    removed = 0
    for name in os.listdir(TMP):
        p = os.path.join(TMP, name)
        try:
            if os.path.isdir(p):
                shutil.rmtree(p)
            else:
                os.remove(p)
            removed += 1
            print(f"  - {name}")
        except OSError as e:
            print(f"  ! 跳过 {name}: {e}")
    print(f"[cleanup] 完成，共清理 {removed} 项。tools/tmp/ 现为空。")
    if removed == 0:
        print("[cleanup] 没有需要清理的临时文件。")


if __name__ == "__main__":
    sys.exit(main())
