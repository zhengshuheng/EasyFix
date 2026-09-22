# PRACTICE_REFLOW — 练习流程重构
## 阶段1：出题入口迁移 ✅
- [x] Questions.vue 移除「生成练习」按钮与弹窗逻辑
- [x] PracticeSets.vue 顶部加「出题」按钮 + 生成练习弹窗（学科/年级/数量，自动生成PDF）
- [x] npm run build 构建通过
- [x] git 提交

## 阶段2：AI 批改（LLM 一键批改）
- [ ] 后端：POST /api/practice-sets/{id}/ai-grade —— LLM 逐题判对错 + 错因分析
- [ ] 前端：批改交互（输入/粘贴学生作答 → 逐题结果 → 确认落库）
- [ ] 构建 + 提交

## 阶段3：错题回流
- [ ] 批改确认时答错的题自动生成错题（对应学科错题本，无则自动建）
- [ ] 错误类型 LLM 预判 + 家长可改
- [ ] 构建 + 提交
