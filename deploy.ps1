# ==========================================
#  IMPORTANT: This file MUST be saved as UTF-8 with BOM.
#  Windows PowerShell 5.1 decodes BOM-less files as ANSI/GBK,
#  which garbles the Chinese text and breaks if/else syntax.
#  If it ever breaks after an edit, re-save it with BOM.
# ==========================================
#  一键自动化部署脚本 (deploy.ps1) — Docker + Caddy 方式
#  由 deploy.bat 调用（本脚本用 PowerShell 执行，避免 bat 编码/闪退问题）
#
#  用法：
#    deploy.bat               部署（交互询问域名 + 是否跳过本地数据库；配置自动记住）
#    deploy.bat skipdb        日常更新（跳过询问，不带本地库，防止覆盖服务器数据）
#    deploy.bat domain        重新设置域名（覆盖已保存的配置）
#    deploy.bat resetdomain   清除域名配置（下次部署重新询问）
# ==========================================

# --- 1. 修改以下配置 ---
$ECS_IP         = "47.112.13.123"
$ECS_USER       = "root"
$REMOTE_DIR     = "/opt/easyfix"          # 远端代码目录（Dockerfile 在此构建）
$DATA_DIR       = "/opt/easyfix-data"     # 远端数据目录（db/uploads/data/caddy 持久化）
$IMAGE_NAME     = "easyfix"
$CONTAINER_NAME = "easyfix"
$HOST_PORT      = 8012                    # 对外直连端口（与本地/容器一致，公网 http://IP:8012）
$CONTAINER_PORT = 8012                    # 容器内后端端口（与 backend/.env 的 PORT 一致）
$SSH_KEY        = Join-Path $env:USERPROFILE ".ssh\id_rsa_ecs"

# --- 2. 参数处理（兼容 bat 传参） ---
$SkipDb = $false; $ResetDomain = $false; $ForceDomain = $false
if ($args -contains "skipdb")      { $SkipDb = $true }
if ($args -contains "resetdomain") { $ResetDomain = $true }
if ($args -contains "domain")      { $ForceDomain = $true }

$Root        = $PSScriptRoot
$DOMAIN_CONF = Join-Path $Root "deploy\domain.conf"

if ($ResetDomain) {
    if (Test-Path $DOMAIN_CONF) { Remove-Item $DOMAIN_CONF -Force }
    Write-Host "已清除域名配置，下次部署会重新询问。"
    exit 0
}

# --- 3. 域名配置（交互式，保存后自动记住） ---
$DOMAIN = ""
if ($ForceDomain -or -not (Test-Path $DOMAIN_CONF)) {
    Write-Host ""
    Write-Host "  域名配置（HTTPS 语音输入需要域名；没有可以跳过）"
    Write-Host "  有域名：输入后自动启用 HTTPS 并记住，下次部署不再询问"
    Write-Host "  没有域名：直接回车跳过（HTTP 模式，语音输入不可用）"
    $DOMAIN = Read-Host "请输入域名（回车跳过）"
    Set-Content -Path $DOMAIN_CONF -Value $DOMAIN -Encoding ASCII
    if ($DOMAIN) { Write-Host "  已记住域名: $DOMAIN，本次按 HTTPS 部署" }
    else         { Write-Host "  已记住：无域名。以后要启用 HTTPS 请运行: deploy.bat domain" }
}
elseif ((Get-Content $DOMAIN_CONF -Raw -ErrorAction SilentlyContinue).Trim()) {
    $DOMAIN = (Get-Content $DOMAIN_CONF -Raw).Trim()
    Write-Host "  使用已保存的域名: $DOMAIN （deploy.bat domain 可修改）"
}
else {
    Write-Host "  使用已保存的配置：无域名（HTTP 模式，语音输入不可用）"
}
Write-Host ""

# --- 4. 数据库选择（交互式；命令行传 skipdb 则跳过询问） ---
if (-not $SkipDb) {
    Write-Host "  数据库选择："
    Write-Host "  默认【带本地数据库】上传（首次部署用这个，会初始化种子题库）"
    Write-Host "  日常更新选跳过——保留服务器上的数据，不被本地库覆盖"
    $dbChoice = Read-Host "  是否跳过本地数据库（保留服务器数据）？[y/N，回车=带库]"
    if ($dbChoice -match '^[yY]') { $SkipDb = $true }
}
if ($SkipDb) { Write-Host "  已选择：跳过本地数据库（保留服务器数据）" }
else         { Write-Host "  已选择：带本地数据库（首次部署）" }
Write-Host ""

# --- 5. 部署流程 ---
Write-Host "=========================================="
Write-Host "  一键自动化部署流程 (Docker)"
Write-Host "=========================================="
Write-Host ""

# [0/5] 检查本机后端服务是否正在运行（会锁住 easyfix_main.db 导致打包失败）
$listener = Get-NetTCPConnection -LocalPort $CONTAINER_PORT -State Listen -ErrorAction SilentlyContinue
if ($listener) {
    Write-Host ""
    Write-Host "[警告] 检测到本机 EasyFix 后端服务正在运行（端口 $CONTAINER_PORT，PID $($listener.OwningProcess)）。" -ForegroundColor Yellow
    Write-Host "       该服务会锁住 backend\easyfix_main.db，导致打包失败（tar: Permission denied）。" -ForegroundColor Yellow
    Write-Host "       请先关闭服务（如一键启动.bat 的窗口，或 taskkill /PID $($listener.OwningProcess) /F）再部署。" -ForegroundColor Yellow
    Write-Host "       按回车继续（可能仍会打包失败），或按 Ctrl+C 取消..." -ForegroundColor Yellow
    Read-Host
    Write-Host ""
}

# [1/5] 本地构建前端（前端源码不进包，只带构建产物 dist + dist-trial）
Write-Host "[1/5] 本地构建前端 (npm run build + build:trial)..."
Push-Location (Join-Path $Root "frontend")
if (Test-Path "node_modules") {
    npm run build > $null 2>&1
    $buildRc = $LASTEXITCODE
    if ($buildRc -ne 0) {
        Pop-Location
        Write-Host ""
        Write-Host "[失败] 前端构建失败（npm run build 退出码 $buildRc）。" -ForegroundColor Red
        Write-Host "       请先检查 frontend 代码错误，修复后重新部署。" -ForegroundColor Red
        exit 1
    }
    npm run build:trial > $null 2>&1
    $trialRc = $LASTEXITCODE
    if ($trialRc -ne 0) {
        Pop-Location
        Write-Host ""
        Write-Host "[失败] 试用版前端构建失败（npm run build:trial 退出码 $trialRc）。" -ForegroundColor Red
        Write-Host "       请先检查 frontend 代码错误（试用版独立配置 vite.trial.config.js），修复后重新部署。" -ForegroundColor Red
        exit 1
    }
    Write-Host "  前端构建成功（frontend/dist 与 frontend/dist-trial 已更新）"
    npm run build:ops > $null 2>&1
    $opsRc = $LASTEXITCODE
    if ($opsRc -ne 0) {
        Pop-Location
        Write-Host ""
        Write-Host "[失败] 运营后台前端构建失败（npm run build:ops 退出码 $opsRc）。" -ForegroundColor Red
        Write-Host "       请先检查 frontend/ops 代码错误（独立配置 vite.ops.config.js），修复后重新部署。" -ForegroundColor Red
        exit 1
    }
    Write-Host "  运营后台前端构建成功（frontend/dist-ops 已更新）"
} else {
    Pop-Location
    Write-Host "  [警告] frontend/node_modules 不存在，跳过前端构建（使用已有的 frontend/dist 与 dist-trial）" -ForegroundColor Yellow
}

# [1.5/5] 导出 ops 权威数据（语法教程/激励配置；远端容器启动后幂等同步进云端主库）
Write-Host "[1.5/5] 导出 ops 权威数据 (deploy/ops_data.sql)..."
Push-Location $Root
python tools/deploy_export_ops.py
$opsRc = $LASTEXITCODE
Pop-Location
if ($opsRc -ne 0) {
    Write-Host "  [警告] ops 权威数据导出失败（跳过；云端不会同步最新配置。可手动运行: python tools/deploy_export_ops.py）" -ForegroundColor Yellow
} else {
    Write-Host "  ops 权威数据已导出（远端自动同步）"
}

# [1.6/5] 导出权威词表（公开牛津深圳版 12 册；远端容器启动后幂等 upsert 进云端主库）
Push-Location $Root
python tools/deploy_export_words.py
$wordsRc = $LASTEXITCODE
Pop-Location
if ($wordsRc -ne 0) {
    Write-Host "  [警告] 权威词表导出失败（跳过；云端不会同步权威词表。可手动运行: python tools/deploy_export_words.py）" -ForegroundColor Yellow
} else {
    Write-Host "  权威词表已导出（远端自动同步）"
}

# [2/5] 清理并打包本地代码
Write-Host "[2/5] 清理并打包本地代码..."
$pkg = Join-Path $Root "deploy_package.tar.gz"
if (Test-Path $pkg) { Remove-Item $pkg -Force }
$TAR_EXCLUDES = @(
    "--exclude=venv", "--exclude=.venv", "--exclude=__pycache__", "--exclude=.git",
    "--exclude=frontend/node_modules", "--exclude=deploy.bat", "--exclude=deploy.ps1",
    "--exclude=deploy_package.tar.gz", "--exclude=backend/easyfix_main.db.pre-*",
    "--exclude=backend/trial_data",  # 空间库/注册表/模板不进部署包（容器挂载数据卷持久化）
    "--exclude=backend/devserver.log", "--exclude=backend/.devserver_state.json", "--exclude=backend/browser*.log",
    "--exclude=backend/test.pdf", "--exclude=backend/test_decode.txt", "--exclude=tools/tmp"  # 本地临时产物，可能被本地服务锁住导致 tar Permission denied
)
if ($SkipDb) { $TAR_EXCLUDES += "--exclude=backend/easyfix_main.db" }

Push-Location $Root
tar -czf deploy_package.tar.gz $TAR_EXCLUDES .
$rc = $LASTEXITCODE
Pop-Location
if ($rc -ne 0) {
    Write-Host ""
    Write-Host "[失败] 本地打包出错（tar 退出码 $rc）。" -ForegroundColor Red
    Write-Host "       常见原因：EasyFix 后端服务正在运行，锁住了 backend\easyfix_main.db（Permission denied）。" -ForegroundColor Red
    Write-Host "       解决：先关闭本机服务（一键启动.bat 窗口 / 8012 端口进程）再重新部署。" -ForegroundColor Red
    Write-Host "       如果只是日常更新不需要本地题库，可改用: deploy.bat skipdb" -ForegroundColor Red
    exit 1
}

# [3/5] 创建远程目录并上传代码
Write-Host ""
Write-Host "[3/5] 创建远程目录并上传代码到 ECS ($ECS_IP)..."
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=accept-new "$ECS_USER@$ECS_IP" "mkdir -p $REMOTE_DIR $DATA_DIR/uploads $DATA_DIR/data $DATA_DIR/caddy"
scp -i "$SSH_KEY" "$pkg" "$($ECS_USER)@$($ECS_IP):$REMOTE_DIR/"
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[失败] 上传失败，请检查网络或 SSH 免密配置！" -ForegroundColor Red
    exit 1
}

# [4/5] SSH 远程构建并启动（easyfix + caddy）
# 先解压上传的 tar 包（首次部署时 /opt/easyfix/deploy/remote_deploy.sh 尚不存在），再执行
Write-Host ""
Write-Host "[4/5] 连接 ECS 并执行部署命令..."
ssh -i "$SSH_KEY" "$ECS_USER@$ECS_IP" "cd $REMOTE_DIR; tar -xzf deploy_package.tar.gz; sed -i 's/\r$//' deploy/remote_deploy.sh; bash deploy/remote_deploy.sh $DOMAIN"
if ($LASTEXITCODE -ne 0) {
    Write-Host ""
    Write-Host "[失败] 远程部署命令执行失败，请查看上方错误信息。" -ForegroundColor Red
    exit 1
}

# 清理本地临时文件
if (Test-Path $pkg) { Remove-Item $pkg -Force }

Write-Host ""
Write-Host "=========================================="
if ($DOMAIN) {
    Write-Host "  部署完成！访问地址: https://$DOMAIN"
}
else {
    Write-Host "  部署完成！访问地址: http://$($ECS_IP):$HOST_PORT"
}
Write-Host "=========================================="
Write-Host ""
Write-Host "  [提示] 公网打不开请检查阿里云安全组："
Write-Host "         ECS 控制台 -> 安全组 -> 入方向放行 $HOST_PORT（有域名时再放行 80 / 443）"
Write-Host "  [提示] 首次打开网页后，进「家长设置」修改家长密码。"
Write-Host ""
exit 0
