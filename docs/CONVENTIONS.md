# 文档归档约定（DOCUMENT CONVENTIONS）

> 本文件是 EasyFix 项目**文档的唯一管理规范**。任何会话（Agent/Claude Code/人工）在开始任务前先读 `docs/README.md`（文档地图），结束时按本约定归档。

## 1. 目录结构

```
根目录（只允许 4 个常驻文件）
├── README.md          # 项目介绍（用户/访客入口）
├── AGENTS.md          # Agent 实操要点 + 本约定的入口
├── CLAUDE.md          # Claude Code 架构参考
├── CHANGELOG.md       # 版本变更记录
└── docs/              # 其余所有文档都在这下面
    ├── README.md      # 文档地图（索引，必须维护）
    ├── CONVENTIONS.md # 本约定
    ├── product/       # 产品级长期文档（路线图/方案）
    │   ├── PRODUCT_ROADMAP.md
    │   └── KP_PACKAGE_PLAN.md
    ├── tasks/         # 任务工作文档（会话产生）
    │   ├── README.md  # 任务索引（按状态分组）
    │   ├── active/    # 🔥 进行中任务（会话临时，gitignore）
    │   ├── done/      # ✅ 已完成归档（YYYY-MM-DD-{SLUG}.md，入库）
    │   └── planned/   # 📋 计划未开始（入库）
    ├── specs/         # 规格/开发说明（SPEC.md、DEVELOPMENT_PLAN.md 等既有文档）
    └── superpowers/   # 历史设计稿（保留不动）
```

## 2. 任务文档生命周期（所有会话必须遵守）

### 2.1 开始任务时

- 在 `docs/tasks/active/{SLUG}.md` 创建任务文档（**绝不**放在项目根目录）。
- 命名：`SLUG` 用大写蛇形、≤ 24 字符、概括任务意图（如 `PHONICS_MENU`、`DEPLOY_ALIYUN`）。
- 内容模板：

  ```markdown
  # {SLUG} — 一句话目标
  - [ ] 步骤 1
  - [ ] 步骤 2
  ...
  ```

- 每完成一步立刻勾选，不要批量勾。

### 2.2 任务进行中

- 文档留在 `docs/tasks/active/`，随时追加实际进展、决策、验证结果。
- 该目录已被 `.gitignore` 忽略，**不入库**（会话临时工作区）。

### 2.3 任务完成时（收尾动作，不可跳过）

1. 所有步骤勾选完毕，把结果、验证证据、遗留问题写进文档末尾。
2. **移动到归档区**：
   - 已完成 → `docs/tasks/done/{YYYY-MM-DD}-{SLUG}.md`（日期 = 归档当天）
   - 计划未开始 / 明确暂停 → `docs/tasks/planned/{SLUG}.md`
3. 更新 `docs/tasks/README.md` 索引（增/删对应行，保持三组清单准确）。
4. 归档后的文档**入库**（git add/commit），形成历史记录。

### 2.4 重新读取时

- 会话被压缩/跨会话：先读 `docs/README.md` 地图 → 需要任务细节时读 `docs/tasks/README.md` → 按索引读具体文档。
- 不凭记忆猜测任务状态，以 `docs/tasks/` 下文档为准。

## 3. 长期文档分类规则

| 文档类型 | 位置 | 入库 |
|---|---|---|
| 任务计划/执行记录（TODO） | `docs/tasks/{active,done,planned}/` | active 否，done/planned 是 |
| 产品路线图、功能方案 | `docs/product/` | 是 |
| 规格说明、开发计划 | `docs/` 根（现有）或 `docs/specs/` | 是 |
| 架构参考（给 AI 读） | 根目录 `AGENTS.md` / `CLAUDE.md` | 是 |
| 版本变更 | 根目录 `CHANGELOG.md` | 是 |
| 部署/运维说明 | `deploy/README.md`（随部署包） | 是 |

## 4. 临时文件约定（临时 ≠ 归档）

### 4.1 写入位置

| 文件类型 | 允许位置 | 说明 |
|---|---|---|
| 一次性脚本（探测/迁移/调试 `*.py`） | `tools/tmp/` | 有复用价值的工具脚本才留在 `tools/`（如 devserver.py、selftest_*、迁移脚本） |
| 测试产物（mp3/wav/png/zip/json） | `tools/tmp/` | 如 TTS 试听音频、OCR 截图 |
| 调试日志（非运行时的临时 log） | `tools/tmp/` | devserver 运行时日志仍写 `backend/devserver.log` |
| 浏览器截图（browser_screenshot_*.png） | `tools/tmp/` | 截图后立即移入或删除 |
| 后端运行数据（uploads/audio 等） | `backend/uploads/` | 运行期产物，gitignore，不入库 |

**禁止**：根目录散落 `tmp_*`、`_*`、`*.mp3`、`browser_screenshot_*.png`、调试 `.log`。

### 4.2 命名

`tools/tmp/` 内命名：`{用途}.{ext}`（小写 snake_case），如 `tts_test_ee.mp3`、`photo_ocr_debug.png`。

### 4.3 及时清理（会话收尾必做）

1. 会话结束时运行 `python tools/cleanup.py` 清空 `tools/tmp/`；
2. 或手动删除本次产生的临时文件；
3. 不在 `tools/tmp/` 之外遗留任何临时文件。

## 5. 红线

- 项目根目录**不再新增任何 .md**（README/AGENTS/CLAUDE/CHANGELOG 除外）。
- 任务文档一律进 `docs/tasks/`，不新建其他散落目录。
- 完成即归档，不允许 `active` 里堆积已结束的任务。
- 修改约定本身（本文件）需用户确认。

## 6. 检查清单（会话收尾自查）

- [ ] 本次任务文档在 `docs/tasks/active/`？
- [ ] 全部步骤勾选、结果与验证写入？
- [ ] 已移动到 `done/`（或 `planned/`）？
- [ ] `docs/tasks/README.md` 索引已更新？
- [ ] 根目录没有新冒出 .md 文件？
- [ ] `tools/tmp/` 已清理（`python tools/cleanup.py`）？根目录没有临时文件残留？
