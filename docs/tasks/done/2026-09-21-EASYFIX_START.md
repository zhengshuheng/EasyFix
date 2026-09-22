# EASYFIX_START — EasyFix 学习软件一键启动（端口配置化）
- [x] 1. 创建 backend/.env（HOST/PORT 配置化，基于 .env.example）
- [x] 2. 修改 backend/app/main.py：挂载 frontend/dist 静态资源 + SPA fallback（同源 /api）
- [x] 3. 在项目根创建 .venv 虚拟环境并安装依赖（补充 fpdf2/anthropic，paddle 可选）
- [x] 4. 编写 一键启动.bat：读 .env 端口 → 用 .venv 启动 uvicorn → 打开浏览器
- [x] 5. 运行验证：/health 200、/ 返回前端页面、/assets 200、/api 404 隔离
