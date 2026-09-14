import api from './http'

// 认证 API：家长(用户名+密码) / 小孩(用户名+PIN)
export const authApi = {
  login(data) {
    return api.post('/auth/login', data)
  },
  me() {
    return api.get('/auth/me')
  },
}
