# WORD_LEARN_ENHANCE — 单词学习优化：例句融入 + 拼读带读 + 可配置学习模式

## 目标
把单词学习从"孤立背词"升级为"语境化学词"：单词卡带读时带例句（英+中），
拼读拆解随卡展示，例句数量/翻译显示按「学习模式（入门/标准/进阶）」可配置。

## 设计决策（与用户讨论后定稿）
- 例句存 `word.example_sentences`（JSON 数组 `[{"en":"...","zh":"..."}]`，1-2 条/词）
- 例句由 AI 生成，与拼读/词根/相关词同入「记忆增强包」；老词只缺例句 → 单独补例句（不覆盖已编辑字段）
- 例句必须语法正确、贴近孩子生活、难度 i+1；严禁 AI 裸生成不校验（石化风险）
- 学习模式：前端 localStorage 配置（入门=无例句/标准=1句/进阶=2句+翻译可隐藏），默认「标准」=默认即合理
- 例句发音：浏览器 speechSynthesis en-US（不写 TTS 文件缓存，避免污染 audio_dir）
- 数据隔离：example_sentences 是 A 类（全局共享），不加 user_id

## 步骤
- [x] 1. 模型 + 迁移：`word` 表加 `example_sentences TEXT`（models/word.py + main.py _ensure_column）
- [x] 2. Schemas：WordBase/WordUpdate/WordResponse 支持 example_sentences（JSON 解析）
- [x] 3. 后端增强：_enhance_words_llm prompt 加例句生成；新增 _fill_sentences_llm（只补例句）；_needs_sentences；worker 分两类处理
- [x] 4. 后端返回：list/get/daily-task/memory-review 返回 example_sentences（解析 JSON）—— py_compile 通过
- [x] 5. 前端 Words.vue：学习卡 + 新词学习题加「例句」区块（英+中+喇叭）
- [x] 6. 前端学习模式：设置区加「学习模式」选择（入门/标准/进阶），localStorage；例句数量/翻译按模式
- [x] 7. 前端 WordLibrary.vue：详情「记忆增强」tab 展示例句 + 批量补生成入口
- [x] 8. 验证：后端 py_compile + 冒烟（列迁移✅ daily-task/list 返回例句✅ /enhance 真实 LLM 生成 apple 2 条例句✅）+ 前端 npm run build ✅
- [ ] 9. 归档：移 docs/tasks/done/ + 更新索引 + 提交 git

## 验证记录
- `py_compile` 4 个后端文件通过
- `[migrate] word 增加列 example_sentences` 成功（启动时 _ensure_column）
- 冒烟（直接调 router 函数，TestClient 版本不兼容）：
  - daily-task total=35，sample=apple 返回 `[{'en': 'I like to eat apples.', 'zh': '我喜欢吃苹果。'}, {'en': 'This apple is red.', 'zh': '这个苹果是红色的。'}]`
  - list_words total=313，字段 example_sentences 存在
  - /enhance（limit=1）真实 LLM 生成 apple 例句并落库 ✅
- 前端 `npm run build` → BUILD_OK
- 注：`[migrate] 跳过激励数据归属迁移: UNIQUE constraint failed: achievement_progress` 为既有逻辑与存量数据冲突，被 try 捕获跳过，非本次改动引入

## 遗留/说明
- 存量 313 词无例句：可在单词库「记忆增强」tab 筛选条件点「补生成」批量补齐（每批最多 50 个，20/次 LLM 调用）
- 例句发音走浏览器 SpeechSynthesis en-US，不走 TTS 文件缓存（避免污染 audio_dir）
- 新词学习题（认一认选择题）例句只显示英文不显示中文——防止中文翻译泄露答案
