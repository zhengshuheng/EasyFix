# 文库「生成短文后界面空白」修复（空间租户头 + 生成后展示）

- **日期**：2026-09-27
- **现象**：空间内「英语阅读 / 文库」→ 点「生成短文」→ 提示生成成功，列表仍显示「暂无短文 / 请在左侧选择一篇短文」，右侧一直空白。
- **状态**：已修复并验证（临时空间验证后已清理）

## 排查过程（先查证）

1. 后端日志：`POST /api/readings/generate` **201 Created**、随后 `GET /api/readings?...` 200 → 接口本身没报错。
2. 查库：空间库 `trial_data/tenants/SvXXG4zukMip0A.db` 只有 1 条模板短文（`grade=7`，2026-09-18），而**刚生成的 `Our School Life` 出现在主库 `easyfix_main.db`**（`created_at 2026-09-27 22:15`）。
3. 查前端：`frontend/src/views/Reading.vue` 全部请求用**裸 `axios`**，未走统一封装 `@/api/http`。

## 根因（三个叠加）

| # | 根因 | 后果 |
|---|---|---|
| 1 | `Reading.vue` 用裸 `axios`，只有 `@/api/http` 的实例才注入 `X-Trial-Key`（裸 axios 的全局拦截器只注入了 `X-Kid-Id`） | 读写请求全部落到**主库**：空间列表读主库（模板 grade=7 被当前年级过滤 → 空）、生成的短文写进主库 → 空间永远看不到 |
| 2 | `generateForm.grade` 硬编码 `7`，且 `onMounted` 只在 `grade == null` 时才跟随空间年级 | 生成 7 年级短文，列表按空间年级（1/2 年级）过滤 → 即使数据落对库也看不到 |
| 3 | `doGenerate` 把 `POST /readings/generate` 的响应**直接**赋给 `selectedPassage`，但该响应**不含 `questions` 关系**（未 `joinedload`，`return passage` 只序列化列） | 模板 `selectedPassage.questions.length` 抛 TypeError → 右侧卡片整块渲染失败 = 空白 |

附带：`createPracticeSet` 用 `window.location.href = '/reading-test/{id}'`（绝对路径，缺 `/{key}/` 前缀）→ 会跳出空间落到官网/404。

## 修复

- `frontend/src/api/http.js`：裸 axios 的全局请求拦截器补注入 `X-Trial-Key`（兜底修复 `ReadingTest.vue` / `Questions.vue` 等仍用裸 axios 的页面）。
- `frontend/src/views/Reading.vue`：
  - 5 处请求全部改走 `api`（`/readings`、`/readings/topics`、`/readings/{id}`、`/readings/generate`、`/practice-sets/generate-from-reading`），移除 `import axios`。
  - `generateForm.grade` 默认改 `null` → 跟随空间年级（`subjectStore.activeGrade ?? 3`，避免「全部年级」空间传空导致 422）。
  - `doGenerate`：生成成功后**同步筛选条件**为本次生成条件（否则新短文被现有 topic/grade/difficulty 筛掉），再用返回的 `id` 走 `selectPassage()` 拉详情展示。
  - 新增 `passageQuestions` computed（`selectedPassage?.questions || []`）+ 模板改用 `passageQuestions`，`contentParagraphs` 增加空值保护 → 缺字段不再白屏。
  - 创建练习集跳转改 `window.location.hash = '#/reading-test/{id}'`。

## 验证（临时空间 `16LiKitbTyRh_w` / `ui_reading_0927`，验证后已 DELETE 清理）

| 项 | 结果 |
|---|---|
| 复现原问题 | ✓ 新空间文库初始「暂无短文」（模板短文 grade=7 被当前 2 年级过滤） |
| 生成弹窗年级 | ✓ 显示「2年级」并禁用（原先硬编码 7 年级） |
| 生成后列表 | ✓ 出现新短文 `A Happy Day at School`（校园生活 / 2年级 / ⭐⭐⭐ / 186词），「暂无短文」消失 |
| 生成后右侧详情 | ✓ 自动展示正文 4 段 + 「选择题（共 4 题）」+ 选项（不再空白） |
| 数据落库（关键） | ✓ 新短文写入租户库 `16LiKitbTyRh_w.db`，主库 `easyfix_main.db` **无新增**（仍然是修复前那条误写数据） |
| 点击列表项 | ✓ 右侧正文 + 4 题正常渲染 |
| 清理 | ✓ registry 0 行、租户 db 文件不存在、`accounts` 0 行 |

## 遗留 / 建议

- 主库里有一条修复前误写的孤儿短文：`easyfix_main.db` → `reading_passage id=2 'Our School Life'`（2026-09-27 22:15，用户那次操作产生）。待用户决定删除或迁移进空间；不做未授权数据变更。
- `ReadingTest.vue`、`Questions.vue` 仍用裸 axios（已由 http.js 兜底注入租户头，功能正确）；建议后续统一迁移到 `api` 实例，避免再踩。

---

## 追加：点「创建练习集」提示创建失败（同日第二轮）

用户反馈：短文详情里点「创建练习集」→ 提示「创建失败」。

### 根因（两个独立缺陷）

1. **`POST /api/practice-sets/generate-from-reading` 漏写 `user_id`**
   日志：`sqlalchemy.exc.IntegrityError: NOT NULL constraint failed: practice_set.user_id`
   （参数 `user_id=None`）→ 500 → 前端「创建失败」。
   该项目里其它建卷接口（组卷 `:249`、AI 出题 `:507`、语法专项 `:1945`）都声明了
   `kid_id: Optional[int] = Depends(get_required_kid_id)` 并 `user_id=kid_id`，只有这个接口漏了。

2. **`GET /api/practice-sets/{id}` 响应漏 `passage_id`**
   `PracticeSetResponse` 有 `grammar_lesson_id` 却没有 `passage_id`，详情接口也不返回它 →
   `ReadingTest.vue` 的 `if (res.data.passage_id)` 永远为假 → 不拉短文和题目 →
   阅读理解测试页只显示标题 + 打印/返回按钮（正文、题目全空白）。

### 修复

- `backend/app/routers/practice_set.py:708`：`generate_practice_from_reading` 增加 `kid_id: Optional[int] = Depends(get_required_kid_id)`，建卷时 `user_id=kid_id`。
- `backend/app/routers/practice_set.py:738`：同样补 `user_id=kid_id`。
- `backend/app/routers/practice_set.py:1246`：详情响应增加 `"passage_id": ps.passage_id`；`PracticeSetResponse` 增加 `passage_id: Optional[int] = None`。
- 复查所有 `PracticeSet(` 构造点（`practice_set.py:321/631/736/854/2002`、`word.py:1332`）均有 `user_id`；仅 `services/init_demo_data.py:169` 没有（demo 初始化路径，非本次链路，未改动）。

### 验证（重启 8012 后；临时空间 `3-E2V_Ya9Aa_jA` / `ui_pset_0927`，验证后已 DELETE 清理）

| 项 | 结果 |
|---|---|
| 创建练习集 | ✓ 成功，自动跳到 `/{key}/#/reading-test/1`（空间前缀内，hash 跳转生效） |
| 阅读理解测试页 | ✓ 渲染短文正文 3 段 + 「选择题」4 题选项（修复前只有标题） |
| 做题交卷 | ✓ 显示「测试结果 正确：1/4（25%）」+ 逐题对错与解析 |
| 数据落库 | ✓ 练习集写入租户库（`practice_set.user_id` 非空） |
| 清理 | ✓ registry 0 行、租户 db 不存在、accounts 0 行、临时脚本已删 |

### 踩坑记录（验证方法）

`page.goto` 到**只有 hash 变化**的 URL 不会重新加载页面 → 看起来"改了没生效"。验证 SPA 页面要换 query（`?v=N`）强制重载。

