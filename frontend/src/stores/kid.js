import { defineStore } from 'pinia'

const KID_KEY = 'easyfix_kid'

function loadKid() {
  try {
    return JSON.parse(localStorage.getItem(KID_KEY) || 'null')
  } catch {
    return null
  }
}

/** 当前使用的小孩身份（软件主服务对象） */
export const useKidStore = defineStore('kid', {
  state: () => ({
    kid: loadKid(),
  }),

  getters: {
    activeKid: (s) => s.kid,
    isKidSelected: (s) => !!s.kid,
    kidName: (s) => s.kid?.display_name || s.kid?.username || '',
  },

  actions: {
    select(kid) {
      this.kid = {
        id: kid.id,
        username: kid.username,
        display_name: kid.display_name || kid.username,
        avatar: kid.avatar || null,
      }
      localStorage.setItem(KID_KEY, JSON.stringify(this.kid))
    },
    clear() {
      this.kid = null
      localStorage.removeItem(KID_KEY)
    },
  },
})
