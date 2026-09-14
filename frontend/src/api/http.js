import axios from 'axios'
import { ElMessage } from 'element-plus'

// 共享 axios 实例：所有 API 统一走这里，自动附带登录 token
const api = axios.create({
  baseURL: '/api',
  timeout: 60000,
})

// 请求拦截：从 localStorage 读取 token 并附加到 Authorization 头
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('easyfix_token')
  if (token) {
    config.headers = config.headers || {}
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

// 响应拦截：401 未登录/过期时清理家长会话并回到选择页
api.interceptors.response.use(
  (res) => res,
  (err) => {
    if (err.response && err.response.status === 401) {
      localStorage.removeItem('easyfix_token')
      localStorage.removeItem('easyfix_user')
      if (window.location.pathname !== '/') {
        ElMessage.warning('登录已过期，请重新进入')
        window.location.href = '/'
      }
    }
    return Promise.reject(err)
  }
)

export default api
