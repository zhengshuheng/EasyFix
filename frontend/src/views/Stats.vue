<template>
  <div class="stats-page">
    <!-- 年级快速切换（与顶栏联动，指定年级后隐藏；合并自原首页） -->
    <section v-if="subjectStore.isAllGrade" class="grade-switch-bar">
      <div class="grade-switch-label">年级</div>
      <div class="grade-switch-chips">
        <button
          class="grade-switch-chip"
          :class="{ active: selectedGrade === null }"
          @click="onGradeChange(null)"
        >
          全部
        </button>
        <button
          v-for="g in gradeOptions"
          :key="g.value"
          class="grade-switch-chip"
          :class="{ active: selectedGrade === g.value }"
          @click="onGradeChange(g.value)"
        >
          {{ g.label }}
          <span v-if="kidGrade && g.value <= kidGrade" class="chip-badge" :class="{ 'is-current': g.value === kidGrade }">
            {{ g.value === kidGrade ? '当前' : '已学' }}
          </span>
        </button>
      </div>
      <div class="grade-switch-note">不区分上下学期 · 切换后整页数据联动（与顶部空间选择一致）</div>
    </section>

    <!-- 学习概览（昨日 vs 今日，合并自原首页） -->
    <el-row :gutter="16" class="overview-cards">
      <el-col :xs="24" :sm="12" v-for="col in overviewCols" :key="col.title">
        <div class="overview-panel">
          <div class="overview-panel-title">{{ col.title }}</div>
          <div class="overview-panel-list">
            <div v-for="item in col.items" :key="item.label" class="overview-panel-item">
              <span class="op-dot" :style="{ background: item.color }"></span>
              <span>{{ item.text }}</span>
            </div>
          </div>
        </div>
      </el-col>
    </el-row>

    <!-- 顶部总览卡片 -->
    <el-row :gutter="16" class="overview-cards">
      <el-col :xs="12" :sm="8" :md="4" v-for="card in overviewCards" :key="card.label">
        <div class="overview-card" :style="{ borderTopColor: card.color }">
          <div class="card-value" :style="{ color: card.color }">{{ card.value }}</div>
          <div class="card-label">{{ card.label }}</div>
        </div>
      </el-col>
    </el-row>

    <!-- 知识点掌握 -->
    <el-row :gutter="20" class="section-row">
      <el-col :xs="24" :md="10">
        <el-card class="chart-card">
          <template #header><span class="card-title">知识点正确率</span></template>
          <v-chart :option="kpRadarOption" autoresize style="height: 320px" />
        </el-card>
      </el-col>
      <el-col :xs="24" :md="14">
        <el-card class="chart-card">
          <template #header><span class="card-title">知识点题数与正确率</span></template>
          <v-chart :option="kpBarOption" autoresize style="height: 320px" />
        </el-card>
      </el-col>
    </el-row>

    <!-- 错题分析 + 单词分析 -->
    <el-row :gutter="20" class="section-row">
      <el-col :xs="24" :md="12">
        <el-card class="chart-card">
          <template #header><span class="card-title">错题错误类型分布</span></template>
          <v-chart :option="errorTypeOption" autoresize style="height: 280px" />
        </el-card>
      </el-col>
      <el-col :xs="24" :md="12">
        <el-card class="chart-card">
          <template #header><span class="card-title">单词记忆阶段</span></template>
          <v-chart :option="wordPhaseOption" autoresize style="height: 280px" />
          <!-- 单词学习过程五维进度（合并自原首页） -->
          <div v-if="showWordStats && wordDimStats.length" class="word-dim-list">
            <div v-for="d in wordDimStats" :key="d.key" class="word-dim-item">
              <div class="wd-top">
                <span class="wd-label">{{ d.label }}</span>
                <span class="wd-num">{{ d.done }} / {{ d.total }}</span>
              </div>
              <el-progress :percentage="pct(d)" :stroke-width="8" :color="dimColor(d.key)" />
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 难度分布 + 复习正确率趋势 -->
    <el-row :gutter="20" class="section-row">
      <el-col :xs="24" :md="10">
        <el-card class="chart-card">
          <template #header><span class="card-title">错题难度分布</span></template>
          <v-chart :option="difficultyOption" autoresize style="height: 280px" />
        </el-card>
      </el-col>
      <el-col :xs="24" :md="14">
        <el-card class="chart-card">
          <template #header><span class="card-title">正确率趋势（单词 + 错题）</span></template>
          <v-chart :option="dualAccuracyCurveOption" autoresize style="height: 280px" />
        </el-card>
      </el-col>
    </el-row>

    <!-- 复习状态明细 -->
    <el-row :gutter="20" class="section-row">
      <el-col :span="24">
        <el-card class="chart-card">
          <template #header><span class="card-title">知识点复习状态明细</span></template>
          <el-table :data="kpTableData" stripe size="small" style="width: 100%">
            <el-table-column prop="name" label="知识点" min-width="120" />
            <el-table-column prop="total" label="题数" width="70" align="center" />
            <el-table-column label="已复习" width="80" align="center">
              <template #default="{ row }">
                <span>{{ row.reviewed }}/{{ row.total }}</span>
              </template>
            </el-table-column>
            <el-table-column label="复习进度" width="140">
              <template #default="{ row }">
                <el-progress
                  :percentage="Math.round(row.reviewed / row.total * 100)"
                  :stroke-width="10"
                  :color="row.reviewed >= row.total ? '#67c23a' : '#409eff'"
                />
              </template>
            </el-table-column>
            <el-table-column label="正确率" width="100" align="center">
              <template #default="{ row }">
                <el-tag :type="accTagType(row.accuracy)" size="small">{{ row.accuracy }}%</el-tag>
              </template>
            </el-table-column>
            <el-table-column label="正确率条" min-width="160">
              <template #default="{ row }">
                <div class="acc-bar-bg">
                  <div class="acc-bar-fill" :style="{ width: row.accuracy + '%', background: accColor(row.accuracy) }"></div>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { statsApi, statsOverviewApi } from '@/api/question'
import { wordApi } from '@/api/word'
import { motivationApi } from '@/api/motivation'
import { useSubjectStore } from '@/stores/subject'
import { useKidStore } from '@/stores/kid'
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart, BarChart, RadarChart, LineChart } from 'echarts/charts'
import {
  TitleComponent, TooltipComponent, LegendComponent,
  GridComponent, RadarComponent, MarkLineComponent
} from 'echarts/components'

use([
  CanvasRenderer, PieChart, BarChart, RadarChart, LineChart,
  TitleComponent, TooltipComponent, LegendComponent,
  GridComponent, RadarComponent, MarkLineComponent
])

const router = useRouter()
const subjectStore = useSubjectStore()
const kidStore = useKidStore()

const stats = ref({})
const kpStats = ref([])
const wordMastery = ref({ new_words: 0, learning_words: 0, mastered_words: 0 })

// ========== 合并自原首页：单词指标只在「全部」或「英语」空间展示 ==========
const showWordStats = computed(() => subjectStore.isAll || subjectStore.isEnglish)
const wordDimStats = computed(() => stats.value.word_stats?.dim_stats || [])
const pct = (d) => (d.total ? Math.round((d.done / d.total) * 100) : 0)
const dimColor = (key) => {
  const map = { listen: '#409eff', recognize: '#67c23a', read: '#e6a23c', speak: '#9b59b6', write: '#f56c6c' }
  return map[key] || '#409eff'
}

// ========== 合并自原首页：学习概览（昨日 vs 今日） ==========
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
const overviewCols = computed(() => {
  const ov = learningOverview.value
  const cols = [
    { title: '昨日', items: [
      { label: 'qw', color: '#10b981', text: `${ov.yesterday_word_review_count} 复习单词` },
      { label: 'qq', color: '#3b82f6', text: `${ov.yesterday_question_review_count} 复习错题` },
      { label: 'wac', color: '#a7f3d0', text: `${ov.yesterday_word_accuracy}% 单词正确率` },
      { label: 'qac', color: '#bfdbfe', text: `${ov.yesterday_question_accuracy}% 错题正确率` },
    ]},
    { title: '今日', items: [
      { label: 'tw', color: '#10b981', text: `${ov.today_word_review_count} 复习单词` },
      { label: 'tq', color: '#3b82f6', text: `${ov.today_question_review_count} 复习错题` },
      { label: 'twac', color: '#a7f3d0', text: `${ov.today_word_accuracy}% 单词正确率` },
      { label: 'tqac', color: '#bfdbfe', text: `${ov.today_question_accuracy}% 错题正确率` },
    ]},
  ]
  if (!showWordStats.value) {
    cols.forEach(c => { c.items = c.items.filter(i => !i.label.includes('w')) })
  }
  return cols
})

// ========== 合并自原首页：年级切换条 ==========
const gradeLabelMap = {
  1: '一年级', 2: '二年级', 3: '三年级', 4: '四年级', 5: '五年级', 6: '六年级',
  7: '初一', 8: '初二', 9: '初三', 10: '高一', 11: '高二', 12: '高三',
}
const gradeOptions = [
  { label: '一年级', value: 1 }, { label: '二年级', value: 2 }, { label: '三年级', value: 3 },
  { label: '四年级', value: 4 }, { label: '五年级', value: 5 }, { label: '六年级', value: 6 },
  { label: '初一', value: 7 }, { label: '初二', value: 8 }, { label: '初三', value: 9 },
  { label: '高一', value: 10 }, { label: '高二', value: 11 }, { label: '高三', value: 12 },
]
const kidGrade = computed(() => {
  const g = kidStore.activeKid?.current_grade
  const n = Number(g)
  return n >= 1 && n <= 12 ? n : null
})
const selectedGrade = computed({
  get: () => subjectStore.activeGrade,
  set: (v) => subjectStore.setGrade(v),
})
const onGradeChange = (g) => {
  if (subjectStore.activeGrade === g) return
  subjectStore.setGrade(g)
  loadAll()
}

const overviewCards = computed(() => {
  const s = stats.value
  const ws = s.word_stats || {}
  return [
    { label: '错题总数', value: s.total_questions || 0, color: '#f56c6c' },
    { label: '单词总数', value: ws.total_words || 0, color: '#409eff' },
    { label: '知识点数', value: kpStats.value.length || 0, color: '#9a60b4' },
    { label: '待复习错题', value: s.to_review_questions || 0, color: '#e6a23c' },
    { label: '待复习单词', value: ws.to_review_count || 0, color: '#e6a23c' },
    { label: '复习次数', value: ws.total_reviews || 0, color: '#67c23a' },
  ]
})

// ========== 知识点雷达图 ==========
const kpRadarOption = computed(() => {
  const data = kpStats.value
  if (!data.length) return {}
  const indicator = data.map(d => ({ name: d.name, max: 100 }))
  // 指定学科时单系列；全部时按学科分组（动态，不依赖硬编码名单）
  let seriesData
  if (subjectStore.isAll) {
    const groups = new Map()
    data.forEach(d => {
      if (!groups.has(d.subject_id)) groups.set(d.subject_id, [])
      groups.get(d.subject_id).push(d)
    })
    const colors = ['#f56c6c', '#409eff', '#67c23a', '#e6a23c', '#9a60b4', '#73c0de']
    seriesData = [...groups.entries()].map(([sid, items], i) => {
      const names = items.map(d => d.name)
      return {
        name: items[0].subject_name || '未分类',
        value: data.map(d => names.includes(d.name) ? d.accuracy : 0),
        lineStyle: { color: colors[i % colors.length], width: 2 },
        areaStyle: { color: colors[i % colors.length] + '26' },
        itemStyle: { color: colors[i % colors.length] },
        symbol: 'circle', symbolSize: 6,
      }
    })
  } else {
    const subjectName = subjectStore.activeSubject?.name || '当前学科'
    seriesData = [{
      name: subjectName,
      value: data.map(d => d.accuracy),
      lineStyle: { color: '#409eff', width: 2 },
      areaStyle: { color: 'rgba(64,158,255,0.15)' },
      itemStyle: { color: '#409eff' },
      symbol: 'circle', symbolSize: 6,
    }]
  }
  return {
    tooltip: { trigger: 'item' },
    legend: { data: seriesData.map(s => s.name), bottom: 0 },
    radar: {
      indicator,
      shape: 'polygon',
      splitNumber: 5,
      axisName: { fontSize: 11, color: '#666' },
    },
    series: [{
      type: 'radar',
      data: seriesData,
    }]
  }
})

// ========== 知识点柱状图 ==========
const kpBarOption = computed(() => {
  const data = kpStats.value
  if (!data.length) return {}
  const sorted = [...data].sort((a, b) => b.total - a.total)
  return {
    tooltip: {
      trigger: 'axis',
      formatter: params => {
        const d = params[0]
        const kp = sorted[d.dataIndex]
        return `${kp.name}<br/>题数: ${kp.total}<br/>正确率: ${kp.accuracy}%`
      }
    },
    grid: { left: 100, right: 50, top: 10, bottom: 30 },
    xAxis: { type: 'value', name: '题数' },
    yAxis: {
      type: 'category',
      data: sorted.map(d => d.name),
      axisLabel: { fontSize: 12 },
    },
    series: [{
      type: 'bar',
      data: sorted.map(d => ({
        value: d.total,
        itemStyle: { color: accColor(d.accuracy), borderRadius: [0, 4, 4, 0] }
      })),
      barWidth: 18,
      label: {
        show: true, position: 'right',
        formatter: p => sorted[p.dataIndex].accuracy + '%',
        fontSize: 11, color: '#666',
      },
    }]
  }
})

// ========== 错误类型环形图 ==========
const errorTypeOption = computed(() => {
  const dist = stats.value.error_type_distribution || {}
  const entries = Object.entries(dist)
  const colors = ['#5470c6','#91cc75','#fac858','#ee6666','#73c0de','#3ba272','#fc8452','#9a60b4']
  return {
    tooltip: { trigger: 'item', formatter: '{b}: {c}题 ({d}%)' },
    legend: { orient: 'vertical', right: 10, top: 'center', textStyle: { fontSize: 12 } },
    series: [{
      type: 'pie', radius: ['40%', '70%'], center: ['40%', '50%'],
      itemStyle: { borderRadius: 6, borderColor: '#fff', borderWidth: 2 },
      label: { show: false },
      emphasis: { label: { show: true, fontSize: 14, fontWeight: 'bold' } },
      data: entries.map(([name, value], i) => ({
        name, value,
        itemStyle: { color: colors[i % colors.length] }
      })),
    }]
  }
})

// ========== 单词记忆阶段 ==========
const wordPhaseOption = computed(() => {
  const m = wordMastery.value
  const phases = [
    { name: '新学', value: m.new_words || 0, color: '#409eff' },
    { name: '学习中', value: m.learning_words || 0, color: '#e6a23c' },
    { name: '已牢记', value: m.mastered_words || 0, color: '#67c23a' },
  ].filter(p => p.value > 0)
  const total = phases.reduce((s, d) => s + d.value, 0)
  return {
    tooltip: { trigger: 'item', formatter: p => `${p.name}: ${p.value}词 (${Math.round(p.value/total*100)}%)` },
    legend: { bottom: 0 },
    series: [{
      type: 'pie', radius: ['40%', '70%'], center: ['50%', '45%'],
      itemStyle: { borderRadius: 6, borderColor: '#fff', borderWidth: 2 },
      label: { show: true, formatter: '{b}\n{d}%', fontSize: 12 },
      data: phases.map(d => ({
        name: d.name, value: d.value,
        itemStyle: { color: d.color }
      })),
    }]
  }
})

// ========== 难度分布 ==========
const difficultyOption = computed(() => {
  const dist = stats.value.difficulty_distribution || {}
  const levels = ['1','2','3','4','5']
  const labels = ['简单', '较易', '中等', '较难', '困难']
  const colors = ['#67c23a','#95d475','#e6a23c','#f56c6c','#c45656']
  return {
    tooltip: { trigger: 'axis' },
    grid: { left: 50, right: 20, top: 10, bottom: 30 },
    xAxis: { type: 'category', data: labels },
    yAxis: { type: 'value' },
    series: [{
      type: 'bar',
      data: levels.map((l, i) => ({
        value: dist[l] || 0,
        itemStyle: { color: colors[i], borderRadius: [6, 6, 0, 0] }
      })),
      barWidth: 36,
      label: { show: true, position: 'top', fontSize: 12 },
    }]
  }
})

// ========== 正确率趋势（单词+错题双线，合并自原首页） ==========
const curveRange = ref('month')
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
      data: showWordStats.value ? ['单词正确率', '错题正确率'] : ['错题正确率'],
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
      ...(showWordStats.value ? [{
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
      }] : []),
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

// ========== 复习状态表格 ==========
const kpTableData = computed(() => kpStats.value)

const accTagType = (acc) => {
  if (acc >= 70) return 'success'
  if (acc >= 50) return 'warning'
  return 'danger'
}
const accColor = (acc) => {
  if (acc >= 70) return '#67c23a'
  if (acc >= 50) return '#e6a23c'
  return '#f56c6c'
}

// ========== 数据加载 ==========
const loadAll = async () => {
  // 学习空间指定学科/年级时，只加载当前空间分析
  const subjectParams = {}
  const activeSubjectId = subjectStore.activeSubjectId
  if (activeSubjectId !== null) subjectParams.subject_id = activeSubjectId
  if (subjectStore.activeGrade !== null) subjectParams.grade = subjectStore.activeGrade
  try {
    const [summaryRes, kpRes, wordRes, overviewRes] = await Promise.all([
      statsApi.getSummary(subjectParams),
      statsApi.getKnowledgePoints(subjectParams),
      wordApi.getStats(subjectParams),
      statsOverviewApi.getOverview(subjectParams),
    ])
    stats.value = summaryRes.data
    kpStats.value = kpRes.data
    learningOverview.value = overviewRes.data

    // Word mastery from word stats API
    const ws = wordRes.data || {}
    wordMastery.value = {
      new_words: ws.new_words || 0,
      learning_words: ws.learning_words || 0,
      mastered_words: ws.mastered_words || 0,
    }
  } catch (e) {
    console.error('加载统计数据失败:', e)
  }

  // 每日签到（激励中心）：当天首次进入自动 +积分，静默失败不影响分析
  try {
    const { data } = await motivationApi.checkin()
    if (data && data.checked && !data.already) {
      ElMessage.success(`每日签到成功，积分 +${data.star_delta}`)
    }
  } catch (e) {
    // 忽略：激励系统不可用不影响分析
  }
}

onMounted(loadAll)
</script>

<style scoped>
.stats-page {
  max-width: 1200px;
  margin: 0 auto;
}

.overview-cards {
  margin-bottom: 20px;
}

.overview-card {
  background: #fff;
  border-radius: 12px;
  padding: 20px 16px;
  text-align: center;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  border-top: 3px solid #409eff;
  transition: transform 0.2s;
}
.overview-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
}

.card-value {
  font-size: 32px;
  font-weight: 700;
  line-height: 1;
}

.card-label {
  font-size: 13px;
  color: #909399;
  margin-top: 8px;
}

.section-row {
  margin-bottom: 20px;
}

.chart-card {
  border-radius: 12px;
  overflow: hidden;
  height: 100%;
}

.chart-card :deep(.el-card__header) {
  padding: 14px 20px;
  background: #fafbfc;
  border-bottom: 1px solid #ebeef5;
}

.card-title {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
}

.acc-bar-bg {
  height: 8px;
  background: #f0f0f0;
  border-radius: 4px;
  overflow: hidden;
}

.acc-bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.6s ease;
}

/* ===== 合并自原首页：年级切换条 ===== */
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
  display: inline-flex;
  align-items: center;
  gap: 6px;
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

.chip-badge {
  font-size: 10px;
  line-height: 16px;
  padding: 0 6px;
  border-radius: 8px;
  color: #64748b;
  background: #e2e8f0;
}

.chip-badge.is-current {
  color: #fff;
  background: #4f46e5;
}

.grade-switch-chip.active .chip-badge {
  color: #fff;
  background: rgba(255, 255, 255, 0.22);
}

.grade-switch-note {
  font-size: 12px;
  color: #94a3b8;
  white-space: nowrap;
}

/* ===== 合并自原首页：学习概览面板 ===== */
.overview-panel {
  background: #fff;
  border-radius: 12px;
  padding: 16px 18px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  height: 100%;
}

.overview-panel-title {
  font-size: 14px;
  font-weight: 700;
  color: #303133;
  margin-bottom: 12px;
}

.overview-panel-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px 18px;
}

.overview-panel-item {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 13px;
  color: #606266;
}

.op-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  flex-shrink: 0;
}

/* ===== 合并自原首页：单词五维进度 ===== */
.word-dim-list {
  margin-top: 14px;
  padding-top: 10px;
  border-top: 1px dashed #ebeef5;
}

.word-dim-item {
  margin-bottom: 10px;
}

.word-dim-item:last-child {
  margin-bottom: 0;
}

.wd-top {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}

.wd-label {
  font-size: 12px;
  font-weight: 600;
  color: #606266;
}

.wd-num {
  font-size: 12px;
  color: #909399;
  font-weight: 600;
}

@media (max-width: 768px) {
  .overview-card { padding: 14px 10px; }
  .card-value { font-size: 24px; }
  .card-label { font-size: 12px; }
  .grade-switch-note { white-space: normal; }
}
</style>
