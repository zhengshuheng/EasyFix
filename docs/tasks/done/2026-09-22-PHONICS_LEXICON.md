# PHONICS_LEXICON — 自然拼读词库覆盖（学段选择 + 从单词表提取分类 + 覆盖量展示）

目标：拼读页能看到"覆盖词汇量/学段"，词库从 word 表按学段提取并自动归入规则。

- [x] 后端：phonics.py 增加 stage 参数 + 词库覆盖统计（word 表按 grade 分学段，pattern 匹配归类，去重，过滤多词短语）
- [x] 后端：list_rules 返回每条规则的 lexicon_words / lexicon_count / lexicon_total（示例词与词库词并存）
- [x] 后端：/api/phonics/lexicon-stats 学段统计（总词数/覆盖词数/覆盖率/规则覆盖数）
- [x] 前端：Phonics.vue 顶部加学段选择（小学/初中）+ 覆盖量统计条（词库总数/覆盖词数/覆盖率进度条）
- [x] 前端：规则卡片显示"词库覆盖 N 词"，可展开查看词库词（含年级标签）
- [x] 前端：练习出题池按学段词库词优先（lexicon_words → example_words 兜底）
- [x] 前端：初中词库为空时提示先导入教材词
- [ ] 初中词库：等用户确认 A(内置 seed 1000-1500 词) / B(先空，用户导入后自动归类)
- [x] vite build 验证通过（后端 _test_lexicon2 验证：小学 234 词/覆盖 160/40 规则全覆盖）
