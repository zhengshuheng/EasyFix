<template>
  <el-dialog
    :model-value="modelValue"
    title="🤖 AI 生成知识点"
    width="1060px"
    class="ai-kp-dialog"
    @update:model-value="val => emit('update:modelValue', val)"
    @open="onOpen"
  >
    <el-form :model="form" label-width="90px">
      <el-form-item label="生成方式">
        <el-radio-group v-model="form.mode">
          <el-radio label="textbook">教材模式（选教材即可，无需输入指令）</el-radio>
          <el-radio label="custom">自定义指令（输入一句话）</el-radio>
        </el-radio-group>
      </el-form-item>

      <el-form-item v-if="form.mode === 'textbook'" label="教材">
        <div style="display: flex; flex-wrap: wrap; gap: 10px; width: 100%">
          <el-select v-model="form.subject_id" placeholder="学科" style="width: 120px" @change="loadVersions">
            <el-option v-for="s in subjects" :key="s.id" :label="s.name" :value="s.id" />
          </el-select>
          <el-select v-model="form.version" placeholder="教材版本" style="width: 300px" filterable>
            <el-option v-for="v in versions" :key="v" :label="v" :value="v" />
          </el-select>
          <el-select v-model="form.grade" placeholder="年级" style="width: 100px">
            <el-option v-for="g in 6" :key="g" :label="g + '年级'" :value="g" />
          </el-select>
          <el-select v-model="form.semester" placeholder="册次" style="width: 100px" clearable>
            <el-option label="上册" :value="1" />
            <el-option label="下册" :value="2" />
          </el-select>
        </div>
        <div v-if="form.version && !versions.includes(form.version)" style="margin-top: 6px; font-size: 12px; color: #e6a23c">
          该版本不在目录列表中，AI 仍会按教材知识生成，可放心使用
        </div>
      </el-form-item>

      <el-form-item v-else label="指令">
        <el-input
          v-model="form.instruction"
          type="textarea"
          :rows="3"
          placeholder="例如：生成人教版小学数学三年级上册的全部知识点；或：外研社版英语三年级起点五年级下册第3、4单元的知识点"
        />
      </el-form-item>

      <el-form-item v-if="form.mode === 'custom'" label="归属">
        <div style="display: flex; gap: 10px">
          <el-select v-model="form.grade" placeholder="年级" style="width: 110px">
            <el-option v-for="g in 6" :key="g" :label="g + '年级'" :value="g" />
          </el-select>
          <el-select v-model="form.semester" placeholder="册次" style="width: 110px" clearable>
            <el-option label="上册" :value="1" />
            <el-option label="下册" :value="2" />
          </el-select>
        </div>
        <div style="font-size: 12px; color: #909399; line-height: 1.6">
          生成结果将归属到所选年级/学期；版本信息请在教材模式下选择
        </div>
      </el-form-item>

      <el-form-item label="操作">
        <el-button
          type="primary"
          :loading="generating"
          :disabled="generateDisabled"
          @click="generate"
        >{{ form.mode === 'textbook' ? '生成全册知识点' : 'AI 生成知识点' }}</el-button>
        <el-button v-if="form.mode === 'custom'" plain @click="fillSample('人教版小学数学三年级上册')">示例：人教版小学数学三上</el-button>
        <el-button v-if="form.mode === 'custom'" plain @click="fillSample('沪教版深圳英语三年级上册')">示例：沪教版深圳英语三上</el-button>
      </el-form-item>

      <el-form-item v-if="items.length" label="预览">
        <div style="width: 100%">
          <el-table :data="items" border stripe size="small" max-height="340">
            <el-table-column label="入" width="48" align="center">
              <template #default="{ row }">
                <el-checkbox v-model="row.checked" />
              </template>
            </el-table-column>
            <el-table-column label="状态" width="78" align="center">
              <template #default="{ row }">
                <el-tag v-if="row.existing" type="warning" size="small">已存在</el-tag>
                <el-tag v-else type="success" size="small">新增</el-tag>
              </template>
            </el-table-column>
            <el-table-column prop="chapter" label="单元/章节" width="170" show-overflow-tooltip />
            <el-table-column label="知识点名称" min-width="170">
              <template #default="{ row }">
                <el-input v-model="row.name" size="small" />
              </template>
            </el-table-column>
            <el-table-column label="说明" min-width="230">
              <template #default="{ row }">
                <el-input v-model="row.description" size="small" />
              </template>
            </el-table-column>
            <el-table-column label="要求" width="96">
              <template #default="{ row }">
                <el-select v-model="row.requirement" size="small" clearable placeholder="—">
                  <el-option v-for="r in REQUIREMENTS" :key="r" :label="r" :value="r" />
                </el-select>
              </template>
            </el-table-column>
            <el-table-column label="标签" width="140">
              <template #default="{ row }">
                <el-select v-model="row.tags" multiple size="small" placeholder="—" style="width: 100%">
                  <el-option v-for="t in TAGS" :key="t" :label="t" :value="t" />
                </el-select>
              </template>
            </el-table-column>
          </el-table>
          <div style="margin-top: 8px; font-size: 13px; color: #909399">
            共 {{ items.length }} 条，其中 {{ existingCount }} 条已存在（默认不勾选）；勾选后点「导入所选」写入知识点库
          </div>
        </div>
      </el-form-item>
    </el-form>

    <template #footer>
      <el-button @click="emit('update:modelValue', false)">取消</el-button>
      <el-button type="primary" :loading="importing" :disabled="checkedCount === 0" @click="doImport">
        导入所选（{{ checkedCount }}）
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import http from '@/api/http'
import { questionApi } from '@/api/question'

const props = defineProps({
  modelValue: Boolean,
  subjects: { type: Array, default: () => [] },
})
const emit = defineEmits(['update:modelValue', 'imported'])

const TAGS = ['重点', '难点', '易错点']
const REQUIREMENTS = ['识记', '理解', '背诵', '运用', '综合']

const generating = ref(false)
const importing = ref(false)
const versions = ref([])
const items = ref([])

const form = reactive({
  mode: 'textbook',
  subject_id: null,
  version: '',
  grade: null,
  semester: 1,
  instruction: '',
})

const checkedCount = computed(() => items.value.filter(w => w.checked).length)
const existingCount = computed(() => items.value.filter(w => w.existing).length)
const generateDisabled = computed(() => {
  if (generating.value) return true
  if (form.mode === 'textbook') return !form.subject_id || !form.grade
  return !form.instruction || !form.instruction.trim()
})

const onOpen = () => {
  // 每次打开重置（年级/册次留空由用户自选，不再默认）
  form.mode = 'textbook'
  form.subject_id = props.subjects.length ? props.subjects[0].id : null
  form.version = ''
  form.grade = null
  form.semester = null
  form.instruction = ''
  items.value = []
  if (form.subject_id) loadVersions()
}

const loadVersions = async () => {
  versions.value = []
  form.version = ''
  if (!form.subject_id) return
  try {
    const { data } = await http.get('/textbook/catalog')
    const books = data.books || []
    const vers = []
    for (const b of books) {
      const subj = (b.subject || '')
      const subjName = props.subjects.find(s => s.id === form.subject_id)?.name || ''
      if (subj === subjName || subj.includes(subjName)) {
        const v = (b.version || '').trim()
        if (v && !vers.includes(v)) vers.push(v)
      }
    }
    versions.value = vers
  } catch (e) {
    console.error('加载教材版本失败:', e)
  }
}

const fillSample = (text) => {
  form.instruction = `生成${text}的全部知识点`
}

const generate = async () => {
  generating.value = true
  try {
    const payload = { mode: form.mode }
    if (form.mode === 'textbook') {
      payload.subject_id = form.subject_id
      payload.version = form.version || undefined
      payload.grade = form.grade
      payload.semester = form.semester || null
    } else {
      payload.instruction = form.instruction
    }
    const { data } = await questionApi.aiGenerateKp(payload)
    if (!data.items || data.items.length === 0) {
      ElMessage.warning(data.detail || 'AI 未生成任何知识点，请调整后重试')
      return
    }
    items.value = data.items.map(it => ({
      chapter: it.chapter || '',
      name: it.name,
      description: it.description || '',
      requirement: it.requirement || '',
      tags: Array.isArray(it.tags) ? it.tags : [],
      kp_type: it.kp_type || '',
      existing: !!it.existing,
      checked: !it.existing,
    }))
    ElMessage.success(`AI 生成 ${data.items.length} 条知识点，请核对后导入`)
  } catch (error) {
    console.error('AI 生成知识点失败:', error)
    ElMessage.error((error.response && error.response.data && error.response.data.detail) || 'AI 生成失败，请检查大模型配置或稍后重试')
  } finally {
    generating.value = false
  }
}

const doImport = async () => {
  const selected = items.value.filter(w => w.checked && w.name && w.name.trim())
  if (!selected.length) {
    ElMessage.warning('请先勾选要导入的知识点')
    return
  }
  importing.value = true
  let ok = 0
  let fail = 0
  try {
    for (const it of selected) {
      try {
        await questionApi.createKnowledgePoint({
          name: it.name.trim(),
          subject_id: form.subject_id || (props.subjects[0] ? props.subjects[0].id : undefined),
          grade: form.grade,
          semester: form.semester || null,
          chapter: it.chapter || undefined,
          version: form.mode === 'textbook' ? (form.version || undefined) : undefined,
          description: it.description || undefined,
          tags: it.tags || [],
          requirement: it.requirement || undefined,
          kp_type: it.kp_type || undefined,
        })
        ok++
      } catch (e) {
        fail++
      }
    }
    if (ok > 0) {
      ElMessage.success(`导入完成：成功 ${ok} 条${fail ? `，失败 ${fail} 条` : ''}`)
      emit('imported')
      emit('update:modelValue', false)
    } else {
      ElMessage.error(`导入失败 ${fail} 条，请稍后重试`)
    }
  } finally {
    importing.value = false
  }
}

watch(() => props.modelValue, (v) => {
  if (v) onOpen()
})
</script>

<style scoped>
.ai-kp-dialog :deep(.el-select) {
  width: 100%;
}
</style>
