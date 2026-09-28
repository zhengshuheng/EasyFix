# AI 模型市场 ↔ 学生端 LLM/OCR 联动测试 + deepseek 迁移

任务：把 deepseek 配置从旧 `app_config`（ai_gateway_* 单厂商键）迁移到运营后台 AI 模型市场（`ops_ai_provider`），并完成「模型市场 ↔ 学生端 LLM / OCR 多模态配置」的端到端联动测试。

## 背景与现状

- 模型市场后端已就绪：`ops_ai_provider` 表（vendor/name/protocol/base_url/api_key/models/vision_models/enabled/is_default）、`/api/ops/providers` CRUD + `/{pid}/test` 连通测试、`ai_gateway.resolve_gateway_config(vendor)` 统一收敛。
- 学生端链路已就绪：`config/llm.json`（model+vendor）→ LLM 调用走 `resolve_gateway_config(vendor)`；`config/ocr.json`（multimodal_model+vendor）→ `MultimodalOCRService` 同网关收敛；Settings.vue 厂商下拉 + 按厂商过滤模型（llmVendorModels/ocrVendorModels）。
- **迁移前**：`ops_ai_provider` 为空；deepseek 配置留在主库 `app_config`（ai_gateway_base_url=https://api.deepseek.com、api_key=sk-6f79…、models=deepseek-flash,deepseek-chat、default=deepseek-flash）。

## 改动

### 1. deepseek 迁移到模型市场（已落地，正式数据）

通过运营接口创建厂商（等价运营后台手工新增）：

```
POST /api/ops/providers
name=DeepSeek  vendor=deepseek  protocol=openai
base_url=https://api.deepseek.com
api_key=sk-6****003d（真实 key 已掩码，勿外泄）
models=deepseek-flash,deepseek-chat  vision_models=(空)
enabled=true  is_default=true
```

- 旧 `app_config` ai_gateway_* 键**保留作兜底**：`resolve_gateway_config` 厂商优先，无厂商时才回退旧键（代码注释即此语义）。

### 2. 修正 OCR 视觉模型语义（`backend/app/services/multimodal_ocr.py` + 前端）

**语义纠正**：`vision_models` 留空 = **该厂商不支持 OCR**（纯文本厂商如 DeepSeek），不再是"全部模型可做 OCR"。

- `multimodal_ocr.recognize()`：厂商无 `vision_models` → 直接拒绝（返回"不支持多模态 OCR"提示），不再拿 `default_model`（文本模型）去调视觉接口；显式所选模型不在该厂商视觉列表 → 同样拒绝。
- 后端注释修正：`ops_data.py`（模型/docstring）、`ops_provider_router.py`（ProviderIn）。
- 运营端 `AiMarket.vue`：hint 文案、表格视觉模型列空值显示「不支持」（原「全部」）、表单 placeholder。
- 学生端 `Settings.vue`：OCR 模型列表只取该厂商 `vision_models`（原 `vision_models` 为空时回退 `p.models` 文本模型的错误逻辑已删）；空列表提示指向「AI 模型市场」填写视觉模型。
- 未改动且本就正确：`routers/config.py` 的 `multimodal_providers` 只列 `vision_models` 非空厂商（deepseek 不出现在学生端 OCR 厂商下拉）。

## 验证结果（全部通过，真实调用）

| 项 | 结果 |
|---|---|
| 运营端模型市场列表 | DeepSeek / deepseek / https://api.deepseek.com / deepseek-flash,deepseek-chat / 默认 ✓，key 掩码 `sk-6****003d` |
| 运营端测试连通（AiMarket UI） | ✅ 连接成功，模型 deepseek-flash，真实上游回复 |
| 学生端 GET /api/config/llm | default_model=deepseek-flash、models=[deepseek-flash,deepseek-chat]、providers=[deepseek(默认)]、gateway_configured=true |
| 学生端 POST /api/config/llm | 保存 deepseek/deepseek-flash ✓；未知模型校验 400 ✓ |
| 学生端 LLM UI（浏览器） | AI 厂商下拉选中 DeepSeek（deepseek），模型下拉 deepseek-flash（选中）/deepseek-chat |
| 学生端 GET /api/config/ocr | deepseek 无视觉模型 → multimodal_providers 空（不出现在 OCR 厂商下拉）✓ |
| OCR 视觉厂商动态联动 | 临时加 qwen（vision_models=qwen-vl-plus,qwen-vl-max）→ OCR providers 出现 qwen，浏览器厂商下拉"阿里云百炼（qwen）"、模型下拉 qwen-vl-plus/qwen-vl-max；保存 vendor+model 回读一致 |
| OCR 模型语义修正 | deepseek 无视觉：未选模型→拒绝；显式选模型→拒绝（不再调文本模型）；视觉厂商：未选→vision_models[0]（qwen-vl-plus）、列表内→正常、列表外文本模型→拒绝；运营端表格视觉模型列显示「不支持」 |
| 旧网关兜底测试 | POST /api/config/ops/ai-gateway/test 仍可用（deepseek 旧键） |

## 测试数据清理

- 临时 qwen 视觉厂商（id=2）：已删 ✓
- 测试官网账号 13800000001（accounts id=19）+ registry 空间记录（XOPAgS4iqvzrlA）：已删 ✓
- **孤儿文件**：`backend/trial_data/tenants/XOPAgS4iqvzrlA.db`（1MB 模板复制，不再被引用）——删除命令被审批系统拦截，需用户手动删除或授权后清理。
- 学生端 `config/llm.json` 保留 deepseek/deepseek-flash（迁移后的正确默认）；`config/ocr.json` 已恢复空默认。

## 遗留

- 孤儿空间库文件删除（见上）。
- `tools/tmp/` 下测试脚本（test_llm_ocr_link.py / test_student_link.py / test_ocr_fallback.py / add_qwen.py / cleanup_test_account.py / try_login.py / admin_token.txt 已清空）——临时产物，可随 `python tools/cleanup.py` 收尾。
