# -*- coding: utf-8 -*-
r"""EasyFix 开发测试服务启动器（Agent 自测专用，一行调用）

用法 —— 在常驻内核里 exec（推荐 browser 内核；shell 起的进程会被 QwenPaw 清理）：

    exec(open(r'E:\qianwenpaw\EasyFix-main\tools\devserver.py', encoding='utf-8').read())

随后即可：

    page = await dev_enter_app('/practice-sets')     # 打开页面并确保已进入学习空间
    obs  = await page.snapshot(); print(obs.text[:800])

可在 exec 之前覆盖的变量：
    DEV_PORT = 8016            服务端口（默认 8016，避开用户日常的 8010）
    DEV_ROOT = r'E:\...'       项目根目录
    DEV_FORCE_RESTART = 1      忽略"代码未变更"判断，强制重启

行为（幂等，秒级返回）：
    1. 端口无服务 / backend/app 下 .py 有更新 / 强制重启 → 重启 uvicorn
    2. 否则复用现有服务
    3. 轮询就绪后打印一行状态；失败则打印日志尾部并抛异常

辅助函数：dev_restart() / dev_build() / dev_log_tail(n) / dev_kill()
"""
import json
import os
import re
import subprocess
import sys
import time
import urllib.request

DEV_ROOT = globals().get('DEV_ROOT') or r'E:\qianwenpaw\EasyFix-main'
DEV_PORT = int(globals().get('DEV_PORT') or os.environ.get('DEV_PORT') or 8016)
DEV_BASE = f'http://127.0.0.1:{DEV_PORT}'
LOG_PATH = os.path.join(DEV_ROOT, 'backend', 'devserver.log')
STATE_PATH = os.path.join(DEV_ROOT, 'backend', '.devserver_state.json')
PYTHON = os.path.join(DEV_ROOT, '.venv', 'Scripts', 'python.exe')
BACKEND_DIR = os.path.join(DEV_ROOT, 'backend')

DEV_PROC = None
DEV_READY = False


def _is_up(timeout=2):
    try:
        with urllib.request.urlopen(DEV_BASE + '/api/subjects', timeout=timeout) as r:
            return r.status == 200
    except Exception:
        return False


def _backend_mtime():
    """backend/app 下最新 .py 修改时间（用于判断是否需要重启）"""
    newest = 0.0
    for base, _, files in os.walk(os.path.join(BACKEND_DIR, 'app')):
        for f in files:
            if f.endswith('.py'):
                try:
                    newest = max(newest, os.path.getmtime(os.path.join(base, f)))
                except OSError:
                    pass
    return newest


def _read_state():
    try:
        with open(STATE_PATH, encoding='utf-8') as fh:
            return json.load(fh)
    except Exception:
        return {}


def _write_state(pid, started_at):
    try:
        with open(STATE_PATH, 'w', encoding='utf-8') as fh:
            json.dump({'pid': pid, 'port': DEV_PORT, 'started_at': started_at}, fh)
    except Exception:
        pass


def dev_kill():
    """杀掉占用本端口的进程（仅限 python 进程；返回被杀 PID 列表）"""
    killed = []
    try:
        out = subprocess.run(['netstat', '-ano'], capture_output=True, text=True, timeout=20).stdout
    except Exception:
        return killed
    pat = re.compile(r':%d\s+.*LISTENING\s+(\d+)' % DEV_PORT)
    pids = {m.group(1) for line in out.splitlines() if (m := pat.search(line))}
    for pid in pids:
        try:
            info = subprocess.run(['tasklist', '/FI', f'PID eq {pid}'],
                                  capture_output=True, text=True, timeout=20).stdout
        except Exception:
            continue
        if 'python' not in info.lower():
            continue  # 非本服务的进程，不动
        subprocess.run(['taskkill', '/F', '/PID', pid], capture_output=True, timeout=20)
        killed.append(int(pid))
    if killed:
        time.sleep(1.0)
    return killed


def dev_log_tail(n=40):
    try:
        with open(LOG_PATH, encoding='utf-8', errors='replace') as fh:
            lines = fh.read().splitlines()
        return '\n'.join(lines[-n:])
    except Exception as exc:
        return f'<no log: {exc}>'


def dev_restart(wait=45):
    """强制重启后端并等待就绪"""
    global DEV_PROC, DEV_READY
    dev_kill()
    logf = open(LOG_PATH, 'w', encoding='utf-8', errors='replace')
    DEV_PROC = subprocess.Popen(
        [PYTHON, '-m', 'uvicorn', 'app.main:app', '--host', '127.0.0.1', '--port', str(DEV_PORT)],
        cwd=BACKEND_DIR, stdin=subprocess.DEVNULL, stdout=logf, stderr=subprocess.STDOUT,
    )
    started = time.time()
    _write_state(DEV_PROC.pid, started)
    deadline = started + wait
    while time.time() < deadline:
        if _is_up():
            DEV_READY = True
            return True, time.time() - started
        if DEV_PROC.poll() is not None:  # 进程已退出
            return False, time.time() - started
        time.sleep(0.5)
    return False, time.time() - started


def dev_build(timeout=420, tail_lines=6):
    """构建前端（含 OOM 规避），返回 (ok, 输出尾部)

    注意：非 TTY 下 vite 不打印 "✓ built in Xs"，故以 returncode 判定成败。
    """
    env = dict(os.environ, NODE_OPTIONS='--max-old-space-size=4096')
    r = subprocess.run(['node', os.path.join('node_modules', 'vite', 'bin', 'vite.js'), 'build'],
                       cwd=os.path.join(DEV_ROOT, 'frontend'), env=env,
                       capture_output=True, text=True, timeout=timeout)
    out = ((r.stderr or '') + '\n' + (r.stdout or '')).strip()
    ok = r.returncode == 0
    return ok, '\n'.join(out.splitlines()[-tail_lines:])


async def dev_open(path='/'):
    """（异步）用 Browser SDK 打开页面，复用本 session 的 active page"""
    b = globals().get('browser') or globals().get('BROWSER')
    if b is None:
        b = await Browser.connect()  # noqa: F821  (Browser SDK 由内核注入)
        globals()['browser'] = b
    p = await b.open(DEV_BASE + path)
    globals()['page'] = p
    return p


async def dev_enter_app(path='/practice-sets', user='小红'):
    """（异步）打开应用；若停在"今天谁学习"首页则自动点小孩卡片，最后跳到 path"""
    p = await dev_open('/')
    obs = await p.snapshot()
    if '今天谁学习' in obs.text and user in obs.text:
        try:
            bb = await p.get_by_text(user).first.bounding_box()
            if bb:
                await p.mouse.click(bb['x'] + bb['width'] / 2, bb['y'] + bb['height'] / 2)
                await p.wait_for_timeout(900)
        except Exception as exc:
            print(f'[devserver] 点小孩卡片失败: {exc}')
    if path and path != '/':
        await p.goto(DEV_BASE + path)
    return p


# ==================== 主流程：确保服务就绪 ====================
# 直接以脚本方式运行（python tools/devserver.py）时只提示用法：
# exec 执行时内核不会注入 __file__，故以此区分，避免误判 __name__。
if '__file__' in globals() and os.path.abspath(globals().get('__file__')) == os.path.abspath(__file__):
    print('[devserver] 请用 exec(open(r"...\\tools\\devserver.py", encoding="utf-8").read()) '
          '在常驻内核中执行（shell 会话结束会杀掉子进程）；')
    print('[devserver] 手动启动服务请用项目根目录的「一键启动.bat」。')
    raise SystemExit(0)

_state = _read_state()
_reason = ''
_restart_reasons = []

if _is_up():
    if _state.get('port') != DEV_PORT:
        _restart_reasons.append('端口/状态不匹配')
    else:
        newest = _backend_mtime()
        if newest > _state.get('started_at', 0):
            _restart_reasons.append('后端代码已更新')
else:
    _restart_reasons.append('端口无服务')

if globals().get('DEV_FORCE_RESTART'):
    _restart_reasons.append('强制重启')

if _restart_reasons:
    _reason = '、'.join(_restart_reasons)
    _ok, _secs = dev_restart()
else:
    DEV_READY = True
    _ok, _secs = True, 0.0
    _reason = '复用现有服务'

if _ok:
    _pid = DEV_PROC.pid if DEV_PROC else _state.get('pid')
    print(f'[devserver] OK {DEV_BASE} ({_reason}; pid={_pid}; {_secs:.1f}s) log={LOG_PATH}')
    print("[devserver] 下一步: page = await dev_enter_app('/practice-sets')")
else:
    print(f'[devserver] FAIL 启动失败（{_reason}）log={LOG_PATH}')
    print(dev_log_tail(30))
    raise RuntimeError(f'devserver 启动失败: {_reason}')
