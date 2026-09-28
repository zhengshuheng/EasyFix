# 2026-09-28 — MOBILE_UI_6FIX：移动端 6 处 UI 细节优化

## 需求（用户 9/28 反馈）
1. 错题页筛选条件占半屏
2. 练习页按钮第二行丑（去"练习集管理"标题，出题不换行）
3. 单词页"打印默写"第二行丑（去"单词本"标题、"打印默写"→"打印"）
4. 小孩切换单字换行丑
5. 官网单字换行丑、"退出登录"→"退出"
6. EasyFix logo 移动端隐藏（浏览器标题已清晰）

## 改动
| 位置 | 改动 |
|---|---|
| `frontend/src/views/Questions.vue` | 新增 `@media (max-width:768px)`：`.filters` 改 `flex nowrap + overflow-x:auto` 单行横滑（8 个控件固定宽 135~330px 堆叠占半屏 → 高度仅 1 行） |
| `frontend/src/views/PracticeSets.vue` | @media 块补：`.card-header > span:first-child { display:none }`（藏标题）+ `:deep(.header-actions .el-icon){display:none}`（藏图标）→ 去做题/线下做题·拍照交卷/批改/出题 4 按钮单行（302px < 355px） |
| `frontend/src/views/Words.vue` | 模板"打印默写"→"打印"；@media 块补：藏"单词本"标题 + `:deep(.review-buttons .el-icon){display:none}` → 5 按钮单行（294px < 355px） |
| `frontend/src/styles/mobile.css` | ① `.header-user > *` 由 `min-width:0; max-width:100%` 改为 `flex-shrink:0; min-width:max-content; max-width:max-content` + chips/site-link/logout-btn/name 全部 `white-space:nowrap`；② `.header-content .logo { display:none }` |
| `frontend/src/App.vue` | 头部退出按钮文案"退出登录"→"退出" |
| `frontend/src/views/SelectKid.vue` | 页面退出按钮文案"退出登录"→"退出"（一致） |

## 根因（#4/#5 单字换行）
mobile.css 旧规则 `.header-user > * { min-width: 0 }` 允许 chips 压缩 → flex 子项可缩就不触发容器 overflow-x，nowrap 失效 → 官网/小孩名/退出登录被压成逐字换行。改 `flex-shrink:0 + min-width:max-content` 后保持自然宽度，超宽时容器内横滑。

## 验证
- `npm run build:trial`（29.66s）+ `npm run build`（30.57s）均通过。
- 产物断言（python 脚本）确认：
  - `index-5628a789.css`：`.header-content .logo{display:none}` / `.header-user>*{flex-shrink:0;min-width:max-content;max-width:max-content}` / `.subject-chip,.user-chip,.site-link,.logout-btn,.subject-name,.user-name{white-space:nowrap}`（压缩器把两个规则合并为一个选择器列表）
  - `Questions-81e9f33a.css`：`.filters{...flex-wrap:nowrap;gap:8px;overflow-x:auto...}`
  - `PracticeSets-f02b960c.css` / `Words-3c9c2155.css`：`.card-header>span[data-v]:first-child{display:none}` + `[data-v] .header-actions/.review-buttons .el-icon{display:none}`
  - dist 全量无"退出登录"字符串；Words JS 按钮文案为"打印"

## 遗留
- 用户 deploy 后真机验证 6 处。
- 注意：桌面端"打印默写"按钮文案也简化为"打印"（全局模板改动）；标题"练习集管理/单词本"仅移动端隐藏，桌面保留。
