import { defineStore } from 'pinia'
import { currentTrialKey } from '@/api/http'

/**
 * 空间订阅/体验状态（/api/trial/status，X-Trial-Key 由 URL 解析自动带）。
 *
 * 路由守卫每次导航前保证 statusLoaded：刷新页面即重新校验到期。
 * trial_end_at=NULL = 正式版（is_pro=true，永不过期，如 easyfix_demo 调试空间）。
 * expired=true → 路由守卫拦截跳 /subscribe 续费页。
 */
export const useTrialStore = defineStore('trial', {
  state: () => ({
    statusLoaded: false,
    loadFailed: false,
    is_pro: false,
    expired: false,
    days_left: null,
    expires_at: null,
    trial_days: null,
    space_username: '',  // 空间主账号（官网注册家长），家长中心不可删除
    config: {},
  }),

  actions: {
    async loadStatus() {
      if (this.statusLoaded) return
      try {
        const key = currentTrialKey()
        const res = await fetch('/api/trial/status', {
          headers: { 'X-Trial-Key': key },
        })
        if (res.ok) {
          const data = await res.json()
          const t = data.trial || {}
          this.is_pro = !!t.is_pro
          this.expired = !!t.expired
          this.days_left = t.days_left
          this.expires_at = t.expires_at
          this.trial_days = t.trial_days
          this.space_username = data.space?.username || ''
          this.config = data.config || {}
        }
      } catch (e) {
        this.loadFailed = true
      } finally {
        this.statusLoaded = true
      }
    },
  },
})
