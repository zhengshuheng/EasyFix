import request from './http'

// 能力评测
// 注意：孩子身份走全局 X-Kid-Id 请求头（见 http.js），这里不传 user_id
export const assessmentApi = {
  // 开始评测（生成评测集，返回 record_id）
  start(payload) {
    return request.post('/assessment/start', payload)
  },
  // 评测记录列表（可选按学科过滤）
  list(subjectId) {
    return request.get('/assessment/history', { params: { subject_id: subjectId || undefined } })
  },
  // 提交答案（record_id 为评测集 id；0 为兼容旧流程）
  submit(recordId, payload) {
    return request.post(`/assessment/${recordId || 0}/submit`, payload)
  },
  // 放弃/退出当前评测
  quit(recordId) {
    return request.post(`/assessment/${recordId}/quit`)
  },
  // 评测详情
  detail(id) {
    return request.get(`/assessment/${id}`)
  },
  // ===== 专项评测 =====
  // 学科专项列表（含适用年级）
  specialList(subjectId) {
    return request.get('/assessment/special/list', { params: { subject_id: subjectId } })
  },
  // 开始专项评测（同 start，带 specialty key）
  specialStart(payload) {
    return request.post('/assessment/special/start', payload)
  },
  // 专项评测历史（专项进步曲线数据）
  specialHistory(payload) {
    return request.get('/assessment/special/history', { params: payload })
  },
  // 专项练习：开始（不建评测记录）
  practiceStart(payload) {
    return request.post('/assessment/special/practice/start', payload)
  },
  // 专项练习：提交（判分 + 错题同步，不给等级评级）
  practiceSubmit(payload) {
    return request.post('/assessment/special/practice/submit', payload)
  },
}
