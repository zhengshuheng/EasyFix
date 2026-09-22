# TEXTBOOK_PHOTO — 拍照/自备PDF同步 + 入口配置 + 使用协议

- [x] 1. 拍照教材同步：POST /api/textbook/photo-import + 📷tab + 照片即用即删（用户自己设备仍有原照）
- [x] 2. 导入入口配置：textbook_import_config.json 四开关 + 后端 403 门禁
- [x] 3. 自备教材 PDF：POST /api/textbook/user-pdf-import，PDF 移入**本地教材库**保留（data/textbooks/自备教材/<科目>/<年级><册次>.pdf + OCR txt），重新导入覆盖+强制重OCR；仅清临时上传目录
- [x] 4. 前端：📄 tab + 协议勾选 + 文案「PDF 保存到本地教材库、仅限个人学习、不得传播」
- [x] 5. 使用协议（法律专业版·按用户立场定稿）：七章；不设「权利人救济配合」条款（单机本地工具无平台义务）；2.2 分路径陈述（本地/拍照/自备不主动获取；在线源来自第三方自评合法性）；新增 3.3 禁盗版文件+开发者可拒绝服务；5.1 明确不向第三方分发/共享/转让教材文件
- [x] 6. 构建 + 8016 自测：user-pdf-import → 教材库 PDF/txt 保留✅、upload_ 临时目录清理✅、DB 副本测试后已清理
- [ ] 7. 阻塞项（外部）：deepseek-flash 402 Insufficient Balance（key sk-6****003d），LLM 提取段需充值后端到端验证；代码无需改动
