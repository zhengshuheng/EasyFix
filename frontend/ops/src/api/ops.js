import axios from 'axios'
import { useSession } from '../stores/session.js'
import { ElMessage } from 'element-plus'

// 运营后台 API 客户端：凭证经 X-Ops-* 头传递（双因子）
export function opsApi() {
  const s = useSession()
  const client = axios.create({
    baseURL: '/api/ops',
    headers: { 'X-Ops-Username': s.username, 'X-Ops-Password': s.password },
  })
  client.interceptors.response.use(
    (r) => r.data,
    (e) => {
      const detail = e.response?.data?.detail
      ElMessage.error(typeof detail === 'string' ? detail : (e.message || '请求失败'))
      return Promise.reject(e)
    }
  )
  return client
}

export function opsCatalog() {
  return opsApi().get('/catalog')
}

export function opsPromptRules() {
  return opsApi().get('/prompt-rules')
}

export function opsSavePromptRules(rules) {
  return opsApi().put('/prompt-rules', { rules })
}

export function opsAssessRules() {
  return opsApi().get('/assess-rules')
}

export function opsSaveAssessRules(rules) {
  return opsApi().put('/assess-rules', { rules })
}

export function opsIncentiveRules() {
  return opsApi().get('/incentive-rules')
}

export function opsSaveIncentiveRules(payload) {
  return opsApi().put('/incentive-rules', payload)
}

// ---------------- 语法教程（主库 ops 权威） ----------------

export function opsGrammarLessons(params) {
  return opsApi().get('/grammar/lessons', { params })
}

export function opsGrammarLesson(id) {
  return opsApi().get(`/grammar/lessons/${id}`)
}

export function opsGrammarSave(id, data) {
  return opsApi().put(`/grammar/lessons/${id}`, data)
}

export function opsGrammarAiGenerate(data) {
  return opsApi().post('/grammar/ai-generate', data)
}

export function opsGrammarSyncTenants() {
  return opsApi().post('/grammar/sync-tenants')
}
