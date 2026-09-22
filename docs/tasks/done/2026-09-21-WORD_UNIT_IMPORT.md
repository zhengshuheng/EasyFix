# WORD_UNIT_IMPORT — 文本导入支持整表粘贴（Unit 识别）
- [x] 后端：word 表加 unit/unit_title 列（main.py _ensure_column + models/word.py + schemas/word.py）
- [x] 后端：create/update/batch 支持 unit/unit_title
- [x] 前端：smartParseWords 重写——识别 Unit N 标题行 + 按首个 CJK 切分中英（兼容多词英文/括号释义）
- [x] 前端：预览表格加「单元」列；importWords 传 unit；主表格「单元」列；编辑弹窗加单元
- [ ] 构建 + 重启后端 + 8016 实测（粘贴用户示例 12 单元整表 → 解析→入库→单词库显示单元）
