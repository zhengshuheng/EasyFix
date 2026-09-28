<template>
  <el-dialog :model-value="modelValue" title="🔤 自然拼读" width="860px" top="6vh" @update:model-value="$emit('update:modelValue', $event)">
    <!-- 主 Tab -->
    <div class="panel-main-tabs">
      <div class="main-tab" :class="{ active: mode === 'browse' }" @click="mode = 'browse'">📖 规则浏览</div>
      <div class="main-tab" :class="{ active: mode === 'practice' }" @click="mode = 'practice'">🎯 拼读练习</div>
    </div>
    <div v-if="mode === 'browse'" class="phonics-toolbar">
      <div class="cat-tabs">
        <div class="cat-tab" :class="{ active: category === 'vowel' }" @click="switchCategory('vowel')">元音组合</div>
        <div class="cat-tab" :class="{ active: category === 'consonant' }" @click="switchCategory('consonant')">辅音组合</div>
        <div class="cat-tab" :class="{ active: category === 'silent_e' }" @click="switchCategory('silent_e')">不发音 e</div>
      </div>
      <div class="toolbar-right">
        <el-input v-model="keyword" placeholder="搜字母组合" clearable style="width: 160px" @change="fetchRules" />
        <el-button type="primary" plain :loading="aiLoading" @click="aiGenerate">
          <el-icon><MagicStick /></el-icon>
          AI 生成该类规则
        </el-button>
      </div>
    </div>

    <!-- ============ 浏览模式 ============ -->
    <template v-if="mode === 'browse'">
      <el-alert
        v-if="rules.length === 0"
        type="info"
        :closable="false"
        title="该类别还没有规则，点击右上角「AI 生成该类规则」一键生成（示例词可直接点喇叭听发音）。"
        style="margin: 14px 0"
      />

      <div v-loading="loading" class="phonics-list">
        <div v-for="rule in rules" :key="rule.id" class="rule-card">
          <div class="rule-head">
            <span class="rule-pattern">{{ rule.pattern }}</span>
            <el-button v-if="rule.pattern" size="small" circle text class="pattern-speak-btn" title="读组合发音（如 ee）" @click="speakPatternSound(rule)">
              <el-icon><VolumeHigh /></el-icon>
            </el-button>
            <span v-if="rule.sound" class="rule-sound">{{ rule.sound }}</span>
            <span v-if="rule.grade" class="rule-grade">建议{{ gradeCn(rule.grade) }}</span>
            <el-button v-if="rule.example_words && rule.example_words.length" size="small" text title="依次朗读示例词，体会组合发音规律" @click="speakRuleSounds(rule)">
              <el-icon><Headset /></el-icon>
            </el-button>
          </div>
          <div class="rule-text">{{ rule.rule_text }}</div>
          <div v-if="rule.example_words && rule.example_words.length" class="rule-words">
            <div v-for="(w, i) in rule.example_words" :key="i" class="rule-word">
              <el-button size="small" circle text class="speak-btn" @click="speak(w.en)">
                <el-icon><VolumeHigh /></el-icon>
              </el-button>
              <span class="word-en">{{ w.en }}</span>
              <span class="word-cn">{{ w.cn }}</span>
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
          <h3>选一种练习方式</h3>
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
          <div class="practice-start-btns">
            <el-button type="primary" size="large" :disabled="canPractice === false" @click="startPractice(false)">
              开始练习（10 题）
            </el-button>
            <el-button
              v-if="wrongPoolCount > 0"
              size="large"
              type="warning"
              plain
              :disabled="canPractice === false"
              @click="startPractice(true)"
            >
              🔁 只练错题（{{ wrongPoolCount }} 条）
            </el-button>
          </div>
          <div v-if="wrongPoolCount > 0" class="wrong-pool-tip">
            💡 有 {{ wrongPoolCount }} 条拼读错题待复习，练习会优先从错题出题，答对后自动移出错题池
          </div>
          <el-alert
            v-if="canPractice === false"
            type="warning"
            :closable="false"
            title="当前类别还没有规则/示例词，请先在「规则浏览」中用 AI 生成规则，或切换类别。"
            style="margin-top: 12px"
          />
        </div>

        <!-- 答题中 -->
        <div v-else-if="!practiceDone && currentQ" class="practice-quiz">
          <div class="quiz-top">
            <span class="quiz-count">{{ qIdx + 1 }} / {{ questions.length }}</span>
            <span class="quiz-score">得分：{{ score }} / {{ questions.length }}</span>
            <el-button size="small" text type="info" @click="quitPractice">⏹ 结束练习</el-button>
          </div>
          <div class="quiz-card" :class="answered ? (picked === currentQ.answer ? 'right' : 'wrong') : ''">
            <template v-if="currentQ.type === 'listen'">
              <div class="quiz-label">听发音，选出正确的单词</div>
              <div class="quiz-rule-hint">字母组合 {{ currentQ.ruleText }}</div>
              <el-button circle size="large" class="quiz-speak" @click="speak(currentQ.word)">
                <el-icon :size="26"><VolumeHigh /></el-icon>
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
          <h3>{{ score >= questions.length * 0.8 ? '🎉 太棒了！' : score >= questions.length * 0.5 ? '👍 继续加油！' : '💪 再来一次！' }}</h3>
          <div class="result-score">{{ score }} / {{ questions.length }}</div>
          <el-progress :percentage="Math.round(score / questions.length * 100)" :color="score >= questions.length * 0.6 ? '#67c23a' : '#e6a23c'" style="width: 240px; margin: 12px auto" />
          <div v-if="clearedCount > 0" class="result-cleared">
            ✅ 本轮复习掌握 {{ clearedCount }} 条历史错题，已移出错题池
          </div>
          <div v-if="wrongs.length" class="result-wrongs">
            <div class="rw-title">答错的题（已记入错题集，下次优先练）：</div>
            <el-tag v-for="(w, i) in wrongs" :key="i" closable style="margin: 4px 6px" @close="wrongs.splice(i, 1)">
              {{ w.word }} → {{ w.answer }}
            </el-tag>
            <div class="rw-tip">点「重练错题」只练答错的题</div>
          </div>
          <div class="result-btns">
            <el-button @click="retryWrongs" :disabled="wrongs.length === 0">重练错题</el-button>
            <el-button type="primary" @click="startPractice(false)">再来一轮</el-button>
            <el-button @click="practiceStarted = false">换题型</el-button>
          </div>
        </div>
      </div>
    </template>

    <template #footer>
      <span class="footer-tip">{{ mode === 'browse' ? '示例词发音：点击喇叭即可；未缓存时首次稍慢' : '练习结束后可重练错题' }}</span>
      <el-button @click="$emit('update:modelValue', false)">关闭</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { MagicStick, Headset } from '@element-plus/icons-vue'
import { playServerTts } from '@/utils/speech'

const props = defineProps({ modelValue: Boolean })
const emit = defineEmits(['update:modelValue', 'refresh'])

const category = ref('vowel')
const keyword = ref('')
const rules = ref([])
const loading = ref(false)
const aiLoading = ref(false)

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

const wrongPoolCount = computed(() => {
  // 当前类别下的待复习错题数
  if (!wrongWords.value.length) return 0
  const ruleIds = new Set(rules.value.filter(r => (r.example_words || []).length > 0).map(r => r.id))
  return wrongWords.value.filter(w => ruleIds.has(w.rule_id) || w.category === category.value).length
})

const clearedCount = computed(() => clearedWords.value.length)

const canPractice = computed(() => {
  // 需要至少 2 条规则且有多余示例词才能出题
  return rules.value.some(r => (r.example_words || []).length > 0)
})

function shuffle(arr) {
  return [...arr].sort(() => Math.random() - 0.5)
}

function buildQuestions(type, count = 10, onlyWrong = false) {
  const allRules = rules.value.filter(r => (r.example_words || []).length > 0)
  if (!allRules.length) return []
  // 收集所有词（关联规则）
  const allWords = []
  allRules.forEach(r => (r.example_words || []).forEach(w => allWords.push({ en: w.en, cn: w.cn, rule: r })))
  if (allWords.length < 2) return []
  // 错题池词：历史错题（按词或规则匹配）优先出题，且顺序排在最前
  const wrongEn = new Set(wrongWords.value.map(w => w.word))
  const wrongRuleIds = new Set(wrongWords.value.map(w => w.rule_id))
  const wrongPool = allWords.filter(w => wrongEn.has(w.en) || wrongRuleIds.has(w.rule.id))
  const freshPool = shuffle(allWords.filter(w => !wrongEn.has(w.en)))
  // 顺序 = 错题词（固定复习） → 新词（随机补充）
  let pool
  if (onlyWrong) {
    pool = wrongPool.length >= 2 ? [...wrongPool] : [...wrongPool, ...freshPool]
  } else {
    pool = [...wrongPool, ...freshPool]
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
  ElMessage.info('已结束练习')
}

function startPractice(onlyWrong = false) {
  const qs = buildQuestions(practiceType.value, 10, onlyWrong)
  if (!qs.length) {
    ElMessage.warning('该类别示例词不足，无法出题，请先用 AI 生成规则')
    return
  }
  resetPractice()
  onlyWrongs.value = !!onlyWrong
  questions.value = qs
  practiceStarted.value = true
  autoplayCurrent()
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
    // 答对的是历史错题 → 计入掌握，结束后移出错题池
    if (!onlyWrongs.value && wrongWords.value.some(w => w.word === q.word)) {
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
  rules.value.forEach(r => (r.example_words || []).forEach(w => s.add(w.en)))
  return [...s]
}

const gradeCn = (g) => ['一', '二', '三', '四', '五', '六'][g - 1] + '年级'

function switchCategory(val) {
  if (category.value === val) return
  category.value = val
  fetchRules()
}

async function fetchRules() {
  loading.value = true
  try {
    let url = '/api/phonics?category=' + category.value
    if (keyword.value) url += '&keyword=' + encodeURIComponent(keyword.value)
    const res = await fetch(url)
    rules.value = await res.json()
  } catch (e) {
    ElMessage.error('加载规则失败')
  } finally {
    loading.value = false
  }
  loadWrongWords()
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

async function aiGenerate() {
  const catCn = { vowel: '元音组合', consonant: '辅音组合', silent_e: '不发音 e' }[category.value]
  aiLoading.value = true
  try {
    const res = await fetch('/api/phonics/ai-import', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ category: category.value }),
    })
    const data = await res.json()
    if (!res.ok) throw new Error(data.detail || '生成失败')
    ElMessage.success(`已生成并导入 ${data.created} 条${catCn}规则（跳过已存在的）`)
    fetchRules()
  } catch (e) {
    ElMessage.error('AI 生成失败：' + e.message)
  } finally {
    aiLoading.value = false
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

watch(() => props.modelValue, (v) => {
  resetPractice()
  if (v) fetchRules()
})

onMounted(() => {
  if (props.modelValue) fetchRules()
})
</script>

<style scoped>
/* ===== 主 Tab ===== */
.panel-main-tabs {
  display: flex;
  gap: 8px;
  background: #f0f4fa;
  padding: 5px;
  border-radius: 12px;
  margin-bottom: 12px;
}
.main-tab {
  flex: 1;
  text-align: center;
  padding: 10px 16px;
  border-radius: 9px;
  font-size: 14px;
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
  box-shadow: 0 3px 10px rgba(64, 158, 255, 0.3);
}
/* ===== 类别 Tab ===== */
.cat-tabs {
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}
.cat-tab {
  padding: 7px 16px;
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

﻿.phonics-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 12px;
  padding: 14px 18px;
  background: linear-gradient(135deg, #f7faff, #f5f2ff);
  border: 1px solid #e8eefb;
  border-radius: 12px;
  margin-bottom: 14px;
}
.toolbar-right {
  display: flex;
  gap: 8px;
  align-items: center;
}
.phonics-list {
  max-height: 58vh;
  overflow-y: auto;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}
.rule-card {
  border: 1px solid #e9edf3;
  border-radius: 14px;
  padding: 16px 18px;
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
  font-size: 24px;
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
.rule-text {
  margin-top: 10px;
  color: #4a5568;
  font-size: 13px;
  line-height: 1.7;
}
.rule-words {
  margin-top: 12px;
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
.rule-word {
  display: flex;
  align-items: center;
  gap: 5px;
  padding: 6px 10px;
  background: #f7f9fc;
  border: 1px solid #eef1f6;
  border-radius: 10px;
}
.speak-btn {
  color: #409eff;
}
.word-en {
  font-weight: 700;
  color: #2d3748;
  font-size: 14px;
}
.word-cn {
  font-size: 12px;
  color: #8a93a5;
}
.footer-tip {
  float: left;
  color: #8a93a5;
  font-size: 12px;
}

/* ===== 练习模式 ===== */
.practice-body {
  margin-top: 6px;
  min-height: 320px;
}
.practice-start {
  text-align: center;
  padding: 20px 0 8px;
}
.practice-start h3 {
  font-size: 20px;
  color: #303133;
  margin-bottom: 20px;
  font-weight: 700;
}
.practice-type-cards {
  display: flex;
  justify-content: center;
  gap: 18px;
  margin-bottom: 24px;
}
.practice-type-card {
  width: 190px;
  padding: 22px 14px;
  border: 2px solid #e8ebf1;
  border-radius: 16px;
  cursor: pointer;
  transition: all 0.2s;
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.04);
}
.practice-type-card:hover {
  border-color: #b6d8ff;
  transform: translateY(-3px);
  box-shadow: 0 6px 18px rgba(64, 158, 255, 0.12);
}
.practice-type-card.active {
  border-color: #409eff;
  background: linear-gradient(135deg, #ecf5ff, #f5f0ff);
  box-shadow: 0 6px 18px rgba(64, 158, 255, 0.15);
}
.pt-icon {
  font-size: 34px;
}
.pt-name {
  font-weight: 700;
  color: #303133;
  margin-top: 8px;
  font-size: 15px;
}
.pt-desc {
  font-size: 12px;
  color: #8a93a5;
  margin-top: 5px;
  line-height: 1.5;
}
.practice-start-btns {
  display: flex;
  justify-content: center;
  gap: 12px;
  margin-top: 6px;
  flex-wrap: wrap;
}
.wrong-pool-tip {
  margin-top: 14px;
  padding: 9px 15px;
  border-radius: 10px;
  background: #fdf6ec;
  border: 1px solid #faecd8;
  color: #b88230;
  font-size: 13px;
  text-align: left;
  display: inline-block;
  max-width: 620px;
}
.result-cleared {
  margin: 12px auto 0;
  padding: 8px 15px;
  border-radius: 10px;
  background: #f0f9eb;
  border: 1px solid #e1f3d8;
  color: #529b2e;
  font-size: 13px;
  display: inline-block;
}

/* ===== 答题卡 ===== */
.practice-quiz {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 10px 0;
}
.quiz-top {
  width: 100%;
  max-width: 620px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
  color: #8a93a5;
  margin-bottom: 12px;
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
  max-width: 620px;
  min-height: 190px;
  border-radius: 18px;
  border: 2px solid #e3ecf8;
  background: linear-gradient(160deg, #f4f9ff 0%, #f0f4ff 100%);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 26px;
  transition: border-color 0.2s, background 0.2s;
  box-shadow: 0 4px 16px rgba(64, 128, 255, 0.08);
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
  font-size: 14px;
  color: #8a8fa3;
  letter-spacing: 1px;
}
.quiz-rule-hint {
  margin-top: 8px;
  font-size: 14px;
  color: #b8860b;
  background: #fdf6ec;
  padding: 2px 12px;
  border-radius: 999px;
}
.quiz-speak {
  margin-top: 18px;
  width: 70px;
  height: 70px;
  font-size: 28px;
  box-shadow: 0 6px 18px rgba(64, 158, 255, 0.25);
  background: #fff;
}
.quiz-speak-small {
  margin-top: 8px;
}
.quiz-word {
  font-size: 46px;
  font-weight: 800;
  color: #2b6cb0;
  margin-top: 10px;
  letter-spacing: 3px;
}
.quiz-cn {
  color: #8a93a5;
  font-size: 15px;
  margin-top: 6px;
}
.quiz-options {
  width: 100%;
  max-width: 620px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  margin-top: 18px;
}
.quiz-option {
  height: 50px;
  font-size: 17px;
  font-weight: 700;
  border-radius: 12px !important;
}
.quiz-feedback {
  margin-top: 16px;
  font-size: 15px;
}
.fb-right {
  color: #67c23a;
}
.fb-wrong {
  color: #f56c6c;
}

/* ===== 结果页 ===== */
.practice-result {
  text-align: center;
  padding: 24px 0;
}
.practice-result h3 {
  font-size: 24px;
  color: #303133;
  margin-bottom: 8px;
}
.result-score {
  font-size: 42px;
  font-weight: 800;
  color: #409eff;
  margin: 12px 0;
}
.result-wrongs {
  margin-top: 16px;
  max-width: 540px;
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
  margin-top: 22px;
  display: flex;
  justify-content: center;
  gap: 12px;
}

</style>
