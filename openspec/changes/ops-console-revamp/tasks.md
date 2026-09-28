# Tasks — 运营后台改造 + AI 模型市场

> 用户已确认工程化方向：运营后台改为 Vue 独立入口（frontend/ops/ → dist-ops，后端 /ops），不再维护静态 ops.html。

## 阶段 1：Vue 工程化运营后台（纯前端，已完成主体）

- [x] 工程骨架：vite.ops.config.js + ops/index.html + src/main.js + pinia + vue-router(hash) + api/ops.js（X-Ops 双因子）
- [x] 登录页：双因子 → 进入后台
- [x] 全宽布局：OpsLayout 固定侧栏 220px 全高 + 内容区铺满无大卡片（登录页保持居中）
- [x] 两级导航：教材数据▸知识点管理/英语单词管理；系统配置▸系统设置/AI 模型市场
- [x] 知识点管理：目录联动筛选（科目/版本/年级/册次）+ 列表 CRUD
- [x] 英语单词管理：版本/年级/册次筛选 + 列表 CRUD
- [x] 系统设置：体验与价格/运营账号/AI 网关旧配置表单 + 连通测试
- [x] AI 模型市场占位页（阶段 3 完整实现）
- [x] 后端 main.py mount /ops → frontend/dist-ops；package.json build:ops
- [x] 浏览器端到端验证：登录 → 布局/菜单 → kp 372 条 → word 917 条 → 设置表单 → CRUD 冒烟；测试数据已清理
- [x] AI 导入弹窗（教材模式/自定义指令 → 预览 → 勾选导入）迁移 Vue → components/AiImportDialog.vue（kp/word 共用；OCR 结果 openWithPreview 承接）
- [x] 批量导入弹窗（文本粘贴/文件/图片识别）迁移 Vue → components/BatchImportDialog.vue（图片识别仅 word → emit ocr → AI 弹窗预览）
- [ ] 旧静态 ops.html/ops_data.js/ops.js 移除（footer 入口已改 /ops/；删除命令被安全策略拦截，需手动删或授权重试）

## 阶段 2：AI 模型市场后端（已完成，TestClient 验证）

- [x] 新增表 ops_ai_provider（含 vision_models）+ ensure 建表（主库）
- [x] ai_gateway.py：list_providers/get_provider/resolve_gateway_config；AIGatewayClient(config) 支持显式厂商配置；无厂商兜底旧 ai_gateway_*
- [x] 新增 routers/ops_provider_router：CRUD + test API（X-Ops 双因子保护）
- [x] config.py：/config/models 返回 providers+default_vendor；/config/llm 支持 vendor（存 llm.json）；/config/ocr 返回 multimodal_providers + 保存 vendor
- [x] llm.py / multimodal_ocr.py：读取用户 vendor → 按厂商取模型/视觉模型
- [x] API 验证：CRUD、掩码 key、重复拒绝、test 容错（假 key 401 不崩）、models/ocr 返回、llm.json vendor 存取、无厂商兜底（TestClient 直接调函数 10 项全过）

## 阶段 3：运营面板 + 学生端（已实现，浏览器验证部分完成）

- [x] AiMarket.vue：厂商列表/新增/编辑（含视觉模型）/默认标记/连通测试/删除（替代 ops_ai_market.js 方案）
- [x] Settings.vue：LLM 配置改厂商下拉 + 模型下拉（联动）
- [x] Settings.vue：OCR 面板多模态改厂商下拉 + 视觉模型下拉（联动）
- [~] 浏览器验证：运营端已验证（新增 DeepSeek → 掩码 → 测试 401 详情 → 删除）；学生端 Settings 联动未跑 UI（构建通过 + 接口已验证），待服务运行后补验

## 阶段 4：全量回归 + 归档

- [ ] 回归：知识点/单词 CRUD、AI 导入/批量导入、图片识别、系统设置表单
- [ ] 旧配置兼容：清空 providers → AI 调用回退 ai_gateway_* 正常
- [ ] 测试数据清理（tools/cleanup.py）
- [ ] 归档 openspec/changes/archive/，关键结论沉淀 docs/AI_CONTEXT.md
