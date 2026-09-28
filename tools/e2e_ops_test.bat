@echo off
cd /d E:\qianwenpaw\EasyFix-main
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0e2e_ops_test.ps1"
pause
