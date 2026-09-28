# PARENT_GUARD_DELETE — 学生端删除操作家长认证

> 需求：单词、练习、错题等学生端的删除操作需要家长认证，学生（role=child）自己不能删除。

## 方案

- **后端兜底**：学生端数据删除接口加 `require_admin`（admin=家长）依赖，child 直接调接口返回 403。
- **前端体验**：孩子会话下点击删除 → 弹「家长验证」密码框 → 验证通过后执行删除 → 恢复孩子会话；家长会话直接删除。

## 后端（5 个接口加 require_admin）✅

- [x] `question.py` `DELETE /api/questions/{question_id}`（错题）
- [x] `word.py` `DELETE /api/words/{word_id}`（单词）
- [x] `practice_set.py` `DELETE /api/practice-sets/{practice_set_id}` + `POST /api/practice-sets/batch-delete`
- [x] `learning_report.py` `DELETE /api/learning-reports/{report_id}`
- [x] `reading.py` `DELETE /api/readings/{reading_id}`
- [x] `py_compile` 通过

> 注意：`phonics.py` `POST /api/phonics/wrong-words/clear` 兼作练习自动「掌握即移除」逻辑（Phonics.vue `saveAttempts`），**不**加后端拦截；拼音错题池移除属于学习流程，危害低。仅前端手动删除按钮加认证弹窗。

## 前端

- [x] `ParentLockDialog.vue`：文案 props 化（title/tip/confirmText）
- [x] 新建 `frontend/src/composables/useParentGuard.js`：`guard(action)` 家长直通 / 孩子弹窗 → 验证通过执行 → 恢复孩子会话
- [x] `Questions.vue` deleteQuestion 接入
- [x] `Words.vue` deleteWord 接入
- [x] `PracticeSets.vue` deletePracticeSet + batchDelete 接入
- [x] `LearningReports.vue` deleteReport 接入
- [x] `Reading.vue` deletePassage 接入（删除改用 api 实例带 token，其余读取保持裸 axios）
- [x] `Phonics.vue` removeWrong + clearWrongs 接入（仅弹窗，接口不动）

## 验证

- [x] 后端冒烟：child token 调 DELETE → 403；admin token → 204/404（不存在的 id，未污染数据）。12 项全 PASS。
- [x] 前端 `npm run build` 通过（vite 28.42s）
- [x] 说明：原 8012 uvicorn（PID 24800，旧代码）已 kill，需重启后端加载新代码
