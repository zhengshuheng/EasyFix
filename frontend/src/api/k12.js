import api from './http'

// K12 教材知识点库（https://github.com/mmlong818/k12-knowledge-points）
export const k12Api = {
  // 获取知识库索引（学段×科目文件清单）
  catalog() {
    return api.get('/k12/catalog')
  },
  // 导入指定 学段×科目 知识点（LLM 自动分配年级学期）
  importSubject(data) {
    return api.post('/k12/import', data)
  },
}
