# EasyFix 知识点包化实施计划

> 更新：2026-09-20
> 一句话：**教材知识点「打包分发 + 按需下载」，自定义知识点「本地维护」；版本绑定在小孩身上，共享库全家一份。**
> 现状：没有现成知识点包——现在是「下载教材 PDF → 本地 OCR → LLM 按单元提取」（`TextbookImport.vue` 链路），每个家庭每次现场花 token + 等待。
> 目标：常见版本开发期打包一次 → 分发 0 token 下载；冷门/特殊版本运行时 AI 提取兜底（每家庭几毛钱）。

---

## 0. 总体模型

```
① 共享库（全家一份）
   knowledge_point 表：教材知识点（source='textbook'，带 edition_key）+ 自定义知识点（source='custom'）

② 小孩绑定（新增 kid_textbook 偏好表）
   建小孩/账号管理：按学科选教材版本（地区推荐可改）→ 只记偏好，不复制数据

③ 自动下载（主路径，覆盖 90%）
   保存偏好 → 检查共享库该版本是否存在 → 没有 → 下载整版包（0 token）→ 导入

④ 手动兜底（3 个现有入口改造，预填小孩偏好）
   AI 生成 / 教材同步导入 / K12 导入：冷门版本、本地教材、补充单元

⑤ 出题/列表过滤
   WHERE subject_id=? AND grade=? AND semester=? AND (source='custom' OR edition_key IS NULL OR edition_key=小孩偏好)

⑥ 更新
   家长中心「检查知识点更新」→ kp-index.json 出新修订 → 按 edition_key 全量替换 → 全体小孩生效
```

**数据分层**：知识点本体共享（全家一份）；教材版本偏好、学习进度按小孩隔离。与单词本体共享、进度按小孩的既定规则一致。

---

## 1. 数据模型变更

### 1.1 `knowledge_point` 表新增列

沿用 `ensure_kp_dimension_columns()`（`backend/app/models/knowledge_point.py:14`）的幂等补列模式，扩展新函数（如 `ensure_kp_package_columns()`）：

| 列 | 类型 | 说明 |
|---|---|---|
| `source` | VARCHAR(20) DEFAULT 'custom' | `textbook`（教材内置，只读）/ `custom`（用户自定义） |
| `edition_key` | VARCHAR(50) NULL | 教材身份（如 `math-rj-2022`）；`textbook` 必填，`custom` 为空；**NULL 表示通用教材数据（旧 K12 导入，任何版本可见）** |
| `revision` | VARCHAR(20) NULL | 数据修订号（如 `v2026.1`）；`textbook` 用 |

索引：`edition_key`（更新时定位整版替换）。`version` 列保留作为显示名（如「人教版数学（2022课标版）」）。

### 1.2 新建 `kid_textbook` 表（小孩教材偏好）

| 列 | 类型 | 说明 |
|---|---|---|
| `id` | Integer PK | |
| `kid_id` | FK users.id | 小孩 |
| `subject_id` | FK subject.id | 学科 |
| `edition_key` | VARCHAR(50) | 教材身份 |
| `version_name` | VARCHAR(100) | 显示名冗余 |
| `source` | VARCHAR(20) | `package`（下载包）/ `local`（本地 AI 提取兜底） |
| `created_at` / `updated_at` | DateTime | |

UNIQUE `(kid_id, subject_id)`——每小孩每学科一个版本偏好。

---

## 2. 知识点包格式与打包脚本

### 2.1 包格式

文件：`kp-<edition_key>-<revision>.json.gz`（几百 KB~1 MB/套，含 1-6 年级全部）

```json
{
  "edition_key": "math-rj-2022",
  "subject": "数学",
  "version_name": "人教版数学（2022课标版）",
  "revision": "v2026.1",
  "grades": [1,2,3,4,5,6],
  "points": [
    {
      "name": "认识秒",
      "grade": 3, "semester": 1,
      "chapter": "第一单元 时、分、秒",
      "description": "知道秒是比分更小的时间单位，会认秒针",
      "requirement": "理解",
      "tags": ["重点"],
      "kp_type": "数与代数"
    }
  ]
}
```

### 2.2 打包脚本 `backend/tools/build_kp_packages.py`（开发期一次性工具）

**模式 A：K12 数据集 → 包**（复用 `backend/app/services/k12_import.py`）
- 第一步**先调研** `backend/data/k12/index.json` 真实结构，确认 347 本教材能否按「教材版本」归类（关键风险点，见 §10）；
- 若能归类：读 split 数据 → 学科映射（复用 `subject_aliases`）→ LLM 分配年级学期（复用 `assign_grades_llm`，thinking disabled）→ 按 edition_key 聚合 → 输出包；
- 若不能归类：退化为**通用整包**（`edition_key` 为空，如 `kp-数学-通用`），出题时任何版本都可见（§7 的 NULL 过滤分支）。

**模式 B：新教材 OCR+LLM → 包**（2022 课标新教材，K12 没有的）
- 复用 `backend/app/services/textbook_service.py`：`get_index()` 找书 → `download_book()` 下载 PDF → RapidOCR 本地识别；
- 复用 `backend/app/routers/knowledge_point.py:330` `ai-generate` 的 prompt/解析逻辑，改成批量落盘（每单元一章，chapter/description/requirement/tags/kp_type 齐全）；
- 输出同一格式包 → 同目录。

**输出**：`backend/data/kp_packages/*.json.gz` + 生成 `kp-index.json`：

```json
{
  "edition_key": {
    "subject": "数学",
    "version_name": "人教版数学（2022课标版）",
    "revision": "v2026.1",
    "url": "https://github.com/<user>/EasyFix/releases/download/kp-v2026.1/kp-math-rj-2022-v2026.1.json.gz",
    "sha256": "...",
    "size": 483210,
    "grades": [1,2,3,4,5,6]
  }
}
```

**分发**：GitHub Releases（每个 revision 一个 tag，如 `kp-v2026.1`）；国内访问走 ghproxy 镜像（沿用 `k12_import._download()` 多源容错模式）。

---

## 3. 运行期下载/导入/更新服务

新文件 `backend/app/services/kp_package.py`：

| 函数 | 职责 |
|---|---|
| `download_package(edition_key)` | 拉 `kp-index.json`（进程缓存）→ 找 URL → 多源下载（GitHub → ghproxy）→ 校验 sha256 → 返回本地路径；失败返回错误（**不导入，库保持原状**） |
| `import_package(pkg)` | 事务：删该 `edition_key` 全部 `source='textbook'` 旧行 → 批量插入新行（幂等，重复执行行数恒定） |
| `ensure_edition(edition_key)` | `COUNT(knowledge_point WHERE edition_key=? AND source='textbook')` = 0 → 下载+导入；>0 → 直接返回（已就绪） |
| `check_updates()` | 比对本地 `revision` vs `kp-index.json` 的 `revision` → 返回可更新列表 |
| `apply_update(edition_key)` | 下载新版 → `import_package` 全量替换 |

新路由 `backend/app/routers/kp_package.py`（注册进 `main.py`，`dependencies=[Depends(require_admin)]`）：

| 接口 | 用途 |
|---|---|
| `GET /api/knowledge-points/packages` | 版本包目录 + 本地已导入状态（家长中心「知识点更新」用） |
| `POST /api/knowledge-points/packages/{edition_key}/sync` | 按需下载导入（建小孩保存绑定后前端自动调用；等待 5-60s，返回导入条数） |
| `POST /api/knowledge-points/packages/update` | 检查并应用所有可更新版本（家长中心按钮） |
| `GET /api/knowledge-points/editions` | 库中已导入的版本（出题/列表过滤用） |

---

## 4. 小孩教材绑定流程

**后端**（`backend/app/routers/users.py`）：
- `PUT /api/kids/{kid_id}/textbooks`：批量保存该小孩各学科版本偏好（`kid_textbook` upsert）；
- 建小孩接口（`POST /api/users`，role=child）允许带 `textbooks` 数组，一步完成。

**前端**：
- 建小孩流程（`SelectKid.vue` / 账号管理 `UserManage.vue`）：新增「教材版本选择」——按学科展示版本下拉；地区选择 → 预填推荐版本（可改，`data/region_versions.json`，先省级、手工维护）；
- 保存偏好后：调 `POST /api/knowledge-points/packages/{edition_key}/sync`，弹出 loading「正在同步教材知识点…」，完成提示；失败可重试；
- 小孩设置里随时可改版本（转学/换教材）：改偏好 → 重新 sync → 知识点列表跟着换；**历史题目/错题/统计冗余的是知识点名称字符串，天然不受影响**。

**地区推荐数据** `backend/data/region_versions.json`（可后置，先做手动选版本即可跑通）。

---

## 5. 现有导入入口改造（3 处）

| 入口 | 改法 |
|---|---|
| AI 生成知识点（`frontend/src/components/AiKpImport.vue`） | 顶部加「按小孩带入」下拉：选小孩 → 预填 subject_id + version（后端 `ai-generate` 查重逻辑带 `edition_key`，跨版本不再误判重复）；生成结果导入时写 `source='textbook'` + `edition_key` |
| 按教材同步导入（`frontend/src/views/TextbookImport.vue`） | 同上预填；在线大纲 / PDF OCR 提取写入时带 `edition_key`（若该版本已有官方包，提示「官方包已覆盖此版本，建议直接同步」） |
| K12 导入（`backend/app/routers/k12.py`） | 保留为兜底；导入行写 `source='textbook'` + `edition_key=NULL`（通用数据，任何版本可见）；出题过滤靠 §7 的 NULL 分支兼容旧数据 |

---

## 6. 出题/知识点列表过滤

- `backend/app/routers/knowledge_point.py:128` `list_knowledge_points` 加参数 `edition_key`；
- 过滤条件：`source='custom'` **OR** `edition_key IS NULL`（通用教材数据，兼容旧 K12 导入）**OR** `edition_key = 小孩偏好`；
- 前端出题弹窗（`PracticeSets.vue`）请求时传小孩该学科偏好 `edition_key`（从 `/api/kids/{kid_id}/textbooks` 取）；
- 家长中心知识点管理（`Management.vue` 知识点 tab）：**教材知识点只读**（标注版本来源，不提供编辑/删除按钮）；**自定义知识点可编辑**（现状功能保留）。

---

## 7. 验收标准

1. **建小孩**：选完三科版本 → 出题界面知识点 = 该版本×年级×学科 + 自定义，无缺无重；
2. **改版本**：设置里换版本 → 知识点列表跟着换，历史错题/报告原样；
3. **重复初始化**：同一版本 sync 两次 → 行数不翻倍（按 edition_key 全量替换天然幂等）；
4. **更新发布**：分发源出新修订 → 点击更新 → 旧版行被新版替换、全库无重复；其他版本和自定义知识点原样；
5. **断网/失败**：下载失败可重试、库不受影响；
6. **多小孩**：大孩三年级用 A 版、小孩一年级用 B 版，互不干扰（共享库一份数据，偏好各自过滤）。

---

## 8. 阶段划分与工作量

| 阶段 | 内容 | 估计 |
|---|---|---|
| P1 | 数据模型：`knowledge_point` 3 列 + `kid_textbook` 表 + 索引 | 0.5～1 人日 |
| P2 | **调研 K12 数据结构**（能否按版本归类）→ 打包脚本（模式 A + 模式 B）+ 首批常见版本包 | 2～4 人日 |
| P3 | `kp_package.py` 服务 + 4 个接口 + 更新机制（版本化/覆盖/失败安全） | 1～2 人日 |
| P4 | 小孩教材绑定：后端 API + 建小孩/账号管理 UI + sync 流程 | 1～2 人日 |
| P5 | 导入入口改造（3 处预填小孩偏好）+ 出题/列表过滤 + 家长中心只读分层 | 1～1.5 人日 |
| **合计** | | **约 5.5～10.5 人日**（不含后续新增教材版本的 OCR+LLM 生成，每版本 1-2 人日） |

建议实施顺序：**P1 → P2（先调研）→ P3 → P4 → P5**；P2 的调研结果决定模式 A 走「按版本归类」还是「通用整包」，影响后续全部设计。

---

## 9. 决策点（实施前需确认）

1. K12 数据集若能按教材归类，首批打包哪几套？（建议：语文统编、数学人教/北师大/苏教、英语人教PEP/外研）
2. 2022 课标新教材（2024 起滚动替换）是否本轮就生成打包，还是先做旧课标、新教材走本地兜底？
3. 地区推荐（`region_versions.json`）先做省级还是后置（先只手动选版本）？
4. 家长中心「检查更新」按钮 vs 启动自动检查+角标（默认推荐手动按钮，无打扰）。

## 10. 风险

| 风险 | 对策 |
|---|---|
| K12 数据集结构无法按教材版本归类 | P2 第一步先调研；退化为「通用整包」（edition_key NULL），出题任何版本可见，损失仅为版本精确度 |
| 2022 课标新教材不在 K12 数据集中 | 模式 B（OCR+LLM 开发期生成一次打包），或先走本地 AI 提取兜底 |
| 分发源国内访问慢/挂 | 多源容错（GitHub → ghproxy）+ 手动放包兜底 `backend/data/kp_packages/`（沿用 data/textbooks 模式） |
| 本地 OCR+LLM 提取的冷门版本知识点质量 | 只作兜底；官方包一出即按 edition_key 覆盖 |
