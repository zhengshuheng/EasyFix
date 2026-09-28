<template>
  <div class="settings">
    <el-card shadow="never">
      <el-tabs v-model="activeTab" class="mgmt-tabs">
        <!-- 通用配置 -->
        <el-tab-pane label="通用配置" name="general">
          <div class="tab-content general-config">
            <div class="gen-config-form">
              <el-form :model="appConfigForm" label-width="120px" style="max-width: 480px">
                <el-form-item label="默认学期">
                  <el-select v-model="appConfigForm.defaultSemester" placeholder="选择默认学期" clearable style="width: 100%">
                    <el-option label="上学期" :value="1" />
                    <el-option label="下学期" :value="2" />
                  </el-select>
                  <div class="form-tip">仅用于首次启动（未手动选过学期）时默认进入的学期</div>
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="saveAppConfig" :loading="savingAppConfig">保存配置</el-button>
                </el-form-item>
              </el-form>
              <el-alert type="info" :closable="false" style="margin-top: 8px">
                <template #title>
                  各小孩的年级已不再全局配置：请到「账号管理」为每个小孩设置入学日期，系统会自动推断当前年级，点选小孩即进入对应年级学习空间。
                </template>
              </el-alert>
            </div>
            <el-card class="sys-info-card" shadow="never">
              <template #header><span>系统信息</span></template>
              <el-descriptions :column="1" size="small">
                <el-descriptions-item label="服务状态">{{ healthText }}</el-descriptions-item>
                <el-descriptions-item label="运行端口">{{ portText }}</el-descriptions-item>
                <el-descriptions-item label="数据存储">backend/easyfix_main.db（主库，仅本机）</el-descriptions-item>
                <el-descriptions-item label="运行模式">本地单机 · 数据不出本机</el-descriptions-item>
              </el-descriptions>
            </el-card>
          </div>
        </el-tab-pane>

        <!-- OCR配置 -->
        <el-tab-pane label="OCR配置" name="ocr">
          <el-form :model="ocrForm" label-width="120px" style="max-width: 600px">
            <el-form-item label="OCR服务商">
              <el-select v-model="ocrForm.provider" placeholder="选择OCR服务商">
                <el-option label="多模态模型 (推荐)" value="multimodal" />
                <el-option label="百度OCR" value="baidu" />
                <el-option label="腾讯OCR" value="tencent" />
                <el-option label="PaddleOCR (本地)" value="paddleocr" />
                <el-option label="Tesseract (本地)" value="tesseract" />
              </el-select>
            </el-form-item>

            <!-- 多模态模型配置 -->
            <el-divider v-if="ocrForm.provider === 'multimodal'">多模态模型OCR配置</el-divider>
            <el-form-item v-if="ocrForm.provider === 'multimodal'" label="厂商">
              <el-select v-model="ocrForm.vendor" placeholder="选择平台提供的厂商" style="width: 100%" @change="onOcrVendorChange">
                <el-option v-for="p in ocrProviders" :key="p.vendor" :label="`${p.name}（${p.vendor}）`" :value="p.vendor" />
              </el-select>
            </el-form-item>
            <el-form-item v-if="ocrForm.provider === 'multimodal'" label="模型">
              <el-select v-model="ocrForm.multimodal_model" placeholder="选择平台提供的模型" style="width: 100%">
                <el-option v-for="m in ocrVendorModels" :key="m" :label="m" :value="m" />
              </el-select>
              <div class="form-tip">
                订阅制下无需配置 API Key，多模态模型由平台统一提供；如列表为空，说明当前厂商未配置视觉模型（不支持多模态 OCR），请联系运营在「AI 模型市场」填写视觉模型。
              </div>
            </el-form-item>

            <!-- 传统OCR配置 -->
            <el-divider v-if="ocrForm.provider === 'baidu'">百度OCR配置</el-divider>
            <el-form-item v-if="ocrForm.provider === 'baidu'" label="API Key">
              <el-input v-model="ocrForm.baidu_api_key" placeholder="请输入百度OCR API Key" show-password />
            </el-form-item>
            <el-form-item v-if="ocrForm.provider === 'baidu'" label="Secret Key">
              <el-input v-model="ocrForm.baidu_secret_key" placeholder="请输入百度OCR Secret Key" show-password />
            </el-form-item>
            <el-form-item v-if="ocrForm.provider === 'baidu'">
              <el-alert type="info" :closable="false">
                <template #title>
                  百度OCR计费：¥1/1000次 | <a href="https://cloud.baidu.com/product/ocr" target="_blank">前往申请</a>
                </template>
              </el-alert>
            </el-form-item>

            <el-divider v-if="ocrForm.provider === 'tencent'">腾讯OCR配置</el-divider>
            <el-form-item v-if="ocrForm.provider === 'tencent'" label="App ID">
              <el-input v-model="ocrForm.tencent_app_id" placeholder="请输入腾讯App ID" />
            </el-form-item>
            <el-form-item v-if="ocrForm.provider === 'tencent'" label="Secret ID">
              <el-input v-model="ocrForm.tencent_secret_id" placeholder="请输入Secret ID" show-password />
            </el-form-item>
            <el-form-item v-if="ocrForm.provider === 'tencent'" label="Secret Key">
              <el-input v-model="ocrForm.tencent_secret_key" placeholder="请输入Secret Key" show-password />
            </el-form-item>
            <el-form-item v-if="ocrForm.provider === 'tencent'" label="Bucket">
              <el-input v-model="ocrForm.tencent_bucket" placeholder="请输入Bucket名称" />
            </el-form-item>
            <el-form-item v-if="ocrForm.provider === 'tencent'">
              <el-alert type="info" :closable="false">
                <template #title>
                  腾讯OCR计费：¥0.0015/次 | <a href="https://cloud.tencent.com/product/ocr" target="_blank">前往申请</a>
                </template>
              </el-alert>
            </el-form-item>

            <el-divider v-if="ocrForm.provider === 'paddleocr'">PaddleOCR配置 (本地)</el-divider>
            <el-form-item v-if="ocrForm.provider === 'paddleocr'">
              <el-alert type="success" :closable="false">
                <template #title>
                  PaddleOCR为本地OCR引擎，无需API密钥，但需要安装paddlepaddle。<br>
                  安装命令：pip install paddlepaddle paddleocr<br>
                  注意：需要Python 3.10以下环境
                </template>
              </el-alert>
            </el-form-item>

            <el-divider v-if="ocrForm.provider === 'tesseract'">Tesseract配置 (本地)</el-divider>
            <el-form-item v-if="ocrForm.provider === 'tesseract'" label="Tesseract路径">
              <el-input v-model="ocrForm.tesseract_path" placeholder="如：C:\Program Files\Tesseract-OCR\tesseract.exe" />
            </el-form-item>
            <el-form-item v-if="ocrForm.provider === 'tesseract'">
              <el-alert type="success" :closable="false">
                <template #title>
                  Tesseract为开源本地OCR引擎，需要单独安装。<br>
                  下载地址：https://github.com/UB-Mannheim/tesseract/wiki<br>
                  中文语言包：chi_sim (简体中文)
                </template>
              </el-alert>
            </el-form-item>

            <el-form-item>
              <el-button type="primary" @click="saveOcrConfig" :loading="saving">
                保存OCR配置
              </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <!-- 自定义OCR -->
        <el-tab-pane label="自定义OCR" name="custom">
          <el-form :model="customForm" label-width="120px" style="max-width: 800px">
            <el-form-item label="接口地址">
              <el-input v-model="customForm.api_url" placeholder="自定义OCR API接口地址" />
            </el-form-item>
            <el-form-item label="请求方法">
              <el-select v-model="customForm.method">
                <el-option label="POST" value="POST" />
                <el-option label="GET" value="GET" />
              </el-select>
            </el-form-item>
            <el-form-item label="请求头">
              <el-input
                v-model="customForm.headers"
                type="textarea"
                :rows="3"
                placeholder='{"Content-Type": "application/json", "Authorization": "Bearer xxx"}'
              />
            </el-form-item>
            <el-form-item label="请求体模板">
              <el-input
                v-model="customForm.body_template"
                type="textarea"
                :rows="4"
                placeholder='{"image": "${base64_image}"}'
              />
              <div class="form-tip">
                支持变量：${base64_image} (图片Base64), ${image_path} (图片路径)
              </div>
            </el-form-item>
            <el-form-item label="结果提取">
              <el-input
                v-model="customForm.response_parser"
                type="textarea"
                :rows="2"
                placeholder='response.words_result.map(w => w.words).join("\n")'
              />
              <div class="form-tip">
                JavaScript表达式，从API响应中提取文字
              </div>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveCustomConfig" :loading="saving">
                保存自定义配置
              </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>

        <!-- LLM配置（订阅制：无需配置 Key，只选模型名） -->
        <el-tab-pane label="LLM配置" name="llm">
          <el-form :model="llmForm" label-width="120px" style="max-width: 600px">
            <el-form-item label="AI 厂商">
              <el-select v-model="llmForm.vendor" placeholder="选择平台提供的厂商" style="width: 100%" @change="onLlmVendorChange">
                <el-option v-for="p in llmProviders" :key="p.vendor" :label="`${p.name}（${p.vendor}）`" :value="p.vendor" />
              </el-select>
            </el-form-item>
            <el-form-item label="AI 模型">
              <el-select v-model="llmForm.model" placeholder="选择平台提供的模型" style="width: 100%">
                <el-option v-for="m in llmVendorModels" :key="m" :label="m" :value="m" />
              </el-select>
              <div class="form-tip">
                订阅制下无需配置 API Key，模型由平台统一提供；如列表为空，请联系运营在后台配置 AI 网关。
              </div>
            </el-form-item>
            <el-form-item>
              <el-button type="primary" @click="saveLlmConfig" :loading="saving">
                保存LLM配置
              </el-button>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
      </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { configApi } from '@/api/question'
import { useAppConfigStore } from '@/stores/appConfig'

const appConfigStore = useAppConfigStore()
const activeTab = ref('general')
const saving = ref(false)
const loading = ref(false)

const healthText = ref('检测中…')
const portText = ref(window.location.port || '80')

async function fetchHealth() {
  try {
    const res = await fetch('/health')
    const data = await res.json()
    healthText.value = data.status === 'ok' ? '✅ 服务正常' : '⚠️ 服务异常'
  } catch {
    healthText.value = '❌ 无法连接'
  }
}

// 通用配置：默认学期（年级已改为按小孩入学日期自动推断，不再全局配置）
const appConfigForm = reactive({
  defaultSemester: null,
})
const savingAppConfig = ref(false)

const loadAppConfig = async () => {
  await appConfigStore.load(true)
  appConfigForm.defaultSemester = appConfigStore.defaultSemester
}

const saveAppConfig = async () => {
  savingAppConfig.value = true
  try {
    await appConfigStore.save({
      defaultSemester: appConfigForm.defaultSemester,
    })
    ElMessage.success('默认学期配置已保存')
  } catch (e) {
    ElMessage.error('保存失败')
  } finally {
    savingAppConfig.value = false
  }
}

const ocrForm = reactive({
  provider: 'multimodal',
  // 多模态模型（订阅制：只选厂商+模型名，Key 由平台 AI 网关统一提供）
  multimodal_model: '',
  vendor: '',
  // 百度
  baidu_api_key: '',
  baidu_secret_key: '',
  // 腾讯
  tencent_app_id: '',
  tencent_secret_id: '',
  tencent_secret_key: '',
  tencent_bucket: '',
  // 本地
  tesseract_path: '',
})
const ocrModels = ref([])
const ocrProviders = ref([])
const ocrVendorModels = computed(() => {
  // 只列该厂商的视觉模型；vision_models 留空 = 不支持 OCR（模型列表为空，前端显示提示）
  const p = ocrProviders.value.find((x) => x.vendor === ocrForm.vendor)
  return p ? p.vision_models : ocrModels.value
})
function onOcrVendorChange() {
  ocrForm.multimodal_model = ''
}

const customForm = reactive({
  api_url: '',
  method: 'POST',
  headers: '{}',
  body_template: '{"image": "${base64_image}"}',
  response_parser: 'response.words_result?.map(w => w.words).join("\\n") || ""',
})

const llmForm = reactive({
  model: '',
  vendor: '',
})
const llmModels = ref([])
const llmProviders = ref([])
const llmVendorModels = computed(() => {
  const p = llmProviders.value.find((x) => x.vendor === llmForm.vendor)
  return p ? p.models : llmModels.value
})
function onLlmVendorChange() {
  llmForm.model = ''
}

const saveOcrConfig = async () => {
  saving.value = true
  try {
    await configApi.saveOcrConfig(ocrForm)
    ElMessage.success('OCR配置已保存')
  } catch (error) {
    ElMessage.error('保存失败: ' + (error.message || '未知错误'))
  } finally {
    saving.value = false
  }
}

const saveCustomConfig = async () => {
  saving.value = true
  try {
    await configApi.saveCustomOcrConfig(customForm)
    ElMessage.success('自定义OCR配置已保存')
  } catch (error) {
    ElMessage.error('保存失败: ' + (error.message || '未知错误'))
  } finally {
    saving.value = false
  }
}

const saveLlmConfig = async () => {
  saving.value = true
  try {
    await configApi.saveLlmConfig({ model: llmForm.model, vendor: llmForm.vendor })
    ElMessage.success('LLM配置已保存')
  } catch (error) {
    ElMessage.error('保存失败: ' + (error.message || '未知错误'))
  } finally {
    saving.value = false
  }
}

const loadConfigs = async () => {
  loading.value = true
  try {
    const { data: ocrData } = await configApi.getOcrConfig()
    Object.assign(ocrForm, ocrData)
    ocrModels.value = ocrData.multimodal_models || []
    ocrProviders.value = ocrData.multimodal_providers || []
    if (!ocrForm.vendor && ocrProviders.value.length) {
      ocrForm.vendor = ocrProviders.value.find((p) => p.is_default)?.vendor || ocrProviders.value[0].vendor
    }

    const { data: customData } = await configApi.getCustomOcrConfig()
    Object.assign(customForm, customData)

    const { data: llmData } = await configApi.getLlmConfig()
    llmForm.model = llmData.model || llmData.default_model || ''
    llmForm.vendor = llmData.vendor || ''
    llmModels.value = llmData.models || []
    llmProviders.value = llmData.providers || []
    if (!llmForm.vendor && llmProviders.value.length) {
      llmForm.vendor = llmProviders.value.find((p) => p.is_default)?.vendor || llmProviders.value[0].vendor
    }
  } catch (error) {
    console.error('加载配置失败:', error)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  // 家长中心已统一密码验证，进入即加载配置
  loadConfigs()
  loadAppConfig()
  fetchHealth()
})
</script>

<style scoped>
.settings {
  width: 100%;
}

.tab-content {
  padding: 10px 0;
}

/* 系统配置子导航：顶部横向 tabs */
.mgmt-tabs :deep(.el-tabs__item) {
  height: 44px;
  line-height: 44px;
  font-size: 14px;
}

.mgmt-tabs :deep(.el-tabs__content) {
  padding: 12px 2px 0;
  overflow: visible;
}

.general-config {
  display: flex;
  gap: 24px;
  align-items: flex-start;
  flex-wrap: wrap;
}

.gen-config-form {
  flex: 0 0 480px;
  max-width: 520px;
}

.sys-info-card {
  flex: 1 1 260px;
  min-width: 260px;
  background: #fafbfc;
  border-color: #ebeef5;
}

.sys-info-card :deep(.el-card__header) {
  padding: 12px 16px;
  font-weight: bold;
  background: #f0f2f5;
}

.sys-info-card :deep(.el-card__body) {
  padding: 16px;
}

.sys-info-card :deep(.el-descriptions__label) {
  color: #909399;
}

.form-tip {
  font-size: 12px;
  color: #999;
  margin-top: 5px;
}

.el-divider {
  margin: 20px 0 10px;
}

/* ============ 移动端：设置卡片单列全宽 ============
 * 桌面 .gen-config-form 是 flex-basis 480px 且 flex-shrink:0，
 * 375px 屏上换行后仍是 480px 宽 → 横向溢出（body overflow-x 裁掉右缘）。
 * 移动端改为 100% 全宽，系统信息卡同步占满。 */
@media screen and (max-width: 768px) {
  .general-config {
    gap: 16px;
  }
  .gen-config-form {
    flex: 1 1 100%;
    max-width: 100%;
  }
  .sys-info-card {
    flex: 1 1 100%;
    min-width: 0;
  }
}
</style>
