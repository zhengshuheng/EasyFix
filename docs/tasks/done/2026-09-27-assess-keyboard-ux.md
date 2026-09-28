# 做题环节键盘化 + 答对彩蛋（2026-09-27）

## 需求（用户四连）
1. 进入做题环节鼠标自动切换到输入框（自动聚焦）
2. 答题确认提交后答对可自动弹彩蛋
3. 选择题可通过方向键操作
4. 减少鼠标操作（小孩对鼠标不方便）

评测宪法对齐：彩蛋 = 答对即时正向反馈（提升积极性，非揠苗）；不干扰答题流程，可一键关闭。

## 改动（仅前端 `frontend/src/views/Assessment.vue`，后端零改动）
- **自动聚焦**：`startAssessment`/`next()` 后 `focusFillInput()`（nextTick → el-input focus）；选择题无输入框，由 `keyNavIdx=0` 默认高亮第一项承接键盘。
- **选择题方向键**：window `keydown` 监听（onMounted 注册 / onUnmounted 移除）：
  - ↑/← 上移、↓/→ 下移高亮（`keyNavIdx`，模环绕），未答且高亮≥0 时 Enter 提交 `pickChoice`；
  - 答完（full/wrong）Enter 直接 `next()`；
  - 填空 half 态输入框可编辑 → 原有 `@keyup.enter` 订正优先，window handler 跳过 half 防重复。
- **答对彩蛋**：`celebrate()` 生成 16 个 fixed 定位 emoji span（🎉⭐✨🌟💫🎊），CSS `confetti-fly` 动画随机飞散 1.3s 后自动移除；`pickChoice`/`pickFill`/`correctFill` 判 full 时触发。开关 `celebrateOn`（localStorage `easyfix_assess_celebrate` 持久化，默认开），答题顶部「🎉 特效开/关」按钮切换。
- 新增样式：`.quiz-option.key-nav-active`（蓝色高亮边框）、`.key-hint`（「⌨️ 方向键选答案，回车确认」提示）、`.confetti-emoji` + `@keyframes confetti-fly`。

## 端到端验证（浏览器真实操作，测试空间 d1SO5UQis99fhQ）
- 自动聚焦：数学/英语/1年级卷每题进入输入框均 `focused` ✓
- 填空键盘：fill `90-24-29=37` + Enter → ✅ 答对了 + confetti 16 ✓；答对后 Enter → 下一题 ✓
- 选择题键盘：↓↓ 高亮 A→C（`key-nav-active` 跟随）、Enter 提交判分 ❌/✅ 均正确 ✓
- 彩蛋开关：开→答对弹 16；关（按钮变「🎉 特效关」）→ 答对 confetti 0 ✓；答错不弹 ✓
- 组卷坑：`TYPE_ORDER` 里 application(1)/fill(2) 优先于 choice(3)，普通数学/英语卷 10 题几乎抽不到选择题 → 验证时对测试空间库 `UPDATE practice_question SET deleted=1 WHERE question_type!='choice'`（剩 89 条 choice）强制抽 choice；AI 每卷仍补 4 道 fill 变式排在前。

## 清理
- 测试空间 d1SO5UQis99fhQ：registry 行 + 主库账号 t_ak_92701 已删；db 文件被 8012 占用成孤儿（下次服务重启可删，无害）
- `tools/tmp/reset_test_pw.py`、`cleanup_keyboard_test.py`、reg.json/reg_out.json 已删（cleanup.py 顺带清）
- 构建产物：`npm run build` + `npm run build:trial` 均已更新（Assessment chunk 新 hash），8012 无需重启（后端零改动）
