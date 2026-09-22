# WORD_AUTO_ENHANCE — 记忆增强改为导入/新增时自动附带

- [x] 摸底：新增与导入路径（text/file/image/textbook/ai）全部经 `POST /words` 逐个创建；独立操作= `POST /words/enhance` + WordLibrary 顶部按钮/详情页按钮
- [x] 后端：抽取共享核心 `_enhance_words_llm(db, words)`（≤20 词/次 LLM 调用，拼读规则/词根词源/相关词）
- [x] 后端：新增/批量创建后 `_schedule_auto_enhance`（去抖 4s 后台批处理，静默失败，不阻塞接口）
- [x] 后端：`/enhance` 改为复用核心；待增强判定改为「拼读规则+词根词源都缺」（去掉 mnemonic 旧条件）
- [x] 前端：WordLibrary 移除「生成记忆增强」按钮 + batchEnhance/enhanceOne；详情页空态改为「导入/新增时自动生成」
- [x] 前端：MemoryReviewPanel 空态文案同步
- [x] 验证：8017 沙盒（scratch 库）实测新增 sunny → 6s 自动出现 phonetic_rule/word_root/related_words ✅；vite build 通过，dist 无旧按钮残留
- [x] 归档到 docs/tasks/done/

## 结果与验证证据

- **实现**：`backend/app/routers/word.py` 新增 `_needs_enhance` / `_enhance_words_llm` / `_schedule_auto_enhance` / `_auto_enhance_worker`；`create_word` 与 `batch_create_words` 落库后登记待增强词，后台线程去抖 4s 合并一批（每批 ≤20 词一次 LLM 调用），失败静默（打日志）。
- **沙盒实测（8017 + easyfix.scratch.db）**：POST /words 创建 sunny → 约 6s 后 GET 详情返回 phonetic_rule（s→/s/、u→/ʌ/、nn→/n/、y→/i/…）、word_root（sun 太阳 + -y 形容词后缀 → sunny）、related_words（sun/rainy/windy）。RESULT: PASS。沙盒与 scratch 库已清理。
- **顺修既有 bug**：`WordResponse.related_words` 声明为 List，但 DB 列存 JSON 字符串（`_dump_json` → `'[]'`），导致 `POST /words` 响应校验 500（行已落库但前端算失败）→ 在 `backend/app/schemas/word.py` 加 `field_validator(mode="before")` 解析 JSON 字符串。
- **前端**：WordLibrary 顶部「生成记忆增强」按钮、batchEnhance/enhanceOne 删除；详情页「记忆增强」tab 空态改为「新增/导入单词时自动生成…稍等刷新」；新增/导入成功提示追加「（记忆增强自动生成中）」；MemoryReviewPanel 空态同步。构建产物 `Management-4e8128f4.js`（旧按钮文案 0 残留）。
- **`/enhance` 端点保留**（未暴露 UI）：用于历史存量单词补增强（现有词不会自动回填，如需补增强可调该接口）。
