import api from './question.js'

// 学习分析API
export const learningAnalysisApi = {
  // 获取完整分析数据
  getFullStats() {
    return api.get('/stats/analysis/full')
  },

  // 获取LLM分析
  getLlmAnalysis() {
    return api.post('/stats/analysis/llm', {})
  },
}

export default learningAnalysisApi