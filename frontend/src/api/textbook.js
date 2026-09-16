import api from './http'

// 教材同步导入（内置目录 + 按需下载 + OCR + LLM 提取 / ChinaStudyFree 在线大纲）
export const textbookApi = {
  // 教材目录（369 本，多版本）
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
}
