# OpenSpec 执行规范（Agent 侧）

本文是编码 agent 的工程手册，与根目录 `AGENTS.md` 配合使用。

## 命令执行纪律（省 token，用户 9/25 确立）

- Windows 命令一律用 PowerShell：`execute_shell_command` 里以
  `powershell -NoProfile -Command "..."` 执行；含中文的脚本存 `.ps1`
  （UTF-8 with BOM）+ `[Console]::OutputEncoding = UTF8`，不要用 cmd.exe
  直接跑含中文的 .bat（GBK 解码乱码 → 反复转码浪费 token）。
- 中文名 .bat（如 `一键重启.bat`）由 ps1 用 `& '.\一键重启.bat'` 调用。
- E2E 启动一条命令：
  `powershell -NoProfile -ExecutionPolicy Bypass -File tools\e2e_ops_test.ps1`
  （重启 8012 服务 + 打开运营后台浏览器）。

## 何时使用

- **必须走 OpenSpec**：跨多文件的功能改造、UI 重构、新模块、涉及数据模型的变更。
- **可跳过**：单文件 bug 修复、一行配置改动、临时验证脚本（用 `docs/tasks/active/` 即可）。

## 执行纪律

1. **先 propose 再动代码**——用户要求"重新规划/改造"时，先写 `proposal.md` + `design.md` + `tasks.md` 并给用户确认，得到确认或用户已授权后再实现。
2. **保持变更聚焦**——一个 change 只做一件事；范围变大就开新 change。
3. **tasks 即进度**——每完成一项立即打勾，不批量补勾。
4. **验证后再归档**——apply 完成后跑真实验证（API / 浏览器 / 构建产物），把输出记录在 tasks 或 change 内；未验证不算完成。
5. **归档沉淀**——归档时把易返工点写进 `docs/AI_CONTEXT.md`。
6. **诚实**——失败、阻塞如实记录在 change 文档里，不编造验证结果。

## 变更模板

新变更从 `changes/_template/` 复制：`proposal.md`（动机/目标/范围/非目标/验收标准）+ `design.md`（方案/接口/数据）+ `tasks.md`（- [ ] 清单）。
