# ERRORBOOK_ISOLATION — 错题本按小孩隔离
- [x] 1. 模型 error_book 加 user_id + SQLite 迁移 + 旧数据按方案B分配/复制给小孩
- [x] 2. 自动创建逻辑改为按小孩（每小孩每学科一条）
- [x] 3. 接口 /api/error-books 鉴权+按小孩过滤（admin看全部/child只看自己+403跨小孩）
- [x] 4. 前端：错题本管理页按小孩筛选/显示归属/新增选小孩；delete_user 软删小孩错题本
- [x] 5. 验证：后端代码级冒烟全过 + vite build 26.8s 通过
