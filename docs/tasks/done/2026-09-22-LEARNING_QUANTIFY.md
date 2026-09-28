# LEARNING_QUANTIFY — 四组优化需求

目标：①错题来源展示 ②科目切换不跳首页 ③报告三优化 ④英语学习过程量化

## A. 错题来源字段（后端已落 source，只需前端展示）
- [x] 调研：ErrorQuestion.source 已存在（practice/assessment/upload/error_review/ai），list_questions 已返回 source（question.py:145）
- [x] A1: Questions.vue 错题列表加「来源」列（source→标签映射，宽 110，放难度前）

## B. 科目切换不刷新跳首页（App.vue）
- [x] B1: handleSubjectCommand 改为留当前页（仅 route.path==='/' 时进首页），spaceKey 触发重挂载
- [x] B2: openSubjectSpace(id) 改为：新学科不支持当前页面（英语专属页切数学）→ 跳该学科默认页；否则留当前页
- [x] B3: vite build 验证通过

## C. 报告优化（学习报告）
- [x] C1: App.vue 菜单「报告」去掉 v-if="subjectStore.isEnglish"（每个学科都有）
- [x] C2: LearningReports.vue 生成弹窗删除标题输入框（后端 _generate_title 已自动生成）
- [x] C3: LearningReports.vue 加载后：指定学科/年级且该空间无报告 → 自动生成一份并刷新（全科不自动；generateReport 支持 silent 参数）

## D. 英语学习过程量化（概览页 Home）
- [x] D1: stats.py WordStats schema 增加 dim_stats: [{key,label,done,total}]
- [x] D2: stats.py summary 计算 dim_stats（按小孩+学科+年级；五维映射：
        跟读=listen_correct>0、认读=recognize_correct>0、读词=speak_count>0、
        说词=speak_correct>0、听写=write_correct>0；total=当前空间单词总数）
- [x] D3: Home.vue 英语空间（showWordStats）加「单词学习进度」卡片（5 行 完成/总数 进度条）

## 收尾
- [x] 后端冒烟（stats summary dim_stats 真实数据：跟读0/认读1/读词28/说词1/听写1 per kid_id=3；旧接口不回归）
- [x] 修复 stats.py 循环变量覆盖参数 bug（by_subject 循环 subject_id → sid，导致 include_words 误判 False、dim_stats 恒空）
- [x] 修复 LearningReports.vue generateReport 重复声明（vite build 报错）
- [x] vite build 通过（29.2s）
- [x] docs/AI_CONTEXT.md 补充要点（循环变量覆盖坑 + 五维量化/来源列/科目切换/报告索引）
- [x] 临时脚本清理（tools/tmp/）
