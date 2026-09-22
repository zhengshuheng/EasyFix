# INCENTIVE_COMPLETE — 激励中心半成品补全
## 现状盘点（已完成）
- [x] 后端基础设施：8 张表（star_action/star_balance/star_record/achievement/achievement_progress/achievement_config/reward/redemption）
- [x] 后端 API：积分余额/明细/手动调整/行为CRUD、成就CRUD+进度、奖励CRUD+兑换+图片上传、概览、触发接口
- [x] MotivationService：trigger_action/连续学习/单词正确率/兑换
- [x] 预设数据：11 行为 + 18 成就 + 启动初始化
- [x] 已接入触发点：review_practice_set（复习/拍照交卷/单词≥10）、generate_similar、review_word_accuracy
- [x] 家长端 IncentiveConfig.vue：行为/成就/奖励 CRUD + 积分调整 + 图片上传
- [x] 学生端 Motivation.vue：积分概览/成就墙/商城/明细（界面）

## 阶段一（P0 核心闭环，后端）
- [x] motivation.py：余额/明细/调整/兑换/兑换记录/进度/概览/触发 全部按小孩隔离（get_current_kid_id/get_required_kid_id）
- [x] motivation.py：get_progress 返回真实统计并同步 current_count
- [x] services/motivation.py：_get_achievement_total_count 按 user_id 过滤（WordProgress/PracticeSet.user_id/ErrorQuestion.user_id）
- [x] 触发点补全：create_practice_set（practice_set.py）、upload_question（question.py create/batch）、review_word（word.py 单词复习）、daily_login（新 POST /motivation/checkin 按日幂等）
- [x] main.py 启动迁移：激励数据 user_id=1(admin) 归第一个小孩；init_achievement_progress 按每个小孩初始化
- [x] 语法/冒烟验证（8016 最小挂载：8 接口 200 + checkin 幂等 + 400/404 边界；测试数据已清理）

## 阶段二（P0 前端闭环）
- [x] Motivation.vue：redeemReward 调后端 + 刷新余额/库存/兑换记录
- [x] Motivation.vue：成就分组映射修正（continuous→连续学习、review_word_accuracy→正确率成就）
- [x] Motivation.vue：新增「我的兑换」区块（redemptionList）+ 已兑换状态
- [x] Motivation.vue：积分明细 action_code 中文显示；成就详情补触发条件
- [x] IncentiveConfig.vue：积分调整加小孩选择下拉
- [x] Home.vue：进入学习时调用每日签到（daily checkin）
- [x] vite build 验证（378 modules transformed，dist 已更新）

## 阶段三（P1/P2 完善）
- [ ] 兑换核销闭环：Redemption 加 status 字段 + POST /rewards/redemptions/{id}/grant + 家长端「兑换记录」tab
- [ ] 奖励上下架（is_active）：getRewards 支持 include_inactive；家长端表单加开关
- [ ] 成就/行为表单补 icon/description 字段
- [ ] 成就解锁全局庆祝提示
