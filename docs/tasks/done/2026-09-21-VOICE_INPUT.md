# VOICE_INPUT — 学生做题界面无障碍优化（一年级友好）
- [x] 探查做题界面结构（PracticeSets.vue studentDoDialogVisible，每题 el-input 作答）
- [x] 语音读题：SpeechSynthesis 中文朗读题面+阅读题选项（🔊按钮，朗读中可点停止）
- [x] 软键盘：自定义屏幕键盘（数字/字母/符号/退格/清空），聚焦输入框自动弹出
- [x] 语音输入答案：SpeechRecognition zh-CN + 中文数字自动转阿拉伯（🎤按钮，不支持/网络失败优雅降级提示）
- [x] 构建 + 浏览器验证（软键盘输入/退格/清空实测通过；读题/语音按钮渲染与降级验证）

