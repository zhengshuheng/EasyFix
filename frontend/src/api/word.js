import api from './http'

// 单词相关API
export const wordApi = {
  // 获取单词列表
  list(params) {
    return api.get('/words', { params })
  },

  // 获取单词详情
  get(id) {
    return api.get(`/words/${id}`)
  },

  // 创建单词
  create(data) {
    return api.post('/words', data)
  },

  // 更新单词
  update(id, data) {
    return api.put(`/words/${id}`, data)
  },

  // 删除单词
  delete(id) {
    return api.delete(`/words/${id}`)
  },

  // 获取单词统计
  getStats(params) {
    return api.get('/words/stats/summary', { params })
  },

  // 开始复习
  startReview(params) {
    return api.post('/words/review/start', null, { params })
  },

  // 提交复习结果
  submitReview(data) {
    return api.post('/words/review/submit', data)
  },

  // 获取错词列表
  getErrors(params) {
    return api.get('/words/errors', { params })
  },

  // 生成打印PDF
  printPdf(params) {
    return api.post('/words/print-pdf', null, { params })
  },

  // 获取单词记忆曲线
  getMemoryCurve(wordId, params) {
    return api.get(`/words/${wordId}/memory-curve`, { params })
  },

  // 教材单词表提取（多图/PDF → OCR + AI）
  extractFromTextbook(formData) {
    return api.post('/words/extract-from-textbook', formData)
  },

  // AI 智能导入：大模型生成单词表（textbook / custom）
  aiGenerate(data) {
    return api.post('/words/ai-generate', data)
  },

  // AI 批量生成记忆增强（拼读规则/词根词源/相关词/语境例句）
  enhance(data) {
    return api.post('/words/enhance', data)
  },
}

export default wordApi
