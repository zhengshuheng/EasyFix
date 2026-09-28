# 2026-09-26 密码重置 + 练习端浏览器验证与修复

## 背景
- easyfix_demo 家长账号 zhengshuheng_demo 密码未知（哈希不可逆，候选全 False），评测端与练习端浏览器验证被卡在登录
- 用户授权方案 B：重置密码为 `Easyfix@2026`

## 已完成
1. **密码重置**：`users(id=1)` password_hash 用 `auth.hash_password('Easyfix@2026')` 重写；登录 API 200 验证通过
   - 新密码：`Easyfix@2026`（8–20 位、含字母数字大小写+符号，满足复杂度规则）
2. **评测端浏览器验证**（修复后首次全流程）：
   - 登录→选体验小朋友（2年级）→ 数学→评测
   - 评测设置页「🔊 自动读题」开关存在且 2 年级默认开（checked=true）
   - 答题页：🔊 读题按钮、低年级 fillTip「填数字就行，不用写单位（填完按回车确认）」、placeholder「输入数字后按回车确认」
   - 填数字不带单位提交 → 「✅ 答对了！」满分（低年级忽略单位生效）
   - SceneVisual 图文场景（🍬 糖果组图）渲染正常
3. **练习页白屏修复**（用户控制台报错 `ReferenceError: watch is not defined`）：
   - 根因：`frontend/src/views/PracticeSets.vue` `<script setup>` 用了 `watch()` 但 import 只导入了 `ref, reactive, computed, onMounted, nextTick`，漏了 `watch`
   - 修复：import 行补 `watch`；重新 build:trial
4. **练习端低年级判定修复**：
   - 根因：`practice_set` 表无 grade 列，详情接口不返回 grade → `openStudentDo` 里 `ps.grade=undefined` → `isLowGradeMathDo=false` → 低年级 placeholder/fillTip/自动带读全失效
   - 修复：后端 `practice_set.py` 详情接口从题目快照取第一个非空 grade 返回（`grade` 字段），`PracticeSetResponse` 加 `grade: Optional[int]`；`pairs=[]` 提前初始化防 word/reading 分支 NameError
   - 前端 `openStudentDo` 用 `data.grade ?? ps.grade` 覆盖
5. **练习端浏览器验证**（临时数据，已清理）：
   - 临时给体验小朋友插入练习集（5 道二年级数学题，后换为 158 苹果+香蕉/桃子场景题）验证做题弹层
   - 「🔊 自动读题」开关默认开；顶部「🔊」全部朗读按钮；每题 🔊
   - 低年级 placeholder「填数字就行（可点右边麦克风语音输入）」+ fillTip「填数字就行，不用写单位（填完按回车确认）」生效
   - SceneVisual 🍎 图文场景（左 8 个+右 9 个）渲染正常
   - 排查并修掉：测试练习集 `reviewed/review_count=NULL` 导致详情 500（Pydantic bool/int 校验）——仅手动 INSERT 才触发，正式创建路径有默认值
6. **清理**：临时练习集（practice_set id=1 + 关联）、测试评测记录（assessment_record id=1）、临时 JSON/脚本/根目录截图

## 遗留 / 注意
- 当前 8012 服务为**手动后台进程**（pid 29492，日志 tools/tmp/uvicorn_manual.log）；计划任务 EasyFixBackend 为一次性触发（被我 taskkill 后未自动拉起）。如需恢复计划任务托管，运行 `schtasks /run /tn EasyFixBackend`（注意其日志写入 tools/tmp/uvicorn.log 会被手动进程占用而失败）或一键部署脚本重启
- 用户浏览器需 Ctrl+F5 强刷加载新 dist-trial（PracticeSets-84db4cbf.js）
- 账号 zhengshuheng_demo / 密码 `Easyfix@2026`（临时密码，用户可自行修改）
