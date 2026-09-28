# DEPLOY_OPS_SYNC — 一键部署增加 ops 权威数据同步（完成）

**背景**：`deploy/remote_deploy.sh` 只在首次部署复制种子主库，此后云端主库保留服务器数据；`deploy.bat skipdb` 时本地主库不进包 → 云端 ops 权威数据（语法教程 44 条 / 激励 star_action 11 / achievement 19 / achievement_config 3）不会更新。用户拍板方案 A：部署时自动幂等同步配置表。

**改动**：
1. 新增 `tools/deploy_export_ops.py`：从本地主库导出 4 张 ops 权威表 → `deploy/ops_data.sql`（按 id `ON CONFLICT(id) DO UPDATE` 幂等 upsert，共 77 条；TABLES 列表可扩展）。
2. 新增 `deploy/ops_data_sync.py`：容器内执行，读 `/data/ops_data.sql`（env `OPS_SQL_FILE` 可覆盖）导入 `DB_PATH` 主库，只动配置表。
3. `deploy/remote_deploy.sh`：健康检查通过后，检测 `deploy/ops_data.sql` 且云端主库存在 → `cp` 到 `$DATA_DIR` → `docker exec easyfix python3 /data/ops_data_sync.py`；失败仅警告不阻断部署，成功后清理 sql 文件。
4. `deploy.ps1`：新增 `[1.5/5] 导出 ops 权威数据` 步骤（打包前调用导出脚本，失败警告不阻断）。

**BOM 处理（坑已踩）**：`edit_file` 修改 deploy.ps1 后 BOM 丢失（NO_BOM）→ 按 AGENTS.md 处方用 `[System.IO.File]::WriteAllText($p,$c,(New-Object System.Text.UTF8Encoding($true)))` 重写回 BOM → `Parser::ParseFile` 零错误 → 复检 `BOM_PRESENT`。

**验证**：
- 导出：`python tools/deploy_export_ops.py` → 77 条 upsert（44/11/19/3）生成 `deploy/ops_data.sql`。
- 模拟云端旧库（复制主库→删 grammar_lesson id>29、删 achievement 最大 id、改 star_action/grammar id=1 内容）→ 容器脚本导入 → 行数恢复 44/11/19/3、id=1 内容还原、star_action 原值恢复。验证脚本 `tools/tmp/verify_ops_sync.py`（已清理）。
- `bash -n deploy/remote_deploy.sh` 通过；deploy.ps1 Parser 零错误 + BOM 在位。

**使用**：正常 `deploy.bat` / `deploy.bat skipdb` 即可，每次部署自动把本地主库最新 ops 配置同步到云端（幂等，不覆盖云端空间/用户/错题数据）。
