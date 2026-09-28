# GRAMMAR_AUTOREAD — 语法学习自动带读 + 手动语音（2026-09-28）

## 需求

语法教程"看不进去"：提供 ①自动带读（带设置开关）②手动语音按钮，用"听"带动"看"。

## 实现（Grammar.vue，最小可用）

**自动带读（骨架导读，避免长文通读冗长）**
- 设置开关：教程页导航条右侧 `自动带读` el-switch，绑定 `grammarAutoRead`（localStorage key `easyfix_grammar_auto_read`，默认开）。
- 朗读顺序：标题 → 一句话总结 → 各节标题 → 记忆口诀；每节全文由节内 🔊 手动朗读。
- 触发：fetchLesson / switchLesson 加载成功后 `autoTeachLesson()`；token 中断式循环（grammarTeachToken），切课/关页面/手动朗读都会先失效旧循环再播新内容。
- 停止：onUnmounted `stopGrammarTeach()`（离开语法页不残留，沿用 3.10 铁律）。

**手动语音按钮（speakZh 中文为主；例句保持 speakSequence 英→中）**
- 标题旁 🔊、总结旁 🔊、每节（block-head）🔊（读"节标题。正文全文"，@click.stop 防折叠冒泡）、易错点整块 🔊（join('。')）、口诀 🔊。
- 例句区原本已有 speakExample 按钮，未动。

## 验证

- `npm run build:trial` 通过；产物断言：Grammar-ca4d2a40.js 含 `easyfix_grammar_auto_read`，Grammar-1a3b009e.css 含 .speak-btn / .auto-read-toggle / .lesson-title-row。
- 部署后真机验证：进入语法点自动读骨架；各节 🔊 手动朗读全文；开关关掉后进课不自动读。
