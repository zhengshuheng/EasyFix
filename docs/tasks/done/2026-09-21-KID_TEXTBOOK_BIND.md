# KID_TEXTBOOK_BIND — 小孩教材知识点绑定 + AI 出题按版本过滤

- [x] 读现状代码（users.py/UserManage.vue/SelectKid.vue/PracticeSets.vue/knowledge_point.py）
- [x] P1 数据模型：knowledge_point 加 source/edition_key/revision 列；新建 kid_textbook 表
- [x] 后端：kid_textbook CRUD API + 建小孩可带 textbooks + textbook_meta 版本清单/edition_key
- [x] 前端：建小孩/账号管理 教材版本选择（UserManage.vue）+ api/store 封装
- [x] AI 出题界面：按小孩教材版本显示并过滤知识点（PracticeSets.vue）
- [x] 构建前端 + 8016 实测（含修复 edition_key 必填报错：改 Optional 由后端兜底生成）


