# 2026-09-27 出题规则集成运营中心（Prompt 可维护）

## 背景
- 出题规则（prompt）硬编码在 `question_prompts.py` 常量与 `llm.py` f-string 里，改规则必须改代码重启
- 用户要求集成到运营中心，便于维护管理、保障出题质量

## 已完成
1. **新表 `ops_prompt_rule`**（主库，`backend/app/models/ops_data.py`）：scope → rule_text（Text 无长度限制），`ensure_ops_tables` 自动建表
   - scope 约定：`general`（通用规则段）/ `base:科目`（科目基础段）/ `style:科目:学段`（学段真题段）
2. **新服务 `backend/app/services/prompt_rules_service.py`**：
   - `DEFAULT_GENERAL_RULES`：内置通用规则（看图列式必带数量 / 计算准确 / 难度标注 / 变式要求）
   - `SCOPE_META`：12 个 scope 元数据（标题/分组/提示，前端渲染用）
   - `load_prompt_rule_map()`：读 DB 已启用规则（表不存在/失败返回 {}，默认兜底）
   - `get_scope_default_text(scope)`：内置默认文本
3. **出题链路读配置**：
   - `question_prompts.py` `get_subject_stage_prompt(subject, grade, overrides=None)`：overrides 按 `base:科目`/`style:科目:学段` 覆盖默认
   - `llm.py` `_build_question_gen_prompt`：`load_prompt_rule_map()` → general 规则段替换硬编码固定段 + subject_guide 传 overrides
4. **运营 API**（`backend/app/routers/ops_data_router.py`）：
   - `GET /api/ops/prompt-rules`：12 scope 全量（DB 值 + 默认值 + is_default 标记）
   - `PUT /api/ops/prompt-rules`：批量保存；空文本 或 与内置默认一致 → 删除记录恢复默认
5. **运营前端**：
   - `frontend/ops/src/views/PromptRulesManage.vue`：通用规则大 textarea + 学科×学段折叠面板（数学/语文/英语/通用分组）+ 保存/恢复全部默认
   - `OpsLayout.vue` 系统配置菜单加「▸ 出题规则」；`router.js` 加 `/prompt-rules` 路由
   - `npm run build:ops`（cd frontend）构建成功（dist-ops/index-c4f378e1.js）

## 验证（全部通过）
- Python 语法编译 OK；模块导入 OK
- API：GET 12 scope 全默认 → PUT 测试规则 → GET 已保存（default: False）→ 链路注入 → 恢复默认（default: True）
- **核心链路**：`load_prompt_rule_map()` 返回测试规则 → `get_subject_stage_prompt('数学',2,overrides)` 含覆盖段 → `LLMService._build_question_gen_prompt` prompt 含测试 general + base:数学 规则
- **浏览器端到端**：运营后台登录 → 系统配置 → 出题规则页渲染（通用规则全文 + 学科折叠面板）→ 编辑保存 → 标签变「已自定义」+ API 确认入库 → 清空保存恢复「内置默认」→ 刷新全 13 个「内置默认」标签
- 测试数据已清理（ops_prompt_rule 清空，恢复全默认）

## 补充（用户要求改为按科目 tab 维护，已完成）
- `PromptRulesManage.vue` 由折叠面板改为 **el-tabs**：🧾 通用（通用出题规则 + 默认科目基础段）/ 数学 / 语文 / 英语（各科 科目基础段 + 学段真题段）
- 保存/恢复全部默认逻辑不变；`npm run build:ops` 构建成功
- 浏览器验证：tab 切换显示正确（数学 4 段、英语 3 段、语文 3 段）；编辑保存 → 已自定义；清空保存 → 恢复内置默认
- **服务已重启**（schtasks /end + /run，pid 26044）：后端 PUT「与内置默认一致的文本按恢复默认处理」修复已生效——浏览器实测：保存与默认相同的文本后仍 0 个「已自定义」（不再存默认副本）

## 补充（数学专属规则拆分，用户指出看图列式/计算准确是数学规范）
- `prompt_rules_service.py` `DEFAULT_GENERAL_RULES` 裁剪为仅【难度标注】【变式要求】（各学科通用）；general tip 同步更新
- `question_prompts.py` `MATH_BASE`【质量硬性要求】追加第 6 条【看图列式必带数量】、第 7 条【计算准确】（数学专属）
- 服务已重启（pid 12848）；验证：API GET general 默认不含看图列式/计算准确、base:数学 含；出题链路 `_build_question_gen_prompt`——数学 prompt 含看图列式/计算准确、语文/英语不含（通用难度标注仍保留）；浏览器精确验证通用 tab textarea 无看图列式/计算准确、数学 tab 有

## 遗留 / 注意
- 服务当前为计划任务 EasyFixBackend 托管（pythonw + uvicorn 8012，日志 tools/tmp/uvicorn.log）
- 前端 dist-ops 已构建，静态读盘无需重启
- 运营后台双因子：账号 `admin` 口令 `easyfix-ops`（X-Ops-Username / X-Ops-Password）
