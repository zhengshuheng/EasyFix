# EasyFix 本地打包上传脚本（Windows 运行）
# 用法: powershell -ExecutionPolicy Bypass -File deploy\build_upload.ps1 -Server root@IP [-Domain easyfix.example.com] [-Email you@x.com] [-SkipDb]
param(
    [Parameter(Mandatory = $true)][string]$Server,   # 例如 root@1.2.3.4
    [string]$Domain = "",
    [string]$Email = "",
    [switch]$SkipDb
)

$ErrorActionPreference = "Stop"

# ===== 可调整 =====
$Root = "E:\qianwenpaw\EasyFix-main"
# =================

$Stage = Join-Path $env:TEMP "easyfix-deploy"
$Tar   = Join-Path $env:TEMP "easyfix-deploy.tar.gz"

Write-Host "[1/4] 收集文件..." -ForegroundColor Cyan
if (Test-Path $Stage) { Remove-Item -Recurse -Force $Stage }
New-Item -ItemType Directory -Force -Path $Stage | Out-Null

# backend 代码（排除运行时数据）
xcopy "$Root\backend" "$Stage\backend" /E /I /Q /Y | Out-Null
foreach ($ex in @("uploads", "__pycache__", ".pytest_cache")) {
    $p = Join-Path $Stage "backend\$ex"
    if (Test-Path $p) { Remove-Item -Recurse -Force $p }
}
Get-ChildItem "$Stage\backend" -Filter "*.db.pre-*" -Recurse -ErrorAction SilentlyContinue | Remove-Item -Force
Remove-Item (Join-Path $Stage "backend\devserver.log") -Force -ErrorAction SilentlyContinue
Remove-Item (Join-Path $Stage "backend\.devserver_state.json") -Force -ErrorAction SilentlyContinue
Remove-Item (Join-Path $Stage "backend\devscratch.log") -Force -ErrorAction SilentlyContinue

# 前端构建产物
xcopy "$Root\frontend\dist" "$Stage\frontend\dist" /E /I /Q /Y | Out-Null

# 部署脚本
New-Item -ItemType Directory -Force -Path "$Stage\deploy" | Out-Null
Copy-Item "$Root\deploy\install.sh"   "$Stage\deploy\"
Copy-Item "$Root\deploy\easyfix.service"   "$Stage\deploy\"
Copy-Item "$Root\deploy\nginx-easyfix.conf" "$Stage\deploy\"
Copy-Item "$Root\deploy\backup.sh"    "$Stage\deploy\"

# 数据库：默认带本地数据；更新服务器时用 -SkipDb
if (-not $SkipDb -and (Test-Path "$Root\backend\easyfix_main.db")) {
    Copy-Item "$Root\backend\easyfix_main.db" "$Stage\backend\easyfix_main.db"
    Write-Host "  已包含本地数据库 easyfix_main.db"
} else {
    Write-Host "  跳过数据库（全新部署或保留服务器数据）"
}

# PDF 中文字体：随包带 simhei.ttf，服务器通过 EASYFIX_FONT 使用
$fontSrc = "C:\Windows\Fonts\simhei.ttf"
if (Test-Path $fontSrc) {
    New-Item -ItemType Directory -Force -Path "$Stage\backend\fonts" | Out-Null
    Copy-Item $fontSrc "$Stage\backend\fonts\simhei.ttf"
    Write-Host "  已包含 PDF 字体 simhei.ttf"
} else {
    Write-Host "  [警告] 未找到 C:\Windows\Fonts\simhei.ttf，服务器将回退 fonts-noto-cjk"
}

# ===== 打包 =====
Write-Host "[2/4] 打包 tar.gz..." -ForegroundColor Cyan
if (Test-Path $Tar) { Remove-Item -Force $Tar }
Push-Location $Stage
tar -czf $Tar backend frontend deploy
if ($LASTEXITCODE -ne 0) { Pop-Location; throw "tar 打包失败" }
Pop-Location

$size = [math]::Round((Get-Item $Tar).Length / 1MB, 1)
Write-Host "  包大小: ${size} MB"

# ===== 上传 =====
Write-Host "[3/4] 上传到 $Server ..." -ForegroundColor Cyan
scp $Tar "$Server`:/tmp/easyfix-deploy.tar.gz"
if ($LASTEXITCODE -ne 0) { throw "scp 上传失败（检查 ssh 连通性/免密）" }

# ===== 远端执行 =====
Write-Host "[4/4] 远端安装..." -ForegroundColor Cyan
$cmd = "set -e; mkdir -p /opt/easyfix && tar -xzf /tmp/easyfix-deploy.tar.gz -C /opt/easyfix && bash /opt/easyfix/deploy/install.sh '$Domain' '$Email'"
ssh $Server $cmd
if ($LASTEXITCODE -ne 0) { throw "远端安装失败，见上方日志" }

Write-Host ""
Write-Host "部署完成！" -ForegroundColor Green
if ($Domain) {
    Write-Host "访问: https://$Domain"
} else {
    Write-Host "访问: http://<服务器IP>（无 HTTPS，语音输入不可用）"
}
Write-Host "收尾：阿里云安全组放行 80/443；进家长设置改家长密码。"
