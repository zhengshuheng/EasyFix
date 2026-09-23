# AI 工作上下文速查（AI_CONTEXT）

> 给模型看的"本仓库常识"：容易返工、踩坑、跨会话丢失的关键逻辑。
> 每次改 EasyFix 代码前先扫一遍本文件 + `../AGENTS.md`。架构细节看 `../ARCHITECTURE.md`。

## 0. 铁律（违反必返工）

- **根目录禁止新增任何 .md**（README/AGENTS/CLAUDE/CHANGELOG 除外）。任务文档 → `docs/tasks/active/`，完成 → `done/`（见 `CONVENTIONS.md`）。
- **临时脚本/截图/产物** → `tools/tmp/`，会话收尾跑 `python tools/cleanup.py` 清空。
- **禁止在请求体传 user_id**；孩子身份一律 `X-Kid-Id` 头（`app/utils/kid_context.py`）。查询必须 `deleted=False` 过滤（软删除）。
- **改表结构**：无迁移系统，SQLite 删 `backend/easyfix.db` 重建（**数据会丢**，谨慎）；MySQL 手动改表。

## 1. 运行环境（易错）

- 后端端口：`backend/.env` 里 `PORT=8012`（**不是 8000**）。启动：`cd backend && ..\.venv\Scripts\python.exe -m uvicorn app.main:app --port 8012`（用项目 `.venv`，系统 python 缺依赖）。
- 前端：`cd frontend && npm run build`（产物 dist/，由后端托管）。开发 dev server 走 5173。
- **SQLite 路径是相对 cwd 的**：跑后端脚本必须在 `backend/` 目录下执行，否则连到空库报 `no such table`。
- 数据库：`backend/easyfix.db`。表名：`practice_question`（345+ 题）、`assessment_record`、`user`（家长+小孩同表，role=child）、`knowledge_point` 等。

## 2. 评测（assessment）核心逻辑——改这里先读

### 2.1 判分（`app/routers/assessment.py`）
- `_normalize_answer`：去空白/全角/尾部量词/判断题符号归一（√/对→1，×/错→0）。
- `_grade_fill_answer`（填空/解答三态）：
  - **1.0** 数值结果对 + 单位齐（标准答案无单位时数值对即满分）
  - **0.5** 数值/算式对，但标准带单位而孩子缺单位或单位错（**打钩减半**，教学逻辑）
  - **0.0** 结果错
  - 数值判定 = 提取所有数字，**只看末位（结果）是否相等**——列式过程宽容（"8+8=15" 蒙对结果也给内容分）。
  - 单位提取 `_extract_unit`：优先括号内（本/个…），其次数字后 1~4 个汉字。
- choice：选项文本/字母归一比对；`数的分解` 题走 `_check_decompose`（任意两数之和=N）。

### 2.2 结算（submit）
- 前端 `buildFullAnswers()` **提交全卷所有题**，未答 `user_answer:''` → 判 0。
- `total = len(detail)` = 全卷题数 → **做 1 题退出就是 1/10**，不会虚高成优秀。
- `answers` 为空 → 400，不生成记录。中途退出（≥1 题已答）→ 照常提交结算保存。
- 报告 detail 逐题：stem/answer/user_answer/correct(0|0.5|1)/knowledge；前端 `Assessment.vue` 弹窗逐题回顾。

### 2.3 组卷（start）
- 按 `subject_id + grade` 抽题，`TYPE_ORDER` 应用题最优先，同知识点最多 2 题。
- **学科题型白名单 `_SUBJECT_ALLOW_TYPES`**：英语(2)/语文(3) **排除 application**（应用题是数学题型；历史教训：qid 72 英语卷混入 "I have three red apples" 数学题被用户投诉）。
- 低年级(1-2)数学先跑 `_ensure_pictorial_questions` 模板引擎补图示算式题；题库不足自动调 AI 补题（`_auto_refill`）。

### 2.4 评测集管理（2026-09 五需求）
- `assessment_record` 即评测集：`status` 三态 **in_progress/done/quit**；`questions` 列 = 题目快照 JSON（start 时写入）。
- **start 会建 in_progress 记录并返回 record_id**；同一孩子同学科同年级只留一条进行中（旧的自动置 quit）。前端必须把 record_id 带回 submit（`POST /assessment/{record_id}/submit`）；放弃时调 `POST /assessment/{record_id}/quit`。
- history 接口支持 `subject_id` 过滤（数学页不加载英语记录），返回 done+in_progress（未完成在前），quit 不显示。
- **评测排重 `RECENT_EXCLUDE_DAYS=7`**：start 组卷排除最近 7 天该孩子同学科同年级已完成评测用过的题（pool key 排最后兜底，题量不足自动放宽）。
- **错题同步 `_sync_error_questions`**：评测答错（correct<1）→ 进统一错题集（`source='assessment'`，复用 `upsert_error_question_from_practice_question` 幂等）；评测答对 → 该题 active 错题置 mastered（自动排除）。错题本查询只滤 deleted/status/source!='ai'，assessment 错题与练习错题同池可见。

### 2.5 前端状态机（`frontend/src/views/Assessment.vue`）
- `answerState`：`'' | full | half | wrong`。half 时输入框可编辑 + 「📝 订正」按钮，订正成功补 0.5 分（补满）。
- **`answerLog` 每次 startAssessment 必须重置**（历史 bug：残留答案导致"一题未做也提交 0/10"记录）。

### 2.6 评测需求优化（2026-09-23：难度分层 + 三档卷型 + 能力定位 + 报告Tab）
- **题库难度分层**：`practice_question.difficulty` 1-5（规则：题型基础分 + question_category 修正，见 `tools/tmp/backfill_difficulty.py`，已落库 418 题）。档位：basic=d1-2 / mid=d3 / hard=d4-5（`_difficulty_tier`）。
- **三档卷型 `paper_type`**（`AssessmentStartRequest` + start 组卷）：standard=40/40/20、challenge=20/50/30、explore=10/40/50（基础/中等/拓展）。组卷按难度分桶抽题，每桶内保持图题/情景/未考/题型优先级；题量不足时放宽补足（`quota` 尾差进基础档）。**坑：`_take` 闭包里 `pictorial_taken += 1` 必须 `nonlocal`，否则 UnboundLocalError**。
- **能力定位 `mastery`**（submit/detail 返回）：按难度维度统计 `tier_stats`（basic/mid/hard 正确率）+ 本年级内掌握等级（待巩固/基础掌握/掌握良好/学有余力，**不跨年级判级**）+ 强项(≥0.8)/弱项(<0.6)知识点 + 边界声明。前端报告弹窗三 Tab：能力定位/知识点(网格两列)/题目回顾，Tab 内容超长仅内部滚动（`.rp-tabs :deep(.el-tabs__content){max-height:56vh;overflow-y:auto}`）。
- 前端入口：hero 区卷型卡片（标准/拔高/拓展）→ `assessPayload` 带 `paper_type`；**题目数量选择器**（5/10/15/20 题，`questionCount` ref，默认10，`assessPayload` 带 `count`，后端 `req.count or ASSESS_QUESTION_COUNT`）。
- **AI 补题带难度+变式（任务D，2026-09-23）**：`_auto_refill(db, ..., difficulty=None)` 新增目标难度参数，start 缺题时按卷型传（标准=3/拔高=4/拓展=5，1-2年级自动降4）；LLM 每题输出 `difficulty` 1-5（prompt 难度标注段 + JSON 示例），`_auto_refill` 对漏标/越界难度做兜底夹取（1-2年级封顶4）。**DB 有 CHECK 约束 `check_pquestion_difficulty` 拒绝越界难度（1-5）**，漏夹时整题入库失败但不影响其他题。prompt 新增【变式要求】：同知识点多题情境/数据/问法各异，防雷同枯燥。

## 3. 高频坑（本仓库实测）

- **单词例句/学习模式（2026-09-23，WORD_LEARN_ENHANCE）**：`word.example_sentences` 列 = JSON `[{en,zh}]`，`_ensure_column` 迁移。AI 增强包含例句：`_enhance_words_llm`（新词完整生成含例句）/ `_fill_sentences_llm`（老词只补例句，**不覆盖已编辑字段**）；`_needs_enhance`=拼读+词根缺失，`_needs_sentences`=例句为空；`POST /words/enhance` 同时补增强+例句（limit≤50，20/次 LLM）。前端学习模式在 Words.vue `dimConfigForm.learnMode`（easy/standard/advanced，localStorage `easyfix_dims_{kid}`），例句数量按模式截断（easy=0/standard=1/advanced=2），进阶可关中文翻译（`showSentenceZh`）。**新词学习题（认一认选择题）例句只显示英文不显示中文——防止中文翻译泄露答案**。例句发音走浏览器 SpeechSynthesis en-US（`speakEn`），不走 TTS 文件缓存（`generate_word_audio` 用 `{text}.wav` 缓存，句子会污染 audio_dir）。存量老词无例句 → WordLibrary「记忆增强」tab 筛选批量补生成。

- **Python 循环变量覆盖函数参数**（stats.py 实测翻车）：`for subject_id, ... in subject_query:` 循环变量会**覆盖函数参数 subject_id**，后续 `is_english_subject(db, subject_id)` 拿到的是最后一个学科 id 而非参数值。凡参数名与循环变量同名必翻车——循环变量一律用 `sid` 等别名。
- **cmd.exe 多行 python -c 会被压成一行报 IndentationError** → 临时脚本写成 .py 文件跑。
- **TestClient 版本不兼容**（starlette/httpx 新版报 `Client.__init__() got an unexpected keyword 'app'`）→ 改用直接调用 router 函数传参冒烟，或起真实 uvicorn + curl。
- **冒烟/测试会在真实 SQLite 里创建 AssessmentRecord 等记录** → 测完按特征清理（写清理脚本），别污染用户历史。
- **评测空答案=孩子空卷提交**（Assessment.vue `buildFullAnswers` 未答题显式发 `user_answer=''`）——错题详情看到"未作答"是真实数据，不是接口 bug。**且 `_sync_error_questions` 会跳过 user_answer 为空的题**（评测未作答不入错题集，只有输入了答案且判错的才算错题）；存量清理：source='assessment' 且该题在所有评测 detail 中从未有过答案的错题已软删除（36 条，含原停车场题 id=24）。
- **错题详情作答历史**：`GET /api/questions/{id}/practice-history` 合并 练习(PracticeAttempt.student_answer) + 评测(AssessmentRecord.detail 按 source_practice_question_id 匹配) 两种来源，字段含 `student_answer/source(practice|assessment)/is_correct/date`；is_correct 为数值三态（1 正确 / 0.5 半对 / 0 错误，评测 correct 是 0~1 分数，不能 bool 化）；前端 Questions.vue「最近一次作答」+「作答历史」两块展示。
- **错题详情图例**：ErrorQuestion 无 visual 列；`GET /api/questions` 列表与 `/{id}` 详情通过 `_visual_map_for(db, eqs)` 取图例，**优先级：PracticeQuestion.visual（题库落库）→ 评测快照 AssessmentRecord.questions JSON 里该题的 scene（组卷时动态配的图）**——评测组卷会为普通应用题动态配 scene 但**不回写题库**（PracticeQuestion.visual 常为 None），必须用评测快照兜底；前端 Questions.vue 详情题目卡片用 `<SceneVisual :scene="currentQuestion.visual">` 渲染（与评测页同一组件）。
- 改 Vue 模板后 `npm run build` 验证；Element Plus 组件在 scoped style 里覆盖内部样式需 `:deep()`。
- 浏览器截图：`browser.screenshot()` 存根目录 → **立即移入 `tools/tmp/`**（模型多数不支持读图，以 `snapshot()` 文本 + `bounding_box()` 验证为准）。

## 4. 判分/评测相关文档索引

| 想看什么 | 去哪里 |
|---|---|
| **评测教育理念（产品宪法）+ 三档卷型/能力定位蓝图** | `docs/ASSESSMENT_DESIGN.md`（改评测相关代码必读） |
| 数据隔离架构 + 路由模板 | `docs/ARCHITECTURE.md` |
| 单词学习五维量化（概览页进度卡） | `stats.py` `dim_stats`（WordStats 字段）：跟读=listen_correct>0、认读=recognize_correct>0、读词=speak_count>0、说词=speak_correct>0、听写=write_correct>0；total=当前空间单词总数 |
| 错题来源列 | 后端 `ErrorQuestion.source`（practice/assessment/upload/error_review/ai）已在 list 返回，前端 `Questions.vue` 来源列映射 |
| 科目切换不跳首页 | `App.vue` `openSubjectSpace`/`handleSubjectCommand` 只切数据上下文（spaceKey 重挂载），英语专属页切非英语才跳 `/practice-sets` |
| 学习报告 | `learning_report.py` 标题自动生成；`LearningReports.vue` 无报告时自动生成一份（仅指定学科空间） |
| 判分三态/订正机制实现 | `app/routers/assessment.py` + `Assessment.vue` |
| 图示算式模板引擎 | `backend/app/services/pictorial_math.py`（如有） |
| 文档管理规则 | `docs/CONVENTIONS.md` |
| 本文件由谁维护 | 每次会话收尾把"新踩的坑/新规则"补进来 |
