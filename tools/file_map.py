# -*- coding: utf-8 -*-
"""大文件结构地图：定位问题时先跑它拿行号索引，避免全量 read_file 大文件。

用法:
    python tools/file_map.py <file> [--kwd 关键词] [--max 200]
    python tools/file_map.py frontend/src/views/PracticeSets.vue
    python tools/file_map.py backend/app/routers/practice_set.py --kwd grading

输出紧凑行号索引（不打印代码内容）：
  .vue -> [tpl] template 区块注释 / [scr] script 顶层符号 / [sty] style 边界
  .py  -> [fn] 函数 / [cl] 类 / [im] import（仅顶层）
"""
import ast
import re
import sys

def map_py(path, kwd, max_rows):
    src = open(path, encoding='utf-8').read()
    tree = ast.parse(src)
    out = []
    for node in tree.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            tag, name = 'fn ', node.name
        elif isinstance(node, ast.ClassDef):
            tag, name = 'cl ', node.name
        elif isinstance(node, ast.Import) or isinstance(node, ast.ImportFrom):
            tag, name = 'im ', (node.names[0].name if node.names else '?')
        else:
            continue
        span = node.end_lineno - node.lineno + 1
        row = f'{node.lineno:>5}  {tag}{name}  ({span}行)'
        if not kwd or kwd.lower() in name.lower():
            out.append(row)
        if len(out) >= max_rows:
            out.append(f'... 超过 {max_rows} 行，用 --kwd 过滤')
            break
    return out

def map_vue(path, kwd, max_rows):
    lines = open(path, encoding='utf-8').read().splitlines()
    out = []
    in_script = False
    for i, line in enumerate(lines, 1):
        s = line.strip()
        if s.startswith('<script'):
            in_script = True
            out.append(f'{i:>5}  scr <script setup> 开始')
            continue
        if in_script and (s.startswith('</script>') or s.startswith('<style')):
            if s.startswith('<style'):
                out.append(f'{i:>5}  sty <style> 开始')
            in_script = False
            continue
        if not in_script:
            if s.startswith('<!--'):
                row = f'{i:>5}  tpl {s[:60]}'
                if not kwd or kwd.lower() in s.lower():
                    out.append(row)
            elif s == '<template>' and not line[:1].isspace():
                out.append(f'{i:>5}  tpl <template> 开始')
            elif s == '</template>' and not line[:1].isspace():
                out.append(f'{i:>5}  tpl </template> 结束')
            continue
        # script 顶层符号
        m = re.match(r'^(const|let|function|async function|import)\s+([A-Za-z_$][\w$]*)', s)
        if m:
            row = f'{i:>5}  scr {m.group(1)} {m.group(2)}'
            if not kwd or kwd.lower() in (m.group(2).lower() + s):
                out.append(row)
        if len(out) >= max_rows:
            out.append(f'... 超过 {max_rows} 行，用 --kwd 过滤')
            break
    return out

def main():
    args = sys.argv[1:]
    if not args:
        print(__doc__)
        sys.exit(1)
    path = args[0]
    kwd = None
    max_rows = 200
    i = 1
    while i < len(args):
        if args[i] == '--kwd' and i + 1 < len(args):
            kwd = args[i + 1]
            i += 2
        elif args[i] == '--max' and i + 1 < len(args):
            max_rows = int(args[i + 1])
            i += 2
        else:
            i += 1
    try:
        total = sum(1 for _ in open(path, encoding='utf-8'))
    except OSError as e:
        print(f'error: {e}')
        sys.exit(1)
    print(f'== {path}（{total} 行）==')
    if path.endswith('.py'):
        rows = map_py(path, kwd, max_rows)
    elif path.endswith('.vue'):
        rows = map_vue(path, kwd, max_rows)
    else:
        print('仅支持 .py / .vue')
        sys.exit(1)
    print('\n'.join(rows))

if __name__ == '__main__':
    main()
