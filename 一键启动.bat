@echo off
title EasyFix 学习软件 - 一键启动
cd /d "%~dp0"

echo ============================================
echo   EasyFix 学习软件 一键启动
echo ============================================
echo.

REM ---------- 从配置文件读取端口（backend\.env 中的 PORT）----------
set "HOST=0.0.0.0"
set "PORT=8000"
if exist "backend\.env" (
    for /f "usebackq tokens=1,* delims== eol=#" %%a in ("backend\.env") do (
        if /i "%%a"=="HOST" set "HOST=%%b"
        if /i "%%a"=="PORT" set "PORT=%%b"
    )
)
set "HOST=%HOST: =%"
set "PORT=%PORT: =%"
echo   [配置] 监听地址: %HOST%    端口: %PORT%  (修改 backend\.env 后重启生效)
echo.

REM ---------- 使用项目内虚拟环境 .venv ----------
set "PY=%~dp0.venv\Scripts\python.exe"
if not exist "%PY%" (
    echo   [错误] 未找到项目虚拟环境 .venv
    echo          请先执行: uv venv .venv --python 3.12
    echo                   uv pip install -r backend\requirements.txt
    pause
    exit /b 1
)

REM ---------- 检查端口是否被占用 ----------
netstat -ano | findstr ":%PORT% " | findstr "LISTENING" >nul 2>&1
if not errorlevel 1 (
    echo   [提示] 端口 %PORT% 已被其它程序占用！
    echo          请修改 backend\.env 中的 PORT 后重新启动。
    pause
    exit /b 1
)

REM ---------- 启动后端（含前端页面）----------
echo   [启动] 正在启动服务，请稍候...
start "EasyFix-Backend" /d "%~dp0backend" "%PY%" -m uvicorn app.main:app --host %HOST% --port %PORT%

REM 等待服务就绪（最多 30 秒）
set "READY="
for /l %%i in (1,1,30) do (
    timeout /t 1 /nobreak >nul 2>&1
    curl -s -o nul http://127.0.0.1:%PORT%/health 2>nul && set "READY=1" && goto :ready
)
:ready
if defined READY (
    echo   [完成] 服务已启动！
    echo.
    echo   访问地址: http://localhost:%PORT%/
    echo.
    set /p "OPEN=按回车键自动打开浏览器..."
    start http://localhost:%PORT%/
) else (
    echo   [警告] 服务启动超时，请查看后端窗口中的日志确认状态。
    pause
)
