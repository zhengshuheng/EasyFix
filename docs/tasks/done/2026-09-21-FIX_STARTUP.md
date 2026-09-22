# FIX_STARTUP — 修复服务启动不起来（kid 重构后遗留引用）
- [x] 定位根因：question.py 用了 get_current_kid_id / ErrorQuestion 但没导入 → NameError 导致整个后端起不来
- [x] 补导入 + question.py 全端点切 error_question（GET 列表/详情/练习历史/新增/批量/更新/删除/筛选选项）
- [x] 编译 + 导入验证通过；8016 起服务验证 /api/subjects、/api/questions、/api/practice-sets 均为 200
- [ ] 修 stats.py：PracticeSetQuestion.question_id 已改名（/api/stats/overview 500），Question → ErrorQuestion + 按小孩过滤
- [ ] 修 similar.py / learning_report.py / learning_analysis.py 遗留 Question 引用
- [ ] 浏览器端到端验证（学生端错题/练习/统计）
- [ ] 通知用户重启 8012 生效
