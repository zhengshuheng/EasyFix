<template>
  <el-dialog :model-value="modelValue" title="🧠 联想记忆" width="640px" top="8vh" @update:model-value="$emit('update:modelValue', $event)">
    <div v-if="loading" v-loading="true" class="mem-loading" />
    <template v-else>
      <el-empty v-if="allItems.length === 0" description="还没有带记忆增强的单词。新增 / 导入单词时会自动生成拼读规则与词根词源，稍后再来这里复习。" />

      <div v-else class="mem-body">
        <!-- 顶栏：归类选择 + 模式切换 -->
        <div class="mem-toolbar">
          <el-select v-model="activeGroup" size="default" style="width: 190px" @change="rebuildSession">
            <el-option label="📚 全部单词" value="__all__" />
            <el-option v-for="g in groups" :key="g.key" :label="g.label" :value="g.key" />
          </el-select>
          <el-radio-group v-model="mode" size="default" @change="onModeChange">
            <el-radio-button value="guess">口诀猜词</el-radio-button>
            <el-radio-button value="recall">看词想口诀</el-radio-button>
          </el-radio-group>
        </div>
        <div class="mem-group-tip">
          {{ activeGroup === '__all__' ? '全部单词' : groupLabelOf(activeGroup) }} · 本轮 {{ sessionItems.length }} 词
          <span v-if="activeGroup !== '__all__'" class="group-desc">{{ groupDescOf(activeGroup) }}</span>
        </div>

        <!-- 进度条 -->
        <div v-if="!sessionDone" class="mem-progress">
          <span>{{ idx + 1 }} / {{ sessionItems.length }}</span>
          <div class="progress-bar">
            <div class="progress-fill" :style="{ width: ((idx + 1) / sessionItems.length * 100) + '%' }" />
          </div>
          <span class="mem-score"><span class="sc-ok">✓{{ correctCount }}</span> <span class="sc-bad">✗{{ wrongCount }}</span></span>
        </div>

        <!-- 卡片 -->
        <template v-if="!sessionDone">
          <transition name="flip" mode="out-in">
            <div :key="current.word_id + (flipped ? 'f' : 'b')" class="mem-card" :class="{ flipped }" @click="flipped = !flipped">
              <div v-if="!flipped" class="card-front">
                <div class="card-label">{{ mode === 'guess' ? '看口诀猜单词' : '看单词，回想口诀' }}</div>
                <div v-if="mode === 'guess'" class="card-mnemonic">{{ current.mnemonic }}</div>
                <div v-else class="card-english-big">{{ current.english }}</div>
                <div v-if="current.word_root" class="card-root">词根：{{ current.word_root }}</div>
                <div v-if="mode === 'guess'" class="card-hint">{{ current.hint }}</div>
                <div class="card-tap">点击卡片看答案</div>
              </div>
              <div v-else class="card-back">
                <div v-if="mode === 'guess'" class="card-answer-row">
                  <span class="card-english">{{ current.english }}</span>
                  <el-button size="small" circle text @click.stop="speak(current.english)">
                    <el-icon><VolumeHigh /></el-icon>
                  </el-button>
                </div>
                <div v-else class="card-answer-row">
                  <span class="card-mnemonic-answer">{{ current.mnemonic }}</span>
                  <el-button size="small" circle text @click.stop="speak(current.english)">
                    <el-icon><VolumeHigh /></el-icon>
                  </el-button>
                </div>
                <div v-if="mode === 'guess' && current.phonetic" class="card-phonetic">{{ current.phonetic }}</div>
                <div class="card-chinese">{{ current.chinese }}</div>
                <div v-if="current.related_words && current.related_words.length" class="card-related">
                  相关词：
                  <el-tag v-for="(r, i) in current.related_words" :key="i" size="small" style="margin-right: 6px" @click="speak(r.en)">
                    {{ r.en }} {{ r.cn }}
                  </el-tag>
                </div>
                <div class="card-buttons">
                  <el-button size="large" type="danger" plain @click.stop="submit(false)">记错了 ✗</el-button>
                  <el-button size="large" type="success" @click.stop="submit(true)">答对了 ✓</el-button>
                </div>
              </div>
            </div>
          </transition>
        </template>

        <!-- 本轮完成 -->
        <div v-else class="mem-done">
          <div class="done-icon">🎉</div>
          <h3>本轮完成！</h3>
          <div class="done-stats">
            <div class="done-stat ok">答对 <b>{{ correctCount }}</b> 题</div>
            <div class="done-stat bad">答错 <b>{{ wrongCount }}</b> 题</div>
          </div>
          <div class="done-btns">
            <el-button v-if="wrongItems.length" type="primary" @click="retryWrongs">重练错题（{{ wrongItems.length }}）</el-button>
            <el-button @click="rebuildSession">再练一遍</el-button>
            <el-button @click="resetSession">换一组</el-button>
          </div>
        </div>
      </div>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { Headset } from '@element-plus/icons-vue'
import { playServerTts } from '@/utils/speech'
import { apiHeaders } from '@/api/http'

const props = defineProps({ modelValue: Boolean })
const emit = defineEmits(['update:modelValue', 'refresh'])

const loading = ref(false)
const allItems = ref([])          // 全部有口诀的词（含 word_root）
const groups = ref([])            // 词根分组
const activeGroup = ref('__all__')
const mode = ref('guess')         // guess=口诀猜词 recall=看词想口诀
const sessionItems = ref([])
const idx = ref(0)
const flipped = ref(false)
const correctCount = ref(0)
const wrongCount = ref(0)
const wrongItems = ref([])
const sessionDone = ref(false)

const current = computed(() => sessionItems.value[idx.value] || {})

function rootKeyOf(item) {
  return (item.word_root || '').trim()
}

function buildGroups() {
  const map = new Map()
  allItems.value.forEach(it => {
    const key = rootKeyOf(it)
    if (!key) return
    if (!map.has(key)) map.set(key, { key, label: `🧩 ${key}`, items: [] })
    map.get(key).items.push(it)
  })
  groups.value = [...map.values()].map(g => ({ ...g, label: `🧩 ${g.key}（${g.items.length}）` }))
}

function groupLabelOf(key) {
  const g = groups.value.find(x => x.key === key)
  return g ? g.key : key
}

function groupDescOf(key) {
  const g = groups.value.find(x => x.key === key)
  return g ? `同词根一起记，共 ${g.items.length} 词` : ''
}

function rebuildSession() {
  let items = allItems.value
  if (activeGroup.value !== '__all__') {
    items = allItems.value.filter(it => rootKeyOf(it) === activeGroup.value)
  }
  if (!items.length) {
    sessionItems.value = []
    return
  }
  sessionItems.value = [...items]
  resetSession()
}

function resetSession() {
  idx.value = 0
  flipped.value = false
  correctCount.value = 0
  wrongCount.value = 0
  wrongItems.value = []
  sessionDone.value = false
}

function onModeChange() {
  flipped.value = false
}

async function load() {
  loading.value = true
  try {
    const res = await fetch('/api/words/memory-review?limit=100', { headers: apiHeaders() })
    const data = await res.json()
    allItems.value = (data && data.items) || []
    buildGroups()
    rebuildSession()
  } catch (e) {
    ElMessage.error('加载复习列表失败')
  } finally {
    loading.value = false
  }
}

async function submit(correct) {
  const cur = sessionItems.value[idx.value]
  if (!cur) return
  try {
    await fetch('/api/words/memory-review/submit', {
      method: 'POST',
      headers: apiHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({ word_id: cur.word_id, correct }),
    })
  } catch (e) {
    /* 忽略提交失败 */
  }
  emit('refresh')
  if (correct) {
    correctCount.value += 1
  } else {
    wrongCount.value += 1
    wrongItems.value.push(cur)
  }
  if (idx.value + 1 >= sessionItems.value.length) {
    sessionDone.value = true
  } else {
    idx.value += 1
    flipped.value = false
  }
}

function retryWrongs() {
  if (!wrongItems.value.length) return
  sessionItems.value = [...wrongItems.value]
  wrongItems.value = []
  sessionDone.value = false
  idx.value = 0
  flipped.value = false
  correctCount.value = 0
  wrongCount.value = 0
}

function speak(word) {
  if (!word) return
  playServerTts(word)
}

watch(() => props.modelValue, (v) => {
  if (v) load()
})
</script>

<style scoped>
.mem-loading {
  min-height: 200px;
}
.mem-body {
  min-height: 320px;
  display: flex;
  flex-direction: column;
}
.mem-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
  flex-wrap: wrap;
}
.mem-group-tip {
  font-size: 12px;
  color: #8a7cd8;
  margin-bottom: 8px;
}
.group-desc {
  color: #bbb;
}
.mem-progress {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 14px;
  font-size: 13px;
  color: #888;
}
.progress-bar {
  flex: 1;
  height: 6px;
  background: #f0f2f5;
  border-radius: 3px;
  overflow: hidden;
}
.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #7c5cff, #409eff);
  transition: width 0.3s;
}
.mem-score {
  white-space: nowrap;
  font-size: 12px;
}
.sc-ok {
  color: #67c23a;
}
.sc-bad {
  color: #f56c6c;
  margin-left: 4px;
}
.mem-card {
  flex: 1;
  border-radius: 16px;
  padding: 34px 28px;
  text-align: center;
  cursor: pointer;
  user-select: none;
  background: linear-gradient(160deg, #f6f3ff 0%, #eef4ff 100%);
  border: 1px solid #dcd4ff;
  min-height: 250px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.card-label {
  font-size: 12px;
  color: #8a7cd8;
  letter-spacing: 2px;
  margin-bottom: 16px;
}
.card-mnemonic {
  font-size: 19px;
  line-height: 1.7;
  color: #4a3f78;
  font-weight: 500;
}
.card-english-big {
  font-size: 38px;
  font-weight: 800;
  color: #2b6cb0;
  letter-spacing: 2px;
}
.card-mnemonic-answer {
  font-size: 19px;
  line-height: 1.7;
  color: #4a3f78;
  font-weight: 500;
}
.card-root {
  margin-top: 10px;
  font-size: 13px;
  color: #8b6fd8;
}
.card-hint {
  margin-top: 16px;
  font-size: 24px;
  letter-spacing: 4px;
  color: #b3a6e8;
  font-family: 'Segoe UI', Consolas, monospace;
}
.card-tap {
  margin-top: 18px;
  font-size: 12px;
  color: #bbb;
}
.card-answer-row {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 6px;
}
.card-english {
  font-size: 34px;
  font-weight: 700;
  color: #2b6cb0;
}
.card-phonetic {
  margin-top: 4px;
  color: #d97706;
}
.card-chinese {
  margin-top: 12px;
  font-size: 18px;
  color: #333;
}
.card-related {
  margin-top: 14px;
  font-size: 12px;
  color: #888;
}
.card-buttons {
  margin-top: 24px;
  display: flex;
  justify-content: center;
  gap: 16px;
}
.flip-enter-active,
.flip-leave-active {
  transition: opacity 0.15s;
}
.flip-enter-from,
.flip-leave-to {
  opacity: 0;
}
.mem-done {
  text-align: center;
  padding: 26px 0;
}
.done-icon {
  font-size: 40px;
}
.mem-done h3 {
  font-size: 20px;
  color: #303133;
  margin: 10px 0 6px;
}
.done-stats {
  display: flex;
  justify-content: center;
  gap: 24px;
  margin: 12px 0 18px;
}
.done-stat {
  font-size: 14px;
  color: #666;
}
.done-stat b {
  font-size: 22px;
}
.done-stat.ok b {
  color: #67c23a;
}
.done-stat.bad b {
  color: #f56c6c;
}
.done-btns {
  display: flex;
  justify-content: center;
  gap: 10px;
}
</style>
