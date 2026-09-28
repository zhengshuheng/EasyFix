<template>
  <el-dialog v-model="show" :title="title" width="880px" destroy-on-close>
    <!-- 知识点：统一单按钮智能导入 + 策略说明 -->
    <template v-if="type === 'kp'">
      <el-alert type="info" :closable="false" show-icon class="strategy">
        <div class="strategy-title">🤖 智能导入策略（系统自动选择最佳方式）：</div>
        <ol class="strategy-list">
          <li>① 权威在线知识源（官网/教育部公开大纲优先，其次 GitHub 教材大纲；秒级导入、准确性最高，命中即不做教材 OCR）</li>
          <li>② 本地权威大纲缓存（之前已下载过的权威大纲，秒级导入、准确性高）</li>
          <li>③ 本地教材 PDF（教材库中已放置的 PDF，优先于在线下载；识别优先多模态模型，key 无效自动降级本地 OCR；先识别目录页定位单元页码，再按页范围提取）</li>
          <li>④ 在线教材资源（自动下载 PDF，识别流程同③）</li>
          <li>⑤ AI 指令生成（以上均不可用时自动兜底）</li>
        </ol>
        <div class="strategy-note">每条知识点会记录识别方式：权威源 / 多模态 / 本地OCR / AI生成，可在知识点列表查看</div>
      </el-alert>
      <el-form inline class="filters">
        <el-form-item label="学科">
          <el-select v-model="form.subject" style="width:110px;" @change="onSubjectChange">
            <el-option v-for="s in subjects" :key="s" :label="s" :value="s" />
          </el-select>
        </el-form-item>
        <el-form-item label="版本">
          <el-select v-model="form.version" style="width:170px;">
            <el-option v-for="v in versions" :key="v" :label="v" :value="v" />
          </el-select>
        </el-form-item>
        <el-form-item label="年级">
          <el-select v-model="form.grade" style="width:100px;">
            <el-option v-for="g in gradeOptions" :key="g" :label="`${g} 年级`" :value="g" />
          </el-select>
        </el-form-item>
        <el-form-item label="册次">
          <el-select v-model="form.semester" style="width:90px;">
            <el-option :value="1" label="上册" /><el-option :value="2" label="下册" />
          </el-select>
        </el-form-item>
      </el-form>
      <div class="row-end mb">
        <el-checkbox v-model="skipOnline" class="skip-online">跳过在线教材下载（在线 PDF 较大较慢，未选则优先用本地教材或 AI 生成）</el-checkbox>
        <el-button type="primary" :loading="checking" @click="smartImport">🔍 智能导入</el-button>
      </div>
    </template>

    <!-- 单词：保留教材模式 / 自定义指令 / AI 生成 -->
    <template v-else>
      <el-radio-group v-model="mode" class="mb">
        <el-radio-button value="textbook">📖 教材模式</el-radio-button>
        <el-radio-button value="custom">✍️ 自定义指令</el-radio-button>
      </el-radio-group>

      <el-form v-if="mode === 'textbook'" inline class="filters">
        <el-form-item label="学科">
          <el-select v-model="form.subject" disabled style="width:110px;">
            <el-option value="英语" label="英语" />
          </el-select>
        </el-form-item>
        <el-form-item label="版本">
          <el-select v-model="form.version" style="width:170px;">
            <el-option v-for="v in versions" :key="v" :label="v" :value="v" />
          </el-select>
        </el-form-item>
        <el-form-item label="年级">
          <el-select v-model="form.grade" style="width:100px;">
            <el-option v-for="g in gradeOptions" :key="g" :label="`${g} 年级`" :value="g" />
          </el-select>
        </el-form-item>
        <el-form-item label="册次">
          <el-select v-model="form.semester" style="width:90px;">
            <el-option :value="1" label="上册" /><el-option :value="2" label="下册" />
          </el-select>
        </el-form-item>
      </el-form>
      <el-input v-else v-model="form.instruction" type="textarea" :rows="3" :placeholder="instructionPlaceholder" />

      <div class="row-end mb">
        <el-button :loading="generating" @click="generate">🤖 AI 生成</el-button>
      </div>
    </template>

    <el-progress v-if="task && !['done', 'failed'].includes(task.status)" class="mb"
                 :percentage="task.progress" :stroke-width="12" striped />
    <div v-if="task && task.message && !['done', 'failed'].includes(task.status)" class="task-msg mb">{{ task.message }}</div>

    <el-alert v-if="msg" :title="msg" :type="msgType" :closable="false" show-icon class="mb" />

    <template v-if="preview.length">
      <el-table :data="preview" border max-height="380" size="small" @selection-change="onSel">
        <el-table-column type="selection" width="42" />
        <template v-if="type === 'kp'">
          <el-table-column prop="name" label="知识点" min-width="170" show-overflow-tooltip />
          <el-table-column prop="chapter" label="章节" width="110" />
          <el-table-column prop="description" label="说明" min-width="160" show-overflow-tooltip />
          <el-table-column prop="requirement" label="要求" width="76" />
        </template>
        <template v-else>
          <el-table-column prop="english" label="英文" min-width="120" show-overflow-tooltip />
          <el-table-column prop="chinese" label="中文释义" min-width="140" show-overflow-tooltip />
          <el-table-column prop="unit" label="单元" width="64" />
          <el-table-column prop="phonetic" label="音标" width="120" show-overflow-tooltip />
        </template>
        <el-table-column label="状态" width="110">
          <template #default="{ row }">
            <el-tag v-if="row.existing" type="warning" size="small">已存在·更新</el-tag>
          </template>
        </el-table-column>
      </el-table>
      <div class="row-between mb">
        <span class="hint">共生成 {{ preview.length }} 条，已勾选 {{ selected.length }} 条；同名同册自动更新</span>
        <el-button type="success" :disabled="!selected.length" :loading="importing" @click="doImport">导入所选（{{ selected.length }}）</el-button>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { computed, onUnmounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { opsApi } from '../api/ops.js'

const props = defineProps({ type: { type: String, default: 'kp' }, catalog: { type: Object, default: () => ({ subjects: {} }) } })
const emit = defineEmits(['imported'])

const show = ref(false)
const mode = ref('textbook')
const form = reactive({ subject: '', version: '', grade: 1, semester: 1, instruction: '' })
const preview = ref([])
const selected = ref([])
const generating = ref(false)
const importing = ref(false)
const checking = ref(false)
const skipOnline = ref(false)  // 跳过在线教材下载（在线 PDF 较大较慢）
const task = ref(null)
const msg = ref('')
const msgType = ref('info')
let taskTimer = null

const gradeOptions = [1, 2, 3, 4, 5, 6]
const subjects = computed(() => (props.type === 'word' ? ['英语'] : Object.keys(props.catalog?.subjects || {})))
const versions = computed(() => (form.subject ? Object.keys(props.catalog?.subjects?.[form.subject] || {}) : []))
const title = computed(() => `🤖 智能导入 · ${props.type === 'kp' ? '知识点' : '英语单词'}`)
const instructionPlaceholder = computed(() => props.type === 'kp'
  ? '用一句话描述想生成的内容，例如：生成人教版小学数学三年级上册的全部知识点'
  : '用一句话描述想生成的内容，例如：导入沪教版英语三年级上册全册单词')

function open(defaults = {}) {
  show.value = true
  mode.value = 'textbook'
  form.subject = props.type === 'word' ? '英语' : (defaults.subject || '')
  form.version = defaults.version || ''
  form.grade = defaults.grade || 1
  form.semester = defaults.semester || 1
  form.instruction = ''
  preview.value = []
  selected.value = []
  msg.value = ''
  msgType.value = 'info'
  generating.value = false
  importing.value = false
  checking.value = false
  skipOnline.value = false
  task.value = null
  if (taskTimer) { clearInterval(taskTimer); taskTimer = null }
}

// 图片识别承接：OCR 结果直接进预览（batch 弹窗 emit ocr → 本组件）
function openWithPreview(items, defaults = {}) {
  open(defaults)
  preview.value = items || []
  msg.value = `✅ 共 ${(items || []).length} 条，请勾选后导入`
  msgType.value = 'success'
}

function onSubjectChange() {
  form.version = ''
  preview.value = []
  selected.value = []
}

function setMsg(text, type = 'info') {
  msg.value = text
  msgType.value = type
}

const METHOD_LABEL = {
  'ctsf-online': '在线知识点',
  'ctsf-local': '本地大纲',
  'textbook-online': '在线教材提取',
  'textbook-local': '本地教材提取',
  ai: 'AI指令生成',
}
function methodLabel(m) { return METHOD_LABEL[m] || m || '未知来源' }

// 智能导入自动决策：①在线知识大纲 → ②在线教材 → ③本地大纲 → ④本地教材 PDF → ⑤AI 生成
async function smartImport() {
  if (props.type !== 'kp') return generate()
  const need = []
  if (!form.subject) need.push('学科')
  if (!form.version) need.push('版本')
  if (!form.grade) need.push('年级')
  if (need.length) { setMsg('请选择：' + need.join('、'), 'error'); return }

  checking.value = true
  task.value = null
  setMsg('🔍 自动选择最佳导入方式…', 'info')
  try {
    const r = await opsApi().post('/knowledge-points/smart-import', {
      subject: form.subject, version: form.version, grade: form.grade, semester: form.semester,
      skip_online_textbook: skipOnline.value,
    })
    if (r.done) {
      const n = r.imported ?? 0
      setMsg(`✅ 已通过「${methodLabel(r.method)}」导入 ${n} 条（共 ${r.units ?? '-'} 个单元）`, 'success')
      emit('imported', n)
      ElMessage.success(`✅ 智能导入完成：${n} 条（来源：${methodLabel(r.method)}）`)
      show.value = false
    } else {
      task.value = { id: r.task_id, status: 'pending', progress: 0, message: `已选择「${methodLabel(r.method)}」，处理中…` }
      setMsg(`🔍 系统已选择「${methodLabel(r.method)}」方式导入，请稍候…`, 'info')
      pollTask()
    }
  } catch (e) {
    setMsg('智能导入失败：' + (e?.response?.data?.detail || e?.message || '未知错误'), 'error')
    checking.value = false
  }
}

function pollTask() {
  if (taskTimer) clearInterval(taskTimer)
  taskTimer = setInterval(async () => {
    try {
      const t = await opsApi().get(`/tasks/${task.value.id}`)
      task.value = t
      if (t.status === 'done') {
        clearInterval(taskTimer); taskTimer = null
        checking.value = false
        const n = t.result?.imported ?? 0
        const method = t.result?.method || t.source || ''
        ElMessage.success(`✅ 智能导入完成：${n} 条（来源：${methodLabel(method) || '系统自动'}）`)
        emit('imported', n)
        show.value = false
      } else if (t.status === 'failed') {
        clearInterval(taskTimer); taskTimer = null
        checking.value = false
        setMsg('智能导入失败：' + (t.error || '未知错误'), 'error')
      }
    } catch (e) { /* 轮询瞬断忽略，下轮继续 */ }
  }, 1500)
}

async function generate() {
  const need = []
  if (mode.value === 'textbook') {
    if (props.type === 'kp' && !form.subject) need.push('学科')
    if (!form.version) need.push('版本')
    if (!form.grade) need.push('年级')
    if (need.length) { setMsg('请选择：' + need.join('、'), 'error'); return }
  } else {
    if (!form.instruction.trim()) { setMsg('请输入自定义指令', 'error'); return }
  }
  generating.value = true
  try {
    const body = mode.value === 'textbook'
      ? (props.type === 'kp'
        ? { mode: 'textbook', subject: form.subject, version: form.version, grade: form.grade, semester: form.semester }
        : { mode: 'textbook', version: form.version, grade: form.grade, semester: form.semester })
      : { mode: 'custom', instruction: form.instruction.trim() }
    setMsg('AI 生成中（约 1~3 分钟），请稍候…', 'info')
    const path = props.type === 'kp' ? '/knowledge-points/ai-generate' : '/words/ai-generate'
    const r = await opsApi().post(path, body)
    preview.value = r.items || r.words || []
    selected.value = []
    if (preview.value.length) setMsg(`✅ 生成 ${preview.value.length} 条，请勾选后导入`, 'success')
    else setMsg('AI 未生成内容，请调整描述重试', 'warning')
  } catch (e) {
    setMsg('AI 生成失败，请重试', 'error')
  } finally {
    generating.value = false
  }
}

function onSel(rows) {
  selected.value = rows
}

async function doImport() {
  if (!selected.value.length) return
  importing.value = true
  try {
    const items = selected.value.map(({ existing, ...rest }) => rest)
    const body = props.type === 'kp'
      ? { items, subject: form.subject, version: form.version, grade: form.grade, semester: form.semester }
      : { words: items, version: form.version, grade: form.grade, semester: form.semester }
    const path = props.type === 'kp' ? '/knowledge-points/import' : '/words/import'
    const r = await opsApi().post(path, body)
    emit('imported', r.imported ?? selected.value.length)
    show.value = false
  } catch (e) {
    setMsg('导入失败，请重试', 'error')
  } finally {
    importing.value = false
  }
}

onUnmounted(() => {
  if (taskTimer) clearInterval(taskTimer)
})

defineExpose({ open, openWithPreview })
</script>

<style scoped>
.filters { margin-bottom: 4px; }
.mb { margin-bottom: 12px; }
.row-end { display: flex; justify-content: flex-end; gap: 8px; }
.skip-online { margin-right: auto; font-size: 12px; }
.row-between { display: flex; align-items: center; justify-content: space-between; margin-top: 12px; }
.hint { color: #6b7280; font-size: 13px; }
.task-msg { color: #6b7280; font-size: 13px; }
.strategy { margin-bottom: 12px; }
.strategy-title { font-weight: 600; margin-bottom: 4px; }
.strategy-list { margin: 0; padding-left: 20px; line-height: 1.7; font-size: 13px; color: #374151; }
.strategy-note { margin-top: 6px; font-size: 12px; color: #6b7280; }
</style>
