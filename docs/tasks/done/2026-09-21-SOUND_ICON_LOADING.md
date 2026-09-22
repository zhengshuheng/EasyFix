# SOUND_ICON_LOADING — 单词界面声音图标全部变 loading 的修复
- [x] 定位根因：Words.vue 全局 audioLoading 布尔导致所有图标一起 loading
- [x] Words.vue：改用按单词 id 隔离的 loading 状态（audioLoadingMap + isAudioLoading），更新所有模板绑定
- [x] WordLibrary.vue：补上缺失的 audioLoadingMap / isAudioLoading / playWordAudio 定义并更新模板绑定
- [x] 语法检查 / 构建验证（vite build 成功，2547 modules）
