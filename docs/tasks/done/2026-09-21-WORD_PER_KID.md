# WORD_PER_KID — 单词库共享、复习数据按小孩隔离

- [x] 后端：models/word.py 新增 WordProgress 表（word_id+user_id 唯一），WordReviewLog/WordReview 加 user_id 列
- [x] 后端：迁移脚本（建表/ALTER/把 Word 旧复习数据归给第一个小孩 id=2）
- [x] 后端：word.py 全部复习相关接口加 user_id（list/review/start/submit/stats/errors/memory-curve/get_word）
- [x] 前端：Words.vue（学生端）请求带 kidStore.activeKid.id
- [x] 前端：WordLibrary.vue（家长端）加小孩下拉选择，按小孩显示复习情况
- [x] 验证：后端冒烟全过（隔离/提交/默认回退/errors 修复）；SFC 编译校验通过
- [ ] 阻塞：vite build 因系统虚拟内存耗尽失败（QwenPaw+8012 后端占用）；待内存空闲后 npm run build
