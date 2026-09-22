# KID_ISOLATION_ARCH — 数据隔离架构说明 + 评测分小孩修复

- [x] 诊断评测分小孩问题根因（后端 _resolve_user_id 回退第一个小孩，前端未走 X-Kid-Id）
- [x] 后端 assessment.py 改用 kid_context 依赖（history=current，start/submit=required，detail 加归属校验）
- [x] _auto_refill 不再硬编码 user_id=1，归属当前小孩
- [x] 前端保持 header 注入规范（不传 body user_id），恢复 assessment.js / Assessment.vue
- [x] 真实 HTTP 冒烟：未选孩子 start 400、孩子A/B 历史隔离、跨孩子 detail 404
- [x] vite build 通过
- [ ] 编写 docs/ARCHITECTURE.md（数据隔离架构说明）
- [ ] AGENTS.md 加入口指引
- [ ] docs/README.md 快速导航加行
- [ ] 归档任务文档到 docs/tasks/done/ 并更新索引

## 验证证据

- `python -m py_compile app/routers/assessment.py` OK
- `.venv` 导入 app.routers OK
- 真实 HTTP（uvicorn :8756）：login 401（密码非 admin123，不影响）；未选孩子 start → 400；
  kidA(3) start 10 题/submit 200/history 7 条；kidB(5) history 0 条；detail 跨孩子 404
- `npm run build` → BUILD_OK
