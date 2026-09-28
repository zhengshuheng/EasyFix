# REVIEW_FEEDBACK_UI — 新词学习复习三处修复（2026-09-28）

## 问题 1：做题自动带读泄题（读中文=报答案）

- **根因**：`Words.vue` watch(currentQuestion) 对新词学习题（is_new）故意 `noZh: false` 全量带读（题干→英语→中文→词根→例句→选项）。9/28 曾为"新词学习中文没声音"把 noZh 一刀切改 false，但"认一认：选出对应的中文意思"题的**正确答案就是中文意思**，带读中文=直接报答案；例句中文同理泄题。
- **修复**：`Words.vue:1332-1341` 改为 `noZh: true` 且**不自动读选项**（选项=答案集合，需要时点选项旁喇叭手动读）。做题时只读：题干 → 英语 → 例句英文。
- **注意**：autoTeach 已有 noZh 分支（不读 word.chinese / word_root / 例句中文），`opts.options` 朗读在 noZh 时仍会执行——调用处不传 options 即可。

## 问题 2：移动端「终止/提交」按钮换行挤一起

- **根因**：`.question-actions .el-button { font-size: 28px; padding: 25px 80px; }` 巨大按钮，375px 放不下 → 全局 `:has(> .el-button)` 兜底 flex-wrap → 换行挤。
- **修复**：`@media (max-width: 768px)` 内 `.question-actions` 显式 `display:flex; flex-wrap:nowrap; gap:12px`，按钮 `flex:1; font-size:16px; padding:12px 4px; margin:0` → 单行并排。

## 问题 3：移动端结果报告（review-result）变形

- **修复**：`@media (max-width: 768px)` 内：
  - `.result-header` 改纵向堆叠（正确率卡在上、统计卡在下），`.accuracy-big` 80px→44px；
  - `.stats-panel` 内边距/字号压缩；
  - `.error-word-item` 允许换行，`.wrong-side` 由右侧竖条改为**整行横条**（width:100%、border-top、横向 space-between）；
  - `.finish-btn` 40px。

## 验证

- `npm run build:trial` 通过；产物断言：Words-3b88b2fc.css 含 nowrap/新规则于 @media 块内，Words-a593f601.js 含 `noZh:!0`。
- 部署后真机验证：做题不再读中文/例句中文；按钮单行；报告页布局正常。

## 追加：终止/提交/下一个/关闭后旧词还在自动读（音频残留）

- **根因**：`autoTeach` 用 `teachToken` 中断循环、`autoPlayWithReplay` 用 `autoPlayToken` 中断重播，但 **submitAnswer / nextQuestion / finishReview / terminateReview 均未使 token 失效也没 stopSpeech**——提交/切题/结算时旧循环继续朗读，甚至与下一题自动播放交叉重叠；finishReview 原本只 `++autoPlayToken` 停重播，漏了 autoTeach 循环。
- **修复**：新增统一 `stopTeaching()`（`teachToken++ + autoPlayToken.value++ + stopSpeech()`），调用点：
  - submitAnswer（答题即停）、nextQuestion（切题即停）、terminateReview（终止即停）、finishReview（结算即停，替换原 autoPlayToken++）；
  - watch(reviewVisible) 关闭弹窗、startLearnPractice 学习→复习、watch(learnIndex) 学习卡切卡（先停旧卡再带读新卡）；
  - 新增 onBeforeUnmount 路由离开本页时停（弹窗开着切走路由不残留）。
- 产物：Words-4347bc87.js（build:trial 通过，源码 9 处 stopTeaching 已断言）。
