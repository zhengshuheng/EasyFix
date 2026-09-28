# 知识点导入优化（智能导入自动决策 + 分组列表）— 2026-09-25

## 背景
教材 PDF 导入链路完成（北师大版数学 3上 20 条）。用户提出 6 点导入体验优化，
已完成并端到端验证。

## 完成项
1. **智能导入自动决策**（`ops_data_router.py: smart-import`）：
   ①在线知识大纲(ctsf-online) → ②在线教材资源(textbook-online) → ③本地大纲缓存(ctsf-local)
   → ④本地教材PDF(textbook-local) → ⑤AI生成(ai)。慢路径走异步任务，PDF 失败自动降级 AI。
2. **知识点来源方式**：`ops_knowledge_point.source_type` 列（ctsf-online/ctsf-local/
   textbook-online/textbook-local/ai），`ensure_ops_tables` 兜底补列；列表/编辑弹窗显示来源标签。
3. **按单元分组 + 保序**：`GET /knowledge-points/grouped` 按单元分组（单元按首次 id、组内按 id），
   前端 KpManage 分组渲染（单元标题行 + 知识点行）。
4. **按钮与筛选解耦**：智能导入/批量导入/新增 不再依赖筛选条件 disabled。
5. **去重合并更新**：统一 `_kp_upsert`（subject+version+grade+semester+name 同名更新），
   三种来源均走 upsert。
6. **默认选中科目+版本**：进入自动选第一科目/版本/册，无"先选科目+版本"空提示。

## 配套改动
- `ctsf_import.py`：`fetch_outline` 支持本地缓存落盘（data/textbooks/{source}/outlines/{fn}）
  + `use_cache` 模式 + `load_local_outline`/`local_outline_exists`。
- `AiImportDialog.vue`：智能导入改调 smart-import（同步直接完成；异步轮询任务进度条）。

## 验证
- API：grouped 保序/来源；smart-import 北师大版→textbook-online（异步完成）；湘教版→AI 兜底
  （42 条/9 单元，已清理）；重复导入 total 不变（去重）。
- 浏览器：按钮解禁、默认选中、分组视图、来源标签、智能导入秒级完成（人教版 1上→在线知识点）。

## 注意
- 历史数据 source_type 为 NULL 显示"未知"；用户导入该册后自动回填正确来源。
- 运营后台构建必须 `npm run build:ops`（输出 frontend/dist-ops，后端 mount /ops）。
- PDF 提取名称不稳定可能导致多次导入少量语义重复（同名才合并）。
