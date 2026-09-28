# EasyFix 部署方式总览

> **语音输入（🎤）硬约束**：浏览器 `webkitSpeechRecognition` 只在 secure context 可用 —— **HTTPS 或 localhost 二选一**；公网 IP 直连 HTTP 不行（IP 签不了免费可信证书）。

| 方式 | 适合场景 | 语音输入 | 访问地址 | 入口 |
|---|---|---|---|---|
| **A. Windows 本机** | 个人本机使用 | ✅ localhost | http://localhost:8012 | 根目录 `一键启动.bat` |
| **B. 远端 Docker + Caddy** | 公网访问（推荐） | ✅ 需域名 | https://你的域名 | `deploy.bat`（配置区填 `DOMAIN`） |
| **C. 远端 Docker（无域名）** | 公网访问 | ❌ | http://IP:8012 | `deploy.bat`（DOMAIN 留空） |
| **D. systemd + Nginx**（本节下方） | 已有旧方案 | ✅ 需域名 | https://你的域名 | `deploy/build_upload.ps1` + `install.sh` |
| **E. Docker Compose（可选）** | 想用 compose 管理 | 同 B/C | 同 B/C | 根目录 `docker-compose.yml` |

## HTTPS 快速说明（方式 B）

1. 准备一个域名，DNS 控制台加 **A 记录**指向 ECS 公网 IP（先解析，再部署）。
2. 阿里云安全组放行 **80 / 443**。
3. 编辑 `deploy.bat` 配置区 `set "DOMAIN=你的域名"`，运行 `deploy.bat`。
4. Caddy 容器会自动申请并**自动续期** Let's Encrypt 证书（首次约 1-2 分钟），之后访问 `https://你的域名`，语音输入可用。

无域名时：只能 HTTP 直连，语音输入不可用；Windows 本机部署（方式 A）不受影响（localhost 天然 secure context）。

---

# 原方案：EasyFix 阿里云部署（ECS e 实例 2核2GB / Ubuntu 20.04+ / 3Mbps）—— 方式 D（systemd + Nginx）

> 以下为早期 systemd 方案（非 Docker），保留备用。新部署推荐方式 B（Docker + Caddy）。

个人/家庭自用部署包。包含：本地打包上传脚本（Windows）、服务器一键安装脚本、systemd 服务、Nginx 反代（HTTPS）、每日备份 cron。

## 架构

```
阿里云 ECS (2核2GB + 3Mbps + 40G 云盘, Ubuntu 22.04)
  └─ Nginx :443 (HTTPS, 反代) ──> uvicorn :8012 (127.0.0.1, systemd 守护)
       └─ FastAPI + SQLite(easyfix_main.db) + frontend/dist（同源托管）
```

- 3Mbps 对个人使用充足（首屏 ~1.6MB 一次加载，之后浏览器缓存；语音 MP3 每个 <30KB）
- 2GB 内存充足（fpdf2 轻量、OCR 走云端视觉 API 不占本地内存）；脚本会加 2GB swap 兜底
- **必须 HTTPS**：做题页「🎤 语音输入」用浏览器 `webkitSpeechRecognition`，非 HTTPS 不可用

## 部署步骤

### 1. 本地准备（Windows）

编辑 `backend/.env`，填好你自己的 API keys（只改键值，别动其他行）：

```ini
# LLM 出题（deepseek 兼容 OpenAI 协议）
OPENAI_API_KEY=sk-xxxx
OPENAI_BASE_URL=https://api.deepseek.com/v1
LLM_MODEL=deepseek-chat

# 视觉 OCR（拍照导入题目；国内推荐阿里云百炼 qwen-vl-max）
MULTIMODAL_PROVIDER=qwen
QWEN_API_KEY=sk-xxxx
QWEN_VISION_MODEL=qwen-vl-max

# TTS 走有道词典（免费，无需 key）
```

然后运行打包上传（需要本机已装 OpenSSH Client，Windows 10/11 自带）：

```powershell
cd E:\qianwenpaw\EasyFix-main
powershell -ExecutionPolicy Bypass -File deploy\build_upload.ps1 -Server root@你的服务器IP
```

脚本会把 `backend`（含 easyfix_main.db 本地数据、speech_models）、`frontend/dist`、部署脚本打成一个 tar 包
传到服务器并自动执行安装。参数：

| 参数 | 说明 |
|---|---|
| `-Server` | 必填，`用户@IP`（如 `root@1.2.3.4`） |
| `-Domain` | 可选，你的域名（如 `easyfix.example.com`）。**有域名才能自动申请 HTTPS 证书** |
| `-Email` | 可选，certbot 证书通知邮箱 |
| `-SkipDb` | 加此开关则不打包本地 easyfix_main.db（全新部署） |

> 无域名也可以部署（80 端口直连），但「🎤 语音输入」不可用，其余功能正常。

首次上传约 93MB（含前端产物、语音模型、本地数据），在 3Mbps 入网带宽下约 4-5 分钟，
属正常现象；之后日常更新（`-SkipDb`）约 60-90 秒。

### 2. 服务器侧（install.sh 自动完成，不用手动）

自动执行：系统依赖 → venv + pip 依赖 → 固定监听 127.0.0.1:8012 → 2GB swap →
systemd 服务 → Nginx 反代 →（有域名时）certbot 自动申请证书 → 自检 API → 每日备份 cron。

### 3. 收尾

- 阿里云控制台 **安全组**放行 80/443（HTTPS 必须 443）
- 如果域名没解析到服务器，先去 DNS 控制台加 A 记录，**先解析再运行 install.sh**
- 登录系统后：进入「家长设置」修改家长密码；首次使用按激活码授权流程激活
- 数据备份在服务器 `/opt/easyfix-backups/`（每日自动，保留 7 天），需要更稳可配 ossutil 同步 OSS

## 日常运维

```bash
sudo systemctl status easyfix        # 查看服务状态
sudo systemctl restart easyfix       # 重启（改后端代码后）
sudo journalctl -u easyfix -n 100    # 看日志
bash /opt/easyfix/deploy/backup.sh   # 手动备份一次
```

更新版本：本地 `npm run build` 后重新打包上传（会覆盖 /opt/easyfix，数据库保留在
`backend/easyfix_main.db`，注意上传包默认带 db 会覆盖服务器数据——**更新时用 `-SkipDb`**）。

## 已知注意点

1. **PDF 中文字体**：本地 `C:/Windows/Fonts/simhei.ttf` 会自动随包上传到
   `backend/fonts/simhei.ttf`，服务器上通过 `EASYFIX_FONT` 生效；未携带时回退
   `fonts-noto-cjk`（ttc 格式，fpdf2 兼容性一般，建议带上 simhei.ttf）。
2. **e 实例是突发性能 CPU（积分制）**：低频个人使用无感；长时间高负载会被限流。
3. **磁盘**：教材下载 + 照片积累会增长，关注 `du -sh /opt/easyfix/backend`，必要时挂数据盘。
4. **SQLite 并发**：个人/家庭 1-3 并发无压力，不需要换 MySQL。
5. 首次上传如果 scp 要输密码，建议先 `ssh-copy-id` 配置免密，后续更新方便。
