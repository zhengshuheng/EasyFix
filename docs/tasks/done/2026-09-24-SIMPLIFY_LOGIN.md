# SIMPLIFY_LOGIN — 官网登录即进家长空间，token 永久（已完成 2026-09-24）

- [x] 后端 trial.py：新增 issue_space_token_for_account（账号→空间→签发主账号永久 token）
- [x] 后端 account_api.py：register/login 返回 space_token；account token 改永久
- [x] 前端 site/app.js：登录成功自动跳空间；双 token（space/account）；getToken 改读 account token；logout 清双 token
- [x] 空间 Login.vue：文案注明主/辅家长账号均可登录（已重建 dist-trial 生效）
- [x] 验证：后端语法+前端语法；浏览器实测官网登录→SelectKid、清缓存→登录页、辅账号登录
- [x] 修复 easyfix_demo 登录后 SelectKid chunk 404：npm run build:trial 重建产物，浏览器回归通过（admin/32167 → SelectKid 正常 + 新文案生效）

> 后续任务 ONBOARDING+OPS（引导 v2）基于其上：注册标记 → 首次引导。
