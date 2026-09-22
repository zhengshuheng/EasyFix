# ENROLLMENT_GRADE — 入学日期自动推断年级，取消全局默认年级

- [x] 后端：users 表加 enrollment_date 列 + 旧 current_grade 反推迁移（main.py `_backfill_user_enrollment_date`）
- [x] 后端：infer_grade() 按 9 月 1 日学年分界推断年级（timeutil.py），users API 返回 enrollment_date + current_grade 推断值
- [x] 后端：PUT 显式 null 可清空入学日期（model_fields_set 判断）；创建小孩支持 enrollment_date
- [x] 前端：UserManage.vue 创建/编辑弹窗改「入学日期」日期选择器，表格列改「入学日期 / 当前年级」
- [x] 前端：Settings.vue 删除「默认年级」表单项与 gradeOptions，提示改为入学日期说明
- [x] 前端：Home.vue 移除 appConfigStore 加载与 ensureDefaultGrade(6) 兜底
- [x] 前端：SelectKid.vue 小孩卡片显示推断年级徽标；kid store 存 enrollment_date
- [x] 构建 + 8016 实测：迁移后演示小孩=三年级(2024-09-01)、郑予/郑好=一年级(2026-09-01)；改日期联动 2/3 年级；点郑予自动进 1 年级空间；系统配置无「默认年级」
- [x] 选择页删除「快速进入指定空间」预选区（学科/年级下拉+applySpace+预选初始化+样式），点小孩一律按推断年级进 /home；构建并实测：选择页无残留，点郑好(2023-09-01 入学)→自动进 4 年级空间
- [ ] 用户在 8010 重启后端（后端有改动）+ Ctrl+F5 验收
