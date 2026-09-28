import { defineStore } from 'pinia'

// 登录态持久化到 localStorage：刷新页面不丢失
const LS_USER = 'ops_session_username'
const LS_PASS = 'ops_session_password'

export const useSession = defineStore('ops-session', {
  state: () => ({
    username: localStorage.getItem(LS_USER) || '',
    password: localStorage.getItem(LS_PASS) || '',
    logged: !!(localStorage.getItem(LS_USER)),
  }),
  actions: {
    login(username, password) {
      this.username = username
      this.password = password
      this.logged = true
      localStorage.setItem(LS_USER, username)
      localStorage.setItem(LS_PASS, password)
    },
    logout() {
      this.username = ''
      this.password = ''
      this.logged = false
      localStorage.removeItem(LS_USER)
      localStorage.removeItem(LS_PASS)
    },
  },
})
