<template>
  <el-dialog v-model="visible" title="按教材同步知识点" width="720px" :close-on-click-modal="false" @open="onOpen">
    <el-alert type="info" :closable="false" style="margin-bottom: 14px">
      <template #title>
        两种方式：<b>在线知识大纲</b>（数学人教版 / 语文统编 / 英语PEP / 科学教科版，免下载秒级导入，推荐）；
        <b>教材 PDF 提取</b>（支持北师大 / 苏教 / 冀教 / 青岛等 30+ 版本，应用内下载 PDF → 本地 OCR → AI 提取，约 10~15 分钟/册）。
      </template>
    </el-alert>

    <el-tabs v-model="activeTab">
      <!-- ============ Tab 1：在线知识大纲 ============ -->
      <el-tab-pane label="在线知识大纲（推荐）" name="ctsf">
        <el-form :model="form" label-width="90px" @submit.prevent>
          <el-form-item label="学科" required>
            <el-select v-model="form.subject" placeholder="选择学科" style="width: 220px" @change="onSubjectChange">
              <el-option v-for="s in subjects" :key="s" :label="s" :value="s" />
            </el-select>
          </el-form-item>
          <el-form-item label="版本" required>
            <el-select v-model="form.version" placeholder="先选学科" style="width: 220px" @change="onVersionChange">
              <el-option v-for="v in versions" :key="v" :label="v" :value="v" />
            </el-select>
          </el-form-item>
          <el-form-item label="年级" required>
            <el-select v-model="form.grade" placeholder="先选版本" style="width: 220px" @change="onGradeChange">
              <el-option v-for="g in grades" :key="g" :label="g" :value="g" />
            </el-select>
          </el-form-item>
          <el-form-item label="册次" required>
            <el-select v-model="form.semester" placeholder="先选年级" style="width: 220px">
              <el-option v-for="s in semesters" :key="s" :label="s" :value="s" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <span v-if="selectedCtsfBook" class="tb-hint">
              {{ selectedCtsfBook.file.replace('.json', '') }} ·
              <span v-if="selectedCtsfBook.imported > 0">已导入 {{ selectedCtsfBook.imported }} 个知识点（重复自动跳过）</span>
              <span v-else>未导入</span>
            </span>
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <!-- ============ Tab 2：教材 PDF 提取 ============ -->
      <el-tab-pane label="教材 PDF 提取（多版本）" name="pdf">
        <el-form :model="form" label-width="90px" @submit.prevent>
          <el-form-item label="学科" required>
            <el-select v-model="form.subject" placeholder="选择学科" style="width: 220px" @change="onSubjectChange">
              <el-option v-for="s in pdfSubjects" :key="s" :label="s" :value="s" />
            </el-select>
          </el-form-item>
          <el-form-item label="版本" required>
            <el-select v-model="form.version" placeholder="先选学科" style="width: 220px" @change="onVersionChange">
              <el-option v-for="v in pdfVersions" :key="v" :label="v" :value="v" />
            </el-select>
          </el-form-item>
          <el-form-item label="年级" required>
            <el-select v-model="form.grade" placeholder="先选版本" style="width: 220px" @change="onGradeChange">
              <el-option v-for="g in pdfGrades" :key="g" :label="g" :value="g" />
            </el-select>
          </el-form-item>
          <el-form-item label="册次" required>
            <el-select v-model="form.semester" placeholder="先选年级" style="width: 220px">
              <el-option v-for="s in pdfSemesters" :key="s" :label="s" :value="s" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <span v-if="selectedPdfBook" class="tb-hint">
              {{ selectedPdfBook.version }} {{ selectedPdfBook.subject }} {{ selectedPdfBook.grade }}{{ selectedPdfBook.semester }}
              · <span v-if="selectedPdfBook.local">PDF 已在本地</span>
              <span v-else-if="selectedPdfBook.local_only">⚠ 无在线资源，需手动放置 PDF</span>
              <span v-else>需下载（约 5~30MB）</span> · 源：{{ sourceLabels(selectedPdfBook) }}
            </span>
          </el-form-item>
        </el-form>
        <div class="tb-manual">
          <el-button size="small" @click="doOpenFolder">打开教材文件夹</el-button>
          <el-button size="small" @click="doScan">扫描本地 PDF</el-button>
          <span class="tb-hint" style="margin-left: 10px">
            网络全部失败时：手动下载 PDF 放入 <code>data/textbooks/版本/科目/三年级上册.pdf</code> 后点“扫描本地 PDF”再导入
          </span>
        </div>
      </el-tab-pane>
    </el-tabs>

    <!-- 进度条 -->
    <div v-if="runningTask" style="margin-top: 12px">
      <el-progress :percentage="runningTask.progress" :status="runningTask.status === 'failed' ? 'exception' : undefined" />
      <div class="tb-hint" style="margin-top: 6px">
        {{ runningTask.message }}<span v-if="runningTask.status === 'done' && runningTask.result">（共 {{ runningTask.result.units || '' }} 个单元）</span>
      </div>
    </div>

    <template #footer>
      <el-button @click="visible = false" :disabled="!!runningTask && runningTask.status === 'pending'">取消</el-button>
      <el-button type="primary" :loading="!!runningTask && runningTask.status === 'pending'" @click="doImport">
        {{ activeTab === 'ctsf' ? '导入在线大纲' : '下载并提取' }}
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, computed, onBeforeUnmount } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { textbookApi } from '@/api/textbook'

const props = defineProps({
  modelValue: Boolean,
})
const emit = defineEmits(['update:modelValue', 'imported'])

const visible = computed({
  get: () => props.modelValue,
  set: (v) => emit('update:modelValue', v),
})

const activeTab = ref('ctsf')
const form = reactive({ subject: '', version: '', grade: '', semester: '' })

// ---- 目录数据 ----
const ctsfBooks = ref([])   // 在线大纲 44 本
const pdfBooks = ref([])    // 教材 PDF 369 本

// ---- 当前任务（轮询） ----
const runningTask = ref(null)
let pollTimer = null

const GRADES = ['一年级', '二年级', '三年级', '四年级', '五年级', '六年级']
const SEMESTERS = ['上册', '下册']

const onOpen = async () => {
  if (!ctsfBooks.value.length) {
    try {
      const { data } = await textbookApi.ctsfCatalog()
      ctsfBooks.value = data.books || []
    } catch (e) {
      ElMessage.error('获取在线大纲目录失败（需要联网）')
    }
  }
  if (!pdfBooks.value.length) {
    try {
      const { data } = await textbookApi.catalog()
      pdfBooks.value = data.books || []
    } catch (e) {
      ElMessage.error('获取教材目录失败')
    }
  }
}

// ---- 选择器联动 ----
const subjects = computed(() => [...new Set(ctsfBooks.value.map(b => b.subject))])
const pdfSubjects = computed(() => [...new Set(pdfBooks.value.map(b => b.subject))])

const versions = computed(() => [...new Set(ctsfBooks.value.filter(b => b.subject === form.subject).map(b => b.version))])
const grades = computed(() => {
  const base = ctsfBooks.value.filter(b => b.subject === form.subject && b.version === form.version)
  return GRADES.filter(g => base.some(b => b.grade === g))
})
const semesters = computed(() => {
  const base = ctsfBooks.value.filter(b => b.subject === form.subject && b.version === form.version && b.grade === form.grade)
  return SEMESTERS.filter(s => base.some(b => b.semester === s))
})

const pdfVersions = computed(() => [...new Set(pdfBooks.value.filter(b => b.subject === form.subject).map(b => b.version))])
const pdfGrades = computed(() => {
  const base = pdfBooks.value.filter(b => b.subject === form.subject && b.version === form.version)
  return GRADES.filter(g => base.some(b => b.grade === g))
})
const pdfSemesters = computed(() => {
  const base = pdfBooks.value.filter(b => b.subject === form.subject && b.version === form.version && b.grade === form.grade)
  return SEMESTERS.filter(s => base.some(b => b.semester === s))
})

const selectedCtsfBook = computed(() =>
  ctsfBooks.value.find(b => b.subject === form.subject && b.version === form.version
    && b.grade === form.grade && b.semester === form.semester) || null)
const selectedPdfBook = computed(() =>
  pdfBooks.value.find(b => b.subject === form.subject && b.version === form.version
    && b.grade === form.grade && b.semester === form.semester) || null)

const sourceLabels = (book) => {
  const srcs = (book.downloads || []).map(d => d.source === 'freepep' ? '直连' : 'GitHub')
  return srcs.join(' + ')
}

const onSubjectChange = () => { form.version = ''; form.grade = ''; form.semester = '' }
const onVersionChange = () => { form.grade = ''; form.semester = '' }
const onGradeChange = () => { form.semester = '' }

// ---- 导入 ----
const doImport = async () => {
  if (!form.subject || !form.version || !form.grade || !form.semester) {
    ElMessage.warning('请完整选择 学科/版本/年级/册次')
    return
  }
  if (activeTab.value === 'ctsf' && !selectedCtsfBook.value) {
    ElMessage.warning('在线大纲中未找到该教材')
    return
  }
  if (activeTab.value === 'pdf' && !selectedPdfBook.value) {
    ElMessage.warning('教材目录中未找到该教材')
    return
  }
  const tip = activeTab.value === 'ctsf'
    ? `从在线大纲导入《${form.version} ${form.subject} ${form.grade}${form.semester}》知识点，并同步下载对应教材 PDF（教材库可直接按知识点对照）。`
    : selectedPdfBook.value?.local_only
      ? `《${form.version} ${form.subject} ${form.grade}${form.semester}》暂无在线资源。\n\n请手动下载教材 PDF，放到 data/textbooks/${form.version}/英语/${form.grade}${form.semester}.pdf，\n然后点「打开教材文件夹」→ 放入文件 → 「扫描本地 PDF」后再次导入。\n\n现在就打开教材文件夹？`
      : `下载并提取《${form.version} ${form.subject} ${form.grade}${form.semester}》？PDF 下载 + OCR 识别 + AI 提取约需 10~15 分钟，期间可关闭本窗口，任务会继续。`
  try {
    await ElMessageBox.confirm(tip, '确认导入', { type: 'info' })
  } catch {
    return
  }
  if (selectedPdfBook.value?.local_only) {
    // 无在线源：打开文件夹引导手动放置
    doOpenFolder()
    ElMessage.info('已打开教材文件夹，放入 PDF 后点「扫描本地 PDF」再导入')
    return
  }
  try {
    let res
    if (activeTab.value === 'ctsf') {
      res = await textbookApi.ctsfImport({
        subject: form.subject, version: form.version, grade: form.grade, semester: form.semester,
      })
    } else {
      res = await textbookApi.importBook({
        subject: form.subject, version: form.version, grade: form.grade, semester: form.semester,
      })
    }
    startPoll(res.data.task_id)
  } catch (e) {
    ElMessage.error(e.detail || e.message || '启动导入失败')
  }
}

const startPoll = (taskId) => {
  runningTask.value = { id: taskId, progress: 0, message: '排队中', status: 'pending' }
  pollTimer = setInterval(async () => {
    try {
      const { data } = await textbookApi.task(taskId)
      runningTask.value = data
      if (data.status === 'done') {
        clearInterval(pollTimer)
        ElMessage.success(data.message || '导入完成')
        emit('imported')
        setTimeout(() => { runningTask.value = null }, 4000)
      } else if (data.status === 'failed') {
        clearInterval(pollTimer)
        ElMessage.error(data.error || data.message || '导入失败')
        setTimeout(() => { runningTask.value = null }, 8000)
      }
    } catch {
      clearInterval(pollTimer)
      ElMessage.error('查询任务进度失败')
    }
  }, 1500)
}

// ---- 手动放置兜底 ----
const doOpenFolder = async () => {
  try {
    await textbookApi.openFolder()
  } catch (e) {
    ElMessage.error(e.detail || '打开文件夹失败')
  }
}

const doScan = async () => {
  try {
    const { data } = await textbookApi.scanLocal()
    const files = data.files || []
    if (!files.length) {
      ElMessage.info('未发现本地教材 PDF')
      return
    }
    const list = files.map(f => `${f.version}/${f.subject}/${f.grade}${f.semester || ''}（${(f.size / 1024 / 1024).toFixed(1)}MB）`).join('\n')
    const choose = await ElMessageBox.confirm(
      `扫描到 ${files.length} 个本地教材 PDF：\n${list}\n\n是否导入第一个？`,
      '扫描结果', { type: 'info', confirmButtonText: '导入第一个', cancelButtonText: '暂不' }
    ).catch(() => null)
    if (!choose) return
    const f = files[0]
    const res = await textbookApi.importBook({
      subject: f.subject === '未分类' ? form.subject || '数学' : f.subject,
      version: f.version === '未分类' ? form.version || '手动放置' : f.version,
      grade: f.grade || form.grade || '三年级',
      semester: f.semester || form.semester || '上册',
      local_pdf: f.path,
    })
    startPoll(res.data.task_id)
  } catch (e) {
    if (e === 'cancel' || e?.message?.includes('cancel')) return
    ElMessage.error(e.detail || e.message || '扫描失败')
  }
}

onBeforeUnmount(() => { if (pollTimer) clearInterval(pollTimer) })
</script>

<style scoped>
.tb-hint {
  font-size: 12px;
  color: #909399;
}
.tb-manual {
  margin-top: 4px;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}
</style>
