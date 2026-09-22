# KID_ISOLATION — 错题/练习重构 + 全链路按小孩隔离（实施中）

## 用户定的方向
1. 错题来源 = 批改时判错 → 进错题库表；错题表与练习表互相可查；复习次数/正确率从练习（作答）数据得出。
2. 现有 144 题 / 29 卷视为脏数据，全部清空。
3. 隔离范围：错题、练习、统计、学习报告、单词、激励。
4. 单词本体共享（两个小孩共用一份词库）；单词进度/复习次数/正确率按小孩隔离。
5. 家长中心 = 全家配置，不选小孩；主页入口必须选一个小孩，学生端才可操作。

## 用户拍板的三件规则（已定）
- 已掌握：**连续答对 2 次** → status='mastered'，移出错题本。
- 手动上传错题：**保留**（拍照/OCR 录入，source='upload'，保留错题来源）。
- 错题列表统计：**缓存列**（review_count/correct_count/wrong_count/accuracy/correct_streak），**每次批改同事务更新**；事实来源仍是 practice_attempt，可全量重算。

## 目标数据模型（已建）
新表
- practice_question：练习题目快照（user_id, subject_id, 题干/选项/答案/解析, 题型, knowledge_point, difficulty, source[ai|error_review|upload], error_question_id）
- practice_attempt：作答记录（user_id, practice_set_id, practice_question_id, error_question_id, student_answer, is_correct, graded_by, answered_at）
- error_question：错题库（user_id, error_book_id, subject_id, 本体快照, source[practice|upload], source_practice_question_id, 缓存统计列, correct_streak, status[active|mastered], first/last_wrong_at）
改造
- practice_set：+ user_id（NOT NULL）；作答结果不再存 practice_set_question
- practice_set_question：改指向 practice_question，去掉 is_correct/student_answer
- learning_report / word_review_session：+ user_id
- question / 旧 practice_set_question 数据：已清空；question 表废弃（保留表结构，代码不再引用）

## 实施进度
- [x] M1 数据模型 + 迁移脚本（`tools/migrate_kid_refactor.py`，已跑：清 144 题 / 154 关联 / 29 卷；新表已建；演示数据初始化停用）
- [ ] M2 练习链路：AI 出题/组卷 → practice_question 快照 → 做题 → practice_attempt → 批改
- [ ] M3 错题派生：答错入库 + 缓存列更新 + 连续答对2次移出 + 错题列表/复习组卷 + 手动上传归位
- [ ] M4 隔离贯通：X-Kid-Id 注入 + 全接口过滤 + 学生端强制选小孩 + 家长中心去选择
- [ ] M5 统计/学习报告按小孩（聚合 attempt）
- [ ] M6 双小孩实测 + 提交

## 待验证
- 生成练习集后新卷在列表可见（重启服务 + Ctrl+F5）
- 两个小孩分别登录：错题/练习/统计/单词进度互不可见

## 备份
- 重构前数据库快照：`backend/easyfix.db.pre-kid-refactor-20260917_224048`
