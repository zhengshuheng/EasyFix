# SUBJECT_TABS — 主菜单重构：动态学科一级菜单 + 学科页内部 tab
- [x] 新建 SubjectSpace.vue（/space/:id）：内部 el-tabs，错题/练习 + 英语加单词/阅读/学习报告（lazy 加载）
- [x] router 加 /space/:id
- [x] App.vue 菜单重构：一级菜单 = 动态学科(v-for subjects) + 学习分析 + 激励中心 + 家长中心；删除 错题/练习/英语子菜单/单词/阅读/学习报告 菜单项
- [x] Logo 点击回 /home；openSubjectSpace 同步空间学科
- [x] 旧路由 /questions /practice-sets /words /reading /learning-reports 保留（首页卡片与 tab 内嵌仍用）
- [x] vite build 通过（27.4s）
- [ ] 用户 Ctrl+F5 验证
