<template>
  <div class="words">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>英语单词库（全局共享，家长统一管理）</span>
          <div>
            <el-button type="primary" @click="showAddDialog">
              <el-icon><Plus /></el-icon>
              新增单词
            </el-button>
            <el-button type="info" @click="showImportDialog">
              <el-icon><Upload /></el-icon>
              导入单词
            </el-button>
          </div>
        </div>
      </template>

      <!-- 筛选条件 -->
      <div class="filters">
        <el-input
          v-model="filters.keyword"
          placeholder="搜索单词"
          clearable
          @change="fetchWords"
          style="width: 180px"
        />
        <el-select v-if="subjectStore.isAllGrade" v-model="filters.grade" placeholder="年级" clearable @change="fetchWords" style="width: 120px">
          <el-option v-for="g in gradeOptions" :key="g.value" :label="g.label" :value="g.value" />
        </el-select>
        <el-select v-model="filters.semester" placeholder="学期" clearable @change="fetchWords" style="width: 100px">
          <el-option label="上学期" :value="1" />
          <el-option label="下学期" :value="2" />
        </el-select>
        <el-select v-model="filters.tag_id" placeholder="标签" clearable @change="fetchWords" style="width: 150px">
          <el-option v-for="t in allTags" :key="t.id" :label="t.name" :value="t.id" />
        </el-select>
      </div>

      <!-- 单词列表 -->
      <el-table
        ref="tableRef"
        :data="words.items"
        stripe
        style="width: 100%; margin-top: 20px"
        @sort-change="handleSortChange"
      >
        <el-table-column prop="english" label="英文" width="210">
          <template #default="{ row }">
            <div class="word-cell">
              <span class="word-english">{{ row.english }}</span>
              <el-button class="audio-btn-table" @click.stop="playWordAudio(row.id)" :loading="audioLoading" circle>
                <span v-if="!audioLoading">🔊</span>
              </el-button>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="chinese" label="中文" min-width="200" />
        <el-table-column prop="phonetic" label="音标" width="150">
          <template #default="{ row }">
            <span class="phonetic">{{ row.phonetic || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column label="属性" width="150">
          <template #default="{ row }">
            <el-tag v-if="row.grade" :style="{ fontSize: '14px' }">{{ row.grade }}年级</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="280" fixed="right">
          <template #default="{ row }">
            <el-button type="info" size="default" @click="viewDetail(row)">详情</el-button>
            <el-button type="primary" size="default" @click="editWord(row)">编辑</el-button>
            <el-button type="danger" size="default" @click="deleteWord(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.limit"
          :page-sizes="[10, 20, 50, 100]"
          :total="words.total"
          layout="total, sizes, prev, pager, next"
          @change="fetchWords"
        />
      </div>
    </el-card>

    <!-- 新增/编辑弹窗 -->
    <el-dialog v-model="dialogVisible" :title="dialogTitle" width="500px">
      <el-form :model="form" label-width="80px">
        <el-form-item label="英文" required>
          <el-input v-model="form.english" placeholder="输入英文单词" />
        </el-form-item>
        <el-form-item label="中文" required>
          <el-input v-model="form.chinese" placeholder="输入中文释义" />
        </el-form-item>
        <el-form-item label="音标">
          <el-input v-model="form.phonetic" placeholder="输入音标（可选）" />
        </el-form-item>
        <el-form-item label="年级">
          <el-select v-model="form.grade" placeholder="选择年级" clearable style="width: 100%">
            <el-option v-for="g in gradeOptions" :key="g.value" :label="g.label" :value="g.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="学期">
          <el-select v-model="form.semester" placeholder="选择学期" clearable style="width: 100%">
            <el-option label="上学期" :value="1" />
            <el-option label="下学期" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="标签">
          <el-select v-model="form.tag_ids" multiple placeholder="选择标签" style="width: 100%">
            <el-option v-for="t in allTags" :key="t.id" :label="t.name" :value="t.id" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="saveWord">保存</el-button>
      </template>
    </el-dialog>

    <!-- 详情弹窗 -->
    <el-dialog v-model="detailVisible" title="单词详情" width="600px">
      <el-tabs v-if="detailVisible" v-model="activeTab">
        <el-tab-pane label="基本信息" name="info">
          <el-form label-width="80px" size="default">
            <el-form-item label="英文">
              {{ detailWord.english }}
              <el-button class="audio-btn" @click="playWordAudio(detailWord.id)" :loading="audioLoading" size="small">🔊</el-button>
            </el-form-item>
            <el-form-item label="中文">{{ detailWord.chinese }}</el-form-item>
            <el-form-item label="音标">{{ detailWord.phonetic || '-' }}</el-form-item>
            <el-form-item label="年级">{{ detailWord.grade ? detailWord.grade + '年级' : '-' }}</el-form-item>
            <el-form-item label="学期">{{ detailWord.semester === 1 ? '上学期' : detailWord.semester === 2 ? '下学期' : '-' }}</el-form-item>
            <el-form-item label="标签">
              <el-tag v-for="t in detailWord.tags" :key="t.id" style="margin-right: 5px">{{ t.name }}</el-tag>
              <span v-if="!detailWord.tags || detailWord.tags.length === 0">-</span>
            </el-form-item>
          </el-form>
        </el-tab-pane>
      </el-tabs>
      <template #footer>
        <el-button @click="detailVisible = false">关闭</el-button>
      </template>
    </el-dialog>

    <!-- 导入弹窗 -->
    <el-dialog v-model="importDialogVisible" title="导入单词" width="1100px" class="import-dialog">
      <el-form :model="importForm" label-width="100px">
        <el-form-item label="导入方式">
          <el-radio-group v-model="importForm.mode">
            <el-radio label="text">文本粘贴</el-radio>
            <el-radio label="file">文件上传</el-radio>
            <el-radio label="image">图片识别</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item v-if="importForm.mode === 'text'" label="单词格式">
          <el-input
            v-model="importForm.text"
            type="textarea"
            :rows="6"
            placeholder="每行一个单词，格式：英文 中文（用空格分隔）
例如：
apple 苹果
banana 香蕉
orange 橙子"
            @input="onTextChange"
          />
        </el-form-item>
        <el-form-item v-else-if="importForm.mode === 'file'" label="上传文件">
          <el-upload
            ref="uploadRef"
            :auto-upload="false"
            :limit="1"
            accept=".txt,.csv"
            :on-change="handleFileChange"
          >
            <el-button>选择文件</el-button>
            <template #tip>
              <div class="el-upload__tip">支持 .txt 或 .csv 文件，每行一个单词，格式：英文 中文</div>
            </template>
          </el-upload>
        </el-form-item>
        <el-form-item v-else-if="importForm.mode === 'image'" label="上传图片">
          <el-upload
            ref="imageUploadRef"
            :auto-upload="false"
            :limit="1"
            accept="image/*"
            :on-change="handleImageChange"
            :on-remove="handleImageRemove"
          >
            <el-button>选择图片</el-button>
            <template #tip>
              <div class="el-upload__tip">支持 JPG、PNG 格式，图片中的单词文字将被识别提取</div>
            </template>
          </el-upload>
          <!-- OCR识别结果预览 -->
          <div v-if="importForm.ocrText" class="ocr-preview">
            <div class="ocr-label">OCR原始识别：</div>
            <el-input
              v-model="importForm.ocrText"
              type="textarea"
              :rows="4"
              placeholder="OCR识别的原始文本"
              @input="importForm.parsedWords = smartParseWords(importForm.ocrText)"
            />
          </div>
        </el-form-item>

        <!-- 单词预览表格 -->
        <el-form-item v-if="importForm.parsedWords.length > 0" label="单词预览">
          <div class="words-preview">
            <el-table :data="importForm.parsedWords" border stripe size="small" max-height="300">
              <el-table-column prop="english" label="英文" width="150">
                <template #default="{ row }">
                  <el-input v-model="row.english" size="small" />
                </template>
              </el-table-column>
              <el-table-column prop="chinese" label="中文" min-width="150">
                <template #default="{ row }">
                  <el-input v-model="row.chinese" size="small" />
                </template>
              </el-table-column>
              <el-table-column prop="phonetic" label="音标" width="120">
                <template #default="{ row }">
                  <el-input v-model="row.phonetic" size="small" placeholder="可选" />
                </template>
              </el-table-column>
              <el-table-column label="操作" width="60" fixed="right">
                <template #default="{ $index }">
                  <el-button type="danger" size="small" link @click="importForm.parsedWords.splice($index, 1)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
            <div class="preview-summary">共 {{ importForm.parsedWords.length }} 个单词</div>
          </div>
        </el-form-item>

        <el-form-item label="默认年级">
          <el-select v-model="importForm.grade" placeholder="选择年级（可选）" clearable style="width: 100%">
            <el-option v-for="g in gradeOptions" :key="g.value" :label="g.label" :value="g.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="默认学期">
          <el-select v-model="importForm.semester" placeholder="选择学期（可选）" clearable style="width: 100%">
            <el-option label="上学期" :value="1" />
            <el-option label="下学期" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="标签">
          <el-select v-model="importForm.tag_ids" multiple placeholder="选择标签（可选）" style="width: 100%">
            <el-option v-for="t in allTags" :key="t.id" :label="t.name" :value="t.id" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="importDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="importWords" :loading="importing">导入</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Edit, Printer, Upload } from '@element-plus/icons-vue'
import { wordApi } from '@/api/word'
import { questionApi } from '@/api/question'
import { motivationApi } from '@/api/motivation'
import { useAppConfigStore } from '@/stores/appConfig'
import { useSubjectStore } from '@/stores/subject'

const route = useRoute()
const appConfigStore = useAppConfigStore()
const subjectStore = useSubjectStore()
const words = ref({ total: 0, items: [] })
const allTags = ref([])
const filters = reactive({
  keyword: '',
  grade: null,
  semester: null,
  tag_id: null,
  sort_by: null,
  sort_order: 'desc',
})
const pagination = reactive({
  page: 1,
  limit: 20,
})

const dialogVisible = ref(false)
const dialogTitle = ref('新增单词')
const isEdit = ref(false)
const currentWordId = ref(null)

const form = reactive({
  english: '',
  chinese: '',
  phonetic: '',
  grade: null,
  semester: null,
  tag_ids: [],
})

const gradeOptions = [
  { label: '一年级', value: 1 },
  { label: '二年级', value: 2 },
  { label: '三年级', value: 3 },
  { label: '四年级', value: 4 },
  { label: '五年级', value: 5 },
  { label: '六年级', value: 6 },
  { label: '初一', value: 7 },
  { label: '初二', value: 8 },
  { label: '初三', value: 9 },
  { label: '高一', value: 10 },
  { label: '高二', value: 11 },
  { label: '高三', value: 12 },
]

// 打印相关
const printDialogVisible = ref(false)
const printForm = reactive({
  count: 25,
  grade: appConfigStore.defaultGrade,
})

// 导入相关
const importDialogVisible = ref(false)
const importing = ref(false)
const uploadRef = ref()
const imageUploadRef = ref()
const importForm = reactive({
  mode: 'text',
  text: '',
  file: null,
  image: null,
  ocrText: '',
  parsedWords: [],  // 解析后的单词预览
  grade: appConfigStore.defaultGrade,
  semester: appConfigStore.defaultSemester,
  tag_ids: [],
})

// 详情弹窗相关
const detailVisible = ref(false)
const detailWord = ref({})
const activeTab = ref('info')

const viewDetail = async (row) => {
  detailWord.value = row
  activeTab.value = 'info'
  detailVisible.value = true
}

// 处理表格排序变化（使用后端排序）
const handleSortChange = ({ prop, order }) => {
  if (!prop) {
    // 取消排序
    filters.sort_by = null
    filters.sort_order = 'desc'
  } else {
    // 其他字段使用后端排序
    filters.sort_by = prop
    filters.sort_order = order === 'ascending' ? 'asc' : 'desc'
  }
  pagination.page = 1 // 重置到第一页
  fetchWords()
}

const fetchWords = async () => {
  try {
    const params = {
      skip: (pagination.page - 1) * pagination.limit,
      limit: pagination.limit,
    }
    if (filters.keyword) params.keyword = filters.keyword
    if (filters.grade) params.grade = filters.grade
    if (filters.semester) params.semester = filters.semester
    if (filters.tag_id) params.tag_ids = filters.tag_id
    if (filters.sort_by) {
      params.sort_by = filters.sort_by
      params.sort_order = filters.sort_order
    }

    const { data } = await wordApi.list(params)
    words.value = data
  } catch (error) {
    ElMessage.error('获取单词列表失败')
  }
}

const fetchTags = async () => {
  try {
    const { data } = await questionApi.listTags()
    allTags.value = data
  } catch (error) {
    console.error('获取标签失败:', error)
  }
}

const showAddDialog = () => {
  dialogTitle.value = '新增单词'
  isEdit.value = false
  resetForm()
  dialogVisible.value = true
}

const editWord = (row) => {
  dialogTitle.value = '编辑单词'
  isEdit.value = true
  currentWordId.value = row.id
  form.english = row.english
  form.chinese = row.chinese
  form.phonetic = row.phonetic || ''
  form.grade = row.grade
  form.semester = row.semester
  form.tag_ids = row.tags ? row.tags.map(t => t.id) : []
  dialogVisible.value = true
}

const resetForm = () => {
  form.english = ''
  form.chinese = ''
  form.phonetic = ''
  form.grade = appConfigStore.defaultGrade
  form.semester = appConfigStore.defaultSemester
  form.tag_ids = []
}

const saveWord = async () => {
  if (!form.english || !form.chinese) {
    ElMessage.warning('请填写必填项')
    return
  }

  try {
    if (isEdit.value) {
      await wordApi.update(currentWordId.value, form)
      ElMessage.success('更新成功')
    } else {
      await wordApi.create(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchWords()
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

const deleteWord = async (row) => {
  try {
    await ElMessageBox.confirm('确定删除该单词吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await wordApi.delete(row.id)
    ElMessage.success('删除成功')
    fetchWords()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 打印
const showPrintDialog = () => {
  printDialogVisible.value = true
}

const generatePrintPdf = async () => {
  try {
    const params = { count: printForm.count }
    if (printForm.grade) params.grade = printForm.grade

    const { data } = await wordApi.printPdf(params)
    window.open(data.pdf_url, '_blank')
    printDialogVisible.value = false
    ElMessage.success('PDF已生成')
  } catch (error) {
    ElMessage.error('生成PDF失败')
  }
}

// 导入
const showImportDialog = () => {
  importForm.mode = 'text'
  importForm.text = ''
  importForm.file = null
  importForm.image = null
  importForm.ocrText = ''
  importForm.parsedWords = []
  importForm.grade = null
  importForm.semester = null
  importForm.tag_ids = []
  importDialogVisible.value = true
}

const handleFileChange = (file) => {
  onFileChange(file)
}

const handleImageChange = async (file) => {
  importForm.image = file.raw
  // 自动调用OCR识别
  await recognizeImage(file.raw)
}

const handleImageRemove = () => {
  importForm.image = null
  importForm.ocrText = ''
  importForm.parsedWords = []
}

// 文本模式变化时更新预览
const onTextChange = () => {
  if (importForm.mode === 'text' && importForm.text.trim()) {
    importForm.parsedWords = smartParseWords(importForm.text)
  }
}

// 文件模式变化时
const onFileChange = (file) => {
  importForm.file = file.raw
  if (file.raw) {
    const reader = new FileReader()
    reader.onload = e => {
      importForm.parsedWords = smartParseWords(e.target.result)
    }
    reader.readAsText(file.raw)
  }
}

const recognizeImage = async (file) => {
  try {
    const formData = new FormData()
    formData.append('file', file)

    const response = await fetch('/api/upload/image', {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      throw new Error('OCR识别失败')
    }

    const result = await response.json()
    if (result.ocr_result && result.ocr_result.full_text) {
      importForm.ocrText = result.ocr_result.full_text
      // 智能分隔单词并更新预览
      importForm.parsedWords = smartParseWords(result.ocr_result.full_text)
      ElMessage.success('图片识别成功，请检查识别结果')
    } else {
      ElMessage.warning('未识别到文字，请上传更清晰的图片')
    }
  } catch (error) {
    console.error('OCR error:', error)
    ElMessage.error('图片识别失败，请尝试其他方式导入')
  }
}

// 智能分隔单词 - 自动识别英文和中文
const smartParseWords = (text) => {
  // 清理OCR噪声字符（保留\n\r）
  const cleaned = text
    .replace(/[\u0001-\u0009\u000B\u000C\u000E-\u001F\u007F-\u009F]/g, '') // 移除控制字符（保留\n\r即10和13）
    .replace(/['']/g, "'")  // 规范化撇号
    .replace(/[""]/g, '"')
    .replace(/（/g, '(').replace(/）/g, ')')  // 规范化中文括号
    .replace(/[ \t]+/g, ' ')   // 规范化空格（保留换行）

  const words = []

  // 按行分割
  const lines = cleaned.split('\n')

  for (const line of lines) {
    const trimmed = line.trim()
    if (!trimmed) continue

    // 分割本行的各个单词（按制表符或连续空格分割）
    // 格式如: "1.mess 杂乱  2.whose 谁的" 或 "1.mess 杂乱\t2.whose 谁的"
    const entries = trimmed.split(/(?:\t|  +)(?=\d+\.)/)

    for (const entry of entries) {
      if (!entry.trim()) continue

      // 去掉序号前缀，如 "1.mess" 或 "1. mess"
      let content = entry.replace(/^\d+\.?\s*/, '').trim()
      if (!content) continue

      let phonetic = ''
      let english = ''
      let chinese = ''

      // 先提取音标 /eɪ/ 或 [音标] 格式（可能在末尾或中间）
      // 提取末尾的 /音标/ 格式
      const phoneticMatch = content.match(/\/([^\/]+)\/$/)
      if (phoneticMatch) {
        phonetic = phoneticMatch[1]
        content = content.replace(/\/[^\/]+\/$/, '').trim()
      }
      // 提取 [音标] 格式
      const bracketPhonetic = content.match(/\[([^\]]+)\]/)
      if (bracketPhonetic) {
        phonetic = bracketPhonetic[1]
        content = content.replace(/\[[^\]]+\]/, '').trim()
      }

      // 去掉末尾的括号注释如 (复数)
      content = content.replace(/\s*\([^)]*\)\s*$/, '').trim()

      // 分离英文和中文
      // 格式1: 英文 + 空格 + 中文（如 "mess 杂乱" 或 "school bag 书包"）
      // 格式2: 只有英文或只有中文
      // 格式3: 英文 + 空格 + 音标（如 "baby /eɪ/"）

      // 尝试按空格分割
      const parts = content.split(/\s+/)

      if (parts.length >= 2) {
        // 检查第一部分是否是纯英文
        const firstPart = parts[0]
        const isEnglish = /^[a-zA-Z][a-zA-Z'-]*$/.test(firstPart) ||
                          /^[a-zA-Z][a-zA-Z'-]*(?:\s+[a-zA-Z][a-zA-Z'-]*)+$/.test(firstPart)

        if (isEnglish) {
          english = firstPart
          // 剩余部分是中文或其他
          const rest = parts.slice(1).join(' ').trim()
          if (rest) {
            // 检查是否是音标格式
            if (rest.startsWith('/') && rest.endsWith('/')) {
              phonetic = rest.slice(1, -1)
            } else {
              chinese = rest
            }
          }
        } else {
          // 第一部分不是纯英文，可能是中文
          chinese = content
        }
      } else if (parts.length === 1) {
        // 只有一个部分
        const part = parts[0]
        if (/^[a-zA-Z][a-zA-Z'-]*$/.test(part) || /^[a-zA-Z][a-zA-Z'-]*(?:\s+[a-zA-Z][a-zA-Z'-]*)+$/.test(part)) {
          // 纯英文
          english = part
        } else {
          // 纯中文
          chinese = part
        }
      }

      if (english || chinese) {
        words.push({
          english: english || '',
          chinese: chinese || '',
          phonetic: phonetic || '',
          original: entry
        })
      }
    }
  }

  return words
}

const parseTextToWords = (text) => {
  const lines = text.trim().split('\n')
  const words = []
  for (const line of lines) {
    const trimmed = line.trim()
    if (!trimmed) continue
    // 智能分隔
    const parsed = smartParseWords(trimmed)
    if (parsed.length > 0) {
      words.push(parsed[0])
    }
  }
  return words
}

const importWords = async () => {
  let words = []

  // 优先使用预览表格中的数据（用户可能已编辑）
  if (importForm.parsedWords && importForm.parsedWords.length > 0) {
    words = importForm.parsedWords.filter(w => w.english && w.chinese)
  } else if (importForm.mode === 'text') {
    if (!importForm.text.trim()) {
      ElMessage.warning('请输入单词内容')
      return
    }
    words = smartParseWords(importForm.text)
  } else if (importForm.mode === 'file') {
    if (!importForm.file) {
      ElMessage.warning('请选择文件')
      return
    }
    // 读取文件内容
    try {
      const reader = new FileReader()
      const fileContent = await new Promise((resolve, reject) => {
        reader.onload = e => resolve(e.target.result)
        reader.onerror = reject
        reader.readAsText(importForm.file)
      })
      words = smartParseWords(fileContent)
    } catch (error) {
      ElMessage.error('读取文件失败')
      return
    }
  } else if (importForm.mode === 'image') {
    if (!importForm.ocrText.trim()) {
      ElMessage.warning('请先上传图片并等待识别完成')
      return
    }
    words = smartParseWords(importForm.ocrText)
  }

  if (words.length === 0) {
    ElMessage.warning('未解析到有效单词')
    return
  }

  importing.value = true
  let successCount = 0
  let failCount = 0

  for (const word of words) {
    try {
      await wordApi.create({
        english: word.english,
        chinese: word.chinese,
        phonetic: word.phonetic || undefined,
        grade: importForm.grade,
        semester: importForm.semester,
        tag_ids: importForm.tag_ids,
      })
      successCount++
    } catch (error) {
      failCount++
    }
  }

  importing.value = false
  importDialogVisible.value = false

  ElMessage.success(`导入完成：成功 ${successCount} 个，失败 ${failCount} 个`)
  fetchWords()
}

onMounted(async () => {
  await appConfigStore.load()
  // 首页年级维度跳转：/words?grade=6；学习空间指定年级优先
  const routeGrade = Number(route.query.grade)
  if (subjectStore.activeGrade !== null) {
    filters.grade = subjectStore.activeGrade
  } else if (routeGrade) {
    filters.grade = routeGrade
  } else if (filters.grade == null) {
    filters.grade = appConfigStore.defaultGrade
  }
  if (filters.semester == null) filters.semester = appConfigStore.defaultSemester
  if (reviewConfig.grade == null) reviewConfig.grade = subjectStore.activeGrade !== null ? subjectStore.activeGrade : appConfigStore.defaultGrade
  if (printForm.grade == null) printForm.grade = subjectStore.activeGrade !== null ? subjectStore.activeGrade : appConfigStore.defaultGrade
  if (importForm.grade == null) importForm.grade = subjectStore.activeGrade !== null ? subjectStore.activeGrade : appConfigStore.defaultGrade
  if (importForm.semester == null) importForm.semester = appConfigStore.defaultSemester
  fetchWords()
  fetchTags()
})
</script>

<style scoped>
.words {
  width: 100%;
  min-width: 0;
  max-width: 1400px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filters {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.word-english {
  font-weight: bold;
  color: #409eff;
  font-size: 16px;
}

.word-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.word-cell .word-english {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.phonetic {
  color: #909399;
  font-family: monospace;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

/* 喇叭按钮通用样式 */
.audio-btn {
  font-size: 20px;
  padding: 8px 12px;
  border-radius: 50%;
  margin-left: 8px;
  vertical-align: middle;
}

.audio-btn-table {
  font-size: 13px;
  flex-shrink: 0;
  margin-left: 0;
}

/* 禁用卡片的hover效果 */
.words :deep(.el-card) {
  transition: none;
}
.words :deep(.el-card:hover) {
  transform: none;
  box-shadow: var(--shadow-sm) !important;
}
</style>

<style>
.toast-large.el-message {
  font-size: 24px !important;
  padding: 20px 30px !important;
  min-width: 300px !important;
}
.toast-large.el-message .el-message__content {
  font-size: 24px !important;
}
</style>
