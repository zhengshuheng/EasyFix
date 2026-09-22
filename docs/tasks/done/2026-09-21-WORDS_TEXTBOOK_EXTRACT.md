# WORDS_TEXTBOOK_EXTRACT — 单词库「教材单词表提取」松耦合功能
- [x] 调研：教材同步只提知识点；OCR(_get_ocr/_page_to_text)/LLM(_llm_json/_parse_json)/batch 入库可复用
- [x] 后端 word.py 新增 POST /words/extract-from-textbook（多图+PDF→OCR→LLM单词表提取→查重标记 existing）
- [x] 前端 wordApi 新增 extractFromTextbook（multipart）
- [x] 前端 WordLibrary.vue 导入弹窗加「教材单词表提取」radio + 多文件上传 + 提取按钮 + 预览勾选列（已存在默认不勾选）
- [x] 构建前端 + 后端重启 + 8016/TestClient 端到端实测（图片 OCR 12/12 → mock LLM 提取 → 查重 3 个 existing=True；真实 LLM 因 deepseek-flash 402 余额不足暂不可用）
- [x] 清理临时文件；README 不涉及（单词域功能）
