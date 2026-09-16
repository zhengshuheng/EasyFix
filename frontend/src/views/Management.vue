<template>
  <div class="management">
    <el-card shadow="never">
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
            <!-- 筛选：标签组平铺点选，组间组合过滤 -->
            <div class="kp-filter-bar">
              <div class="kp-filter-group">
                <span class="kp-filter-label">学科</span>
                <div class="kp-filter-chips">
                  <el-check-tag
                    v-for="s in subjects"
                    :key="s.id"
                    :checked="kpFilterSubject.includes(s.id)"
                    @change="toggleKpFilter(kpFilterSubject, s.id)"
                  >{{ s.name }}</el-check-tag>
                </div>
              </div>
              <div class="kp-filter-group">
                <span class="kp-filter-label">年级</span>
                <div class="kp-filter-chips">
                  <el-check-tag
                    v-for="g in gradeOptions"
                    :key="g.value"
                    :checked="kpFilterGrade.includes(g.value)"
                    @change="toggleKpFilter(kpFilterGrade, g.value)"
                  >{{ g.label }}</el-check-tag>
                </div>
              </div>
              <div class="kp-filter-group">
                <span class="kp-filter-label">学期</span>
                <div class="kp-filter-chips">
                  <el-check-tag :checked="kpFilterSemester.includes(1)" @change="toggleKpFilter(kpFilterSemester, 1)">上学期</el-check-tag>
                  <el-check-tag :checked="kpFilterSemester.includes(2)" @change="toggleKpFilter(kpFilterSemester, 2)">下学期</el-check-tag>
                </div>
              </div>
              <div class="kp-filter-group">
                <span class="kp-filter-label">标签</span>
                <div class="kp-filter-chips">
                  <el-check-tag
                    v-for="t in kpOptionTags"
                    :key="t"
                    :checked="kpFilterTag.includes(t)"
                    @change="toggleKpFilter(kpFilterTag, t)"
                  >{{ t }}</el-check-tag>
                </div>
              </div>
              <div class="kp-filter-group">
                <span class="kp-filter-label">要求</span>
                <div class="kp-filter-chips">
                  <el-check-tag
                    v-for="r in kpOptionRequirements"
                    :key="r"
                    :checked="kpFilterRequirement.includes(r)"
                    @change="toggleKpFilter(kpFilterRequirement, r)"
                  >{{ r }}</el-check-tag>
                </div>
              </div>
              <div class="kp-filter-group">
                <span class="kp-filter-label">类型</span>
                <div class="kp-filter-chips">
                  <el-check-tag
                    v-for="t in kpOptionTypes"
                    :key="t"
                    :checked="kpFilterType.includes(t)"
                    @change="toggleKpFilter(kpFilterType, t)"
                  >{{ t }}</el-check-tag>
                  <span v-if="!kpOptionTypes.length" class="kp-filter-empty">（暂无类型，新增知识点时可输入）</span>
                </div>
              </div>
            </div>
            <div class="action-bar" style="display: flex; flex-wrap: wrap; gap: 10px; align-items: center; margin-top: 10px">
              <el-button type="primary" @click="openKnowledgeDialog">
                <el-icon><Plus /></el-icon>
                新增知识点
              </el-button>
              <el-button type="warning" plain @click="showTextbookImport = true">
                <el-icon><Reading /></el-icon>
                按教材同步导入
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
                  <el-table-column label="操作" width="200" fixed="right">
                    <template #default="{ row }">
                      <el-button link type="primary" size="small" @click="editKnowledgePoint(row)">编辑</el-button>
                      <el-button link type="warning" size="small" @click="viewInTextbook(row)">看教材</el-button>
                      <el-button link type="danger" size="small" @click="deleteKnowledgePoint(row)">删除</el-button>
                    </template>
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
              <el-table-column label="操作" width="200" fixed="right">
                <template #default="{ row }">
                  <el-button link type="primary" size="small" @click="editKnowledgePoint(row)">编辑</el-button>
                  <el-button link type="warning" size="small" @click="viewInTextbook(row)">看教材</el-button>
                  <el-button link type="danger" size="small" @click="deleteKnowledgePoint(row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>

        <!-- 错题本管理 -->
        <el-tab-pane label="错题本管理" name="errorBooks">
          <div class="tab-content">
            <el-alert type="info" :closable="false" style="margin-bottom: 10px" title="添加小孩账号时，系统会自动为该小孩创建各学科错题本；错题本按小孩隔离，每个小孩只能看到/使用自己的错题本。" />
            <div class="action-bar" style="display: flex; gap: 10px; align-items: center">
              <el-button type="primary" @click="openCreateErrorBook">
                <el-icon><Plus /></el-icon>
                新增错题本
              </el-button>
              <el-select v-model="errorBookFilterKid" placeholder="全部小孩" clearable style="width: 160px" @change="fetchErrorBooks">
                <el-option v-for="k in kids" :key="k.id" :label="k.display_name || k.username" :value="k.id" />
              </el-select>
            </div>
            <el-table :data="errorBooks" stripe style="width: 100%; margin-top: 15px">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="name" label="错题本名称" />
              <el-table-column prop="subject_name" label="学科" width="100" />
              <el-table-column label="所属小孩" width="120">
                <template #default="{ row }">
                  {{ row.user_name || (row.user_id ? '小孩#' + row.user_id : '未分配') }}
                </template>
              </el-table-column>
              <el-table-column prop="description" label="描述" />
              <el-table-column label="操作" width="180">
                <template #default="{ row }">
                  <el-button link type="primary" size="small" @click="editErrorBook(row)">编辑</el-button>
                  <el-button link type="danger" size="small" @click="deleteErrorBook(row)">删除</el-button>
                </template>
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

    <!-- 新增/编辑错题本弹窗 -->
    <el-dialog v-model="showErrorBookDialog" :title="editErrorBookData ? '编辑错题本' : '新增错题本'" width="500px">
      <el-form :model="errorBookForm" label-width="100px">
        <el-form-item label="错题本名称" required>
          <el-input v-model="errorBookForm.name" placeholder="请输入错题本名称" />
        </el-form-item>
        <el-form-item label="学科" required>
          <el-select v-model="errorBookForm.subject_id" placeholder="选择学科" style="width: 100%">
            <el-option v-for="s in subjects" :key="s.id" :label="s.name" :value="s.id" />
          </el-select>
        </el-form-item>
        <el-form-item v-if="!editErrorBookData" label="所属小孩" required>
          <el-select v-model="errorBookForm.user_id" placeholder="选择小孩" style="width: 100%">
            <el-option v-for="k in kids" :key="k.id" :label="k.display_name || k.username" :value="k.id" />
          </el-select>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="errorBookForm.description" type="textarea" :rows="3" placeholder="请输入描述" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showErrorBookDialog = false">取消</el-button>
        <el-button type="primary" @click="createOrUpdateErrorBook">保存</el-button>
      </template>
    </el-dialog>

    <!-- 教材同步导入弹窗 -->
    <TextbookImport v-model="showTextbookImport" @imported="onTextbookImported" />
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { questionApi } from '@/api/question'
import { usersApi } from '@/api/users'
import WordLibrary from './WordLibrary.vue'
import TextbookImport from './TextbookImport.vue'

const activeTab = ref('subjects')

// 教材同步导入弹窗
const showTextbookImport = ref(false)
const onTextbookImported = () => {
  // 刷新知识点列表
  fetchKpAll()
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

// 年级选项
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

// 知识点（筛选：标签组平铺点选，组间组合过滤）
const knowledgePoints = ref([])
const kpAll = ref([])               // 全量知识点（前端过滤）
const kpFilterSubject = ref([])     // 学科多选
const kpFilterGrade = ref([])       // 年级多选
const kpFilterSemester = ref([])    // 学期多选
const kpFilterTag = ref([])         // 标签：重点/难点/易错点
const kpFilterRequirement = ref([]) // 要求：识记/理解/背诵/运用/综合
const kpFilterType = ref([])        // 内容类型（学科 distinct + 可自定义）
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

// 标签组点选：点一下选中/取消，组内多选
const toggleKpFilter = (arr, value) => {
  const i = arr.indexOf(value)
  if (i >= 0) arr.splice(i, 1)
  else arr.push(value)
  applyKpFilter()
}

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
    const subjectId = kpFilterSubject.value.length === 1 ? kpFilterSubject.value[0] : null
    const { data } = await questionApi.knowledgePointOptions(subjectId)
    if (data.tags) kpOptionTags.value = data.tags
    if (data.requirements) kpOptionRequirements.value = data.requirements
    if (Array.isArray(data.kp_types)) kpOptionTypes.value = data.kp_types
  } catch (e) {
    console.error('获取知识点选项失败:', e)
  }
}

// 错题本
const errorBooks = ref([])
const kids = ref([])                    // 小孩列表（错题本归属/筛选）
const errorBookFilterKid = ref(null)    // 错题本管理按小孩筛选
const showErrorBookDialog = ref(false)
const editErrorBookData = ref(null)
const errorBookForm = reactive({ name: '', subject_id: null, user_id: null, description: '' })

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
  applyKpFilter()
  fetchKpOptions()
}

// 前端按条件过滤（学科/年级/学期/标签/要求/类型，组内多选，组间组合）
const applyKpFilter = () => {
  knowledgePoints.value = kpAll.value.filter(k => {
    if (kpFilterSubject.value.length && !kpFilterSubject.value.includes(k.subject_id)) return false
    if (kpFilterGrade.value.length && !kpFilterGrade.value.includes(k.grade)) return false
    if (kpFilterSemester.value.length && !kpFilterSemester.value.includes(k.semester)) return false
    if (kpFilterTag.value.length && !(k.tags || []).some(t => kpFilterTag.value.includes(t))) return false
    if (kpFilterRequirement.value.length && !kpFilterRequirement.value.includes(k.requirement)) return false
    if (kpFilterType.value.length && !kpFilterType.value.includes(k.kp_type)) return false
    return true
  })
  if (kpGrouped.value) {
    kpOpenChapters.value = kpGroups.value.map(g => g.key)
  }
}

// 当前筛选条件文本
const kpFilterText = computed(() => {
  const parts = []
  if (kpFilterSubject.value.length) {
    parts.push(kpFilterSubject.value.map(id => subjects.value.find(x => x.id === id)?.name || `学科${id}`).join('、'))
  }
  if (kpFilterGrade.value.length) {
    parts.push(kpFilterGrade.value.map(g => getGradeLabel(g)).join('、'))
  }
  if (kpFilterSemester.value.length) {
    parts.push(kpFilterSemester.value.map(s => s === 1 ? '上学期' : '下学期').join('、'))
  }
  if (kpFilterTag.value.length) {
    parts.push(`标签:${kpFilterTag.value.join('、')}`)
  }
  if (kpFilterRequirement.value.length) {
    parts.push(`要求:${kpFilterRequirement.value.join('、')}`)
  }
  if (kpFilterType.value.length) {
    parts.push(`类型:${kpFilterType.value.join('、')}`)
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
  knowledgeForm.subject_id = kpFilterSubject.value.length === 1 ? kpFilterSubject.value[0] : null
  knowledgeForm.grade = kpFilterGrade.value.length === 1 ? kpFilterGrade.value[0] : null
  knowledgeForm.semester = kpFilterSemester.value.length === 1 ? kpFilterSemester.value[0] : null
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

// 获取错题本列表（按小孩隔离）
const fetchErrorBooks = async () => {
  try {
    const params = {}
    if (errorBookFilterKid.value) params.user_id = errorBookFilterKid.value
    const { data } = await questionApi.listErrorBooks(params)
    errorBooks.value = data.items || []
    // 如果有subject_id，获取学科名称
    if (errorBooks.value.length > 0) {
      await fetchSubjects()
      errorBooks.value = errorBooks.value.map(eb => ({
        ...eb,
        subject_name: subjects.value.find(s => s.id === eb.subject_id)?.name || ''
      }))
    }
  } catch (e) {
    console.error('获取错题本失败:', e)
  }
}

// 获取小孩列表（错题本归属/筛选）
const fetchKids = async () => {
  try {
    const { data } = await usersApi.listKids()
    kids.value = (data && data.kids) || []
  } catch (e) {
    console.error('获取小孩列表失败:', e)
  }
}

// 打开新增错题本弹窗
const openCreateErrorBook = () => {
  editErrorBookData.value = null
  errorBookForm.name = ''
  errorBookForm.subject_id = null
  errorBookForm.user_id = errorBookFilterKid.value || null
  errorBookForm.description = ''
  showErrorBookDialog.value = true
}

// 创建或更新错题本
const createOrUpdateErrorBook = async () => {
  if (!errorBookForm.name.trim()) {
    ElMessage.warning('请输入错题本名称')
    return
  }
  if (!errorBookForm.subject_id) {
    ElMessage.warning('请选择学科')
    return
  }
  if (!editErrorBookData.value && !errorBookForm.user_id) {
    ElMessage.warning('请选择所属小孩')
    return
  }
  try {
    if (editErrorBookData.value) {
      const payload = { name: errorBookForm.name, subject_id: errorBookForm.subject_id, description: errorBookForm.description }
      await questionApi.updateErrorBook(editErrorBookData.value.id, payload)
      ElMessage.success('更新成功')
    } else {
      await questionApi.createErrorBook({ ...errorBookForm })
      ElMessage.success('创建成功')
    }
    showErrorBookDialog.value = false
    editErrorBookData.value = null
    errorBookForm.name = ''
    errorBookForm.subject_id = null
    errorBookForm.user_id = null
    errorBookForm.description = ''
    fetchErrorBooks()
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

// 编辑错题本
const editErrorBook = (row) => {
  editErrorBookData.value = row
  errorBookForm.name = row.name
  errorBookForm.subject_id = row.subject_id
  errorBookForm.user_id = row.user_id
  errorBookForm.description = row.description || ''
  showErrorBookDialog.value = true
}

// 删除错题本
const deleteErrorBook = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该错题本吗？', '删除确认', { type: 'warning' })
    await questionApi.deleteErrorBook(row.id)
    ElMessage.success('删除成功')
    fetchErrorBooks()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('删除失败')
  }
}

const fetchAll = async () => {
  fetchSubjects()
  fetchTags()
  fetchErrorTypes()
  fetchKpAll()
  fetchKids()
  fetchErrorBooks()
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

/* 禁用卡片的hover效果 */
.management :deep(.el-card) {
  transition: none;
}
.management :deep(.el-card:hover) {
  transform: none;
  box-shadow: var(--shadow-sm) !important;
}
</style>
