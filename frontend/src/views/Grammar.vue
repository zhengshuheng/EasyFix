<template>
  <div class="grammar-page">
    <!-- ================= 列表视图 /grammar ================= -->
    <template v-if="!lesson">
      <el-card shadow="never" class="grammar-hero">
        <div class="hero-title">📖 语法专项</div>
        <div class="hero-desc">按板块系统学语法：先读讲解、记口诀，再练专项卷子。语法点教程已完整内置，直接点击板块即可开始学习。</div>
      </el-card>

      <!-- 筛选条件 -->
      <div class="filters">
        <el-select v-model="gradeFilter" placeholder="全部年级" clearable style="width: 120px" @change="resetExpand">
          <el-option v-for="g in 6" :key="g" :label="g + '年级'" :value="g" />
        </el-select>
        <el-select v-model="categoryFilter" placeholder="全部板块" clearable style="width: 170px" @change="resetExpand">
          <el-option v-for="c in allCategories" :key="c.category" :label="c.category" :value="c.category" />
        </el-select>
        <el-input
          v-model="keyword"
          placeholder="搜索语法点"
          clearable
          style="width: 200px"
          @input="resetExpand"
        />
        <span v-if="activeFilters" class="filter-count">共 {{ filteredCategories.length }} 个板块 · {{ filteredLessons.length }} 个语法点</span>
      </div>

      <!-- 板块卡片 -->
      <div v-if="loading" class="loading">加载中...</div>
      <div v-else-if="filteredCategories.length === 0" class="empty">
        <!-- 低年级无语法内容：友好提示 -->
        <template v-if="emptyHintGrade">
          <div class="empty-hint-card">
            <div class="eh-icon">📖</div>
            <div class="eh-title">{{ emptyHintGrade }} 年级暂未开放语法专项</div>
            <div class="eh-desc">
              语法板块从三年级开始，低年级先打好单词和自然拼读基础。想看语法内容，可以查看全部年级：
            </div>
            <el-button type="primary" plain @click="gradeFilter = null; resetExpand()">查看全部年级语法</el-button>
          </div>
        </template>
        <!-- 其它筛选无结果 -->
        <template v-else>没有符合筛选条件的语法板块</template>
      </div>
      <div v-else class="category-grid">
        <el-card
          v-for="cat in filteredCategories"
          :key="cat.category"
          shadow="hover"
          class="category-card"
          @click="toggleCategory(cat.category)"
        >
          <div class="category-header">
            <span class="category-name">{{ cat.category }}</span>
            <el-progress
              type="circle"
              :width="44"
              :stroke-width="5"
              :percentage="cat.count ? Math.round(cat.learned * 100 / cat.count) : 0"
              :status="cat.learned >= cat.count && cat.count > 0 ? 'success' : undefined"
            />
          </div>
          <div class="category-meta">共 {{ cat.count }} 个语法点 · 已学 {{ cat.learned }}</div>
          <div v-if="activeCategory === cat.category" class="lesson-list">
            <div
              v-for="l in lessonsOf(cat.category)"
              :key="l.id"
              class="lesson-item"
              :class="{ mastered: l.progress_status === 'mastered', done: l.progress_status === 'learned' || l.progress_status === 'practiced' }"
              @click.stop="openLesson(l.id)"
            >
              <span class="lesson-dot" />
              <span class="lesson-title">{{ l.title }}</span>
              <el-tag v-if="l.grade" size="small" type="info" effect="plain">{{ l.grade }}年级</el-tag>
              <el-tag
                v-if="l.progress_status"
                size="small"
                :type="l.progress_status === 'mastered' ? 'success' : 'primary'"
                effect="light"
              >{{ statusLabel(l.progress_status) }}</el-tag>
              <span v-else class="lesson-new">未学</span>
            </div>
          </div>
          <div v-else class="category-hint">点击展开板块语法点</div>
        </el-card>
      </div>
    </template>

    <!-- ================= 教程视图 /grammar/:id ================= -->
    <template v-else>
      <div class="lesson-layout">
        <!-- 左栏：教程内容 -->
        <div class="lesson-main">
          <el-card shadow="never" class="lesson-page">
            <div class="lesson-nav">
              <el-button size="small" text @click="backToList">← 返回语法板块</el-button>
              <el-tag size="small" type="info">{{ lesson.category }}</el-tag>
              <el-tag v-if="lesson.grade" size="small" type="warning" effect="plain">{{ lesson.grade }}年级</el-tag>
              <el-tag
                v-if="lesson.progress_status"
                size="small"
                :type="lesson.progress_status === 'mastered' ? 'success' : 'primary'"
              >{{ statusLabel(lesson.progress_status) }}</el-tag>
              <span class="auto-read-toggle">
                <el-switch v-model="grammarAutoRead" size="small" @change="toggleGrammarAutoRead" />
                <span class="auto-read-label">自动带读</span>
              </span>
            </div>

            <div class="lesson-title-row">
              <h2 class="lesson-title-big">{{ lesson.title }}</h2>
              <el-button size="small" circle plain class="speak-btn" title="朗读本课标题" @click="speakText(lesson.title)">🔊</el-button>
            </div>

            <!-- 一句话总结 -->
            <div v-if="lesson.summary" class="lesson-summary">
              <span class="summary-text">💡 {{ lesson.summary }}</span>
              <el-button size="small" circle plain class="speak-btn" title="朗读本课总结" @click="speakText(lesson.summary)">🔊</el-button>
            </div>

            <!-- 本课包含（一眼看全貌，点击直达） -->
            <div v-if="outlineItems.length" class="lesson-outline">
              <span class="outline-label">📖 本课包含</span>
              <span
                v-for="o in outlineItems"
                :key="o.id"
                class="outline-chip"
                @click="scrollToSection(o.id)"
              >{{ o.icon }} {{ o.label }}</span>
              <el-button class="outline-toggle" size="small" text @click="toggleAllBlocks">
                {{ allCollapsed ? '全部展开' : '全部收起' }}
              </el-button>
            </div>

            <!-- 教程正文：按 ## 分节，逐节卡片 + 可折叠 -->
            <div
              v-for="(sec, i) in contentSections"
              :key="'sec' + i"
              class="lesson-block"
              :id="'gsec-' + i"
              data-sec="gsec"
            >
              <div v-if="sec.title" class="block-head" @click="toggleBlock('s' + i)">
                <span class="block-no">{{ i + 1 }}</span>
                <span class="block-title">{{ sec.title }}</span>
                <el-button size="small" circle plain class="speak-btn" title="朗读本节内容" @click.stop="speakText((sec.title ? sec.title + '。' : '') + sec.text)">🔊</el-button>
                <span class="block-toggle">{{ collapsed['s' + i] ? '▸' : '▾' }}</span>
              </div>
              <div v-show="!collapsed['s' + i]" class="lesson-content" v-html="sec.html" />
            </div>

            <!-- 例句（带朗读） -->
            <div v-if="lesson.examples && lesson.examples.length" class="lesson-block" id="gsec-examples" data-sec="gsec">
              <div class="block-head" @click="toggleBlock('examples')">
                <span class="block-no">📝</span>
                <span class="block-title">例句（{{ lesson.examples.length }} 条）</span>
                <span class="block-toggle">{{ collapsed.examples ? '▸' : '▾' }}</span>
              </div>
              <div v-show="!collapsed.examples" class="block-body">
                <div v-for="(ex, i) in lesson.examples" :key="i" class="example-item">
                  <el-button
                    size="small"
                    circle
                    type="primary"
                    plain
                    @click="speakExample(ex, i)"
                  >{{ speakingIndex === i ? '🔊' : '🔈' }}</el-button>
                  <div class="example-text">
                    <div class="example-en">{{ ex.en }}</div>
                    <div class="example-zh">{{ ex.zh }}</div>
                  </div>
                </div>
              </div>
            </div>

            <!-- 易错点 -->
            <div v-if="lesson.common_mistakes && lesson.common_mistakes.length" class="lesson-block" id="gsec-mistakes" data-sec="gsec">
              <div class="block-head" @click="toggleBlock('mistakes')">
                <span class="block-no">⚠️</span>
                <span class="block-title">易错点提醒（{{ lesson.common_mistakes.length }} 条）</span>
                <el-button size="small" circle plain class="speak-btn" title="朗读易错点" @click.stop="speakText(lesson.common_mistakes.join('。'))">🔊</el-button>
                <span class="block-toggle">{{ collapsed.mistakes ? '▸' : '▾' }}</span>
              </div>
              <div v-show="!collapsed.mistakes" class="block-body">
                <div v-for="(m, i) in lesson.common_mistakes" :key="i" class="mistake-item">✗ {{ m }}</div>
              </div>
            </div>

            <!-- 口诀 -->
            <div v-if="lesson.mnemonic" class="lesson-block" id="gsec-mnemonic" data-sec="gsec">
              <div class="block-head" @click="toggleBlock('mnemonic')">
                <span class="block-no">🎵</span>
                <span class="block-title">记忆口诀</span>
                <el-button size="small" circle plain class="speak-btn" title="朗读口诀" @click.stop="speakText(lesson.mnemonic)">🔊</el-button>
                <span class="block-toggle">{{ collapsed.mnemonic ? '▸' : '▾' }}</span>
              </div>
              <div v-show="!collapsed.mnemonic" class="block-body">
                <div class="mnemonic-box">{{ lesson.mnemonic }}</div>
              </div>
            </div>

            <div v-if="!lesson.content_md" class="empty">
              该语法点教程内容暂缺，点「同步官方教程」从运营中心拉取最新内容。
            </div>
          </el-card>

          <!-- 底部：同板块上/下一个语法点 -->
          <div v-if="siblingNav.total > 1" class="lesson-footer-nav">
            <el-button :disabled="!siblingNav.prev" @click="siblingNav.prev && switchLesson(siblingNav.prev.id)">
              ← {{ siblingNav.prev ? siblingNav.prev.title : '已是第一个' }}
            </el-button>
            <span class="footer-pos">{{ siblingNav.pos }} / {{ siblingNav.total }}</span>
            <el-button :disabled="!siblingNav.next" @click="siblingNav.next && switchLesson(siblingNav.next.id)">
              {{ siblingNav.next ? siblingNav.next.title : '已是最后一个' }} →
            </el-button>
          </div>
        </div>

        <!-- 右栏：目录 + 操作面板（常驻） -->
        <div class="lesson-side">
          <!-- 本课目录（滚动高亮） -->
          <el-card v-if="outlineItems.length" shadow="never" class="side-card">
            <div class="side-title">📑 本课目录</div>
            <div
              v-for="o in outlineItems"
              :key="o.id"
              class="toc-item"
              :class="{ active: activeSection === o.id }"
              @click="scrollToSection(o.id)"
            >
              <span class="toc-icon">{{ o.icon }}</span>
              <span class="toc-label">{{ o.label }}</span>
            </div>
          </el-card>

          <el-card shadow="never" class="side-card">
            <div class="side-title">📌 本语法点</div>
            <div class="side-status">
              <span>学习状态</span>
              <el-tag
                v-if="lesson.progress_status"
                :type="lesson.progress_status === 'mastered' ? 'success' : 'primary'"
                effect="light"
              >{{ statusLabel(lesson.progress_status) }}</el-tag>
              <el-tag v-else type="info" effect="plain">未学</el-tag>
            </div>

            <el-button
              class="side-btn"
              size="large"
              @click="markLearned"
              :disabled="lesson.progress_status === 'learned' || lesson.progress_status === 'practiced' || lesson.progress_status === 'mastered'"
            >✓ 标记已学</el-button>

            <el-button
              class="side-btn practice-big-btn"
              type="warning"
              size="large"
              :loading="practiceGenerating"
              @click="openPracticeDialog"
            >📝 语法专项练习</el-button>
            <div class="practice-hint">生成一份针对「{{ lesson.title }}」的专项练习卷，做完自动批改、错题进错题本</div>
          </el-card>

          <!-- 同板块其它语法点导航 -->
          <el-card v-if="siblings.length" shadow="never" class="side-card">
            <div class="side-title">📚 同板块语法点</div>
            <div
              v-for="s in siblings"
              :key="s.id"
              class="sibling-item"
              :class="{ active: s.id === lesson.id }"
              @click="switchLesson(s.id)"
            >
              <span class="lesson-dot" :class="{ done: s.progress_status }" />
              <span class="sibling-title">{{ s.title }}</span>
              <el-tag v-if="s.grade" size="small" type="info" effect="plain">{{ s.grade }}年级</el-tag>
            </div>
          </el-card>
        </div>
      </div>

      <!-- 回到顶部：长教程随时回目录 -->
      <el-backtop :right="28" :bottom="32" />
    </template>

    <!-- 语法专项练习设置弹窗 -->
    <el-dialog v-model="practiceDialogVisible" title="📝 语法专项练习" width="460px" destroy-on-close>
      <div class="practice-desc">为「{{ lesson ? lesson.title : '' }}」生成一份专项练习卷，共 {{ practiceForm.count }} 题（百分制）。</div>
      <el-form label-width="90px" style="margin-top: 12px">
        <el-form-item label="题数">
          <el-radio-group v-model="practiceForm.count">
            <el-radio-button :value="4">4题</el-radio-button>
            <el-radio-button :value="6">6题</el-radio-button>
            <el-radio-button :value="8">8题</el-radio-button>
            <el-radio-button :value="10">10题</el-radio-button>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="难度">
          <el-rate v-model="practiceForm.difficulty" :max="5" />
        </el-form-item>
        <el-form-item label="卷面分数">
          <el-switch v-model="practiceForm.show_score" active-text="显示分数（百分制）" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="practiceDialogVisible = false">取消</el-button>
        <el-button type="warning" :loading="practiceGenerating" @click="generatePractice">生成并去做题</el-button>
      </template>
    </el-dialog>
  </div>
</template>


<script setup>
import { ref, reactive, computed, onMounted, onUnmounted, nextTick, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { grammarApi } from '@/api/grammar'
import { useSubjectStore } from '@/stores/subject'
import { speakSequence, speakZh, stopSpeech, installSpeechUnlock } from '@/utils/speech'

const route = useRoute()
const router = useRouter()
const subjectStore = useSubjectStore()

const categories = ref([])          // 板块（含 count/learned，全量）
const allLessons = ref([])          // 全部语法点（带进度）
const activeCategory = ref(null)
const loading = ref(false)
const lesson = ref(null)            // 当前教程（教程视图）
const lessonLoading = ref(false)

// 筛选
const gradeFilter = ref(null)
const categoryFilter = ref(null)
const keyword = ref('')

// 练习生成
const practiceDialogVisible = ref(false)
const practiceGenerating = ref(false)
const practiceForm = reactive({ count: 6, difficulty: 3, show_score: true })

// 例句朗读
const speakingIndex = ref(null)

const lessonId = computed(() => Number(route.params.id || 0))

const statusLabel = (s) => ({
  learned: '已学',
  practiced: '已练',
  mastered: '已掌握',
}[s] || s || '')

// 按筛选条件过滤后的语法点
const filteredLessons = computed(() => {
  let list = allLessons.value
  if (gradeFilter.value) list = list.filter(l => l.grade === gradeFilter.value)
  if (categoryFilter.value) list = list.filter(l => l.category === categoryFilter.value)
  if (keyword.value) {
    const kw = keyword.value.trim().toLowerCase()
    list = list.filter(l => l.title.toLowerCase().includes(kw))
  }
  return list
})

// 按筛选条件重新聚合板块统计
const filteredCategories = computed(() => {
  const map = new Map()
  for (const l of filteredLessons.value) {
    if (!map.has(l.category)) map.set(l.category, { category: l.category, count: 0, learned: 0 })
    const item = map.get(l.category)
    item.count++
    if (l.progress_status) item.learned++
  }
  return [...map.values()]
})

const activeFilters = computed(() => gradeFilter.value || categoryFilter.value || keyword.value)

// 低年级（1/2 年级）暂未开放语法内容 → 空列表时给出友好提示
const emptyHintGrade = computed(() => {
  if (gradeFilter.value !== 1 && gradeFilter.value !== 2) return null
  if (filteredCategories.value.length > 0) return null
  return gradeFilter.value
})

const allCategories = computed(() => {
  const seen = new Set()
  const out = []
  for (const l of allLessons.value) {
    if (!seen.has(l.category)) {
      seen.add(l.category)
      out.push({ category: l.category })
    }
  }
  return out
})

const lessonsOf = (cat) => filteredLessons.value.filter(l => l.category === cat)

// 同板块其它语法点（教程视图右侧导航）
const siblings = computed(() => {
  if (!lesson.value) return []
  return allLessons.value.filter(l => l.category === lesson.value.category && l.id !== lesson.value.id)
})

/* ---------------- 教程版面：分节卡片 + 目录锚点 + 折叠（长教程体验优化） ---------------- */

// 正文按 `## 小节` 拆分成分节（### 归属其父节），逐节卡片渲染
// text=该节原始 Markdown 纯文本（朗读用，不经过 HTML 渲染）
const contentSections = computed(() => {
  const md = lesson.value?.content_md || ''
  if (!md.trim()) return []
  const parts = md.split(/^##\s+/m)
  const secs = []
  if (parts[0].trim()) secs.push({ title: '', text: parts[0], html: renderMd(parts[0]) })
  for (let i = 1; i < parts.length; i++) {
    const raw = parts[i]
    const nl = raw.indexOf('\n')
    const title = (nl === -1 ? raw : raw.slice(0, nl)).trim()
    const body = nl === -1 ? '' : raw.slice(nl + 1)
    secs.push({ title, text: body, html: renderMd(body) })
  }
  return secs
})

// 折叠状态：key = 's0'/'s1'...（正文节）、'examples'/'mistakes'/'mnemonic'
const collapsed = ref({})
function toggleBlock(key) {
  collapsed.value = { ...collapsed.value, [key]: !collapsed.value[key] }
}

const foldableKeys = computed(() => {
  const keys = []
  contentSections.value.forEach((s, i) => { if (s.title) keys.push('s' + i) })
  if (lesson.value?.examples?.length) keys.push('examples')
  if (lesson.value?.common_mistakes?.length) keys.push('mistakes')
  if (lesson.value?.mnemonic) keys.push('mnemonic')
  return keys
})
const allCollapsed = computed(() => foldableKeys.value.length > 0 && foldableKeys.value.every(k => collapsed.value[k]))
function toggleAllBlocks() {
  const next = !allCollapsed.value
  const obj = { ...collapsed.value }
  foldableKeys.value.forEach(k => { obj[k] = next })
  collapsed.value = obj
}

// 目录（本课包含 / 右侧吸顶目录共用）
const outlineItems = computed(() => {
  const items = []
  contentSections.value.forEach((s, i) => {
    items.push({ id: 'gsec-' + i, icon: '📖', label: s.title || `第 ${i + 1} 节` })
  })
  const ex = lesson.value?.examples || []
  const ms = lesson.value?.common_mistakes || []
  if (ex.length) items.push({ id: 'gsec-examples', icon: '📝', label: `例句（${ex.length}）` })
  if (ms.length) items.push({ id: 'gsec-mistakes', icon: '⚠️', label: `易错点（${ms.length}）` })
  if (lesson.value?.mnemonic) items.push({ id: 'gsec-mnemonic', icon: '🎵', label: '记忆口诀' })
  return items
})

// 滚动高亮当前节
const activeSection = ref('')
let scrollTimer = 0
function onWindowScroll() {
  if (scrollTimer) return
  scrollTimer = window.setTimeout(() => {
    scrollTimer = 0
    const els = document.querySelectorAll('.lesson-block[data-sec]')
    if (!els.length) return
    let cur = ''
    els.forEach((el) => { if (el.getBoundingClientRect().top <= 140) cur = el.id })
    activeSection.value = cur || els[0].id
  }, 80)
}
function scrollToSection(id) {
  // 目标块被折叠时先自动展开，否则跳过去看不到内容
  const keyMap = { 'gsec-examples': 'examples', 'gsec-mistakes': 'mistakes', 'gsec-mnemonic': 'mnemonic' }
  let key = keyMap[id]
  if (!key && id.startsWith('gsec-')) {
    const idx = Number(id.slice(5))
    if (!Number.isNaN(idx) && contentSections.value[idx]?.title) key = 's' + idx
  }
  if (key && collapsed.value[key]) {
    collapsed.value = { ...collapsed.value, [key]: false }
  }
  nextTick(() => {
    const el = document.getElementById(id)
    if (el) el.scrollIntoView({ behavior: 'smooth', block: 'start' })
  })
}

// 底部「上/下一个语法点」
const siblingNav = computed(() => {
  if (!lesson.value) return { prev: null, next: null, pos: 0, total: 0 }
  const list = allLessons.value.filter(l => l.category === lesson.value.category)
  const idx = list.findIndex(l => l.id === lesson.value.id)
  return {
    prev: idx > 0 ? list[idx - 1] : null,
    next: idx >= 0 && idx < list.length - 1 ? list[idx + 1] : null,
    pos: idx + 1,
    total: list.length,
  }
})

// 切换语法点：重置版面状态并回到顶部
function resetLessonView() {
  collapsed.value = {}
  activeSection.value = ''
  window.scrollTo({ top: 0, behavior: 'auto' })
}

// 直达教程页（/grammar/:id）时补加载语法点索引，供「同板块语法点」「上/下一个」导航使用
async function ensureLessonIndex() {
  if (allLessons.value.length) return
  try {
    const { data } = await grammarApi.lessons({})
    allLessons.value = data || []
  } catch (e) { /* 导航辅助数据，失败不阻塞教程阅读 */ }
}

async function fetchCategories() {
  loading.value = true
  try {
    const { data } = await grammarApi.categories()
    categories.value = data || []
    const { data: lessons } = await grammarApi.lessons({})
    allLessons.value = lessons || []
  } catch (e) {
    ElMessage.error('加载语法板块失败：' + (e.response?.data?.detail || e.message))
  } finally {
    loading.value = false
  }
}

function resetExpand() {
  activeCategory.value = null
}

function toggleCategory(cat) {
  activeCategory.value = activeCategory.value === cat ? null : cat
}

async function openLesson(id) {
  router.push('/grammar/' + id)
}

function backToList() {
  router.push('/grammar')
}

/**
 * 同板块语法点切换：直接在前端加载新数据并替换当前 lesson，
 * 用 router.replace 同步 URL（不 push 历史），避免视图闪回列表再重新加载。
 */
async function switchLesson(id) {
  if (!id || (lesson.value && lesson.value.id === id)) return
  lessonLoading.value = true
  try {
    const { data } = await grammarApi.get(id)
    lesson.value = data
    resetLessonView()
    autoTeachLesson() // 自动带读新语法点（设置开时）；内部先停旧课音频
    if (route.params.id !== String(id)) {
      router.replace('/grammar/' + id)
    }
  } catch (e) {
    ElMessage.error('加载语法点失败：' + (e.response?.data?.detail || e.message))
  } finally {
    lessonLoading.value = false
  }
}

async function fetchLesson() {
  if (!lessonId.value) return
  lessonLoading.value = true
  try {
    const { data } = await grammarApi.get(lessonId.value)
    lesson.value = data
    resetLessonView()
    autoTeachLesson() // 自动带读（设置开时）；直达/刷新页面同样生效
  } catch (e) {
    ElMessage.error('加载语法点失败：' + (e.response?.data?.detail || e.message))
  } finally {
    lessonLoading.value = false
  }
}

async function markLearned() {
  if (!lesson.value) return
  try {
    await grammarApi.recordProgress({ lesson_id: lesson.value.id, status: 'learned' })
    lesson.value.progress_status = 'learned'
    ElMessage.success('已标记为已学，去生成一份专项练习巩固吧！')
    fetchCategories()
  } catch (e) {
    ElMessage.error('标记失败：' + (e.response?.data?.detail || e.message))
  }
}

// 轻量 Markdown 渲染（教程正文由 AI 生成，结构受控：## ### ** ** - 列表）
function renderMd(md) {
  if (!md) return ''
  let html = md
    .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
    .replace(/^### (.*)$/gm, '<h4>$1</h4>')
    .replace(/^## (.*)$/gm, '<h3>$1</h3>')
    .replace(/^# (.*)$/gm, '<h2>$1</h2>')
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/^- (.*)$/gm, '<li>$1</li>')
    .replace(/(<li>[\s\S]*?<\/li>)(?![\s\S]*?<li>)/g, '<ul>$1</ul>')
  html = html.replace(/\n{3,}/g, '\n\n').replace(/\n/g, '<br>')
  return html
}

/* ---------------- 语法教程语音：自动带读 + 手动按钮 ---------------- */

// 自动带读开关（localStorage 持久化，默认开：教程以"听"带"看"，避免学生看不进去）
const grammarAutoRead = ref(localStorage.getItem('easyfix_grammar_auto_read') !== '0')
function toggleGrammarAutoRead(v) {
  localStorage.setItem('easyfix_grammar_auto_read', v ? '1' : '0')
}

let grammarTeachToken = 0
// 停止一切语法朗读（自动带读循环 token 失效 + 停当前音频）；切课/关开关/离开页面时调用
function stopGrammarTeach() {
  grammarTeachToken++
  stopSpeech()
}

// 骨架导读：标题 → 总结 → 各节标题 → 口诀（每节全文由节内 🔊 手动朗读，避免长文通读冗长）
async function autoTeachLesson() {
  if (!grammarAutoRead.value || !lesson.value) return
  const token = ++grammarTeachToken
  stopSpeech()
  const parts = []
  if (lesson.value.title) parts.push({ text: lesson.value.title, lang: 'zh-CN' })
  if (lesson.value.summary) parts.push({ text: '，' + lesson.value.summary, lang: 'zh-CN' })
  contentSections.value.forEach((s) => {
    if (s.title) parts.push({ text: '，' + s.title, lang: 'zh-CN' })
  })
  if (lesson.value.mnemonic) parts.push({ text: '，记忆口诀：' + lesson.value.mnemonic, lang: 'zh-CN' })
  for (const p of parts) {
    if (token !== grammarTeachToken) return
    const ok = await speakZh(p.text, { force: true })
    if (!ok) break // 播放失败（未解锁/无网络）静默放弃，不刷屏
  }
}

// 手动朗读一段文本（再点即先停旧再播新）
async function speakText(text) {
  if (!text || !text.trim()) return
  stopGrammarTeach()
  const ok = await speakZh(text, { force: true })
  if (!ok) ElMessage.warning('朗读失败，请检查网络后重试')
}

// 例句朗读（先英文后中文）：统一走 utils/speech，Chrome 无可用语音时自动降级服务器 TTS
async function speakExample(ex, i) {
  if (!ex || (!ex.en && !ex.zh)) return
  if (speakingIndex.value === i) { // 再点一次 = 停止
    stopSpeech()
    speakingIndex.value = null
    return
  }
  speakingIndex.value = i
  const played = await speakSequence([
    ex.en && { text: ex.en, lang: 'en-US', rate: 0.85 },
    ex.zh && { text: '，' + ex.zh, lang: 'zh-CN', rate: 0.95 },
  ])
  if (speakingIndex.value === i) speakingIndex.value = null
  if (!played) ElMessage.warning('朗读失败，请检查网络后重试')
}

function openPracticeDialog() {
  practiceDialogVisible.value = true
}

async function generatePractice() {
  if (!lesson.value) return
  practiceGenerating.value = true
  try {
    const { data } = await grammarApi.generatePractice({
      lesson_id: lesson.value.id,
      count: practiceForm.count,
      difficulty: practiceForm.difficulty,
      question_types: ['choice', 'fill', 'judge', 'sentence'],
      show_score: practiceForm.show_score,
      score_mode: 'hundred',
    })
    practiceDialogVisible.value = false
    ElMessage.success('专项练习卷已生成：' + (data.name || ''))
    // 记录练习进度（有成绩后再由批改接口回写 last_score；这里标记 practiced 待优化）
    try {
      await grammarApi.recordProgress({ lesson_id: lesson.value.id, status: 'practiced' })
      lesson.value.progress_status = 'practiced'
      fetchCategories()
    } catch (e) { /* 进度记录失败不阻塞做题 */ }
    // 直达做题页（PracticeSets 检测 auto_do 参数自动打开做题弹窗）
    router.push('/practice-sets?auto_do=' + data.id)
  } catch (e) {
    ElMessage.error('生成失败：' + (e.response?.data?.detail || e.message))
  } finally {
    practiceGenerating.value = false
  }
}

watch(lessonId, () => {
  if (lessonId.value) {
    // switchLesson 已在前端替换 lesson 数据，避免重复加载导致视图闪缩
    if (!lesson.value || lesson.value.id !== lessonId.value) {
      lesson.value = null
      ensureLessonIndex()
      fetchLesson()
    }
  } else {
    lesson.value = null
    fetchCategories()
  }
})

onMounted(() => {
  installSpeechUnlock() // 首次点击解锁 AudioContext：服务器 TTS 降级音任意时刻可播
  window.addEventListener('scroll', onWindowScroll, { passive: true })
  if (lessonId.value) {
    ensureLessonIndex()
    fetchLesson()
  } else {
    // 学习空间指定年级优先：语法列表默认按当前小孩年级过滤（参考单词页）
    if (subjectStore.activeGrade !== null && gradeFilter.value === null) {
      gradeFilter.value = subjectStore.activeGrade
    }
    fetchCategories()
  }
})

onUnmounted(() => {
  window.removeEventListener('scroll', onWindowScroll)
  if (scrollTimer) window.clearTimeout(scrollTimer)
  stopGrammarTeach() // 离开语法页停掉一切朗读（音频不残留）
})
</script>

<style scoped>
.grammar-page {
  padding: 4px;
}
.grammar-hero {
  margin-bottom: 16px;
  background: linear-gradient(135deg, #f0f9ff, #e6f7ff);
  border: none;
}
.hero-title {
  font-size: 22px;
  font-weight: 700;
  color: #0f4c81;
}
.hero-desc {
  margin-top: 6px;
  color: #5b6b7b;
  font-size: 13px;
}
.loading, .empty {
  text-align: center;
  color: #909399;
  padding: 40px 0;
}
.empty-hint-card {
  display: inline-block;
  background: #f7faff;
  border: 1px solid #dbe7fb;
  border-radius: 14px;
  padding: 28px 40px;
  color: #5b6b7b;
}
.eh-icon {
  font-size: 40px;
  margin-bottom: 10px;
}
.eh-title {
  font-size: 17px;
  font-weight: 800;
  color: #2b6cb0;
  margin-bottom: 8px;
}
.eh-desc {
  font-size: 13px;
  line-height: 1.6;
  margin-bottom: 16px;
  max-width: 420px;
}

/* ---------- 列表视图 ---------- */
.filters {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-bottom: 14px;
  flex-wrap: wrap;
}
.filter-count {
  font-size: 12px;
  color: #909399;
  margin-left: 4px;
}
.category-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
  gap: 14px;
}
.category-card {
  cursor: pointer;
  transition: box-shadow .2s;
}
.category-card:hover {
  box-shadow: 0 4px 16px rgba(0, 0, 0, .12);
}
.category-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.category-name {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}
.category-meta {
  margin-top: 6px;
  font-size: 12px;
  color: #909399;
}
.category-hint {
  margin-top: 10px;
  font-size: 12px;
  color: #a8abb2;
}
.lesson-list {
  margin-top: 10px;
  border-top: 1px dashed #ebeef5;
  padding-top: 6px;
}
.lesson-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 7px 4px;
  border-radius: 6px;
  font-size: 13px;
  color: #303133;
}
.lesson-item:hover {
  background: #f5f7fa;
}
.lesson-item.done .lesson-title {
  color: #67c23a;
}
.lesson-item.mastered .lesson-title {
  color: #67c23a;
  text-decoration: line-through;
}
.lesson-dot {
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: #c0c4cc;
  flex-shrink: 0;
}
.lesson-item.done .lesson-dot, .lesson-item.mastered .lesson-dot {
  background: #67c23a;
}
.lesson-title {
  flex: 1;
}
.lesson-new {
  font-size: 12px;
  color: #a8abb2;
}

/* ---------- 教程视图（两栏布局） ---------- */
.lesson-layout {
  display: flex;
  gap: 16px;
  align-items: flex-start;
}
.lesson-main {
  flex: 1;
  min-width: 0;
  max-width: 860px;
}
.lesson-side {
  width: 300px;
  flex-shrink: 0;
  position: sticky;
  top: 12px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.side-card {
  margin-bottom: 0;
}
.side-title {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 10px;
}
.side-status {
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 13px;
  color: #606266;
  margin-bottom: 10px;
}
.side-btn {
  width: 100%;
  margin-left: 0;
  margin-bottom: 8px;
}
.practice-big-btn {
  font-size: 15px;
  font-weight: 600;
}
.practice-hint {
  font-size: 12px;
  color: #a8abb2;
  line-height: 1.6;
}
.sibling-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 7px 6px;
  border-radius: 6px;
  font-size: 13px;
  color: #303133;
  cursor: pointer;
}
.sibling-item:hover {
  background: #f5f7fa;
}
.sibling-item.active {
  background: #ecf5ff;
  color: #409eff;
}
.sibling-title {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.sibling-item .lesson-dot.done {
  background: #67c23a;
}
.lesson-nav {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}
.auto-read-toggle {
  margin-left: auto;
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #5b6b7b;
}
.lesson-title-row {
  display: flex;
  align-items: center;
  gap: 8px;
}
.lesson-title-big {
  font-size: 24px;
  color: #0f4c81;
  margin: 8px 0 12px;
}
.speak-btn {
  flex-shrink: 0;
  font-size: 14px;
}
.lesson-summary {
  display: flex;
  align-items: flex-start;
  gap: 8px;
  background: #f0f9ff;
  border-left: 4px solid #409eff;
  padding: 10px 14px;
  border-radius: 6px;
  font-size: 15px;
  color: #1d4e7a;
  margin-bottom: 16px;
}
.summary-text {
  flex: 1;
}
/* ---------- 教程分节卡片（长教程体验优化） ---------- */
.lesson-outline {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 14px;
  padding: 8px 10px;
  background: #f7fbff;
  border: 1px dashed #d6e8fa;
  border-radius: 8px;
}
.outline-label {
  font-size: 12px;
  color: #6b7c8f;
  font-weight: 600;
}
.outline-chip {
  font-size: 12px;
  color: #1d6fb8;
  background: #fff;
  border: 1px solid #d6e8fa;
  border-radius: 12px;
  padding: 2px 10px;
  cursor: pointer;
  transition: all 0.15s;
}
.outline-chip:hover {
  background: #ecf5ff;
  border-color: #a8cdf0;
}
.outline-toggle {
  margin-left: auto;
  font-size: 12px;
}
.lesson-block {
  border: 1px solid #eef2f7;
  border-radius: 10px;
  margin-bottom: 12px;
  background: #fff;
  overflow: hidden;
  scroll-margin-top: 84px;
}
.lesson-block:hover {
  border-color: #dbe9f7;
}
.block-head {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 9px 12px;
  background: linear-gradient(90deg, #f6faff, #fbfdff);
  cursor: pointer;
  user-select: none;
  border-bottom: 1px solid #f0f5fa;
}
.block-no {
  flex-shrink: 0;
  min-width: 20px;
  height: 20px;
  line-height: 20px;
  text-align: center;
  border-radius: 6px;
  background: #e8f3ff;
  color: #1d6fb8;
  font-size: 12px;
  font-weight: 700;
}
.block-title {
  flex: 1;
  font-size: 15px;
  font-weight: 600;
  color: #0f4c81;
}
.block-toggle {
  font-size: 12px;
  color: #a8abb2;
}
.block-body {
  padding: 8px 12px 12px;
}
.toc-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 8px;
  border-radius: 6px;
  font-size: 13px;
  color: #4a5a6a;
  cursor: pointer;
}
.toc-item:hover {
  background: #f5f9ff;
}
.toc-item.active {
  background: #ecf5ff;
  color: #1d6fb8;
  font-weight: 600;
}
.toc-icon {
  font-size: 12px;
}
.toc-label {
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.lesson-footer-nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 10px;
  margin-top: 12px;
  padding: 8px 4px;
}
.footer-pos {
  font-size: 12px;
  color: #909399;
}
.lesson-content {
  line-height: 1.9;
  font-size: 14px;
  color: #303133;
  padding: 10px 12px 12px;
}
.lesson-content h3 {
  margin: 14px 0 6px;
  color: #0f4c81;
}
.lesson-content h4 {
  margin: 10px 0 4px;
  color: #303133;
}
.lesson-content li {
  margin-left: 20px;
}
.lesson-section {
  margin-top: 18px;
}
.lesson-section h3 {
  font-size: 15px;
  color: #0f4c81;
  border-bottom: 2px solid #e6f0fa;
  padding-bottom: 6px;
}
.example-item {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  padding: 8px 0;
  border-bottom: 1px dashed #f0f2f5;
}
.example-en {
  font-size: 15px;
  color: #303133;
}
.example-zh {
  font-size: 13px;
  color: #909399;
}
.mistake-item {
  background: #fef0f0;
  border: 1px solid #fde2e2;
  color: #a44141;
  border-radius: 6px;
  padding: 7px 12px;
  margin-bottom: 6px;
  font-size: 13px;
}
.mnemonic-box {
  background: #fdf6ec;
  border: 1px solid #faecd8;
  color: #7a5b2e;
  border-radius: 8px;
  padding: 12px 16px;
  font-size: 16px;
  font-weight: 600;
  text-align: center;
}
.practice-desc {
  color: #606266;
  font-size: 13px;
  line-height: 1.7;
}

@media (max-width: 900px) {
  .lesson-layout {
    flex-direction: column;
  }
  .lesson-side {
    width: 100%;
    position: static;
  }
}

/* ===== 移动端：筛选条件（年级 120 + 板块 170 + 搜索 200 ≈ 490px）单行横向滑动 ===== */
@media screen and (max-width: 768px) {
  .filters {
    display: flex;
    flex-wrap: nowrap;
    gap: 8px;
    overflow-x: auto;
    -webkit-overflow-scrolling: touch;
    padding-bottom: 4px;
    align-items: center;
  }
  .filters .el-select,
  .filters .el-input,
  .filters .filter-count {
    flex: 0 0 auto;
  }
  .filters .filter-count {
    white-space: nowrap;
    font-size: 12px;
  }
}
</style>