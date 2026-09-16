import api from './http'

// 教材同步导入（内置目录 + 按需下载 + OCR + LLM 提取 / ChinaStudyFree 在线大纲）
export const textbookApi = {
  // 教材目录（381 本，多版本）
  catalog() {
    return api.get('/textbook/catalog')
  },
  // 下载并导入指定教材（后台任务，返回 task_id）
  importBook(data) {
    return api.post('/textbook/import', data)
  },
  // 查询任务进度
  task(taskId) {
    return api.get(`/textbook/task/${taskId}`)
  },
  // 最近任务列表
  tasks() {
    return api.get('/textbook/tasks')
  },
  // 扫描本地教材文件夹（手动放置兜底）
  scanLocal() {
    return api.get('/textbook/scan')
  },
  // 打开本地教材文件夹
  openFolder() {
    return api.get('/textbook/open-folder')
  },
  // 在线知识大纲目录（ChinaStudyFree，44 本）
  ctsfCatalog() {
    return api.get('/textbook/ctsf/catalog')
  },
  // 从在线大纲导入（免下载/免OCR）
  ctsfImport(data) {
    return api.post('/textbook/ctsf/import', data)
  },
  // ---- 教材知识库（本地 PDF 在线预览） ----
  // 本地已下载教材书目
  library() {
    return api.get('/textbook/library')
  },
  // 预览指定页（返回 base64 PNG + 总页数）
  preview(params) {
    return api.get('/textbook/library/preview', { params })
  },
  // 单元目录（标题 + 起始页码，需要已 OCR）
  units(params) {
    return api.get('/textbook/library/units', { params })
  },
  // 关键词定位页码
  locate(params) {
    return api.get('/textbook/library/locate', { params })
  },
  // 该教材已导入的知识点（章节分组 + 页码）
  knowledgePoints(params) {
    return api.get('/textbook/library/knowledge-points', { params })
  },
}
