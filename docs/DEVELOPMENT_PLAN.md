# EasyFix 开发计划与商业闭环路线图

> 更新：2026-09-14
> 目标：本地数据 + 远程授权订阅的混合架构；当前执行 **阶段 1（本地角色系统）**

---

## 商业闭环总览

```
用户转账 → 后台手动发激活码 → 本地输入激活码 → 联网激活一次（绑定设备指纹）
→ 签发签名 License 存本地 → 日常离线可用 + 定期心跳校验订阅 → 到期宽限期 → 续费
```

| 阶段 | 内容 | 状态 |
|------|------|------|
| 阶段 1 | 本地角色系统：家长(≤2)/小孩(≤5)、登录、权限控制 | 🟢 本次执行 |
| 阶段 2 | 最小授权闭环：远程账户 + 手动激活码 + License 签名 | ⏳ 待办 |
| 阶段 3 | 支付接入、打包分发、版本更新 | ⏳ 待办 |

---

## 阶段 1：本地角色系统

### 背景约束

- 前端源码不在本仓库（`frontend/` 仅有 dist 构建产物）→ 前端菜单显隐、角色登录页**无法本次完成**
- 策略：**后端角色体系 + 权限强校验**先行；前端通过「宽松→严格」兼容模式保持现有页面可用；前端源码到位后再做登录页/菜单改造
- 鉴权模式：系统只有默认家长账号时 = **宽松模式**（未登录视为 admin，兼容旧前端）；创建第二个用户后 = **严格模式**（所有管理接口必须登录）

### 任务清单

#### 1. 数据模型
- [ ] `backend/app/models/user.py`：User 表（username/password_hash/role/pin/display_name/avatar/enabled/created_at）
- [ ] `backend/app/models/__init__.py` 注册 User

#### 2. 认证基础（标准库，不新增依赖）
- [ ] `backend/app/utils/auth.py`：PBKDF2 密码哈希 + HMAC 签名 Token（签发/解析）+ `get_current_user` / `require_admin` FastAPI 依赖 + 宽松模式判定

#### 3. 认证 API（`backend/app/routers/auth.py`）
- [ ] `POST /api/auth/login`：家长(用户名+密码) / 小孩(username+PIN) → `{token, role, user}`
- [ ] `GET /api/auth/me`：当前用户信息
- [ ] `POST /api/auth/verify-password`：保留旧接口兼容旧前端（校验默认家长密码 → success）

#### 4. 用户管理 API（`backend/app/routers/users.py`，仅 admin）
- [ ] `GET /api/users`：用户列表
- [ ] `POST /api/users`：创建小孩(上限5) / 第二个家长(上限2)
- [ ] `PUT /api/users/{id}`：改名/头像/启用禁用
- [ ] `PUT /api/users/{id}/password`：家长改密 / 小孩改 PIN
- [ ] `DELETE /api/users/{id}`：删除小孩；保护：不能删自己、不能删最后一个家长

#### 5. 集成与初始化
- [ ] `backend/app/main.py`：注册 auth/users 路由
- [ ] 启动初始化：无用户时自动创建默认家长 `admin / 32167`（迁移自 ACCESS_PASSWORD）
- [ ] 权限加固：管理类接口挂 `require_admin`（先覆盖 `config_router` 等最明显的管理接口，其余列出待扩展）

#### 6. 验证
- [ ] 启动服务：默认家长可登录、宽松模式旧前端接口正常
- [ ] 严格模式：创建小孩后管理接口未登录返回 401
- [ ] 数量限制：家长 2 / 小孩 5 超限返回错误

### 已知限制（待前端源码）
- 前端无角色选择登录页、无菜单显隐 → 小孩目前仍能打开管理页面（接口会被 403），需前端源码接入后才能完整体验

---

## 阶段 2：最小授权闭环（待办，本次不执行）

- [ ] 远程授权服务 `server/`（轻量 FastAPI）：账号注册/登录、激活码生成与绑定、设备指纹登记、License RSA 签名签发
- [ ] 本地激活模块：`POST /api/license/activate`（激活码 → 联网换 License 存本地）、`GET /api/license/status`（心跳/到期日）
- [ ] License 本地校验（RSA 验签 + 到期日 + 设备指纹比对 + 宽限期）
- [ ] 后台管理页：生成激活码、订单状态（转账手动确认）、解绑设备
- [ ] 打包分发（PyInstaller + PyArmor 混淆）

---

## 阶段 3：商业化（待办）

- [ ] 支付接入（先手动转账确认，后微信/支付宝自动回调）
- [ ] 授权后台：订单管理、设备管理、订阅期管理
- [ ] 版本更新机制、用户协议/隐私声明
