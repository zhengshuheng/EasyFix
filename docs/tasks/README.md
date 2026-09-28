# 任务文档索引

> 任务工作文档统一归档于此。规则见 `../CONVENTIONS.md`。
> 新任务 → `active/`；完成 → 移入 `done/`；计划/暂停 → `planned/`。每完成一项任务后必须更新本索引。

## 🔥 进行中（active/）

_（当前为空。进行中的任务文档在 `active/` 下，不入库。）_

## ✅ 已完成（done/，77 项）

| 任务 | 文档 |
|---|---|
| 语法学习自动带读+手动语音：教程页导航条自动带读开关(localStorage easyfix_grammar_auto_read 默认开)、骨架导读(标题→总结→节标题→口诀)、标题/总结/每节/易错点/口诀 🔊 手动朗读(例句原有)、切课/卸载 token 中断停音频 | `done/2026-09-28-GRAMMAR_AUTOREAD.md` |
| 新词学习复习三处修复：做题带读不再读中文/例句中文/选项（noZh:true，原 9/28 误改 false 泄题）、移动端终止/提交按钮单行并排、结果报告窄屏纵向堆叠+错词条整行化 | `done/2026-09-28-REVIEW_FEEDBACK_UI.md` |
| 移动端筛选单行+练习窄屏+报告沉淀：单词/语法 filters 单行横滑、日期弹层 94vw 收窄、PracticeSets 操作列移动端收敛为下拉(400px fixed 挤没数据列)、报告列表按 kid 隔离+grade 过滤+生成后 unshift 沉淀兜底 | `done/2026-09-28-MOBILE_UI_5FIX.md` |
| 移动端 6 处 UI 优化：错题筛选单行横滑(不再半屏)/练习页去标题+藏图标按钮单行/单词页去标题+「打印默写」简化「打印」+藏图标单行/头部 chips 逐字换行根因(header-user min-width:0 改 max-content+nowrap)/「退出登录」→「退出」/logo 移动端隐藏 | `done/2026-09-28-MOBILE_UI_6FIX.md` |
| 家长中心账号管理：仅主账号可删除账号/小孩（辅助家长 403 + 前端删除按钮禁用，is_owner 收口） | `done/2026-09-28-PARENT_OWNER_DELETE.md` |
| 辅助账号进家长中心密码锁卡死修复：ParentLockDialog 原生 fetch `/api/auth/me` 缺 X-Trial-Key → 落主库 id 错位（child 顶替 admin 候选）→ 辅助密码全败；补租户头后端到端验证通过（部署 f9dafad） | `done/2026-09-28-HELPER_PARENT_LOCK.md` |
| 远端移动端两个问题修复：①单词卡片换行——Words.vue 补全站唯一缺失的移动端适配（@media 768：review-dialog 96vw/字号缩放/单词 flex-wrap+word-break）；②自动带读例句中文翻译无声——autoTeach 例句循环补 `speakZh(s.zh,{force:true})`（noZh 复习题/隐藏翻译时不读） | `done/2026-09-28-WORD_CARD_TTS_FIX.md` |
| 一键部署增加 ops 权威数据同步：tools/deploy_export_ops.py 导出主库配置表(语法教程/激励/成就) → deploy/ops_data.sql，remote_deploy.sh 容器内幂等 upsert 云端主库（不覆盖空间/用户数据），deploy.ps1 加 [1.5/5] 导出步骤（保持 BOM） | `done/2026-09-27-deploy-ops-sync.md` |
| 家长端知识点过滤条件与运营平台对齐：过滤栏 7 组收敛为 5 组（学科/版本/年级/册次/搜索，删 标签/要求/类型），年级收敛为小学 1-6，版本默认选中教材（修复 synced 为空无默认），新增名称/章节搜索 | `done/2026-09-27-kp-filter-align.md` |
| 语法教程运营化：主库 ops 权威 + 建空间自动同步 + 更新逻辑（sync-tutorials / sync-tenants）+ 家长端固化只读（403），修复模板/存量空间教程缺失；**追加教程版面优化**：正文按 `##` 分节卡片 + 可折叠 + 本课目录锚点 + 上/下一个语法点 | `done/2026-09-27-GRAMMAR_OPS_TUTORIAL.md` |
| 文库「生成短文后界面空白」修复：Reading.vue 裸 axios 缺 X-Trial-Key 导致读写落主库 + 生成年级硬编码 7 + generate 响应不含 questions 致右侧白屏；全部改走 `api`、年级跟随空间、生成后同步筛选并拉详情展示；**追加第二轮**：「创建练习集」500（practice_set.user_id NOT NULL）+ 详情响应漏 passage_id 致阅读理解测试页空白 | `done/2026-09-27-READING_TENANT_FIX.md` |
| 做题环节键盘化：自动聚焦输入框 + 选择题方向键 + 答完回车下一题 + 答对彩蛋（可开关） | `done/2026-09-27-assess-keyboard-ux.md` |
| 出题规则集成运营中心：ops_prompt_rule 表 + 运营后台「出题规则」页 + llm/question_prompts 读配置（改规则不用改代码） | `done/2026-09-27-prompt-rules-ops.md` |
| 评测举一反三出题：库存只作参考+每次生成新变式+题干排重+错题知识点加权（9卷连续切卷0重叠） | `done/2026-09-27-assessment-variant.md` |
| 密码重置（easyfix_demo）+ 练习端浏览器验证：修复 watch 未 import 白屏 + 练习集详情返回 grade 低年级判定 | `done/2026-09-26-password-reset-practice-verify.md` |
| 大陆义务教育教材版本全量登记（数学12/语文10/英语15，共37个版本） | `done/2026-09-26-mandatory-editions.md` |
| 运营后台体验账号管理：列表/延长体验/删除账号（含 delete_space 句柄修复） | `done/2026-09-26-trial-account-mgmt.md` |
| AI 模型市场 ↔ 学生端 LLM/OCR 联动测试 + deepseek 配置迁移到模型市场 | `done/2026-09-26-ai-market-link.md` |
| 教材版本独立菜单：知识点/单词统一版本库 + 未登记版本一键登记/删除 | `done/2026-09-26-editions-menu.md` |
| 教材识别策略升级：多模态优先+目录定位+ocr_mode识别方式字段 | `done/2026-09-26-textbook-ocr-strategy.md` |
| 知识点导入优化：智能导入自动决策 + 来源标记 + 按单元分组保序 | `done/2026-09-25-kp-import-optimize.md` |
| 运营后台改造：账号+口令登录、后台布局导航、数据列表、敏感文案移除 | `done/2026-09-24-OPS_ADMIN_UI.md` |
| 架构统一：注册即建空间 + 正式数据收编 easyfix_demo + 移除 /app | `done/2026-09-24-EASYFIX_DEMO.md` |
| 定位检索省 token：file_map 结构地图 + AGENTS.md 定位 SOP | `done/2026-09-24-SEARCH_OPTIMIZE.md` |
| 模块体积上限约束（AGENTS.md 代码规范） | `done/2026-09-24-MODULE_SIZE_LIMIT.md` |
| 搜索纪律（AGENTS.md 省 token 扫描约束） | `done/2026-09-24-SEARCH_DISCIPLINE.md` |
| 学生端删除家长认证（单词/练习/错题/报告/阅读） | `done/2026-09-23-PARENT_GUARD_DELETE.md` |
| 单词学习优化（例句融入 + 拼读带读 + 学习模式） | `done/2026-09-23-WORD_LEARN_ENHANCE.md` |
| 评测分小孩 + 数据隔离架构文档 | `done/2026-09-22-KID_ISOLATION_ARCH.md` |
| 低年级图示算式模板引擎（1-2年级数学） | `done/2026-09-22-PICTORIAL_MATH_ENGINE.md` |
| 评测自动补题 | `done/2026-09-22-ASSESS_AUTO_REFILL.md` |
| 评测填空交互（提交答案按钮） | `done/2026-09-22-ASSESS_FILL_UI.md` |
| 评测判分修复（归一化/三态） | `done/2026-09-22-ASSESS_GRADE_FIX.md` |
| 评测配图场景（count-split 图例） | `done/2026-09-22-ASSESS_SCENE.md` |
| 缺单位半对判分 + 订正机制 | `done/2026-09-22-HALF_CREDIT.md` |
| 语法管理隐藏管理入口 | `done/2026-09-22-HIDE_GRAMMAR_MGMT.md` |
| 菜单顺序调整 | `done/2026-09-22-MENU_ORDER.md` |
| 语法 UI 优化 | `done/2026-09-22-OPTIMIZE_GRAMMAR_UI.md` |
| 拼读 tab 重构 + 练习区大气化 | `done/2026-09-22-OPTIMIZE_PHONICS_TAB.md` |
| 拼读 UI 优化 | `done/2026-09-22-OPTIMIZE_PHONICS_UI.md` |
| 拼读词库扩容咨询 | `done/2026-09-22-PHONICS_LEXICON.md` |
| 拼读练习 | `done/2026-09-22-PHONICS_PRACTICE.md` |
| 图例引擎修复 + 乘法图误配 | `done/2026-09-22-SCENE_GOVERN.md` |
| AI 出题年级纠偏 | `done/2026-09-21-AI_GRADE_GEN.md` |
| AI 知识点导入 | `done/2026-09-21-AI_KP_IMPORT.md` |
| AI 练习题来源隔离 | `done/2026-09-21-AI_QUIZ_SOURCE.md` |
| AI 单词智能导入 | `done/2026-09-21-AI_WORD_IMPORT.md` |
| 选择题题型纠偏 | `done/2026-09-21-CHOICE_TYPE.md` |
| 今日任务（四维记忆） | `done/2026-09-21-DAILY_TASK.md` |
| 详情页卷子化 | `done/2026-09-21-DETAIL_UI.md` |
| 删除错题本管理 tab | `done/2026-09-21-DROP_ERRORBOOK_TAB.md` |
| README 撰写 | `done/2026-09-21-EASYFIX_README.md` |
| 角色系统 | `done/2026-09-21-EASYFIX_ROLES.md` |
| 一键启动 | `done/2026-09-21-EASYFIX_START.md` |
| 入学年级 | `done/2026-09-21-ENROLLMENT_GRADE.md` |
| 错题本按小孩隔离 | `done/2026-09-21-ERRORBOOK_ISOLATION.md` |
| 修复启动 bug | `done/2026-09-21-FIX_STARTUP.md` |
| git 分支方案 | `done/2026-09-21-GIT_DEV_BRANCH.md` |
| 年级隔离 | `done/2026-09-21-GRADE_ISOLATION.md` |
| 语法专项 P1 | `done/2026-09-21-GRAMMAR_P1.md` |
| 激励中心完整化 | `done/2026-09-21-INCENTIVE_COMPLETE.md` |
| 全链路按小孩隔离 | `done/2026-09-21-KID_ISOLATION.md` |
| 小孩教材绑定 | `done/2026-09-21-KID_TEXTBOOK_BIND.md` |
| 知识点系统 | `done/2026-09-21-KP_SYSTEM.md` |
| 本地时间修复 | `done/2026-09-21-LOCAL_TIME.md` |
| 卷名/分数参数化 | `done/2026-09-21-PAPER_TITLE_SCORE.md` |
| 家长中心优化 | `done/2026-09-21-PARENT_CENTER_OPT.md` |
| 自然拼读+联想记忆 | `done/2026-09-21-PHONICS_MEMORY_COMPLETE.md` |
| 低年级拼音辅助 | `done/2026-09-21-PINYIN_ASSIST.md` |
| 出题入口迁移 | `done/2026-09-21-PRACTICE_REFLOW.md` |
| AI 出题维度 | `done/2026-09-21-QUESTION_GEN.md` |
| 喇叭加载状态 | `done/2026-09-21-SOUND_ICON_LOADING.md` |
| 学科统计隔离 | `done/2026-09-21-SUBJECT_ISOLATION.md` |
| 学科空间 A/B 方案 | `done/2026-09-21-SUBJECT_SPACE_A.md` |
| 学科内部 tab | `done/2026-09-21-SUBJECT_TABS.md` |
| 切换不刷新修复 | `done/2026-09-21-SWITCH_REFRESH.md` |
| 教材同步导入 | `done/2026-09-21-TEXTBOOK_IMPORT.md` |
| 教材路径约定 | `done/2026-09-21-TEXTBOOK_PATH.md` |
| 教材拍照导入 | `done/2026-09-21-TEXTBOOK_PHOTO.md` |
| 语音输入+软键盘 | `done/2026-09-21-VOICE_INPUT.md` |
| 教材提取单词 | `done/2026-09-21-WORDS_TEXTBOOK_EXTRACT.md` |
| 单词库过滤条 | `done/2026-09-21-WORD_FILTER.md` |
| 单词库独立页 | `done/2026-09-21-WORD_LIBRARY_MOVE.md` |
| 单词记忆 P2 | `done/2026-09-21-WORD_P2.md` |
| 单词按小孩隔离 | `done/2026-09-21-WORD_PER_KID.md` |
| 单词单元导入 | `done/2026-09-21-WORD_UNIT_IMPORT.md` |
| 记忆增强自动附带 | `done/2026-09-21-WORD_AUTO_ENHANCE.md` |
| 错题来源+科目切换+报告优化+单词五维量化 | `done/2026-09-22-LEARNING_QUANTIFY.md` |

## 📋 计划 / 待做（planned/）

| 任务 | 文档 |
|---|---|
| 拍照自动交卷（线下卷拍照识别批改） | `planned/PHOTO_SUBMIT.md` |
| 口语评测（STT/edge-tts） | `planned/SPEAKING.md` |
