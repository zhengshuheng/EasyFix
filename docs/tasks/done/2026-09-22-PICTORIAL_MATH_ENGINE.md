# PICTORIAL_MATH_ENGINE — 低年级图示算式模板引擎（1-2年级）

## 决策依据（课标研究）
- 2022 版课标第一学段 = 1-2 年级；"利用画图、实物操作等方法表达情境中的数量关系，体会几何直观"（教学提示原文）
- 台湾课纲 N-1-2：一年级不做加数/被减数未知题型；N-2-3 二年级才引入未知数
- 三年级起进入第二学段（万以内/多位数乘除），图例骤减 → 不做图示算式
- 故范围：1 年级=看图列式；2 年级=未知数填空+乘法 group 图

## 计划
- [x] 后端模板引擎 backend/app/services/pictorial_math.py（确定性生成，动物emoji×算式模板）
- [x] 评测 start 接入：数学1-2年级 _ensure_pictorial_questions 保证图示题足量（入库 source=template）
- [x] 组卷排序：图示题最优先但占比限制 count//2（图文混排），修复 application 先取满导致图示题抽不中的 bug
- [x] SceneVisual.vue 支持 count-split（左右两堆+运算符+等号+问号；乘法 group 盒子）
- [x] 判分：decompose 分解题任意两数和=N 即对（_check_decompose）；前端答案显示友好文本
- [x] 冒烟：1年级 8题含2图题/2年级含4图题，判分 8/8；vite build 通过
- [x] 归档任务文档

## 验证证据
- 模板引擎自测：sum/addend_left/addend_right/minuend/subtrahend/decompose/mul_sum 全部生成正常
- 题库：grade1 11 道（sum）、grade2 11 道（mul_sum 5/decompose 3/addend* 2/subtrahend 1）
- 评测 start：grade1 8题含2图题、grade2 8题含4图题；submit 8/8 优秀
- decompose 判分：'3和4'/'1,6'/'3+4' → True；'5'/'8'/'' → False
- npm run build → BUILD_OK

## 设计
visual 新类型 `count-split`：
{"type":"count-split","left_emoji":"🐤","left_count":3,"right_emoji":"🐤","right_count":4,
 "operator":"+","unknown":"sum","label":"小鸟","max_count":7}
unknown ∈ {sum, addend_left, addend_right, minuend, subtrahend, decompose, mul_sum}

