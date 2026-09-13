<template>
  <div class="home">
    <!-- Hero -->
    <header class="hero">
      <div class="hero-left">
        <p class="hero-eyebrow">WELCOME BACK</p>
        <h1 class="hero-title">学习概览</h1>
        <p class="hero-sub">保持节奏，每天进步一点点</p>
      </div>
      <div class="hero-right">
        <div class="date-chip">
          <svg class="chip-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
            <rect x="3" y="4" width="18" height="18" rx="2" />
            <line x1="16" y1="2" x2="16" y2="6" />
            <line x1="8" y1="2" x2="8" y2="6" />
            <line x1="3" y1="10" x2="21" y2="10" />
          </svg>
          <span class="chip-text">{{ todayText }}</span>
        </div>
      </div>
    </header>

    <!-- Stats Grid -->
    <section class="stats-grid">
      <div class="stat-card tone-indigo stat-lg" @click="$router.push('/questions')">
        <div class="stat-top">
          <span class="stat-label">错题总数</span>
          <div class="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z" />
              <polyline points="14 2 14 8 20 8" />
              <line x1="16" y1="13" x2="8" y2="13" />
              <line x1="16" y1="17" x2="8" y2="17" />
              <line x1="10" y1="9" x2="8" y2="9" />
            </svg>
          </div>
        </div>
        <div class="stat-value">{{ stats.total_questions }}</div>
        <div class="stat-foot">点击查看详情 <span class="arrow">→</span></div>
      </div>

      <div class="stat-card tone-violet" @click="$router.push('/questions')">
        <div class="stat-top">
          <span class="stat-label">学科数量</span>
          <div class="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
            </svg>
          </div>
        </div>
        <div class="stat-value">{{ stats.total_subjects }}</div>
      </div>

      <div class="stat-card tone-sky" @click="$router.push('/management')">
        <div class="stat-top">
          <span class="stat-label">活跃天数</span>
          <div class="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <rect x="3" y="4" width="18" height="18" rx="2" />
              <line x1="16" y1="2" x2="16" y2="6" />
              <line x1="8" y1="2" x2="8" y2="6" />
              <line x1="3" y1="10" x2="21" y2="10" />
            </svg>
          </div>
        </div>
        <div class="stat-value">{{ stats.active_days || 0 }}</div>
      </div>

      <div class="stat-card tone-emerald" @click="$router.push('/words')">
        <div class="stat-top">
          <span class="stat-label">待复习(单词)</span>
          <div class="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10" />
              <polyline points="12 6 12 12 16 14" />
            </svg>
          </div>
        </div>
        <div class="stat-value">{{ stats.word_stats?.to_review_count || 0 }}</div>
      </div>

      <div class="stat-card tone-amber" @click="$router.push('/words')">
        <div class="stat-top">
          <span class="stat-label">待复习(错题)</span>
          <div class="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10" />
              <polyline points="12 6 12 12 16 14" />
            </svg>
          </div>
        </div>
        <div class="stat-value">{{ stats.to_review_questions || 0 }}</div>
      </div>

      <div class="stat-card tone-rose" @click="$router.push('/words')">
        <div class="stat-top">
          <span class="stat-label">复习次数</span>
          <div class="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="23 4 23 10 17 10" />
              <polyline points="1 20 1 14 7 14" />
              <path d="M3.51 9a9 9 0 0 1 14.85-3.36L23 10M1 14l4.64 4.36A9 9 0 0 0 20.49 15" />
            </svg>
          </div>
        </div>
        <div class="stat-value">{{ stats.word_stats?.total_reviews || 0 }}</div>
      </div>

      <div class="stat-card tone-fuchsia" @click="$router.push('/words')">
        <div class="stat-top">
          <span class="stat-label">单词总数</span>
          <div class="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20" />
              <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z" />
            </svg>
          </div>
        </div>
        <div class="stat-value">{{ stats.word_stats?.total_words || 0 }}</div>
      </div>

      <div class="stat-card tone-cyan" @click="$router.push('/words')">
        <div class="stat-top">
          <span class="stat-label">已复习单词</span>
          <div class="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <polyline points="20 6 9 17 4 12" />
            </svg>
          </div>
        </div>
        <div class="stat-value">{{ stats.word_stats?.reviewed_words || 0 }}</div>
      </div>

      <div class="stat-card tone-lime" @click="$router.push('/words')">
        <div class="stat-top">
          <span class="stat-label">单词正确率</span>
          <div class="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <circle cx="12" cy="12" r="10" />
              <circle cx="12" cy="12" r="6" />
              <circle cx="12" cy="12" r="2" />
            </svg>
          </div>
        </div>
        <div class="stat-value">{{ stats.word_stats?.accuracy || 0 }}%</div>
      </div>
    </section>

    <!-- Global Grade Switcher -->
    <section class="grade-switch-bar">
      <div class="grade-switch-label">年级</div>
      <div class="grade-switch-chips">
        <button
          v-for="g in gradeOptions"
          :key="g.value"
          class="grade-switch-chip"
          :class="{ active: selectedGrade === g.value }"
          @click="onGradeChange(g.value)"
        >
          {{ g.label }}
        </button>
      </div>
      <div class="grade-switch-note">不区分上下学期 · 切换后整页数据联动</div>
    </section>

    <!-- Content Grid -->
    <section class="content-grid">
      <!-- Learning Overview -->
      <article class="panel">
        <div class="panel-head">
          <h2 class="panel-title">学习概览</h2>
        </div>
        <div class="overview-grid">
          <div class="overview-col">
            <div class="overview-col-title">
              <span class="title-dot dot-slate"></span>昨日
            </div>
            <div class="overview-list">
              <div class="overview-item">
                <span class="ov-dot dot-emerald"></span>
                <span>{{ learningOverview.yesterday_word_review_count }} 复习单词</span>
              </div>
              <div class="overview-item">
                <span class="ov-dot dot-blue"></span>
                <span>{{ learningOverview.yesterday_question_review_count }} 复习错题</span>
              </div>
              <div class="overview-item">
                <span class="ov-dot dot-emerald-light"></span>
                <span>{{ learningOverview.yesterday_word_accuracy }}% 单词正确率</span>
              </div>
              <div class="overview-item">
                <span class="ov-dot dot-blue-light"></span>
                <span>{{ learningOverview.yesterday_question_accuracy }}% 错题正确率</span>
              </div>
            </div>
          </div>
          <div class="overview-col">
            <div class="overview-col-title">
              <span class="title-dot dot-indigo"></span>今日
            </div>
            <div class="overview-list">
              <div class="overview-item">
                <span class="ov-dot dot-emerald"></span>
                <span>{{ learningOverview.today_word_review_count }} 复习单词</span>
              </div>
              <div class="overview-item">
                <span class="ov-dot dot-blue"></span>
                <span>{{ learningOverview.today_question_review_count }} 复习错题</span>
              </div>
              <div class="overview-item">
                <span class="ov-dot dot-emerald-light"></span>
                <span>{{ learningOverview.today_word_accuracy }}% 单词正确率</span>
              </div>
              <div class="overview-item">
                <span class="ov-dot dot-blue-light"></span>
                <span>{{ learningOverview.today_question_accuracy }}% 错题正确率</span>
              </div>
            </div>
          </div>
        </div>
      </article>

      <!-- Error Type Distribution -->
      <article class="panel">
        <div class="panel-head">
          <h2 class="panel-title">错误类型分布</h2>
          <el-select v-model="selectedSubject" placeholder="选择学科" size="small" class="subject-select">
            <el-option
              v-for="subject in stats.by_subject"
              :key="subject.subject_id"
              :label="subject.subject_name"
              :value="subject.subject_id"
            />
          </el-select>
        </div>
        <div v-if="hasFilteredErrorTypeData" class="chart-container">
          <v-chart :option="errorTypePieOption" autoresize style="height: 240px" />
        </div>
        <el-empty v-else description="暂无数据" :image-size="80" />
      </article>

      <!-- Accuracy Curve -->
      <article class="panel panel-full">
        <div class="panel-head">
          <h2 class="panel-title">准确率曲线</h2>
          <el-radio-group v-model="curveRange" size="small" class="curve-tabs">
            <el-radio-button label="week">最近一周</el-radio-button>
            <el-radio-button label="month">最近一月</el-radio-button>
            <el-radio-button label="3months">最近3月</el-radio-button>
            <el-radio-button label="halfyear">最近半年</el-radio-button>
            <el-radio-button label="all">全部</el-radio-button>
          </el-radio-group>
        </div>
        <div v-if="hasAccuracyCurve" class="chart-container">
          <v-chart :option="dualAccuracyCurveOption" autoresize style="height: 300px" />
        </div>
        <el-empty v-else description="暂无准确率数据" :image-size="80" />
      </article>

      <!-- Subject Table -->
      <article class="panel panel-full">
        <div class="panel-head">
          <h2 class="panel-title">学科详细数据</h2>
          <el-button type="primary" size="small" round @click="$router.push('/questions')">查看全部</el-button>
        </div>
        <el-table :data="subjectTableData" stripe class="subject-table">
          <el-table-column type="index" label="#" width="60" align="center" />
          <el-table-column prop="subject_name" label="学科" width="80">
            <template #default="{ row }">
              <el-tag type="primary" plain round>{{ row.subject_name }}</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="错题数" width="70" align="center">
            <template #default="{ row }">
              <span class="question-count">{{ row.question_count }}</span>
            </template>
          </el-table-column>
          <el-table-column label="难度分布" min-width="240">
            <template #default="{ row }">
              <div class="difficulty-bars">
                <div v-for="i in 5" :key="i" class="diff-bar-item">
                  <span class="diff-label">难度{{ i }}</span>
                  <el-progress
                    :percentage="getPercentage(row.difficulty_distribution?.[i] || 0, row.question_count)"
                    :stroke-width="10"
                    :color="getDifficultyColor(i)"
                    :show-text="false"
                    style="flex:1"
                  />
                  <span class="diff-count">{{ row.difficulty_distribution?.[i] || 0 }}</span>
                </div>
              </div>
            </template>
          </el-table-column>
          <el-table-column label="主要错误类型" min-width="180">
            <template #default="{ row }">
              <div class="error-tags">
                <el-tag
                  v-for="(count, type) in getTopErrorTypes(row.error_type_counts)"
                  :key="type"
                  :type="getErrorTagType(type)"
                  size="small"
                  round
                  style="margin-right: 4px"
                >
                  {{ type }} {{ count }}
                </el-tag>
              </div>
            </template>
          </el-table-column>
          <el-table-column prop="practice_count" label="练习次数" width="120" align="center">
            <template #default="{ row }">
              <span class="practice-count">{{ row.practice_count || 0 }}</span>
            </template>
          </el-table-column>
        </el-table>
      </article>
    </section>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { statsApi, statsOverviewApi } from '@/api/question'
import { useAppConfigStore } from '@/stores/appConfig'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart, BarChart, LineChart, RadarChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, LegendComponent, GridComponent, GraphicComponent } from 'echarts/components'
import 'echarts-gl'

use([CanvasRenderer, PieChart, BarChart, LineChart, RadarChart, TitleComponent, TooltipComponent, LegendComponent, GridComponent, GraphicComponent])

const router = useRouter()
const appConfigStore = useAppConfigStore()

const stats = ref({
  total_questions: 0,
  total_subjects: 0,
  total_error_books: 0,
  active_days: 0,
  difficulty_distribution: {},
  error_type_distribution: {},
  by_subject: [],
  word_stats: {
    total_words: 0,
    reviewed_words: 0,
    total_reviews: 0,
    accuracy: 0
  },
  word_accuracy_curve: [],
  question_accuracy_curve: []
})

const selectedSubject = ref('')

const gradeLabelMap = {
  1: '一年级', 2: '二年级', 3: '三年级', 4: '四年级',
  5: '五年级', 6: '六年级', 7: '初一', 8: '初二', 9: '初三',
  10: '高一', 11: '高二', 12: '高三',
}

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

const getGradeLabel = (g) => gradeLabelMap[g] || `${g}年级`

// 全局年级：默认六年级（与管理配置一致），切换后整页联动
const selectedGrade = ref(null)

const onGradeChange = (g) => {
  if (selectedGrade.value === g) return
  selectedGrade.value = g
  loadAllStats()
}

const loadAllStats = async () => {
  const params = {}
  if (selectedGrade.value) params.grade = selectedGrade.value
  try {
    const { data } = await statsApi.getSummary(params)
    stats.value = data
    // 学科筛选在年级变化后可能失效，重置
    if (selectedSubject.value && !data.by_subject?.some(s => s.subject_id === selectedSubject.value)) {
      selectedSubject.value = ''
    }
  } catch (error) {
    console.error('获取统计失败:', error)
  }
  try {
    const overviewRes = await statsOverviewApi.getOverview(params)
    learningOverview.value = overviewRes.data
  } catch (error) {
    console.error('获取学习概览失败:', error)
  }
}

const learningOverview = ref({
  yesterday_word_review_count: 0,
  yesterday_question_review_count: 0,
  yesterday_word_accuracy: 0,
  yesterday_question_accuracy: 0,
  today_word_review_count: 0,
  today_question_review_count: 0,
  today_word_accuracy: 0,
  today_question_accuracy: 0,
})

const curveRange = ref('month')

const todayText = computed(() => {
  const now = new Date()
  const weekdays = ['周日', '周一', '周二', '周三', '周四', '周五', '周六']
  return `${now.getFullYear()}年${now.getMonth() + 1}月${now.getDate()}日 ${weekdays[now.getDay()]}`
})

const getPercentage = (count, total) => {
  if (!total) return 0
  return Math.round((count / total) * 100)
}

const getDifficultyColor = (level) => {
  const colors = ['', '#67c23a', '#85ce61', '#e6a23c', '#f56c6c', '#f56c6c']
  return colors[level] || '#909399'
}

const adjustColor = (hex, amount) => {
  const num = parseInt(hex.replace('#', ''), 16)
  const r = Math.min(255, Math.max(0, (num >> 16) + amount))
  const g = Math.min(255, Math.max(0, ((num >> 8) & 0x00FF) + amount))
  const b = Math.min(255, Math.max(0, (num & 0x0000FF) + amount))
  return '#' + ((r << 16) | (g << 8) | b).toString(16).padStart(6, '0')
}

const getErrorTagType = (type) => {
  const types = { '计算': 'danger', '概念': 'warning', '审题': 'info', '粗心': 'success', '其他': '' }
  return types[type] || ''
}

const getTopErrorTypes = (errorTypeCounts) => {
  if (!errorTypeCounts) return {}
  return Object.fromEntries(Object.entries(errorTypeCounts).sort((a, b) => b[1] - a[1]).slice(0, 3))
}

const hasAccuracyCurve = computed(() => {
  return stats.value.word_accuracy_curve && stats.value.word_accuracy_curve.length > 0
})

const filteredErrorTypeData = computed(() => {
  const bySubject = stats.value.by_subject || []
  if (!selectedSubject.value && bySubject.length > 0) {
    const mathSubject = bySubject.find(s => s.subject_name.includes('数学'))
    selectedSubject.value = mathSubject ? mathSubject.subject_id : bySubject[0].subject_id
  }
  const subject = bySubject.find(s => s.subject_id === selectedSubject.value)
  return subject?.error_type_counts || {}
})

const hasFilteredErrorTypeData = computed(() => {
  return Object.keys(filteredErrorTypeData.value).length > 0
})

const errorTypePieOption = computed(() => {
  const data = filteredErrorTypeData.value
  if (!Object.keys(data).length) return {}
  const colors = ['#4f46e5', '#22c55e', '#f59e0b', '#ef4444', '#06b6d4', '#84cc16', '#f97316', '#8b5cf6', '#ec4899']
  const entries = Object.entries(data).sort((a, b) => b[1] - a[1])
  const total = entries.reduce((sum, [, v]) => sum + v, 0)
  return {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} ({d}%)',
      backgroundColor: '#ffffff',
      borderColor: '#e2e8f0',
      borderWidth: 1,
      textStyle: { color: '#334155' }
    },
    legend: {
      orient: 'vertical',
      right: 8,
      top: 'center',
      itemWidth: 12,
      itemHeight: 12,
      itemGap: 14,
      textStyle: { color: '#64748b', fontSize: 13, lineHeight: 22 },
      formatter: (name) => {
        const item = entries.find(([n]) => n === name)
        if (!item) return name
        const pct = ((item[1] / total) * 100).toFixed(1)
        return `${name}  ${item[1]}  ${pct}%`
      }
    },
    series: [{
      type: 'pie',
      radius: ['32%', '68%'],
      center: ['34%', '50%'],
      avoidLabelOverlap: true,
      itemStyle: {
        borderRadius: 8,
        borderColor: '#ffffff',
        borderWidth: 3,
      },
      label: { show: false },
      emphasis: {
        scaleSize: 8,
        itemStyle: { shadowBlur: 16, shadowColor: 'rgba(79, 70, 229, 0.35)' }
      },
      labelLine: { show: false },
      data: entries.map(([name, value], i) => ({
        name,
        value,
        itemStyle: {
          color: {
            type: 'linear',
            x: 0, y: 0, x2: 1, y2: 1,
            colorStops: [
              { offset: 0, color: colors[i % colors.length] },
              { offset: 1, color: adjustColor(colors[i % colors.length], -24) }
            ]
          }
        }
      }))
    }]
  }
})

const subjectTableData = computed(() => stats.value.by_subject || [])

const filteredCurveData = computed(() => {
  const curve = stats.value.word_accuracy_curve || []
  if (!curve.length) return []

  const now = new Date()
  const range = curveRange.value
  let startDate = null

  if (range === 'week') {
    startDate = new Date(now.getTime() - 7 * 24 * 60 * 60 * 1000)
  } else if (range === 'month') {
    startDate = new Date(now.getTime() - 30 * 24 * 60 * 60 * 1000)
  } else if (range === '3months') {
    startDate = new Date(now.getTime() - 90 * 24 * 60 * 60 * 1000)
  } else if (range === 'halfyear') {
    startDate = new Date(now.getTime() - 180 * 24 * 60 * 60 * 1000)
  } else {
    return curve
  }

  return curve.filter(p => new Date(p.date) >= startDate)
})

const dualAccuracyCurveOption = computed(() => {
  const wordCurve = filteredCurveData.value
  const questionCurve = stats.value.question_accuracy_curve || []

  const allDates = [...new Set([...wordCurve.map(p => p.date), ...questionCurve.map(p => p.date)])].sort()

  if (!allDates.length) return {}

  const wordMap = new Map(wordCurve.map(p => [p.date, p.accuracy]))
  const questionMap = new Map(questionCurve.map(p => [p.date, p.accuracy]))

  return {
    tooltip: {
      trigger: 'axis',
      backgroundColor: '#ffffff',
      borderColor: '#e2e8f0',
      borderWidth: 1,
      textStyle: { color: '#334155' },
      formatter: function(params) {
        let result = params[0].name + '<br/>'
        params.forEach(p => {
          if (p.value !== null) {
            result += '<span style="display:inline-block;margin-right:4px;border-radius:10px;width:10px;height:10px;background-color:' + p.color + '"></span>'
            result += p.seriesName + ': ' + p.value + '%<br/>'
          }
        })
        return result
      }
    },
    legend: {
      data: ['单词正确率', '错题正确率'],
      bottom: 0,
      textStyle: { color: '#64748b' }
    },
    grid: { left: '3%', right: '4%', bottom: '15%', top: '10px', containLabel: true },
    xAxis: {
      type: 'category',
      data: allDates,
      axisLine: { lineStyle: { color: '#e2e8f0' } },
      axisLabel: { color: '#64748b' }
    },
    yAxis: {
      type: 'value',
      name: '正确率%',
      min: 0,
      max: 100,
      axisLabel: { formatter: '{value}%', color: '#64748b' },
      splitLine: { lineStyle: { color: '#eef2f7' } }
    },
    series: [
      {
        name: '单词正确率',
        type: 'line',
        smooth: true,
        connectNulls: true,
        symbol: 'circle',
        symbolSize: 7,
        lineStyle: { color: '#22c55e', width: 3 },
        itemStyle: { color: '#22c55e' },
        areaStyle: {
          color: {
            type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(34, 197, 94, 0.22)' },
              { offset: 1, color: 'rgba(34, 197, 94, 0.03)' }
            ]
          }
        },
        data: allDates.map(date => wordMap.get(date) ?? null)
      },
      {
        name: '错题正确率',
        type: 'line',
        smooth: true,
        connectNulls: true,
        symbol: 'circle',
        symbolSize: 7,
        lineStyle: { color: '#4f46e5', width: 3 },
        itemStyle: { color: '#4f46e5' },
        areaStyle: {
          color: {
            type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(79, 70, 229, 0.2)' },
              { offset: 1, color: 'rgba(79, 70, 229, 0.03)' }
            ]
          }
        },
        data: allDates.map(date => questionMap.get(date) ?? null)
      }
    ]
  }
})

onMounted(async () => {
  // 默认使用管理配置中的年级（当前为六年级）
  try {
    await appConfigStore.load()
    selectedGrade.value = appConfigStore.defaultGrade || 6
  } catch {
    selectedGrade.value = 6
  }
  await loadAllStats()
})
</script>

<style scoped>
.home {
  min-height: 100vh;
  background: linear-gradient(180deg, #eef2ff 0%, #f8fafc 100%);
  padding: 32px;
  max-width: 1600px;
  margin: 0 auto;
}

/* Hero */
.hero {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  margin-bottom: 32px;
}

.hero-eyebrow {
  font-size: 12px;
  font-weight: 700;
  letter-spacing: 0.14em;
  color: #6366f1;
  text-transform: uppercase;
  margin: 0 0 8px 0;
}

.hero-title {
  font-size: 40px;
  font-weight: 800;
  color: #312e81;
  margin: 0 0 6px 0;
  letter-spacing: -0.02em;
}

.hero-sub {
  font-size: 16px;
  color: #64748b;
  margin: 0;
}

.date-chip {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 12px 18px;
  background: #ffffff;
  border: 3px solid #c7d2fe;
  border-radius: 16px;
  box-shadow: 5px 5px 0 rgba(99, 102, 241, 0.28), 0 10px 24px rgba(79, 70, 229, 0.12);
}

.chip-icon {
  width: 20px;
  height: 20px;
  color: #6366f1;
}

.chip-text {
  font-size: 14px;
  font-weight: 600;
  color: #4338ca;
}

/* Stats Grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
}

.stat-card {
  position: relative;
  background: #ffffff;
  border: 3px solid;
  border-radius: 22px;
  padding: 20px;
  cursor: pointer;
  transition: transform 0.25s ease, box-shadow 0.25s ease;
}

.stat-lg {
  grid-column: span 2;
  grid-row: span 2;
}

.stat-top {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 18px;
}

.stat-label {
  font-size: 13px;
  font-weight: 600;
  color: #64748b;
  letter-spacing: 0.02em;
}

.stat-icon {
  width: 40px;
  height: 40px;
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #ffffff;
}

.stat-icon svg {
  width: 22px;
  height: 22px;
}

.stat-value {
  font-size: 44px;
  font-weight: 800;
  color: #1e293b;
  line-height: 1;
  letter-spacing: -0.02em;
}

.stat-foot {
  margin-top: 14px;
  font-size: 12px;
  color: #94a3b8;
  display: flex;
  align-items: center;
  gap: 4px;
}

.arrow {
  transition: transform 0.25s ease;
}

.stat-card:hover .arrow {
  transform: translateX(4px);
}

/* Tone variants */
.tone-indigo {
  border-color: #4f46e5;
  box-shadow: 7px 7px 0 rgba(79, 70, 229, 0.32), 0 14px 30px rgba(79, 70, 229, 0.18);
}
.tone-indigo:hover {
  box-shadow: 11px 11px 0 rgba(79, 70, 229, 0.32), 0 22px 38px rgba(79, 70, 229, 0.24);
}
.tone-indigo .stat-icon { background: linear-gradient(135deg, #6366f1, #4f46e5); }
.tone-indigo .stat-value { color: #3730a3; }

.tone-violet {
  border-color: #8b5cf6;
  box-shadow: 7px 7px 0 rgba(139, 92, 246, 0.32), 0 14px 30px rgba(139, 92, 246, 0.16);
}
.tone-violet:hover {
  box-shadow: 11px 11px 0 rgba(139, 92, 246, 0.32), 0 22px 38px rgba(139, 92, 246, 0.22);
}
.tone-violet .stat-icon { background: linear-gradient(135deg, #a78bfa, #8b5cf6); }
.tone-violet .stat-value { color: #5b21b6; }

.tone-sky {
  border-color: #0ea5e9;
  box-shadow: 7px 7px 0 rgba(14, 165, 233, 0.32), 0 14px 30px rgba(14, 165, 233, 0.16);
}
.tone-sky:hover {
  box-shadow: 11px 11px 0 rgba(14, 165, 233, 0.32), 0 22px 38px rgba(14, 165, 233, 0.22);
}
.tone-sky .stat-icon { background: linear-gradient(135deg, #38bdf8, #0ea5e9); }
.tone-sky .stat-value { color: #075985; }

.tone-emerald {
  border-color: #10b981;
  box-shadow: 7px 7px 0 rgba(16, 185, 129, 0.32), 0 14px 30px rgba(16, 185, 129, 0.16);
}
.tone-emerald:hover {
  box-shadow: 11px 11px 0 rgba(16, 185, 129, 0.32), 0 22px 38px rgba(16, 185, 129, 0.22);
}
.tone-emerald .stat-icon { background: linear-gradient(135deg, #34d399, #10b981); }
.tone-emerald .stat-value { color: #047857; }

.tone-amber {
  border-color: #f59e0b;
  box-shadow: 7px 7px 0 rgba(245, 158, 11, 0.32), 0 14px 30px rgba(245, 158, 11, 0.16);
}
.tone-amber:hover {
  box-shadow: 11px 11px 0 rgba(245, 158, 11, 0.32), 0 22px 38px rgba(245, 158, 11, 0.22);
}
.tone-amber .stat-icon { background: linear-gradient(135deg, #fbbf24, #f59e0b); }
.tone-amber .stat-value { color: #92400e; }

.tone-rose {
  border-color: #f43f5e;
  box-shadow: 7px 7px 0 rgba(244, 63, 94, 0.32), 0 14px 30px rgba(244, 63, 94, 0.16);
}
.tone-rose:hover {
  box-shadow: 11px 11px 0 rgba(244, 63, 94, 0.32), 0 22px 38px rgba(244, 63, 94, 0.22);
}
.tone-rose .stat-icon { background: linear-gradient(135deg, #fb7185, #f43f5e); }
.tone-rose .stat-value { color: #9f1239; }

.tone-fuchsia {
  border-color: #d946ef;
  box-shadow: 7px 7px 0 rgba(217, 70, 239, 0.32), 0 14px 30px rgba(217, 70, 239, 0.16);
}
.tone-fuchsia:hover {
  box-shadow: 11px 11px 0 rgba(217, 70, 239, 0.32), 0 22px 38px rgba(217, 70, 239, 0.22);
}
.tone-fuchsia .stat-icon { background: linear-gradient(135deg, #e879f9, #d946ef); }
.tone-fuchsia .stat-value { color: #86198f; }

.tone-cyan {
  border-color: #06b6d4;
  box-shadow: 7px 7px 0 rgba(6, 182, 212, 0.32), 0 14px 30px rgba(6, 182, 212, 0.16);
}
.tone-cyan:hover {
  box-shadow: 11px 11px 0 rgba(6, 182, 212, 0.32), 0 22px 38px rgba(6, 182, 212, 0.22);
}
.tone-cyan .stat-icon { background: linear-gradient(135deg, #22d3ee, #06b6d4); }
.tone-cyan .stat-value { color: #155e75; }

.tone-lime {
  border-color: #84cc16;
  box-shadow: 7px 7px 0 rgba(132, 204, 22, 0.32), 0 14px 30px rgba(132, 204, 22, 0.16);
}
.tone-lime:hover {
  box-shadow: 11px 11px 0 rgba(132, 204, 22, 0.32), 0 22px 38px rgba(132, 204, 22, 0.22);
}
.tone-lime .stat-icon { background: linear-gradient(135deg, #a3e635, #84cc16); }
.tone-lime .stat-value { color: #3f6212; }

/* Content Grid */
.content-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-top: 20px;
}

/* Grade Switcher */
.grade-switch-bar {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
  margin: 0 0 20px 0;
  padding: 14px 16px;
  background: #ffffff;
  border: 3px solid #c7d2fe;
  border-radius: 18px;
  box-shadow: 5px 5px 0 rgba(99, 102, 241, 0.18);
}

.grade-switch-label {
  font-size: 13px;
  font-weight: 800;
  color: #4338ca;
  letter-spacing: 0.04em;
}

.grade-switch-chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  flex: 1;
}

.grade-switch-chip {
  border: 2px solid #e2e8f0;
  background: #fff;
  border-radius: 999px;
  padding: 6px 14px;
  font-size: 13px;
  font-weight: 600;
  color: #475569;
  cursor: pointer;
  transition: all 0.15s ease;
}

.grade-switch-chip:hover {
  border-color: #a5b4fc;
  color: #3730a3;
}

.grade-switch-chip.active {
  border-color: #4f46e5;
  background: #4f46e5;
  color: #fff;
  box-shadow: 0 6px 14px rgba(79, 70, 229, 0.28);
}

.grade-switch-note {
  font-size: 12px;
  color: #94a3b8;
  white-space: nowrap;
}

@media (max-width: 720px) {
  .grade-switch-note {
    white-space: normal;
  }
}

.panel {
  background: #ffffff;
  border: 3px solid #e2e8f0;
  border-radius: 22px;
  padding: 24px;
  box-shadow: 7px 7px 0 rgba(148, 163, 184, 0.28), 0 14px 30px rgba(79, 70, 229, 0.08);
}

.panel-full {
  grid-column: span 2;
}

.panel-head {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 18px;
  flex-wrap: wrap;
  gap: 12px;
}

.panel-title {
  font-size: 18px;
  font-weight: 700;
  color: #312e81;
  margin: 0;
}

.subject-select {
  width: 140px;
}

/* Overview */
.overview-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

.overview-col {
  background: #f8fafc;
  border: 2px solid #e2e8f0;
  border-radius: 16px;
  padding: 16px;
}

.overview-col-title {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  font-weight: 700;
  color: #475569;
  margin-bottom: 14px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}

.title-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

.dot-slate { background: #94a3b8; }
.dot-indigo { background: #6366f1; }

.overview-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.overview-item {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 14px;
  color: #475569;
}

.ov-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

.dot-emerald { background: #10b981; }
.dot-blue { background: #3b82f6; }
.dot-emerald-light { background: #6ee7b7; }
.dot-blue-light { background: #93c5fd; }

/* Chart */
.chart-container {
  padding: 6px 0;
}

/* Table */
.subject-table {
  width: 100%;
}

.subject-table :deep(.el-table__header-wrapper th) {
  background: #f8fafc !important;
  color: #64748b;
  font-weight: 600;
}

.subject-table :deep(.el-table--striped .el-table__body tr.el-table__row--striped td) {
  background: #f8fafc;
}

.question-count {
  font-weight: 700;
  color: #4f46e5;
  font-size: 15px;
}

.practice-count {
  color: #059669;
  font-weight: 600;
}

.difficulty-bars {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.diff-bar-item {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
}

.diff-label {
  width: 40px;
  color: #64748b;
  flex-shrink: 0;
}

.diff-count {
  width: 22px;
  text-align: right;
  color: #94a3b8;
  font-size: 11px;
  flex-shrink: 0;
}

.error-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 4px;
}

/* Responsive */
@media (max-width: 1200px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }

  .stat-lg {
    grid-column: span 2;
  }

  .content-grid {
    grid-template-columns: 1fr;
  }

  .panel-full {
    grid-column: span 1;
  }
}

@media (max-width: 768px) {
  .home {
    padding: 16px;
  }

  .stats-grid {
    grid-template-columns: 1fr;
  }

  .stat-lg {
    grid-column: span 1;
    grid-row: auto;
  }

  .hero {
    flex-direction: column;
    align-items: flex-start;
    gap: 16px;
  }

  .hero-title {
    font-size: 30px;
  }

  .stat-value {
    font-size: 36px;
  }

  .overview-grid {
    grid-template-columns: 1fr;
  }
}
</style>
