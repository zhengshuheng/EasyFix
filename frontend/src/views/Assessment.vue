<template>
  <div class="assessment">
    <!-- 主视觉 Hero：仅在首页（未开始评测）显示；答题时隐藏，避免挤占题目空间 -->
    <div v-if="!inProgress" class="assess-hero">
      <div class="hero-inner">
        <span class="orb orb-1"></span>
        <span class="orb orb-2"></span>
        <span class="orb orb-3"></span>
        <span class="orb orb-4"></span>
        <!-- 模式切换：综合评测（全学科均衡）/ 专项评测（知识模块深度摸底） -->
        <div class="mode-tabs">
          <span class="mode-tab" :class="{ active: mode === 'general' }" @click="mode = 'general'">🎯 综合评测</span>
          <span class="mode-tab" :class="{ active: mode === 'special' }" @click="mode = 'special'">📌 专项评测</span>
        </div>
        <div class="hero-emoji">{{ mode === 'special' ? '🎯' : '📊' }}</div>
        <h2>{{ heroTitle }}</h2>
        <p class="hero-desc">
          {{ mode === 'special'
            ? '针对一个知识模块深度摸底，看看这个专项学得扎不扎实、哪个知识点还欠火候'
            : (readyToAssess ? '做一套标准卷，看看孩子现在学到什么程度、哪个知识点最薄弱' : '选择右上角的「学科」和「年级」，即可开始智能组卷评测') }}
        </p>
        <div v-if="readyToAssess" class="hero-chips">
          <span class="hero-chip">📖 {{ mode === 'special' ? (specialSubjectId === 1 ? '数学' : specialSubjectId === 2 ? '英语' : '语文') : subjectStore.activeSubject?.name }}</span>
          <span class="hero-chip">🎓 {{ subjectStore.activeGradeName }}</span>
          <span class="hero-chip">✏️ {{ questionCount }} 题</span>
        </div>
        <!-- 专项模式：学科选择 + 专项卡片（按课标适用学段过滤） -->
        <div v-if="mode === 'special'" class="hero-special">
          <div class="special-subj">
            <span class="hero-read-label">学科</span>
            <el-select v-model="specialSubjectId" size="large" class="special-subj-select">
              <el-option :value="1" label="数学" />
              <el-option :value="2" label="英语" />
              <el-option :value="3" label="语文" />
            </el-select>
          </div>
          <div v-if="usableSpecials.length" class="special-grid">
            <div
              v-for="s in usableSpecials"
              :key="s.key"
              class="special-card"
              :class="{ active: selectedSpecialty?.key === s.key }"
              @click="selectedSpecialty = s"
            >
              <span class="sc-name">{{ s.name }}</span>
              <span class="sc-desc">{{ s.desc }}</span>
              <span v-if="s.min_grade || s.max_grade" class="sc-grade">适用 {{ s.min_grade }}-{{ s.max_grade }} 年级</span>
            </div>
          </div>
          <div v-else-if="readyToAssess" class="hero-hint">该年级暂无适用专项（按课标学段设计），可先做综合评测</div>
        </div>
        <!-- 卷型选择：标准=检验课内掌握 / 拔高=本年级深度变式（跳一跳够得着）/ 拓展=摸上限可选轻探 -->
        <div v-if="readyToAssess" class="hero-papers">
          <div
            v-for="p in paperOptions"
            :key="p.value"
            class="paper-card"
            :class="{ active: paperType === p.value }"
            @click="paperType = p.value"
          >
            <span class="paper-name">{{ p.label }}</span>
            <span class="paper-desc">{{ p.desc }}</span>
          </div>
        </div>
        <!-- 题目数量选择 -->
        <div v-if="readyToAssess" class="hero-count">
          <span class="hero-count-label">题目数量</span>
          <div class="count-opts">
            <span
              v-for="n in questionCountOptions"
              :key="n"
              class="count-opt"
              :class="{ active: questionCount === n }"
              @click="questionCount = n"
            >{{ n }} 题</span>
          </div>
        </div>
        <!-- 自动读题开关（低年级默认开：孩子不认识字，语音带读；可随时关闭） -->
        <div v-if="readyToAssess" class="hero-read">
          <span class="hero-read-label">🔊 自动读题</span>
          <el-switch v-model="autoRead" size="large" />
          <span class="hero-read-hint">{{ autoRead ? '每道题自动朗读，答题时可点喇叭重听' : '已关闭，答题时可点喇叭手动读题' }}</span>
        </div>
        <div v-if="readyToAssess" class="hero-start-row">
          <el-button
            class="hero-start"
            size="large"
            round
            :disabled="!canStart"
            :loading="starting"
            @click="startAssessment"
          >
            {{ starting ? '正在智能生成题目…' : '开始评测' }}
            <span v-if="!starting" class="btn-arrow">→</span>
          </el-button>
          <!-- 专项练习（非评测）：基础+中等为主，答完只入错题本、不给等级评级 -->
          <el-button
            v-if="mode === 'special'"
            class="hero-start hero-start-secondary"
            size="large"
            round
            :disabled="!canStart"
            :loading="starting"
            @click="startPractice"
          >
            🏋️ 专项练习
          </el-button>
        </div>
        <div v-else class="hero-hint">⬆ 请先在右上角选择「学科」和「年级」</div>
      </div>
    </div>

    <!-- 评测首页：历史记录 -->
    <div v-if="!inProgress" class="assess-home">
      <div class="assess-history">
        <el-card class="history-card" shadow="never">
          <template #header>
            <div class="history-header">
              <span>📚 历史评测</span>
              <el-tag v-if="history.length" size="small" round type="info">{{ history.length }} 次</el-tag>
            </div>
          </template>
          <el-empty v-if="!history.length" description="还没有评测记录，点击上方「开始评测」试试吧" :image-size="80" />
          <div v-else class="history-list">
            <div
              v-for="r in history"
              :key="r.id"
              class="history-item"
              :class="{ 'is-pending': r.status === 'in_progress' }"
              @click="r.status === 'in_progress' ? retakeAssessment(r) : viewReport(r)"
            >
              <div class="hi-left">
                <div class="hi-icon">{{ subjectEmoji(r.subject_name) }}</div>
                <div class="hi-main">
                  <div class="hi-subject">{{ r.subject_name }} · {{ r.grade }}年级<template v-if="r.specialty_name"> · {{ r.specialty_name }}</template></div>
                  <div class="hi-time">{{ formatDate(r.created_at) }}</div>
                </div>
              </div>
              <div class="hi-right">
                <template v-if="r.status === 'in_progress'">
                  <span class="hi-pending">🕐 未完成</span>
                  <el-button size="small" type="primary" round @click.stop="retakeAssessment(r)">重新评测</el-button>
                </template>
                <template v-else>
                  <span class="hi-score">{{ r.score }}<small>/{{ r.total }}</small></span>
                  <el-tag :type="levelTag(r.level)" round>{{ r.level || '未评级' }}</el-tag>
                  <el-button size="small" round @click.stop="retakeAssessment(r)">重新评测</el-button>
                </template>
              </div>
            </div>
          </div>
        </el-card>
      </div>
    </div>

    <!-- 答题中 -->
    <div v-else-if="inProgress" class="assess-quiz">
      <div class="quiz-top">
        <span class="quiz-count">第 {{ qIdx + 1 }} 题 / 共 {{ questions.length }} 题</span>
        <div class="quiz-top-right">
          <el-button
            size="small"
            text
            :type="celebrateOn ? 'primary' : 'info'"
            @click="toggleCelebrate"
            :title="celebrateOn ? '答对彩蛋特效已开启' : '答对彩蛋特效已关闭'"
          >🎉 特效{{ celebrateOn ? '开' : '关' }}</el-button>
          <el-button
            size="small"
            circle
            :type="speakingId === currentQ.question_id ? 'danger' : 'primary'"
            plain
            :disabled="!readableStem"
            @click="speakStem()"
            :title="speakingId === currentQ.question_id ? '停止朗读' : '朗读题目'"
          >🔊</el-button>
          <el-button size="small" text type="info" @click="confirmQuit">⏹ 退出评测</el-button>
        </div>
      </div>
      <el-card class="quiz-card">
        <SceneVisual v-if="currentQ.scene" :scene="currentQ.scene" />
        <div class="quiz-stem">{{ currentQ.stem }}</div>
        <!-- 选择题 -->
        <div v-if="currentQ.type === 'choice'" class="quiz-options">
          <el-button
            v-for="(opt, i) in currentQ.options"
            :key="i"
            class="quiz-option"
            :class="{ 'key-nav-active': !answerState && keyNavIdx === i }"
            :type="answerState ? (choiceLetter(opt) === currentQ.answer ? 'success' : (picked === opt ? 'danger' : 'default')) : 'default'"
            :disabled="!!answerState"
            @click="pickChoice(opt)"
          >
            <span class="opt-letter">{{ choiceLetter(opt) }}.</span> {{ opt }}
          </el-button>
          <div v-if="!answerState" class="key-hint">⌨️ 方向键选答案，回车确认（不用鼠标）</div>
        </div>
        <!-- 填空/解答题 -->
        <div v-else class="quiz-fill">
          <div class="quiz-fill-tip">
            <span>{{ fillTip }}</span>
          </div>
          <el-input
            ref="fillInputRef"
            v-model="fillValue"
            :placeholder="inputPlaceholder"
            size="large"
            :disabled="answerState === 'full' || answerState === 'wrong'"
            @keyup.enter="answerState === '' ? pickFill() : (answerState === 'half' ? correctFill() : null)"
          />
          <el-button
            v-if="!answerState"
            type="primary"
            size="large"
            class="quiz-submit"
            :disabled="!fillValue.trim()"
            @click="pickFill()"
          >
            提交答案
          </el-button>
          <el-button
            v-else-if="answerState === 'half'"
            type="warning"
            size="large"
            class="quiz-submit"
            :disabled="!fillValue.trim()"
            @click="correctFill()"
          >
            📝 订正
          </el-button>
        </div>
        <div v-if="answerState" class="quiz-feedback" style="justify-content: space-between">
          <span class="feedback-text">
            <template v-if="currentQ.type === 'choice'">
              {{ isChoiceCorrect ? '✅ 答对了！' : '❌ 正确答案：' + currentQ.answer }}
            </template>
            <template v-else-if="answerState === 'full'">✅ 答对了！</template>
            <template v-else-if="answerState === 'half'">⚠️ 算式正确，还差单位「{{ missingUnit }}」，补上单位再订正（本题减半记分）</template>
            <template v-else>❌ 正确答案：{{ currentQ.answer }}</template>
          </span>
          <el-button type="primary" size="small" @click="next()">
            {{ qIdx + 1 >= questions.length ? '查看结果' : '下一题' }}
          </el-button>
        </div>
      </el-card>
    </div>

    <!-- 结果页 -->
    <div v-else class="assess-result">
      <el-card class="result-card">
        <div class="result-emoji">{{ scoreRate >= 0.8 ? '🎉' : scoreRate >= 0.5 ? '👍' : '💪' }}</div>
        <h3>{{ levelTitle }}</h3>
        <div class="result-score">{{ score }} <span class="result-total">/ {{ questions.length }}</span></div>
        <el-progress
          :percentage="Math.round(scoreRate * 100)"
          :color="scoreRate >= 0.6 ? '#67c23a' : '#e6a23c'"
          :stroke-width="14"
          style="width: 260px; margin: 12px auto"
        />
        <p class="result-desc">{{ levelDesc }}</p>
        <div class="result-btns">
          <el-button @click="backHome">返回评测首页</el-button>
          <el-button type="primary" @click="startAssessment">再测一次</el-button>
        </div>
      </el-card>
    </div>

    <!-- 历史报告弹窗（专项评测/练习小结共用；专项报告含进步曲线） -->
    <el-dialog v-model="reportVisible" :title="reportTitle" width="680px">
      <div v-if="currentReport" class="report-content">
        <div class="rp-overview">
          <span class="rp-subject">{{ currentReport.subject_name || (currentReport.practice ? '专项练习' : '') }}</span>
          <el-tag v-if="currentReport.specialty_name" type="warning" round>📌 {{ currentReport.specialty_name }}</el-tag>
          <span class="rp-score">{{ currentReport.score }}/{{ currentReport.total }}</span>
          <el-tag :type="levelTag(currentReport.level)" round>{{ currentReport.level || '未评级' }}</el-tag>
          <el-tag v-if="currentReport.practice" type="info" round>练习模式 · 不计等级</el-tag>
        </div>
        <el-tabs v-model="reportTab" class="rp-tabs">
          <!-- Tab 1 能力定位（本年级内，不跨年级判级） -->
          <el-tab-pane label="能力定位" name="locate">
            <div v-if="currentReport.mastery" class="rp-mastery">
              <div class="rp-mastery-head">
                <el-tag :type="masteryTag(currentReport.mastery.level)" size="large" round>{{ currentReport.mastery.label }}</el-tag>
                <span class="rp-advice">{{ currentReport.mastery.advice }}</span>
              </div>
              <div v-if="currentReport.tier_stats" class="rp-tiers">
                <div v-for="t in tierRows" :key="t.key" class="tier-row">
                  <span class="tier-name">{{ t.name }}</span>
                  <el-progress
                    :percentage="tierPct(t.key)"
                    :color="tierColor(t.key)"
                    :stroke-width="10"
                    :show-text="false"
                    style="flex: 1"
                  />
                  <span class="tier-num">{{ tierNum(t.key) }}</span>
                </div>
              </div>
              <div v-if="currentReport.mastery.strengths?.length" class="rp-strong">
                <span class="rp-tag">💪 强项</span>{{ currentReport.mastery.strengths.map(s => s.name).join('、') }} —— 可以往更灵活的方向拓展
              </div>
              <div v-if="currentReport.mastery.weaknesses?.length" class="rp-weak">
                <span class="rp-tag">🎯 巩固</span>{{ currentReport.mastery.weaknesses.map(s => s.name).join('、') }} —— 建议先专项巩固再继续
              </div>
              <div class="rp-note">📌 快速摸底，非专业测评。报告只定位当前年级内的掌握程度，不跨年级评级、不替代学校考试。</div>
            </div>
          </el-tab-pane>
          <!-- Tab 2 知识点（紧凑网格，减少滚动） -->
          <el-tab-pane label="知识点" name="kps">
            <div v-if="currentReport.knowledge?.length" class="kp-grid">
              <div v-for="k in currentReport.knowledge" :key="k.name" class="kp-card">
                <div class="kp-card-name" :title="k.name">{{ k.name }}</div>
                <div class="kp-card-body">
                  <el-progress
                    :percentage="Math.round((k.correct / k.total) * 100)"
                    :color="k.correct / k.total >= 0.8 ? '#67c23a' : k.correct / k.total >= 0.5 ? '#e6a23c' : '#f56c6c'"
                    :stroke-width="8"
                    :show-text="false"
                    style="flex: 1"
                  />
                  <span class="kp-card-num">{{ k.correct }}/{{ k.total }}</span>
                </div>
              </div>
            </div>
          </el-tab-pane>
          <!-- Tab 3 题目回顾 -->
          <el-tab-pane label="题目回顾" name="detail">
            <div v-if="currentReport.detail?.length" class="rp-detail">
              <div v-for="(d, i) in currentReport.detail" :key="i" class="rp-q">
                <div class="rp-q-head">
                  <span class="rp-q-idx">第 {{ i + 1 }} 题</span>
                  <span class="rp-q-mark">{{ Number(d.correct) === 1 ? '✅' : Number(d.correct) === 0.5 ? '⚠️' : '❌' }}</span>
                  <el-tag size="small" :type="Number(d.correct) === 1 ? 'success' : Number(d.correct) === 0.5 ? 'warning' : 'danger'">
                    {{ Number(d.correct) === 1 ? '答对' : Number(d.correct) === 0.5 ? '半对' : '答错' }}
                  </el-tag>
                  <span class="rp-q-kp">{{ d.knowledge }}</span>
                </div>
                <div class="rp-q-stem">{{ d.stem }}</div>
                <div class="rp-q-line"><span class="rp-q-label">我的答案</span>：{{ d.user_answer || '（未作答）' }}</div>
                <div v-if="Number(d.correct) !== 1" class="rp-q-line rp-q-right"><span class="rp-q-label">正确答案</span>：{{ d.answer }}</div>
              </div>
            </div>
          </el-tab-pane>
          <!-- Tab 4 专项进步（阶段 B：同一专项历次正确率曲线） -->
          <el-tab-pane v-if="specialHistory.length" label="专项进步" name="progress">
            <div class="rp-progress">
              <div class="rp-progress-note">📈 {{ currentReport.specialty_name || '专项' }} 历次正确率（专项进步曲线，越练越高）</div>
              <div v-for="(h, i) in specialHistory" :key="h.record_id" class="progress-item">
                <span class="progress-date">{{ h.date }}</span>
                <div class="progress-track">
                  <span
                    class="progress-bar"
                    :style="{ width: (h.rate * 100) + '%', background: h.rate >= 0.8 ? '#67c23a' : h.rate >= 0.5 ? '#e6a23c' : '#f56c6c' }"
                  ></span>
                </div>
                <span class="progress-rate">{{ Math.round(h.rate * 100) }}%</span>
                <span v-if="i > 0 && specialHistory[i - 1]" class="progress-trend">
                  {{ h.rate > specialHistory[i - 1].rate ? '↑' : h.rate < specialHistory[i - 1].rate ? '↓' : '→' }}
                </span>
                <el-tag size="small" :type="levelTag(h.level)" round>{{ h.level || '未评级' }}</el-tag>
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch, nextTick, onUnmounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useSubjectStore } from '@/stores/subject'
import { assessmentApi } from '@/api/assessment'
import { speak, stopSpeech, installSpeechUnlock } from '@/utils/speech'
import SceneVisual from '@/components/SceneVisual.vue'

const subjectStore = useSubjectStore()

// ===== 首页/配置（跟随右上角空间：学科 + 年级） =====
const starting = ref(false)
const history = ref([])

// 评测模式：general=综合评测（全学科知识点均衡）/ special=专项评测（知识模块深度摸底）
const mode = ref('general')
// 专项评测：学科独立选择（专项可跨空间学科）+ 专项列表/选中项
const specialSubjectId = ref(subjectStore.activeSubjectId)
const specialItems = ref([]) // 当前学科专项列表
const specialMap = {} // key -> 专项配置（历史重测用）
const selectedSpecialty = ref(null) // 选中专项配置
// 练习模式（专项练习：不建评测记录、不给等级评级）
const currentPractice = ref(false)

// 卷型（教育理念：深度优先于速度——拔高=本年级深度变式，不是超纲）
const paperType = ref('standard')
const paperOptions = [
  { value: 'standard', label: '标准卷', desc: '检验课内掌握' },
  { value: 'challenge', label: '拔高卷', desc: '跳一跳够得着' },
  { value: 'explore', label: '拓展卷', desc: '摸上限 · 可选轻探' },
]
// 题目数量选择（默认10，支持 5/10/15/20）
const questionCount = ref(10)
const questionCountOptions = [5, 10, 15, 20]

// 空间状态：学科/年级来自右上角切换
const spaceSubjectId = computed(() => subjectStore.activeSubjectId)
const spaceGrade = computed(() => subjectStore.activeGrade)

// 是否已具备评测条件（指定学科 + 指定年级；专项模式用专项学科）
const readyToAssess = computed(() =>
  mode.value === 'special'
    ? !!specialSubjectId.value && !!spaceGrade.value
    : !!spaceSubjectId.value && !!spaceGrade.value
)
const canStart = computed(() => readyToAssess.value && !inProgress.value)

// 标题：X年级X学科能力评测 / 专项评测
const heroTitle = computed(() => {
  if (!readyToAssess.value) return '能力评测'
  const subId = mode.value === 'special' ? specialSubjectId.value : spaceSubjectId.value
  const subName = subId === 1 ? '数学' : subId === 2 ? '英语' : subId === 3 ? '语文' : '学科'
  const gradeName = subjectStore.activeGradeName
  return mode.value === 'special'
    ? `${gradeName}${subName}专项评测`
    : `${gradeName}${subName}能力评测`
})

// 评测请求体（从空间取；专项模式取专项学科）；孩子身份由全局 X-Kid-Id 头携带
function assessPayload() {
  const payload = {
    subject_id: mode.value === 'special' ? specialSubjectId.value : spaceSubjectId.value,
    grade: spaceGrade.value,
    paper_type: paperType.value,
    count: questionCount.value,
  }
  if (mode.value === 'special' && selectedSpecialty.value) {
    payload.specialty = selectedSpecialty.value.key
  }
  return payload
}

// ===== 专项评测 =====
// 当前空间年级（专项卡片按课标适用学段过滤）
const specialGrade = computed(() => spaceGrade.value)
const usableSpecials = computed(() => {
  const g = specialGrade.value
  if (!g) return specialItems.value
  return specialItems.value.filter(s => !s.min_grade || !s.max_grade || (g >= s.min_grade && g <= s.max_grade))
})

async function loadSpecialList() {
  try {
    const { data } = await assessmentApi.specialList(specialSubjectId.value)
    specialItems.value = data?.items || []
    for (const s of specialItems.value) specialMap[s.key] = s
    // 保持选中项在列表内（学科切换后可能失效）
    if (!selectedSpecialty.value || !specialItems.value.some(s => s.key === selectedSpecialty.value.key)) {
      selectedSpecialty.value = usableSpecials.value[0] || specialItems.value[0] || null
    }
  } catch (e) {
    specialItems.value = []
  }
}
watch(specialSubjectId, () => {
  selectedSpecialty.value = null
  loadSpecialList()
})

// ===== 答题 =====
const inProgress = ref(false)
const questions = ref([])
const qIdx = ref(0)
// 当前评测集 id（start 时后端创建；submit 时带回，quit 时废弃）
const currentRecordId = ref(null)
const picked = ref('')
const fillValue = ref('')
const fillInputRef = ref(null) // 答题输入框（自动聚焦用）
// 选择题键盘导航：高亮索引（进入题目默认第一项，方向键移动，回车确认）
const keyNavIdx = ref(0)
// 答对彩蛋开关（localStorage 持久化，默认开——答对自动弹彩蛋，正向即时反馈）
const CELEBRATE_KEY = 'easyfix_assess_celebrate'
function readCelebrateDefault() {
  try {
    const saved = localStorage.getItem(CELEBRATE_KEY)
    if (saved !== null) return saved === '1'
  } catch (e) { /* ignore */ }
  return true
}
const celebrateOn = ref(readCelebrateDefault())
watch(celebrateOn, (v) => {
  try { localStorage.setItem(CELEBRATE_KEY, v ? '1' : '0') } catch (e) { /* ignore */ }
})
// 答题状态：'' 未答 / 'full' 全对 / 'half' 算式对缺单位（可订正）/ 'wrong' 答错
const answerState = ref('')
const score = ref(0)
const answerLog = ref([]) // [{question_id, user_answer}]
const lastLogIdx = ref(-1) // 订正时覆盖最后一条 answerLog 的答案
const submitting = ref(false)
const currentQ = computed(() => questions.value[qIdx.value] || {})
// 低年级数学（1-2 年级）：不会打字记单位、不理解"列算式"，答题只填数字
const isLowGradeMath = computed(() => spaceSubjectId.value === 1 && spaceGrade.value <= 2)
// 答题引导按 学科×题型 分开——各学科作答要求不同，不能共用一套通用文案
// （如英语填空题不能显示数学的"请列式计算"；语文填空也不是"把答案填在下面的框里"）
const fillTip = computed(() => {
  const t = currentQ.value.type
  const s = spaceSubjectId.value
  if (s === 2) {
    // 英语：作答要求以英语学科为准（词形/语序/判断）
    if (t === 'application') return '✏️ 用英语写出算式和答案'
    if (t === 'sentence') return '✏️ 把单词连成正确的句子'
    if (t === 'judge') return '✏️ 判断正误，填 T 或 F'
    if (t === 'reading') return '✏️ 根据短文内容作答'
    if (t === 'fill') return '✏️ 用英语把正确的单词填在横线上'
    return '✏️ 用英语填上正确的答案'
  }
  if (s === 3) {
    // 语文：书写为主，无"列式计算"概念
    if (t === 'judge') return '✏️ 判断正误'
    return '✏️ 把正确答案填在横线上'
  }
  // 数学
  if (isLowGradeMath.value) {
    // 低年级（1-2）：不会打字记单位、不理解"列算式"，只填数字；填写后回车确认
    if (t === 'application') return '🧮 写出算式和答案，不用写单位'
    if (t === 'operation') return '✏️ 按题目要求操作，填上答案就行（不用写单位）'
    return '✏️ 填数字就行，不用写单位（填完按回车确认）'
  }
  if (t === 'application') return '✏️ 请列式计算，把答案填在下面的框里'
  if (t === 'operation') return '✏️ 按题目要求操作，把答案填在下面的框里'
  return '✏️ 把答案填在下面的框里'
})
// 输入框占位提示：低年级提示"填数字后回车确认"
const inputPlaceholder = computed(() => {
  if (isLowGradeMath.value && ['fill', 'calc', 'application', 'operation'].includes(currentQ.value.type)) {
    if (currentQ.value.type === 'application') return '写出算式和答案后按回车确认'
    if (currentQ.value.type === 'operation') return '按题目要求操作后按回车确认'
    return '输入数字后按回车确认'
  }
  return '输入答案'
})
const scoreRate = computed(() => (questions.value.length ? score.value / questions.value.length : 0))
const isChoiceCorrect = computed(() => choiceLetter(picked.value) === currentQ.value.answer)
const missingUnit = computed(() => extractUnit(currentQ.value.answer || ''))

// 与后端 _normalize_answer 保持一致的宽容判分：去空白/全角/尾部量词
function normalizeAnswer(s) {
  if (!s) return ''
  let v = String(s)
    .replace(/[，；．。]/g, c => ({ '，': ',', '；': ';', '．': '.', '。': '.' }[c]))
    .replace(/\s+/g, '')
    .toLowerCase()
    .replace(/[（]/g, '(')
    .replace(/[）]/g, ')')
  for (let i = 0; i < 2; i++) {
    const m = v.match(/([\u4e00-\u9fa5]{0,6})([个只本支颗朵块条张匹头串双把盒袋包排群辆架棵根枝片页元角分米厘米名位岁层间艘列节道件副双沓叠堆筐篮箱株])([\u4e00-\u9fa5]{0,4})$/)
    if (m && m[1] === '') v = v.slice(0, m.index)
    else break
  }
  const map = { '√': '1', '对': '1', '正确': '1', 't': '1', 'true': '1', 'yes': '1', '×': '0', 'x': '0', '错': '0', '错误': '0', 'f': '0', 'false': '0', 'no': '0' }
  return map[v] ?? v
}

// 提取答案单位：优先括号内（本/个…），其次数字后紧跟单位词；无则 ''
function extractUnit(s) {
  if (!s) return ''
  let m = String(s).match(/[（(]([\u4e00-\u9fa5]{1,4})[)）]/)
  if (m) return m[1]
  m = String(s).match(/\d+\s*([\u4e00-\u9fa5]{1,4})\s*$/)
  return m ? m[1] : ''
}

// 填空/解答题三态判分（与后端 _grade_fill_answer 一致）
// 数值对 + 单位齐全 → 1 分；数值对但缺单位/单位错 → 0.5 分（打钩减半，可订正）；数值错 → 0 分
function gradeFill(v) {
  const ans = String(currentQ.value.answer || '')
  if (!v || !ans) return { state: 'wrong', pts: 0 }
  const qn = (normalizeAnswer(ans).match(/\d+/g) || [])
  const un = (normalizeAnswer(v).match(/\d+/g) || [])
  if (!qn.length || !un.length) {
    return normalizeAnswer(v) === normalizeAnswer(ans) ? { state: 'full', pts: 1 } : { state: 'wrong', pts: 0 }
  }
  if (qn[qn.length - 1] !== un[un.length - 1]) return { state: 'wrong', pts: 0 }
  // 低年级数学：数值对即满分，忽略单位（一年级不会打字记单位）
  if (isLowGradeMath.value) return { state: 'full', pts: 1 }
  const qUnit = extractUnit(ans)
  const uUnit = extractUnit(v)
  if (qUnit && uUnit !== qUnit) return { state: 'half', pts: 0.5 }
  return { state: 'full', pts: 1 }
}

// ===== 语音读题（低年级自动带读，家长无需陪读） =====
// 自动读题开关：低年级默认开，用户选择存 localStorage
const AUTO_READ_KEY = 'easyfix_assess_autoread'
function readAutoReadDefault() {
  try {
    const saved = localStorage.getItem(AUTO_READ_KEY)
    if (saved !== null) return saved === '1'
  } catch (e) { /* ignore */ }
  return spaceGrade.value <= 2 // 低年级默认自动带读
}
const autoRead = ref(readAutoReadDefault())
watch(autoRead, (v) => {
  try { localStorage.setItem(AUTO_READ_KEY, v ? '1' : '0') } catch (e) { /* ignore */ }
})

const speakingId = ref(null) // 正在朗读的题目 id
const readableStem = computed(() => !!String(currentQ.value.stem || '').trim() || (currentQ.value.options || []).length > 0)

// 读题文本：题干 +（选择题）选项 +（低年级/填空）操作提醒
function buildSpeakText(q) {
  const parts = []
  const stem = String(q.stem || '').trim()
  if (stem) parts.push(stem)
  if (q.type === 'choice' && q.options && q.options.length) {
    parts.push(q.options.map((o, i) => `选项${String.fromCharCode(65 + i)}，${o}`).join('。'))
  }
  if (q.type === 'judge') parts.push('填 对，或者 错')
  if (isLowGradeMath.value) {
    // 一年级：应用题要求写算式+答案，单位可省略（判分忽略单位）；操作题按题目要求操作
    if (q.type === 'application') {
      parts.push('想一想，写出算式和答案，不用写单位')
    } else if (q.type === 'operation') {
      parts.push('想一想，按题目要求操作，填上答案就行，不用写单位')
    } else if (q.type === 'fill' || q.type === 'calc') {
      parts.push('把算出的答案填进去，不用写单位，填好后按回车键确认')
    } else {
      parts.push('选好答案后，按回车键确认')
    }
  } else if (['fill', 'calc', 'application', 'operation'].includes(q.type)) {
    parts.push('填好答案后，按回车键确认')
  }
  return parts.join('，')
}

function stopSpeak() {
  stopSpeech()
  speakingId.value = null
}

function speakStem() {
  if (speakingId.value === currentQ.value.question_id) {
    stopSpeak()
    return
  }
  const text = buildSpeakText(currentQ.value)
  if (!text) {
    ElMessage.warning('该题没有可朗读的文字内容')
    return
  }
  const id = currentQ.value.question_id
  speakingId.value = id
  speak(text, { lang: 'zh-CN', rate: 0.85 }).then((ok) => {
    if (speakingId.value === id) speakingId.value = null
    if (!ok) ElMessage.warning('朗读失败，请检查网络后重试')
  })
}

function choiceLetter(opt) {
  const idx = currentQ.value.options.indexOf(opt)
  return idx >= 0 ? String.fromCharCode(65 + idx) : ''
}
// ===== 结果/报告 =====
const reportVisible = ref(false)
const currentReport = ref(null)
const reportTab = ref('locate')
const specialHistory = ref([]) // 专项进步曲线数据（专项报告 Tab）

const reportTitle = computed(() => {
  if (currentReport.value?.practice) return '练习小结'
  if (currentReport.value?.specialty_name) return '专项评测报告'
  return '评测报告'
})

const levelTitle = computed(() =>
  scoreRate.value >= 0.8 ? '太棒了！' : scoreRate.value >= 0.5 ? '继续加油！' : '需要多多练习'
)
const levelDesc = computed(() =>
  scoreRate.value >= 0.8
    ? '掌握很好，继续保持！'
    : scoreRate.value >= 0.5
      ? '基础已掌握，建议针对弱项知识点多练一练'
      : '建议先从薄弱知识点重新学起，再做专项练习巩固'
)

function formatDate(v) {
  if (!v) return ''
  const d = new Date(v)
  return `${d.getMonth() + 1}月${d.getDate()}日`
}

function levelTag(level) {
  if (level === '优秀') return 'success'
  if (level === '良好') return 'warning'
  if (level === '待提升') return 'danger'
  return 'info'
}

// 能力定位（本年级内掌握等级）
function masteryTag(level) {
  if (level === 'advanced') return 'success'
  if (level === 'solid') return 'primary'
  if (level === 'foundation') return 'warning'
  return 'danger'
}
const tierRows = [
  { key: 'basic', name: '基础' },
  { key: 'mid', name: '中等' },
  { key: 'hard', name: '拓展' },
]
function tierPct(key) {
  const s = currentReport.value?.tier_stats?.[key]
  if (!s || !s.total) return 0
  return Math.round((s.correct / s.total) * 100)
}
function tierNum(key) {
  const s = currentReport.value?.tier_stats?.[key]
  if (!s) return '0/0'
  return `${s.correct}/${s.total}`
}
function tierColor(key) {
  const p = tierPct(key)
  if (p >= 80) return '#67c23a'
  if (p >= 60) return '#e6a23c'
  return '#f56c6c'
}

function subjectEmoji(name = '') {
  const n = String(name)
  if (n.includes('数学')) return '🔢'
  if (n.includes('语文')) return '📖'
  if (n.includes('英语')) return '🔤'
  return '📚'
}

async function loadHistory() {
  try {
    // 按当前空间学科过滤（数学页不加载英语记录）
    const { data } = await assessmentApi.list(spaceSubjectId.value)
    history.value = data || []
  } catch (e) {
    // 后端未实现时静默
  }
}
// 切换学科/年级时刷新历史（历史记录按当前学科过滤）
watch([spaceSubjectId, spaceGrade], () => {
  if (!inProgress.value) loadHistory()
})

async function startAssessment() {
  if (!canStart.value) return
  if (mode.value === 'special' && !selectedSpecialty.value) {
    ElMessage.warning('请先选择一个专项')
    return
  }
  starting.value = true
  try {
    const payload = assessPayload()
    const { data } = mode.value === 'special'
      ? await assessmentApi.specialStart(payload)
      : await assessmentApi.start(payload)
    currentPractice.value = false
    if (!applyPaper(data)) return
  } catch (e) {
    ElMessage.error('评测启动失败：' + (e.response?.data?.detail || e.message))
  } finally {
    starting.value = false
  }
}

// 专项练习模式（非评测：不建评测记录、不给等级评级，答完入错题本）
async function startPractice() {
  if (!canStart.value) return
  if (!selectedSpecialty.value) {
    ElMessage.warning('请先选择一个专项')
    return
  }
  starting.value = true
  try {
    const { data } = await assessmentApi.practiceStart(assessPayload())
    currentPractice.value = true
    if (!applyPaper(data)) return
    ElMessage.success('专项练习已开始：基础+中等为主，答完自动把错题收进错题本')
  } catch (e) {
    ElMessage.error('练习启动失败：' + (e.response?.data?.detail || e.message))
  } finally {
    starting.value = false
  }
}

// 组卷结果落地（start/practice/历史重测共用）
function applyPaper(data) {
  questions.value = data?.questions || []
  if (!questions.value.length) {
    ElMessage.warning(data?.message || '题库暂时没有合适的题目')
    return false
  }
  if (data?.shortage && data?.message) {
    ElMessage.warning(data.message)
  } else if (data?.generated && data?.generated > 0 && data?.message) {
    ElMessage.success(data.message)
  }
  currentRecordId.value = data?.record_id || null
  inProgress.value = true
  qIdx.value = 0
  picked.value = ''
  fillValue.value = ''
  answerState.value = ''
  answerLog.value = []   // 必须重置：避免上次评测残留答案导致"一题未做也提交"
  lastLogIdx.value = -1
  score.value = 0
  keyNavIdx.value = 0
  // 自动读题（低年级默认开）：进入第一题即语音带读
  if (autoRead.value) speakStem()
  // 自动聚焦输入框（打字题），选择题由高亮承接
  focusFillInput()
  return true
}

// 答对彩蛋：轻量 emoji 爆花（答对自动弹出，正向即时反馈，可开关）
function celebrate() {
  if (!celebrateOn.value) return
  const emojis = ['🎉', '⭐', '✨', '🌟', '💫', '🎊']
  for (let i = 0; i < 16; i++) {
    const s = document.createElement('span')
    s.className = 'confetti-emoji'
    s.textContent = emojis[i % emojis.length]
    s.style.left = (38 + Math.random() * 24) + '%'
    s.style.top = '42%'
    s.style.fontSize = (16 + Math.random() * 20) + 'px'
    const angle = Math.random() * Math.PI * 2
    const dist = 130 + Math.random() * 200
    s.style.setProperty('--dx', (Math.cos(angle) * dist) + 'px')
    s.style.setProperty('--dy', (Math.sin(angle) * dist - 90) + 'px')
    document.body.appendChild(s)
    setTimeout(() => s.remove(), 1500)
  }
}

function toggleCelebrate() {
  celebrateOn.value = !celebrateOn.value
  ElMessage.success(celebrateOn.value ? '答对彩蛋已开启' : '答对彩蛋已关闭')
}

// 进入题目自动聚焦输入框（打字题）；选择题由 keyNavIdx 高亮承接键盘操作
function focusFillInput() {
  nextTick(() => {
    if (currentQ.value.type !== 'choice') fillInputRef.value?.focus?.()
  })
}

// 键盘操作（小孩对鼠标不方便，全流程免鼠标）：
// - 选择题：↑↓ / ←→ 移动高亮选项，回车确认提交
// - 答完（全对/答错）：回车进入下一题
function onKeydown(e) {
  const type = currentQ.value?.type
  if (!type) return
  if (type === 'choice' && !answerState.value) {
    const opts = currentQ.value.options || []
    if (!opts.length) return
    if (['ArrowUp', 'ArrowLeft'].includes(e.key)) {
      e.preventDefault()
      keyNavIdx.value = (keyNavIdx.value + opts.length - 1) % opts.length
    } else if (['ArrowDown', 'ArrowRight'].includes(e.key)) {
      e.preventDefault()
      keyNavIdx.value = (keyNavIdx.value + 1) % opts.length
    } else if (e.key === 'Enter') {
      e.preventDefault()
      if (keyNavIdx.value >= 0 && keyNavIdx.value < opts.length) pickChoice(opts[keyNavIdx.value])
    }
    return
  }
  if (e.key === 'Enter' && (answerState.value === 'full' || answerState.value === 'wrong')) {
    e.preventDefault()
    next()
  }
}
onMounted(() => window.addEventListener('keydown', onKeydown))
onUnmounted(() => window.removeEventListener('keydown', onKeydown))

function pickChoice(opt) {
  if (answerState.value) return
  picked.value = opt
  const correct = isChoiceCorrect.value
  answerState.value = correct ? 'full' : 'wrong'
  answerLog.value.push({ question_id: currentQ.value.question_id, user_answer: opt })
  if (correct) {
    score.value += 1
    celebrate()
  }
}

function pickFill() {
  if (answerState.value) return
  if (!fillValue.value.trim()) return
  const g = gradeFill(fillValue.value.trim())
  answerState.value = g.state
  lastLogIdx.value = answerLog.value.push({ question_id: currentQ.value.question_id, user_answer: fillValue.value.trim() }) - 1
  score.value += g.pts
  if (g.state === 'full') celebrate()
}

// 半对订正：算式已对、只缺单位。补上单位且数值仍对 → 补满 1 分，覆盖 answerLog 为订正后答案
function correctFill() {
  if (answerState.value !== 'half') return
  if (!fillValue.value.trim()) return
  const g = gradeFill(fillValue.value.trim())
  if (g.state === 'full') {
    answerState.value = 'full'
    score.value += 0.5 // 0.5 → 1.0
    if (lastLogIdx.value >= 0) answerLog.value[lastLogIdx.value].user_answer = fillValue.value.trim()
    celebrate()
  } else if (g.state === 'wrong') {
    // 订正时把数值改错了：不二次扣分，维持半对并提示
    ElMessage.warning('算式结果好像不对，请检查一下')
  }
  // g.state === 'half'：单位还是缺/错，继续保持订正态
}

function next() {
  if (qIdx.value + 1 >= questions.value.length) {
    finishAssessment()
  } else {
    qIdx.value += 1
    picked.value = ''
    fillValue.value = ''
    answerState.value = ''
    lastLogIdx.value = -1
    keyNavIdx.value = 0
    // 自动带读下一题
    if (autoRead.value) speakStem()
    // 自动聚焦输入框（打字题），选择题由高亮承接
    focusFillInput()
  }
}

// 提交全量题目：已答用答案，未答 user_answer=''（后端判 0 分）
// 这样 total = 全卷题数，只做 1 题退出就是 1/N，不会虚高成"优秀"
function buildFullAnswers() {
  const map = {}
  for (const a of answerLog.value) map[a.question_id] = a.user_answer
  return questions.value.map(q => ({
    question_id: q.question_id,
    user_answer: map[q.question_id] ?? '',
  }))
}

async function finishAssessment() {
  submitting.value = true
  try {
    if (currentPractice.value) {
      // 专项练习：判分 + 错题同步，不建评测记录；完成即弹练习小结（不给等级评级）
      const { data } = await assessmentApi.practiceSubmit({
        answers: buildFullAnswers(),
        grade: spaceGrade.value,
        duration: 0,
      })
      currentReport.value = { ...(data || {}), practice: true, specialty_name: selectedSpecialty.value?.name || data?.specialty_name || null }
      reportVisible.value = true
    } else {
      await assessmentApi.submit(currentRecordId.value, {
        answers: buildFullAnswers(),
        grade: spaceGrade.value,
        duration: 0,
      })
    }
  } catch (e) {
    ElMessage.warning('成绩提交失败，本次为本地成绩')
  } finally {
    submitting.value = false
    inProgress.value = false
    await loadHistory()
  }
}

// 历史未完成评测：重新评测（后端开新评测集，旧未完成记录自动废弃）
// 专项记录保持专项重测（综合记录走综合）
async function retakeAssessment(r) {
  if (!canStart.value) {
    ElMessage.warning('请先在右上角选择「学科」和「年级」')
    return
  }
  if (r?.specialty) {
    starting.value = true
    try {
      const payload = {
        subject_id: r.subject_id,
        grade: r.grade,
        paper_type: paperType.value,
        count: questionCount.value,
        specialty: r.specialty,
      }
      const { data } = await assessmentApi.specialStart(payload)
      currentPractice.value = false
      if (!applyPaper(data)) return
    } catch (e) {
      ElMessage.error('评测启动失败：' + (e.response?.data?.detail || e.message))
    } finally {
      starting.value = false
    }
    return
  }
  startAssessment()
}

function confirmQuit() {
  const done = answerLog.value.length
  const total = questions.value.length
  const tip =
    done > 0
      ? `退出后本次评测将按全部 ${total} 题结算（已做 ${done} 题计分，未答题目计 0 分），确定退出吗？`
      : '退出后本次评测不计入成绩，确定退出吗？'
  ElMessageBox.confirm(tip, '退出评测', {
    confirmButtonText: '退出',
    cancelButtonText: '继续评测',
    type: 'warning',
  })
    .then(() => {
      if (answerLog.value.length > 0) {
        // 已作答部分照常结算保存，避免白做；按全卷题数计分
        finishAssessment()
      } else {
        // 一题未做：废弃当前评测集（历史里不再显示未完成）
        if (currentRecordId.value) {
          assessmentApi.quit(currentRecordId.value).catch(() => {})
          currentRecordId.value = null
        }
        inProgress.value = false
        loadHistory()
      }
    })
    .catch(() => {})
}

function backHome() {
  inProgress.value = false
  loadHistory()
}

async function viewReport(r) {
  try {
    const { data } = await assessmentApi.detail(r.id)
    currentReport.value = data || r
    reportVisible.value = true
  } catch (e) {
    currentReport.value = r
    reportVisible.value = true
  }
  // 专项记录：拉取该专项的历史（进步曲线数据，阶段 B）
  specialHistory.value = []
  if (r?.specialty) {
    try {
      const { data: hist } = await assessmentApi.specialHistory({
        subject_id: r.subject_id,
        grade: r.grade,
        specialty: r.specialty,
      })
      specialHistory.value = hist?.items || []
    } catch (e) { /* ignore */ }
  }
}

onMounted(() => {
  installSpeechUnlock() // 首次手势解锁 AudioContext：自动读题（服务器 TTS 降级）任意时刻可播
  loadHistory()
  // 专项模式打开时加载专项列表
  watch(mode, (m) => { if (m === 'special') loadSpecialList() }, { immediate: true })
})
</script>

<style scoped>
.assessment {
  padding: 16px 4px 36px;
  min-height: calc(100vh - 120px);
  background: linear-gradient(180deg, #eef2ff 0%, #f8faff 260px, #ffffff 100%);
}
/* ===== 主视觉 Hero ===== */
.assess-hero {
  max-width: 960px;
  margin: 0 auto 22px;
  padding: 0 8px;
}
.hero-inner {
  position: relative;
  overflow: hidden;
  border-radius: 24px;
  background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 55%, #a855f7 100%);
  color: #fff;
  text-align: center;
  padding: 46px 24px 42px;
  box-shadow: 0 14px 34px rgba(99, 102, 241, 0.35);
}
.orb {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.14);
  pointer-events: none;
}
.orb-1 { width: 230px; height: 230px; top: -90px; left: -70px; }
.orb-2 { width: 170px; height: 170px; bottom: -80px; right: -50px; background: rgba(255, 255, 255, 0.1); }
.orb-3 { width: 72px; height: 72px; top: 30px; right: 100px; background: rgba(255, 255, 255, 0.12); }
.orb-4 { width: 40px; height: 40px; bottom: 36px; left: 120px; background: rgba(255, 255, 255, 0.1); }
/* ===== 模式切换（综合/专项） ===== */
.mode-tabs {
  display: inline-flex;
  gap: 8px;
  background: rgba(255, 255, 255, 0.16);
  border-radius: 999px;
  padding: 4px;
  margin-bottom: 18px;
}
.mode-tab {
  padding: 8px 20px;
  border-radius: 999px;
  font-size: 15px;
  font-weight: 600;
  color: rgba(255, 255, 255, 0.82);
  cursor: pointer;
  transition: all 0.2s;
  user-select: none;
}
.mode-tab.active {
  background: #fff;
  color: #6366f1;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.14);
}
/* ===== 专项选择（学科 + 专项卡片） ===== */
.hero-special {
  margin: 18px auto 0;
  max-width: 860px;
  background: rgba(255, 255, 255, 0.92);
  border-radius: 16px;
  padding: 14px 16px;
  text-align: left;
  color: #303133;
}
.special-subj {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 12px;
}
.special-subj .hero-read-label {
  color: #606266;
}
.special-subj-select {
  width: 160px;
}
.special-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 10px;
}
.special-card {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 10px 12px;
  border: 2px solid #e4e7ed;
  border-radius: 12px;
  cursor: pointer;
  transition: all 0.15s;
  background: #fff;
}
.special-card.active {
  border-color: #6366f1;
  background: #eef1ff;
  box-shadow: 0 4px 12px rgba(99, 102, 241, 0.18);
}
.sc-name {
  font-size: 15px;
  font-weight: 700;
  color: #303133;
}
.sc-desc {
  font-size: 12px;
  color: #909399;
  line-height: 1.4;
}
.sc-grade {
  font-size: 11px;
  color: #a855f7;
  background: #f3e8ff;
  border-radius: 6px;
  padding: 1px 6px;
  align-self: flex-start;
}
/* 开始按钮行（评测 + 专项练习） */
.hero-start-row {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 22px;
}
.hero-start-secondary {
  background: rgba(255, 255, 255, 0.18);
  border: 1px solid rgba(255, 255, 255, 0.55);
  color: #fff;
}
.hero-start-secondary:hover,
.hero-start-secondary:focus {
  background: rgba(255, 255, 255, 0.3);
  color: #fff;
}
/* ===== 专项进步曲线（报告 Tab4） ===== */
.rp-progress {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.rp-progress-note {
  font-size: 13px;
  color: #606266;
  margin-bottom: 4px;
}
.progress-item {
  display: flex;
  align-items: center;
  gap: 8px;
}
.progress-date {
  width: 74px;
  font-size: 12px;
  color: #606266;
  flex-shrink: 0;
}
.progress-track {
  flex: 1;
  background: #f2f3f5;
  border-radius: 6px;
  height: 10px;
  overflow: hidden;
}
.progress-bar {
  display: block;
  height: 100%;
  border-radius: 6px;
  transition: width 0.4s;
}
.progress-rate {
  width: 46px;
  font-size: 13px;
  font-weight: 700;
  text-align: right;
  flex-shrink: 0;
}
.progress-trend {
  font-size: 14px;
  color: #67c23a;
  flex-shrink: 0;
}
/* 移动端窄屏：专项卡片单列、按钮竖排 */
@media (max-width: 640px) {
  .special-grid {
    grid-template-columns: 1fr;
  }
  .hero-start-row {
    flex-direction: column;
    align-items: center;
  }
}
.hero-emoji {
  font-size: 54px;
  position: relative;
  filter: drop-shadow(0 6px 14px rgba(0, 0, 0, 0.18));
}
.hero-inner h2 {
  margin: 12px 0 6px;
  color: #fff;
  font-size: 28px;
  letter-spacing: 1px;
  position: relative;
}
.hero-desc {
  color: rgba(255, 255, 255, 0.92);
  font-size: 15px;
  margin: 0;
  position: relative;
}
.hero-chips {
  margin-top: 20px;
  display: flex;
  justify-content: center;
  gap: 10px;
  position: relative;
  flex-wrap: wrap;
}
.hero-chip {
  background: rgba(255, 255, 255, 0.2);
  border: 1px solid rgba(255, 255, 255, 0.38);
  color: #fff;
  padding: 6px 16px;
  border-radius: 999px;
  font-size: 13px;
  backdrop-filter: blur(4px);
}
.hero-papers {
  margin-top: 18px;
  display: flex;
  justify-content: center;
  gap: 10px;
  position: relative;
  flex-wrap: wrap;
}
.paper-card {
  background: rgba(255, 255, 255, 0.14);
  border: 1px solid rgba(255, 255, 255, 0.35);
  color: #fff;
  border-radius: 14px;
  padding: 10px 16px;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  flex-direction: column;
  gap: 3px;
  min-width: 120px;
  backdrop-filter: blur(4px);
}
.paper-card:hover {
  background: rgba(255, 255, 255, 0.24);
}
.paper-card.active {
  background: #ffffff;
  border-color: #ffffff;
  color: #6d28d9;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.2);
}
.paper-name {
  font-weight: 700;
  font-size: 15px;
}
.paper-desc {
  font-size: 12px;
  opacity: 0.85;
}
/* 题目数量选择（跟随卷型卡片的浅胶囊） */
.hero-count {
  margin-top: 14px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}
.hero-count-label {
  color: rgba(255, 255, 255, 0.85);
  font-size: 13px;
}
/* 自动读题开关（跟随卷型卡片的浅胶囊） */
.hero-read {
  margin-top: 14px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}
.hero-read-label {
  color: rgba(255, 255, 255, 0.95);
  font-size: 14px;
  font-weight: 600;
}
.hero-read-hint {
  color: rgba(255, 255, 255, 0.72);
  font-size: 12px;
}
.hero-read :deep(.el-switch.is-checked .el-switch__core) {
  background: rgba(255, 255, 255, 0.3);
  border-color: rgba(255, 255, 255, 0.6);
}
.count-opts {
  display: flex;
  gap: 8px;
}
.count-opt {
  background: rgba(255, 255, 255, 0.14);
  border: 1px solid rgba(255, 255, 255, 0.35);
  color: #fff;
  border-radius: 999px;
  padding: 4px 14px;
  font-size: 13px;
  cursor: pointer;
  transition: all 0.2s;
  user-select: none;
}
.count-opt:hover {
  background: rgba(255, 255, 255, 0.24);
}
.count-opt.active {
  background: #ffffff;
  border-color: #ffffff;
  color: #6d28d9;
  font-weight: 700;
}
.hero-start {
  margin-top: 26px;
  position: relative;
  background: #ffffff;
  border-color: #ffffff;
  color: #7c3aed;
  font-weight: 600;
  height: 46px;
  padding: 0 34px;
  font-size: 16px;
  box-shadow: 0 8px 22px rgba(0, 0, 0, 0.16);
}
.hero-start:hover {
  background: #f3f0ff;
  border-color: #f3f0ff;
  color: #6d28d9;
}
.hero-start.is-disabled {
  background: rgba(255, 255, 255, 0.5) !important;
  border-color: transparent !important;
  color: rgba(124, 58, 237, 0.6) !important;
}
.btn-arrow {
  font-size: 18px;
  margin-left: 4px;
}
.hero-hint {
  margin-top: 22px;
  display: inline-block;
  background: rgba(255, 255, 255, 0.22);
  border: 1px solid rgba(255, 255, 255, 0.4);
  padding: 9px 20px;
  border-radius: 999px;
  font-size: 14px;
  color: #fff;
  position: relative;
}
/* ===== 首页内容 ===== */
.assess-home {
  max-width: 900px;
  margin: 0 auto;
}
.history-card {
  border-radius: 16px;
  border: 1px solid #edeff5;
}
.history-header {
  display: flex;
  align-items: center;
  gap: 8px;
  font-weight: 600;
  font-size: 15px;
}
.history-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.history-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 13px 16px;
  border: 1px solid #f0f2f7;
  border-radius: 12px;
  background: #fff;
  cursor: pointer;
  transition: all 0.2s;
}
.history-item:hover {
  border-color: #c7d2fe;
  box-shadow: 0 6px 18px rgba(99, 102, 241, 0.14);
  transform: translateY(-1px);
}
.hi-left {
  display: flex;
  gap: 12px;
  align-items: center;
}
.hi-icon {
  width: 42px;
  height: 42px;
  border-radius: 12px;
  background: linear-gradient(135deg, #eef2ff, #ede9fe);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
}
.hi-main {
  display: flex;
  flex-direction: column;
  gap: 3px;
}
.hi-subject {
  font-weight: 600;
  color: #303133;
}
.hi-time {
  color: #909399;
  font-size: 12px;
}
.hi-right {
  display: flex;
  gap: 12px;
  align-items: center;
}
.hi-score {
  font-weight: 700;
  font-size: 18px;
  color: #6366f1;
}
.hi-pending {
  font-size: 13px;
  color: #e6a23c;
  font-weight: 600;
  white-space: nowrap;
}
.history-item.is-pending {
  background: #fffaf0;
}
.hi-score small {
  font-size: 12px;
  color: #909399;
  font-weight: 400;
}
.assess-quiz {
  max-width: 640px;
  margin: 20px auto 0;
}
.quiz-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
  color: #606266;
}
.quiz-top-right {
  display: flex;
  align-items: center;
  gap: 8px;
}
.quiz-stem {
  font-size: 18px;
  color: #303133;
  margin-bottom: 20px;
  line-height: 1.6;
}
.quiz-options {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.quiz-option {
  width: 100%;
  justify-content: flex-start;
  height: 44px;
}
/* 键盘导航高亮：选择题方向键选中的选项 */
.quiz-option.key-nav-active {
  border-color: #409eff;
  background: #ecf5ff;
  box-shadow: 0 0 0 1px #409eff inset;
}
.key-hint {
  margin-top: 10px;
  font-size: 12px;
  color: #909399;
  text-align: center;
  background: #f5f7fa;
  border-radius: 8px;
  padding: 6px 10px;
}
/* 答对彩蛋：轻量 emoji 爆花（fixed 定位飞散后自动移除） */
.confetti-emoji {
  position: fixed;
  z-index: 9999;
  pointer-events: none;
  animation: confetti-fly 1.3s ease-out forwards;
}
@keyframes confetti-fly {
  from { transform: translate(0, 0) scale(1); opacity: 1; }
  to { transform: translate(var(--dx), var(--dy)) scale(0.3); opacity: 0; }
}
.opt-letter {
  font-weight: 600;
  margin-right: 4px;
}
.quiz-fill {
  margin-bottom: 12px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.quiz-fill-tip {
  font-size: 14px;
  color: #909399;
  background: #f5f7fa;
  border-radius: 8px;
  padding: 8px 12px;
  line-height: 1.5;
}
.quiz-submit {
  width: 100%;
  margin-top: 4px;
}
.quiz-feedback {
  margin-top: 16px;
  color: #606266;
  display: flex;
  align-items: center;
}
.assess-result {
  max-width: 480px;
  margin: 30px auto 0;
}
.result-card {
  text-align: center;
  padding: 16px;
}
.result-emoji {
  font-size: 44px;
}
.result-card h3 {
  color: #303133;
  margin: 8px 0;
}
.result-score {
  font-size: 32px;
  font-weight: 700;
  color: #409eff;
}
.result-total {
  font-size: 16px;
  color: #909399;
}
.result-desc {
  color: #606266;
  margin: 12px 0;
}
.result-btns {
  margin-top: 8px;
}
.rp-overview {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}
.rp-subject {
  font-weight: 600;
  font-size: 16px;
}
.rp-score {
  font-size: 20px;
  font-weight: 700;
  color: #409eff;
}
.rp-mastery {
  background: #f7f8ff;
  border: 1px solid #e4e7fd;
  border-radius: 12px;
  padding: 12px 14px;
  margin-bottom: 16px;
}
.rp-mastery-head {
  display: flex;
  align-items: flex-start;
  gap: 10px;
  margin-bottom: 10px;
}
.rp-advice {
  flex: 1;
  color: #303133;
  font-size: 13px;
  line-height: 1.6;
  padding-top: 2px;
}
.rp-tiers {
  display: flex;
  flex-direction: column;
  gap: 6px;
  margin: 8px 0;
}
.tier-row {
  display: flex;
  align-items: center;
  gap: 10px;
}
.tier-name {
  width: 42px;
  color: #606266;
  font-size: 13px;
}
.tier-num {
  color: #909399;
  font-size: 12px;
  width: 42px;
  text-align: right;
}
.rp-strong,
.rp-weak {
  font-size: 13px;
  color: #606266;
  line-height: 1.6;
  margin-top: 6px;
}
.rp-tag {
  display: inline-block;
  font-weight: 600;
  margin-right: 6px;
}
.rp-strong .rp-tag {
  color: #67c23a;
}
.rp-weak .rp-tag {
  color: #e6a23c;
}
.rp-note {
  margin-top: 10px;
  font-size: 12px;
  color: #909399;
  border-top: 1px dashed #dfe3f5;
  padding-top: 8px;
  line-height: 1.5;
}
.rp-knowledge h4 {
  margin: 8px 0;
}
.kp-row {
  display: flex;
  align-items: center;
  gap: 10px;
  margin: 6px 0;
}
.kp-name {
  width: 90px;
  color: #606266;
  font-size: 13px;
}
.kp-num {
  color: #909399;
  font-size: 12px;
  width: 36px;
  text-align: right;
}
/* 知识点网格（Tab2 紧凑两列，减少滚动） */
.kp-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}
.kp-card {
  border: 1px solid #e8eaf2;
  border-radius: 10px;
  padding: 8px 10px;
  background: #fafbff;
}
.kp-card-name {
  font-size: 13px;
  color: #303133;
  margin-bottom: 6px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.kp-card-body {
  display: flex;
  align-items: center;
  gap: 8px;
}
.kp-card-num {
  color: #909399;
  font-size: 12px;
  white-space: nowrap;
}
/* 报告 Tab 区：内容超长时仅 Tab 内部滚动，弹窗不整体拉高 */
.rp-tabs :deep(.el-tabs__content) {
  max-height: 56vh;
  overflow-y: auto;
}
.rp-detail {
  margin-top: 14px;
}
.rp-detail h4 {
  margin: 8px 0;
}
.rp-q {
  border: 1px solid #ebeef5;
  border-radius: 8px;
  padding: 10px 12px;
  margin: 8px 0;
  background: #fafafa;
}
.rp-q-head {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}
.rp-q-idx {
  font-weight: 600;
  font-size: 13px;
  color: #303133;
}
.rp-q-mark {
  font-size: 16px;
}
.rp-q-kp {
  margin-left: auto;
  color: #909399;
  font-size: 12px;
}
.rp-q-stem {
  font-size: 14px;
  color: #303133;
  margin-bottom: 6px;
  line-height: 1.6;
}
.rp-q-line {
  font-size: 13px;
  color: #606266;
  margin: 2px 0;
}
.rp-q-label {
  color: #909399;
}
.rp-q-right {
  color: #67c23a;
}
</style>
