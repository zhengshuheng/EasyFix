<template>
  <el-card shadow="never">
    <h2 style="font-size:16px;margin:0 0 4px;">⚙️ 系统设置</h2>
    <p class="hint">AI 网关旧配置保留为默认厂商兜底；模型市场上线后学生端优先选择厂商 + 模型。</p>

    <el-tabs v-model="tab">
      <el-tab-pane label="体验与价格" name="price">
        <el-form label-width="140px" class="cfg-form">
          <el-form-item label="免费体验天数"><el-input-number v-model="cfg.trial_days" :min="0" :max="365" /></el-form-item>
          <el-form-item label="云端订阅价（元）"><el-input-number v-model="cfg.online_price" :min="0" /></el-form-item>
          <el-form-item label="本地版价格（元）"><el-input-number v-model="cfg.local_price" :min="0" /></el-form-item>
          <el-form-item label="本地版下载地址"><el-input v-model="cfg.local_download_url" placeholder="https://…" /></el-form-item>
          <el-form-item label="本地版引导地址"><el-input v-model="cfg.local_guide_url" placeholder="https://…" /></el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="运营账号" name="account">
        <el-form label-width="140px" class="cfg-form">
          <el-form-item label="运营账号"><el-input v-model="cfg.ops_username" /></el-form-item>
          <el-form-item label="运营口令"><el-input v-model="cfg.ops_password" type="password" show-password /></el-form-item>
          <el-alert title="修改运营账号/口令会立即生效；保存后请用新凭证重新登录" type="warning" :closable="false" show-icon />
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="AI 网关（默认厂商）" name="gateway">
        <el-form label-width="140px" class="cfg-form">
          <el-form-item label="协议">
            <el-select v-model="cfg.ai_gateway_provider" style="width:200px;">
              <el-option label="OpenAI 兼容" value="openai" />
              <el-option label="Anthropic" value="anthropic" />
            </el-select>
          </el-form-item>
          <el-form-item label="Base URL"><el-input v-model="cfg.ai_gateway_base_url" placeholder="https://api.openai.com/v1" /></el-form-item>
          <el-form-item label="API Key"><el-input v-model="cfg.ai_gateway_api_key" type="password" show-password /></el-form-item>
          <el-form-item label="可用模型"><el-input v-model="cfg.ai_gateway_models" placeholder="逗号分隔，如 gpt-4o,gpt-4o-mini" /></el-form-item>
          <el-form-item label="默认模型"><el-input v-model="cfg.ai_gateway_default_model" placeholder="如 gpt-4o-mini" /></el-form-item>
          <el-form-item>
            <el-button @click="testGateway" :loading="testing">测试连通</el-button>
            <span v-if="testResult" :style="{ color: testOk ? '#16a34a' : '#dc2626', marginLeft: '10px' }">{{ testResult }}</span>
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>

    <div class="actions">
      <el-button type="primary" :loading="saving" @click="save">保存设置</el-button>
    </div>
  </el-card>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { opsApi } from '../api/ops.js'

const tab = ref('price')
const cfg = reactive({})
const saving = ref(false)
const testing = ref(false)
const testResult = ref('')
const testOk = ref(false)

async function loadCfg() {
  const d = await opsApi().get('/config')
  Object.assign(cfg, d.config)
}

async function save() {
  saving.value = true
  try {
    await opsApi().put('/config', { values: { ...cfg } })
    ElMessage.success('设置已保存')
  } finally {
    saving.value = false
  }
}

async function testGateway() {
  testing.value = true
  testResult.value = ''
  try {
    await opsApi().post('/ai-gateway/test', {})
    testOk.value = true
    testResult.value = '连通正常 ✓'
  } catch (e) {
    testOk.value = false
    testResult.value = '连通失败（见上方错误提示）'
  } finally {
    testing.value = false
  }
}

onMounted(loadCfg)
</script>

<style scoped>
.hint { color: #6b7280; font-size: 13px; margin: 0 0 16px; }
.cfg-form { max-width: 560px; margin-top: 8px; }
.actions { margin-top: 16px; }
</style>
