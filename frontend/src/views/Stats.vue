<template>
  <div class="stats-page">
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
          <template #header><span class="card-title">复习正确率趋势</span></template>
          <v-chart :option="trendOption" autoresize style="height: 280px" />
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
import { statsApi } from '@/api/question'
import { wordApi } from '@/api/word'
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

const stats = ref({})
const kpStats = ref([])
const wordMastery = ref({ new_words: 0, learning_words: 0, mastered_words: 0 })
const questionTrend = ref([])

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
const mathKPNames = ['方程与代数', '小数运算', '立体几何', '数的认识', '平面几何']

const kpRadarOption = computed(() => {
  const data = kpStats.value
  if (!data.length) return {}
  const indicator = data.map(d => ({ name: d.name, max: 100 }))
  return {
    tooltip: { trigger: 'item' },
    legend: { data: ['数学', '英语'], bottom: 0 },
    radar: {
      indicator,
      shape: 'polygon',
      splitNumber: 5,
      axisName: { fontSize: 11, color: '#666' },
    },
    series: [{
      type: 'radar',
      data: [
        {
          name: '数学',
          value: data.map(d => mathKPNames.includes(d.name) ? d.accuracy : 0),
          lineStyle: { color: '#f56c6c', width: 2 },
          areaStyle: { color: 'rgba(245,108,108,0.15)' },
          itemStyle: { color: '#f56c6c' },
          symbol: 'circle', symbolSize: 6,
        },
        {
          name: '英语',
          value: data.map(d => !mathKPNames.includes(d.name) ? d.accuracy : 0),
          lineStyle: { color: '#409eff', width: 2 },
          areaStyle: { color: 'rgba(64,158,255,0.15)' },
          itemStyle: { color: '#409eff' },
          symbol: 'circle', symbolSize: 6,
        },
      ]
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

// ========== 复习正确率趋势 ==========
const trendOption = computed(() => {
  const trend = questionTrend.value
  if (!trend.length) return {}
  return {
    tooltip: {
      trigger: 'axis',
      formatter: params => {
        let s = params[0].axisValue
        params.forEach(p => { s += `<br/>${p.marker} 正确率: ${p.value}%` })
        return s
      }
    },
    grid: { left: 50, right: 20, top: 20, bottom: 40 },
    xAxis: {
      type: 'category',
      data: trend.map(d => d.date),
      axisLabel: { fontSize: 11, rotate: 30 },
    },
    yAxis: { type: 'value', min: 0, max: 100, axisLabel: { formatter: '{value}%' } },
    series: [{
      name: '错题正确率',
      type: 'line', smooth: true,
      data: trend.map(d => d.accuracy),
      lineStyle: { color: '#409eff', width: 2.5 },
      itemStyle: { color: '#409eff' },
      areaStyle: { color: { type: 'linear', x: 0, y: 0, x2: 0, y2: 1, colorStops: [{ offset: 0, color: 'rgba(64,158,255,0.25)' }, { offset: 1, color: 'rgba(64,158,255,0.02)' }] } },
      symbol: 'circle', symbolSize: 5,
    }]
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
  try {
    const [summaryRes, kpRes, wordRes] = await Promise.all([
      statsApi.getSummary(),
      statsApi.getKnowledgePoints(),
      wordApi.getStats(),
    ])
    stats.value = summaryRes.data
    kpStats.value = kpRes.data

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

  // Load question trend from analysis API
  try {
    const { default: analysisApi } = await import('@/api/learning_analysis')
    const { data } = await analysisApi.getFullStats()
    questionTrend.value = data?.question_stats?.accuracy_trend || []
  } catch (e) {
    console.error('加载分析数据失败:', e)
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

@media (max-width: 768px) {
  .overview-card { padding: 14px 10px; }
  .card-value { font-size: 24px; }
  .card-label { font-size: 12px; }
}
</style>
