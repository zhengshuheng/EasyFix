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

### 2.4 前端状态机（`frontend/src/views/Assessment.vue`）
- `answerState`：`'' | full | half | wrong`。half 时输入框可编辑 + 「📝 订正」按钮，订正成功补 0.5 分（补满）。
- **`answerLog` 每次 startAssessment 必须重置**（历史 bug：残留答案导致"一题未做也提交 0/10"记录）。

## 3. 高频坑（本仓库实测）

- **cmd.exe 多行 python -c 会被压成一行报 IndentationError** → 临时脚本写成 .py 文件跑。
- **TestClient 版本不兼容**（starlette/httpx 新版报 `Client.__init__() got an unexpected keyword 'app'`）→ 改用直接调用 router 函数传参冒烟，或起真实 uvicorn + curl。
- **冒烟/测试会在真实 SQLite 里创建 AssessmentRecord 等记录** → 测完按特征清理（写清理脚本），别污染用户历史。
- 改 Vue 模板后 `npm run build` 验证；Element Plus 组件在 scoped style 里覆盖内部样式需 `:deep()`。
- 浏览器截图：`browser.screenshot()` 存根目录 → **立即移入 `tools/tmp/`**（模型多数不支持读图，以 `snapshot()` 文本 + `bounding_box()` 验证为准）。

## 4. 判分/评测相关文档索引

| 想看什么 | 去哪里 |
|---|---|
| 数据隔离架构 + 路由模板 | `docs/ARCHITECTURE.md` |
| 判分三态/订正机制实现 | `app/routers/assessment.py` + `Assessment.vue` |
| 图示算式模板引擎 | `backend/app/services/pictorial_math.py`（如有） |
| 文档管理规则 | `docs/CONVENTIONS.md` |
| 本文件由谁维护 | 每次会话收尾把"新踩的坑/新规则"补进来 |
