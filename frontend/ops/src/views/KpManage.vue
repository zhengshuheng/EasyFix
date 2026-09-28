<template>
  <el-card shadow="never">
    <div class="head">
      <h2>📚 知识点管理</h2>
      <div class="head-actions">
        <el-button type="success" @click="openAi">🤖 智能导入</el-button>
        <el-button type="warning" @click="openBatch">📥 批量导入</el-button>
        <el-button type="primary" @click="openDialog()">＋ 新增</el-button>
      </div>
    </div>

    <div class="kp-filter-bar">
      <div class="kp-filter-group">
        <span class="kp-filter-label">学科</span>
        <div class="kp-filter-chips">
          <el-radio-group v-model="filters.subject" size="small" @change="onSubjectChange">
            <el-radio-button v-for="s in subjects" :key="s" :value="s">{{ s }}</el-radio-button>
          </el-radio-group>
          <span v-if="!subjects.length" class="kp-filter-empty">（暂无科目，可新建教材版本）</span>
        </div>
      </div>
      <div class="kp-filter-group">
        <span class="kp-filter-label">版本</span>
        <div class="kp-filter-chips">
          <el-radio-group v-model="filters.version" size="small" @change="onVersionChange">
            <el-radio-button v-for="v in versions" :key="v" :value="v">{{ v }}</el-radio-button>
          </el-radio-group>
          <span v-if="!versions.length" class="kp-filter-empty">（暂无版本，可新建教材版本）</span>
        </div>
      </div>
      <div class="kp-filter-group">
        <span class="kp-filter-label">年级</span>
        <div class="kp-filter-chips">
          <el-radio-group v-model="filters.grade" size="small" @change="load">
            <el-radio-button :value="null">全部年级</el-radio-button>
            <el-radio-button v-for="g in grades" :key="g" :value="g">{{ g }} 年级</el-radio-button>
          </el-radio-group>
        </div>
      </div>
      <div class="kp-filter-group">
        <span class="kp-filter-label">册次</span>
        <div class="kp-filter-chips">
          <el-radio-group v-model="filters.semester" size="small" @change="load">
            <el-radio-button :value="null">全部册次</el-radio-button>
            <el-radio-button :value="1">上册</el-radio-button>
            <el-radio-button :value="2">下册</el-radio-button>
          </el-radio-group>
        </div>
      </div>
      <div class="kp-filter-group">
        <span class="kp-filter-label">搜索</span>
        <div class="kp-filter-chips">
          <el-input v-model="filters.q" placeholder="搜索名称/章节" clearable style="width:220px;" @keyup.enter="load" />
          <el-button type="primary" @click="load">查询</el-button>
        </div>
      </div>
    </div>

    <div v-loading="loading" class="kp-list">
      <div v-for="g in visibleGroups" :key="g.chapter" class="kp-group">
        <div class="kp-chapter">
          <span class="ch-name">{{ g.chapter }}</span>
          <span class="ch-count">{{ g.items.length }} 条</span>
        </div>
        <table class="kp-table">
          <tbody>
            <tr v-for="row in g.items" :key="row.id">
              <td class="col-name">{{ row.name }}</td>
              <td class="col-desc">{{ row.description || '—' }}</td>
              <td class="col-req">{{ row.requirement || '—' }}</td>
              <td class="col-src">
                <el-tag :type="srcType(row.source_type)" size="small">{{ srcLabel(row.source_type) }}</el-tag>
              </td>
              <td class="col-ocr">
                <el-tag :type="ocrType(row.ocr_mode)" size="small">{{ ocrLabel(row.ocr_mode) }}</el-tag>
              </td>
              <td class="col-ops">
                <el-button link type="primary" @click="openDialog(row)">编辑</el-button>
                <el-button link type="danger" @click="remove(row)">删除</el-button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
      <el-empty v-if="!loading && !total" description="暂无知识点，可「智能导入」或新建教材版本" />
    </div>
    <div class="count">共 {{ total }} 条</div>

    <el-dialog v-model="dialog" :title="form.id ? '编辑知识点' : '新增知识点'" width="540px" @closed="form.id = null">
      <el-form label-width="70px">
        <el-form-item label="科目">
          <el-select v-model="form.subject" style="width:100%;">
            <el-option v-for="s in subjects" :key="s" :label="s" :value="s" />
          </el-select>
        </el-form-item>
        <el-form-item label="版本">
          <el-select v-model="form.version" style="width:100%;">
            <el-option v-for="v in versions" :key="v" :label="v" :value="v" />
          </el-select>
        </el-form-item>
        <el-form-item label="年级">
          <el-select v-model="form.grade" style="width:100%;">
            <el-option v-for="g in grades" :key="g" :label="gradeLabel(g)" :value="g" />
          </el-select>
        </el-form-item>
        <el-form-item label="册次">
          <el-select v-model="form.semester" style="width:100%;">
            <el-option :value="1" label="上册" /><el-option :value="2" label="下册" />
          </el-select>
        </el-form-item>
        <el-form-item label="名称"><el-input v-model="form.name" placeholder="知识点名称（必填）" /></el-form-item>
        <el-form-item label="章节"><el-input v-model="form.chapter" placeholder="如 第一单元 或 第3课" /></el-form-item>
        <el-form-item label="说明"><el-input v-model="form.description" type="textarea" :rows="2" /></el-form-item>
        <el-form-item label="要求"><el-input v-model="form.requirement" placeholder="如 理解 / 掌握" /></el-form-item>
        <el-form-item label="修订"><el-input v-model="form.revision" placeholder="默认 v1" /></el-form-item>
        <el-form-item v-if="form.id && form.sourceType" label="来源">
          <el-tag :type="srcType(form.sourceType)" size="small">{{ srcLabel(form.sourceType) }}</el-tag>
        </el-form-item>
        <el-form-item v-if="form.id && form.ocrMode" label="识别方式">
          <el-tag :type="ocrType(form.ocrMode)" size="small">{{ ocrLabel(form.ocrMode) }}</el-tag>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialog = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="save">保存</el-button>
      </template>
    </el-dialog>

    <AiImportDialog ref="aiRef" type="kp" :catalog="catalog" @imported="onImported" />
    <BatchImportDialog ref="batchRef" type="kp" :catalog="catalog" @imported="onImported" @ocr="onOcr" />
  </el-card>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { opsApi, opsCatalog } from '../api/ops.js'
import AiImportDialog from '../components/AiImportDialog.vue'
import BatchImportDialog from '../components/BatchImportDialog.vue'

const aiRef = ref()
const batchRef = ref()

const catalog = ref({ subjects: {} })
const groups = ref([])
const total = ref(0)
const loading = ref(false)
const saving = ref(false)
const dialog = ref(false)
const filters = reactive({ subject: '', version: '', grade: null, semester: null, q: '' })
const form = reactive({ id: null, subject: '', version: '', grade: null, semester: 1, name: '', chapter: '', description: '', requirement: '', revision: 'v1', sourceType: '' })

const subjects = computed(() => Object.keys(catalog.value.subjects || {}))
const versions = computed(() => (filters.subject ? Object.keys(catalog.value.subjects[filters.subject] || {}) : []))
const bookKeys = computed(() => {
  if (!filters.subject || !filters.version) return []
  return Object.keys(catalog.value.subjects[filters.subject]?.[filters.version] || {})
})
const grades = computed(() => {
  const fromBooks = [...new Set(bookKeys.value.map((k) => Number(k.split('-')[0])))].sort((a, b) => a - b)
  return fromBooks.length ? fromBooks : [1, 2, 3, 4, 5, 6]
})

const visibleGroups = computed(() => {
  const q = filters.q.trim().toLowerCase()
  if (!q) return groups.value
  return groups.value
    .map((g) => ({ ...g, items: g.items.filter((it) => it.name.toLowerCase().includes(q) || (it.chapter || '').toLowerCase().includes(q)) }))
    .filter((g) => g.items.length)
})

const SRC_LABEL = { 'ctsf-online': '在线知识点', 'ctsf-local': '本地大纲', 'textbook-online': '教材书本生成', 'textbook-local': '本地教材', ai: 'AI指令生成', '': '未知', unknown: '未知' }
const SRC_TYPE = { 'ctsf-online': 'success', 'ctsf-local': 'success', 'textbook-online': 'primary', 'textbook-local': 'primary', ai: 'warning', '': 'info', unknown: 'info' }
function srcLabel(t) { return SRC_LABEL[t] ?? SRC_LABEL.unknown }
function srcType(t) { return SRC_TYPE[t] ?? SRC_TYPE.unknown }

const OCR_LABEL = { authority: '权威源', multimodal: '多模态', local: '本地OCR', llm: 'AI生成', '': '—', unknown: '—' }
const OCR_TYPE = { authority: 'success', multimodal: 'primary', local: '', llm: 'warning', '': 'info', unknown: 'info' }
function ocrLabel(t) { return OCR_LABEL[t] ?? OCR_LABEL.unknown }
function ocrType(t) { return OCR_TYPE[t] ?? OCR_TYPE.unknown }

function gradeLabel(g) { return `${g} 年级` }

function onSubjectChange() {
  filters.version = ''
  filters.grade = null
  filters.semester = null
  groups.value = []
  total.value = 0
  const vs = Object.keys(catalog.value.subjects[filters.subject] || {})
  if (vs.length) filters.version = vs[0]
  pickFirstBook()
}
function onVersionChange() {
  filters.grade = null
  filters.semester = null
  groups.value = []
  total.value = 0
  pickFirstBook()
}
function pickFirstBook() {
  if (!filters.subject || !filters.version) return
  const ks = Object.keys(catalog.value.subjects[filters.subject]?.[filters.version] || {})
  const gs = [...new Set(ks.map((k) => Number(k.split('-')[0])))].sort((a, b) => a - b)
  const ss = [...new Set(ks.map((k) => Number(k.split('-')[1])))].sort((a, b) => a - b)
  filters.grade = gs[0] ?? null
  filters.semester = ss[0] ?? null
  load()
}

async function load() {
  if (!filters.subject || !filters.version) return
  loading.value = true
  try {
    const params = { subject: filters.subject, version: filters.version }
    if (filters.grade !== null && filters.grade !== '') params.grade = filters.grade
    if (filters.semester !== null && filters.semester !== '') params.semester = filters.semester
    const d = await opsApi().get('/knowledge-points/grouped', { params })
    groups.value = d.groups
    total.value = d.total
  } finally {
    loading.value = false
  }
}

function openDialog(row) {
  Object.assign(form, row ? {
    id: row.id, subject: filters.subject, version: filters.version, grade: filters.grade ?? 1,
    semester: filters.semester ?? 1, name: row.name, chapter: row.chapter || '',
    description: row.description || '', requirement: row.requirement || '', revision: row.revision || 'v1',
    sourceType: row.source_type || '', ocrMode: row.ocr_mode || '',
  } : {
    id: null, subject: filters.subject, version: filters.version, grade: filters.grade ?? 1,
    semester: filters.semester ?? 1, name: '', chapter: '', description: '', requirement: '', revision: 'v1', sourceType: '', ocrMode: '',
  })
  dialog.value = true
}

async function save() {
  if (!form.subject || !form.version || !form.name.trim()) {
    ElMessage.warning('科目/版本/名称必填')
    return
  }
  saving.value = true
  try {
    const body = { subject: form.subject, version: form.version, grade: form.grade, semester: form.semester, name: form.name.trim(), chapter: form.chapter || null, description: form.description || null, requirement: form.requirement || null, revision: form.revision || 'v1' }
    if (form.id) await opsApi().put(`/knowledge-points/${form.id}`, body)
    else await opsApi().post('/knowledge-points', body)
    ElMessage.success(form.id ? '已更新' : '已新增')
    dialog.value = false
    load()
  } finally {
    saving.value = false
  }
}

async function remove(row) {
  await ElMessageBox.confirm(`确定删除知识点「${row.name}」？`, '删除确认', { type: 'warning' })
  await opsApi().delete(`/knowledge-points/${row.id}`)
  ElMessage.success('已删除')
  load()
}

function openAi() {
  aiRef.value?.open(defaultsForDialog())
}
function defaultsForDialog() {
  return {
    subject: filters.subject || subjects.value[0] || '',
    version: filters.version || versions.value[0] || '',
    grade: filters.grade ?? grades.value[0] ?? null,
    semester: filters.semester ?? 1,
  }
}
function openBatch() {
  batchRef.value?.open(defaultsForDialog())
}
function onImported(n) {
  ElMessage.success(`✅ 已导入 ${n} 条`)
  load()
}
function onOcr(words, defaults) {
  aiRef.value?.openWithPreview(words, defaults)
}

onMounted(async () => {
  catalog.value = await opsCatalog()
  if (!filters.subject) {
    const ss = Object.keys(catalog.value.subjects || {})
    if (ss.length) {
      filters.subject = ss[0]
      const vs = Object.keys(catalog.value.subjects[ss[0]] || {})
      if (vs.length) filters.version = vs[0]
    }
  }
  if (filters.subject && filters.version) pickFirstBook()
})
</script>

<style scoped>
.head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 14px; }
.head h2 { font-size: 16px; margin: 0; }
.kp-filter-bar { display: flex; flex-direction: column; gap: 8px; margin-bottom: 12px; }
.kp-filter-group { display: flex; align-items: flex-start; gap: 10px; }
.kp-filter-chips { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
.kp-filter-empty { color: #c0c4cc; font-size: 12px; line-height: 24px; }
.kp-filter-label { color: #606266; font-size: 13px; white-space: nowrap; line-height: 24px; min-width: 32px; }
.count { margin-top: 10px; color: #6b7280; font-size: 13px; }
.kp-group { margin-bottom: 14px; border: 1px solid #e5e7eb; border-radius: 8px; overflow: hidden; }
.kp-chapter { display: flex; align-items: center; gap: 8px; padding: 8px 12px; background: #f3f4f6; font-weight: 600; }
.kp-chapter .ch-count { font-weight: 400; color: #9ca3af; font-size: 12px; }
.kp-table { width: 100%; border-collapse: collapse; font-size: 13px; }
.kp-table td { padding: 7px 12px; border-top: 1px solid #f3f4f6; vertical-align: top; }
.col-name { width: 200px; font-weight: 500; }
.col-desc { color: #6b7280; }
.col-req { width: 70px; color: #6b7280; }
.col-src { width: 110px; }
.col-ocr { width: 90px; }
.col-ops { width: 110px; text-align: right; white-space: nowrap; }
</style>
