# editions-menu — 教材版本独立菜单（统一版本管理）

日期：2026-09-26 ｜ 状态：完成

## 目标
知识点与英语单词统一使用同一套教材版本管理；教材版本从知识点页弹窗升级为独立菜单维护。

## 改动

### 前端（frontend/ops/src/）
- 新增 `views/EditionsManage.vue`：独立版本管理页（原 EditionsDialog 弹窗升级为页面）
  - 列表：学科/版本名/册数/知识点/单词/状态/说明/操作
  - 新增/编辑/删除（删除连带软删该版本知识点+单词）
  - **未登记版本**（历史数据中存在、未写入版本表）：状态列显示「未登记」tag，操作列提供「登记」（一键写入版本表，幂等）与「删除」（连带删数据）
  - 顶部提示：知识点与英语单词统一使用本版本库
- `router.js`：新增路由 `/editions`（教材版本）
- `layout/OpsLayout.vue`：教材数据 子菜单新增「▸ 教材版本」
- `views/KpManage.vue`：移除「📖 教材版本」按钮与 EditionsDialog 引用（版本管理统一走独立菜单）

### 后端
- `backend/app/services/ops_data_service.py`
  - `get_ops_editions()`：融合数据中实际存在但未登记的 学科+版本（标记 `registered: False`），版本页成为全量权威视图
  - 新增 `register_ops_edition()`：幂等登记历史版本进版本表
  - 新增 `delete_ops_edition_data()`：按 学科+版本 软删知识点+单词（不涉及版本表）
- `backend/app/routers/ops_data_router.py`
  - 新增 `POST /api/ops/editions/register`（登记）
  - 新增 `DELETE /api/ops/editions/by-name`（按学科+版本删数据）
  - **路由顺序**：`/editions/by-name` 必须定义在 `/editions/{edition_id}` 之前（否则 by-name 被 int 转换拦截）

## 验证（服务 8012 重启后）
- 浏览器：登录 → 教材数据 ▸ 教材版本：显示 4 行全量清单
  - 数学 北师大版（已登记启用）；数学 人教版 / 英语 人教版PEP / 语文 统编版（未登记，各有登记/删除按钮）
- 知识点页版本 chips：人教版 / 北师大版（与版本库一致）
- 单词页版本 chips：人教版PEP（仅英语版本，正确隔离）
- TestClient→HTTP（运行中服务）：register 200 id=4、列表 registered=True、幂等 True、by-name 删数据 200、删版本记录 200、清理后无残留
- 测试临时版本「测试登记版TEMP」已清理

## 补充（同日）：按科目分组显示
- `EditionsManage.vue` 改为 el-collapse 折叠面板按科目分组（默认全展开，可逐组折叠）
  - 组标题：科目 + 统计（N 个版本 · X 知识点 · Y 单词）
  - 组内表格去掉「学科」列，保留 版本名/册数/知识点/单词/状态/说明/操作
  - 科目顺序：数学 → 语文 → 英语；空科目不显示
- 浏览器验证：数学（2 版本·392 知识点·0 单词：北师大版/人教版）、语文（1·299：统编版）、英语（1·160·917：人教版PEP）；折叠语文组后统编版隐藏、再展开恢复；未登记行「登记/删除」、已登记行「编辑/删除」按钮均正常

## 遗留
- 历史版本（人教版/人教版PEP/统编版）保持「未登记」状态，运营可在版本页一键登记（不强制迁移，避免改动正式数据）
- 版本编辑/停用后知识点/单词页 catalog 在下次进入页面时自动刷新（onMounted 重新拉取）
