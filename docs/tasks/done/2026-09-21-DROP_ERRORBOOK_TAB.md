# DROP_ERRORBOOK_TAB — 删除 家长中心·题库管理 → 错题本管理 tab

- [x] 1. 确认功能冗余：建小孩自动建各学科错题本（backend/app/routers/users.py:150）、批改/上传错题时兜底自动建（services/practice_flow.py:138/169、routers/question.py:307/559）、前端无任何页面调用 /api/error-books
- [x] 2. 删除 tab-pane + 新增/编辑弹窗 + errorBooks/kids/errorBookForm 等 state + fetchErrorBooks/fetchKids/openCreateErrorBook/createOrUpdateErrorBook/editErrorBook/deleteErrorBook + fetchAll 里两处调用 + 未使用的 usersApi import
- [x] 3. 重建前端（Management-4259cb06.js / index-5271703d.js）
- [x] 4. 实测：tab 列表只剩 学科管理/标签管理/错误类型管理/知识点管理/英语单词库；逐个点开均有数据无报错；产物中「错题本管理」「新增错题本」「errorBooks」字样已消失
