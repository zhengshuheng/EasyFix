# HALF_CREDIT — 缺单位半对判分 + 订正机制

- [x] 后端 assessment.py：新增 `_extract_unit` / `_grade_fill_answer` 三态判分（数值对+缺单位→0.5），submit 循环改造 correct 支持 0.5
- [x] 前端 Assessment.vue：answerState 三态（full/half/wrong），half 时输入框可编辑 + 订正按钮，订正成功补分
- [x] 前后端判分一致性自测（后端 15 用例 PASS + submit 端到端 0.5/1.0/0.0 + vite build 通过）
