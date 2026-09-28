<template>
  <el-dialog v-model="show" :title="title" width="640px" destroy-on-close>
    <el-radio-group v-model="mode" class="mb">
      <el-radio-button value="text">📝 文本粘贴</el-radio-button>
      <el-radio-button value="file">📄 文件导入</el-radio-button>
      <el-radio-button v-if="type === 'word'" value="image">📷 图片识别</el-radio-button>
    </el-radio-group>

    <el-form inline class="filters">
      <el-form-item v-if="type === 'kp'" label="学科">
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

    <el-input v-if="mode === 'text'" v-model="text" type="textarea" :rows="8" :placeholder="textPlaceholder" />
    <label v-else class="file-box">
      <input type="file" :accept="mode === 'file' ? '.txt,.csv' : '.png,.jpg,.jpeg,.pdf'" multiple @change="onFiles" />
      <div class="file-inner">
        <span class="file-icon">{{ mode === 'file' ? '📄' : '📷' }}</span>
        <span v-if="fileNames">{{ fileNames }}</span>
        <span v-else>{{ mode === 'file' ? '点击选择 .txt / .csv 文件' : '点击选择教材图片 / PDF（可多选）' }}</span>
      </div>
    </label>
    <div v-if="mode === 'image'" class="hint">图片识别仅英语单词可用；识别结果进入 AI 预览，勾选后导入</div>

    <el-alert v-if="msg" :title="msg" :type="msgType" :closable="false" show-icon class="mb" />
    <template #footer>
      <el-button @click="show = false">取消</el-button>
      <el-button type="primary" :loading="busy" @click="doBatch">{{ mode === 'image' ? '📷 识别并预览' : '📥 导入' }}</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { computed, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { opsApi } from '../api/ops.js'

const props = defineProps({ type: { type: String, default: 'kp' }, catalog: { type: Object, default: () => ({ subjects: {} }) } })
const emit = defineEmits(['imported', 'ocr'])

const show = ref(false)
const mode = ref('text')
const form = reactive({ subject: '', version: '', grade: 1, semester: 1 })
const text = ref('')
const files = ref([])
const fileNames = ref('')
const busy = ref(false)
const msg = ref('')
const msgType = ref('info')

const gradeOptions = [1, 2, 3, 4, 5, 6]
const subjects = computed(() => (props.type === 'word' ? ['英语'] : Object.keys(props.catalog?.subjects || {})))
const versions = computed(() => (form.subject ? Object.keys(props.catalog?.subjects?.[form.subject] || {}) : []))
const title = computed(() => `📥 批量导入 · ${props.type === 'kp' ? '知识点' : '英语单词'}`)
const textPlaceholder = computed(() => props.type === 'kp'
  ? '每行一个知识点，可用分隔符拆列：\n名称|章节|说明|要求\n例如：\n分数的基本性质|分数的意义和性质|分子分母同乘除一个不为0的数，分数大小不变|掌握'
  : '每行一个单词，格式：英文 中文释义（可选：英文 /音标/ 中文）\n例如：\napple /ˈæpl/ 苹果\nbanana 香蕉')

function open(defaults = {}) {
  show.value = true
  mode.value = 'text'
  form.subject = props.type === 'word' ? '英语' : (defaults.subject || '')
  form.version = defaults.version || ''
  form.grade = defaults.grade || 1
  form.semester = defaults.semester || 1
  text.value = ''
  files.value = []
  fileNames.value = ''
  msg.value = ''
  busy.value = false
}

function onSubjectChange() { form.version = '' }
function onFiles(e) {
  files.value = Array.from(e.target.files || [])
  fileNames.value = files.value.map((f) => f.name).join('、')
}
function setMsg(t, type = 'info') { msg.value = t; msgType.value = type }

async function doBatch() {
  if (!form.version || !form.grade) { setMsg('请选择 版本 + 年级', 'error'); return }
  busy.value = true
  try {
    if (mode.value === 'image') {
      if (!files.value.length) { setMsg('请先选择教材图片/PDF', 'error'); return }
      const fd = new FormData()
      for (const f of files.value) fd.append('files', f)
      setMsg('识别中（OCR 约 10~60 秒）…', 'info')
      const r = await opsApi().post('/words/extract-textbook', fd)
      if (!r.words || !r.words.length) { setMsg(r.detail || '未识别出单词', 'warning'); return }
      show.value = false
      emit('ocr', r.words, { subject: '英语', version: form.version, grade: form.grade, semester: form.semester })
      return
    }
    let content = text.value.trim()
    if (mode.value === 'file') {
      if (!files.value.length) { setMsg('请先选择 .txt / .csv 文件', 'error'); return }
      content = await files.value[0].text()
    }
    if (!content.trim()) { setMsg('内容为空', 'error'); return }
    const body = { text: content, version: form.version, grade: form.grade, semester: form.semester }
    if (props.type === 'kp') {
      if (!form.subject) { setMsg('请选择学科', 'error'); return }
      body.subject = form.subject
    }
    const path = props.type === 'kp' ? '/knowledge-points/batch-text' : '/words/batch-text'
    const r = await opsApi().post(path, body)
    emit('imported', r.imported ?? 0)
    show.value = false
  } catch (e) {
    setMsg('操作失败，请重试', 'error')
  } finally {
    busy.value = false
  }
}

defineExpose({ open })
</script>

<style scoped>
.filters { margin-bottom: 4px; }
.mb { margin-bottom: 12px; }
.file-box {
  display: block;
  border: 1px dashed #c0c4cc;
  border-radius: 6px;
  padding: 24px;
  cursor: pointer;
  text-align: center;
  transition: border-color .2s;
}
.file-box:hover { border-color: #409eff; }
.file-box input { display: none; }
.file-inner { display: flex; flex-direction: column; gap: 6px; color: #606266; font-size: 14px; }
.file-icon { font-size: 26px; }
.hint { color: #6b7280; font-size: 13px; margin-top: 8px; }
</style>
