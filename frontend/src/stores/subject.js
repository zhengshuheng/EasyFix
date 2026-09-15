import { defineStore } from 'pinia'
import { questionApi } from '@/api/question'

const SUBJECT_KEY = 'easyfix_active_subject_id'

function loadActiveSubjectId() {
  try {
    const raw = sessionStorage.getItem(SUBJECT_KEY)
    if (raw === null || raw === '') return null
    const n = Number(raw)
    return Number.isNaN(n) ? null : n
  } catch {
    return null
  }
}

/**
 * 学习空间学科（null = 全部/多学科汇总）
 * 阶段A：仅前端壳（列表 + 切换 + 菜单联动）；阶段B 起各页面按 activeSubjectId 过滤数据
 */
export const useSubjectStore = defineStore('subject', {
  state: () => ({
    subjects: [],
    loaded: false,
    activeSubjectId: loadActiveSubjectId(),
  }),

  getters: {
    activeSubject: (s) => s.subjects.find((x) => x.id === s.activeSubjectId) || null,
    isAll: (s) => s.activeSubjectId === null,
    /** 当前空间是否为英语学科（决定「英语▾」子菜单显隐） */
    isEnglish: (s) => {
      const sub = s.subjects.find((x) => x.id === s.activeSubjectId)
      return sub ? sub.name === '英语' : false
    },
  },

  actions: {
    async loadSubjects(force = false) {
      if (this.loaded && !force) return
      try {
        const { data } = await questionApi.listSubjects()
        this.subjects = Array.isArray(data) ? data : data?.items || []
        this.loaded = true
      } catch (e) {
        // 列表加载失败不阻塞页面，稍后重试
        console.error('加载学科列表失败:', e)
      }
    },
    select(id) {
      this.activeSubjectId = id == null ? null : Number(id)
      if (this.activeSubjectId === null) sessionStorage.removeItem(SUBJECT_KEY)
      else sessionStorage.setItem(SUBJECT_KEY, String(this.activeSubjectId))
    },
    reset() {
      this.activeSubjectId = null
      sessionStorage.removeItem(SUBJECT_KEY)
    },
  },
})
