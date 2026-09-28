# 2026-09-26-textbook-ocr-strategy.md — 教材识别策略升级

## 需求（用户 9/26 确立）
1. 识别方式：**优先多模态模型，本地模型兜底**——先检测是否配置多模态模型、key 是否有效，无效则降级本地 OCR
2. 内容识别：**先识别目录页，再快速定位单元页**
3. **权威在线知识源优先**（官网 → GitHub 权威大纲），命中即用，不做教材 OCR
4. 所有模式不可行 → **LLM 生成兜底**
5. 教材书本生成模式增加**识别方式字段**，便于知道知识点通过什么生成

## 落地

### 1. 识别方式字段 ocr_mode（教材书本生成记录来源方式）
- `ops_knowledge_point` 新增列 `ocr_mode`，取值：
  | ocr_mode | 含义 | 对应场景 |
  |---|---|---|
  | authority | 权威在线源 | ① 权威大纲（官网/教育部公开大纲 → GitHub 教材大纲）命中 |
  | multimodal | 多模态识别 | ② ④ 教材识别，多模态模型可用且 key 有效 |
  | local | 本地 OCR | ② ④ 教材识别，无多模态配置 / key 无效降级 |
  | llm | AI 生成 | ⑤ 兜底（教材处理失败自动转 AI / AI 指令生成 / 手动导入） |
- `ensure_ops_tables` 幂等补列 + 历史回填（ctsf-*→authority，textbook-*→local，ai→llm）
- 所有写入点标注：大纲导入 authority、教材任务按实际识别器 multimodal/local、降级/手动/AI 任务 llm
- 运营端知识点列表新增"识别方式"列（前端 KpManage.vue + 编辑弹窗显示）

### 2. 多模态优先 → 本地 OCR 降级（textbook_service.py）
- `_resolve_vision_gateway()`：模型市场 vision 厂商（vision_models 非空 + enabled）+ key 有效性检测（GET {base_url}/models，401/网络失败视为无效）→ 任一有效即用；全部无效/未配置 → 本地 RapidOCR
- `_vision_page_text()`：单页 → 视觉模型识别（openai 兼容 / anthropic 两种 content 格式）
- `extract_text()` 支持 vision_cfg：多模态逐页识别，缓存与本地 OCR 分开（.mm.txt）

### 3. 先目录页 → 快速定位单元页
- `_toc_from_text()`：取前 6 页，LLM 判断是否为目录页（词条+页码模式，兼容 OCR 无"目录"二字）→ 输出 [{unit, page}]（PDF 物理页号）
- `split_units_from_toc()`：按单元页码范围精确切分 OCR 文本
- `split_units()` 增强：正则无单元标题时 LLM 推断单元边界 + 模糊定位（跳过页码/页脚噪音行）
- 两种识别模式都先走目录定位（多模态模式目录文本更清晰）

### 4. 权威在线知识源优先（smart-import 决策链）
- ① 权威在线知识源（官网/教育部公开大纲优先，其次 GitHub 教材大纲；命中即用、不做教材 OCR）→
  ② 本地权威大纲缓存（之前已下载过的权威大纲，秒级导入、准确性高，**优先于在线教材**）→
  ③ 在线教材资源（识别优先多模态，key 无效降级本地 OCR；先目录页定位再按页提取）→
  ④ 本地教材 PDF（同③）→ ⑤ AI 生成兜底
- 说明：当前无稳定官网知识点公开 API，实际权威源 = GitHub ChinaTextbookStudyFree 大纲（由教材官网公开内容整理）；接入官网源时置于 ① 首位
- 弹窗策略说明文案同步升级（AiImportDialog.vue 顶部常驻 5 级决策 + 识别方式说明）
- 2026-09-26 追加：按用户要求将 ③ 本地权威大纲缓存 提前至 ②（在线教材之前），后端代码块顺序、docstring、弹窗文案三处同步
- 2026-09-26 追加：按用户要求将 ④ 本地教材 PDF 提前至 ③（在线教材之前）→ 最终决策链：
  ① 权威在线知识源 → ② 本地权威大纲缓存 → ③ 本地教材 PDF（优先于在线下载）→ ④ 在线教材资源 → ⑤ AI 生成兜底；
  实测北师大三上由 textbook-online 改走 textbook-local（148 条/10 单元）
- 2026-09-26 追加：防重逻辑（同一教材反复重跑智能导入不累积重复知识点）——
  `ops_knowledge_point.import_batch` 批次列 + 教材任务成功后 `_clean_old_kp_batches()` 清理同教材旧批次（软删）；
  保留无批次行（手动新增/AI 指令生成/权威大纲）；
  实测北师大三上连续重跑 3 次，条数稳定 147-152（此前会累积到 224）

### 5. 修复（验证中发现）
- `_kp_upsert` 不再过滤 deleted：软删行按唯一约束占名，查询过滤 deleted=False 导致 INSERT 撞 UNIQUE → 命中任意行并复活（deleted=False）
- `_kp_upsert` 开头 `db.flush()`：SessionLocal autoflush=False，同批导入跨单元同名知识点时 pending 行查询不可见 → 二次 INSERT 撞 UNIQUE；flush 后同名走 UPDATE

## 验证（真实数据）
- 北师大版数学三年级上册 smart-import：决策 textbook-online → 目录定位 **10 个单元** → 148 条知识点全部 `source_type=textbook-online, ocr_mode=local`
- 分组：混合运算 19 / 加与减 14 / 总复习 12 / 整理与复习 15 / 乘法 18 / 观察物体 10 / 周长 14 / 数学好玩 15 / 认识小数 14 / 乘与除 17
- 多模态检测：当前模型市场仅 DeepSeek（无 vision）→ 正确返回 None 降级本地
- 历史回填：ctsf-online 32→authority、ai 42→llm、textbook-online 41→local（全库）
- 清理：失败任务 AI 兜底冗余 36 条 + 旧"全册"残留 11 条已软删（北师大 3 上）
- 前端 build:ops 通过（识别方式列 + 弹窗文案）

## 待用户验收
- 运营后台 Ctrl+F5 强刷：知识点列表"识别方式"列、智能导入弹窗策略说明
- 北师大版 3 上列表现为 10 单元分组（原"全册"20 条已升级替换）
