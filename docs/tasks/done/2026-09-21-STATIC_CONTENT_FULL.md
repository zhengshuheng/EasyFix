# STATIC_CONTENT_FULL — 语法/拼读静态知识一次性生成完整，移除家长 AI 生成入口

- [x] 摸底：grammar_lesson 44 点，缺正文 28 个（skeleton）；phonics_rule 40 条三类齐全（vowel 22/consonant 17/silent_e 5）已完整
- [x] 生成 28 个语法教程正文（按板块调 8012 `/api/grammar/ai-generate-tutorial`：词法·名词3/代词4/动词5/形副4/其他4/句法8 全成功，LLM 一次性补齐；44/44 全部有正文）
- [x] 前端 GrammarManager.vue：移除骨架生成按钮+弹窗、批量教程按钮、行内生成教程按钮；提示改为「语法教程已完整内置」；保留新增/编辑/删除
- [x] 前端 Phonics.vue：移除「AI 生成该类规则」按钮 + aiGenerate + MagicStick + aiLoading；空态/无示例词文案更新（PhonicsPanel.vue 为无引用死代码，未动）
- [x] 验证：查库 44 点全部有正文（content_md/examples 非空）；vite build 通过；dist 中旧生成入口文案 0 残留（Management-43a76413.js 新提示就位、无 ai-generate-skeleton 引用；Phonics-2817e8a3.js 无 ai-import 引用）
- [x] 归档 docs/tasks/done/

说明：后端 /api/grammar/ai-generate-* 与 /api/phonics/ai-generate 接口保留（前端已无入口，留作未来扩展/补数据用）。
