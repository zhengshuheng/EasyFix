# OPTIMIZE_PHONICS_TAB — 重建 Phonics.vue（修复 edit_file 全局替换导致的内容重复）

- [x] 用临时文件分段写模板/脚本/样式（避开 edit_file 全局替换）
- [x] 重做 tab 结构：hero 顶部主 tab（规则浏览/拼读练习）+ 浏览模式下类别 tab 分离
- [x] 拼读练习区大气化（题型卡 230px、答题卡 720px 居中、结果卡大数字）
- [x] PhonicsPanel.vue tab 结构同步（main-tabs/cat-tabs + switchCategory）
- [x] node 拼接生成完整文件
- [x] 校验结构（script/style 各 1 份）+ 构建验证（Phonics.js 12.70kB）
