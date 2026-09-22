# TEXTBOOK_PATH — 教材「手动放置」路径随选择动态显示 + 目录自动创建

- [x] 1. 后端 textbook_service：新增 manual_pdf_dir/manual_pdf_path/ensure_manual_dir（含目录名清洗、自动 makedirs、可选打开资源管理器）
- [x] 2. 后端 download_book 无在线源分支先建目录再抛错；scan_local 目录缺失时自动创建
- [x] 3. 路由新增 GET /api/textbook/manual-dir（版本/科目/年级/册次 + open 参数）
- [x] 4. 前端 api/textbook.js 加 manualDir()
- [x] 5. 前端 TextbookImport.vue：提示改为按当前选择动态显示绝对路径 + 文件名；加「创建并打开该教材文件夹」按钮与「复制路径」；修掉硬编码「英语」的兜底文案；选择变化即静默建目录
- [x] 6. 前端构建（NODE_OPTIONS=4096）→ dist/index-5b291178.js
- [x] 7. 自测：8016 浏览器实测动态路径/目录自动创建/复制路径/按钮启用；curl 验证 manual-dir（含空值不建 未分类、非法字符清洗）；自测残留目录已清理
- [x] 8. 「扫描本地 PDF」改为扫描当前选择的教材目录：后端 scan_local(version/subject) 只扫 data/textbooks/<版本>/<科目>（返回 scoped+dir），/scan 接受 query；前端已选学科+版本时传参扫描、提示显示被扫目录，空目录提示放入路径与文件名；优先精确 <年级><册次>.pdf 匹配
- [x] 9. 重建 dist（index-23950964.js）；8016 浏览器实测：人教版/数学 扫描出 1 个 PDF 并选中当前教材、苏教版/数学 空目录提示；用户 8012 实例已跑新后端代码（manual-dir/scan 均 200）
