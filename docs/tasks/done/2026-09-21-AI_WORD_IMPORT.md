# AI_WORD_IMPORT — AI 智能导入单词（LLM 生成）
- [x] 调研：llm 服务调用方式、教材版本清单、word extract 现有 LLM 调用、前端导入弹窗结构
- [x] 后端：POST /api/words/ai-generate（textbook 模式：学科/版本/年级/册次 → 构造指令；custom 模式：自然语言指令）→ LLM 生成 Unit 格式文本 → 解析返回
- [x] 前端：导入弹窗加「AI 智能导入」选项（教材模式下拉 + 自定义指令 + 生成按钮）→ 结果进预览 → 复用导入
- [x] 构建 + 重启后端 + 8016 实测（custom 模式 6 词✅ + textbook 模式沪教版深圳三上 137 词✅ + UI 149 词预览✅）
