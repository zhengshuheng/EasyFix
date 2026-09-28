<template>
  <div class="management">
    <el-card shadow="never">
      <div class="mgmt-topbar">
        <span class="mgmt-title">家长中心</span>
        <el-button class="mgmt-guide-btn" text @click="guideVisible = true">
          <el-icon><Reading /></el-icon>
          使用指南
        </el-button>
      </div>
      <el-tabs v-model="activeTab" class="mgmt-tabs">
        <!-- 学科管理 -->
        <el-tab-pane label="学科管理" name="subjects">
          <div class="tab-content">
            <div class="action-bar">
              <el-button type="primary" @click="showSubjectDialog = true">
                <el-icon><Plus /></el-icon>
                新增学科
              </el-button>
            </div>
            <el-table :data="subjects" stripe style="width: 100%; margin-top: 15px">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="name" label="学科名称">
                <template #default="{ row }">
                  {{ row.name }}
                  <el-tag v-if="isBuiltinSubject(row)" size="small" type="info" style="margin-left: 6px">系统内置</el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="120">
                <template #default="{ row }">
                  <el-button link type="danger" size="small" :disabled="isBuiltinSubject(row)" @click="deleteSubject(row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>

        <!-- 标签管理 -->
        <el-tab-pane label="标签管理" name="tags">
          <div class="tab-content">
            <div class="action-bar">
              <el-button type="primary" @click="showTagDialog = true">
                <el-icon><Plus /></el-icon>
                新增标签
              </el-button>
            </div>
            <el-table :data="tags" stripe style="width: 100%; margin-top: 15px">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="name" label="标签名称">
                <template #default="{ row }">
                  {{ row.name }}
                  <el-tag v-if="isBuiltinTag(row)" size="small" type="info" style="margin-left: 6px">系统内置</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="color" label="颜色" width="120">
                <template #default="{ row }">
                  <el-tag :style="{ backgroundColor: row.color, color: '#fff' }">{{ row.color || '默认' }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="120">
                <template #default="{ row }">
                  <el-button link type="danger" size="small" :disabled="isBuiltinTag(row)" @click="deleteTag(row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>

        <!-- 错误类型管理 -->
        <el-tab-pane label="错误类型管理" name="errorTypes">
          <div class="tab-content">
            <div class="action-bar">
              <el-button type="primary" @click="openErrorTypeDialog">
                <el-icon><Plus /></el-icon>
                新增错误类型
              </el-button>
            </div>
            <el-table :data="errorTypes" stripe style="width: 100%; margin-top: 15px">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="name" label="类型名称">
                <template #default="{ row }">
                  {{ row.name }}
                  <el-tag v-if="isBuiltinErrorType(row)" size="small" type="info" style="margin-left: 6px">系统内置</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="subject_name" label="学科" width="120" />
              <el-table-column label="操作" width="180">
                <template #default="{ row }">
                  <el-button type="primary" size="default" @click="editErrorType(row)">编辑</el-button>
                  <el-button type="danger" size="default" :disabled="isBuiltinErrorType(row)" @click="deleteErrorType(row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>

        <!-- 知识点管理 -->
        <el-tab-pane label="知识点管理" name="knowledgePoints">
          <div class="tab-content">
            <!-- 筛选：与运营平台对齐 = 学科/版本/年级/册次/搜索（标签/要求/类型不再作为过滤维度） -->
            <div class="kp-filter-bar">
              <div class="kp-filter-group">
                <span class="kp-filter-label">学科</span>
                <div class="kp-filter-chips">
                  <el-radio-group v-model="kpFilterSubject" size="small" @change="applyKpFilter">
                    <el-radio-button :value="null">全部学科</el-radio-button>
                    <el-radio-button v-for="s in subjects" :key="s.id" :value="s.id">{{ s.name }}</el-radio-button>
                  </el-radio-group>
                </div>
              </div>
              <div class="kp-filter-group">
                <span class="kp-filter-label">版本</span>
                <div class="kp-filter-chips">
                  <el-radio-group v-model="kpFilterEdition" size="small" @change="applyKpFilter">
                    <el-radio-button v-for="v in kpEditionOptions" :key="v.key" :value="v.key">{{ v.label }}</el-radio-button>
                  </el-radio-group>
                  <span v-if="!kpEditionOptions.length" class="kp-filter-empty">（暂无，可在 同步最新知识点 导入教材版本）</span>
                </div>
              </div>
              <div class="kp-filter-group">
                <span class="kp-filter-label">年级</span>
                <div class="kp-filter-chips">
                  <el-radio-group v-model="kpFilterGrade" size="small" @change="applyKpFilter">
                    <el-radio-button :value="null">全部年级</el-radio-button>
                    <el-radio-button v-for="g in gradeOptions" :key="g.value" :value="g.value">{{ g.label }}</el-radio-button>
                  </el-radio-group>
                </div>
              </div>
              <div class="kp-filter-group">
                <span class="kp-filter-label">册次</span>
                <div class="kp-filter-chips">
                  <el-radio-group v-model="kpFilterSemester" size="small" @change="applyKpFilter">
                    <el-radio-button :value="null">全部册次</el-radio-button>
                    <el-radio-button :value="1">上册</el-radio-button>
                    <el-radio-button :value="2">下册</el-radio-button>
                  </el-radio-group>
                </div>
              </div>
              <div class="kp-filter-group">
                <span class="kp-filter-label">搜索</span>
                <div class="kp-filter-chips">
                  <el-input v-model="kpFilterQ" placeholder="搜索名称/章节" clearable size="small" style="width: 200px" @keyup.enter="applyKpFilter" @clear="applyKpFilter" />
                  <el-button size="small" type="primary" @click="applyKpFilter">查询</el-button>
                </div>
              </div>
            </div>
            <div class="action-bar" style="display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin-top: 10px">
              <el-button type="primary" @click="openKpSyncDialog">
                <el-icon><Refresh /></el-icon>
                同步最新知识点
              </el-button>
              <el-button :type="kpGrouped ? 'primary' : 'default'" plain size="small" style="margin-left: auto" @click="toggleKpGrouped">
                {{ kpGrouped ? '平铺视图' : '按单元分组' }}
              </el-button>
            </div>
            <div class="kp-summary">
              <span class="kp-path">{{ kpFilterText }}（共 {{ knowledgePoints.length }} 条）</span>
            </div>
            <!-- 按单元分组视图 -->
            <el-collapse v-if="kpGrouped" v-model="kpOpenChapters" class="kp-groups" style="margin-top: 10px">
              <el-collapse-item v-for="g in kpGroups" :key="g.key" :name="g.key">
                <template #title>
                  <span class="kp-group-title">{{ g.label }}</span>
                  <span class="kp-group-count">{{ g.items.length }} 条</span>
                </template>
                <el-table :data="g.items" stripe style="width: 100%">
                  <el-table-column prop="id" label="ID" width="70" />
                  <el-table-column prop="name" label="知识点名称" min-width="240" show-overflow-tooltip />
                  <el-table-column label="标签" width="150">
                    <template #default="{ row }">
                      <el-tag v-for="t in (row.tags || [])" :key="t" :type="tagType(t)" size="small" style="margin-right: 4px">{{ t }}</el-tag>
                      <span v-if="!(row.tags || []).length" style="color: #c0c4cc">—</span>
                    </template>
                  </el-table-column>
                  <el-table-column label="要求" width="80">
                    <template #default="{ row }">{{ row.requirement || '—' }}</template>
                  </el-table-column>
                  <el-table-column label="类型" width="100">
                    <template #default="{ row }">{{ row.kp_type || '—' }}</template>
                  </el-table-column>
                </el-table>
              </el-collapse-item>
            </el-collapse>
            <!-- 平铺视图 -->
            <el-table v-else :data="knowledgePoints" stripe style="width: 100%; margin-top: 10px">
              <el-table-column prop="id" label="ID" width="70" />
              <el-table-column prop="name" label="知识点名称" min-width="240" show-overflow-tooltip />
              <el-table-column prop="subject_name" label="学科" width="90" />
              <el-table-column label="年级" width="90">
                <template #default="{ row }">
                  {{ getGradeLabel(row.grade) }}
                </template>
              </el-table-column>
              <el-table-column label="学期" width="90">
                <template #default="{ row }">
                  {{ row.semester === 1 ? '上学期' : row.semester === 2 ? '下学期' : '未分学期' }}
                </template>
              </el-table-column>
              <el-table-column label="单元" min-width="130" show-overflow-tooltip>
                <template #default="{ row }">{{ row.chapter || '—' }}</template>
              </el-table-column>
              <el-table-column label="标签" width="150">
                <template #default="{ row }">
                  <el-tag v-for="t in (row.tags || [])" :key="t" :type="tagType(t)" size="small" style="margin-right: 4px">{{ t }}</el-tag>
                  <span v-if="!(row.tags || []).length" style="color: #c0c4cc">—</span>
                </template>
              </el-table-column>
              <el-table-column label="要求" width="70">
                <template #default="{ row }">{{ row.requirement || '—' }}</template>
              </el-table-column>
              <el-table-column label="类型" width="90">
                <template #default="{ row }">{{ row.kp_type || '—' }}</template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>

        <!-- 英语单词库管理 -->
        <el-tab-pane label="英语单词库" name="wordLibrary">
          <div class="tab-content">
            <WordLibrary />
          </div>
        </el-tab-pane>

        <!-- 英语语法专项管理 -->
        <el-tab-pane label="语法专项管理" name="grammarManager">
          <div class="tab-content">
            <GrammarManager />
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <!-- 新增学科弹窗 -->
    <el-dialog v-model="showSubjectDialog" title="新增学科" width="400px">
      <el-form :model="subjectForm" label-width="80px">
        <el-form-item label="学科名称" required>
          <el-input v-model="subjectForm.name" placeholder="请输入学科名称" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showSubjectDialog = false">取消</el-button>
        <el-button type="primary" @click="createSubject">保存</el-button>
      </template>
    </el-dialog>

    <!-- 新增标签弹窗 -->
    <el-dialog v-model="showTagDialog" title="新增标签" width="400px">
      <el-form :model="tagForm" label-width="80px">
        <el-form-item label="标签名称" required>
          <el-input v-model="tagForm.name" placeholder="请输入标签名称" />
        </el-form-item>
        <el-form-item label="颜色">
          <el-color-picker v-model="tagForm.color" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showTagDialog = false">取消</el-button>
        <el-button type="primary" @click="createTag">保存</el-button>
      </template>
    </el-dialog>

    <!-- 新增/编辑错误类型弹窗 -->
    <el-dialog v-model="showErrorTypeDialog" :title="editErrorTypeData ? '编辑错误类型' : '新增错误类型'" width="400px">
      <el-form :model="errorTypeForm" label-width="80px">
        <el-form-item label="类型名称" required>
          <el-input v-model="errorTypeForm.name" placeholder="请输入错误类型名称" />
        </el-form-item>
        <el-form-item label="学科">
          <el-select v-model="errorTypeForm.subject_id" placeholder="选择学科（空表示通用）" clearable style="width: 100%">
            <el-option v-for="s in subjects" :key="s.id" :label="s.name" :value="s.id" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="closeErrorTypeDialog">取消</el-button>
        <el-button type="primary" @click="saveErrorType">保存</el-button>
      </template>
    </el-dialog>

    <!-- 新增/编辑知识点弹窗 -->
    <el-dialog v-model="showKnowledgeDialog" :title="editKnowledgeData ? '编辑知识点' : '新增知识点'" width="500px">
      <el-form :model="knowledgeForm" label-width="100px">
        <el-form-item label="知识点名称" required>
          <el-input v-model="knowledgeForm.name" placeholder="请输入知识点名称" />
        </el-form-item>
        <el-form-item label="学科" required>
          <el-select v-model="knowledgeForm.subject_id" placeholder="选择学科" style="width: 100%">
            <el-option v-for="s in subjects" :key="s.id" :label="s.name" :value="s.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="年级">
          <el-select v-model="knowledgeForm.grade" placeholder="选择年级" clearable style="width: 100%">
            <el-option v-for="g in gradeOptions" :key="g.value" :label="g.label" :value="g.value" />
          </el-select>
        </el-form-item>
        <el-form-item label="学期">
          <el-select v-model="knowledgeForm.semester" placeholder="选择学期" clearable style="width: 100%">
            <el-option label="上学期" :value="1" />
            <el-option label="下学期" :value="2" />
          </el-select>
        </el-form-item>
        <el-form-item label="单元">
          <el-input v-model="knowledgeForm.chapter" placeholder="如：第一单元 分数乘法（教材同步自动带入）" />
        </el-form-item>
        <el-form-item label="标签">
          <el-select v-model="knowledgeForm.tags" multiple placeholder="重点/难点/易错点" style="width: 100%">
            <el-option v-for="t in kpOptionTags" :key="t" :label="t" :value="t" />
          </el-select>
        </el-form-item>
        <el-form-item label="要求">
          <el-select v-model="knowledgeForm.requirement" placeholder="认知要求" clearable style="width: 100%">
            <el-option v-for="r in kpOptionRequirements" :key="r" :label="r" :value="r" />
          </el-select>
        </el-form-item>
        <el-form-item label="类型">
          <el-select v-model="knowledgeForm.kp_type" placeholder="内容类型（可输入新类型）" clearable filterable allow-create default-first-option style="width: 100%">
            <el-option v-for="t in kpOptionTypes" :key="t" :label="t" :value="t" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="closeKnowledgeDialog">取消</el-button>
        <el-button type="primary" @click="saveKnowledgePoint">保存</el-button>
      </template>
    </el-dialog>

    <!-- 教材同步导入弹窗 -->
    <TextbookImport v-model="showTextbookImport" @imported="onTextbookImported" />
    <!-- AI 生成知识点弹窗 -->
    <AiKpImport v-model="showAiKpImport" :subjects="subjects" @imported="onTextbookImported" />

    <!-- 同步最新知识点弹窗（Ops 一键同步） -->    <el-dialog v-model="showKpSyncDialog" title="同步最新知识点" width="420px">
      <p style="color: #909399; font-size: 13px; margin: 0 0 14px">从内置知识库一键同步所选科目的全部年级知识点（教材数据由运营统一维护，同步为全量覆盖）。</p>
      <el-form label-width="80px" @submit.prevent>
        <el-form-item label="科目" required>
          <el-select v-model="kpSyncForm.subject" placeholder="选择科目" style="width: 100%" @change="onKpSyncSubject">
            <el-option v-for="s in kpSyncSubjects" :key="s" :label="s" :value="s" />
          </el-select>
        </el-form-item>
        <el-form-item label="版本" required>
          <el-select v-model="kpSyncForm.version" placeholder="选择版本" style="width: 100%">
            <el-option v-for="v in kpSyncVersions" :key="v" :label="v" :value="v" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showKpSyncDialog = false">取消</el-button>
        <el-button type="primary" :loading="kpSyncing" :disabled="!kpSyncForm.subject || !kpSyncForm.version" @click="doKpSync">
          一键同步
        </el-button>
      </template>
    </el-dialog>

    <!-- 使用指南 -->
    <UsageGuide v-model="guideVisible" />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { questionApi } from '@/api/question'
import { syncApi } from '@/api/sync'
import WordLibrary from './WordLibrary.vue'
import GrammarManager from '@/components/GrammarManager.vue'
import TextbookImport from './TextbookImport.vue'
import AiKpImport from '@/components/AiKpImport.vue'
import UsageGuide from '@/components/UsageGuide.vue'

const activeTab = ref('subjects')
const guideVisible = ref(false)

// 教材同步导入弹窗
const showTextbookImport = ref(false)
// AI 生成知识点弹窗
const showAiKpImport = ref(false)
const onTextbookImported = () => {
  // 刷新知识点列表
  fetchKpAll()
}

// 同步最新知识点（Ops 内置知识库一键同步）
const showKpSyncDialog = ref(false)
const kpSyncing = ref(false)
const kpSyncForm = reactive({ subject: '', version: '' })
const kpSyncSubjects = ref([])
const kpSyncVersions = ref([])
const kpSyncCatalog = ref(null)

const openKpSyncDialog = async () => {
  showKpSyncDialog.value = true
  kpSyncForm.subject = ''
  kpSyncForm.version = ''
  try {
    const { data } = await syncApi.status()
    kpSyncCatalog.value = data.catalog
    kpSyncSubjects.value = Object.keys(data.catalog?.subjects || {}).filter(s => s !== '语文')
    kpSyncVersions.value = []
  } catch {
    kpSyncSubjects.value = []
  }
}

const onKpSyncSubject = (s) => {
  kpSyncForm.version = ''
  const subs = kpSyncCatalog.value?.subjects || {}
  kpSyncVersions.value = Object.keys(subs[s] || {})
  if (kpSyncVersions.value.length) kpSyncForm.version = kpSyncVersions.value[0]
}

const doKpSync = async () => {
  if (kpSyncing.value || !kpSyncForm.subject || !kpSyncForm.version) return
  kpSyncing.value = true
  try {
    const { data } = await syncApi.syncKp({ subject: kpSyncForm.subject, version: kpSyncForm.version })
    ElMessage.success(`已同步 ${data.added} 条知识点（${kpSyncForm.subject}《${kpSyncForm.version}》1~6 年级）`)
    showKpSyncDialog.value = false
    fetchKpAll()
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '同步失败，请稍后重试')
  } finally {
    kpSyncing.value = false
  }
}

// 在教材库中对照该知识点对应的教材内容
const viewInTextbook = (row) => {
  const router = useRouter()
  router.push({
    path: '/textbook-library',
    query: {
      subject: row.subject_name || '',
      grade: getGradeLabel(row.grade),
      semester: row.semester === 1 ? '上册' : row.semester === 2 ? '下册' : '',
      version: row.version || '',
      kw: [row.name, row.chapter].filter(Boolean).join(','),
    },
  })
}

// 年级选项（与运营平台对齐：仅小学 1-6 年级，知识点教材由 Ops 统一维护）
const gradeOptions = [
  { label: '一年级', value: 1 },
  { label: '二年级', value: 2 },
  { label: '三年级', value: 3 },
  { label: '四年级', value: 4 },
  { label: '五年级', value: 5 },
  { label: '六年级', value: 6 },
]

const getGradeLabel = (grade) => {
  if (!grade) return '未设置'
  const g = gradeOptions.find(o => o.value === grade)
  return g ? g.label : `${grade}年级`
}

// 学科
const subjects = ref([])
const showSubjectDialog = ref(false)
// 年级选项
const subjectForm = reactive({ name: '' })

// 标签
const tags = ref([])
const showTagDialog = ref(false)
const tagForm = reactive({ name: '', color: '#409eff' })

// 错误类型
const errorTypes = ref([])
const etFilters = reactive({ subject_id: null })
const showErrorTypeDialog = ref(false)
const editErrorTypeData = ref(null)
const errorTypeForm = reactive({
  name: '',
  subject_id: localStorage.getItem('lastEtSubject') ? parseInt(localStorage.getItem('lastEtSubject')) : null
})

// 知识点（筛选：统一结构 = 每组「全部 + 子项」单选，null=全部）
const knowledgePoints = ref([])
const kpAll = ref([])               // 全量知识点（前端过滤）
const kpFilterSubject = ref(null)   // 学科单选（null=全部）
const kpFilterGrade = ref(null)     // 年级单选（null=全部）
const kpFilterSemester = ref(null)  // 学期单选（null=全部）
const kpFilterQ = ref('')            // 搜索词（名称/章节/说明关键字）
const kpFilterEdition = ref(null)   // 教材版本单选（null=全部；custom=自定义）
const kpOptionTags = ref(['重点', '难点', '易错点'])
const kpOptionRequirements = ref(['识记', '理解', '背诵', '运用', '综合'])
const kpOptionTypes = ref([])       // 类型选项（按学科动态）
const kpGrouped = ref(true)         // 默认按单元分组视图
const kpOpenChapters = ref([])      // 展开的单元
const showKnowledgeDialog = ref(false)
const editKnowledgeData = ref(null)
const knowledgeForm = reactive({
  name: '',
  subject_id: null,
  grade: null,
  semester: null,
  chapter: '',
  tags: [],
  requirement: null,
  kp_type: null
})

// 教材版本选项（从全量去重：edition_key；无版本 = 自定义）
const kpEditionOptions = computed(() => {
  const m = new Map()
  for (const k of kpAll.value) {
    const ek = k.edition_key || 'custom'
    if (!m.has(ek)) {
      m.set(ek, { key: ek, label: ek === 'custom' ? '自定义' : (k.version || ek) })
    }
  }
  return [...m.values()]
})

// 按单元分组（学科×年级×学期×单元）
const kpGroups = computed(() => {
  const map = new Map()
  for (const k of knowledgePoints.value) {
    const key = `${k.subject_id}|${k.grade ?? ''}|${k.semester ?? ''}|${k.chapter ?? ''}`
    if (!map.has(key)) {
      map.set(key, {
        key,
        chapter: k.chapter || '未归类',
        label: `${k.subject_name ? k.subject_name + ' · ' : ''}${k.chapter || '未归类'}`,
        items: [],
      })
    }
    map.get(key).items.push(k)
  }
  return Array.from(map.values())
})

const toggleKpGrouped = () => {
  kpGrouped.value = !kpGrouped.value
  if (kpGrouped.value) {
    kpOpenChapters.value = kpGroups.value.map(g => g.key)
  }
}

const tagType = (t) => {
  if (t === '重点') return 'danger'
  if (t === '难点') return 'warning'
  if (t === '易错点') return 'info'
  return 'primary'
}

// 获取知识点过滤选项（标签/要求/类型）
const fetchKpOptions = async () => {
  try {
    const subjectId = kpFilterSubject.value
    const { data } = await questionApi.knowledgePointOptions(subjectId)
    if (data.tags) kpOptionTags.value = data.tags
    if (data.requirements) kpOptionRequirements.value = data.requirements
    if (Array.isArray(data.kp_types)) kpOptionTypes.value = data.kp_types
  } catch (e) {
    console.error('获取知识点选项失败:', e)
  }
}

// 获取学科列表
const fetchSubjects = async () => {
  try {
    const { data } = await questionApi.listSubjects()
    subjects.value = Array.isArray(data) ? data : (data.items || [])
  } catch (e) {
    console.error('获取学科失败:', e)
  }
}

// 创建学科
const createSubject = async () => {
  if (!subjectForm.name.trim()) {
    ElMessage.warning('请输入学科名称')
    return
  }
  try {
    await questionApi.createSubject(subjectForm.name)
    ElMessage.success('创建成功')
    showSubjectDialog.value = false
    subjectForm.name = ''
    fetchSubjects()
  } catch (e) {
    ElMessage.error('创建失败')
  }
}

// 系统内置：学科/标签/错误类型不允许删除
const BUILTIN_SUBJECTS = ['数学', '英语', '语文']
const BUILTIN_TAGS = ['重点', '粗心', '重复错误', '薄弱']
const isBuiltinSubject = (row) => BUILTIN_SUBJECTS.includes(row.name)
const isBuiltinTag = (row) => BUILTIN_TAGS.includes(row.name)
const isBuiltinErrorType = (row) => row.id <= 6 // 错误类型 1-6 为系统内置

// 删除学科
const deleteSubject = async (row) => {
  if (isBuiltinSubject(row)) {
    ElMessage.warning('系统内置学科，不允许删除')
    return
  }
  try {
    await ElMessageBox.confirm('确定要删除该学科吗？', '删除确认', { type: 'warning' })
    await questionApi.deleteSubject(row.id)
    ElMessage.success('删除成功')
    fetchSubjects()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('删除失败')
  }
}

// 获取标签列表
const fetchTags = async () => {
  try {
    const { data } = await questionApi.listTags()
    tags.value = Array.isArray(data) ? data : (data.items || [])
  } catch (e) {
    console.error('获取标签失败:', e)
  }
}

// 创建标签
const createTag = async () => {
  if (!tagForm.name.trim()) {
    ElMessage.warning('请输入标签名称')
    return
  }
  try {
    await questionApi.createTag(tagForm.name, tagForm.color)
    ElMessage.success('创建成功')
    showTagDialog.value = false
    tagForm.name = ''
    tagForm.color = '#409eff'
    fetchTags()
  } catch (e) {
    ElMessage.error('创建失败')
  }
}

// 删除标签
const deleteTag = async (row) => {
  if (isBuiltinTag(row)) {
    ElMessage.warning('系统内置标签，不允许删除')
    return
  }
  try {
    await ElMessageBox.confirm('确定要删除该标签吗？', '删除确认', { type: 'warning' })
    await questionApi.deleteTag(row.id)
    ElMessage.success('删除成功')
    fetchTags()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('删除失败')
  }
}

// 获取错误类型列表
const fetchErrorTypes = async () => {
  try {
    const params = {}
    if (etFilters.subject_id) params.subject_id = etFilters.subject_id
    const { data } = await questionApi.listErrorTypes(params)
    errorTypes.value = Array.isArray(data) ? data : []
  } catch (e) {
    console.error('获取错误类型失败:', e)
  }
}

// 打开新增错误类型弹窗
const openErrorTypeDialog = () => {
  editErrorTypeData.value = null
  errorTypeForm.name = ''
  errorTypeForm.subject_id = localStorage.getItem('lastEtSubject') ? parseInt(localStorage.getItem('lastEtSubject')) : null
  showErrorTypeDialog.value = true
}

// 关闭错误类型弹窗
const closeErrorTypeDialog = () => {
  showErrorTypeDialog.value = false
  editErrorTypeData.value = null
  errorTypeForm.name = ''
  errorTypeForm.subject_id = localStorage.getItem('lastEtSubject') ? parseInt(localStorage.getItem('lastEtSubject')) : null
}

// 编辑错误类型
const editErrorType = (row) => {
  editErrorTypeData.value = row
  errorTypeForm.name = row.name
  errorTypeForm.subject_id = row.subject_id
  showErrorTypeDialog.value = true
}

// 保存错误类型（新增或编辑）
const saveErrorType = async () => {
  if (!errorTypeForm.name.trim()) {
    ElMessage.warning('请输入类型名称')
    return
  }
  try {
    if (editErrorTypeData.value) {
      await questionApi.updateErrorType(editErrorTypeData.value.id, {
        name: errorTypeForm.name,
        subject_id: errorTypeForm.subject_id,
      })
      ElMessage.success('更新成功')
    } else {
      await questionApi.createErrorType({
        name: errorTypeForm.name,
        subject_id: errorTypeForm.subject_id,
      })
      ElMessage.success('创建成功')
      localStorage.setItem('lastEtSubject', errorTypeForm.subject_id || '')
    }
    closeErrorTypeDialog()
    fetchErrorTypes()
  } catch (e) {
    ElMessage.error(editErrorTypeData.value ? '更新失败' : '创建失败')
  }
}

// 删除错误类型
const deleteErrorType = async (row) => {
  if (isBuiltinErrorType(row)) {
    ElMessage.warning('系统内置错误类型，不允许删除')
    return
  }
  try {
    await ElMessageBox.confirm('确定要删除该错误类型吗？', '删除确认', { type: 'warning' })
    await questionApi.deleteErrorType(row.id)
    ElMessage.success('删除成功')
    fetchErrorTypes()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('删除失败')
  }
}

// 获取全量知识点并应用筛选
const fetchKpAll = async () => {
  try {
    const { data } = await questionApi.listKnowledgePoints({})
    kpAll.value = Array.isArray(data) ? data : []
  } catch (e) {
    console.error('获取知识点失败:', e)
    kpAll.value = []
  }
  await applySyncedEditionDefault()
  applyKpFilter()
  fetchKpOptions()
}

// 版本筛选默认选中「已同步教材版本」（跟随使用界面教材；不再显示全部版本）。
// 未同步过教材（模板库预置数据）时兜底选中第一个教材版本，与运营平台一致
const applySyncedEditionDefault = async () => {
  if (kpFilterEdition.value != null) return // 用户已手动选过则不覆盖
  try {
    const { data } = await syncApi.status()
    const syncedVersions = Object.keys(data.synced?.kp || {})
    const first =
      (syncedVersions.length
        ? kpEditionOptions.value.find(o => syncedVersions.includes(o.label))
        : null) ||
      kpEditionOptions.value.find(o => o.key !== 'custom') ||
      kpEditionOptions.value[0]
    if (first) kpFilterEdition.value = first.key
  } catch {
    // 同步状态拉取失败则保持当前筛选
  }
}

// 前端按条件过滤（每组单选，null=全部，组间组合）
const applyKpFilter = () => {
  knowledgePoints.value = kpAll.value.filter(k => {
    if (kpFilterSubject.value != null && kpFilterSubject.value !== k.subject_id) return false
    if (kpFilterGrade.value != null && kpFilterGrade.value !== k.grade) return false
    if (kpFilterSemester.value != null && kpFilterSemester.value !== k.semester) return false
    if (kpFilterEdition.value != null && kpFilterEdition.value !== (k.edition_key || 'custom')) return false
    const q = kpFilterQ.value.trim().toLowerCase()
    if (q && !`${k.name || ''} ${k.chapter || ''} ${k.description || ''}`.toLowerCase().includes(q)) return false
    return true
  })
  if (kpGrouped.value) {
    kpOpenChapters.value = kpGroups.value.map(g => g.key)
  }
}

// 当前筛选条件文本
const kpFilterText = computed(() => {
  const parts = []
  if (kpFilterSubject.value != null) {
    parts.push(subjects.value.find(x => x.id === kpFilterSubject.value)?.name || `学科${kpFilterSubject.value}`)
  }
  if (kpFilterGrade.value != null) {
    parts.push(getGradeLabel(kpFilterGrade.value))
  }
  if (kpFilterSemester.value != null) {
    parts.push(kpFilterSemester.value === 1 ? '上学期' : '下学期')
  }
  if (kpFilterQ.value.trim()) {
    parts.push(`搜索:${kpFilterQ.value.trim()}`)
  }
  if (kpFilterEdition.value != null) {
    const o = kpEditionOptions.value.find(x => x.key === kpFilterEdition.value)
    parts.push(o ? `版本:${o.label}` : `版本:${kpFilterEdition.value}`)
  }
  return parts.length ? '筛选：' + parts.join(' · ') : '全部知识点'
})

// 创建/编辑知识点
const createKnowledgePoint = async () => {
  if (!knowledgeForm.name.trim()) {
    ElMessage.warning('请输入知识点名称')
    return
  }
  if (!knowledgeForm.subject_id) {
    ElMessage.warning('请选择学科')
    return
  }
  const payload = {
    name: knowledgeForm.name,
    subject_id: knowledgeForm.subject_id,
    grade: knowledgeForm.grade,
    semester: knowledgeForm.semester,
    chapter: knowledgeForm.chapter || null,
    tags: knowledgeForm.tags || [],
    requirement: knowledgeForm.requirement || null,
    kp_type: knowledgeForm.kp_type || null,
  }
  try {
    if (editKnowledgeData.value) {
      await questionApi.updateKnowledgePoint(editKnowledgeData.value.id, payload)
      ElMessage.success('更新成功')
    } else {
      await questionApi.createKnowledgePoint(payload)
      ElMessage.success('创建成功')
    }
    closeKnowledgeDialog()
    fetchKpAll()
  } catch (e) {
    ElMessage.error(editKnowledgeData.value ? '更新失败' : '创建失败')
  }
}

// 打开新增知识点弹窗（默认带入筛选条件）
const openKnowledgeDialog = () => {
  editKnowledgeData.value = null
  knowledgeForm.name = ''
  knowledgeForm.subject_id = kpFilterSubject.value
  knowledgeForm.grade = kpFilterGrade.value
  knowledgeForm.semester = kpFilterSemester.value
  knowledgeForm.chapter = ''
  knowledgeForm.tags = []
  knowledgeForm.requirement = null
  knowledgeForm.kp_type = null
  showKnowledgeDialog.value = true
}

// 关闭知识点弹窗
const closeKnowledgeDialog = () => {
  showKnowledgeDialog.value = false
  editKnowledgeData.value = null
  knowledgeForm.name = ''
  knowledgeForm.chapter = ''
  knowledgeForm.tags = []
  knowledgeForm.requirement = null
  knowledgeForm.kp_type = null
}

// 编辑知识点
const editKnowledgePoint = (row) => {
  editKnowledgeData.value = row
  knowledgeForm.name = row.name
  knowledgeForm.subject_id = row.subject_id
  knowledgeForm.grade = row.grade
  knowledgeForm.semester = row.semester
  knowledgeForm.chapter = row.chapter || ''
  knowledgeForm.tags = row.tags || []
  knowledgeForm.requirement = row.requirement || null
  knowledgeForm.kp_type = row.kp_type || null
  showKnowledgeDialog.value = true
}

// 保存知识点（新增或编辑）
const saveKnowledgePoint = async () => {
  await createKnowledgePoint()
}

// 删除知识点
const deleteKnowledgePoint = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该知识点吗？', '删除确认', { type: 'warning' })
    await questionApi.deleteKnowledgePoint(row.id)
    ElMessage.success('删除成功')
    fetchKpAll()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('删除失败')
  }
}

const fetchAll = async () => {
  fetchSubjects()
  fetchTags()
  fetchErrorTypes()
  fetchKpAll()
}

onMounted(() => {
  // 家长中心已统一密码验证，进入即加载数据
  fetchAll()
})
</script>

<style scoped>
.management {
  /* 不限制最大宽度：内容区占满右侧区域，避免宽屏下左右大片空白 */
  width: 100%;
}

.tab-content {
  padding: 10px 0;
}

/* 知识点管理：表格上方 学科/年级/学期 平铺多选筛选 */
.kp-filters {
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  align-items: center;
  padding: 12px 14px;
  background: #f5f7fa;
  border-radius: 8px;
}

.kp-filter-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.kp-filter-bar {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.kp-filter-group {
  display: flex;
  align-items: flex-start;
  gap: 10px;
}

.kp-filter-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  align-items: center;
}

.kp-filter-empty {
  color: #c0c4cc;
  font-size: 12px;
  line-height: 24px;
}

.kp-filter-label {
  color: #606266;
  font-size: 13px;
  white-space: nowrap;
  line-height: 24px;
  min-width: 32px;
}

.kp-group-title {
  font-weight: 600;
  max-width: 420px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.kp-group-count {
  margin-left: 8px;
  color: #909399;
  font-size: 12px;
}

.kp-summary {
  display: flex;
  align-items: center;
  margin-top: 10px;
}

.kp-path {
  color: #606266;
  font-size: 13px;
}

.action-bar {
  margin-bottom: 10px;
}

/* 家长中心顶栏 + 使用指南入口 */
.mgmt-topbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 4px;
}
.mgmt-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}
.mgmt-guide-btn {
  color: #8a94b5;
  font-size: 13px;
}
.mgmt-guide-btn:hover {
  color: #4f7df3;
}

/* 题库管理子导航：顶部横向 tabs */
.mgmt-tabs :deep(.el-tabs__item) {
  height: 44px;
  line-height: 44px;
  font-size: 14px;
}

.mgmt-tabs :deep(.el-tabs__content) {
  padding: 12px 2px 0;
  overflow: visible;
}

/* 移动端适配：tab 多时横向滑动，避免展示不全 */
@media (max-width: 768px) {
  .mgmt-tabs :deep(.el-tabs__nav-wrap) {
    overflow-x: auto;
    overflow-y: hidden;
  }

  .mgmt-tabs :deep(.el-tabs__nav) {
    min-width: max-content;
  }

  .mgmt-tabs :deep(.el-tabs__item) {
    padding: 0 14px;
    font-size: 13px;
  }

  .mgmt-topbar {
    flex-wrap: wrap;
    gap: 6px;
  }
}

/* 禁用卡片的hover效果 */
.management :deep(.el-card) {
  transition: none;
}
.management :deep(.el-card:hover) {
  transform: none;
  box-shadow: var(--shadow-sm) !important;
}
</style>
