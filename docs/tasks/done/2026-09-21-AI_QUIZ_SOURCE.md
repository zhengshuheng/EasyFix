# AI_QUIZ_SOURCE — AI 练习题不再混进错题列表 / 新卷在列表可见

现象：刚生成的 AI 练习题出现在「错题列表」，而练习列表里看不到新卷。
诊断：
1. AI 出题的题会写入 `question` 表（既有设计），而 `GET /api/questions`（错题列表）只看
   `deleted == False`，不区分来源 → 104 道 AI 练习题混进错题列表（`error_book_id` 全为 NULL）。
2. 练习列表按 `subjectStore.activeSubjectId + activeGrade` 过滤，而 AI 出题弹窗里可另选年级
   （如刚生成的 ps 26 是 1 年级，当前视图是 6 年级）→ 生成完刷新列表看不到新卷。
3. `practice_set.source_type='ai'` 是精确判据：15 个 AI 卷关联 104 道题，全部无错题本。

- [x] 1 排查根因（数据 + `/api/questions` 与 `/api/practice-sets` 的过滤口径差异）
- [x] 2 后端：`question` 加 `source` 列（'ai'）+ `main.py` 迁移 + 幂等回填 104 道旧 AI 练习题
- [x] 3 后端：AI 出题入库写 `source='ai'`；薄弱知识点统计、学习报告、统计概览、错题组卷均排除 AI 练习题
- [x] 4 后端：`/api/questions` 默认排除 AI 练习题（`include_ai=true` 可放开）→ 实测 132 → 28 条
- [x] 5 前端：生成成功后自动对齐学科/年级视图并提示（否则新卷在列表里看不到）
- [x] 6 端到端实测（错题列表只剩真实错题；生成 ps 27 后列表第一行即新卷；切到 1 年级空间才看到 ps 26 → 证实根因）+ 提交
- [x] 7 补闭环：删除 AI 练习集时一并软删除其题目（否则题从错题列表隐藏后成为不可见孤儿）→ ps 28 实测题 138/139 随卷 deleted=1
- [x] 8 清理修复前测试卷（ps 27）留下的 5 道孤儿题（133-137）→ 库内现为 28 错题 + 104 AI 练习题
- [x] 9 提交 `7339bca`（dev1.0，7 files，70+/7-）
