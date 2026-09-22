# SWITCH_REFRESH — 切换年级/小孩后当前页面数据不刷新
- [x] 定位根因：各页面只在 onMounted 读一次 subjectStore.activeGrade / kidStore.activeKid，顶栏切换后不重新拉数据（App.vue 切年级只在非首页时 push('/home')，切小孩原地不动）
- [x] 方案：给 router-view 加 spaceKey（小孩+学科+年级），空间变化时整页重挂载并重新拉数据，一次覆盖所有页面
- [x] 改 App.vue：新增 spaceKey computed + <router-view :key="spaceKey" />
- [x] 前端构建（NODE_OPTIONS=4096）+ 重启 8016
- [x] 浏览器实测：/questions 切年级、切小孩，列表与统计随之变化
- [x] 切年级不再跳回首页（handleGradeCommand 改为仅在选择页 push('/home')）
- [x] 实测：/questions 与 /stats 上切年级 URL 不变，日志出现 grade=3 / grade=6 的新请求
- [ ] 待用户确认：切换学科是否也改成留在当前页（现在仍会跳首页）
- [ ] 通知用户 Ctrl+F5 验证
