import api from './question.js'

/** 显式指定小孩 id（家长中心选小孩操作时用，覆盖默认 localStorage 孩子） */
function kidHeader(kidId) {
  const headers = {}
  if (kidId) headers['X-Kid-Id'] = String(kidId)
  return { headers }
}

export const motivationApi = {
  // 积分
  getBalance(options = {}) {
    const { kid_id } = options
    return api.get('/stars/balance', kidHeader(kid_id))
  },
  getRecords(params = {}) {
    const { kid_id, ...rest } = params
    // 显式传 kid_id：积分明细跟随「当前选择的小孩」，不依赖 localStorage 隐式头
    // （否则缺头时后端 _kid_or_first 兜底返回空间第一个小孩的记录，切小孩后明细错位）
    return api.get('/stars/records', { params: rest, ...kidHeader(kid_id) })
  },
  getActions() {
    return api.get('/stars/actions')
  },

  // 家长（空间）保存激励自定义：行为积分值 / 成就触发次数 / 成就奖励积分
  saveIncentiveSettings(data) {
    return api.put('/incentive-settings', data)
  },

  // 成就
  getAchievements() {
    return api.get('/achievements')
  },
  getAchievementProgress(options = {}) {
    const { kid_id } = options
    return api.get('/achievements/progress', kidHeader(kid_id))
  },

  // 奖励
  getRewards() {
    return api.get('/rewards')
  },
  createReward(data) {
    return api.post('/rewards', data)
  },
  updateReward(id, data) {
    return api.put(`/rewards/${id}`, data)
  },
  deleteReward(id) {
    return api.delete(`/rewards/${id}`)
  },
  redeemReward(id) {
    return api.post(`/rewards/${id}/redeem`)
  },
  getRedemptions(options = {}) {
    const { kid_id } = options
    return api.get('/rewards/redemptions', kidHeader(kid_id))
  },

  // 概览（积分余额/今日获取：显式跟随当前小孩，避免缺头兜底第一个小孩）
  getOverview(options = {}) {
    const { kid_id } = options
    return api.get('/motivation/overview', kidHeader(kid_id))
  },

  // 积分调整（家长中心：需显式指定小孩）
  adjustStars(data) {
    const { kid_id, ...body } = data
    return api.post('/stars/adjust', body, kidHeader(kid_id))
  },

  // 每日签到
  checkin() {
    return api.post('/motivation/checkin')
  },

  // 单词复习正确率触发
  triggerWordAccuracy(data) {
    return api.post('/motivation/trigger/review_word_accuracy', data)
  }
}