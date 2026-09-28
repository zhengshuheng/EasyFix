import api from './http'

// 空间数据同步：从主库 Ops 仓库一键同步教材数据（全量替换、幂等）
export const syncApi = {
  // 同步状态 + Ops 目录（可同步的 科目/版本/册次 及其数据量）
  status() {
    return api.get('/sync/status')
  },
  // 一键同步某科目某版本全部年级知识点
  syncKp(data) {
    return api.post('/sync/knowledge-points', data)
  },
  // 一键同步某版本 1-6 年级全部英语单词
  syncWordsAll(data) {
    return api.post('/sync/words-all', data)
  },
}
