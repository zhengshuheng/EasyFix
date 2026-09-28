# E2E 浏览器测试代码块（运营后台）

> 用途：启动 `tools\e2e_ops_test.bat`（服务 + 浏览器）后，
> 把下面的代码块整体复制到 browser 工具运行，即可快速完成运营后台冒烟。
> 每次改动后按需增删验证点；遇到 locator 报错先 snapshot() 看实际页面。

```python
browser = await Browser.connect()
page = await browser.open("http://localhost:8012/site/ops.html")
await page.wait_for_load_state("load")

# 1) 登录（双因子：admin / easyfix-ops）
await page.locator("#opsUsernameInput").fill("admin")
await page.locator("#opsPasswordInput").fill("easyfix-ops")
await page.get_by_role("button", name="进入后台 →").click()
await page.wait_for_timeout(1500)

# 2) 一级导航
navs = await page.locator(".ops-nav").all_text_contents()
print("一级导航:", navs)  # 期望：📚 教材数据 / ⚙️ 系统配置 / ↩ 退出登录

# 3) 知识点列表（默认面板）加载
await page.wait_for_timeout(1000)
rows = await page.locator(".ops-table tbody tr").count()
print("知识点行数:", rows)

# 4) 切换单词面板（若当前导航是两级，先展开教材数据）
# await page.get_by_role("button", name="单词管理").click()
# await page.wait_for_timeout(800)
# print("单词行数:", await page.locator(".ops-table tbody tr").count())

# 5) AI 导入弹窗（数据管理面板）
await page.locator("#dataAiImport").click()
await page.wait_for_timeout(600)
print("AI 弹窗可见:", await page.locator("#aiImportModal").is_visible())
print("AI 标题:", await page.locator("#aiTitle").inner_text())
await page.locator("#aiImportModal .ops-modal-close").click()
await page.wait_for_timeout(300)

# 6) 批量导入弹窗（数据管理面板）
await page.locator("#dataBatchImport").click()
await page.wait_for_timeout(600)
print("批量弹窗可见:", await page.locator("#batchModal").is_visible())
print("批量模式:", await page.locator("#batchMode option").all_text_contents())
await page.locator("#batchModal .ops-modal-close").click()

# 7) 配置表单（系统设置面板）
# await page.get_by_role("button", name="系统设置").click()
# await page.wait_for_timeout(500)
# print("配置面板可见:", await page.locator("#configPanel").is_visible())
```

## 常见验证点（按功能）

- **AI 导入**：选科目/版本 → 输入示例 → 生成 → 预览勾选 → 导入运营主库
- **批量导入**：文本粘贴 / 文件上传 / 图片识别（单词）
- **导出 CSV**：选好筛选 → 导出按钮 → 响应为 text/csv
- **版本管理**：新建版本 → catalog 出现 → 停用 → 列表标记
- **用户管理**：新增管理员 → 新账号登录 → 禁用 → 401
- **权限**：editor 登录后看不到用户/权限管理

## 注意

- 官网静态文件实时读盘，改 ops 前端无需重启服务，刷新即可
- 后端改动需跑 `tools\e2e_ops_test.bat`（或 `一键重启.bat`）重启 8012
- 测试产生的数据走真实 SQLite，测完执行 `python tools/cleanup.py` 并清理测试记录
