# PHONICS_MEMORY_COMPLETE — 自然拼读 + 联想记忆补全
## 现状盘点（已完成）
- [x] 自然拼读：PhonicsPanel 规则库浏览（元音/辅音/不发音e 分类、搜索、AI 生成）+ 示例词喇叭按钮
- [x] 联想记忆：MemoryReviewPanel 口诀猜词卡片流（正翻卡）+ 艾宾浩斯进度（word_progress）
- [x] 后端：/api/phonics 规则库 + /api/words/memory-review + submit

## 根因（用户反馈）
- [x] 自然拼读"没有读音"：/api/words/audio 先查词库，示例词（bee/cake/bike）不在词库直接 404，不走 TTS → 喇叭无声
- [x] 自然拼读"没有练习"：只有规则浏览，无练习题
- [x] 联想记忆"没有归类"：卡片流不按词根/类别组织
- [x] 联想记忆"没有练习、不便记忆"：只有口诀猜词一种形式，无反向/错词重练/统计

## 阶段一（读音修复 + 后端）
- [x] word_memory.py /api/words/audio：词不在词库时直接 TTS 生成（不再 404）
- [ ] 冒烟验证：bee/cake/bike 返回 200 音频（需重启后端后测）

## 阶段二（自然拼读练习，前端 PhonicsPanel）
- [x] PhonicsPanel 增加「浏览 / 练习」模式切换
- [x] 练习1 听音选词：播放示例词发音 → 4 选 1 正确拼写
- [x] 练习2 组合判断：看词选组合（pattern 4 选 1）
- [x] 结果统计 + 错题重练

## 阶段三（联想记忆归类+练习增强，前端 MemoryReviewPanel）
- [x] 前端按 word_root 词根分组（后端 items 已含 word_root，无需后端改）
- [x] MemoryReviewPanel 顶部分组选择（全部/各词根分组）
- [x] 模式切换：口诀猜词（正向）/ 看词想口诀（反向）
- [x] 错题重练（本轮内收集 + 结束后重练错题按钮） + 本轮对错统计
