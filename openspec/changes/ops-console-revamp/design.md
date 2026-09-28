# 运营后台改造 + AI 模型市场 · 技术方案

## 0. UI 布局改造（现代化管理后台，用户 9/25 要求）

当前是传统居中布局（`.ops-wrap max-width:1100px; margin:32px auto` + 大卡片悬浮），
改为数据密集型全宽后台：

- `.ops-wrap`：去掉居中（`max-width:none; margin:0; padding:0`）→ 全宽
- `.ops-layout`：`min-height:100vh; gap:0` → 满高
- `.ops-side`：固定侧边栏（`width:220px; border-radius:0; position:sticky; top:0; height:100vh`），
  深色导航，两级菜单
- `.ops-main`：内容区铺满（`border-radius:0; box-shadow:none; padding:24px`），
  面板直接铺满内容区，不再悬浮卡片
- 登录页保持居中卡片（登录场景惯例，不适用全宽）
- 表格/筛选区保持数据密集型（sticky 表头已有）；各面板按 data-view 切换

## 1. 菜单结构（前端）

```
主侧栏
├─ 📚 教材数据（可展开）
│   ├─ ▸ 知识点管理       → kp-panel（现有：搜索/筛选/增删改/AI导入/批量导入）
│   └─ ▸ 英语单词管理     → word-panel（现有：搜索/筛选/增删改/AI导入/批量导入/图片识别）
├─ ⚙️ 系统配置（可展开）
│   ├─ ▸ 系统设置         → config-panel（现有表单：AI 网关旧配置/价格/引导/运营账号/体验天数）
│   └─ ▸ AI 模型市场      → 新 ai-market-panel（厂商 CRUD + 连通测试）
└─ ↩ 退出登录
```

- `ops.html`：`ops-nav` 两级（教材数据/系统配置可展开）；面板容器 `data-view`：
  `kp` / `word` / `config` / `ai-market`，默认 kp
- `ops_data.js`：知识点/单词面板切换 + 导入按钮保留各自面板；AI 网关旧配置表单
  移到「系统设置」面板（保留，作为默认厂商兜底编辑入口）
- 新增 `ops_ai_market.js`：模型市场面板逻辑

## 2. AI 模型市场（后端）

### 2.1 新表 `ops_ai_providers`（主库 app 库——不能走空间库分发）
```
id, name(unique, 厂商名如 DeepSeek/OpenAI/Anthropic/阿里云百炼/智谱GLM),
protocol('openai'|'anthropic'), base_url, api_key,
models(JSON list 或逗号分隔), vision_models(逗号分隔，该厂商支持多模态/OCR 的模型；留空=全部模型可 OCR),
default_model,
enabled(bool), is_default(bool), sort_order(int),
created_at, updated_at
```

### 2.2 运营 API（X-Ops 双因子保护）
- `GET    /api/ops/ai-providers`         列表
- `POST   /api/ops/ai-providers`         新增
- `PUT    /api/ops/ai-providers/{id}`    编辑 / 启用禁用 / 设默认
- `DELETE /api/ops/ai-providers/{id}`    删除
- `POST   /api/ops/ai-providers/{id}/test` 连通测试（真实上游最小请求）

### 2.3 网关改造（`services/ai_gateway.py`，收敛点）
- `get_providers()`：启用厂商列表（含 models/default_model）
- `get_provider(name)`：按厂商取配置；`default_provider()`：is_default → 第一个启用 → ai_gateway_* 兜底
- `AIGatewayClient(provider=None)`：按厂商初始化客户端；provider 缺省用默认厂商
- `list_available_models()`：所有启用厂商模型并集（兼容旧平铺接口）
- `list_provider_models(name)`：单厂商模型

### 2.4 学生端接口（`routers/config.py`）
- `GET /api/config/models` → `{providers:[{name, models}], default_provider, models(兼容旧), default_model}`
- `GET /api/config/llm` / `POST /api/config/llm`：支持 `vendor` 字段（用户选择厂商名），
  旧数据无 vendor → 默认厂商
- `services/llm.py`：`_get_config("model")` 增加读取 llm.json 的 vendor → 网关按厂商取默认模型

### 2.5 OCR 兼容（模型市场内）
- **运营侧**：厂商配置多一个 `vision_models` 字段（该厂商可作 OCR 的视觉模型；
  留空 = 该厂商全部模型可 OCR，兼容现状语义）
- **学生端 OCR 面板**（provider=multimodal 时）：改为**厂商下拉 + 视觉模型下拉**（联动），
  只列各启用厂商的 `vision_models`（留空则列全部 models），与 LLM 选择交互一致
- **后端 `/api/config/ocr`**：返回 `multimodal_providers:[{name, vision_models}]` +
  兼容旧 `multimodal_models`（全部视觉模型并集，保持旧前端可用）；
  `ocr.json` 保存时新增 `vendor` 字段
- **OCR 调用**：按 vendor + multimodal_model 走网关（AIGatewayClient(provider)），
  与 LLM 同一收敛点；无 vendor → 默认厂商
- **兼容**：旧 ocr.json（只有 multimodal_model）→ 默认厂商；vision_models 未配置的厂商
  全部模型出现在 OCR 下拉（现状语义不变）

### 2.6 兼容策略
- `ops_ai_providers` 为空 → 网关完全回退 ai_gateway_*（现状不变，零影响）
- 运营后台旧 AI 网关表单保留在「系统设置」，等价于维护"默认厂商"；模型市场新增厂商后
  学生端优先看到厂商列表

## 3. 实施阶段

- 阶段 1：前端两级导航 + 面板切换（纯前端；kp/word/config/ai-market 容器就绪）
- 阶段 2：AI 模型市场后端（表 + CRUD + test API + 网关多厂商 + config API 扩展）
- 阶段 3：模型市场运营面板（ops_ai_market.js）+ 学生端 Settings 厂商/模型联动
- 阶段 4：全量回归（知识点/单词 CRUD、AI 导入/批量导入、各厂商路由、旧配置兜底）+ 归档

## 4. 明确不做（延后）

权限管理 / 用户管理 / 版本管理 / 独立数据管理菜单 —— 单人运营暂不需要，后续开新 change。
