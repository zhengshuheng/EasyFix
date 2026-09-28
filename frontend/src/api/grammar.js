import api from './http'

// 语法专项 API
export const grammarApi = {
  // 板块列表（含各板块语法点数与当前小孩已学数）
  categories() {
    return api.get('/grammar/categories')
  },

  // 语法点列表（可按板块/年级过滤，带当前小孩进度）
  lessons(params) {
    return api.get('/grammar/lessons', { params })
  },

  // 语法点详情（含进度）
  get(id) {
    return api.get(`/grammar/lessons/${id}`)
  },

  // 新建语法点（家长管理）
  create(data) {
    return api.post('/grammar/lessons', data)
  },

  // 更新语法点（家长管理，含教程内容）
  update(id, data) {
    return api.put(`/grammar/lessons/${id}`, data)
  },

  // 删除语法点（软删除）
  delete(id) {
    return api.delete(`/grammar/lessons/${id}`)
  },

  // 记录学习/练习进度（按小孩隔离）
  recordProgress(data) {
    return api.post('/grammar/progress', data)
  },

  // AI 生成板块语法点骨架（家长管理，含查重）
  aiGenerateSkeleton(data) {
    return api.post('/grammar/ai-generate-skeleton', data)
  },

  // AI 生成教程（单点或按板块整批）
  aiGenerateTutorial(data) {
    return api.post('/grammar/ai-generate-tutorial', data)
  },

  // 同步官方语法教程（从运营中心主库更新本空间，语法点固化后家长端只读）
  syncTutorials() {
    return api.post('/grammar/sync-tutorials')
  },

  // 生成语法专项练习卷（直接创建练习集）
  generatePractice(data) {
    return api.post('/practice-sets/generate-grammar', data)
  },
}

export default grammarApi
