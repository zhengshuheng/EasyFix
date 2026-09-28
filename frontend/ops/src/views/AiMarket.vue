<template>
  <el-card shadow="never">
    <div class="head">
      <h2>🤖 AI 模型市场</h2>
      <el-button type="primary" @click="openDialog()">＋ 新增厂商</el-button>
    </div>
    <p class="hint">配置多家 LLM 厂商后，学生端只需选择「厂商 + 模型」；未配置时沿用旧 AI 网关配置。vision_models 留空 = 该厂商不支持 OCR（如 DeepSeek 纯文本模型）。</p>

    <el-table :data="items" border stripe v-loading="loading">
      <el-table-column prop="name" label="厂商" width="120" />
      <el-table-column prop="vendor" label="标识" width="100" />
      <el-table-column prop="protocol" label="协议" width="86" />
      <el-table-column prop="base_url" label="Base URL" min-width="190" show-overflow-tooltip />
      <el-table-column prop="api_key" label="API Key" width="130" />
      <el-table-column label="可用模型" min-width="180" show-overflow-tooltip>
        <template #default="{ row }">{{ row.models.join(', ') }}</template>
      </el-table-column>
      <el-table-column label="视觉模型" min-width="140" show-overflow-tooltip>
        <template #default="{ row }">{{ row.vision_models.join(', ') || '不支持' }}</template>
      </el-table-column>
      <el-table-column label="默认" width="64" align="center">
        <template #default="{ row }">
          <el-tag v-if="row.is_default" type="success" size="small">默认</el-tag>
          <span v-else style="color:#9ca3af;">—</span>
        </template>
      </el-table-column>
      <el-table-column label="状态" width="70" align="center">
        <template #default="{ row }">
          <el-tag :type="row.enabled ? 'success' : 'info'" size="small">{{ row.enabled ? '启用' : '停用' }}</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button size="small" @click="test(row)">测试</el-button>
          <el-button size="small" type="primary" @click="openDialog(row)">编辑</el-button>
          <el-button size="small" type="danger" @click="remove(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <el-dialog v-model="dialogVisible" :title="form.id ? '编辑厂商' : '新增厂商'" width="620px" destroy-on-close>
      <el-form label-width="110px">
        <el-form-item label="厂商名称">
          <el-input v-model="form.name" placeholder="如：DeepSeek / OpenAI / 阿里云百炼 / 智谱GLM" />
        </el-form-item>
        <el-form-item label="厂商标识">
          <el-input v-model="form.vendor" placeholder="如：deepseek / openai / dashscope / zhipu / anthropic" :disabled="!!form.id" />
        </el-form-item>
        <el-form-item label="协议">
          <el-radio-group v-model="form.protocol">
            <el-radio-button value="openai">OpenAI 兼容</el-radio-button>
            <el-radio-button value="anthropic">Anthropic</el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="Base URL">
          <el-input v-model="form.base_url" placeholder="上游接口地址（空=官方默认）" />
        </el-form-item>
        <el-form-item label="API Key">
          <el-input v-model="form.api_key" placeholder="编辑时留空 = 不修改" show-password />
        </el-form-item>
        <el-form-item label="可用模型">
          <el-input v-model="form.models" placeholder="逗号分隔，如：deepseek-chat,deepseek-reasoner" />
        </el-form-item>
        <el-form-item label="视觉模型">
          <el-input v-model="form.vision_models" placeholder="逗号分隔；留空 = 不支持 OCR" />
        </el-form-item>
        <el-form-item label="启用"><el-switch v-model="form.enabled" /></el-form-item>
        <el-form-item label="设为默认"><el-switch v-model="form.is_default" /></el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="save">保存</el-button>
      </template>
    </el-dialog>

    <el-dialog v-model="testVisible" title="连通测试" width="480px">
      <div v-if="testResult" class="test-body" :class="testResult.ok ? 'ok' : 'err'">
        <div class="test-title">{{ testResult.ok ? '✅ 连接成功' : '❌ 连接失败' }}</div>
        <div v-if="testResult.ok">模型：{{ testResult.model }}<br />回复：{{ testResult.reply }}</div>
        <div v-else class="test-msg">{{ testResult.message }}</div>
      </div>
      <div v-else class="test-body">正在测试（真实调用上游，消耗极少量 token）…</div>
      <template #footer><el-button @click="testVisible = false">关闭</el-button></template>
    </el-dialog>
  </el-card>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { opsApi } from '../api/ops.js'

const items = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const saving = ref(false)
const testVisible = ref(false)
const testResult = ref(null)

const form = reactive({
  id: null, name: '', vendor: '', protocol: 'openai', base_url: '',
  api_key: '', models: '', vision_models: '', enabled: true, is_default: false,
})

async function load() {
  loading.value = true
  try {
    const r = await opsApi().get('/providers')
    items.value = r.items || []
  } catch (e) {
    ElMessage.error('加载失败')
  } finally {
    loading.value = false
  }
}

function openDialog(row) {
  Object.assign(form, row ? {
    id: row.id, name: row.name, vendor: row.vendor, protocol: row.protocol,
    base_url: row.base_url, api_key: '', models: row.models.join(','),
    vision_models: row.vision_models.join(','), enabled: row.enabled, is_default: row.is_default,
  } : {
    id: null, name: '', vendor: '', protocol: 'openai', base_url: '',
    api_key: '', models: '', vision_models: '', enabled: true, is_default: false,
  })
  dialogVisible.value = true
}

async function save() {
  if (!form.name.trim() || !form.vendor.trim() || !form.models.trim()) {
    ElMessage.warning('请填写 厂商名称 / 标识 / 可用模型')
    return
  }
  saving.value = true
  try {
    if (form.id) {
      await opsApi().put(`/providers/${form.id}`, form)
    } else {
      await opsApi().post('/providers', form)
    }
    ElMessage.success('已保存')
    dialogVisible.value = false
    load()
  } catch (e) {
    ElMessage.error(e.detail || '保存失败')
  } finally {
    saving.value = false
  }
}

async function remove(row) {
  await ElMessageBox.confirm(`确定删除厂商「${row.name}」？`, '删除确认', { type: 'warning' })
  await opsApi().delete(`/providers/${row.id}`)
  ElMessage.success('已删除')
  load()
}

async function test(row) {
  testVisible.value = true
  testResult.value = null
  try {
    const r = await opsApi().post(`/providers/${row.id}/test`)
    testResult.value = r
  } catch (e) {
    testResult.value = { ok: false, message: e.detail || '测试失败' }
  }
}

onMounted(load)
</script>

<style scoped>
.head { display: flex; align-items: center; justify-content: space-between; margin-bottom: 6px; }
.head h2 { font-size: 16px; margin: 0; }
.hint { color: #6b7280; font-size: 13px; margin: 0 0 12px; }
.test-body { padding: 12px; border-radius: 6px; font-size: 13px; }
.test-body.ok { background: #ecfdf5; color: #065f46; }
.test-body.err { background: #fef2f2; color: #991b1b; }
.test-title { font-weight: 600; margin-bottom: 6px; }
.test-msg { word-break: break-all; }
</style>
