# SCENE_GOVERN — 图例治理：校验+占比+年级降频
- [x] A: _validate_scene() 校验 LLM 自带 visual（单位/乘法/未知数/触发词/数字一致性）非法回退
- [x] D: detect_scene 题型过滤（calc/judge 不配图）
- [x] C: detect_scene 年级阶梯（3年级仅shape、2年级去count示意、1年级全量）
- [x] B: 评测组卷图题占比 ≤50% 覆盖全部图型
- [x] prompt: 3年级以上 LLM 少生成 visual
- [x] 测试用例扩展 + 全库校验 + build
