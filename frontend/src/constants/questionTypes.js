// 题型分值/名称/大题顺序（与后端 PDF 一致，参考学校试卷）
// 由 PracticeSets.vue 拆出题弹窗时抽取，供列表/做题/详情/出题多处共用
export const QUESTION_TYPE_SCORES = { choice: 3, fill: 3, judge: 2, calc: 4, application: 6, operation: 5, reading: 4, writing: 10, sentence: 2 }
export const QUESTION_TYPE_NAMES = { choice: '选择题', fill: '填空题', judge: '判断题', calc: '计算题', application: '应用题', operation: '操作实践题', reading: '阅读理解', writing: '写话·习作', sentence: '连词成句' }
export const QUESTION_TYPE_ORDER = ['choice', 'fill', 'judge', 'calc', 'application', 'operation', 'reading', 'writing', 'sentence']
