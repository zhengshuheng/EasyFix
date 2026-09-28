import axios from 'axios'
import { ElMessage } from 'element-plus'

const KID_KEY = 'easyfix_kid'
const TRIAL_KEY = 'easyfix_trial_key'

/** 当前选中的孩子 id（主页/顶栏选择后写入 localStorage） */
export function currentKidId() {
  try {
    const kid = JSON.parse(localStorage.getItem(KID_KEY) || 'null')
    return kid && kid.id ? kid.id : null
  } catch {
    return null
  }
}

/** 试用空间 key（URL /{key}/ 优先解析；无则回退 localStorage，兼容官网跳转前瞬间）

 * 架构统一后空间 SPA 部署在 /{key}/ 下，URL 即真相；localStorage 全局共享，
 * 多空间/直达 /{key}/ 时可能残留别的 key（曾导致 API 打到别的空间）。
 */
export function currentTrialKey() {
  const m = window.location.pathname.match(/^\/([^/]+)\//)
  if (m && m[1]) return m[1]
  return localStorage.getItem(TRIAL_KEY) || ''
}

/** 统一注入 token 与当前孩子标识（后端据此做按小孩数据隔离） */
function injectHeaders(config) {
  config.headers = config.headers || {}
  const token = localStorage.getItem('easyfix_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  const kidId = currentKidId()
  // 调用方显式指定的 X-Kid-Id（如家长中心选小孩调整积分）优先，不被 localStorage 覆盖
  if (kidId && !config.headers['X-Kid-Id']) config.headers['X-Kid-Id'] = String(kidId)
  // 试用空间：后端 middleware 按 X-Trial-Key 切换到该用户独立 db
  const trialKey = currentTrialKey()
  if (trialKey) config.headers['X-Trial-Key'] = trialKey
  return config
}

/**
 * 原生 fetch 专用请求头：Authorization + X-Kid-Id + X-Trial-Key。
 * 裸 fetch 不带租户头会落到主库（曾导致空间内「今日任务/已学会的词/联想记忆」
 * 错读主库 demo 数据、练习记录写错库，见 AI_CONTEXT 单词分级空数据教训）。
 * 调用方显式传入的 headers（如指定的 X-Kid-Id）优先，不被覆盖。
 */
export function apiHeaders(extra = {}) {
  const headers = { ...extra }
  const token = localStorage.getItem('easyfix_token')
  if (token) headers.Authorization = `Bearer ${token}`
  const kidId = currentKidId()
  if (kidId && !headers['X-Kid-Id']) headers['X-Kid-Id'] = String(kidId)
  const trialKey = currentTrialKey()
  if (trialKey && !headers['X-Trial-Key']) headers['X-Trial-Key'] = trialKey
  return headers
}

// 共享 axios 实例：所有 API 统一走这里，自动附带登录 token
const api = axios.create({
  baseURL: '/api',
  timeout: 60000,
})

// 请求拦截：从 localStorage 读取 token 并附加到 Authorization 头
api.interceptors.request.use((config) => injectHeaders(config))

// 各页面直接 import axios 发出的请求（如阅读理解、练习历史）也带上当前孩子 + 租户 key：
// - 缺 X-Kid-Id 会被写入类接口判成"未选孩子"
// - 缺 X-Trial-Key 会落到主库（曾导致空间内「生成短文」写进 easyfix_main.db，空间列表看不到）
axios.interceptors.request.use((config) => {
  config.headers = config.headers || {}
  const kidId = currentKidId()
  if (kidId) {
    config.headers['X-Kid-Id'] = String(kidId)
  }
  const trialKey = currentTrialKey()
  if (trialKey && !config.headers['X-Trial-Key']) {
    config.headers['X-Trial-Key'] = trialKey
  }
  return config
})

// 响应拦截：
// - 带 token 请求返回 401 → token 失效，清家长会话并回选择页
// - 未带 token 的 401（如小孩会话访问家长接口）→ 不跳转，由调用方处理
api.interceptors.response.use(
  (res) => res,
  (err) => {
    const reqHadToken = !!err.config?.headers?.Authorization
    if (err.response && err.response.status === 401 && reqHadToken) {
      localStorage.removeItem('easyfix_token')
      localStorage.removeItem('easyfix_user')
      const trialKey = currentTrialKey()
      if (trialKey) {
        // 试用空间：token 失效则回到试用入口（重新注册/登录）
        ElMessage.warning('请重新进入试用空间')
        window.location.href = '/' + trialKey + '/'
      } else if (window.location.pathname !== '/') {
        ElMessage.warning('家长登录已过期，请重新验证')
        window.location.href = '/'
      }
    }
    return Promise.reject(err)
  }
)

export default api
