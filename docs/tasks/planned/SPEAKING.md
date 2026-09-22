# SPEAKING — 口语模块（后端 STT + 后端 TTS，摆脱浏览器语音 API）
> 目标：一年级起步口语环节。MediaRecorder 录音上传 → 后端本地 STT 识别 → 跟标准句比对打分；发音走后端 TTS（可控），不依赖浏览器 SpeechSynthesis/SpeechRecognition。

- [ ] 环境探查：requirements.txt、Python 版本、网络可达性（hf 模型 / edge-tts）
- [ ] 安装依赖：faster-whisper（或 Vosk 兜底）+ edge-tts；下载英文 STT 模型
- [ ] 后端 speech 服务：sentence TTS（edge-tts 优先 / mimo 兜底）+ 本地 STT 识别
- [ ] 后端 speaking 路由：内容列表 / 录音提交打分 / 成绩入库（按小孩隔离，照 phonics.py 模式）
- [ ] 数据库模型 + 一年级种子口语内容（日常用语 ~50 句）
- [ ] 前端 Speaking.vue：听（后端音频）/ 录（MediaRecorder）/ 评分展示
- [ ] 前端入口 + 路由 + API 封装
- [ ] 构建前端 dist 并端到端验证（HTTP 局域网可用、授权不再依赖安全上下文）
