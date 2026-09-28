<template>
  <!-- 出题弹窗：错题组卷 / AI 出题（自动生成PDF） -->
  <el-dialog v-model="generateDialogVisible" title="出题" width="480px">
    <el-tabs v-model="generateTab">
      <el-tab-pane label="错题组卷" name="pool">
        <el-form :model="generateForm" label-width="70px">
          <el-form-item label="学科" required>
            <el-select v-model="generateForm.subject_id" placeholder="选择学科" style="width: 100%" :disabled="!subjectStore.isAll">
              <el-option
                v-for="subject in subjects"
                :key="subject.id"
                :label="subject.name"
                :value="subject.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="年级">
            <el-select v-model="generateForm.grade" placeholder="全部" clearable style="width: 100%" :disabled="!subjectStore.isAllGrade">
              <el-option v-for="g in gradeOptions" :key="g.value" :label="g.label" :value="g.value" />
            </el-select>
          </el-form-item>
          <el-form-item label="数量">
            <el-input-number v-model="generateForm.count" :min="1" :max="99" />
          </el-form-item>
          <el-form-item label="卷面分数">
            <el-radio-group v-model="poolScoreSetting" style="display: flex; flex-direction: column; gap: 6px; align-items: flex-start">
              <el-radio value="hundred">百分制（满分 100 分）</el-radio>
              <el-radio value="default">按题型默认分值</el-radio>
              <el-radio value="none">不显示分数（纯练习卷）</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item>
            <span style="color: #909399; font-size: 12px">优先选择未复习、低正确率的题目，生成后自动打印 PDF</span>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="AI 出题" name="ai">
        <el-form :model="aiGenerateForm" label-width="70px">
          <el-form-item label="学科" required>
            <el-select v-model="aiGenerateForm.subject_id" placeholder="选择学科" style="width: 100%" :disabled="!subjectStore.isAll" @change="loadAiKnowledgePoints">
              <el-option
                v-for="subject in subjects"
                :key="subject.id"
                :label="subject.name"
                :value="subject.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="年级">
            <el-select v-model="aiGenerateForm.grade" placeholder="全部" clearable style="width: 100%" :disabled="!subjectStore.isAllGrade" @change="loadAiKnowledgePoints">
              <el-option v-for="g in gradeOptions" :key="g.value" :label="g.label" :value="g.value" />
            </el-select>
          </el-form-item>
          <el-form-item v-if="currentAiTextbook" label="教材版本">
            <div style="width: 100%; display: flex; align-items: center; gap: 8px; flex-wrap: wrap">
              <el-tag size="small" type="warning" effect="plain">{{ currentAiTextbook.version_name }}</el-tag>
              <span style="font-size: 12px; color: #909399">AI 出题按该版本筛选知识点（{{ kidStore.kidName }}）</span>
            </div>
          </el-form-item>
          <el-form-item label="知识点">
            <el-radio-group v-model="aiGenerateForm.knowledge_mode">
              <el-radio value="auto">自动（按错题薄弱点）</el-radio>
              <el-radio value="select">从知识点库选择</el-radio>
              <el-radio value="manual">手动输入</el-radio>
            </el-radio-group>
            <div v-if="aiGenerateForm.knowledge_mode === 'select'" style="width: 100%; margin-top: 8px">
              <el-button type="primary" plain style="width: 100%" @click="openKpPicker" :loading="aiKpLoading">
                <el-icon><Collection /></el-icon>
                &nbsp;选择知识点（{{ aiGenerateForm.selected_kp_ids.length }}）
              </el-button>
              <div v-if="aiSelectedKp.length" style="display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px">
                <el-tag
                  v-for="kp in aiSelectedKp"
                  :key="kp.id"
                  closable
                  size="small"
                  @close="toggleAiKp(kp.id)"
                >{{ kp.chapter ? kp.chapter + ' · ' : '' }}{{ kp.name }}</el-tag>
              </div>
              <div v-else-if="!aiKpLoading" style="color: #e6a23c; font-size: 12px; margin-top: 6px; line-height: 1.6">
                当前学科/年级暂无知识点{{ currentAiTextbook ? `（${currentAiTextbook.version_name}）` : '' }}：请在家长中心 → 题库管理 → 知识点管理用「按教材同步导入」，或切换到其他年级
              </div>
            </div>
            <div v-else-if="aiGenerateForm.knowledge_mode === 'auto'" style="color: #909399; font-size: 12px; margin-top: 8px; line-height: 1.6">
              自动统计当前学科错误最多的知识点出题（需有错题记录，否则请选择/输入知识点）
            </div>
            <el-input
              v-if="aiGenerateForm.knowledge_mode === 'manual'"
              v-model="aiGenerateForm.knowledge_text"
              placeholder="多个知识点用逗号分隔，如：分数加减法,乘法分配律"
              style="margin-top: 8px"
            />
          </el-form-item>
          <el-form-item label="数量">
            <el-select v-model="aiGenerateForm.count" style="width: 100%">
              <el-option v-for="n in [3, 5, 10, 15, 20]" :key="n" :label="`${n} 题`" :value="n" />
            </el-select>
          </el-form-item>
          <el-form-item label="难度">
            <el-select v-model="aiGenerateForm.difficulty" placeholder="中等（默认）" clearable style="width: 100%">
              <el-option label="简单" :value="1" />
              <el-option label="基础" :value="2" />
              <el-option label="中等" :value="3" />
              <el-option label="偏难" :value="4" />
              <el-option label="困难" :value="5" />
            </el-select>
          </el-form-item>
          <el-form-item label="试卷结构">
            <div style="width: 100%">
              <el-select v-model="aiPaperStructure" placeholder="不选 = 默认均衡结构" clearable style="width: 100%" @change="applyPaperStructure">
                <el-option v-for="(s, key) in paperStructuresForSubject" :key="key" :label="s.label" :value="key">
                  <span style="font-weight: 600">{{ s.label }}</span>
                  <span style="color: #909399; font-size: 12px; margin-left: 8px">{{ s.desc }}</span>
                </el-option>
              </el-select>
              <div v-if="currentPaperStructure" style="margin-top: 6px; font-size: 12px; color: #909399; line-height: 1.6">
                已套用「{{ currentPaperStructure.label }}」：题型 {{ currentPaperStructure.types.map(t => QUESTION_TYPE_NAMES[t]).join('、') }} · 难度 {{ ['简单','基础','中等','偏难','困难'][currentPaperStructure.difficulty - 1] }}；可在下方高级设置微调
              </div>
            </div>
          </el-form-item>
          <!-- 高级设置：卷面分数/出题人署名/题型/类型（默认收起，减少弹窗高度） -->
          <el-form-item>
            <div style="width: 100%">
              <div class="ai-advanced-header" @click="aiAdvancedOpen = !aiAdvancedOpen">
                <el-icon :style="{ transition: 'transform .2s' }">
                  <ArrowDown v-if="aiAdvancedOpen" />
                  <ArrowRight v-else />
                </el-icon>
                <span style="font-weight: 600">高级设置</span>
                <span style="color: #909399; font-size: 12px">卷面分数 · 出题人署名 · 题型 · 类型</span>
              </div>
              <template v-if="aiAdvancedOpen">
                <div class="ai-adv-row">
                  <span class="ai-adv-label">卷面分数</span>
                  <div style="flex: 1; min-width: 0">
                    <el-radio-group v-model="aiScoreSetting" style="display: flex; flex-wrap: wrap; gap: 4px 12px">
                      <el-radio value="hundred">百分制100分</el-radio>
                      <el-radio value="default">题型默认分值</el-radio>
                      <el-radio value="none">不显示分数</el-radio>
                    </el-radio-group>
                  </div>
                </div>
                <div class="ai-adv-row">
                  <span class="ai-adv-label">出题人署名</span>
                  <div style="flex: 1; min-width: 0; display: flex; align-items: center; gap: 8px; flex-wrap: wrap">
                    <el-switch v-model="aiShowAiAuthor" />
                    <span style="font-size: 12px; color: #909399">显示「AI 出题助手」（默认留空白让孩子自己写）</span>
                  </div>
                </div>
                <div class="ai-adv-row">
                  <span class="ai-adv-label">题型</span>
                  <div style="flex: 1; min-width: 0">
                    <el-checkbox-group v-model="aiGenerateForm.question_types" style="display: flex; flex-wrap: wrap; gap: 4px 12px">
                      <el-checkbox
                        v-for="t in filteredQuestionTypes"
                        :key="t.value"
                        :value="t.value"
                        style="margin-right: 0"
                      >{{ t.label }}</el-checkbox>
                    </el-checkbox-group>
                    <div style="display: flex; justify-content: space-between; margin-top: 4px">
                      <span style="color: #c0c4cc; font-size: 12px">不选 = 混合出题</span>
                      <el-link
                        v-if="aiGenerateForm.question_types.length"
                        type="primary"
                        :underline="false"
                        style="font-size: 12px"
                        @click="aiGenerateForm.question_types = []"
                      >清空</el-link>
                    </div>
                  </div>
                </div>
                <div class="ai-adv-row">
                  <span class="ai-adv-label">类型</span>
                  <div style="flex: 1; min-width: 0">
                    <el-checkbox-group v-model="aiGenerateForm.question_categories" style="display: flex; flex-wrap: wrap; gap: 4px 12px">
                      <el-checkbox
                        v-for="c in questionCategoriesForSubject"
                        :key="c.value"
                        :value="c.value"
                        style="margin-right: 0"
                      >
                        <span style="font-weight: 600">{{ c.label }}</span>
                        <span style="color: #909399; font-size: 12px; margin-left: 4px">{{ c.desc }}</span>
                      </el-checkbox>
                    </el-checkbox-group>
                    <div style="display: flex; justify-content: space-between; margin-top: 4px">
                      <span style="color: #c0c4cc; font-size: 12px">不选 = 按课标梯度（基础→情境→综合→拓展）编排</span>
                      <el-link
                        v-if="aiGenerateForm.question_categories.length"
                        type="primary"
                        :underline="false"
                        style="font-size: 12px"
                        @click="aiGenerateForm.question_categories = []"
                      >清空</el-link>
                    </div>
                  </div>
                </div>
              </template>
            </div>
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>
    <template #footer>
      <el-button @click="generateDialogVisible = false">取消</el-button>
      <el-button
        type="primary"
        :loading="generating"
        @click="generateTab === 'ai' ? generateAiPractice() : generatePractice()"
      >
        {{ generateTab === 'ai' ? 'AI 生成' : '生成并打印' }}
      </el-button>
    </template>
  </el-dialog>

  <!-- 知识点选择弹窗（按单元分组标签点选） -->
  <el-dialog v-model="kpPickerVisible" title="选择知识点" width="640px" append-to-body>
    <div style="display: flex; gap: 10px; margin-bottom: 12px; align-items: center">
      <el-input v-model="kpSearch" placeholder="搜索知识点名称" clearable style="flex: 1">
        <template #prefix><el-icon><Search /></el-icon></template>
      </el-input>
      <el-button v-if="aiGenerateForm.selected_kp_ids.length" size="default" @click="clearAiKpSelection">清空已选</el-button>
      <span v-if="aiGenerateForm.selected_kp_ids.length" style="color: #409eff; font-size: 13px; white-space: nowrap">已选 {{ aiGenerateForm.selected_kp_ids.length }} 个</span>
    </div>
    <div v-if="aiKpLoading" style="text-align: center; padding: 30px; color: #909399">知识点加载中…</div>
    <div v-else style="max-height: 400px; overflow-y: auto">
      <div v-for="g in filteredAiKpGroups" :key="g.key" style="margin-bottom: 10px">
        <div
          style="display: flex; align-items: center; gap: 8px; padding: 6px 10px; background: #f5f7fa; border-radius: 6px; cursor: pointer; user-select: none"
          @click="toggleGroup(g)"
        >
          <el-checkbox :model-value="isGroupAllChecked(g)" @click.stop @change="toggleGroup(g)" />
          <span style="font-weight: 600; font-size: 13px">{{ g.label }}</span>
          <span style="color: #909399; font-size: 12px">{{ g.items.length }} 个</span>
          <span v-if="isGroupAllChecked(g)" style="color: #409eff; font-size: 12px; margin-left: auto">已全选</span>
          <span v-else style="color: #c0c4cc; font-size: 12px; margin-left: auto">全选本单元</span>
        </div>
        <div style="display: flex; flex-wrap: wrap; gap: 6px; padding: 8px 6px 0 6px">
          <el-check-tag
            v-for="kp in g.items"
            :key="kp.id"
            :checked="aiGenerateForm.selected_kp_ids.includes(kp.id)"
            @change="toggleAiKp(kp.id)"
          >{{ kp.name }}</el-check-tag>
        </div>
      </div>
      <div v-if="!filteredAiKpGroups.length" style="text-align: center; padding: 30px; color: #909399">
        没有匹配的知识点，可在家长中心导入教材或切换学科/年级
      </div>
    </div>
    <template #footer>
      <el-button @click="kpPickerVisible = false">取消</el-button>
      <el-button type="primary" @click="kpPickerVisible = false">确定（已选 {{ aiGenerateForm.selected_kp_ids.length }}）</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Collection, Search, ArrowDown, ArrowRight } from '@element-plus/icons-vue'
import { questionApi } from '@/api/question'
import { useSubjectStore } from '@/stores/subject'
import { useKidStore } from '@/stores/kid'

const props = defineProps({
  subjects: { type: Array, default: () => [] },
})
const emit = defineEmits(['created'])

const subjectStore = useSubjectStore()
const kidStore = useKidStore()

const generateDialogVisible = ref(false)
const generating = ref(false)
const generateTab = ref('pool') // pool=错题组卷 ai=AI出题
const generateForm = reactive({
  subject_id: null,
  grade: null,
  count: 5,
})
// 错题组卷卷面分数：hundred=百分制 / default=题型默认分值 / none=不显示
const poolScoreSetting = ref('hundred')
const aiGenerateForm = reactive({
  subject_id: null,
  grade: null,
  knowledge_mode: 'auto', // auto=按错题薄弱点 select=从知识点库选择 manual=手动输入
  knowledge_text: '',
  selected_kp_ids: [],    // 从知识点库选择的 id 列表
  count: 5,
  difficulty: null,
  question_types: [],       // 题型多选（空=混合）
  question_categories: [],  // 类型多选（空=混合）
})
const aiPaperStructure = ref('') // 试卷结构预设：basic/standard/advanced
// 卷面分数：hundred=百分制100分 / default=题型默认分值 / none=不显示分数
const aiScoreSetting = ref('hundred')
// 卷面「出题人」是否署名「AI 出题助手」（默认关 = 留空白手填）
const aiShowAiAuthor = ref(false)
// 高级设置折叠区（卷面分数/出题人署名/题型/类型），默认收起
const aiAdvancedOpen = ref(false)

// 题型配置（按学科过滤显示）：value -> 中文名
const QUESTION_TYPES = [
  { value: 'choice', label: '选择题' },
  { value: 'fill', label: '填空题' },
  { value: 'judge', label: '判断题' },
  { value: 'calc', label: '计算题' },
  { value: 'application', label: '应用题' },
  { value: 'operation', label: '操作实践题' },
  { value: 'reading', label: '阅读理解' },
  { value: 'writing', label: '写话·习作' },
  { value: 'sentence', label: '连词成句' },
]
// 题型按学科+学段过滤（数学：初中以上无操作实践题；语文/英语各自题型不同）
const filteredQuestionTypes = computed(() => {
  const sub = props.subjects.find(s => s.id === aiGenerateForm.subject_id)
  const name = sub ? (sub.name || '') : ''
  const grade = aiGenerateForm.grade || 0
  if (name.includes('语文')) return QUESTION_TYPES.filter(t => ['choice', 'fill', 'judge', 'reading', 'writing'].includes(t.value))
  if (name.includes('英语')) return QUESTION_TYPES.filter(t => ['choice', 'fill', 'judge', 'sentence', 'reading'].includes(t.value))
  if (grade >= 7) return QUESTION_TYPES.filter(t => ['choice', 'fill', 'judge', 'calc', 'application'].includes(t.value))
  return QUESTION_TYPES.filter(t => ['choice', 'fill', 'judge', 'calc', 'application', 'operation'].includes(t.value))
})
// 当前出题科目 key：math / chinese / english / other
const currentSubjectKey = computed(() => {
  const sub = props.subjects.find(s => s.id === aiGenerateForm.subject_id)
  const name = sub ? (sub.name || '') : ''
  if (name.includes('语文')) return 'chinese'
  if (name.includes('英语')) return 'english'
  return 'math'
})
// 类型配置按学科差异化（对齐各科课标）
const QUESTION_CATEGORIES_BY_SUBJECT = {
  math: [
    { value: 'basic', label: '基础巩固', desc: '概念·公式·法则直接考查（四基）' },
    { value: 'scene', label: '情境应用', desc: '生活真实情境解决问题（四能·情景设计）' },
    { value: 'comprehensive', label: '综合提升', desc: '跨知识点·多步综合运用（综合与实践）' },
    { value: 'thinking', label: '思维拓展', desc: '开放探究·规律推理（素养导向）' },
  ],
  chinese: [
    { value: 'basic', label: '积累运用', desc: '字词句·古诗文积累（语言运用）' },
    { value: 'scene', label: '阅读理解', desc: '现代文·文言文阅读与鉴赏（阅读与鉴赏）' },
    { value: 'comprehensive', label: '表达交流', desc: '口语交际·写话习作（表达与交流）' },
  ],
  english: [
    { value: 'basic', label: '词汇语法', desc: '词汇·语法单项（语言能力）' },
    { value: 'scene', label: '情景交际', desc: '对话·日常交际用语（真实语境）' },
    { value: 'comprehensive', label: '阅读理解', desc: '短文理解·信息获取（思维品质）' },
    { value: 'thinking', label: '书面表达', desc: '写作·语言输出（学习能力）' },
  ],
}
const questionCategoriesForSubject = computed(() => QUESTION_CATEGORIES_BY_SUBJECT[currentSubjectKey.value] || QUESTION_CATEGORIES_BY_SUBJECT.math)

// 题型分值/名称/大题顺序（与后端 PDF 一致，参考学校试卷）
import { QUESTION_TYPE_NAMES } from '@/constants/questionTypes'

// 试卷结构预设按学科差异化（一键填充 题型+类型+难度）
const PAPER_STRUCTURES_BY_SUBJECT = {
  math: {
    basic: { label: '基础卷', desc: '基础巩固为主（计算+填空，对应课标"四基"）', types: ['fill', 'calc', 'choice', 'application'], categories: ['basic'], difficulty: 2 },
    standard: { label: '标准卷', desc: '均衡结构（模拟学校单元/期末卷，7:2:1 梯度）', types: ['fill', 'calc', 'choice', 'application'], categories: ['basic', 'scene'], difficulty: 3 },
    advanced: { label: '拓展卷', desc: '素养拓展（应用+操作+思维，对应课标"四能"）', types: ['application', 'choice', 'fill', 'operation'], categories: ['comprehensive', 'thinking'], difficulty: 4 },
  },
  chinese: {
    basic: { label: '基础卷', desc: '字词句积累（拼音·字词·句子）', types: ['fill', 'choice', 'judge'], categories: ['basic'], difficulty: 2 },
    standard: { label: '阅读卷', desc: '积累+阅读（字词+短文理解）', types: ['fill', 'reading', 'choice'], categories: ['basic', 'scene'], difficulty: 3 },
    advanced: { label: '表达卷', desc: '阅读+写话习作（综合表达）', types: ['reading', 'writing', 'fill'], categories: ['scene', 'comprehensive'], difficulty: 4 },
  },
  english: {
    basic: { label: '基础卷', desc: '词汇语法单选+词汇填空', types: ['choice', 'fill'], categories: ['basic'], difficulty: 2 },
    standard: { label: '会话卷', desc: '单选+连词成句+情景交际', types: ['choice', 'sentence', 'fill'], categories: ['basic', 'scene'], difficulty: 3 },
    advanced: { label: '综合卷', desc: '阅读+写作（综合语用）', types: ['reading', 'writing', 'choice'], categories: ['comprehensive', 'thinking'], difficulty: 4 },
  },
}
const paperStructuresForSubject = computed(() => PAPER_STRUCTURES_BY_SUBJECT[currentSubjectKey.value] || PAPER_STRUCTURES_BY_SUBJECT.math)
function applyPaperStructure(key) {
  if (!key) return
  const s = paperStructuresForSubject.value[key]
  if (!s) return
  aiGenerateForm.question_types = [...s.types]
  aiGenerateForm.question_categories = [...s.categories]
  aiGenerateForm.difficulty = s.difficulty
}
// 当前选中的试卷结构预设（用于说明文案）
const currentPaperStructure = computed(() => (aiPaperStructure.value ? paperStructuresForSubject.value[aiPaperStructure.value] : null))

// AI 出题知识点库（按学科+年级加载；若小孩绑定了教材版本则按版本过滤，按单元分组）
const currentAiTextbook = computed(() => {
  if (!aiGenerateForm.subject_id) return null
  const tbs = kidStore.activeKid?.textbooks || []
  return tbs.find(t => t.subject_id === aiGenerateForm.subject_id) || null
})
const aiKpAll = ref([])
const aiKpLoading = ref(false)
const loadAiKnowledgePoints = async () => {
  if (!aiGenerateForm.subject_id) return
  aiKpLoading.value = true
  try {
    const params = { subject_id: aiGenerateForm.subject_id }
    if (aiGenerateForm.grade) params.grade = aiGenerateForm.grade
    const tb = currentAiTextbook.value
    if (tb?.edition_key) params.edition_key = tb.edition_key
    const { data } = await questionApi.listKnowledgePoints(params)
    aiKpAll.value = Array.isArray(data) ? data : []
  } catch (e) {
    console.error('加载知识点失败:', e)
    aiKpAll.value = []
  } finally {
    aiKpLoading.value = false
  }
}
const getGradeLabel = (g) => {
  const map = { 1: '一年级', 2: '二年级', 3: '三年级', 4: '四年级', 5: '五年级', 6: '六年级', 7: '初一', 8: '初二', 9: '初三', 10: '高一', 11: '高二', 12: '高三' }
  return map[g] || (g ? `${g}年级` : '')
}

const aiKpGroups = computed(() => {
  const map = new Map()
  for (const k of aiKpAll.value) {
    const key = `${k.grade ?? ''}|${k.semester ?? ''}|${k.chapter ?? ''}`
    if (!map.has(key)) {
      map.set(key, {
        key,
        label: [k.grade ? getGradeLabel(k.grade) : '', k.semester === 1 ? '上学期' : k.semester === 2 ? '下学期' : '', k.chapter || '未归类'].filter(Boolean).join(' · '),
        items: [],
      })
    }
    map.get(key).items.push(k)
  }
  return Array.from(map.values())
})

// 知识点选择弹窗（按单元分组标签点选）
const kpPickerVisible = ref(false)
const kpSearch = ref('')
const openKpPicker = () => {
  if (aiGenerateForm.subject_id) {
    loadAiKnowledgePoints() // 打开时强制刷新，保证最新数据
  }
  kpSearch.value = ''
  kpPickerVisible.value = true
}
const toggleAiKp = (id) => {
  const i = aiGenerateForm.selected_kp_ids.indexOf(id)
  if (i >= 0) aiGenerateForm.selected_kp_ids.splice(i, 1)
  else aiGenerateForm.selected_kp_ids.push(id)
}
const clearAiKpSelection = () => {
  aiGenerateForm.selected_kp_ids = []
}
// 已选知识点对象（用于标签回显）
const aiSelectedKp = computed(() => {
  const set = new Set(aiGenerateForm.selected_kp_ids)
  return aiKpAll.value.filter(k => set.has(k.id))
})
// 按搜索词过滤后的分组
const filteredAiKpGroups = computed(() => {
  const q = kpSearch.value.trim()
  if (!q) return aiKpGroups.value
  return aiKpGroups.value
    .map(g => ({ ...g, items: g.items.filter(k => k.name.includes(q)) }))
    .filter(g => g.items.length)
})
const isGroupAllChecked = (g) => g.items.length > 0 && g.items.every(k => aiGenerateForm.selected_kp_ids.includes(k.id))
const toggleGroup = (g) => {
  const ids = g.items.map(k => k.id)
  const all = isGroupAllChecked(g)
  if (all) {
    aiGenerateForm.selected_kp_ids = aiGenerateForm.selected_kp_ids.filter(id => !ids.includes(id))
  } else {
    const set = new Set(aiGenerateForm.selected_kp_ids)
    ids.forEach(id => set.add(id))
    aiGenerateForm.selected_kp_ids = Array.from(set)
  }
}
const gradeOptions = [
  { value: 1, label: '一年级' },
  { value: 2, label: '二年级' },
  { value: 3, label: '三年级' },
  { value: 4, label: '四年级' },
  { value: 5, label: '五年级' },
  { value: 6, label: '六年级' },
]

const showGenerateDialog = () => {
  // 学习空间指定学科/年级时，生成练习默认该空间且不可切换
  const defaultSubjectId = subjectStore.activeSubjectId !== null ? subjectStore.activeSubjectId : null
  generateForm.subject_id = defaultSubjectId
  generateForm.grade = subjectStore.activeGrade !== null ? subjectStore.activeGrade : null
  generateForm.count = 5
  aiGenerateForm.subject_id = defaultSubjectId
  aiGenerateForm.grade = subjectStore.activeGrade !== null ? subjectStore.activeGrade : null
  aiGenerateForm.knowledge_mode = 'auto'
  aiGenerateForm.knowledge_text = ''
  aiGenerateForm.selected_kp_ids = []
  aiGenerateForm.count = 5
  aiGenerateForm.difficulty = null
  aiGenerateForm.question_types = []
  aiGenerateForm.question_categories = []
  aiPaperStructure.value = ''
  generateTab.value = 'pool'
  generateDialogVisible.value = true
  if (defaultSubjectId) {
    loadAiKnowledgePoints()
  }
}

const generatePractice = async () => {
  if (!generateForm.subject_id) {
    ElMessage.warning('请选择学科')
    return
  }
  generating.value = true
  try {
    const { data } = await questionApi.generateFromQuestions({
      subject_id: generateForm.subject_id,
      grade: generateForm.grade,
      count: generateForm.count,
      show_score: poolScoreSetting.value !== 'none',
      score_mode: poolScoreSetting.value === 'default' ? 'default' : 'hundred',
    })
    ElMessage.success('练习集已生成，可下载打印 PDF')
    generateDialogVisible.value = false
    emit('created', { data, kind: 'pool' })
  } catch (error) {
    ElMessage.error('生成失败')
  } finally {
    generating.value = false
  }
}

const generateAiPractice = async () => {
  if (!aiGenerateForm.subject_id) {
    ElMessage.warning('请选择学科')
    return
  }
  let knowledge_points = []
  if (aiGenerateForm.knowledge_mode === 'manual') {
    knowledge_points = aiGenerateForm.knowledge_text
      .split(/[,，、;；]/)
      .map(s => s.trim())
      .filter(Boolean)
    if (knowledge_points.length === 0) {
      ElMessage.warning('请输入知识点（多个用逗号分隔）')
      return
    }
  } else if (aiGenerateForm.knowledge_mode === 'select') {
    if (aiGenerateForm.selected_kp_ids.length === 0) {
      ElMessage.warning('请选择知识点（可多选）')
      return
    }
    const idSet = new Set(aiGenerateForm.selected_kp_ids)
    knowledge_points = aiKpAll.value.filter(k => idSet.has(k.id)).map(k => k.name)
    if (knowledge_points.length === 0) {
      ElMessage.warning('所选知识点不存在，请重新选择')
      return
    }
  }
  generating.value = true
  try {
    const { data } = await questionApi.generateAiPracticeSet({
      subject_id: aiGenerateForm.subject_id,
      grade: aiGenerateForm.grade,
      knowledge_points,
      count: aiGenerateForm.count,
      difficulty: aiGenerateForm.difficulty,
      question_types: aiGenerateForm.question_types,
      question_categories: aiGenerateForm.question_categories,
      preset_name: aiPaperStructure.value ? PAPER_STRUCTURES[aiPaperStructure.value]?.label : null,
      show_score: aiScoreSetting.value !== 'none',
      score_mode: aiScoreSetting.value === 'default' ? 'default' : 'hundred',
      show_ai_author: aiShowAiAuthor.value,
    })
    ElMessage.success(`AI 已生成 ${data.total_questions} 道题，练习集已创建`)
    generateDialogVisible.value = false
    emit('created', { data, kind: 'ai', grade: aiGenerateForm.grade, subjectId: aiGenerateForm.subject_id })
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || 'AI 出题失败，请检查 LLM 配置后重试')
  } finally {
    generating.value = false
  }
}

defineExpose({ open: showGenerateDialog })
</script>

<style scoped>
.ai-advanced-header {
  display: flex;
  align-items: center;
  gap: 4px;
  cursor: pointer;
  padding: 6px 0;
  color: #606266;
  font-size: 13px;
  user-select: none;
}
.ai-advanced-header:hover { color: #409eff; }
.ai-adv-row {
  display: flex;
  gap: 8px;
  padding: 8px 0;
  align-items: flex-start;
  border-top: 1px dashed #ebeef5;
}
.ai-adv-label {
  width: 70px;
  flex-shrink: 0;
  color: #606266;
  font-size: 13px;
  padding-top: 4px;
}
</style>
