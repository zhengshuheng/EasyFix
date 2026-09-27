# AI 工作上下文速查（AI_CONTEXT）

> 给模型看的"本仓库常识"：容易返工、踩坑、跨会话丢失的关键逻辑。
> 每次改 EasyFix 代码前先扫一遍本文件 + `../AGENTS.md`。架构细节看 `../ARCHITECTURE.md`。

## 0. 铁律（违反必返工）

- **根目录禁止新增任何 .md**（README/AGENTS/CLAUDE/CHANGELOG 除外）。任务文档 → `docs/tasks/active/`，完成 → `done/`（见 `CONVENTIONS.md`）。
- **临时脚本/截图/产物** → `tools/tmp/`，会话收尾跑 `python tools/cleanup.py` 清空。
- **禁止在请求体传 user_id**；孩子身份一律 `X-Kid-Id` 头（`app/utils/kid_context.py`）。查询必须 `deleted=False` 过滤（软删除）。
- **改表结构**：无迁移系统，SQLite 删 `backend/easyfix_main.db` 重建（**数据会丢**，谨慎）；MySQL 手动改表。

## 1. 运行环境（易错）

- 后端端口：`backend/.env` 里 `PORT=8012`（**不是 8000**）。启动：`cd backend && ..\.venv\Scripts\python.exe -m uvicorn app.main:app --port 8012`（用项目 `.venv`，系统 python 缺依赖）。
- 前端：`cd frontend && npm run build`（产物 dist/，由后端托管）。开发 dev server 走 5173。
- **SQLite 路径是相对 cwd 的**：跑后端脚本必须在 `backend/` 目录下执行，否则连到空库报 `no such table`。
- 数据库：`backend/easyfix_main.db`（主库/正式库）。表名：`practice_question`（345+ 题）、`assessment_record`、`user`（家长+小孩同表，role=child）、`knowledge_point` 等。
- **`deploy.ps1` 必须保存为 UTF-8 with BOM**：PowerShell 5.1 读无 BOM 的 .ps1 按 ANSI/GBK 解码 → 中文乱码、乱码字节里"变出"引号/花括号把 if/else 砸断（`else` 被当命令名报错）。改完若丢 BOM：`[System.IO.File]::WriteAllText($p,$c,(New-Object System.Text.UTF8Encoding($true)))` 重写回 BOM + `Parser::ParseFile` 验证零错误（`powershell -NoProfile -Command` 内联执行）。

## 1.5 试用多租户（trial，2026-09-23 模板库重构）

- **架构三件套**（`backend/app/trial.py`）：
  - 模板库 `backend/trial_data/template.db`：预置 40 表 + 基础数据 + 题库/单词/拼读/阅读/知识点 + 占位家长(id=1, role=admin) + 演示小孩(id=2, role=child)，题库 `practice_question.user_id` 全归 id=2。**仅首次启动生成**（`main.py` 模块级调 `ensure_template_db()`，~10s），之后秒开。
  - **创建租户 = `shutil.copy(template.db → tenants/{key}.db)` + 2 条 UPDATE**（占位家长 username/password_hash、演示小孩 display_name）→ 注册 **0.7s**（旧 create_all 方案 10-12s）。
  - 注册表 = 独立 db `backend/trial_data/registry.db`（表 `tenants`: key/username UNIQUE/password_hash/child_name/db_path/created_at），替代早期 registry.json；`get_registered_user`/`is_trial_key`/`_save_registered` 都查它（SQLite 自带并发安全）。
- **用户表名是 `users` 不是 `user`**（正式库 `user` 单数，租户库 create_all 生成的是 `users` 复数——**不要跨库写死表名**）。
- **坑（实测翻车）**：
  - `tenant_factory(key)` 返回 sessionmaker **没有 `.bind`** → `Base.metadata.create_all(bind=te)` 必须用 `register_tenant_engine()` 的返回值（它 return engine）。
  - 模板生成后必须 `PRAGMA wal_checkpoint(TRUNCATE)` + `engine.dispose()` 再复制主文件，否则 WAL 未落盘丢数据；复制只拿 `template.db` 主文件（忽略 -wal/-shm）。
  - 模板引擎缓存用完 `pop`（`db_mod._tenant_engines.pop(TEMPLATE_KEY)`），防重试时指向已删除的 tmp 文件。
  - **execute_shell_command 每次调用结束会杀光子进程树**（DETACHED_PROCESS 也逃不掉）→ 后台长驻服务用 `wmic process call create "cmd /c ..."` 启动（进程独立存活）；验证端口用 `netstat -ano | findstr :8013`。
  - 浏览器端到端：官网 `http://127.0.0.1:8013/site/#trial` 注册 → 跳 `/grgoH_xxx/#/` 显示"今天谁学习？"+ 孩子卡片（模板预置孩子改名生效）。

## 1.6 体验-角色-升级-配置（2026-09-23，阶段 A 后端全绿 15/15）

- **角色体系**：`accounts.role`（parent 默认/org）+ `accounts.child_name`。模板库加 **id=3 空数据小孩「新同学」**（仅错题本空壳，无题库）→ 旧模板库幂等补插 `_ensure_template_demo_children`。建空间时：家长 = 体验小朋友(id=2) + 自己小孩(id=3 改名 child_name)；机构 = 删 id=3（先清其 error_books 再 `db.delete`，SQLite FK OFF 需手动清）。
- **体验期**：`spaces.trial_end_at`（= 创建时间 + `app_config.trial_days`，NULL=正式）。`_compute_trial_end_at()` 用主库 SessionLocal 读配置。
- **配置表** `app_config`（key/value，默认：trial_days=15 / online_price=100 / local_price=50 / local_download_url / local_guide_url / ops_password=easyfix-ops）。API：`GET /api/config/public`（公开）、`GET|PUT /api/ops/config`（X-Ops-Password 口令）。
- **升级**：`POST /api/subscription/upgrade {plan: online|local}`（Bearer account token）→ `subscription_plan`=pro_online/pro_local + `upgrade_account_spaces()` 把名下空间 trial_end_at 置 NULL。
- **`GET /api/trial/status`（X-Trial-Key）**：剩余天数/expired/is_pro + 价格配置（空间内倒计时条用）。
- **坑（实测翻车）**：
  - **带 X-Trial-Key 的请求，`get_db` 分发到空间库** → 读 `app_config`（在主库）必须用 `SessionLocal()` 直连主库，不能用 `Depends(get_db)`（否则 `no such table: app_config`）。
  - **弱密码黑名单**会拦 `abc12345` 这类测试密码 → 测试用 `Abc@12345`（含大写+特殊字符）。
  - 测试服务启动：DETACHED_PROCESS 也随 execute_shell_command 会话被杀 → 用单命令内 Popen + 轮询 + 测试 + terminate 一体脚本（`tools/tmp/test_next_api.py`，端口 8016）；项目依赖用 `.venv\Scripts\python.exe`（系统 python 缺 fpdf）。
  - 测试账号残留会撞唯一键 → 用户名带时间戳 + `tools/tmp/cleanup_test_data.py` 清理（`DELETE accounts WHERE username LIKE 't_%'` + registry spaces + 空间 db 文件）。

## 1.7 官网阶段 B（2026-09-23，前端面板/升级弹层/运营后台全绿）

- **官网面板**（`frontend/site/app.js`）：登录后 `refreshStatus(user, space)` 显示体验剩余天数（`daysBetween(trial_end_at)`）/已过期/正式版徽章 + 升级按钮；未建空间显示"体验空间创建后将开始计算 15 天免费体验"。
- **升级弹层**（index.html #upgradeModal）：套餐 online(¥100/年)/local(¥50)（价格来自 `/api/config/public` 缓存 `publicConfig`）→ 选套餐更新 `#payAmount` →「我已支付完成」`POST /api/subscription/upgrade {plan}` → 成功 `GET /api/account/me` 刷新面板；local 成功追加下载链接（`r.download_url`，30s 消失）。
- **注册表单**：角色 select（parent/org）+ 小孩昵称（org 时隐藏 `#regChildNameWrap`）；提交带 `role`/`child_name`。
- **运营后台** `frontend/site/ops.html` + `ops.js`：口令（X-Ops-Password）→ GET 配置填表 → PUT 保存（改口令后内存 `window.opsPassword` 同步）。入口在官网 footer「· 运营」。
- **坑（实测翻车）**：
  - **`.btn { display:inline-flex }` 覆盖 HTML hidden 属性** → 全局 `[hidden] { display:none !important }` 仍不够（浏览器旧 CSS 缓存不重新请求）；改 style.css 后必须**给 href 加版本参数**（`style.css?v=20260923`，index.html 与 ops.html 同步），否则验证时旧样式在飞。
  - **dist-trial 空间页 401 时执行 `localStorage.removeItem("easyfix_token"/"easyfix_user")`** → 进空间后回官网登录态被清（阶段 C 要做官网 token 与空间页隔离；当前已知行为，验证时用「登录已有账号、不创建空间跳转」绕开）。
  - wmic process call create 起的测试服务：**taskkill 杀父 cmd 杀不死 uvicorn 子进程**（还占端口/库文件）→ 用 `wmic process where "ProcessId=NNN" call terminate`。
  - 清理测试数据脚本 `tools/tmp/cleanup_test_data2.py`（web_parent_% 账号 + registry spaces + 空间 db）。
  - **面板「孩子昵称」输入框无样式**（不在 `.form` 内吃不到 `.form input`）→ 已加 `.space-panel label/input` 同等样式（width:100% + box-sizing）。
  - **tab 与面板叠加**：tab click 原只切表单 `.on` 不移除面板 → 登录后点「登录」tab 会表单+面板叠加 → 已修：tab click 置 `panel.hidden = true`；`showPanel()` 隐藏 `.tabs`（面板=欢迎过渡页，无切换入口）、`showForms()` 恢复；showPanel 加 `scrollIntoView` 平滑滚动。
  - **改 style.css 后浏览器不重新请求**：版本号要同时改 HTML 里 href（`?v=...`）；且 Browser SDK goto 相同 URL 不真正导航 → 验证用「先 goto about:blank 再 goto 新版本 URL」或直接换全新 query。

## 1.8 空间内家长认证统一 + 选人页体验（2026-09-23，端到端全绿）

- **官网账号 = 空间第一个家长**：`create_space_for_account(..., password_hash=account.password_hash)` 把官网密码哈希写入空间库 admin（同一 `hash_password`/`verify_password` pbkdf2）→ 空间内 `/api/auth/login` 用**官网用户名+官网密码**即可进家长中心（不再用模板 `__template__` 密码）。三个调用方（trial_register/create_my_space/reset_my_space）都传 `account.password_hash`；child_name 兜底 `account.child_name`。
- **ParentLockDialog**（空间内家长锁）：用户名不再硬编码 `admin` → 实时查 `/api/trial/status`（X-Trial-Key）拿 registry `space.username`，localStorage 兜底，最后才兜底 admin。
- **SelectKid**（选人页）：新增「🏠 欢迎来到 {username} 的家庭空间」（同样实时查 status）+「退出登录」按钮（清登录态/trial_key/kid → `location.href='/site/'` 回官网）。
- **官网面板昵称不重复填**：注册已填 child_name → `presetChildName` 隐藏 `#spaceChildNameWrap`、创建按钮变「创建「小贝」的体验空间 →」；后端 create_my_space 兜底 account.child_name。
- **本地版体验期文案**：`#download` 补「新账号同样享受免费体验期，体验期结束后 ¥50 一次性买断」+ FAQ；价格动态取 `/api/config/public` 的 `local_price`（`#downloadPrice`/`.faqPrice`）。
- **坑（实测翻车）**：
  - **dist-trial 空间内 401 清 `easyfix_user`（官网登录态）** → 空间内要拿官网用户名/账号名**不要读 localStorage**，实时查 `/api/trial/status` 返回 `space.username`（registry 有）；SelectKid 的 ownerName 必须 `ref`（异步查完模板才更新）。
  - 空间内 admin 在空间库 users 表（`/api/auth/login`），官网账号在 accounts 表（`/api/auth/*`）——**两套认证，靠「建空间时写官网密码 hash + admin.username=官网用户名」对齐**；旧空间（未写 hash）家长锁仍会失败，需重置空间（`/api/trial/spaces/reset`）后生效。

## 1.9 AI 网关（订阅制，2026-09-23，MVP 全绿）

- **订阅制语义**：用户**不再配置模型 Key**，只选模型名；上游凭证由运营统一配置在 AI 网关（ops 后台，X-Ops-Password 保护）。未来消耗/价格计算在网关内统一做（本次未计费）。
- **配置键（app_config，主库）**：`ai_gateway_provider`（openai/anthropic，默认 openai=OpenAI 兼容协议）、`ai_gateway_base_url`、`ai_gateway_api_key`、`ai_gateway_models`（逗号分隔模型列表）、`ai_gateway_default_model`。ops 后台页面 = `frontend/site/ops.html`（含「测试网关连通」按钮 → `POST /api/ops/ai-gateway/test`）。
- **唯一上游入口 `AIGatewayClient.chat()`**（`app/services/ai_gateway.py`）：`LLMService._call_messages_create` 转发给它（`app/services/llm.py` 不再自建 client，`_init_client` 为兼容空方法）。`_get_config` 语义：model 走 `config/llm.json`（用户选择）→ 网关默认模型；api_key/base_url/provider 一律走网关。
- **用户侧接口**：`GET/POST /api/config/llm` 只含 model（**绝不返回 api_key/base_url**）；`GET /api/config/models` 返回可用模型列表。Settings.vue「LLM配置」tab = 模型下拉。
- **chat() 返回**：兼容旧响应对象（`content` 块列表）+ `usage`（归一化 `prompt_tokens/completion_tokens/total_tokens`，openai 与 anthropic usage 字段都转）。**RateLimitError（anthropic/openai）必须原样冒泡**——`_retry_on_rate_limit` 靠捕获这两个类型退避，网关注释里已标。
- **坑（实测翻车）**：
  - 读 app_config 必须主库 `SessionLocal()`（同 1.6，带 X-Trial-Key 时 `get_db` 会分发到空间库）。
  - `config/llm.json` 旧文件含 provider/api_key 等字段——改造后只写 `{"model": ...}`，遗留 key 不再被使用；本地冒烟脚本若从 llm.json 取 key 回填网关，二次运行会因 key 已清而把网关 Key 覆盖成空串（脚本已改幂等：优先保留已存值）。
  - **前端有正式 `dist` 与试用 `dist-trial` 两份产物**（`/site/`、`/` 用 dist；`/{trial_key}/` 用 dist-trial，见 vite.trial.config.js）。改前端后必须 `npm run build` **和** `npm run build:trial` 都跑，否则试用实例还是旧 UI（实测翻车：只 build 了 dist，用户看 `/zxc0ishrSBJ5OQ/` 仍是老表单）。

## 1.10 架构统一（2026-09-24，注册即建空间 + /app 移除 + easyfix_demo）

- **入口形态**：官网 `/`（site）+ 空间 `/{key}/`（dist-trial SPA）。**`/app` 正式 SPA 已移除**（main.py 删 app_spa + spa_fallback；非空间 key 一律 404）。dist 构建产物与 `/assets` `/icons` mount 暂保留（无害），阶段 D 前端合并时清理。Dockerfile/deploy.ps1 仍打包 dist，不用动。
- **注册即建空间**：`/api/account/register` 成功即调 `create_space_for_account`（复用模板快路径，秒级），返回带 `space`（key/url/child_name/trial_end_at）；前端官网 `app.js` 对 `r.space` 自适应，无需改。
- **懒注册机制（必读）**：租户引擎在**进程内字典**，只有建空间/登录时注册——服务重启后所有已有空间引擎丢失，带 X-Trial-Key 请求会**静默回退正式库（数据泄漏）**。已修：`trial.ensure_tenant_engine(key)` 从 registry 取 db_path 注册，middleware 校验后调用。**新增空间/改 db_path 后无需重启，首次请求自动恢复。**
- **前端 trial_key 必须 URL 优先**：`http.js` `currentTrialKey()` 改为解析 `location.pathname` 首段 `/{key}/`，回退 localStorage——localStorage 全局共享，直达 `/easyfix_demo/` 时残留别的 key 会打错空间（实测翻车）。
- **空间 URL 无尾斜杠必须 301 补斜杠（2026-09-24 白屏修复）**：dist-trial 是相对路径 `base='./'`，`/easyfix_demo`（无尾斜杠）时浏览器把 `./assets/...` 解析成根 `/assets/...` → 混入正式版 dist 的 JS → 白屏。`trial_spa` 已对无尾斜杠路径 301 → `/key/`（保留 query；浏览器自动保留 hash fragment）。验证 `tools/tmp/test_trail_slash.py`（7/7）。
- **easyfix_demo 调试租户**：key 固定 `easyfix_demo`，registry `spaces` 挂 account_id=1（zhengshuheng），`trial_end_at=NULL`（正式，不受体验期限制）。db = 正式库 `easyfix_main.db` 直接复制（**40 张业务表 schema 与模板库完全一致**，仅多 accounts/app_config 两张主库表，冗余无害；`practice_set_question` 还多 `student_answer` 列——所以复制正式库最稳，别走"复制模板再搬数据"）。含用户真实数据：3 小孩（郑予/郑好/演示小孩）+ 759 题 + 43 卷 + 39 评测。
- **空间登录墙（2026-09-24）**：空间 URL 无登录态也可见页面 → 加前端守卫 + `Login.vue`。`router.beforeEach`：除 `/login` 外 `easyfix_token` 为空一律跳 `#/login?redirect=原路径`；登录成功 `authStore.login`（`/api/auth/login`，空间库 users）后回跳。**登录墙是纯前端改动（dist-trial 构建产物），后端无改动，无需重启服务，刷新浏览器即生效**。空间 admin = 官网账号（`create_space_for_account` 写入密码哈希）；easyfix_demo 是复制正式库，admin 为 `admin`（正式库密码）。Token 30 天过期（`utils/auth.py TOKEN_TTL`），过期后 401 → http.js 清 token → 跳空间入口 → 守卫再送登录页。
- **空间到期校验 + 续费页（2026-09-24）**：路由守卫每次导航前经 `stores/trial.js` 查 `/api/trial/status`（后端已返回 expired/days_left/is_pro/expires_at，零后端改动）；`expired=true` → 拦到 `/subscribe`（`Subscribe.vue`，显示到期日+价格+"前往官网续费"跳 `/site/`，官网升级接口 `subscription/upgrade` → `upgrade_account_spaces` 转正式 → 回空间放行）。`trial_end_at=NULL`（easyfix_demo/正式版）→ is_pro=true 永不过期不拦截。SelectKid 顶部显示状态条（剩余 X 天/正式版）。纯前端，刷新浏览器即生效。
- **空间登录态永久化（2026-09-24）**：`create_token(user, scope=None, persistent=False)`——`persistent=True` 不写 exp（永久 token），`parse_token` 对无 exp 放行。**空间登录 4 处签发点改为 `persistent=True`**：`routers/auth.py` login、`main.py` `/api/auth/verify-password`、`trial.py` create_my_space/trial_register 自动登录。官网 account token（`account_api.py` 两处）保持默认 30 天（账号入口安全边界）。设计：空间访问门禁 = 到期校验（守卫+`/api/trial/status`→`/subscribe`），不用 token 过期兜底；第二家长各自账号密码登录后同样永久。
- **验证脚本**：`tools/tmp/test_arch_unify.py`（Popen 起 uvicorn 8017 → 轮询 → A/B/C 断言 → 先停服务再删测试空间文件，防 SQLite 文件锁）。注册测试账号用 `t_arch_{ts}` + `Abc@12345`。到期场景测试：注册后手改 registry `trial_end_at` 为过去时间，或注册后调 `/api/subscription/upgrade`（Bearer account token）转正式。
- 官网 `zhengshuheng` 登录面板显示的是**最早空间 ek0d9r-3wLBFYA**（get_space_by_account 按 created_at LIMIT 1），easyfix_demo 靠 URL 直达 `/easyfix_demo/` 使用，不在面板展示。

## 1.11 引导 v2 + Ops 一键同步（2026-09-24，阶段 B/C）

- **`POST /api/sync/words-all`**（sync_router.py:89）：一键同步 1-6 年级全部英语单词（`WordAllSyncRequest{version}`），内部循环 8 册调 `ops_data_service.sync_words`，异常单册吞掉继续，全空才 404。返回 `{books:[{grade,semester,added,removed}...], added, removed}`。
- **家长账号模型（2026-09-24 用户定规则）**：官网注册账号 = 空间**主账号**，**显式标识 `users.is_owner`（每空间仅 1 个）**，注册建空间时 `trial.py create_space_for_account` 标 True；不可删除（users.py delete_user 400「主账号不可删除」+ 前端 UserManage 删除按钮禁用、显示「主账号」标签）。其他家长 = 辅账号，家庭中心删除辅账号 → 其官网账号 `enabled=0`（accounts 表，官网登录 401）→ 官网登录失效；主账号官网登录保持可用。**迁移**：`backend/migrations/003_user_is_owner.py`（幂等：users 加 is_owner 列 + 按 registry spaces.username 标主账号，覆盖正式库/template/tenants）。**关键**：官网登录接口是 `/api/account/login`（不是 `/api/auth/login`——后者是空间内家长登录，走租户 User 表）；账号 token scope=account。**坑：启动服务必须用根 `.venv`（E:\qianwenpaw\EasyFix-main\.venv，含 fpdf 等全依赖），qwenpaw venv 缺 fpdf 起不来**。- **Word 模型补列（必读）**：`models/word.py` 加 `source/edition_key/revision` 三列（custom/ops 标记 + 修订标记）。模板库 word 表**没有**这三列 → `sync_words` 开头 `_ensure_word_package_columns` 幂等 `ALTER TABLE` 补列（空间库每次同步自动补，无需手工迁移）。**坑：补列前 sync_words 赋值 `row.edition_key`/`Word(source=..., edition_key=..., revision=...)` 会抛 AttributeError/TypeError 被 words-all 吞掉 → 整批 404「ops 仓库无该版本」**，症状像"数据源没词"其实模型缺字段。**另一个坑（2026-09-24 实测）：`_ensure_word_package_columns` 只在 sync 入口跑，单词列表等读查询不触发补列 → 未同步过的库 SELECT word.source 直接 `OperationalError: no such column: word.source`。已全库一次性迁移：`backend/migrations/002_word_source_edition_revision.py`（幂等，覆盖正式库 easyfix_main.db + trial_data/template.db + trial_data/tenants/*.db）。模型加列后必须跑该脚本（或等价迁移），读查询会炸。**
  - **辅助家长官网登录链路（2026-09-28，PARENT_HELPER_LOGIN_FIX）**：家长中心「添加家长」= 空间库 User(role=admin、非主账号) + 主库 Account 同步（username + 同 password_hash + `space_key=空间key`，users.py create_user）；官网登录 `/api/account/login` → `get_space_by_account`：主账号按 registry spaces.username 查，**辅助家长按 `Account.space_key` 查（走 `get_space_by_key`）**。**坑：所有「返回空间记录」的 dict 必须含 `url` 字段**——`get_space_by_key` 曾缺 url（只有 get_space_by_username 构造 url），辅助家长官网登录时 `issue_space_token_for_account` 访问 `record["url"]` 直接 KeyError → 500「登录不上」（主账号路径有 url 所以正常，只有辅助家长炸）。**存量旧版辅助家长（基线 users.py 只写空间库、不同步主库 Account）**：官网登录查主库 401 → 靠 `db_migrate.py sync_helper_accounts_to_main()` 启动幂等补录（按 registry 主账号名识别辅助家长，主库重名跳过），main.py 启动时调用。
- **引导 v2（Onboarding.vue 重写）**：Step1 选小孩数量 1~5 → **动态上限 `5 - 现有 child 数`**（模板自带「体验小朋友 id=2 + 我的小孩 id=3」2 个演示/空壳占名额 → 新注册空间实际可加 1-3 个；名额满显示警告 + 「已有小孩，跳过此步」）；批量添加 `usersApi.create({username:`kid_${Date.now()}_${ok}`, role:'child', display_name, enrollment_date})` 循环。Step3 科目卡**只有 数学/英语**（语文文案说明"已内置后续开放"）→ 版本默认 catalog 第一个 → `syncApi.syncKp({subject, version})` 一键导入全年级（数学=372 条）。Step4 `syncApi.syncWordsAll({version})`（人教版PEP=917 词 8 册）。完成写 `localStorage easyfix_onboarded_{trialKey}` + 清 `easyfix_new_space`。
- **新 API 客户端 `frontend/src/api/sync.js`**：status/syncKp/syncWordsAll（http.js 自动带 X-Trial-Key + Bearer token）。
- **家长中心精简（阶段 C）**：Management.vue 知识点 tab 隐藏「新增/按教材同步导入/AI 生成」+ 行内编辑/删除 → 「同步最新知识点」弹窗（科目+版本 → syncKp）；WordLibrary.vue 隐藏「新增单词/导入单词」+ 编辑/删除（详情保留）→ 「同步最新单词」弹窗（版本默认人教版PEP → syncWordsAll）。旧弹窗组件（TextbookImport/AiKpImport/importDialog）仍在 template 但无入口触发。
- **坑（8012 服务被旧进程占端口，重启无效）**：多次 wmic 重启后端口仍是旧代码——**必须 `netstat -ano | findstr :8012` 确认 LISTENING PID 是刚 create 的 cmd 子进程**；`.venv\Scripts\python.exe` 实际解析为 uv 缓存 python（CommandLine 显示 `Roaming\uv\python\...`），cwd=backend 即加载最新代码，判断新旧靠**行为**（如 words-all 是否 405/404）不靠 CommandLine。杀旧进程用 `wmic process where "ProcessId=NNN" call terminate`。
- **坑（多 uvicorn 残留，重启链会断裂）**：旧 cmd 壳退出但 python 子进程仍在监听（`ParentProcessId` 是已退进程）→ 新 create 的进程因端口被占静默失败。**重启前先 `netstat -ano | findstr :8012 | findstr LISTENING` 拿 PID → wmic terminate → 确认无监听 → 再 create**；create 后用 wmic 查 `ParentProcessId=新壳PID` 的 python（uv shim 24656 → 真实解释器 18788 两级）确认血缘。
- **401 vs 400 语义（家长密码验证被踢登录页）**：`http.js` 响应拦截——**带 token 的请求返回 401 会清 easyfix_token/easyfix_user 并 `location.href='/'+trialKey+'/'`（→ #/login?redirect=/）**。因此**密码校验类接口（/api/auth/login、/api/auth/verify-password）密码错误必须返回 400 而非 401**（业务校验失败 vs 登录态失效）。ParentLockDialog 家长验证走 `authStore.login`（/api/auth/login，ownerName 从 /api/trial/status 实时查）——输错密码曾因 401 被踢回登录页且无提示；已改 auth.py login 3 处 401→400 + main.py verify-password 401→400。同理新写"凭据错误"接口避免 401。

## 1.12 语法教程运营化（2026-09-27，主库 ops 权威）

- **权威源**：主库 `grammar_lesson`（easyfix_main.db，44 条全内容）= 运营统一维护的语法教程；**建空间自动同步**（template.db 复制时 copy_global_content 保留主键 id → 空间/主库 id 一致）；`trial._sync_template_grammar()` 在 ensure_template_db 每次调用时从主库 upsert 模板库 → **新空间创建即带最新教程**。
- **更新逻辑**：空间端 `POST /api/grammar/sync-tutorials`（家长管理页「同步官方教程」按钮，GrammarManager.vue 只读 + 该按钮）；运营后台「推送到所有空间」`POST /api/ops/grammar/sync-tenants`（遍历 registry spaces + 模板库）。
- **同步实现**：`backend/app/services/grammar_sync.py` `sync_grammar_from_main(target_db)`（SQLAlchemy，空间端用）/ `sync_grammar_sqlite(db_path)`（sqlite3 直写，ops 批量用）；**按 id upsert + 软删主库已移除的点**；subject_id 用目标库「英语」学科 id（跨库 id 可能不一致，别用主库 id）。
- **固化**：空间端 create/update/delete/ai-generate-skeleton/ai-generate-tutorial 全部 403（`routers/grammar.py` `_ensure_readonly`）；家长 GrammarManager 只读表格。
- **ops 后台**：`routers/ops_grammar_router.py`（`/api/ops/grammar/lessons` GET/PUT/详情、`/ai-generate` AI 批量生成缺失、`/sync-tenants`），X-Ops-* 鉴权；前端「系统配置 ▸ 语法教程」`GrammarTutorialsManage.vue`。
- **教程版面（2026-09-27 体验优化，`frontend/src/views/Grammar.vue`）**：教程长滚动优化——正文按 `##` 拆成**分节卡片**（`contentSections` computed，逐节折叠 + 「全部收起/展开」）；顶部「📖 本课包含」chips；右栏吸顶「📑 本课目录」（点击平滑滚动定位，**目标块折叠时自动展开**，滚动高亮当前节）；底部「上/下一个语法点」（`siblingNav`，显示 n/N）；`el-backtop` 回顶部。**直达 `/grammar/:id` 时 `ensureLessonIndex()` 补载 allLessons**，否则「同板块语法点」「上/下一个」为空。
- **坑（空间内页面禁止用裸 axios）**：只有 `@/api/http` 的 `api` 实例（`baseURL='/api'`）会注入 `X-Trial-Key`。`Reading.vue` 曾用裸 `axios` → 请求缺租户头全落主库：「生成短文」写进 `easyfix_main.db`、空间列表永远「暂无短文」（见 `docs/tasks/done/2026-09-27-READING_TENANT_FIX.md`）。http.js 现已给裸 axios 兜底注入 X-Trial-Key，但**新代码一律用 `api`，路径不写 `/api` 前缀**。
- **坑（`practice_set.user_id` NOT NULL）**：新建 `PracticeSet` 必须带 `user_id`（用 `Depends(get_required_kid_id)` 取当前孩子）；漏了就是 500 `NOT NULL constraint failed: practice_set.user_id`（「创建练习集」曾因此失败）。同类坑：详情接口响应漏 `passage_id` → `ReadingTest.vue` 拉不到短文/题目，测试页只剩标题。
- **坑（空间 SPA 跳转必须用 hash）**：`window.location.href='/xx'` 会跳出 `/{key}/` 落到官网/404；应用 `window.location.hash = '#/xx'`（空间是 hash 路由）。
- **坑（验证 SPA 时 `page.goto` 只改 hash 不会重载）**：看起来"改了没生效"，验证时换 query（`?v=N`）强制重新加载。
- **坑（接口不返回关系字段时前端别直接渲染）**：`POST /api/readings/generate` 返回的 passage **不含 `questions`**（未 joinedload）；直接赋给详情对象会让 `selectedPassage.questions.length` 抛错 → 整块白屏。生成后用返回 id 走详情接口，或模板用 `?.`/computed 兜底。
- **坑（改前端必须 rebuild dist-trial，否则"改了没生效"）**：空间入口 `/{key}/` 加载 `frontend/dist-trial`，`/ops/*` 加载 `dist-ops`，`/assets` 走 `dist`；三端各自 `npm run build` / `build:trial` / `build:ops`。浏览器还会缓存旧 `index.html`（引用旧 chunk）→ 验证时用 `?v=N` 换 URL 或硬刷新；判断产物是否真的更新用 **Python 读文件查字符串**（`findstr` 搜 UTF-8 中文会假阴性）。
- **坑（实测）**：ops PUT 编辑直接改主库、**无备份时被测试值覆盖难还原**——验证「编辑→同步」链路时若改主库数据，先从未同步过的空间库/模板库取原值还原（全库同步后副本都是新值就没得救了；`updated_at` 被改无法还原，`source` 变 manual 需手动改回 ai）。

## 2. 评测（assessment）核心逻辑——改这里先读

### 2.1 判分（`app/routers/assessment.py`）
- `_normalize_answer`：去空白/全角/尾部量词/判断题符号归一（√/对→1，×/错→0）。
- `_grade_fill_answer`（填空/解答三态）：
  - **1.0** 数值结果对 + 单位齐（标准答案无单位时数值对即满分）
  - **0.5** 数值/算式对，但标准带单位而孩子缺单位或单位错（**打钩减半**，教学逻辑）
  - **0.0** 结果错
  - 数值判定 = 提取所有数字，**只看末位（结果）是否相等**——列式过程宽容（"8+8=15" 蒙对结果也给内容分）。
  - 单位提取 `_extract_unit`：优先括号内（本/个…），其次数字后 1~4 个汉字。
- choice：选项文本/字母归一比对；`数的分解` 题走 `_check_decompose`（任意两数之和=N）。

### 2.2 结算（submit）
- 前端 `buildFullAnswers()` **提交全卷所有题**，未答 `user_answer:''` → 判 0。
- `total = len(detail)` = 全卷题数 → **做 1 题退出就是 1/10**，不会虚高成优秀。
- `answers` 为空 → 400，不生成记录。中途退出（≥1 题已答）→ 照常提交结算保存。
- 报告 detail 逐题：stem/answer/user_answer/correct(0|0.5|1)/knowledge；前端 `Assessment.vue` 弹窗逐题回顾。

### 2.3 组卷（start）
- 按 `subject_id + grade` 抽题，`TYPE_ORDER` 应用题最优先，同知识点最多 2 题。
- **学科题型白名单 `_SUBJECT_ALLOW_TYPES`**：英语(2)/语文(3) **排除 application**（应用题是数学题型；历史教训：qid 72 英语卷混入 "I have three red apples" 数学题被用户投诉）。
- 低年级(1-2)数学先跑 `_ensure_pictorial_questions` 模板引擎补图示算式题；题库不足自动调 AI 补题（`_auto_refill`）。

### 2.4 评测集管理（2026-09 五需求）
- `assessment_record` 即评测集：`status` 三态 **in_progress/done/quit**；`questions` 列 = 题目快照 JSON（start 时写入）。
- **start 会建 in_progress 记录并返回 record_id**；同一孩子同学科同年级只留一条进行中（旧的自动置 quit）。前端必须把 record_id 带回 submit（`POST /assessment/{record_id}/submit`）；放弃时调 `POST /assessment/{record_id}/quit`。
- history 接口支持 `subject_id` 过滤（数学页不加载英语记录），返回 done+in_progress（未完成在前），quit 不显示。
- **评测排重 `RECENT_EXCLUDE_DAYS=7`（2026-09-27 升级）**：start 组卷排除最近 7 天该孩子同学科同年级**所有展示过的题（done/in_progress/quit 全算）**，且**按 id + 题干双维度**排重（AI 变式可能生成同题干新 id，仅按 id 防不住）——保证连续切换不同卷型题目不雷同。
- **错题同步 `_sync_error_questions`**：评测答错（correct<1）→ 进统一错题集（`source='assessment'`，复用 `upsert_error_question_from_practice_question` 幂等）；评测答对 → 该题 active 错题置 mastered（自动排除）。错题本查询只滤 deleted/status/source!='ai'，assessment 错题与练习错题同池可见。

### 2.5 前端状态机（`frontend/src/views/Assessment.vue`）
- `answerState`：`'' | full | half | wrong`。half 时输入框可编辑 + 「📝 订正」按钮，订正成功补 0.5 分（补满）。
- **`answerLog` 每次 startAssessment 必须重置**（历史 bug：残留答案导致"一题未做也提交 0/10"记录）。
- **做题键盘化 + 答对彩蛋（2026-09-27）**：① 自动聚焦——start/next 后 `focusFillInput()`（nextTick → el-input focus），选择题无输入框改 `keyNavIdx=0` 默认高亮第一项；② 选择题方向键——window `keydown`（onMounted/onUnmounted）：↑/←↓/→ 移动高亮（模环绕）、Enter 提交 `pickChoice`、答完（full/wrong）Enter 直接 `next()`（half 态由输入框 @keyup.enter 订正优先，window 跳过 half 防重复）；③ 答对彩蛋——`celebrate()` 16 个 fixed emoji span（🎉⭐✨🌟💫🎊）CSS `confetti-fly` 随机飞散 1.3s 自移除，pickChoice/pickFill/correctFill 判 full 触发，开关 `celebrateOn`（localStorage `easyfix_assess_celebrate` 默认开）+ 顶部「🎉 特效开/关」按钮；样式 `.quiz-option.key-nav-active`（蓝高亮）/`.key-hint`/`.confetti-emoji`。
- **组卷坑（验证方向键时实测）**：`TYPE_ORDER` 里 application(1)/fill(2) 优先于 choice(3)，数学/英语卷 10 题几乎抽不到选择题（1年级 choice 13 条、英语 grade2 14 条照样中不了）→ 端到端验证 choice 交互时，对测试空间库 `UPDATE practice_question SET deleted=1 WHERE question_type!='choice'` 强制抽 choice（AI 每卷仍补 4 道 fill 变式排在前，跳过后即 choice）。

### 2.6 评测需求优化（2026-09-23：难度分层 + 三档卷型 + 能力定位 + 报告Tab）
- **题库难度分层**：`practice_question.difficulty` 1-5（规则：题型基础分 + question_category 修正，见 `tools/tmp/backfill_difficulty.py`，已落库 418 题）。档位：basic=d1-2 / mid=d3 / hard=d4-5（`_difficulty_tier`）。
- **三档卷型 `paper_type`**（`AssessmentStartRequest` + start 组卷）：standard=40/40/20、challenge=20/50/30、explore=10/40/50（基础/中等/拓展）。组卷按难度分桶抽题，每桶内保持图题/情景/未考/题型优先级；题量不足时放宽补足（`quota` 尾差进基础档）。**坑：`_take` 闭包里 `pictorial_taken += 1` 必须 `nonlocal`，否则 UnboundLocalError**。
- **能力定位 `mastery`**（submit/detail 返回）：按难度维度统计 `tier_stats`（basic/mid/hard 正确率）+ 本年级内掌握等级（待巩固/基础掌握/掌握良好/学有余力，**不跨年级判级**）+ 强项(≥0.8)/弱项(<0.6)知识点 + 边界声明。前端报告弹窗三 Tab：能力定位/知识点(网格两列)/题目回顾，Tab 内容超长仅内部滚动（`.rp-tabs :deep(.el-tabs__content){max-height:56vh;overflow-y:auto}`）。
- 前端入口：hero 区卷型卡片（标准/拔高/拓展）→ `assessPayload` 带 `paper_type`；**题目数量选择器**（5/10/15/20 题，`questionCount` ref，默认10，`assessPayload` 带 `count`，后端 `req.count or ASSESS_QUESTION_COUNT`）。
- **AI 补题带难度+变式（任务D，2026-09-23）**：`_auto_refill(db, ..., difficulty=None)` 新增目标难度参数，start 缺题时按卷型传（标准=3/拔高=4/拓展=5，1-2年级自动降4）；LLM 每题输出 `difficulty` 1-5（prompt 难度标注段 + JSON 示例），`_auto_refill` 对漏标/越界难度做兜底夹取（1-2年级封顶4）。**DB 有 CHECK 约束 `check_pquestion_difficulty` 拒绝越界难度（1-5）**，漏夹时整题入库失败但不影响其他题。prompt 新增【变式要求】：同知识点多题情境/数据/问法各异，防雷同枯燥。
- **举一反三出题（2026-09-27，用户明确"库存只是参考，不应按库存直出"）**：组卷 = 库存参考 + 每次评测自动生成新变式。① `_auto_refill` 新增 `avoid_stems` 参数并透传到 `llm.generate_questions_by_knowledge` → prompt【严禁重复】段（近期题干直接列出，严禁同题干/只改数字人名）——**源头防撞**；② 每次 start 无论库存是否充足都生成 2 道变式（分档补题已生成则不再重复，`VARIANT_COUNT - generated`），难度按卷型（standard=3/challenge=4/explore=5）；③ 错题知识点加权（`ErrorQuestion` 未掌握知识点在 pool key 里前置，出题依据之一是错题但不是唯一）；④ **pool 排序前先 shuffle 输入 + 卷内 `random.shuffle(sampled)`**（否则三档卷 basic 桶都抽同一批图题，第一题雷同——历史实测：9 卷连续切卷 0 重叠）。
- **看图列式模板坏题（2026-09-27 二修，用户实测再报）**：旧版 `pictorial_math._fill_stem` sum 分支生成"看图列式：小鸡一共有（　）只（个）。"——**题干无数字 + visual=None + 绕过 sanitize 直接入库**（`_ensure_pictorial_questions` 用 `create_practice_question` 不经 `_sanitize_math_item`），孩子无图无法作答。修复 4 层：① `_fill_stem` sum 分支改带数量（"左边有X只小鸡，右边有Y只…一共有（　）只"）——题干自包含；② `_ensure_pictorial_questions` 入库前过滤（"看图列式"必须带数字 + visual 必须有效）；③ 组卷 `_take` 防线（"看图列式"无数字且非 count-split 的题跳过——存量坏题也防住）；④ 存量软删（SvXXG4zukMip0A/xSKrVxSi8MX8ow 各 20 条 id=695-725）。**教训：改模板引擎/生成逻辑后必须检查入库路径是否绕过了 sanitize；assessment.py 顶部 import re 易漏（NameError→500）**。
- **组卷坏题校验（2026-09-27 三修，用户明确"即使来自题库也需校验坏题"）**：`_take` 新增 `_is_bad_question(qq)` 通用校验（start 内闭包，抽题时兜底过滤——AI 题入库有 `_sanitize_math_item`，但模板/存量/导入题可能绕过）：①题干空；②答案空；③choice 选项 <2（**模型是 option_a/b/c/d 四列，不是 options 数组**）；④"看图列式"无数字且非 count-split 配图。`_take` 与兜底补足循环都调用。实测注入 3 类坏题（id=807/808/809）全部被过滤。
  - **评测规则运营化（2026-09-27，用户要求评测相关规则也由运营平台管理）**：主库新表 `ops_assess_rule`（key/value/enabled，`models/ops_data.py`）+ `services/assess_rules_service.py`（`ASSESS_RULES_META` 20 项元数据：组卷策略 dedup_days=7/variant_count=2/refill_margin=2、补题难度档 gap_diff_*=2/3/5、变式难度 variant_diff_*=3/4/5、坏题校验 min_choice_options=2、配图占比 pictorial_ratio=0.5、卷型占比 ratio_{standard,challenge,explore}_{basic,mid,hard}）。**读取端**：assessment.py start 开头 `load_assess_rules()` 一次 → 覆盖 `_recent_done_question_ids(days=)`、`VARIANT_COUNT`、`tier_diff`、`_gap+margin`、`_variant_diff`、`_is_bad_question` 选项阈值、`pictorial_budget`、`PAPER_RATIOS`（9 项）；未配置/坏值/表不存在一律内置默认兜底（`load_assess_rules` 返回空 dict 不影响评测）。运营 API：`GET/PUT /api/ops/assess-rules`（PUT 空文本=恢复默认删记录）；前端 `frontend/ops/src/views/AssessRulesManage.vue`（菜单「系统配置 ▸ 评测规则」，`npm run build:ops` 产物 frontend/dist-ops）。**坑：改 OpsLayout 菜单/新增路由后浏览器会缓存旧 index.html → 验证必须带 query（`/ops/?nocache=1#/xxx`），用户强刷 Ctrl+F5；构建产物目录是 `frontend/dist-ops` 不是 `frontend/ops/dist-ops`**。

## 3. 高频坑（本仓库实测）

- **Dockerfile 必须 COPY frontend/site（2026-09-23，官网进旧界面修复）**：官网目录 `frontend/site` 曾漏在镜像外（只 COPY dist/dist-trial）→ 容器内 SITE_DIR 不存在 → `/` 官网挂载失效 → 根路径被 SPA fallback 吞掉直接进 `/app` 旧单体界面。**已加 `COPY frontend/site /app/frontend/site`**。教训：新增前端目录（官网/站点等）必须同步加 Dockerfile COPY——否则本地正常、容器缺文件，且 tar 包里明明有该目录（迷惑性强）。
- **trial 通配路由抢占 /assets（2026-09-23，白屏修复）**：main.py 里 `/{trial_key}/{full_path:path}`（trial_spa）注册在 `/assets` StaticFiles mount **之前** → `/assets/xxx.js` 被 trial_spa 抢先匹配（trial_key="assets"）→ 非 trial key → fallback 返回 index.html → 浏览器 `Failed to load module script ... MIME text/html` 白屏。**修复：assets/icons mount 已提前到 FRONTEND_DIST 定义后、所有 `/{trial_key}/...` 通配路由之前**。教训：Starlette/FastAPI 按注册顺序匹配，任何 `/{xxx}/{path}` 通配路由都必须排在静态资源 mount 之后，否则 JS/CSS 全被吞成 text/html。

- **删除权限家长认证（2026-09-23，PARENT_GUARD_DELETE）**：学生端数据删除接口全部 `require_admin`（家长）：错题 `DELETE /api/questions/{id}`、单词 `DELETE /api/words/{id}`、练习 `DELETE /api/practice-sets/{id}` + `POST /api/practice-sets/batch-delete`、学习报告 `DELETE /api/learning-reports/{id}`、阅读 `DELETE /api/readings/{id}`——child 调用一律 403。前端孩子会话点删除 → `useParentGuard`（`frontend/src/composables/useParentGuard.js`，`guard(action)` 家长直通/孩子弹窗）→ `ParentLockDialog`（title/tip/confirmText props 化）验证 → 删除 → 恢复孩子会话。**例外**：`POST /api/phonics/wrong-words/clear` 兼自动「掌握即移除」（Phonics.vue `saveAttempts`），后端不拦，仅前端手动删除按钮（removeWrong/clearWrongs）加认证。新增学生端删除接口必须照此模式。

- **单词例句/学习模式（2026-09-23，WORD_LEARN_ENHANCE）**：`word.example_sentences` 列 = JSON `[{en,zh}]`，`_ensure_column` 迁移。AI 增强包含例句：`_enhance_words_llm`（新词完整生成含例句）/ `_fill_sentences_llm`（老词只补例句，**不覆盖已编辑字段**）；`_needs_enhance`=拼读+词根缺失，`_needs_sentences`=例句为空；`POST /words/enhance` 同时补增强+例句（limit≤50，20/次 LLM）。前端学习模式在 Words.vue `dimConfigForm.learnMode`（easy/standard/advanced，localStorage `easyfix_dims_{kid}`），例句数量按模式截断（easy=0/standard=1/advanced=2），进阶可关中文翻译（`showSentenceZh`）。**新词学习题（认一认选择题）例句只显示英文不显示中文——防止中文翻译泄露答案**。例句/中文发音走三级：浏览器 SpeechSynthesis en-US → 无语音/Chrome 时降级服务器 `/api/words/audio?english={句子}&lang=en-US|zh-CN`（edge-tts 生成，缓存于 `uploads/audio/words/sentences/`，md5 文件名不污染单词目录）。**Chrome 的 Google 在线语音（en-US/zh-CN）国内常"列表有但发声不可用"，`Words.vue` 用 UA 检测（`isChromeNoEdge`）强制 Chrome 走服务器 TTS；自动带读例句在点击后 5s+ 才播，会撞 Chrome Autoplay 5 秒窗口，故首次点击时创建 AudioContext 解锁（`unlockAudioOnGesture`），服务器音频走 Web Audio 播放**。`WordLibrary.vue` 的 `speakEn` 同样 Chrome 强制降级。存量老词无例句 → WordLibrary「记忆增强」tab 筛选批量补生成。**9/28 移动端+例句中文修复（WORD_CARD_TTS_FIX）**：① Words.vue 曾是全仓库唯一**无任何 @media 移动端适配**的页面，复习/学习弹窗固定 `--el-dialog-width:1200px`（Element Plus 内联 CSS 变量，覆盖必须用 `:deep(.review-dialog){--el-dialog-width:96vw !important}` 而不是 width 属性），手机窄屏弹窗溢出 → 单词卡片错位换行；已加 `@media(max-width:768px)`（dialog 96vw + 学习卡/复习题/新词卡/默写卡字号内边距缩放 + 单词 `flex-wrap`/`word-break`）。② `autoTeach` 例句带读原只 `speakEn(s.en)` **不读 `s.zh`**（例句中文翻译无声）→ 例句循环补 `speakZh(s.zh,{force:true})`，条件 `!opts.noZh && s.zh && sentenceZhVisible()`（复习题认一认 noZh 不读防报答案；advanced 隐藏中文翻译时不读）。压缩产物验证特征：`I(R.zh,{force:!0})`。

- **Python 循环变量覆盖函数参数**（stats.py 实测翻车）：`for subject_id, ... in subject_query:` 循环变量会**覆盖函数参数 subject_id**，后续 `is_english_subject(db, subject_id)` 拿到的是最后一个学科 id 而非参数值。凡参数名与循环变量同名必翻车——循环变量一律用 `sid` 等别名。
- **cmd.exe 多行 python -c 会被压成一行报 IndentationError** → 临时脚本写成 .py 文件跑。
- **TestClient 版本不兼容**（starlette/httpx 新版报 `Client.__init__() got an unexpected keyword 'app'`）→ 改用直接调用 router 函数传参冒烟，或起真实 uvicorn + curl。
- **冒烟/测试会在真实 SQLite 里创建 AssessmentRecord 等记录** → 测完按特征清理（写清理脚本），别污染用户历史。
- **评测空答案=孩子空卷提交**（Assessment.vue `buildFullAnswers` 未答题显式发 `user_answer=''`）——错题详情看到"未作答"是真实数据，不是接口 bug。**且 `_sync_error_questions` 会跳过 user_answer 为空的题**（评测未作答不入错题集，只有输入了答案且判错的才算错题）；存量清理：source='assessment' 且该题在所有评测 detail 中从未有过答案的错题已软删除（36 条，含原停车场题 id=24）。
- **错题详情作答历史**：`GET /api/questions/{id}/practice-history` 合并 练习(PracticeAttempt.student_answer) + 评测(AssessmentRecord.detail 按 source_practice_question_id 匹配) 两种来源，字段含 `student_answer/source(practice|assessment)/is_correct/date`；is_correct 为数值三态（1 正确 / 0.5 半对 / 0 错误，评测 correct 是 0~1 分数，不能 bool 化）；前端 Questions.vue「最近一次作答」+「作答历史」两块展示。
- **错题详情图例**：ErrorQuestion 无 visual 列；`GET /api/questions` 列表与 `/{id}` 详情通过 `_visual_map_for(db, eqs)` 取图例，**优先级：PracticeQuestion.visual（题库落库）→ 评测快照 AssessmentRecord.questions JSON 里该题的 scene（组卷时动态配的图）**——评测组卷会为普通应用题动态配 scene 但**不回写题库**（PracticeQuestion.visual 常为 None），必须用评测快照兜底；前端 Questions.vue 详情题目卡片用 `<SceneVisual :scene="currentQuestion.visual">` 渲染（与评测页同一组件）。
- 改 Vue 模板后 `npm run build` 验证；Element Plus 组件在 scoped style 里覆盖内部样式需 `:deep()`。
- 浏览器截图：`browser.screenshot()` 存根目录 → **立即移入 `tools/tmp/`**（模型多数不支持读图，以 `snapshot()` 文本 + `bounding_box()` 验证为准）。

## 3.5 数据库地图 + 运营后台会话/账号（2026-09-26 踩坑固化）

- **数据库地图（2026-09-26 已改名 `easyfix.db` → `easyfix_main.db`）**：
  - `backend/easyfix_main.db` = **主库/正式库**（混合四类）：①官网账号 `accounts`（全局身份+订阅，当前为空）②运营数据 `ops_knowledge_point`/`ops_word`/`ops_edition`/`ops_ai_provider` ③空间同步状态 `space_sync_state` ④**历史单体业务表**（`users`/`practice_question`/`word`/`assessment_record`/`achievement`/`star_*` 等——重构前正式数据/模板源，**新数据不写这里**，写入各空间库）。
  - 空间数据 = `backend/trial_data/tenants/{key}.db`（一个空间一个库，来自 template.db 复制）；空间注册表 = `backend/trial_data/registry.db`（`spaces` 表：key/account_id/username/child_name/db_path/trial_end_at）；模板库 = `backend/trial_data/template.db`。
  - 改名联动已全量更新：backend/.env DB_PATH、config.py、migrations/002+003、deploy.ps1、build_upload.ps1、remote_deploy.sh（含服务器旧库自动迁移 /data/easyfix.db → easyfix_main.db）、docker-compose.yml、backup.sh、.gitignore/.dockerignore、README/AGENTS/CLAUDE/AI_CONTEXT/ARCHITECTURE/deploy README、Settings.vue 文案（build:trial 后生效）。备份：tools/tmp/easyfix.db.bak。
- **registry.spaces.account_id 会悬空/撞车（实测误删 demo 空间）**：账号删除后 `account_id` 保留（如 easyfix_demo 仍 account_id=1），新注册账号自增 id 会复用 1 → `get_space_by_account(id)` 匹配到**别人的空间** → 运营删除账号会**误删错空间**。铁律：**账号→空间一律按 `username` 匹配**（`get_space_by_username`），`get_space_by_account` 已改为先经 accounts 取 username 再查（账号已删 → 返回 None，不误匹配）。
- **删除体验账号 = `delete_space(key)`（trial.py）**：dispose 引擎 → 删 db/-wal/-shm 文件 → 删 registry 行；文件删除失败（Windows 句柄占用）会**重试一次后抛 RuntimeError**，运营接口转 500 明确告知（旧版静默 print 导致孤儿文件堆积）。孤儿文件（registry 无记录）服务不会访问，可安全删除；本次已清 20 个历史孤儿 db + 附属 wal/shm（38 文件）。
- **运营后台登录态持久化**：`frontend/ops/src/stores/session.js` 把 username/password 存 localStorage（`ops_session_username`/`ops_session_password`），刷新不掉登录；退出清 localStorage。明文存口令仅限内部工具（双因子 X-Ops-* 头无 token）。
- **smart-import 支持 `skip_online_textbook: bool`**（KPSmartImportRequest）：跳过④在线教材下载（PDF 大、下载慢），直接⑤AI 兜底；③本地教材不受影响。前端 AiImportDialog 知识点模式有「跳过在线教材下载」勾选。
- **一键部署（deploy.bat → deploy.ps1 → remote_deploy.sh）已对齐 ops 与 trial_data**：①`deploy.ps1` 构建步骤含 `npm run build:ops`（dist-ops 必须构建才会进包）②`Dockerfile` COPY `frontend/ops/dist-ops`（漏了服务器 /ops 404）③tar 已 `--exclude=backend/trial_data`（本地空间库/注册表/模板**不上传**），容器挂载 `$DATA_DIR/trial_data:/app/backend/trial_data`，首启自动生成 template.db + registry.db（`ensure_template_db`/`_registry_conn` 幂等）。改 deploy.ps1 后必须重写 UTF-8 BOM + Parser 零错误（edit_file 会丢 BOM）。
- **验证 smart-import 会触发真实任务写主库**（本地识别/AI 生成/在线下载导入）→ 验证后必须按 subject/version/grade/semester 清理 `ops_knowledge_point`（本次北师大三上由 ~152 增至 396、语文人教版1上新增 90 条，均已处理：90 条已删，北师大保留现状待用户定夺）。

## 3.6 辅助家长账号官网登录（2026-09-28 修复闭环）

- **根因**：家长中心「添加家长」创建的是**空间库** `users`（role=admin、is_owner=0），而官网登录 `/api/account/login` 只查**主库 accounts** → 辅助账号在官网永远 401（或已补录但 space=null 进不去）。
- **修复链路（三处必须同时成立）**：
  1. **创建同步**：`users.py create_user`（role=admin）→ 同步建 `Account`（username 全局唯一、`space_key=当前空间 key`、同密码）；改密码 → `update_password` 同步 `Account.password_hash`；删除 → 已有逻辑置 `Account.enabled=False`（官网登录立即 401）。
  2. **空间定位**：`Account.space_key` 列（主账号留空，按 `get_space_by_username` 查；辅助账号按 `space_key` 直接 `get_space_by_key`）——`get_space_by_account` 必须先判 space_key，否则辅助 username≠主账号 username 查不到空间。
  3. **身份签发**：`issue_space_token_for_account` 按账号 username 在租户库找对应 admin 签发**它自己的 token**（主账号=同 username 的 is_owner；辅助=同 username 的辅助家长；查不到兜底第一个 admin）。旧版一律签发主账号 token，辅助账号会以主账号身份进空间。
- **存量修复**：`db_migrate.sync_helper_accounts_to_main(db)`（main.py 启动调用，幂等）扫描各空间库把 role=admin 且 username≠registry 主账号名的账号补录进 accounts（含 space_key）。只跑启动时一次——**新账号靠创建同步，不等重启**。
- **坑（实测翻车）**：
  - 官网注册校验用户名=手机号/旧用户名 + 强密码（`Abc@12345` 级别）；**辅助账号用户名任意但必须全局唯一**（与官网已注册账号撞名 → 400 提示换名）。
  - 辅助账号密码规则沿用空间内（≥4 位），官网登录不校验强度（只校验存在+密码）；两边密码不同步=登录失败。
  - `remote_deploy.sh` 的 schema 漂移检查脚本用 `conn.dialect`（sqlite3.Connection 无此属性）会警告失败——**无害**（应用启动 main.py 迁移兜底），已改为 `create_engine('sqlite:///...').dialect`。
- **坑2（9/28 同日，ParentLockDialog 原生 fetch）**：`frontend/src/components/ParentLockDialog.vue` 的家长密码锁用**原生 fetch(`/api/auth/me`)**（不走 `@/api/http`）→ **缺 X-Trial-Key** → 租户中间件不切库 → me 落**主库** → 主库 `User.id` 与租户库**错位**（同 id 可能是 child）→ `role==='admin'` 候选收集失败 → 只剩 registry 主账号名，辅助账号**输对密码也全败**（弹窗不关=「家长中心进不去」）。已修：原生 fetch 手动拼 `X-Trial-Key`（URL pathname 解析 `/{key}/`，回退 localStorage `easyfix_trial_key`）。**铁律：空间内任何原生 fetch 必须带 X-Trial-Key；一律优先走 `@/api/http` 的 `api` 实例。**

## 4. 判分/评测相关文档索引



| 想看什么 | 去哪里 |
|---|---|
| **评测教育理念（产品宪法）+ 三档卷型/能力定位蓝图** | `docs/ASSESSMENT_DESIGN.md`（改评测相关代码必读） |
| 数据隔离架构 + 路由模板 | `docs/ARCHITECTURE.md` |
| 单词学习五维量化（概览页进度卡） | `stats.py` `dim_stats`（WordStats 字段）：跟读=listen_correct>0、认读=recognize_correct>0、读词=speak_count>0、说词=speak_correct>0、听写=write_correct>0；total=当前空间单词总数 |
| 错题来源列 | 后端 `ErrorQuestion.source`（practice/assessment/upload/error_review/ai）已在 list 返回，前端 `Questions.vue` 来源列映射 |
| 科目切换不跳首页 | `App.vue` `openSubjectSpace`/`handleSubjectCommand` 只切数据上下文（spaceKey 重挂载），英语专属页切非英语才跳 `/practice-sets` |
| 学习报告 | `learning_report.py` 标题自动生成；`LearningReports.vue` 无报告时自动生成一份（仅指定学科空间）；**数据不足（错题+单词都 0）返回 200 + `generated:false` + 友好 message（2026-09-27 改，不再 400——业务状态不算请求错误；前端 `generated===false` → warning 提示，自动出报告静默）**；生成成功 `generated:true` + id，前端自动 `viewReport` 打开详情 |
| 判分三态/订正机制实现 | `app/routers/assessment.py` + `Assessment.vue` |
| 图示算式模板引擎 | `backend/app/services/pictorial_math.py`（如有） |
| 文档管理规则 | `docs/CONVENTIONS.md` |
| 本文件由谁维护 | 每次会话收尾把"新踩的坑/新规则"补进来 |
