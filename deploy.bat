@echo off
rem ==========================================
rem  EasyFix one-click deploy (entry)
rem  Runs deploy.ps1 via PowerShell so that
rem  errors stay visible (no flash-close) and
rem  Chinese text renders correctly.
rem
rem  Usage:
rem    deploy.bat                deploy (asks domain on first run, remembers it)
rem    deploy.bat skipdb         daily update (no local db, keep server data)
rem    deploy.bat domain         re-set domain (overwrite saved config)
rem    deploy.bat resetdomain    clear domain config (ask again next deploy)
rem ==========================================

powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0deploy.ps1" %*

if errorlevel 1 (
    echo.
    echo [FAILED] Deploy failed - please read the errors above.
    echo Press any key to close this window...
    pause >nul
)
