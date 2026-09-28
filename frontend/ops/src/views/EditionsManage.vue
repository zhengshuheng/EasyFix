<template>
  <el-card shadow="never">
    <div class="head">
      <h2>📖 教材版本管理</h2>
      <div class="head-actions">
        <el-button type="primary" @click="openForm()">＋ 新增版本</el-button>
      </div>
    </div>
    <el-alert type="warning" :closable="false" show-icon class="mb">
      知识点与英语单词统一使用本版本库；版本删除会连带删除该版本下全部知识点与单词，请谨慎操作。
    </el-alert>

    <el-collapse v-model="expanded" v-loading="loading" class="groups">
      <el-collapse-item v-for="g in groups" :key="g.subject" :name="g.subject">
        <template #title>
          <span class="group-title">
            <span class="group-subject">{{ g.subject }}</span>
            <span class="group-meta">{{ g.items.length }} 个版本 · {{ g.kp }} 知识点 · {{ g.words }} 单词</span>
          </span>
        </template>
        <el-table :data="g.items" border stripe>
          <el-table-column prop="name" label="版本名" min-width="170" />
          <el-table-column prop="books" label="册数" width="70" align="center" />
          <el-table-column prop="kp" label="知识点" width="90" align="center" />
          <el-table-column prop="words" label="单词" width="90" align="center" />
          <el-table-column label="状态" width="110" align="center">
            <template #default="{ row }">
              <el-tag v-if="!row.registered" type="warning" size="small">未登记</el-tag>
              <el-tag v-else :type="row.enabled ? 'success' : 'info'" size="small">{{ row.enabled ? '启用' : '停用' }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column prop="description" label="说明" min-width="150" show-overflow-tooltip />
          <el-table-column label="操作" width="170" fixed="right">
            <template #default="{ row }">
              <template v-if="!row.registered">
                <el-button link type="primary" @click="register(row)">登记</el-button>
                <el-button link type="danger" @click="removeData(row)">删除</el-button>
              </template>
              <template v-else>
                <el-button link type="primary" @click="openForm(row)">编辑</el-button>
                <el-button link type="danger" @click="remove(row)">删除</el-button>
              </template>
            </template>
          </el-table-column>
          <template #empty><el-empty description="该科目暂无版本" /></template>
        </el-table>
      </el-collapse-item>
    </el-collapse>
    <el-empty v-if="!loading && !items.length" description="暂无版本，点击「新增版本」添加" />

    <el-dialog v-model="formShow" :title="form.id ? '编辑版本' : '新增版本'" width="420px">
      <el-form label-width="64px">
        <el-form-item label="学科" required>
          <el-select v-model="form.subject" style="width:100%;">
            <el-option v-for="s in subjectOptions" :key="s" :label="s" :value="s" />
          </el-select>
        </el-form-item>
        <el-form-item label="版本名" required>
          <el-input v-model="form.name" placeholder="如 人教版 / 北师大版 / 外研版" />
        </el-form-item>
        <el-form-item label="说明">
          <el-input v-model="form.description" type="textarea" :rows="2" placeholder="可选：该版本的备注信息" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="formShow = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="save">保存</el-button>
      </template>
    </el-dialog>
  </el-card>
</template>

<script setup>
import { computed, onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { opsApi } from '../api/ops.js'

const loading = ref(false)
const saving = ref(false)
const items = ref([])
const formShow = ref(false)
const subjectOptions = ['数学', '语文', '英语']
const expanded = ref([...subjectOptions])
const form = reactive({ id: null, subject: '', name: '', description: '' })

const groups = computed(() => {
  const map = new Map()
  for (const it of items.value) {
    if (!map.has(it.subject)) map.set(it.subject, [])
    map.get(it.subject).push(it)
  }
  return [...map.entries()]
    .sort((a, b) => {
      const ia = subjectOptions.indexOf(a[0])
      const ib = subjectOptions.indexOf(b[0])
      return (ia < 0 ? 99 : ia) - (ib < 0 ? 99 : ib)
    })
    .map(([subject, its]) => ({
      subject,
      items: its,
      kp: its.reduce((s, i) => s + (i.kp || 0), 0),
      words: its.reduce((s, i) => s + (i.words || 0), 0),
    }))
})

onMounted(load)

async function load() {
  loading.value = true
  try {
    const d = await opsApi().get('/editions')
    items.value = d.items
  } finally {
    loading.value = false
  }
}

function openForm(row) {
  Object.assign(form, row
    ? { id: row.id, subject: row.subject, name: row.name, description: row.description || '' }
    : { id: null, subject: subjectOptions[0], name: '', description: '' })
  formShow.value = true
}

async function save() {
  if (!form.subject || !form.name.trim()) {
    ElMessage.warning('学科与版本名必填')
    return
  }
  saving.value = true
  try {
    const body = { subject: form.subject, name: form.name.trim(), description: form.description || null }
    if (form.id) await opsApi().put(`/editions/${form.id}`, body)
    else await opsApi().post('/editions', body)
    ElMessage.success(form.id ? '已更新' : '已新增')
    formShow.value = false
    await load()
  } finally {
    saving.value = false
  }
}

async function remove(row) {
  await ElMessageBox.confirm(
    `确定删除版本「${row.subject} ${row.name}」？\n该版本下 ${row.kp} 条知识点、${row.words} 个单词将一并删除（不可恢复）。`,
    '删除版本', { type: 'warning', confirmButtonText: '删除' }
  )
  await opsApi().delete(`/editions/${row.id}`)
  ElMessage.success('已删除')
  await load()
}

async function register(row) {
  await ElMessageBox.confirm(
    `将「${row.subject} ${row.name}」登记进版本库？\n登记后可在本页编辑/停用，该版本下 ${row.kp} 条知识点、${row.words} 个单词数据保持不变。`,
    '登记版本', { type: 'info', confirmButtonText: '登记' }
  )
  await opsApi().post('/editions/register', { subject: row.subject, name: row.name })
  ElMessage.success('已登记')
  await load()
}

async function removeData(row) {
  await ElMessageBox.confirm(
    `确定删除数据版本「${row.subject} ${row.name}」？\n该版本下 ${row.kp} 条知识点、${row.words} 个单词将一并删除（不可恢复）。`,
    '删除版本', { type: 'warning', confirmButtonText: '删除' }
  )
  const d = await opsApi().delete('/editions/by-name', { params: { subject: row.subject, name: row.name } })
  ElMessage.success(`已删除（${d.kp} 知识点 / ${d.words} 单词）`)
  await load()
}
</script>

<style scoped>
.head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 12px; }
.head h2 { font-size: 16px; margin: 0; }
.mb { margin-bottom: 12px; }
.groups :deep(.el-collapse-item__header) { font-weight: 600; }
.group-title { display: flex; align-items: baseline; gap: 12px; }
.group-subject { font-size: 15px; }
.group-meta { font-size: 12px; color: #6b7280; font-weight: 400; }
</style>
