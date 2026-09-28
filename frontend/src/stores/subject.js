import { defineStore } from 'pinia'
import { questionApi } from '@/api/question'

const SUBJECT_KEY = 'easyfix_active_subject_id'
const GRADE_KEY = 'easyfix_active_grade'
const GRADE_TOUCHED_KEY = 'easyfix_grade_touched'

function loadGradeTouched() {
  try {
    return sessionStorage.getItem(GRADE_TOUCHED_KEY) === '1'
  } catch {
    return false
  }
}

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

function loadActiveGrade() {
  try {
    const raw = sessionStorage.getItem(GRADE_KEY)
    if (raw === null || raw === '') return null
    const n = Number(raw)
    return Number.isNaN(n) ? null : n
  } catch {
    return null
  }
}

/**
 * 学习空间（null = 全部/汇总）
 * 空间 = 小孩 + 学科 + 年级：各页面按 activeSubjectId / activeGrade 过滤数据
 */
export const useSubjectStore = defineStore('subject', {
  state: () => ({
    subjects: [],
    loaded: false,
    activeSubjectId: loadActiveSubjectId(),
    activeGrade: loadActiveGrade(),
    /** 用户是否显式选过年级（含"全部年级"）：选过之后不再用配置默认年级覆盖 */
    gradeTouched: loadGradeTouched(),
  }),

  getters: {
    activeSubject: (s) => s.subjects.find((x) => x.id === s.activeSubjectId) || null,
    isAll: (s) => s.activeSubjectId === null,
    /** 年级是否为全部 */
    isAllGrade: (s) => s.activeGrade === null,
    activeGradeName: (s) => (s.activeGrade === null ? '全部年级' : `${s.activeGrade}年级`),
    /** 当前空间是否为英语学科（决定「英语▾」子菜单显隐） */
    isEnglish: (s) => {
      const sub = s.subjects.find((x) => x.id === s.activeSubjectId)
      return sub ? sub.name === '英语' : false
    },
    /** 空间是否涉及英语单词：全部学科 或 英语学科 时显示单词相关 */
    showWordStats: (s) => {
      const sub = s.subjects.find((x) => x.id === s.activeSubjectId)
      if (!sub) return true
      const name = sub.name || ''
      return name === '英语'
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
    setGrade(grade, { markTouched = true } = {}) {
      this.activeGrade = grade == null || grade === '' ? null : Number(grade)
      if (this.activeGrade === null) sessionStorage.removeItem(GRADE_KEY)
      else sessionStorage.setItem(GRADE_KEY, String(this.activeGrade))
      if (markTouched) {
        this.gradeTouched = true
        sessionStorage.setItem(GRADE_TOUCHED_KEY, '1')
      }
    },
    /**
     * 首屏兜底：只有用户从未显式选过年级时才套用配置默认年级。
     * 避免刚选完"全部年级"又被默认年级（六年级）覆盖，看起来像"切换没生效"。
     */
    ensureDefaultGrade(defaultGrade) {
      if (this.gradeTouched || this.activeGrade !== null) return
      if (defaultGrade == null || defaultGrade === '') return
      this.setGrade(defaultGrade, { markTouched: false })
    },
    /**
     * 默认年级跟随小孩：选小孩/切小孩时总是把空间年级设为该小孩的当前年级。
     * 不做 gradeTouched 拦截——「点小孩」本身就是以该小孩身份进入，默认年级应归属小孩；
     * 用户若要指定年级，用选择页「快速进入指定空间」的下拉（那一路径走 setGrade 手动选择）。
     */
    applyKidDefaultGrade(kid) {
      const grade = kid?.current_grade
      if (grade == null || grade === '') return
      this.setGrade(Number(grade), { markTouched: false })
    },
    reset() {
      this.activeSubjectId = null
      this.activeGrade = null
      this.gradeTouched = false
      sessionStorage.removeItem(SUBJECT_KEY)
      sessionStorage.removeItem(GRADE_KEY)
      sessionStorage.removeItem(GRADE_TOUCHED_KEY)
    },
  },
})
