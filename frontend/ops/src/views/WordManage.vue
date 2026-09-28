<template>
  <el-card shadow="never">
    <div class="head">
      <h2>📖 英语单词管理</h2>
      <div class="head-actions">
        <el-button type="success" @click="openAi">🤖 AI 智能导入</el-button>
        <el-button type="warning" @click="openBatch">📥 批量导入</el-button>
        <el-button type="primary" plain :loading="filling" @click="fillSentences">✨ 补全例句</el-button>
        <el-button type="primary" @click="openDialog()">＋ 新增</el-button>
      </div>
    </div>

    <div class="kp-filter-bar">
      <div class="kp-filter-group">
        <span class="kp-filter-label">学科</span>
        <div class="kp-filter-chips">
          <span class="kp-chip-static">英语</span>
        </div>
      </div>
      <div class="kp-filter-group">
        <span class="kp-filter-label">版本</span>
        <div class="kp-filter-chips">
          <el-radio-group v-model="filters.version" size="small" @change="onVersionChange">
            <el-radio-button v-for="v in allVersions" :key="v" :value="v">{{ v }}</el-radio-button>
          </el-radio-group>
          <span v-if="!allVersions.length" class="kp-filter-empty">（暂无版本，可先 AI 导入单词）</span>
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
          <el-input v-model="filters.q" placeholder="搜索英文/中文" clearable style="width:220px;" @keyup.enter="load" />
          <el-button type="primary" @click="load">查询</el-button>
        </div>
      </div>
    </div>

    <el-table v-loading="loading" :data="items" border stripe>
      <el-table-column prop="english" label="英文" min-width="150" />
      <el-table-column prop="chinese" label="中文释义" min-width="180" show-overflow-tooltip />
      <el-table-column prop="phonetic" label="音标" width="140" />
      <el-table-column prop="unit" label="单元" width="70" />
      <el-table-column prop="revision" label="修订" width="80" />
      <el-table-column label="例句" width="80" align="center">
        <template #default="{ row }">
          <el-tag v-if="hasExample(row)" type="success" size="small">有</el-tag>
          <el-tag v-else type="info" size="small">无</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="130" fixed="right">
        <template #default="{ row }">
          <el-button link type="primary" @click="openDialog(row)">编辑</el-button>
          <el-button link type="danger" @click="remove(row)">删除</el-button>
        </template>
      </el-table-column>
      <template #empty><el-empty description="暂无单词，可「AI 智能导入」或新增" /></template>
    </el-table>
    <div class="count">共 {{ total }} 条</div>

    <el-dialog v-model="dialog" :title="form.id ? '编辑单词' : '新增单词'" width="540px" @closed="form.id = null">
      <el-form label-width="90px">
        <el-form-item label="版本">
          <el-select v-model="form.version" style="width:100%;">
            <el-option v-for="v in allVersions" :key="v" :label="v" :value="v" />
          </el-select>
        </el-form-item>
        <el-form-item label="年级">
          <el-select v-model="form.grade" style="width:100%;">
            <el-option v-for="g in gradeOptions" :key="g" :label="gradeLabel(g)" :value="g" />
          </el-select>
        </el-form-item>
        <el-form-item label="册次">
          <el-select v-model="form.semester" style="width:100%;">
            <el-option :value="1" label="上册" /><el-option :value="2" label="下册" />
          </el-select>
        </el-form-item>
        <el-form-item label="英文"><el-input v-model="form.english" placeholder="英文单词（必填）" /></el-form-item>
        <el-form-item label="中文释义"><el-input v-model="form.chinese" placeholder="中文释义（必填）" /></el-form-item>
        <el-form-item label="音标"><el-input v-model="form.phonetic" placeholder="/.../" /></el-form-item>
        <el-form-item label="单元"><el-input-number v-model="form.unit" :min="1" :max="20" /></el-form-item>
        <el-form-item label="修订"><el-input v-model="form.revision" placeholder="默认 v1" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialog = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="save">保存</el-button>
      </template>
    </el-dialog>

    <AiImportDialog ref="aiRef" type="word" :catalog="catalog" @imported="onImported" />
    <BatchImportDialog ref="batchRef" type="word" :catalog="catalog" @imported="onImported" @ocr="onOcr" />
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
const items = ref([])
const total = ref(0)
const loading = ref(false)
const saving = ref(false)
const filling = ref(false)
const dialog = ref(false)
const filters = reactive({ version: '', grade: null, semester: null, q: '' })
const form = reactive({ id: null, version: '', grade: 1, semester: 1, english: '', chinese: '', phonetic: '', unit: 1, revision: 'v1' })

const allVersions = computed(() => Object.keys(catalog.value.subjects['英语'] || {}))
const gradeOptions = [1, 2, 3, 4, 5, 6, 7, 8, 9]
const grades = computed(() => {
  const fromBooks = [...new Set(bookKeys.value.map((k) => Number(k.split('-')[0])))].sort((a, b) => a - b)
  return fromBooks.length ? fromBooks : gradeOptions
})
const bookKeys = computed(() => {
  if (!filters.version) return []
  return Object.keys(catalog.value.subjects['英语']?.[filters.version] || {})
})

function gradeLabel(g) { return `${g} 年级` }
function onVersionChange() {
  filters.grade = null
  filters.semester = null
  items.value = []
  total.value = 0
  pickFirstBook()
}
function pickFirstBook() {
  if (!filters.version) return
  const ks = bookKeys.value
  const gs = [...new Set(ks.map((k) => Number(k.split('-')[0])))].sort((a, b) => a - b)
  const ss = [...new Set(ks.map((k) => Number(k.split('-')[1])))].sort((a, b) => a - b)
  filters.grade = gs[0] ?? null
  filters.semester = ss[0] ?? null
  load()
}

async function load() {
  if (!filters.version) return
  loading.value = true
  try {
    const params = { version: filters.version, page: 1, page_size: 500, q: filters.q }
    if (filters.grade !== null && filters.grade !== '') params.grade = filters.grade
    if (filters.semester !== null && filters.semester !== '') params.semester = filters.semester
    const d = await opsApi().get('/words', { params })
    items.value = d.items
    total.value = d.total
  } finally {
    loading.value = false
  }
}

function openDialog(row) {
  Object.assign(form, row ? {
    id: row.id, version: row.version, grade: row.grade, semester: row.semester,
    english: row.english, chinese: row.chinese, phonetic: row.phonetic || '',
    unit: row.unit || 1, revision: row.revision || 'v1',
  } : {
    id: null, version: filters.version || '', grade: filters.grade ?? 1,
    semester: filters.semester ?? 1, english: '', chinese: '', phonetic: '', unit: 1, revision: 'v1',
  })
  dialog.value = true
}

async function save() {
  if (!form.version || !form.english.trim() || !form.chinese.trim()) {
    ElMessage.warning('版本/英文/中文释义必填')
    return
  }
  saving.value = true
  try {
    const body = { version: form.version, grade: form.grade, semester: form.semester, english: form.english.trim(), chinese: form.chinese.trim(), phonetic: form.phonetic || null, unit: form.unit || null, revision: form.revision || 'v1' }
    if (form.id) await opsApi().put(`/words/${form.id}`, body)
    else await opsApi().post('/words', body)
    ElMessage.success(form.id ? '已更新' : '已新增')
    dialog.value = false
    load()
  } finally {
    saving.value = false
  }
}

async function remove(row) {
  await ElMessageBox.confirm(`确定删除单词「${row.english}」？`, '删除确认', { type: 'warning' })
  await opsApi().delete(`/words/${row.id}`)
  ElMessage.success('已删除')
  load()
}

function openAi() {
  aiRef.value?.open({ version: filters.version, grade: filters.grade, semester: filters.semester })
}
function hasExample(row) {
  const ex = row.example_sentences
  return !!(ex && typeof ex === 'string' && ex.trim() && ex.trim() !== '[]')
}
async function fillSentences() {
  const scope = `${filters.version || '全部版本'}`
    + (filters.grade !== null && filters.grade !== '' ? ` · ${filters.grade}年级` : '')
    + (filters.semester !== null && filters.semester !== '' ? (filters.semester === 1 ? '上册' : '下册') : '')
  await ElMessageBox.confirm(
    `将为「${scope}」范围内缺例句的单词 AI 生成例句并写入运营词库（后台执行，按 20 个/批，一册约 1~3 分钟）。\n生成后租户端点击「同步」即可把例句带过去。`,
    '补全例句', { type: 'info' })
  filling.value = true
  try {
    const body = { version: filters.version || undefined }
    if (filters.grade !== null && filters.grade !== '') body.grade = filters.grade
    if (filters.semester !== null && filters.semester !== '') body.semester = filters.semester
    const r = await opsApi().post('/words/fill-sentences', body)
    ElMessage.success(r.message || `已提交 ${r.queued || 0} 个单词`)
    setTimeout(load, 3000)
  } finally {
    filling.value = false
  }
}
function openBatch() {
  batchRef.value?.open({ version: filters.version, grade: filters.grade, semester: filters.semester })
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
  if (!filters.version && allVersions.value.length) {
    filters.version = allVersions.value[0]
    pickFirstBook()
  }
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
.kp-chip-static { display: inline-flex; align-items: center; padding: 0 12px; height: 24px; border-radius: 4px; background: #409eff; color: #fff; font-size: 12px; }
.mb { margin-bottom: 12px; }
.count { margin-top: 10px; color: #6b7280; font-size: 13px; }
</style>
