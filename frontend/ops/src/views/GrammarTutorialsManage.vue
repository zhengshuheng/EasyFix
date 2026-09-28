<template>
  <div class="grammar-tutorials-page">
    <el-card shadow="never" class="header-card">
      <div class="header-row">
        <div>
          <h2>语法教程</h2>
          <p class="desc">
            这里维护的是<b>全部空间的语法知识点与教程内容（主库权威）</b>：语法点固化、全空间一致，家长端只读。
            新建空间创建时自动同步最新教程；存量空间可点「推送到所有空间」一键更新（或由家长在空间内点「同步官方教程」）。
            内容缺失的点点「生成缺失教程」由 AI 按小学课标批量生成。
          </p>
        </div>
        <div class="actions">
          <el-button :disabled="loading" @click="load">🔄 刷新</el-button>
          <el-button type="warning" plain :loading="generating" @click="generateMissing">✨ 生成缺失教程</el-button>
          <el-button type="primary" :loading="syncing" @click="syncTenants">📤 推送到所有空间</el-button>
        </div>
      </div>
    </el-card>

    <el-card shadow="never">
      <div class="filter-row">
        <el-select v-model="categoryFilter" placeholder="全部板块" clearable style="width: 180px" @change="load">
          <el-option v-for="c in categories" :key="c" :label="c" :value="c" />
        </el-select>
        <el-checkbox v-model="onlyMissing" @change="load">只看缺内容</el-checkbox>
        <span class="count">共 {{ total }} 个语法点 · 缺内容 {{ missingCount }} 个</span>
      </div>

      <el-table :data="items" v-loading="loading" size="default" border stripe>
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column prop="category" label="板块" width="130" />
        <el-table-column prop="title" label="语法点" min-width="200" />
        <el-table-column label="年级" width="80">
          <template #default="{ row }">{{ row.grade ? row.grade + '年级' : '通用' }}</template>
        </el-table-column>
        <el-table-column label="教程状态" width="100">
          <template #default="{ row }">
            <el-tag v-if="row.has_content" type="success" size="small">✓ 有内容</el-tag>
            <el-tag v-else type="warning" size="small">缺内容</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="source" label="来源" width="80" />
        <el-table-column prop="updated_at" label="更新时间" width="130" />
        <el-table-column label="操作" width="90" fixed="right">
          <template #default="{ row }">
            <el-button size="small" type="primary" plain @click="openEdit(row)">编辑</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 编辑弹窗 -->
    <el-dialog v-model="editVisible" title="编辑语法教程" width="760px" top="4vh">
      <el-form label-width="110px" v-if="editing">
        <el-form-item label="板块">
          <el-input v-model="editing.category" />
        </el-form-item>
        <el-form-item label="语法点">
          <el-input v-model="editing.title" />
        </el-form-item>
        <el-form-item label="适用年级">
          <el-select v-model="editing.grade" clearable style="width: 160px">
            <el-option v-for="g in 12" :key="g" :label="g + '年级'" :value="g" />
          </el-select>
        </el-form-item>
        <el-form-item label="一句话总结">
          <el-input v-model="editing.summary" type="textarea" :rows="2" />
        </el-form-item>
        <el-form-item label="教程正文">
          <el-input v-model="editing.content_md" type="textarea" :rows="12" placeholder="Markdown 格式：## 这是啥 / ### 怎么用 / 例句" />
        </el-form-item>
        <el-form-item label="例句 JSON">
          <el-input v-model="editing.examples" type="textarea" :rows="4" placeholder='[{"en":"I am a student.","zh":"我是一名学生。"}]' />
        </el-form-item>
        <el-form-item label="易错点 JSON">
          <el-input v-model="editing.common_mistakes" type="textarea" :rows="3" placeholder='["I am 不能写成 I is"]' />
        </el-form-item>
        <el-form-item label="记忆口诀">
          <el-input v-model="editing.mnemonic" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editVisible = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="saveEdit">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  opsGrammarLessons,
  opsGrammarLesson,
  opsGrammarSave,
  opsGrammarAiGenerate,
  opsGrammarSyncTenants,
} from '../api/ops.js'

const items = ref([])
const categories = ref([])
const total = ref(0)
const missingCount = ref(0)
const loading = ref(false)
const generating = ref(false)
const syncing = ref(false)
const categoryFilter = ref(null)
const onlyMissing = ref(false)
const editVisible = ref(false)
const editing = ref(null)
const saving = ref(false)

async function load() {
  loading.value = true
  try {
    const params = {}
    if (categoryFilter.value) params.category = categoryFilter.value
    if (onlyMissing.value) params.has_content = 0
    const data = await opsGrammarLessons(params)
    items.value = data.items || []
    total.value = data.total || 0
    if (!onlyMissing.value) {
      missingCount.value = items.value.filter((r) => !r.has_content).length
    }
    // 板块下拉（完整列表时）
    if (!categoryFilter.value && !onlyMissing.value) {
      categories.value = [...new Set(items.value.map((r) => r.category))]
    }
  } catch (e) {
    /* interceptor 已提示 */
  } finally {
    loading.value = false
  }
}

async function openEdit(row) {
  try {
    const d = await opsGrammarLesson(row.id)
    editing.value = {
      ...d,
      examples: Array.isArray(d.examples) ? JSON.stringify(d.examples, null, 2) : (d.examples || '[]'),
      common_mistakes: Array.isArray(d.common_mistakes) ? JSON.stringify(d.common_mistakes, null, 2) : (d.common_mistakes || '[]'),
    }
    editVisible.value = true
  } catch (e) { /* interceptor 已提示 */ }
}

async function saveEdit() {
  saving.value = true
  try {
    const payload = {
      category: editing.value.category,
      title: editing.value.title,
      grade: editing.value.grade || null,
      summary: editing.value.summary,
      content_md: editing.value.content_md,
      examples: parseJson(editing.value.examples),
      common_mistakes: parseJson(editing.value.common_mistakes),
      mnemonic: editing.value.mnemonic,
    }
    await opsGrammarSave(editing.value.id, payload)
    ElMessage.success('已保存（成为全部空间的新教程内容）')
    editVisible.value = false
    await load()
  } catch (e) {
    ElMessage.error('保存失败：' + (e.response?.data?.detail || e.message))
  } finally {
    saving.value = false
  }
}

function parseJson(s) {
  try {
    const v = JSON.parse(s || '[]')
    return Array.isArray(v) ? v : []
  } catch (e) {
    ElMessage.warning('JSON 格式不正确，已按空数组保存')
    return []
  }
}

async function generateMissing() {
  try {
    await ElMessageBox.confirm('将为所有「缺内容」的语法点调用 AI 生成教程（耗时较长，可分批执行）。确定继续？', '生成缺失教程', { type: 'warning' })
  } catch (e) {
    return
  }
  generating.value = true
  try {
    const r = await opsGrammarAiGenerate({})
    ElMessage.success(`生成完成：成功 ${r.ok_count || 0} / ${r.total || 0} 个`)
    await load()
  } catch (e) {
    /* interceptor 已提示 */
  } finally {
    generating.value = false
  }
}

async function syncTenants() {
  try {
    await ElMessageBox.confirm('将主库语法教程推送到全部空间库 + 模板库（按 id 更新内容、同步软删多余语法点）。确定继续？', '推送到所有空间', { type: 'warning' })
  } catch (e) {
    return
  }
  syncing.value = true
  try {
    const r = await opsGrammarSyncTenants()
    const t = r.template || {}
    ElMessage.success(`推送完成：模板更新 ${t.updated || 0} 个；空间 ${r.space_count || 0} 个（失败 ${(r.failures || []).length} 个）`)
  } catch (e) {
    /* interceptor 已提示 */
  } finally {
    syncing.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.header-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
}
h2 {
  margin: 0 0 6px;
}
.desc {
  color: #666;
  font-size: 12px;
  line-height: 1.8;
  max-width: 720px;
  margin: 0;
}
.actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}
.filter-row {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 12px;
  flex-wrap: wrap;
}
.count {
  color: #909399;
  font-size: 12px;
}
</style>
