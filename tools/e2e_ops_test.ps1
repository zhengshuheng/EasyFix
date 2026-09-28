# EasyFix E2E Test Launcher (Ops Console)
$ErrorActionPreference = 'Continue'
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8
Set-Location 'E:\qianwenpaw\EasyFix-main'

Write-Host '============================================'
Write-Host ' EasyFix E2E Test Launcher - Ops Console'
Write-Host '============================================'
Write-Host '[1/2] Restart backend on port 8012'
& '.\一键重启.bat'
Write-Host '[2/2] Open ops console in browser'
Start-Process 'http://localhost:8012/ops/'
Write-Host ''
Write-Host 'Done! Wait 3-5 seconds then refresh.'
Write-Host 'Browser automation snippets: tools\e2e\ops_smoke.md'
Write-Host '============================================'
