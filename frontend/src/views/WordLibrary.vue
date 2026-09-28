<template>
  <div class="words">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>英语单词库（全局共享，家长统一管理）</span>
          <div>
            <el-button type="primary" @click="openWordSyncDialog">
              <el-icon><Refresh /></el-icon>
              同步最新单词
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
        <div class="filter-item">
          <span class="filter-label">年级</span>
          <el-select v-model="filters.grade" placeholder="全部年级" clearable @change="fetchWords" style="width: 120px">
            <el-option v-for="g in gradeOptions" :key="g.value" :label="g.label" :value="g.value" />
          </el-select>
        </div>
        <div class="filter-item">
          <span class="filter-label">学期</span>
          <el-select v-model="filters.semester" placeholder="全部学期" clearable @change="fetchWords" style="width: 100px">
            <el-option label="上学期" :value="1" />
            <el-option label="下学期" :value="2" />
          </el-select>
        </div>
        <div class="filter-item">
          <span class="filter-label">标签</span>
          <el-select v-model="filters.tag_id" placeholder="全部标签" clearable filterable @change="fetchWords" style="width: 150px">
            <el-option v-for="t in allTags" :key="t.id" :label="t.name" :value="t.id" />
          </el-select>
        </div>
        <el-button @click="resetFilters">重置</el-button>
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
              <el-button class="audio-btn-table" @click.stop="playWordAudio(row.id)" :loading="isAudioLoading(row.id)" circle>
                <span v-if="!isAudioLoading(row.id)">🔊</span>
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
        <el-table-column label="单元" width="180">
          <template #default="{ row }">
            <span v-if="row.unit" class="unit-cell">Unit {{ row.unit }}<span v-if="row.unit_title" class="unit-title"> {{ row.unit_title }}</span></span>
            <span v-else class="unit-cell muted">—</span>
          </template>
        </el-table-column>
        <el-table-column label="年级/学期/标签" width="220">
          <template #default="{ row }">
            <div class="attr-cell">
              <el-tag v-if="row.grade" size="small">{{ row.grade }}年级</el-tag>
              <el-tag v-if="row.semester" size="small" type="info">
                {{ row.semester === 1 ? '上学期' : '下学期' }}
              </el-tag>
              <el-tag v-for="t in row.tags || []" :key="t.id" size="small" type="success">
                {{ t.name }}
              </el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="280" fixed="right">
          <template #default="{ row }">
            <el-button type="info" size="default" @click="viewDetail(row)">详情</el-button>
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
        <el-form-item label="单元">
          <div style="display: flex; gap: 8px; width: 100%">
            <el-input-number v-model="form.unit" :min="1" :max="99" placeholder="单元号" controls-position="right" style="width: 120px" />
            <el-input v-model="form.unit_title" placeholder="单元标题（可选，如 Meeting new people）" />
          </div>
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
              <el-button class="audio-btn" @click="playWordAudio(detailWord.id)" :loading="isAudioLoading(detailWord.id)" size="small">🔊</el-button>
            </el-form-item>
            <el-form-item label="中文">{{ detailWord.chinese }}</el-form-item>
            <el-form-item label="音标">{{ detailWord.phonetic || '-' }}</el-form-item>
            <el-form-item label="年级">{{ detailWord.grade ? detailWord.grade + '年级' : '-' }}</el-form-item>
            <el-form-item label="学期">{{ detailWord.semester === 1 ? '上学期' : detailWord.semester === 2 ? '下学期' : '-' }}</el-form-item>
            <el-form-item label="单元">{{ detailWord.unit ? 'Unit ' + detailWord.unit + (detailWord.unit_title ? ' ' + detailWord.unit_title : '') : '-' }}</el-form-item>
            <el-form-item label="标签">
              <el-tag v-for="t in detailWord.tags" :key="t.id" style="margin-right: 5px">{{ t.name }}</el-tag>
              <span v-if="!detailWord.tags || detailWord.tags.length === 0">-</span>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="记忆增强" name="memory">
          <div v-if="!detailWord.phonetic_rule && !detailWord.word_root && !(detailWord.example_sentences && detailWord.example_sentences.length)" class="mem-empty">
            <p>记忆增强（拼读规则 / 词根词源 / 相关词 / 语境例句）会在<b>新增 / 导入单词时自动生成</b>，无需手动操作。</p>
            <p class="mem-tip">刚导入的单词请稍等片刻，重新打开详情即可看到。</p>
          </div>
          <template v-else>
            <el-form label-width="90px" size="default">
              <el-form-item label="拼读规则">
                <span class="mem-text">{{ detailWord.phonetic_rule || '-' }}</span>
              </el-form-item>
              <el-form-item label="词根词源">
                <span class="mem-text">{{ detailWord.word_root || '-' }}</span>
              </el-form-item>
              <el-form-item label="相关词">
                <template v-if="detailWord.related_words && detailWord.related_words.length">
                  <el-tag v-for="(r, i) in detailWord.related_words" :key="i" style="margin-right: 6px" @click="playWordAudioByEnglish(r.en)">
                    🔊 {{ r.en }} {{ r.cn }}
                  </el-tag>
                </template>
                <span v-else>-</span>
              </el-form-item>
              <el-form-item label="例句">
                <template v-if="detailWord.example_sentences && detailWord.example_sentences.length">
                  <div v-for="(s, i) in detailWord.example_sentences" :key="i" class="mem-ex">
                    <div class="mem-ex-en">{{ s.en }} <el-button size="small" text title="朗读句子" @click="speakEn(s.en)">🔊</el-button></div>
                    <div class="mem-ex-zh">{{ s.zh }}</div>
                  </div>
                </template>
                <span v-else>-</span>
              </el-form-item>
            </el-form>
          </template>
          <el-divider />
          <div class="mem-batch">
            <p class="mem-tip">老单词缺拼读/词根/例句时，可筛选条件批量补生成（不覆盖已编辑字段）：</p>
            <div class="mem-batch-row">
              <el-select v-model="enhanceForm.grade" placeholder="年级" clearable style="width: 110px">
                <el-option v-for="g in 12" :key="g" :label="g + '年级'" :value="g" />
              </el-select>
              <el-select v-model="enhanceForm.semester" placeholder="学期" clearable style="width: 100px">
                <el-option label="上学期" :value="1" />
                <el-option label="下学期" :value="2" />
              </el-select>
              <el-input-number v-model="enhanceForm.limit" :min="1" :max="50" style="width: 120px" />
              <el-button type="primary" :loading="enhancing" @click="runEnhance">补生成</el-button>
            </div>
            <p v-if="enhanceResult" class="mem-tip">{{ enhanceResult }}</p>
          </div>
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
            <el-radio label="ai">🤖 AI 智能导入</el-radio>
            <el-radio label="text">文本粘贴</el-radio>
            <el-radio label="file">文件上传</el-radio>
            <el-radio label="image">图片识别</el-radio>
            <el-radio label="textbook">📚 教材单词表提取</el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item v-if="importForm.mode === 'ai'" label="AI 导入">
          <div style="width: 100%">
            <el-radio-group v-model="aiForm.mode" style="margin-bottom: 10px">
              <el-radio label="textbook">教材模式（选教材即可，无需输入指令）</el-radio>
              <el-radio label="custom">自定义指令（输入一句话）</el-radio>
            </el-radio-group>

            <div v-if="aiForm.mode === 'textbook'" style="display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin-bottom: 8px">
              <el-select v-model="aiForm.version" placeholder="教材版本" style="width: 300px" filterable>
                <el-option v-for="v in aiVersions" :key="v" :label="v" :value="v" />
              </el-select>
              <el-select v-model="aiForm.grade" placeholder="年级" style="width: 110px">
                <el-option v-for="g in 6" :key="g" :label="g + '年级'" :value="g" />
              </el-select>
              <el-select v-model="aiForm.semester" placeholder="册次" style="width: 110px" clearable>
                <el-option label="上册" :value="1" />
                <el-option label="下册" :value="2" />
              </el-select>
            </div>
            <el-input
              v-else
              v-model="aiForm.instruction"
              type="textarea"
              :rows="3"
              placeholder="用一句话描述要导入的单词，例如：我要导入沪教版深圳英语三年级上册 全册；或：人教版PEP五年级下册第三单元的单词"
              style="margin-bottom: 8px"
            />
            <el-button
              type="primary"
              :loading="aiGenerating"
              :disabled="(aiForm.mode === 'textbook' ? !aiForm.version || !aiForm.grade : !aiForm.instruction || !aiForm.instruction.trim())"
              @click="generateAiWords"
            >{{ aiForm.mode === 'textbook' ? '生成全册单词表' : 'AI 生成单词' }}</el-button>
            <el-button
              v-if="aiForm.mode === 'textbook' && aiForm.version && !aiVersions.includes(aiForm.version)"
              size="small"
              type="warning"
              plain
              @click="aiForm.mode = 'custom'; aiForm.instruction = '我要导入' + aiForm.version + '的单词表'"
            >版本不在列表中，改用自定义指令导入</el-button>
          </div>
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
        <el-form-item v-else-if="importForm.mode === 'textbook'" label="教材单词表">
          <div style="width: 100%">
            <el-upload
              v-model:file-list="importForm.textbookFiles"
              :auto-upload="false"
              multiple
              accept="image/*,.pdf"
              :limit="10"
            >
              <el-button>选择照片 / PDF</el-button>
              <template #tip>
                <div class="el-upload__tip">上传教材里的<b>「单元单词表」页</b>照片（可多张）或自备教材 PDF；本地 OCR → AI 提取单词，照片/PDF 即用即删</div>
              </template>
            </el-upload>
            <el-button
              type="primary"
              style="margin-top: 8px"
              :loading="extracting"
              :disabled="importForm.textbookFiles.length === 0"
              @click="extractTextbookWords"
            >开始提取</el-button>
          </div>
        </el-form-item>

        <!-- 单词预览表格 -->
        <el-form-item v-if="importForm.parsedWords.length > 0" label="单词预览">
          <div class="words-preview">
            <el-table :data="importForm.parsedWords" border stripe size="small" max-height="300">
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
              <el-table-column label="单元" width="150">
                <template #default="{ row }">
                  <span v-if="row.unit" class="unit-cell">Unit {{ row.unit }}<span v-if="row.unit_title" class="unit-title"> {{ row.unit_title }}</span></span>
                  <span v-else class="unit-cell muted">—</span>
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
    <!-- 同步最新单词弹窗（Ops 一键同步 1-6 年级） -->
    <el-dialog v-model="wordSyncVisible" title="同步最新单词" width="420px">
      <p style="color: #909399; font-size: 13px; margin: 0 0 14px">从内置教材词汇库一键同步所选版本的 1~6 年级全部单元单词（全量覆盖，教材数据由运营统一维护）。</p>
      <el-form label-width="80px" @submit.prevent>
        <el-form-item label="版本" required>
          <el-select v-model="wordSyncForm.version" placeholder="选择教材版本" style="width: 100%">
            <el-option v-for="v in wordSyncVersions" :key="v" :label="v" :value="v" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="wordSyncVisible = false">取消</el-button>
        <el-button type="primary" :loading="wordSyncing" :disabled="!wordSyncForm.version" @click="doWordSync">
          一键同步
        </el-button>
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
import { syncApi } from '@/api/sync'
import http from '@/api/http'
import { questionApi } from '@/api/question'
import { motivationApi } from '@/api/motivation'
import { useSubjectStore } from '@/stores/subject'
import { speakEn as ttsSpeakEn, playServerTts } from '@/utils/speech'

const route = useRoute()
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
  unit: null,
  unit_title: '',
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
  grade: null,
})

// 导入相关
const importDialogVisible = ref(false)
const importing = ref(false)

// 同步最新单词（Ops 一键同步）
const wordSyncVisible = ref(false)
const wordSyncing = ref(false)
const wordSyncForm = reactive({ version: '' })
const wordSyncVersions = ref([])

const openWordSyncDialog = async () => {
  wordSyncVisible.value = true
  wordSyncForm.version = ''
  wordSyncVersions.value = []
  try {
    const { data } = await syncApi.status()
    const subjects = data.catalog?.subjects || {}
    const englishBooks = subjects['英语'] || {}
    const versions = Object.keys(englishBooks).filter(v =>
      Object.values(englishBooks[v] || {}).some(b => (b.words || 0) > 0))
    wordSyncVersions.value = versions
    if (versions.length) wordSyncForm.version = versions[0]
  } catch {
    wordSyncVersions.value = []
  }
}

const doWordSync = async () => {
  if (wordSyncing.value || !wordSyncForm.version) return
  wordSyncing.value = true
  try {
    const { data } = await syncApi.syncWordsAll({ version: wordSyncForm.version })
    ElMessage.success(`已同步 ${data.added} 个单词（${wordSyncForm.version} 1~6 年级 ${data.books?.length || 8} 册）`)
    wordSyncVisible.value = false
    fetchWords()
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '同步失败，请稍后重试')
  } finally {
    wordSyncing.value = false
  }
}
const uploadRef = ref()
const imageUploadRef = ref()
const importForm = reactive({
  mode: 'text',
  text: '',
  file: null,
  image: null,
  ocrText: '',
  parsedWords: [],  // 解析后的单词预览
  textbookFiles: [], // 教材单词表提取上传的文件列表
  grade: null,
  semester: null,
  tag_ids: [],
})
const extracting = ref(false)

// AI 智能导入
const aiGenerating = ref(false)
const aiVersions = ref([])
const aiForm = reactive({
  mode: 'textbook',
  version: '',
  grade: null,
  semester: null,
  instruction: '',
})

const loadAiVersions = async () => {
  try {
    const { data } = await http.get('/textbook/catalog')
    const books = data.books || []
    // 教材版本下拉：列出「英语」科目的版本，去重保序
    const vers = []
    for (const b of books) {
      if ((b.subject || '').includes('英语')) {
        const v = (b.version || '').trim()
        if (v && !vers.includes(v)) vers.push(v)
      }
    }
    if (vers.length === 0) {
      // 目录不可用时兜底常见英语教材版本
      vers.push('沪教版（深圳，一年级起点）', '人教版（PEP）（三年级起点）（主编：吴欣）', '外研社版（三年级起点）（主编：陈琳）', '北师大版', '冀教版（三年级起点）')
    }
    aiVersions.value = vers
  } catch (e) {
    console.error('加载教材版本失败:', e)
  }
}
loadAiVersions()

const generateAiWords = async () => {
  if (aiGenerating.value) return
  aiGenerating.value = true
  try {
    const payload = { mode: aiForm.mode }
    if (aiForm.mode === 'textbook') {
      payload.subject = '英语'
      payload.version = aiForm.version
      payload.grade = aiForm.grade
      payload.semester = aiForm.semester || null
    } else {
      payload.instruction = aiForm.instruction
    }
    const { data } = await wordApi.aiGenerate(payload)
    if (!data.words || data.words.length === 0) {
      ElMessage.warning(data.detail || 'AI 未生成任何单词，请调整后重试')
      return
    }
    // 教材模式下同步年级/学期到底部「默认年级/学期」，导入入库时保持一致
    if (aiForm.mode === 'textbook') {
      importForm.grade = aiForm.grade
      importForm.semester = aiForm.semester || null
    }
    importForm.parsedWords = data.words.map(w => ({
      english: w.english,
      chinese: w.chinese,
      phonetic: w.phonetic || '',
      unit: w.unit,
      unit_title: w.unit_title || '',
      existing: !!w.existing,
      checked: !w.existing,
    }))
    ElMessage.success(`AI 生成 ${data.words.length} 个单词，请核对后导入`)
  } catch (error) {
    console.error('AI 生成失败:', error)
    ElMessage.error((error.response && error.response.data && error.response.data.detail) || 'AI 生成失败，请检查大模型配置或稍后重试')
  } finally {
    aiGenerating.value = false
  }
}

// 详情弹窗相关
const detailVisible = ref(false)
const detailWord = ref({})
const activeTab = ref('info')

const viewDetail = async (row) => {
  detailWord.value = row
  activeTab.value = 'info'
  detailVisible.value = true
}

// 正在加载/播放音频的单词 id（按单词隔离 loading，避免点击一个全部图标转圈）
const audioLoadingMap = reactive({})
const isAudioLoading = (wordId) => !!audioLoadingMap[wordId]

// 播放单词音频（Promise 在播放结束/失败时 resolve）
const playWordAudio = async (wordId) => {
  if (!wordId || audioLoadingMap[wordId]) return
  audioLoadingMap[wordId] = true

  try {
    const response = await wordApi.getAudio(wordId)
    const blob = response.data
    const audioUrl = URL.createObjectURL(blob)
    const audio = new Audio(audioUrl)

    await new Promise((resolve) => {
      audio.onended = () => {
        audioLoadingMap[wordId] = false
        URL.revokeObjectURL(audioUrl)
        resolve()
      }
      audio.onerror = () => {
        audioLoadingMap[wordId] = false
        URL.revokeObjectURL(audioUrl)
        resolve()
      }
      audio.play().catch(() => {
        audioLoadingMap[wordId] = false
        URL.revokeObjectURL(audioUrl)
        resolve()
      })
    })
  } catch (e) {
    console.error('音频播放失败:', e)
    ElMessage.warning('音频播放失败')
    audioLoadingMap[wordId] = false
  }
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

// 清空全部筛选条件后重新拉取
const resetFilters = () => {
  filters.keyword = ''
  filters.grade = null
  filters.semester = null
  filters.tag_id = null
  filters.sort_by = null
  filters.sort_order = 'desc'
  pagination.page = 1
  fetchWords()
}

// ============ 记忆增强（自动附带） ============
// 记忆增强（拼读规则/词根词源/相关词）在新增/导入单词时由后端后台自动生成，无需手动触发；
// 详情弹窗「记忆增强」tab 直接展示已生成内容。

// 示例词/相关词按英文直接播放
const playWordAudioByEnglish = (en) => {
  if (!en) return
  playServerTts(en)
}

// 例句英文朗读：统一走 utils/speech（浏览器语音 + 服务器 TTS 降级）
const speakEn = (text) => {
  if (!text) return
  ttsSpeakEn(text)
}

// 批量补生成记忆增强（老单词缺拼读/词根/例句时手动触发）
const enhanceForm = reactive({ grade: null, semester: null, limit: 20 })
const enhancing = ref(false)
const enhanceResult = ref('')
const runEnhance = async () => {
  enhancing.value = true
  enhanceResult.value = ''
  try {
    const payload = { limit: enhanceForm.limit || 20 }
    if (enhanceForm.grade) payload.grade = enhanceForm.grade
    if (enhanceForm.semester) payload.semester = enhanceForm.semester
    const { data } = await wordApi.enhance(payload)
    if (data && data.detail) {
      enhanceResult.value = data.detail
    } else if (data && data.ok_count > 0) {
      enhanceResult.value = `已生成 ${data.ok_count} 个单词的记忆增强`
    }
    if (data && data.ok_count > 0) fetchWords()
  } catch (e) {
    enhanceResult.value = '生成失败：' + (e?.response?.data?.detail || e.message || '未知错误')
  } finally {
    enhancing.value = false
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
  form.unit = row.unit ?? null
  form.unit_title = row.unit_title || ''
  form.tag_ids = row.tags ? row.tags.map(t => t.id) : []
  dialogVisible.value = true
}

const resetForm = () => {
  form.english = ''
  form.chinese = ''
  form.phonetic = ''
  form.grade = null
  form.semester = null
  form.unit = null
  form.unit_title = ''
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
      ElMessage.success('创建成功（记忆增强自动生成中）')
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
  importForm.textbookFiles = []
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

  // 当前单元上下文（文本可含 Unit N 标题行）
  let curUnit = null
  let curUnitTitle = ''

  for (const line of lines) {
    const trimmed = line.trim()
    if (!trimmed) continue

    // 识别单元标题行：Unit 1 Meeting new people（该行不作为单词）
    const unitMatch = trimmed.match(/^Unit\s*(\d+)\s*(.*)$/i)
    if (unitMatch) {
      curUnit = parseInt(unitMatch[1], 10)
      curUnitTitle = (unitMatch[2] || '').trim()
      continue
    }

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

      // 去掉末尾的括号注释如 (复数) —— 保留中文释义里的括号（如 "tooth 牙齿(复数teeth)"）
      // 由下方 CJK 切分后仅在英文侧剥离英文注释括号（如 "first (1st)"）

      // 分离英文和中文：英文在前、中文在后，以第一个中文字符为界
      // （支持多词英文如 "a pair of 一双"、括号释义如 "tooth 牙齿(复数teeth)"）
      const cjkIdx = content.search(/[\u4e00-\u9fa5\u3000-\u303f\uff00-\uffef]/)
      if (cjkIdx >= 0) {
        let english = content.slice(0, cjkIdx).trim()
        let chinese = content.slice(cjkIdx).trim()
        // 英文尾部剥掉英文注释括号（如 first (1st)），多词英文保留
        english = english.replace(/\s*\([^)]*\)\s*$/, '').trim()
        // 英文尾部未闭合的括号（如 "woof (狗叫声)汪汪" 切出 "woof ("）：括号及之后并入中文
        const openParen = english.lastIndexOf('(')
        if (openParen >= 0 && !english.slice(openParen).includes(')')) {
          chinese = english.slice(openParen) + chinese
          english = english.slice(0, openParen).trim()
        }
        // 特例：英文尾部孤立大写字母 + 中文首字（如 "T-shirt T恤衫" → "T-shirt" + "T恤衫"）
        const capM = english.match(/(^|\s)([A-Z])$/)
        if (capM && chinese && /^[\u4e00-\u9fa5]/.test(chinese)) {
          english = english.slice(0, capM.index).trim()
          chinese = capM[2] + chinese
        }
        if (english || chinese) {
          words.push({
            english,
            chinese,
            phonetic: phonetic || '',
            unit: curUnit,
            unit_title: curUnitTitle,
            original: entry
          })
        }
        continue
      }

      // 无中文：尝试按空格分割（纯英文 / 英文+音标）
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
          unit: curUnit,
          unit_title: curUnitTitle,
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

// 教材单词表提取（OCR + AI，松耦合独立于教材同步）
const extractTextbookWords = async () => {
  if (importForm.textbookFiles.length === 0) {
    ElMessage.warning('请先选择单词表照片或 PDF')
    return
  }
  extracting.value = true
  try {
    const formData = new FormData()
    for (const f of importForm.textbookFiles) {
      if (f.raw) formData.append('files', f.raw)
    }
    if (importForm.grade) formData.append('grade', importForm.grade)
    if (importForm.semester) formData.append('semester', importForm.semester)
    const { data } = await wordApi.extractFromTextbook(formData)
    if (!data.words || data.words.length === 0) {
      ElMessage.warning(data.detail || '未提取到单词，请确认上传的是单词表页')
      return
    }
    importForm.parsedWords = data.words.map(w => ({
      english: w.english,
      chinese: w.chinese,
      phonetic: w.phonetic || '',
      existing: !!w.existing,
      checked: !w.existing,
    }))
    ElMessage.success(data.detail || `提取到 ${data.words.length} 个单词`)
  } catch (error) {
    console.error('提取失败:', error)
    ElMessage.error('提取失败，请稍后重试')
  } finally {
    extracting.value = false
  }
}

const importWords = async () => {
  let words = []

  // 优先使用预览表格中的数据（用户可能已编辑）
  if (importForm.parsedWords && importForm.parsedWords.length > 0) {
    // checked === false 的行不导入（教材提取的「已存在」词默认不勾选）
    words = importForm.parsedWords.filter(w => w.checked !== false && w.english && w.chinese)
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
    if (importForm.mode === 'textbook' && importForm.parsedWords.length > 0) {
      ElMessage.warning('没有可导入的单词：已存在的已默认排除，如需强制导入请勾选对应行')
    } else {
      ElMessage.warning('未解析到有效单词')
    }
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
        unit: word.unit || undefined,
        unit_title: word.unit_title || undefined,
        tag_ids: importForm.tag_ids,
      })
      successCount++
    } catch (error) {
      failCount++
    }
  }

  importing.value = false
  importDialogVisible.value = false

  ElMessage.success(`导入完成：成功 ${successCount} 个，失败 ${failCount} 个（记忆增强自动生成中）`)
  fetchWords()
}

onMounted(async () => {
  // 筛选默认值只依赖「当前学习空间 + 路由」，先算好再拉数据：
  // 学习空间指定年级优先（/words?grade=N），否则「全部年级」；学期一律默认「全部学期」。
  // 不做静默过滤，避免用户未选择时列表被过滤成空。
  const routeGrade = Number(route.query.grade)
  if (subjectStore.activeGrade !== null) {
    filters.grade = subjectStore.activeGrade
  } else if (routeGrade) {
    filters.grade = routeGrade
  } else {
    filters.grade = null
  }
  filters.semester = null

  // 先出数据：不等待应用配置接口，配置异常也不会让列表空白
  fetchWords()
  fetchTags()

  // 表单默认年级只跟随当前学习空间（家长中心为空时留空由用户自选），
  // 不再套用系统配置的「默认年级」，避免各表单互相干扰
  if (reviewConfig.grade == null) reviewConfig.grade = subjectStore.activeGrade
  if (printForm.grade == null) printForm.grade = subjectStore.activeGrade
  if (importForm.grade == null) importForm.grade = subjectStore.activeGrade
  if (aiForm.grade == null) aiForm.grade = subjectStore.activeGrade
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
  align-items: center;
}

.filter-item {
  display: inline-flex;
  align-items: center;
  gap: 6px;
}

.filter-label {
  color: #606266;
  font-size: 14px;
  white-space: nowrap;
}

.attr-cell {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

.unit-cell {
  font-size: 13px;
  color: #606266;
  white-space: nowrap;
}
.unit-cell .unit-title {
  color: #909399;
}
.unit-cell.muted {
  color: #c0c4cc;
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

/* 记忆增强 */
.mem-empty {
  text-align: center;
  padding: 30px 0;
  color: #999;
}
.mem-empty p {
  margin-bottom: 14px;
}
.mem-empty .mem-tip {
  margin-bottom: 0;
  font-size: 12px;
  color: #bbb;
}
.mem-text {
  white-space: pre-wrap;
  line-height: 1.7;
  color: #444;
}
.mem-ex {
  margin-bottom: 10px;
}
.mem-ex-en {
  font-size: 16px;
  color: #303133;
  display: flex;
  align-items: center;
}
.mem-ex-zh {
  font-size: 13px;
  color: #909399;
  margin-top: 2px;
}
.mem-batch {
  padding-top: 4px;
}
.mem-batch-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
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
