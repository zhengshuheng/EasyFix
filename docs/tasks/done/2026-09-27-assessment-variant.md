# 2026-09-27 评测举一反三出题（assessment-variant）

## 需求
- 出题不应按库存题目直接出：库存只是参考，应举一反三；库存不足则按知识点+评测要求生成，确保质量可靠
- 连续切换不同级别的卷子，第一题都一模一样（体验不友好）
- 出题依据不仅是已有的错题集

## 改动
- `backend/app/routers/assessment.py`
  - `_auto_refill` 新增 `avoid_stems` 参数（近期题干集合透传 LLM，源头防撞）
  - 每次 start 生成 2 道变式（`VARIANT_COUNT - generated`），难度按卷型 standard=3/challenge=4/explore=5
  - 错题知识点加权：`_pool_key` 新增错题本（`ErrorQuestion` 未掌握）知识点前置项
  - pool 排序前先 `random.sample` 打乱输入（同优先级内随机）；卷内 `random.shuffle(sampled)`
  - 分档补题 `tier_avail` 扣除 `excluded_ids`（排除后缺口才准确）
  - `_recent_done_question_ids` 返回 `(ids, stems)`，排重覆盖 done/in_progress/quit 且按 id+题干双维度
- `backend/app/services/llm.py`
  - `generate_questions_by_knowledge` / `_generate_raw` / `_build_question_gen_prompt` / `_quality_topup` 新增 `avoid_stems` 透传
  - prompt 新增【严禁重复】段：列出近期题干，严禁相同题干或只改数字/人名的相似题

## 验证
- 9 卷连续切卷（standard/challenge/explore × 3 轮）互相 0 重叠，第一题各不相同
- 测试数据已清理（12 条 in_progress/quit 记录、2 道重复题干题），库存 120 道
- 服务已重启（计划任务 EasyFixBackend）

## 二修（用户实测再报："看图列式：小鸡一共有（　）只（个）。"无图）
- 根因：旧版 `pictorial_math._fill_stem` sum 分支生成无数字题干 + `_ensure_pictorial_questions` 绕过 sanitize 入库 + 旧模板题 visual=None
- 修复：① sum 分支题干带数量（自包含）；② `_ensure_pictorial_questions` 入库前过滤（看图列式必带数字 + visual 必有效）；③ 组卷 `_take` 防线（无数字且非 count-split 跳过）；④ 存量软删 40 条（SvXXG4zukMip0A/xSKrVxSi8MX8ow 各 20）
- 修复过程中踩坑：assessment.py 漏 `import re` → 500，已补
- 验证：SvXXG4zukMip0A（kid=3）+ easyfix_demo（kid=2）start 均 0 坏题、10 题正常、自动生成 4 道变式

## 三修（用户要求：即使来自题库也需校验坏题过滤）
- `_take` 新增 `_is_bad_question(qq)` 通用坏题校验（题干空/答案空/choice 选项<2/看图列式无数字无图），`_take` 与兜底循环都调用
- 模型字段坑：PracticeQuestion 无 options 属性（选项在 option_a/b/c/d 四列）
- 实测：注入 3 类坏题（id=807/808/809）全部被过滤，卷中 0 出现；单测 10/10 通过；测试数据已清理

## 后续
- 用户强刷验收：切卷子第一题/题面均不同、每次评测有新变式
