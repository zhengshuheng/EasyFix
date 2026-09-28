# 2026-09-28 — MOBILE_UI_5FIX：筛选单行 + 练习窄屏 + 报告沉淀列表

## 需求（用户 9/28 反馈第二批）
1. 单词模块：搜索单词/学期/标签筛选 → 一行展示（现换行）
2. 语法模块：年级/板块/搜索语法点筛选 → 一行展示（现换行）
3. 练习模块：日期筛选时间选择器过大、显示不完整
4. 练习模块：类别（操作）项过大导致数据显示不完整无法操作
5. 报告模块：生成的报告无法记录沉淀到列表中

## 改动
### 前端 UI
| 位置 | 改动 |
|---|---|
| `frontend/src/views/Words.vue` | @media 块加 `.filters` 单行横滑（搜索180+年级120+学期100+标签150≈590px，flex nowrap + overflow-x:auto，控件 flex:0 0 auto） |
| `frontend/src/views/Grammar.vue` | 新增 `@media (max-width:768px)`：`.filters` 单行横滑（年级120+板块170+搜索200≈490px + filter-count 计数 nowrap） |
| `frontend/src/styles/mobile.css` | 日期范围弹层收窄：`.el-picker-panel{width:94vw!important}` + `.el-date-range-picker__body{min-width:0}` + 左右两列各 50% + body-wrapper overflow-x:auto（桌面弹层 646px 两列日历，375px 屏显示不完整/无法操作） |
| `frontend/src/views/PracticeSets.vue` | 操作列 `width="400" fixed="right"` → `:width="isMobile ? 90 : 400"`；移动端按钮组收敛为「操作」el-dropdown（查看详情/下载PDF/删除）。script 加 `isMobile`（matchMedia ≤768 + change listener + onBeforeUnmount 清理）与 `handleMobileAction(cmd,row)`。根因：固定列 400px 占满 375px 屏 → 数据列完全不可见 |
| `frontend/src/views/LearningReports.vue` | generateReport 成功后 `await fetchReports()` + **沉淀兜底**：若新报告不在列表（空间学科/年级筛选不匹配，如全科报告在学科空间生成），unshift 到列表顶部 + total+1，保证"生成的报告一定能沉淀到列表" |

### 后端（报告数据隔离 + 参数契约）
| 位置 | 改动 |
|---|---|
| `backend/app/routers/learning_report.py` | `/generate` 加 `kid_id=Depends(get_current_kid_id)` → `LearningReport(user_id=kid_id)`（模型早有 user_id 字段但从未接线） |
| 同上 | `/list` 补 `grade: Optional[int]` 参数（前端一直传、旧版被 FastAPI 静默忽略）+ `kid_id` 过滤 `or_(user_id==kid_id, user_id.is_(None))`（按小孩隔离，兼容历史 NULL 归属报告） |

## 根因
- #3：日期范围选择器弹层（el-date-range-picker popper）桌面默认两列日历约 646px，375px 屏弹出即溢出 → 显示不完整、操作不便。
- #4：el-table 操作列 `width="400" fixed="right"` 在窄屏永远占满可视宽度 → 数据列被挤出（表格横滑也看不到数据）。
- #5：`LearningReport` 模型有 `user_id`（"归属小孩，数据隔离"）但 generate 不写入、list 不按小孩过滤；且前端传 grade 参数后端忽略 → 报告生成后可能因列表筛选条件不匹配而"看不见"。前端已生成过的报告（详情能打开）但列表无 → 用户视为"没沉淀"。

## 验证
- `npm run build:trial`（28.72s）+ `npm run build`（28.06s）均通过。
- 后端 `python -m py_compile` 通过。
- 产物断言：
  - `Words-1ae130b8.css` / `Grammar-a0117a6d.css`：`.filters{display:flex;flex-wrap:nowrap;gap:8px;overflow-x:auto...}`
  - `index-2b753928.css`：`.el-picker-panel{width:94vw!important}` + range picker 两列 50%
  - `PracticeSets-90b989d0.js`：matchMedia change listener + dropdown 命令 "pdf"/"delete"
  - `LearningReports-f634c393.js`：`items.unshift` 沉淀兜底
  - 后端：list 签名含 grade + kid_id 过滤；generate 写 user_id=kid_id

## 遗留
- 用户 deploy（前端 dist + 后端 learning_report.py）后真机验证。
- 行为变化提示：报告列表现在**按小孩隔离**（X-Kid-Id 头自动生效），家长空间未选小孩时仍全量可见；历史 NULL 归属报告兼容可见。
- 列表 grade 过滤已生效：学习空间指定年级时列表只显示该年级报告（与前端原设计一致，旧版被后端静默忽略）。
