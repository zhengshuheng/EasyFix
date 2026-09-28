# -*- coding: utf-8 -*-
"""ops-dev：一键重启/启动 8012 服务 + 打开浏览器（编码 agent 与用户共用）。

用法（cmd / PowerShell 均可）：
    python tools\\ops_dev.py restart [--url http://localhost:8012/ops/#/kp] [--browser auto|chrome|none]
    python tools\\ops_dev.py start    [--url ...]     # 仅启动（不杀旧进程）
    python tools\\ops_dev.py stop                     # 仅停止 8012
    python tools\\ops_dev.py health                   # 仅健康检查

说明：
    * 服务以 DETACHED 进程启动（脱离调用者会话），日志写 tools/tmp/uvicorn.log
    * 自动杀旧端口进程 → 等 /health 200（最长 60s）→ 打开浏览器
    * --browser auto：优先 Chrome，找不到回退系统默认浏览器；none = 不打开
"""
import argparse
import os
import subprocess
import sys
import time
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 项目根
BACKEND = os.path.join(ROOT, "backend")
PYTHON = os.path.join(ROOT, ".venv", "Scripts", "python.exe")
LOG = os.path.join(ROOT, "tools", "tmp", "uvicorn.log")


def log(msg):
    print(f"[ops-dev] {msg}")


def find_pids(port):
    try:
        out = subprocess.run(["netstat", "-ano"], capture_output=True, text=True, timeout=10).stdout
    except Exception as e:
        log(f"netstat 失败: {e}")
        return []
    pids = set()
    for line in out.splitlines():
        if f":{port}" in line and "LISTENING" in line.upper():
            parts = line.split()
            if parts:
                pids.add(parts[-1])
    return sorted(pids)


def stop(port):
    pids = find_pids(port)
    if not pids:
        log(f"端口 {port} 无监听进程")
        return
    for pid in pids:
        log(f"停止 PID {pid}")
        subprocess.run(["taskkill", "/F", "/PID", pid], capture_output=True, text=True)
    time.sleep(1.5)


def start(port, host="0.0.0.0", svc=False):
    os.makedirs(os.path.join(ROOT, "tools", "tmp"), exist_ok=True)
    if svc:
        # 计划任务托管：进程由 Task Scheduler 维护，脱离调用者会话（agent 会话也可跨命令存活）
        task = "EasyFixBackend"
        pythonw = os.path.join(ROOT, ".venv", "Scripts", "pythonw.exe")
        if not os.path.exists(pythonw):
            pythonw = PYTHON
        cmd = f'cmd /c cd /d "{BACKEND}" && "{pythonw}" -m uvicorn app.main:app --host {host} --port {port} >> "{LOG}" 2>&1'
        subprocess.run(["schtasks", "/create", "/tn", task, "/tr", cmd,
                        "/sc", "once", "/st", "00:00", "/f"],
                       capture_output=True, text=True)
        r = subprocess.run(["schtasks", "/run", "/tn", task], capture_output=True, text=True)
        log(f"计划任务 {task} 已启动（Task Scheduler 托管）")
        return None
    with open(LOG, "w", encoding="utf-8") as f:
        p = subprocess.Popen(
            [PYTHON, "-m", "uvicorn", "app.main:app", "--host", host, "--port", str(port)],
            cwd=BACKEND,
            stdout=f, stderr=f,
            creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP,
            close_fds=True,
        )
    log(f"服务已启动 PID {p.pid}（日志 {LOG}）")
    return p.pid


def wait_health(port, timeout=60):
    url = f"http://127.0.0.1:{port}/health"
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            with urllib.request.urlopen(url, timeout=3) as r:
                if r.status == 200:
                    log(f"健康检查通过（{time.time() - t0:.1f}s）")
                    return True
        except Exception:
            pass
        time.sleep(1)
    log(f"健康检查超时（{timeout}s），看日志: {LOG}")
    return False


def open_browser(url, browser):
    if browser == "none":
        log(f"浏览器未打开（--browser none），访问: {url}")
        return
    try:
        if browser in ("auto", "chrome"):
            for env in ("PROGRAMFILES", "PROGRAMFILES(X86)"):
                cand = os.path.join(os.environ.get(env, ""), "Google", "Chrome", "Application", "chrome.exe")
                if os.path.exists(cand):
                    subprocess.Popen([cand, url],
                                     creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NEW_PROCESS_GROUP)
                    log(f"已用 Chrome 打开: {url}")
                    return
            if browser == "chrome":
                log("未找到 Chrome")
                return
        os.startfile(url)  # 系统默认浏览器
        log(f"已打开: {url}")
    except Exception as e:
        log(f"打开浏览器失败: {e}")


def main():
    ap = argparse.ArgumentParser(description="ops-dev：重启/启动 8012 服务 + 打开浏览器")
    ap.add_argument("action", choices=["restart", "start", "stop", "health"], nargs="?", default="restart")
    ap.add_argument("--port", type=int, default=8012)
    ap.add_argument("--url", default="http://localhost:8012/ops/")
    ap.add_argument("--browser", default="auto", choices=["auto", "chrome", "none"])
    ap.add_argument("--svc", action="store_true", help="用计划任务托管服务（推荐：跨会话/重启机器后仍可用，需一次创建任务）")
    args = ap.parse_args()

    if args.action == "stop":
        stop(args.port)
        return
    if args.action == "health":
        ok = wait_health(args.port, timeout=10)
        sys.exit(0 if ok else 1)
    if args.action in ("restart", "start"):
        if args.action == "restart":
            stop(args.port)
        start(args.port, svc=args.svc)
        if not wait_health(args.port):
            sys.exit(1)
        open_browser(args.url, args.browser)


if __name__ == "__main__":
    main()
