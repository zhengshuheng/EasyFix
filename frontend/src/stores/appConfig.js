import { defineStore } from 'pinia'
import { configApi } from '@/api/config'

/**
 * 应用级默认配置（管理中心维护）
 * default_grade / default_semester 用于各页面搜索与新建表单的默认值
 */
export const useAppConfigStore = defineStore('appConfig', {
  state: () => ({
    defaultGrade: null,
    defaultSemester: null,
    loaded: false,
  }),

  actions: {
    async load(force = false) {
      if (this.loaded && !force) return
      try {
        const { data } = await configApi.getApp()
        this.defaultGrade = data?.default_grade ?? null
        this.defaultSemester = data?.default_semester ?? null
        this.loaded = true
      } catch (e) {
        console.error('加载应用配置失败:', e)
      }
    },

    async save({ defaultGrade, defaultSemester }) {
      const payload = {
        default_grade: defaultGrade ?? null,
        default_semester: defaultSemester ?? null,
      }
      await configApi.saveApp(payload)
      this.defaultGrade = payload.default_grade
      this.defaultSemester = payload.default_semester
      this.loaded = true
    },

    /** 若目标年级为空则填入默认年级 */
    applyDefaultGrade(target) {
      if (target == null && this.defaultGrade != null) {
        return this.defaultGrade
      }
      return target
    },

    /** 若目标学期为空则填入默认学期 */
    applyDefaultSemester(target) {
      if (target == null && this.defaultSemester != null) {
        return this.defaultSemester
      }
      return target
    },
  },
})
