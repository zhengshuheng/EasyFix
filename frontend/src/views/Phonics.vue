<template>
  <div class="page-container phonics-page">
    <!-- Hero 头部 + 主 Tab -->
    <div class="phonics-hero">
      <div class="hero-left">
        <div class="hero-title">🔤 自然拼读</div>
        <div class="hero-desc">掌握字母组合的发音规律，见词能读、听音能写。</div>
      </div>
      <div class="hero-right">
        <div class="main-tabs">
          <div class="main-tab" :class="{ active: mode === 'browse' }" @click="mode = 'browse'">📖 规则浏览</div>
          <div class="main-tab" :class="{ active: mode === 'practice' }" @click="mode = 'practice'">🎯 拼读记忆</div>
        </div>
      </div>
    </div>

    <!-- 词库学段选择 + 覆盖统计 -->
    <div class="lexicon-bar">
      <div class="stage-tabs">
        <div
          v-for="s in stages"
          :key="s.value"
          class="stage-tab"
          :class="{ active: stage === s.value }"
          @click="switchStage(s.value)"
        >
          {{ s.label }}
        </div>
      </div>
      <div class="lexicon-stats" v-if="lexiconStats">
        <div class="stat-item">
          <span class="stat-num">{{ lexiconStats.total_words }}</span>
          <span class="stat-label">词库总词数</span>
        </div>
        <div class="stat-sep">·</div>
        <div class="stat-item">
          <span class="stat-num stat-primary">{{ lexiconStats.covered_words }}</span>
          <span class="stat-label">拼读规则覆盖</span>
        </div>
        <div class="stat-sep">·</div>
        <div class="stat-item">
          <span class="stat-num">{{ lexiconStats.covered_rules }}/{{ lexiconStats.rule_count }}</span>
          <span class="stat-label">规则覆盖</span>
        </div>
        <el-progress
          class="stat-progress"
          :percentage="Math.round((lexiconStats.covered_rate || 0) * 100)"
          :stroke-width="10"
          :color="lexiconStats.covered_rate >= 0.6 ? '#67c23a' : '#e6a23c'"
        />
      </div>
      <div class="lexicon-empty" v-else-if="!loading">
        <el-icon><InfoFilled /></el-icon>
        正在统计词库覆盖…
      </div>
    </div>

    <!-- 初中词库为空提示 -->
    <el-alert
      v-if="lexiconStats && lexiconStats.total_words === 0"
      type="warning"
      :closable="false"
      title="当前学段词库还没有单词：先在「单词库」导入对应年级教材词（初中 = 7~9 年级），拼读页会自动按规则归类并统计覆盖。"
      style="margin-bottom: 14px"
    />

    <!-- ============ 浏览模式 ============ -->
    <template v-if="mode === 'browse'">
      <!-- 类别 tab + 搜索 -->
      <div class="phonics-toolbar">
        <div class="cat-tabs">
          <div
            v-for="c in categories"
            :key="c.value"
            class="cat-tab"
            :class="{ active: category === c.value }"
            @click="switchCategory(c.value)"
          >
            {{ c.label }}
          </div>
        </div>
        <el-input v-model="keyword" placeholder="搜字母组合" clearable style="width: 200px" @change="fetchRules">
          <template #prefix><el-icon><Search /></el-icon></template>
        </el-input>
      </div>

      <el-alert
        v-if="rules.length === 0 && !loading"
        type="info"
        :closable="false"
        title="该类别规则已内置，无需生成（示例词可直接点卡片听发音）。"
        style="margin: 14px 0"
      />

      <div v-loading="loading" class="phonics-list">
        <div v-for="rule in rules" :key="rule.id" class="rule-card">
          <div class="rule-head">
            <span class="rule-pattern">{{ rule.pattern }}</span>
            <el-button v-if="rule.pattern" size="small" circle text class="pattern-speak-btn" title="读组合发音（如 ee）" @click.stop="speakPatternSound(rule)">
              <el-icon><VolumeHigh /></el-icon>
            </el-button>
            <span v-if="rule.sound" class="rule-sound">{{ rule.sound }}</span>
            <span v-if="rule.grade" class="rule-grade">建议{{ gradeCn(rule.grade) }}</span>
            <div class="rule-head-right">
              <el-button v-if="rule.example_words && rule.example_words.length" size="small" type="primary" plain @click.stop="speakRuleSounds(rule)">
                <el-icon><Headset /></el-icon>
                连读示例
              </el-button>
            </div>
          </div>
          <div class="rule-text">{{ rule.rule_text }}</div>
          <div v-if="rule.example_words && rule.example_words.length" class="rule-words">
            <div v-for="(w, i) in rule.example_words" :key="i" class="rule-word" @click="speak(w.en)">
              <el-icon class="speak-icon"><VolumeHigh /></el-icon>
              <div class="word-texts">
                <span class="word-en">{{ w.en }}</span>
                <span class="word-cn">{{ w.cn }}</span>
              </div>
            </div>
          </div>
          <!-- 词库覆盖：从单词表按学段提取归类 -->
          <div v-if="rule.lexicon_count !== undefined" class="lexicon-zone" @click="toggleLexicon(rule)">
            <div class="lexicon-head">
              <span class="lexicon-title">
                <el-icon><Collection /></el-icon>
                词库覆盖 {{ rule.lexicon_count }} 词
              </span>
              <span class="lexicon-toggle">{{ rule._lexiconOpen ? '收起 ▲' : '展开 ▼' }}</span>
            </div>
            <div v-if="rule._lexiconOpen" class="lexicon-words">
              <div v-for="(w, i) in rule.lexicon_words" :key="i" class="lexicon-word" @click.stop="speak(w.en)">
                <span class="lw-en">{{ w.en }}</span>
                <span class="lw-cn">{{ w.cn }}</span>
                <span v-if="w.grade" class="lw-grade">{{ gradeCn(w.grade) }}</span>
              </div>
              <div v-if="rule.lexicon_words && rule.lexicon_count > rule.lexicon_words.length" class="lexicon-more">
                仅显示前 {{ rule.lexicon_words.length }} 个，共 {{ rule.lexicon_count }} 词
              </div>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- ============ 练习模式 ============ -->
    <template v-else>
      <div class="practice-body">
        <!-- 题型选择 / 开始 -->
        <div v-if="!practiceStarted" class="practice-start">
          <div class="practice-hero">
            <div class="practice-hero-icon">🎯</div>
            <h3>选择一种记忆方式</h3>
            <div class="practice-hero-desc">听音辨词 · 看词归类，10 题一轮，答错自动进错题集合</div>
          </div>
          <div class="practice-type-cards">
            <div class="practice-type-card" :class="{ active: practiceType === 'listen' }" @click="practiceType = 'listen'">
              <div class="pt-icon">🔊</div>
              <div class="pt-name">听音选词</div>
              <div class="pt-desc">听单词发音，选出正确的拼写</div>
            </div>
            <div class="practice-type-card" :class="{ active: practiceType === 'match' }" @click="practiceType = 'match'">
              <div class="pt-icon">🔤</div>
              <div class="pt-name">看词选组合</div>
              <div class="pt-desc">看单词，判断属于哪个字母组合</div>
            </div>
          </div>

          <!-- 错题集合卡片区（参考单词页今日任务） -->
          <div v-if="wrongWords.length" class="wrong-set-card">
            <div class="ws-header">
              <div class="ws-title">📋 错题集合 <span class="ws-count">{{ wrongWords.length }} 条</span></div>
              <el-button text type="primary" size="small" @click="wrongDialogVisible = true">查看全部 ›</el-button>
            </div>
            <div class="ws-desc">记忆时记错的组合/示例词自动进错题本，优先复习，答对自动移出</div>
            <div class="ws-sections">
              <div
                v-for="c in wrongCatStats"
                :key="c.value"
                class="ws-section"
                @click="startWrongPractice(c.value)"
              >
                <span class="ws-dot"></span>
                <span class="ws-name">{{ c.label }}</span>
                <b class="ws-num">{{ c.count }}</b>
                <span class="ws-go">开始 ›</span>
              </div>
            </div>
            <div class="ws-actions">
              <el-button type="warning" plain :disabled="canPractice === false" @click="startWrongPractice()">
                🔁 只记全部错题
              </el-button>
              <el-button plain @click="wrongDialogVisible = true">📋 查看错题集合</el-button>
            </div>
          </div>
          <div v-else class="wrong-set-empty">
            ✅ 暂无错题：记忆时记错的题会自动进入错题集合，优先复习
          </div>

          <div class="practice-start-btns">
            <el-button type="primary" size="large" :disabled="canPractice === false" @click="startPractice(false)">
              开始记忆（10 题）
            </el-button>
          </div>
          <el-alert
            v-if="canPractice === false"
            type="warning"
            :closable="false"
            title="当前类别还没有规则/示例词，可切换到其他类别。"
            style="margin-top: 12px"
          />
        </div>

        <!-- 答题中 -->
        <div v-else-if="!practiceDone && currentQ" class="practice-quiz">
          <div class="quiz-top">
            <span class="quiz-count">第 {{ qIdx + 1 }} 题 / 共 {{ questions.length }} 题</span>
            <span class="quiz-score">得分：{{ score }}</span>
            <el-button size="small" text type="info" @click="quitPractice">⏹ 结束记忆</el-button>
          </div>
          <div class="quiz-card" :class="answered ? (picked === currentQ.answer ? 'right' : 'wrong') : ''">
            <template v-if="currentQ.type === 'listen'">
              <div class="quiz-label">听发音，选出正确的单词</div>
              <div class="quiz-rule-hint">字母组合 {{ currentQ.ruleText }}</div>
              <el-button circle size="large" class="quiz-speak" @click="speak(currentQ.word)">
                <el-icon :size="28"><VolumeHigh /></el-icon>
              </el-button>
            </template>
            <template v-else>
              <div class="quiz-label">这个单词属于哪个字母组合？</div>
              <div class="quiz-word">{{ currentQ.word }}</div>
              <div class="quiz-cn">{{ currentQ.cn }}</div>
              <el-button size="small" circle text class="quiz-speak-small" @click="speak(currentQ.word)">
                <el-icon><VolumeHigh /></el-icon>
              </el-button>
            </template>
          </div>
          <div class="quiz-options">
            <el-button
              v-for="(opt, i) in currentQ.options"
              :key="i"
              class="quiz-option"
              :type="answered ? (opt === currentQ.answer ? 'success' : (picked === opt ? 'danger' : 'default')) : 'default'"
              :disabled="answered"
              @click="answer(opt)"
            >
              {{ opt }}
            </el-button>
          </div>
          <div v-if="answered" class="quiz-feedback" :class="picked === currentQ.answer ? 'fb-right' : 'fb-wrong'">
            {{ picked === currentQ.answer ? '✅ 答对了！' : '❌ 答错了，正确答案是「' + currentQ.answer + '」' }}
            <el-button type="primary" size="small" style="margin-left: 12px" @click="next()">
              {{ qIdx + 1 >= questions.length ? '查看结果' : '下一题' }}
            </el-button>
          </div>
        </div>

        <!-- 完成统计 -->
        <div v-else class="practice-result">
          <div class="result-card">
            <div class="result-emoji">{{ score >= questions.length * 0.8 ? '🎉' : score >= questions.length * 0.5 ? '👍' : '💪' }}</div>
            <h3>{{ score >= questions.length * 0.8 ? '太棒了！' : score >= questions.length * 0.5 ? '继续加油！' : '再来一次！' }}</h3>
            <div class="result-score">{{ score }} <span class="result-total">/ {{ questions.length }}</span></div>
            <el-progress :percentage="Math.round(score / questions.length * 100)" :color="score >= questions.length * 0.6 ? '#67c23a' : '#e6a23c'" style="width: 260px; margin: 12px auto" :stroke-width="14" />
            <div v-if="clearedCount > 0" class="result-cleared">
              ✅ 本轮复习掌握 {{ clearedCount }} 条历史错题，已移出错题集合
            </div>
            <div v-if="wrongs.length" class="result-wrongs">
              <div class="rw-title">答错的题（已记入错题集合，下次优先复习）：</div>
              <el-tag v-for="(w, i) in wrongs" :key="i" closable style="margin: 4px 6px" @close="wrongs.splice(i, 1)">
                {{ w.word }} → {{ w.answer }}
              </el-tag>
              <div class="rw-tip">点「复习错题」只复习答错的题</div>
            </div>
            <div class="result-btns">
              <el-button @click="retryWrongs" :disabled="wrongs.length === 0">复习错题</el-button>
              <el-button type="primary" @click="startPractice(false)">再来一轮</el-button>
              <el-button @click="practiceStarted = false">换题型</el-button>
            </div>
          </div>
        </div>
      </div>
    </template>

    <!-- 错题集合弹窗 -->
    <el-dialog v-model="wrongDialogVisible" title="📋 错题集合" width="620px" top="8vh">
      <div v-if="!wrongWords.length" class="wrong-dialog-empty">
        🎉 还没有错题，继续记忆吧！
      </div>
      <template v-else>
        <div class="wrong-dialog-tip">
          共 {{ wrongWords.length }} 条 · 点单词可听发音 · 答对后自动移出错题集合
        </div>
        <div class="wrong-dialog-list">
          <div v-for="w in wrongWords" :key="w.word" class="wrong-dialog-item">
            <div class="wdi-left">
              <span class="wdi-word" @click="speak(w.word)">{{ w.word }}</span>
              <el-icon class="wdi-speak" @click="speak(w.word)"><VolumeHigh /></el-icon>
              <span v-if="wordCnMap[w.word]" class="wdi-cn">{{ wordCnMap[w.word] }}</span>
            </div>
            <div class="wdi-mid">
              <el-tag v-if="w.pattern" size="small" type="info" effect="plain">{{ w.pattern }}</el-tag>
              <el-tag size="small" :type="wrongCatColor(w.category)" effect="plain">{{ wrongCatLabel(w.category) }}</el-tag>
              <span class="wdi-count">错 {{ w.wrong_count }} 次</span>
              <span class="wdi-time">{{ fmtTime(w.updated_at) }}</span>
            </div>
            <div class="wdi-right">
              <el-button size="small" text type="primary" @click="speak(w.word)">🔊</el-button>
              <el-button size="small" text type="danger" @click="removeWrong(w)">删除</el-button>
            </div>
          </div>
        </div>
      </template>
      <template #footer>
        <el-button v-if="wrongWords.length" type="danger" plain @click="clearWrongs">🗑 清空错题</el-button>
        <el-button @click="wrongDialogVisible = false">关闭</el-button>
        <el-button type="primary" :disabled="!wrongWords.length || canPractice === false" @click="startWrongPractice()">
          🎯 只记错题
        </el-button>
      </template>
    </el-dialog>

    <div class="phonics-footer-tip">{{ mode === 'browse' ? '示例词发音：点击卡片即可；未缓存时首次稍慢' : '记忆结束后可复习错题' }}</div>

    <!-- 家长验证：学生删除/清空拼读错题需家长认证 -->
    <ParentLockDialog
      v-model="parentGuardVisible"
      title="家长验证"
      tip="删除错题需要家长验证"
      confirm-text="验证并删除"
      @success="onParentVerified"
      @update:model-value="!$event && onParentGuardCancel()"
    />
  </div>
</template>

﻿<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import ParentLockDialog from '@/components/ParentLockDialog.vue'
import { useParentGuard } from '@/composables/useParentGuard'
import { playServerTts } from '@/utils/speech'

// 家长认证守卫：学生删除/清空拼读错题需家长验证
const {
  visible: parentGuardVisible,
  guard,
  onVerified: onParentVerified,
  onCancel: onParentGuardCancel,
} = useParentGuard()

const category = ref('vowel')
const keyword = ref('')
const rules = ref([])
const loading = ref(false)

// ===== 词库学段（小学/初中）=====
const stages = [
  { value: 'primary', label: '🏫 小学词库' },
  { value: 'junior', label: '🏛 初中词库' },
]
const stage = ref('primary')
const lexiconStats = ref(null)

// ===== 练习模式状态 =====
const mode = ref('browse')
const practiceType = ref('listen')
const practiceStarted = ref(false)
const practiceDone = ref(false)
const questions = ref([])
const qIdx = ref(0)
const score = ref(0)
const picked = ref('')
const answered = ref(false)
const wrongs = ref([])          // 本轮答错的题（结束后保存为错题）
const clearedWords = ref([])    // 本轮答对的历史错题（结束后移出错题池）
const wrongWords = ref([])      // 历史错题池（后端按小孩持久化）
const onlyWrongs = ref(false)   // 是否只练错题
const wrongDialogVisible = ref(false)  // 错题集合弹窗
const pendingWrongStart = ref(false)   // 切类别后自动开始错题练习

const wrongCatStats = computed(() => {
  const list = categories.map(c => ({ ...c, count: 0 }))
  wrongWords.value.forEach(w => {
    const c = list.find(x => x.value === w.category)
    if (c) c.count += 1
  })
  return list.filter(c => c.count > 0)
})

// 错题词 → 中文释义（从当前规则示例词/词库词中反查）
const wordCnMap = computed(() => {
  const map = {}
  rules.value.forEach(r => {
    ;[...(r.example_words || []), ...(r.lexicon_words || [])].forEach(w => {
      if (w.en && !map[w.en]) map[w.en] = w.cn || ''
    })
  })
  return map
})

function wrongCatLabel(val) {
  return (categories.find(c => c.value === val) || {}).label || val || '—'
}
function wrongCatColor(val) {
  return { vowel: 'warning', consonant: 'success', silent_e: 'danger' }[val] || 'info'
}
function fmtTime(t) {
  if (!t) return ''
  try {
    const d = new Date(t)
    return `${d.getMonth() + 1}月${d.getDate()}日 ${String(d.getHours()).padStart(2, '0')}:${String(d.getMinutes()).padStart(2, '0')}`
  } catch (e) {
    return ''
  }
}

const categories = [
  { value: 'vowel', label: '元音组合' },
  { value: 'consonant', label: '辅音组合' },
  { value: 'silent_e', label: '不发音 e' },
]

const clearedCount = computed(() => clearedWords.value.length)

const canPractice = computed(() => {
  // 需要至少 1 条规则有词（示例词或词库词）才能出题
  return rules.value.some(r => (r.example_words || []).length > 0 || (r.lexicon_words || []).length > 0)
})

function shuffle(arr) {
  return [...arr].sort(() => Math.random() - 0.5)
}

function switchCategory(val) {
  if (category.value === val) return
  category.value = val
  fetchRules()
}

function switchStage(val) {
  if (stage.value === val) return
  stage.value = val
  fetchRules()
  fetchLexiconStats()
}

async function fetchLexiconStats() {
  try {
    const res = await fetch('/api/phonics/lexicon-stats?stage=' + stage.value)
    if (res.ok) lexiconStats.value = await res.json()
  } catch (e) {
    /* 静默：统计失败不影响浏览 */
  }
}

// 展开/收起规则的词库覆盖词列表
function toggleLexicon(rule) {
  if (!rule._lexiconOpen && !rule.lexicon_words) {
    // 已由后端一次性返回，无需额外加载
  }
  rule._lexiconOpen = !rule._lexiconOpen
}

function buildQuestions(type, count = 10, onlyWrong = false) {
  const allRules = rules.value.filter(r => (r.example_words || []).length > 0)
  if (!allRules.length) return []
  // 收集所有词（关联规则）：词库覆盖词（按学段提取）优先，示例词兜底
  const allWords = []
  allRules.forEach(r => {
    const pool = (r.lexicon_words && r.lexicon_words.length) ? r.lexicon_words : (r.example_words || [])
    pool.forEach(w => allWords.push({ en: w.en, cn: w.cn, rule: r }))
  })
  if (allWords.length < 2) return []
  // 错题池词：历史错题（按词或规则匹配）优先出题，且顺序排在最前
  const wrongEn = new Set(wrongWords.value.map(w => w.word))
  const wrongRuleIds = new Set(wrongWords.value.map(w => w.rule_id))
  const wrongPool = allWords.filter(w => wrongEn.has(w.en) || wrongRuleIds.has(w.rule.id))
  // 跨类别错题：当前词池匹配不到的错题直接补充（用错题自身的词/组合构造）
  const wrongExtra = wrongWords.value
    .filter(w => !wrongPool.some(x => x.en === w.word))
    .map(w => ({ en: w.word, cn: wordCnMap.value[w.word] || '', rule: { id: w.rule_id, pattern: w.pattern } }))
  const freshPool = shuffle(allWords.filter(w => !wrongEn.has(w.en)))
  // 顺序 = 错题词（固定复习） → 新词（随机补充）
  let pool
  if (onlyWrong) {
    pool = [...wrongPool, ...wrongExtra]
    if (pool.length < 2) pool = [...pool, ...freshPool]
  } else {
    pool = [...wrongPool, ...wrongExtra, ...freshPool]
  }
  const qs = []
  const usedWords = new Set()
  const usedRules = new Set()
  for (let i = 0; i < count && i < pool.length; i++) {
    // 错题段顺序取（保证本轮复习到所有错题），新词段随机取
    let w
    if (i < wrongPool.length) {
      w = pool[i]
    } else {
      const j = i + Math.floor(Math.random() * (pool.length - i))
      w = pool[j]
      pool[j] = pool[i]
    }
    if (usedRules.has(w.rule.id) && i >= wrongPool.length) {
      const alt = pool.slice(i).find(x => !usedRules.has(x.rule.id))
      if (alt) { w = alt }
    }
    usedRules.add(w.rule.id)
    usedWords.add(w.en)

    if (type === 'listen') {
      // 听音选词：选项为 4 个拼写
      const others = allWords.filter(x => x.en !== w.en && !usedWords.has(x.en))
      const distractors = shuffle(others).slice(0, 3).map(x => x.en)
      const options = shuffle([w.en, ...distractors])
      qs.push({ type, word: w.en, cn: w.cn, answer: w.en, options, ruleText: w.rule.pattern, ruleId: w.rule.id })
    } else {
      // 看词选组合：选项为 4 个 pattern
      const otherRules = allRules.filter(x => x.id !== w.rule.id && !usedRules.has(x.id))
      const distractors = shuffle(otherRules).slice(0, 3).map(x => x.pattern)
      const options = shuffle([w.rule.pattern, ...distractors])
      qs.push({ type, word: w.en, cn: w.cn, answer: w.rule.pattern, options, ruleId: w.rule.id })
    }
  }
  return qs
}

function resetPractice() {
  practiceStarted.value = false
  practiceDone.value = false
  questions.value = []
  qIdx.value = 0
  score.value = 0
  picked.value = ''
  answered.value = false
  wrongs.value = []
  clearedWords.value = []
  onlyWrongs.value = false
}

// 中途退出练习：先保存本轮错题，再回到题型选择页
function quitPractice() {
  saveAttempts()
  resetPractice()
  ElMessage.info('已结束记忆')
}

function startPractice(onlyWrong = false) {
  const qs = buildQuestions(practiceType.value, 10, onlyWrong)
  if (!qs.length) {
    ElMessage.warning('该类别示例词不足，无法出题，可切换类别试试')
    return
  }
  resetPractice()
  onlyWrongs.value = !!onlyWrong
  questions.value = qs
  practiceStarted.value = true
  autoplayCurrent()
}

// 从错题集合进入「只练错题」（可指定类别，先切类别再开始）
function startWrongPractice(catValue) {
  if (catValue && category.value !== catValue) {
    switchCategory(catValue)
    wrongDialogVisible.value = false
    // 等待规则加载后开始错题练习
    pendingWrongStart.value = true
    return
  }
  wrongDialogVisible.value = false
  startPractice(true)
}

// 删除单条错题（家长认证：学生需家长验证）
async function removeWrong(w) {
  try {
    await guard(async () => {
      const res = await fetch('/api/phonics/wrong-words/clear', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...kidHeaders() },
        body: JSON.stringify({ words: [w.word] }),
      })
      if (!res.ok) throw new Error('clear failed')
      wrongWords.value = wrongWords.value.filter(x => x.word !== w.word)
    })
    ElMessage.success('已移出错题集合')
  } catch (e) { /* 取消或失败：静默 */ }
}

// 清空错题（家长认证：学生需家长验证）
async function clearWrongs() {
  try {
    const words = wrongWords.value.map(w => w.word)
    if (!words.length) return
    await guard(async () => {
      const res = await fetch('/api/phonics/wrong-words/clear', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', ...kidHeaders() },
        body: JSON.stringify({ words }),
      })
      if (!res.ok) throw new Error('clear failed')
      wrongWords.value = []
    })
    ElMessage.success('已清空错题集合')
  } catch (e) { /* 取消或失败：静默 */ }
}

// 原生 fetch 需要手动注入 X-Kid-Id（http.js 只包装 axios）
function kidHeaders() {
  const headers = {}
  try {
    const kid = JSON.parse(localStorage.getItem('easyfix_kid') || 'null')
    if (kid && kid.id) headers['X-Kid-Id'] = String(kid.id)
  } catch (e) { /* 无孩子上下文时后端会给出明确报错 */ }
  return headers
}

// 练习结束/退出时持久化：新增错题 + 清除已掌握的错题
function saveAttempts() {
  const newWrongs = wrongs.value.filter(w => w.word).map(w => ({
    rule_id: w.ruleId,
    word: w.word,
    pattern: w.answer,
    category: category.value,
  }))
  const headers = { 'Content-Type': 'application/json', ...kidHeaders() }
  if (newWrongs.length) {
    fetch('/api/phonics/wrong-words', {
      method: 'POST',
      headers,
      body: JSON.stringify({ items: newWrongs }),
    }).catch(() => {})
  }
  if (clearedWords.value.length) {
    fetch('/api/phonics/wrong-words/clear', {
      method: 'POST',
      headers,
      body: JSON.stringify({ words: clearedWords.value }),
    }).then(async r => {
      if (r.ok) loadWrongWords()
    }).catch(() => {})
  }
}

function autoplayCurrent() {
  const q = questions.value[qIdx.value]
  if (q && q.type === 'listen') {
    speak(q.word)
  }
}

const currentQ = computed(() => questions.value[qIdx.value] || null)

function answer(opt) {
  if (answered.value) return
  picked.value = opt
  answered.value = true
  const q = currentQ.value
  if (!q) return
  if (opt === q.answer) {
    score.value += 1
    // 答对的是历史错题 → 计入掌握，结束后移出错题池（含只练错题模式）
    if (wrongWords.value.some(w => w.word === q.word)) {
      if (!clearedWords.value.includes(q.word)) clearedWords.value.push(q.word)
    }
  } else {
    if (!wrongs.value.some(w => w.word === q.word)) {
      wrongs.value.push({ word: q.word, answer: q.answer, cn: q.cn || '', ruleId: q.ruleId || null })
    }
  }
}

function next() {
  if (qIdx.value + 1 >= questions.value.length) {
    // 完成：持久化错题（本轮答错入池 + 答对的历史错题清除）
    saveAttempts()
    practiceDone.value = true
    return
  }
  qIdx.value += 1
  picked.value = ''
  answered.value = false
  autoplayCurrent()
}

function retryWrongs() {
  if (!wrongs.value.length) return
  // 用错题重新构造听音选词题
  const qs = wrongs.value.map(w => ({
    type: 'listen',
    word: w.word,
    cn: w.cn || '',
    answer: w.word,
    options: shuffle([w.word, ...shuffle(allWordsForPractice()).filter(x => x !== w.word).slice(0, 3)]),
    ruleText: '',
    ruleId: w.ruleId || null,
  }))
  questions.value = qs
  wrongs.value = []
  practiceDone.value = false
  qIdx.value = 0
  score.value = 0
  picked.value = ''
  answered.value = false
  autoplayCurrent()
}

function allWordsForPractice() {
  const s = new Set()
  rules.value.forEach(r => {
    ;[...(r.example_words || []), ...(r.lexicon_words || [])].forEach(w => s.add(w.en))
  })
  return [...s]
}

const gradeCn = (g) => ['一', '二', '三', '四', '五', '六'][g - 1] + '年级'

async function fetchRules() {
  loading.value = true
  try {
    let url = '/api/phonics?category=' + category.value + '&stage=' + stage.value
    if (keyword.value) url += '&keyword=' + encodeURIComponent(keyword.value)
    const res = await fetch(url)
    rules.value = await res.json()
  } catch (e) {
    ElMessage.error('加载规则失败')
  } finally {
    loading.value = false
  }
  loadWrongWords()
  if (pendingWrongStart.value) {
    pendingWrongStart.value = false
    startPractice(true)
  }
}

// 加载拼读错题池（按小孩，后端持久化）
async function loadWrongWords() {
  try {
    const res = await fetch('/api/phonics/wrong-words', { headers: kidHeaders() })
    if (res.ok) wrongWords.value = await res.json()
  } catch (e) {
    /* 静默：错题池加载失败不影响浏览 */
  }
}

async function speak(word) {
  if (!word) return
  await playServerTts(word) // 统一读音入口：服务器 edge-tts（拼音/示例词）
}

// 依次朗读该规则的全部示例词（间隔 1.3s），让孩子连续听出共同发音
function speakRuleSounds(rule) {
  const words = (rule.example_words || []).map(w => w.en).filter(Boolean)
  if (!words.length) return
  speak(words[0])
  for (let i = 1; i < words.length; i++) {
    setTimeout(() => speak(words[i]), i * 1300)
  }
}

// 读组合本身的发音（如 "ee"）；TTS 不支持的组合（如 "a_e"）回退为读第一个示例词
async function speakPatternSound(rule) {
  if (!rule.pattern) return
  const fallback = (rule.example_words && rule.example_words[0] && rule.example_words[0].en) || ''
  const ok = await playServerTts(rule.pattern)
  if (!ok && fallback) speak(fallback)
}

watch(() => mode.value, () => {
  resetPractice()
})

onMounted(() => {
  fetchRules()
  fetchLexiconStats()
})
</script>

﻿<style scoped>
.phonics-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

/* ===== Hero 头部 + 主 Tab ===== */
.phonics-hero {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 16px;
  padding: 28px 32px;
  margin-bottom: 18px;
  border-radius: 16px;
  background: linear-gradient(135deg, #eef6ff 0%, #e8f1ff 50%, #f3ecff 100%);
  border: 1px solid #e3edff;
  box-shadow: 0 4px 20px rgba(64, 128, 255, 0.08);
}
.hero-left {
  flex: 1;
  min-width: 260px;
}
.hero-title {
  font-size: 26px;
  font-weight: 800;
  color: #1f4e8c;
  letter-spacing: 1px;
}
.hero-desc {
  margin-top: 8px;
  font-size: 14px;
  color: #5a6b85;
  line-height: 1.6;
}
/* 主 Tab：卡片式分段控件 */
.main-tabs {
  display: flex;
  gap: 10px;
  background: rgba(255, 255, 255, 0.85);
  padding: 6px;
  border-radius: 14px;
  border: 1px solid #e3edff;
  box-shadow: 0 2px 10px rgba(64, 128, 255, 0.10);
}
.main-tab {
  padding: 12px 24px;
  border-radius: 10px;
  font-size: 15px;
  font-weight: 700;
  color: #6b7a94;
  cursor: pointer;
  transition: all 0.2s;
  user-select: none;
}
.main-tab:hover {
  color: #2b6cb0;
}
.main-tab.active {
  background: linear-gradient(135deg, #409eff, #6a7ef5);
  color: #fff;
  box-shadow: 0 4px 12px rgba(64, 158, 255, 0.35);
}

/* ===== 词库学段 + 覆盖统计条 ===== */
.lexicon-bar {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 14px;
  padding: 12px 16px;
  background: #fff;
  border: 1px solid #ebeef5;
  border-radius: 12px;
  margin-bottom: 14px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}
.stage-tabs {
  display: flex;
  gap: 6px;
}
.stage-tab {
  padding: 7px 16px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 700;
  color: #6b7a94;
  background: #f2f4f8;
  cursor: pointer;
  transition: all 0.2s;
  user-select: none;
}
.stage-tab:hover {
  color: #2b6cb0;
  background: #e8f1ff;
}
.stage-tab.active {
  background: linear-gradient(135deg, #409eff, #6a7ef5);
  color: #fff;
  box-shadow: 0 3px 10px rgba(64, 158, 255, 0.3);
}
.lexicon-stats {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  flex: 1;
  min-width: 260px;
}
.stat-item {
  display: flex;
  align-items: baseline;
  gap: 6px;
}
.stat-num {
  font-size: 20px;
  font-weight: 800;
  color: #2d3748;
}
.stat-num.stat-primary {
  color: #409eff;
}
.stat-label {
  font-size: 12px;
  color: #8a93a5;
}
.stat-sep {
  color: #d0d5dd;
}
.stat-progress {
  width: 140px;
  margin-left: 4px;
}
.lexicon-empty {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #8a93a5;
  font-size: 13px;
}

/* ===== 规则卡片内的词库覆盖区 ===== */
.lexicon-zone {
  margin-top: 14px;
  border: 1px dashed #c9ddf8;
  border-radius: 10px;
  background: #f8fbff;
  cursor: pointer;
  overflow: hidden;
  transition: border-color 0.2s;
}
.lexicon-zone:hover {
  border-color: #8ab6f2;
}
.lexicon-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 9px 14px;
  font-size: 13px;
  color: #2b6cb0;
  font-weight: 700;
}
.lexicon-title {
  display: flex;
  align-items: center;
  gap: 6px;
}
.lexicon-toggle {
  font-size: 12px;
  color: #8a93a5;
  font-weight: 600;
}
.lexicon-words {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(110px, 1fr));
  gap: 6px;
  padding: 4px 12px 12px;
  border-top: 1px dashed #dbe7f7;
}
.lexicon-word {
  display: flex;
  align-items: center;
  gap: 4px;
  padding: 5px 8px;
  background: #fff;
  border: 1px solid #eef1f6;
  border-radius: 8px;
  font-size: 12px;
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s;
}
.lexicon-word:hover {
  background: #eef5ff;
  border-color: #c9ddf8;
}
.lw-en {
  font-weight: 700;
  color: #2d3748;
}
.lw-cn {
  color: #8a93a5;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
  min-width: 0;
}
.lw-grade {
  font-size: 10px;
  color: #b6bcc6;
  background: #f2f4f8;
  padding: 1px 6px;
  border-radius: 999px;
  flex-shrink: 0;
}
.lexicon-more {
  grid-column: 1 / -1;
  text-align: center;
  font-size: 12px;
  color: #a0a6b1;
  padding: 4px 0;
}

/* ===== 筛选工具条 + 类别 Tab ===== */
.phonics-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  padding: 12px 14px;
  background: #fff;
  border: 1px solid #ebeef5;
  border-radius: 12px;
  margin-bottom: 16px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}
.cat-tabs {
  display: flex;
  gap: 6px;
}
.cat-tab {
  padding: 8px 18px;
  border-radius: 999px;
  font-size: 13px;
  font-weight: 600;
  color: #6b7a94;
  background: #f2f4f8;
  cursor: pointer;
  transition: all 0.2s;
  user-select: none;
}
.cat-tab:hover {
  color: #2b6cb0;
  background: #e8f1ff;
}
.cat-tab.active {
  background: #2b6cb0;
  color: #fff;
  box-shadow: 0 3px 10px rgba(43, 108, 176, 0.3);
}

/* ===== 规则卡片 ===== */
.phonics-list {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}
.rule-card {
  border: 1px solid #e9edf3;
  border-radius: 14px;
  padding: 18px 20px;
  background: #fff;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
  transition: transform 0.2s, box-shadow 0.2s;
}
.rule-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.09);
}
.rule-head {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
}
.rule-pattern {
  font-size: 26px;
  font-weight: 800;
  color: #2b6cb0;
  font-family: 'Segoe UI', Consolas, monospace;
  background: linear-gradient(135deg, #eef4ff, #f6f0ff);
  padding: 4px 14px;
  border-radius: 10px;
  border: 1px solid #e0eaff;
}
.pattern-speak-btn {
  color: #67c23a;
}
.rule-sound {
  color: #d97706;
  font-size: 14px;
  font-weight: 600;
  background: #fff7ed;
  border: 1px solid #fde8c8;
  padding: 2px 10px;
  border-radius: 999px;
}
.rule-grade {
  font-size: 12px;
  color: #8a93a5;
  background: #f2f4f8;
  padding: 2px 10px;
  border-radius: 999px;
}
.rule-head-right {
  margin-left: auto;
}
.rule-text {
  margin-top: 10px;
  color: #4a5568;
  font-size: 14px;
  line-height: 1.7;
}
.rule-words {
  margin-top: 14px;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(120px, 1fr));
  gap: 10px;
}
.rule-word {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 12px;
  background: #f7f9fc;
  border: 1px solid #eef1f6;
  border-radius: 10px;
  cursor: pointer;
  transition: background 0.15s, border-color 0.15s;
}
.rule-word:hover {
  background: #eef5ff;
  border-color: #c9ddf8;
}
.speak-icon {
  color: #409eff;
  font-size: 16px;
  flex-shrink: 0;
}
.word-texts {
  display: flex;
  flex-direction: column;
  min-width: 0;
}
.word-en {
  font-weight: 700;
  color: #2d3748;
  font-size: 15px;
}
.word-cn {
  font-size: 12px;
  color: #8a93a5;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

/* ===== 底部提示 ===== */
.phonics-footer-tip {
  margin-top: 18px;
  text-align: center;
  color: #a0a6b1;
  font-size: 13px;
}

/* ===== 练习模式 ===== */
.practice-body {
  margin-top: 6px;
  min-height: 360px;
}
.practice-hero {
  text-align: center;
  margin-bottom: 26px;
}
.practice-hero-icon {
  font-size: 44px;
}
.practice-hero h3 {
  font-size: 22px;
  color: #303133;
  margin: 8px 0 6px;
  font-weight: 800;
}
.practice-hero-desc {
  font-size: 14px;
  color: #8a93a5;
}
.practice-type-cards {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin-bottom: 28px;
}
.practice-type-card {
  width: 230px;
  padding: 30px 20px;
  border: 2px solid #e8ebf1;
  border-radius: 18px;
  cursor: pointer;
  transition: all 0.2s;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}
.practice-type-card:hover {
  border-color: #b6d8ff;
  transform: translateY(-3px);
  box-shadow: 0 8px 20px rgba(64, 158, 255, 0.12);
}
.practice-type-card.active {
  border-color: #409eff;
  background: linear-gradient(135deg, #ecf5ff, #f5f0ff);
  box-shadow: 0 8px 20px rgba(64, 158, 255, 0.15);
}
.pt-icon {
  font-size: 40px;
}
.pt-name {
  font-weight: 700;
  color: #303133;
  margin-top: 10px;
  font-size: 17px;
}
.pt-desc {
  font-size: 13px;
  color: #8a93a5;
  margin-top: 6px;
  line-height: 1.5;
}
.practice-start-btns {
  display: flex;
  justify-content: center;
  gap: 14px;
  margin-top: 6px;
  flex-wrap: wrap;
}

/* ===== 错题集合卡片区（开始页） ===== */
.wrong-set-card {
  margin: 18px auto 6px;
  max-width: 720px;
  background: #fff;
  border: 1px solid #f0d9b8;
  border-radius: 14px;
  padding: 14px 18px 16px;
  box-shadow: 0 3px 12px rgba(230, 162, 60, 0.08);
  text-align: left;
}
.ws-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 4px;
}
.ws-title {
  font-size: 15px;
  font-weight: 800;
  color: #b88230;
}
.ws-count {
  font-size: 13px;
  color: #b88230;
  background: #fdf3e3;
  border-radius: 999px;
  padding: 2px 10px;
  margin-left: 6px;
}
.ws-desc {
  font-size: 12px;
  color: #a08a6a;
  margin-bottom: 12px;
}
.ws-sections {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 10px;
  margin-bottom: 12px;
}
.ws-section {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 12px;
  background: #fefbf5;
  border: 1px solid #f3e3c8;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}
.ws-section:hover {
  background: #fdf3e3;
  border-color: #e8c78e;
  transform: translateY(-1px);
}
.ws-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #e6a23c;
  flex-shrink: 0;
}
.ws-name {
  font-size: 13px;
  font-weight: 700;
  color: #5d4a2e;
  flex: 1;
}
.ws-num {
  font-size: 16px;
  color: #b88230;
}
.ws-go {
  font-size: 12px;
  color: #c9a35e;
}
.ws-actions {
  display: flex;
  gap: 10px;
}
.wrong-set-empty {
  margin: 16px auto 4px;
  max-width: 720px;
  padding: 14px 18px;
  border-radius: 12px;
  background: #f0f9eb;
  border: 1px solid #e1f3d8;
  color: #67a23a;
  font-size: 13px;
  text-align: left;
}

/* ===== 错题集合弹窗 ===== */
.wrong-dialog-empty {
  text-align: center;
  padding: 30px 0;
  color: #8a93a5;
  font-size: 14px;
}
.wrong-dialog-tip {
  font-size: 12px;
  color: #8a93a5;
  margin-bottom: 10px;
}
.wrong-dialog-list {
  max-height: 52vh;
  overflow-y: auto;
  border: 1px solid #ebeef5;
  border-radius: 10px;
}
.wrong-dialog-item {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  border-bottom: 1px solid #f2f4f8;
}
.wrong-dialog-item:last-child {
  border-bottom: none;
}
.wrong-dialog-item:hover {
  background: #f8fbff;
}
.wdi-left {
  display: flex;
  align-items: center;
  gap: 6px;
  min-width: 130px;
}
.wdi-word {
  font-size: 16px;
  font-weight: 800;
  color: #2d3748;
  cursor: pointer;
}
.wdi-word:hover {
  color: #409eff;
}
.wdi-speak {
  cursor: pointer;
  color: #409eff;
  font-size: 14px;
}
.wdi-cn {
  font-size: 13px;
  color: #8a93a5;
}
.wdi-mid {
  flex: 1;
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}
.wdi-count {
  font-size: 12px;
  color: #b88230;
  font-weight: 700;
}
.wdi-time {
  font-size: 12px;
  color: #b6bcc6;
}
.wdi-right {
  display: flex;
  align-items: center;
  gap: 2px;
}

/* ===== 答题卡 ===== */
.practice-quiz {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 12px 0;
}
.quiz-top {
  width: 100%;
  max-width: 720px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
  color: #8a93a5;
  margin-bottom: 14px;
}
.quiz-count {
  font-weight: 600;
  color: #606266;
}
.quiz-score {
  font-weight: 700;
  color: #2b6cb0;
  font-size: 14px;
}
.quiz-card {
  width: 100%;
  max-width: 720px;
  min-height: 220px;
  border-radius: 20px;
  border: 2px solid #e3ecf8;
  background: linear-gradient(160deg, #f4f9ff 0%, #f0f4ff 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 32px;
  transition: border-color 0.2s, background 0.2s;
  box-shadow: 0 6px 24px rgba(64, 128, 255, 0.10);
}
.quiz-card.right {
  border-color: #67c23a;
  background: #f0f9eb;
}
.quiz-card.wrong {
  border-color: #f56c6c;
  background: #fef0f0;
}
.quiz-label {
  font-size: 15px;
  color: #8a8fa3;
  letter-spacing: 1px;
}
.quiz-rule-hint {
  margin-top: 10px;
  font-size: 14px;
  color: #b8860b;
  background: #fdf6ec;
  padding: 3px 14px;
  border-radius: 999px;
}
.quiz-speak {
  margin-top: 22px;
  width: 80px;
  height: 80px;
  font-size: 34px;
  box-shadow: 0 8px 22px rgba(64, 158, 255, 0.30);
  background: #fff;
}
.quiz-speak-small {
  margin-top: 8px;
}
.quiz-word {
  font-size: 52px;
  font-weight: 800;
  color: #2b6cb0;
  margin-top: 12px;
  letter-spacing: 3px;
}
.quiz-cn {
  color: #8a93a5;
  font-size: 16px;
  margin-top: 6px;
}
.quiz-options {
  width: 100%;
  max-width: 720px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  margin-top: 22px;
}
.quiz-option {
  height: 56px;
  font-size: 19px;
  font-weight: 700;
  border-radius: 12px !important;
}
.quiz-feedback {
  margin-top: 20px;
  font-size: 16px;
}
.fb-right {
  color: #67c23a;
}
.fb-wrong {
  color: #f56c6c;
}

/* ===== 结果页 ===== */
.practice-result {
  display: flex;
  justify-content: center;
  padding: 10px 0;
}
.result-card {
  width: 100%;
  max-width: 560px;
  text-align: center;
  background: #fff;
  border: 1px solid #e9edf3;
  border-radius: 18px;
  padding: 34px 28px;
  box-shadow: 0 4px 18px rgba(0, 0, 0, 0.06);
}
.result-emoji {
  font-size: 56px;
}
.result-card h3 {
  font-size: 24px;
  color: #303133;
  margin: 10px 0 4px;
  font-weight: 800;
}
.result-score {
  font-size: 52px;
  font-weight: 800;
  color: #409eff;
  margin: 10px 0;
}
.result-total {
  font-size: 24px;
  color: #a0a6b1;
  font-weight: 600;
}
.result-cleared {
  margin: 12px auto 0;
  padding: 8px 16px;
  border-radius: 10px;
  background: #f0f9eb;
  border: 1px solid #e1f3d8;
  color: #529b2e;
  font-size: 13px;
  display: inline-block;
}
.result-wrongs {
  margin-top: 18px;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
}
.rw-title {
  font-size: 13px;
  color: #8a93a5;
  margin-bottom: 8px;
}
.rw-tip {
  font-size: 12px;
  color: #b6bcc6;
  margin-top: 8px;
}
.result-btns {
  margin-top: 24px;
  display: flex;
  justify-content: center;
  gap: 12px;
}

@media (max-width: 768px) {
  .phonics-list {
    grid-template-columns: 1fr;
  }
  .phonics-hero {
    padding: 20px;
  }
  .main-tab {
    padding: 10px 16px;
    font-size: 14px;
  }
}
</style>

