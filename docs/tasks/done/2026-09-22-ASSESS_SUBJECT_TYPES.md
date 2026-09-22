# ASSESS_SUBJECT_TYPES — 英语评测题型白名单 + repo wiki + 文档规约整改

## 目标
1. 修复：英语能力评测混入"英语化的数学应用题"（qid 72 'I have three red apples'），1年级英语卷出现"Write the number sentence"数学题。
2. 建立 repo wiki（AI_CONTEXT.md）减少模型返工。
3. 整改：根目录遗留 *_TODO.md 归档、临时文件归位，让模型遵守 docs/CONVENTIONS.md。

## 结果
- [x] 诊断：`_load_questions()` 只按 subject_id+grade 过滤，未按学科限定题型；英语学科 2 道 application 题（How many… 共 4 题）被组进英语卷，且 TYPE_ORDER 应用题最优先
- [x] 新增 `_SUBJECT_ALLOW_TYPES` 学科题型白名单：英语(2)/语文(3) 排除 application（应用题是数学题型）；数学(1) 不限
- [x] 验证：英语组卷题型 ['fill'] 无 application；数学组卷正常（application 10 题）PASS
- [x] 新增 `docs/AI_CONTEXT.md`（模型工作上下文速查：判分三态/组卷白名单/结算规则/高频坑/运行环境），加入 docs/README.md 地图
- [x] 根目录 13 个历史 *_TODO.md → `docs/tasks/done/2026-09-22-*.md`，docs/tasks/README.md 索引更新（45+13）
- [x] backend/_tmp_*、根目录截图 → tools/tmp/
- [x] MEMORY.md 追加"项目文档规约"条目（先读 docs/README.md + AI_CONTEXT.md + AGENTS.md；根目录禁建 md；TODO 进 docs/tasks/；临时文件 tools/tmp/）

## 验证证据
- `_tmp_verify_types.py`：英语组卷题型 ['fill']、无 application；数学 application 10 题 → PASS
- 前端本轮未改动；后端逻辑改动小，冒烟通过

## 遗留
- 英语 1 年级卷题型偏单一（本次实测全 fill）——choice/judge/sentence 题量少或年级匹配不足，后续可调组卷比例；本次不做
