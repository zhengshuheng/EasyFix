import { defineStore } from 'pinia'
import { authApi } from '@/api/auth'

const TOKEN_KEY = 'easyfix_token'
const USER_KEY = 'easyfix_user'

function loadUser() {
  try {
    return JSON.parse(localStorage.getItem(USER_KEY) || 'null')
  } catch {
    return null
  }
}

/** 登录态与角色：家长(admin) / 小孩(child) */
export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem(TOKEN_KEY) || '',
    user: loadUser(),
  }),

  getters: {
    isLoggedIn: (s) => !!s.token,
    role: (s) => s.user?.role || '',
    isAdmin: (s) => s.user?.role === 'admin',
    isChild: (s) => s.user?.role === 'child',
    displayName: (s) => s.user?.display_name || s.user?.username || '未登录',
  },

  actions: {
    async login(payload) {
      const { data } = await authApi.login(payload)
      this.token = data.token
      this.user = data.user
      localStorage.setItem(TOKEN_KEY, data.token)
      localStorage.setItem(USER_KEY, JSON.stringify(data.user))
      return data
    },

    /** 刷新当前用户信息（校验 token 是否仍有效） */
    async refreshMe() {
      if (!this.token) return null
      const { data } = await authApi.me()
      this.user = data
      localStorage.setItem(USER_KEY, JSON.stringify(data))
      return data
    },

    logout() {
      this.token = ''
      this.user = null
      localStorage.removeItem(TOKEN_KEY)
      localStorage.removeItem(USER_KEY)
    },
  },
})
