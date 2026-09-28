# OPS_ADMIN_UI — 运营后台改造：账号登录 + 后台布局 + 数据列表

- 完成日期：2026-09-24
- 状态：✅ 完成

## 需求
用户反馈运营后台（frontend/site/ops.html）三个问题：
1. 登录界面太简陋，连用户名都没有
2. 运营口令是多少？
3. "体验天数 / 价格 / 下载链接配置（口令保护）"这类敏感文案不该出现在公开页面上

随后补充：运营后台要像正常后台，有导航菜单 + 数据列表，便于操作。

## 改动

### 后端（backend/app）
- `config_api.py`
  - `CONFIG_DEFAULTS` 新增 `ops_username: "admin"`（运营账号，默认 admin）
  - `_check_ops_password(db, ops_password, ops_username="")` 改为账号+口令双因子，二者缺一不可（空账号 401「运营账号错误」）
  - `GET/PUT /api/ops/config`、`POST /api/ops/ai-gateway/test` 三个接口新增 `x_ops_username` header
- `routers/ops_data_router.py`（脚本批量替换，10 处接口）
  - 全部接口新增 `x_ops_username` header，`_ops_check(x_ops_username, x_ops_password)` 同步账号校验

### 前端（frontend/site）
- `ops.html`（重写布局）
  - 登录页：新增「运营账号」输入框（+ 运营口令）
  - 副标题改为中性：「运营管理后台 · 授权访问」（去掉"体验天数 / 价格 / 下载链接配置"）
  - 登录后进入标准后台布局：左侧深色导航（📚 教材数据 / ⚙️ 系统配置 / ↩ 退出登录）+ 右侧内容区
  - 默认进入「教材数据」面板（筛选 + 数据列表 + 新增/编辑/删除编辑器）
  - 系统配置面板新增「运营账号」可编辑字段
- `ops.js`
  - 登录请求带 `X-Ops-Username`；网关测试补 `X-Ops-Username`
  - FIELDS 新增 `ops_username`；保存配置后同步内存账号/口令
  - 退出登录按钮（回到登录卡片）
- `ops_data.js`
  - `window.opsDataInit` 从 tab 切换改为左侧导航 `.ops-nav` 切换；登录后默认自动加载教材目录

## 验证（全部通过）
- API 四场景：admin+easyfix-ops → 200；adminx → 401 运营账号错误；错口令 → 401；空账号 → 401
- 网关连通测试（带账号）→ 200（deepseek-flash 真实调用）
- 浏览器端到端：登录 admin/easyfix-ops → 后台布局正常 → 教材数据默认面板 → 目录自动加载（数学/英语/语文）
- 知识点列表：英语 人教版PEP 3年级 → 37 条；英语单词 → 316 条（含编辑/删除按钮）
- 系统配置导航切换正常（cfg_ops_username 回填 admin）；退出登录回到登录页

## 运营登录凭证
- 运营账号：`admin`（默认，可在后台系统配置修改）
- 运营口令：`easyfix-ops`（默认，可在后台系统配置修改）

## 备注
- 官网 footer「· 运营」入口保留（index.html:260）
- 服务 PID 12748（uv python，18:01:32 启动，已加载新代码）
