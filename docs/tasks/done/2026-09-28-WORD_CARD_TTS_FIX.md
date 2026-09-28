# WORD_CARD_TTS_FIX — 移动端单词卡片换行 + 自动带读例句中文翻译无声

> 远端 http://47.112.13.123:8012 部署后用户实测两个问题。

## 问题

1. 移动端单词卡片单词存在换行问题，样式需适配优化（`Words.vue` 学习模式卡片）
2. 开启自动带读例句后，新词学习时中文翻译没有声音

## 排查步骤

- [x] 定位问题 1：单词卡片样式（WordCard / 学习模式卡片），找换行根因 —— Words.vue 无任何 @media 移动端适配，review-dialog 固定 `--el-dialog-width:1200px`，窄屏溢出导致卡片错位换行
- [x] 定位问题 2：自动带读例句逻辑，中文翻译(zh)朗读链路 —— autoTeach 例句循环只 `speakEn(s.en)`，从未读 `s.zh`（最新 chunk 确认 `s.zh count: 0`）；9/28 已修 noZh 一刀切（单词中文有声），但例句中文翻译仍缺
- [x] 修复问题 1：Words.vue 加 `@media (max-width:768px)`：dialog 宽度 96vw + 学习卡/复习题/新词卡/默写卡内边距与字号适配 + 单词 flex-wrap/word-break
- [x] 修复问题 2：autoTeach 例句循环加 `!opts.noZh && s.zh && sentenceZhVisible()` 时 `speakZh(s.zh, {force:true})`
- [x] 本地构建 npm run build + build:trial 验证产物 —— dist-trial Words-ebc648ba.js 含例句中文朗读（`I(R.zh,{force:!0})`）、Words-947cd44f.css 含 `@media (max-width:768px)`；dist 同步构建 Words-394fb7b9.js
- [x] 本地/浏览器验证（桌面视口 + 学习卡正常；服务器 zh-CN TTS 200/11520B；无法模拟手机视口——SDK 无 viewport，移动端以代码+远端用户复验）
- [x] 本地测试数据清理（t_mob_0103/36UQew3CIVT2cQ 已删）
- [ ] **阻塞**：远端部署需要 SSH 私钥 `~/.ssh/id_rsa_ecs`，QwenPaw 安全策略拒绝 agent 访问私钥文件 → 需用户本机运行 `deploy.bat skipdb`
- [ ] 远端验证 http://47.112.13.123:8012（部署后用户手机实测 / agent 浏览器验证）

## 关键参照（AI_CONTEXT）

- 例句发音三级：SpeechSynthesis en-US → 服务器 `/api/words/audio?english=&lang=en-US|zh-CN`（edge-tts）
- Chrome UA 检测强制走服务器 TTS（`isChromeNoEdge`）
- 自动带读撞 Autoplay 5s 窗口 → `unlockAudioOnGesture` 解锁 + Web Audio 播放
- 新词学习题（认一认）例句只显示英文不显示中文（防泄露答案）——但自动带读场景中文翻译应有声？
