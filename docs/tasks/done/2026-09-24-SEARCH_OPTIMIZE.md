# SEARCH_OPTIMIZE — 定位检索省token + 编码规范约束

## 目标
1. 大文件定位问题时不全量 read_file，用结构化检索减少 token
2. 把拆分/检索教训固化为编码规范约束

- [ ] 扩展 AGENTS.md：定位检索 SOP（grep→lsp/ast→精确分段读）+ 大文件定位规范
- [ ] 实现 `tools/file_map.py`：扫描 .vue/.py 输出结构索引（区块/函数/常量行号）
- [ ] 实测对 PracticeSets.vue 等大文件生成地图并演示检索路径
- [ ] 归档任务文档

## 进度
