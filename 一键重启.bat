@echo off
title EasyFix Restart
cd /d "%~dp0"

echo ============================================
echo   EasyFix RESTART  (kill old process, then start)
echo ============================================
echo.

REM ---------- read PORT from backend\.env ----------
set "HOST=0.0.0.0"
set "PORT=8012"
if exist "backend\.env" (
    for /f "usebackq tokens=1,* delims== eol=#" %%a in ("backend\.env") do (
        if /i "%%a"=="HOST" set "HOST=%%b"
        if /i "%%a"=="PORT" set "PORT=%%b"
    )
)
set "HOST=%HOST: =%"
set "PORT=%PORT: =%"
echo   Listen: %HOST%  Port: %PORT%

REM ---------- kill whatever is listening on the port ----------
echo.
echo   [1/3] Killing process on port %PORT% ...
for /f "tokens=5" %%p in ('netstat -ano ^| findstr ":%PORT% " ^| findstr "LISTENING"') do (
    echo          killing PID %%p
    taskkill /F /PID %%p >nul 2>&1
)
REM also kill stale EasyFix-Backend windows by title
taskkill /F /FI "WINDOWTITLE eq EasyFix-Backend*" >nul 2>&1

REM ---------- wait until port is free ----------
set "FREE="
for /l %%i in (1,1,15) do (
    netstat -ano | findstr ":%PORT% " | findstr "LISTENING" >nul 2>&1
    if errorlevel 1 set "FREE=1" & goto :free
    timeout /t 1 /nobreak >nul 2>&1
)
:free
if not defined FREE (
    echo   [WARN] port %PORT% still busy after 15s, continue anyway
)

REM ---------- use project .venv ----------
set "PY=%~dp0.venv\Scripts\python.exe"
if not exist "%PY%" (
    echo   [ERROR] .venv not found: %PY%
    pause
    exit /b 1
)

REM ---------- start backend ----------
echo.
echo   [2/3] Starting backend ...
start "EasyFix-Backend" /d "%~dp0backend" "%PY%" -m uvicorn app.main:app --host %HOST% --port %PORT%

REM ---------- health check (max 30s) ----------
set "READY="
for /l %%i in (1,1,30) do (
    timeout /t 1 /nobreak >nul 2>&1
    curl -s -o nul http://127.0.0.1:%PORT%/health 2>nul && set "READY=1" && goto :ready
)
:ready
if defined READY (
    echo   [3/3] Server ready: http://localhost:%PORT%/
) else (
    echo   [3/3] Timed out waiting for /health; check the log window
)
echo.
echo   Done.
timeout /t 3 /nobreak >nul 2>&1
exit /b 0
