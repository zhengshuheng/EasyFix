# EasyFix 数据隔离架构说明

> 给未来的 Agent / 开发者：**每次新增功能前先读本文档**，按「第 7 节检查清单」逐项核对，
> 确保新表、新接口、新页面从一开始就做对数据隔离，避免出现"评测记录全记在第一个小孩名下"这类问题。
>
> 适用读者：本仓库所有写代码的会话（Claude Code / Agent / 人工）。

## 1. 身份模型：家长 + 多个小孩

本系统是一个**家长账户管理多个小孩**的应用：

- 家长：`users.role == 'admin'`，登录后可在顶栏切换当前操作的**小孩**。
- 小孩：`users.role == 'child'`，是**学习数据的最小归属单元**。
- 前端把"当前选中的小孩"写入 `localStorage['easyfix_kid']`，并由 `frontend/src/api/http.js`
  **自动附加到每个请求的 `X-Kid-Id` 请求头**（调用方显式设置的 `X-Kid-Id` 优先，见 http.js:22）。

```
浏览器
  └─ http.js 拦截器：Authorization: Bearer <token>
                     X-Kid-Id: <当前选中小孩 id>   ← 全自动，页面无需关心
FastAPI
  └─ kid_context.resolve_kid_id()
        - 登录者是小孩(role=child) → 强制用自己的 id（请求头无法冒充他人）
        - 登录者是家长(role=admin) → 读 X-Kid-Id（未传/非法 → None 或 400）
```

**核心约定：不要在请求体（body/query）里传 `user_id`，一律走 `X-Kid-Id` 请求头。**
（历史模块 word.py 等仍用 query 参数 user_id + `_resolve_user_id` 回退第一个小孩，属遗留反模式，见 §6。）

## 2. 数据的三类归属

新增任何数据表前，先回答：**这条数据属于谁？**

| 归属类型 | 判定标准 | 例子 | 表里怎么写 |
|---|---|---|---|
| A. 全局共享 | 所有小孩共用同一份内容，不随孩子变 | 单词库 word、学科 subject、语法课 grammar_lesson、拼读规则 phonics_rule、激励奖品 reward | **没有** user_id（或仅标记创建者） |
| B. 按小孩隔离 | 每个孩子自己的进度/记录/成绩 | 错题 error_question、练习卷 practice_set、作答 practice_attempt、单词进度 word_progress、语法进度 grammar_progress、拼读作答 phonics_attempt、评测记录 assessment_record、积分 star_*、成就 achievement_progress、兑换 redemption、学习报告 learning_report | **必须** `user_id`，且写入时用当前小孩 id |
| C. 家长级 | 家长账户自己的配置/上传 | 家长创建的错题本（未分配）、系统配置 | 无 user_id 或 user_id 可空（NULL=未分配） |

> 一个容易踩的坑：**题目快照 practice_question 是 B 类（归属生成它的那个小孩），
> 但内容上可被所有小孩复用**（评测抽题不按 user_id 过滤，而是按学科+年级）。所以：
> `user_id` 表示"这条快照是谁产生的"，查询是否隔离取决于业务语义，不要机械地在所有查询里都加 user_id 过滤。

## 3. 后端：标准隔离工具（必须使用）

文件：`backend/app/utils/kid_context.py`，共 3 个工具：

```python
from app.utils.kid_context import get_current_kid_id, get_required_kid_id, filter_by_kid
```

| 工具 | 用途 | 未选孩子时 |
|---|---|---|
| `get_current_kid_id` (依赖) | **读类**接口（列表/详情/统计） | 返回 `None` = 家长未指定，**查看全部** |
| `get_required_kid_id` (依赖) | **写类**接口（新增/修改/提交） | 返回 HTTP 400「请先在主页选择孩子」 |
| `filter_by_kid(query, column, kid_id)` | 给查询加 `WHERE column == kid_id`（kid_id 为 None 时不过滤） | — |

### 路由写法模板

```python
# 读类：按当前小孩隔离（家长未选孩子 → 看全部）
@router.get("/history")
def list_something(kid_id: Optional[int] = Depends(get_current_kid_id),
                   db: Session = Depends(get_db)):
    q = db.query(SomeModel).filter(SomeModel.status == "done")
    q = filter_by_kid(q, SomeModel.user_id, kid_id)
    rows = q.order_by(desc(SomeModel.created_at)).all()

# 写类：必须先选孩子，把记录归属到当前小孩
@router.post("/submit")
def submit_something(req: SomeRequest, db: Session = Depends(get_db),
                     kid_id: int = Depends(get_required_kid_id)):
    db.add(SomeModel(user_id=kid_id, ...))   # ← 归属用 kid_id，绝不硬编码

# 详情类：加归属校验（防止小孩 A 看小孩 B 的记录）
@router.get("/{record_id}")
def detail(record_id: int, kid_id: Optional[int] = Depends(get_current_kid_id),
           db: Session = Depends(get_db)):
    r = db.get(SomeModel, record_id)
    if not r:
        raise HTTPException(404, "记录不存在")
    if kid_id is not None and r.user_id != kid_id:
        raise HTTPException(404, "记录不存在")   # 同 404，不泄露存在性
```

**路由函数签名规则**：依赖参数（`kid_id`/`db`）一律放**最后**；FastAPI 按参数名注入，位置不影响调用，
但直接单测调用时按签名传参（参考 `backend/_test_*.py` 的历史写法）。

## 4. 数据表设计规则

新增 ORM 模型时（`backend/app/models/*.py`）：

```python
class SomeRecord(Base):
    __tablename__ = "some_record"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)  # 归属小孩（数据隔离）
    # ...业务字段...
    deleted = Column(Boolean, default=False, nullable=False)  # 软删除，全表强制
```

- **B 类（按小孩隔离）**：`user_id` 必须 `nullable=False, index=True`，注释写明「归属小孩（数据隔离）」。
- **A 类（全局共享）**：不加 user_id；若需记录来源，用单独字段且不参与隔离过滤。
- **软删除**：所有模型必须 `deleted` 字段，查询加 `deleted == False`，禁止硬删除。
- **高频组合查询**：建复合索引，如 `Index("ix_xxx_user_time", "user_id", "created_at")`、
  `Index("ix_error_question_user_active", "user_id", "status", "deleted")`。
- **唯一约束**：按小孩去重时用 `UniqueConstraint('user_id', 'xxx_id')`，如 `achievement_progress`。
- **建表方式**：无迁移系统，`Base.metadata.create_all()` 自动建；改结构需删 `backend/easyfix_main.db` 或手工重建（MySQL）。

## 5. 前端：数据隔离的正确姿势

- **不要**在页面/API 层手动传 `user_id`（body/query 都不传）——http.js 已全局注入 `X-Kid-Id`。
- 需要显式指定**其他**小孩时（如家长中心给某个小孩调积分），在调用处设置请求头：
  ```js
  request.post('/xxx', data, { headers: { 'X-Kid-Id': String(kidId) } })
  ```
- 直接 `import axios` 的请求也会被 `http.js` 的全局 axios 拦截器带上 `X-Kid-Id`（http.js:38-45）。
- 前端切换小孩后，**页面数据要刷新**（监听当前小孩变化重新拉取），避免显示上一个孩子的数据。

## 6. 反模式清单（看到这些 = 立即修）

| 反模式 | 危害 | 正确做法 |
|---|---|---|
| `_resolve_user_id(db, user_id)` 回退"第一个小孩"（word.py 遗留） | 家长未传时全记到第一个孩子，多孩数据混串 | 改用 `get_required_kid_id`（写）/ `get_current_kid_id`（读） |
| 请求体里传 `user_id` 当权威 | 与 header 双通道不一致，可被绕过/伪造 | 一律走 `X-Kid-Id` header |
| 硬编码 `user_id=1`（如 assessment 自动补题历史 bug） | 新孩子生成的数据全归 id=1 | 用当前 kid_id 注入 |
| 详情接口不校验归属 | 小孩 A 可看小孩 B 的隐私 | 见 §3 详情模板 |
| `user_id = Column(Integer, default=1)`（star/achievement/reward 旧模型） | default 1 是魔法数，插入即错 | 显式传 kid_id，模型不要给默认值 |

## 7. 新增功能检查清单（每次必过）

- [ ] 新数据属于 A（全局）/ B（按小孩）/ C（家长级）哪一类？
- [ ] B 类：模型有 `user_id NOT NULL + index`，注释「归属小孩（数据隔离）」？
- [ ] B 类写接口：用了 `get_required_kid_id`，且写入值 = kid_id（无硬编码、无 body user_id）？
- [ ] B 类读接口：用了 `get_current_kid_id` + `filter_by_kid`？
- [ ] 详情/单条查询接口：加了归属校验（同 404）？
- [ ] 所有查询过滤 `deleted == False`？
- [ ] 前端没有手动传 user_id？（有特殊需求走 X-Kid-Id 头覆盖）
- [ ] 冒烟测试覆盖：未选孩子写入 → 400；孩子 A/B 数据互不可见？
- [ ] 后端 `python -m py_compile` + 前端 `npm run build` 通过？

## 8. 现状对照（2026-09 评估）

| 模块 | 隔离方式 | 状态 |
|---|---|---|
| practice_set（练习/出卷） | `get_required_kid_id` / `get_current_kid_id` | ✅ 规范 |
| phonics（拼读） | `get_required_kid_id` / `get_current_kid_id` | ✅ 规范 |
| motivation（积分/成就/兑换） | `get_required_kid_id` / `get_current_kid_id` | ✅ 规范 |
| assessment（评测） | 本次改为 kid_context（history/detail=current，start/submit=required） | ✅ 已修复 |
| word（单词复习/错词） | 旧模式：query user_id + `_resolve_user_id` 回退第一个小孩 | ⚠️ 遗留，待迁移 |
| 模型 star_balance / star_record / achievement_progress / redemption | `user_id default=1` 魔法数 | ⚠️ 遗留，建议改为显式传值 |

> 迁移 word.py 与旧模型时：先按 §3 模板改路由（依赖注入），再改模型默认值；
> 涉及已存在的数据，跑一次性迁移脚本把 `user_id=1` 的数据归到真实小孩（参照 `[migrate]` 提示的迁移逻辑）。
