@echo off
rem ops-dev: restart/start/stop/health (same as: python tools\ops_dev.py ...)
cd /d "%~dp0.."
python tools\ops_dev.py %*
