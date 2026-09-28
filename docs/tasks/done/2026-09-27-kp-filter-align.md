# 2026-09-27-kp-filter-align.md

## 家长端知识点过滤条件与运营平台对齐（完成）

**用户反馈**：家长管理中心「知识点」过滤条件过于复杂、选项与运营平台没有对齐。

**根因**（对比 `frontend/src/views/Management.vue` 与 `frontend/ops/src/views/KpManage.vue`）：
- 家长端知识点过滤栏 7 组：学科/年级/学期/标签/要求/类型/版本；ops 仅 5 组：学科/版本/年级/册次/搜索。
- 家长端独有的「标签/要求/类型」为自由字段聚合（ops 无此维度，不对齐）。
- 家长端年级选项 1-12（含初一~高三）；ops 仅小学 1-6。
- 家长端「版本」组无默认选中（`applySyncedEditionDefault` 在 `synced.kp` 为空时提前 return，而模板库预置数据的空间 synced 恒空）；ops 默认选中第一个版本。

**改动**（均在 `frontend/src/views/Management.vue`）：
1. 过滤栏收敛为 5 组：学科 / 版本 / 年级 / 册次（原「学期」改文案为册次/上册/下册）/ 搜索（新增输入框按名称/章节/说明关键字）。
2. 删除 kpFilterTag/kpFilterRequirement/kpFilterType 状态与过滤逻辑；新增 kpFilterQ 并在 applyKpFilter / kpFilterText 中接入。
3. gradeOptions 收敛为小学 1-6。
4. applySyncedEditionDefault：synced.kp 为空时兜底选中第一个非 custom 版本（与 ops 默认行为一致）。

**保留**：kpOptionTags/kpOptionRequirements/kpOptionTypes 仍用于新增/编辑知识点弹窗表单；fetchKpOptions 调用不变。

**验证**（8012，临时空间 gpxj7jjkErT-Qg / 账号 kpfilter_0927，已清理 registry 与账号）：
- 过滤栏 5 组渲染正确，无 标签/要求/类型 过滤组；
- 年级仅 1-6；版本默认选中「人教版」（checked=true，筛选：版本:人教版 共 98 条）；
- 搜索「分数」→ 筛选：搜索:分数 · 版本:人教版（共 4 条），分组显示正确。
- dist + dist-trial 已构建；浏览器需 Ctrl+F5 / 带 ?v=N 绕过 index.html 缓存。

**遗留**：
- 临时空间 db 文件 `backend/trial_data/tenants/gpxj7jjkErT-Qg.db(+wal/shm)` 因 8012 句柄占用未删，registry 记录已删；下次 8012 重启后运行 `python tools/tmp/cleanup_kpfilter.py` 即可（脚本已留）。
- 观察到的既有问题（不在本次范围，供参考）：`ParentLockDialog` 候选 1 的 `/api/auth/me` 裸 fetch 无 X-Trial-Key 时查主库，返回主库默认家长「admin」，新注册空间（空间 admin 已改名）家长中心弹锁可能失败；建议后续给该 fetch 加 X-Trial-Key header。
