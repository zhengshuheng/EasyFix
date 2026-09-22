# PHOTO_SUBMIT — 线下做题拍照上传 → 自动识别 → 自动交卷

目标：学生线下在打印出来的卷子上作答，家长/学生拍照上传，系统自动识别手写作答、
自动批改并交卷（正确率入库、错题自动进错题库），无需在线逐题输入。

## 方案（复用既有链路，最小新增）
- 已有：`POST /api/practice-sets/{id}/submit-answers`（写作答）、`/ai-grade`（LLM 批改）、
  `/mark-reviewed`（落库判错 + 派生错题 + 积分）。
- 新增：`/recognize-paper`（多模态 OCR 手写作答 → 按题号映射）+ `/photo-submit`
  （写作答 → LLM 批改 → 落库，一步到位）。
- 关键点：打印卷的题号顺序 = 按题型分组（选择→填空→判断→计算→应用→操作→阅读→写作），
  与 DB 顺序不同，必须复现 PDF 的分组顺序做「题号 → question_id」映射。

## 步骤
- [x] 1. 本 TODO + .gitignore（`*_TODO.md` 已在 .gitignore:33）
- [x] 2. multimodal_ocr.recognize 支持自定义 prompt（新增 DEFAULT_OCR_PROMPT）
- [x] 3. services/paper_ocr.py：题号顺序复现 + 结构化 prompt + JSON 解析 + 多图合并
- [x] 4. routers/practice_set.py：抽出 save_student_answers / apply_question_results；
      新增 /recognize-paper、/photo-submit；顺修 db.flush 重复作答 bug
- [x] 5. frontend/src/api/question.js：recognizePaperAnswers / submitPaperPhotos
- [x] 6. PracticeSets.vue：📷 拍照交卷弹窗（上传 → 核对 → 结果三步）+ 入口按钮
- [x] 7. 重建前端（PracticeSets-75909966.js / index-088e47c8.js）
- [x] 8. 端到端验证（沙盒 8017 + 数据库副本）：识别 6 题命中 5，交卷批改 6/6，
      6 条错题入库，attempts.graded_by=ai；真实库 easyfix.db 未被写入
- [x] 9. 题号顺序与真实 PDF 对齐校验（练习集 #9：1..6 题号位置单调递增、全部命中）

## 顺带修掉的既有 bug
- `services/llm.py::_parse_grading_response`：模型按提示词返回的是「第 1..N 题」位置序号，
  原先直接当真实题号用 → 「家长 AI 一键批改」的结果全部匹配不上题目（静默失效）。
  现已映射回真实题号（并保留位置兜底）。

## 追加需求：直接调用摄像头（本轮完成）
- [x] 弹窗「步骤一」新增两个入口：`用电脑摄像头拍摄`（getUserMedia + 连拍，canvas→JPEG，长边≤2000）
      与 `📱 手机 / 平板拍照`（`<input capture="environment">`，不需要 HTTPS），
      拍到的照片与上传的照片合并成同一批送识别。
- [x] 摄像头窗口：实时预览、`📸 拍这一页` 连拍、缩略图可删、关闭自动停流（释放摄像头灯）。
- [x] 失败降级：无摄像头/被拒绝/非安全上下文 → 友好提示并引导改用手机拍照或选照片。
      实测（自动化浏览器无摄像头）：正确显示「没有检测到可用摄像头」，「拍这一页」置灰。
- [x] 后端补两个手机照片的坑 `paper_ocr.normalize_image()`：EXIF 方向摆正 + 长边压到 2000。
      实测：4032×2851、EXIF Orientation=6 的竖拍照片 → 规范化后 1414×2000 方向正确，
      OCR 结果与原始图一致；该照片走真实 HTTP 接口 → 识别 5/6 题、交卷批改 6/6。

## 未验证 / 待用户确认
- 浏览器 SDK 无文件上传、无 JS 执行能力，「选照片」这一步无法由 Agent 驱动：
  需要用户在 8010 上手动点一次「线下做题·拍照交卷」→ 选卷子 → 拍照/选照片 → 识别并自动交卷。
- **摄像头成功路径（真实取景→拍摄→识别）本机无法验证**：自动化环境的浏览器没有摄像头设备，
  只验证到「无摄像头」的降级分支；`captureShot()` 的 canvas→JPEG→File→上传 是标准 API，
  需用户在有摄像头的笔记本上实测一次。
- 手写识别质量只用「打印卷 + 手写体合成」验证过，真实照片/真实字迹需用户实测。
- 计算/应用等主观题由 LLM 看「孩子写的算式」判对错并给评语；纯图片题不支持自动批改。
- 摄像头需页面为 `http://localhost` / `https`；若用手机通过局域网 IP 访问，
  浏览器会禁用 getUserMedia，请走「📱 手机 / 平板拍照」（file input 不受此限制）。
