# AI_KP_IMPORT — AI 智能生成教材知识点（大模型直接获取）
- [x] 后端：KnowledgePointCreate 加 version/description 并写入；POST /api/knowledge-points/ai-generate（教材/自定义模式 → LLM JSON → 查重返回）
- [x] 前端：新建 AiKpImport.vue 弹窗（教材模式学科/版本/年级/册次 + 自定义指令+归属 → 生成 → 预览可编辑 → 导入所选）
- [x] 前端：Management.vue 知识点管理加「🤖 AI 生成知识点」按钮 + 组件挂载
- [x] 构建 + 重启后端 + 8016 实测（custom 4条✅ / textbook 数学人教版三上 9单元46条✅ / UI 教材模式41条预览✅ / custom 导入 grade=3 归属修复✅；测试数据已清理）
