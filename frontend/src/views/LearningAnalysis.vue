<template>
  <div class="learning-analysis">
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <span>学习分析</span>
        </div>
      </template>

      <!-- Tab切换 -->
      <el-tabs v-model="activeTab">
        <!-- 概览 Tab -->
        <el-tab-pane label="概览" name="overview">
          <el-row :gutter="20" class="stat-cards-row">
            <el-col :span="6">
              <div class="stat-card gradient-green">
                <div class="stat-number">{{ overviewData.health_score || 0 }}</div>
                <div class="stat-text">学习健康度</div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-card gradient-orange">
                <div class="stat-number">{{ overviewData.weak_point_count || 0 }}</div>
                <div class="stat-text">薄弱点数量</div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-card gradient-purple">
                <div class="stat-number">{{ overviewData.suggestion_count || 0 }}</div>
                <div class="stat-text">改进建议</div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-card gradient-blue">
                <div class="stat-number">{{ overviewData.accuracy_rate || 0 }}%</div>
                <div class="stat-text">正确率</div>
              </div>
            </el-col>
          </el-row>

          <el-row :gutter="20" style="margin-top: 20px">
            <el-col :span="12">
              <el-card class="chart-card">
                <template #header>
                  <div class="card-header">
                    <span class="card-title">知识点掌握分布</span>
                  </div>
                </template>
                <div ref="overviewPieChartRef" class="chart-container"></div>
              </el-card>
            </el-col>
            <el-col :span="12">
              <el-card class="chart-card">
                <template #header>
                  <div class="card-header">
                    <span class="card-title">最近7天学习趋势</span>
                  </div>
                </template>
                <div ref="overviewLineChartRef" class="chart-container"></div>
              </el-card>
            </el-col>
          </el-row>
        </el-tab-pane>

        <!-- 薄弱点分析 Tab -->
        <el-tab-pane label="薄弱点分析" name="weak-points">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-card class="chart-card">
                <template #header>
                  <div class="card-header">
                    <span class="card-title">知识点错误排行</span>
                  </div>
                </template>
                <div ref="weakPointBarChartRef" class="chart-container"></div>
              </el-card>
            </el-col>
            <el-col :span="12">
              <el-card class="chart-card">
                <template #header>
                  <div class="card-header">
                    <span class="card-title">错误类型分布</span>
                  </div>
                </template>
                <div ref="errorTypePieChartRef" class="chart-container"></div>
              </el-card>
            </el-col>
          </el-row>

          <el-row :gutter="20" style="margin-top: 20px">
            <el-col :span="24">
              <el-card class="chart-card">
                <template #header>
                  <div class="card-header">
                    <span class="card-title">薄弱知识点详情</span>
                  </div>
                </template>
                <el-table :data="weakPointDetails" stripe style="width: 100%">
                  <el-table-column prop="knowledge_point" label="知识点" />
                  <el-table-column prop="error_count" label="错误次数" width="100" />
                  <el-table-column prop="accuracy_rate" label="正确率" width="100">
                    <template #default="{ row }">
                      <span :class="row.accuracy_rate < 50 ? 'text-danger' : 'text-warning'">
                        {{ row.accuracy_rate }}%
                      </span>
                    </template>
                  </el-table-column>
                  <el-table-column prop="mastery_level" label="掌握程度" width="120">
                    <template #default="{ row }">
                      <el-tag :type="getMasteryType(row.mastery_level)" size="small">
                        {{ row.mastery_level }}
                      </el-tag>
                    </template>
                  </el-table-column>
                </el-table>
              </el-card>
            </el-col>
          </el-row>
        </el-tab-pane>

        <!-- 学习行为 Tab -->
        <el-tab-pane label="学习行为" name="behavior">
          <el-row :gutter="20">
            <el-col :span="16">
              <el-card class="chart-card">
                <template #header>
                  <div class="card-header">
                    <span class="card-title">正确率趋势</span>
                  </div>
                </template>
                <div ref="accuracyLineChartRef" class="chart-container-long"></div>
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card class="chart-card">
                <template #header>
                  <div class="card-header">
                    <span class="card-title">学习频率</span>
                  </div>
                </template>
                <div ref="learningHeatmapRef" class="chart-container"></div>
              </el-card>
            </el-col>
          </el-row>

          <el-row :gutter="20" style="margin-top: 20px">
            <el-col :span="12">
              <el-card class="chart-card">
                <template #header>
                  <div class="card-header">
                    <span class="card-title">各学科学习时长分布</span>
                  </div>
                </template>
                <div ref="subjectTimeBarChartRef" class="chart-container"></div>
              </el-card>
            </el-col>
            <el-col :span="12">
              <el-card class="chart-card">
                <template #header>
                  <div class="card-header">
                    <span class="card-title">题目难度分布</span>
                  </div>
                </template>
                <div ref="difficultyBarChartRef" class="chart-container"></div>
              </el-card>
            </el-col>
          </el-row>
        </el-tab-pane>

        <!-- 单词掌握 Tab -->
        <el-tab-pane label="单词掌握" name="words">
          <el-row :gutter="20">
            <el-col :span="12">
              <el-card class="chart-card">
                <template #header>
                  <div class="card-header">
                    <span class="card-title">单词掌握率分布</span>
                  </div>
                </template>
                <div ref="wordMasteryPieChartRef" class="chart-container"></div>
              </el-card>
            </el-col>
            <el-col :span="12">
              <el-card class="chart-card">
                <template #header>
                  <div class="card-header">
                    <span class="card-title">各学科单词量</span>
                  </div>
                </template>
                <div ref="wordCountBarChartRef" class="chart-container"></div>
              </el-card>
            </el-col>
          </el-row>

          <el-row :gutter="20" style="margin-top: 20px">
            <el-col :span="24">
              <el-card class="chart-card">
                <template #header>
                  <div class="card-header">
                    <span class="card-title">掌握较差的单词</span>
                  </div>
                </template>
                <div v-if="lowAccuracyWords.length > 0" class="word-tags">
                  <el-tag
                    v-for="word in lowAccuracyWords"
                    :key="word.id"
                    type="danger"
                    effect="plain"
                    class="word-tag"
                  >
                    {{ word.word }} ({{ word.accuracy_rate }}%)
                  </el-tag>
                </div>
                <el-empty v-else description="暂无掌握较差的单词" />
              </el-card>
            </el-col>
          </el-row>
        </el-tab-pane>

        <!-- 改进建议 Tab -->
        <el-tab-pane label="改进建议" name="suggestions">
          <div v-if="llmSuggestions.length > 0" class="suggestions-container">
            <el-row :gutter="20">
              <el-col :span="24" v-for="(suggestion, index) in llmSuggestions" :key="index">
                <el-card class="suggestion-card" shadow="hover">
                  <template #header>
                    <div class="suggestion-header">
                      <span class="suggestion-title">{{ suggestion.title || `建议 ${index + 1}` }}</span>
                      <el-tag :type="getSuggestionType(suggestion.priority)" size="small">
                        {{ suggestion.priority === 'high' ? '高优先级' : suggestion.priority === 'medium' ? '中优先级' : '低优先级' }}
                      </el-tag>
                    </div>
                  </template>
                  <div class="suggestion-content">
                    <p class="suggestion-text">{{ suggestion.content || suggestion.description }}</p>
                    <div v-if="suggestion.action_items" class="suggestion-actions">
                      <div class="action-title">行动项:</div>
                      <ul>
                        <li v-for="(item, idx) in suggestion.action_items" :key="idx">{{ item }}</li>
                      </ul>
                    </div>
                  </div>
                </el-card>
              </el-col>
            </el-row>
          </div>
          <el-empty v-else description="暂无改进建议，请先完成一些学习内容后再来分析" />
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick, watch } from 'vue'
import * as echarts from 'echarts'
import { learningAnalysisApi } from '@/api/learning_analysis'

const activeTab = ref('overview')
const loading = ref(false)

// 数据
const overviewData = ref({
  health_score: 0,
  weak_point_count: 0,
  suggestion_count: 0,
  accuracy_rate: 0,
})

const weakPointDetails = ref([])
const lowAccuracyWords = ref([])
const llmSuggestions = ref([])

// 图表 DOM 引用
const overviewPieChartRef = ref(null)
const overviewLineChartRef = ref(null)
const weakPointBarChartRef = ref(null)
const errorTypePieChartRef = ref(null)
const accuracyLineChartRef = ref(null)
const learningHeatmapRef = ref(null)
const subjectTimeBarChartRef = ref(null)
const difficultyBarChartRef = ref(null)
const wordMasteryPieChartRef = ref(null)
const wordCountBarChartRef = ref(null)

// 图表实例
let overviewPieChart = null
let overviewLineChart = null
let weakPointBarChart = null
let errorTypePieChart = null
let accuracyLineChart = null
let learningHeatmap = null
let subjectTimeBarChart = null
let difficultyBarChart = null
let wordMasteryPieChart = null
let wordCountBarChart = null

// 获取概览数据
const fetchOverviewData = async () => {
  try {
    const res = await learningAnalysisApi.getFullStats()
    const data = res.data || {}

    overviewData.value = {
      health_score: data.health_score || 0,
      weak_point_count: data.weak_point_count || data.weak_points?.length || 0,
      suggestion_count: data.suggestions?.length || 0,
      accuracy_rate: data.accuracy_rate || 0,
    }

    // 更新概览饼图
    if (data.knowledge_mastery) {
      updateOverviewPieChart(data.knowledge_mastery)
    }

    // 更新概览折线图
    if (data.accuracy_trend) {
      updateOverviewLineChart(data.accuracy_trend)
    }
  } catch (error) {
    console.error('获取概览数据失败:', error)
  }
}

// 获取薄弱点数据
const fetchWeakPointData = async () => {
  try {
    const res = await learningAnalysisApi.getFullStats()
    const data = res.data || {}

    // 薄弱点详情
    weakPointDetails.value = data.weak_points || []

    // 更新错误排行柱状图
    if (data.weak_points && data.weak_points.length > 0) {
      updateWeakPointBarChart(data.weak_points)
    }

    // 更新错误类型饼图
    if (data.error_type_distribution) {
      updateErrorTypePieChart(data.error_type_distribution)
    }
  } catch (error) {
    console.error('获取薄弱点数据失败:', error)
  }
}

// 获取学习行为数据
const fetchBehaviorData = async () => {
  try {
    const res = await learningAnalysisApi.getFullStats()
    const data = res.data || {}

    // 更新正确率趋势图
    if (data.accuracy_trend) {
      updateAccuracyLineChart(data.accuracy_trend)
    }

    // 更新学习频率热力图
    if (data.learning_frequency) {
      updateLearningHeatmap(data.learning_frequency)
    }

    // 更新学科时长图
    if (data.subject_time) {
      updateSubjectTimeBarChart(data.subject_time)
    }

    // 更新难度分布图
    if (data.difficulty_distribution) {
      updateDifficultyBarChart(data.difficulty_distribution)
    }
  } catch (error) {
    console.error('获取学习行为数据失败:', error)
  }
}

// 获取单词掌握数据
const fetchWordMasteryData = async () => {
  try {
    const res = await learningAnalysisApi.getFullStats()
    const data = res.data || {}

    // 低准确率单词
    lowAccuracyWords.value = data.low_accuracy_words || []

    // 更新单词掌握率饼图
    if (data.word_mastery_distribution) {
      updateWordMasteryPieChart(data.word_mastery_distribution)
    }

    // 更新单词数量柱状图
    if (data.word_count_by_subject) {
      updateWordCountBarChart(data.word_count_by_subject)
    }
  } catch (error) {
    console.error('获取单词掌握数据失败:', error)
  }
}

// 获取LLM建议
const fetchLlmSuggestions = async () => {
  try {
    const res = await learningAnalysisApi.getLlmAnalysis()
    const data = res.data || {}

    if (data.suggestions) {
      llmSuggestions.value = data.suggestions
    } else if (Array.isArray(data)) {
      llmSuggestions.value = data
    } else {
      llmSuggestions.value = []
    }
  } catch (error) {
    console.error('获取LLM建议失败:', error)
    llmSuggestions.value = []
  }
}

// 初始化图表
const initCharts = () => {
  // 概览饼图
  if (overviewPieChartRef.value) {
    overviewPieChart = echarts.init(overviewPieChartRef.value)
  }

  // 概览折线图
  if (overviewLineChartRef.value) {
    overviewLineChart = echarts.init(overviewLineChartRef.value)
  }

  // 薄弱点柱状图
  if (weakPointBarChartRef.value) {
    weakPointBarChart = echarts.init(weakPointBarChartRef.value)
  }

  // 错误类型饼图
  if (errorTypePieChartRef.value) {
    errorTypePieChart = echarts.init(errorTypePieChartRef.value)
  }

  // 正确率趋势图
  if (accuracyLineChartRef.value) {
    accuracyLineChart = echarts.init(accuracyLineChartRef.value)
  }

  // 学习频率热力图
  if (learningHeatmapRef.value) {
    learningHeatmap = echarts.init(learningHeatmapRef.value)
  }

  // 学科时长柱状图
  if (subjectTimeBarChartRef.value) {
    subjectTimeBarChart = echarts.init(subjectTimeBarChartRef.value)
  }

  // 难度分布柱状图
  if (difficultyBarChartRef.value) {
    difficultyBarChart = echarts.init(difficultyBarChartRef.value)
  }

  // 单词掌握率饼图
  if (wordMasteryPieChartRef.value) {
    wordMasteryPieChart = echarts.init(wordMasteryPieChartRef.value)
  }

  // 单词数量柱状图
  if (wordCountBarChartRef.value) {
    wordCountBarChart = echarts.init(wordCountBarChartRef.value)
  }
}

// 更新概览饼图
const updateOverviewPieChart = (data) => {
  if (!overviewPieChart) return

  const chartData = Object.entries(data).map(([name, value]) => ({
    name,
    value,
  }))

  overviewPieChart.setOption({
    tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
    legend: { bottom: 10, left: 'center' },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['50%', '50%'],
      avoidLabelOverlap: true,
      itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
      label: { show: true, formatter: '{b}: {d}%' },
      emphasis: { scaleSize: 10 },
      data: chartData.length ? chartData : [{ name: '暂无数据', value: 0 }],
    }],
    color: ['#67c23a', '#e6a23c', '#f56c6c', '#409eff', '#9a60b4'],
  })
}

// 更新概览折线图
const updateOverviewLineChart = (data) => {
  if (!overviewLineChart) return

  // data 可能是数组或对象
  let xData = []
  let yData = []

  if (Array.isArray(data)) {
    xData = data.map((_, i) => `Day ${i + 1}`)
    yData = data
  } else if (typeof data === 'object') {
    xData = Object.keys(data)
    yData = Object.values(data)
  }

  overviewLineChart.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { type: 'category', boundaryGap: false, data: xData },
    yAxis: { type: 'value', min: 0, max: 100 },
    series: [{
      type: 'line',
      smooth: true,
      areaStyle: { opacity: 0.3 },
      data: yData,
      itemStyle: { color: '#409eff' },
      lineStyle: { width: 3 },
    }],
  })
}

// 更新薄弱点柱状图
const updateWeakPointBarChart = (data) => {
  if (!weakPointBarChart) return

  const chartData = data.slice(0, 10).map(item => ({
    name: item.knowledge_point || item.name || '未知',
    value: item.error_count || item.count || 0,
  }))

  weakPointBarChart.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { type: 'value' },
    yAxis: { type: 'category', data: chartData.map(d => d.name).reverse() },
    series: [{
      type: 'bar',
      data: chartData.map(d => d.value).reverse(),
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 1, 0, [
          { offset: 0, color: '#f56c6c' },
          { offset: 1, color: '#f78989' },
        ]),
        borderRadius: [0, 4, 4, 0],
      },
      label: { show: true, position: 'right' },
    }],
  })
}

// 更新错误类型饼图
const updateErrorTypePieChart = (data) => {
  if (!errorTypePieChart) return

  const chartData = Object.entries(data).map(([name, value]) => ({
    name,
    value,
  }))

  const colors = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4']

  errorTypePieChart.setOption({
    tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
    legend: { bottom: 10, left: 'center' },
    series: [{
      type: 'pie',
      radius: ['50%', '70%'],
      center: ['50%', '50%'],
      avoidLabelOverlap: true,
      itemStyle: { borderRadius: 8, borderColor: '#fff', borderWidth: 2 },
      label: { show: false },
      emphasis: { scaleSize: 8 },
      data: chartData.length ? chartData : [{ name: '暂无数据', value: 0 }],
    }],
    color: colors,
  })
}

// 更新正确率趋势图
const updateAccuracyLineChart = (data) => {
  if (!accuracyLineChart) return

  let xData = []
  let yData = []

  if (Array.isArray(data)) {
    xData = data.map((_, i) => `Day ${i + 1}`)
    yData = data
  } else if (typeof data === 'object') {
    xData = Object.keys(data)
    yData = Object.values(data)
  }

  accuracyLineChart.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { type: 'category', boundaryGap: false, data: xData },
    yAxis: { type: 'value', min: 0, max: 100, axisLabel: { formatter: '{value}%' } },
    series: [{
      type: 'line',
      smooth: true,
      areaStyle: { opacity: 0.3 },
      data: yData,
      itemStyle: { color: '#67c23a' },
      lineStyle: { width: 3 },
      markLine: {
        silent: true,
        lineStyle: { color: '#f56c6c', type: 'dashed' },
        data: [{ yAxis: 60, name: '及格线' }],
      },
    }],
  })
}

// 更新学习频率热力图
const updateLearningHeatmap = (data) => {
  if (!learningHeatmap) return

  // 假设数据是 {date: count} 格式
  const heatmapData = Object.entries(data).map(([date, count]) => [date, count])

  learningHeatmap.setOption({
    tooltip: { position: 'top', formatter: '{b}: {c} 题' },
    grid: { left: '2%', right: '2%', bottom: '15%', top: '10%' },
    xAxis: { type: 'category', data: heatmapData.map(d => d[0]), axisLabel: { rotate: 45 } },
    yAxis: { type: 'value', min: 0 },
    visualMap: {
      min: 0,
      max: Math.max(...heatmapData.map(d => d[1]), 10),
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: '0%',
      inRange: { color: ['#e8f4f8', '#409eff', '#f56c6c'] },
    },
    series: [{
      type: 'heatmap',
      data: heatmapData.map((d, i) => [i, 0, d[1]]),
      label: { show: true },
      emphasis: { itemStyle: { shadowBlur: 10, shadowColor: 'rgba(0, 0, 0, 0.5)' } },
    }],
  })
}

// 更新学科时长柱状图
const updateSubjectTimeBarChart = (data) => {
  if (!subjectTimeBarChart) return

  const chartData = Object.entries(data).map(([name, value]) => ({
    name,
    value,
  }))

  subjectTimeBarChart.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { type: 'category', data: chartData.map(d => d.name) },
    yAxis: { type: 'value', axisLabel: { formatter: '{value} min' } },
    series: [{
      type: 'bar',
      data: chartData.map(d => d.value),
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#409eff' },
          { offset: 1, color: '#66b1ff' },
        ]),
        borderRadius: [4, 4, 0, 0],
      },
      label: { show: true, position: 'top' },
    }],
  })
}

// 更新难度分布柱状图
const updateDifficultyBarChart = (data) => {
  if (!difficultyBarChart) return

  const chartData = Object.entries(data).map(([name, value]) => ({
    name: `难度${name}`,
    value,
  }))

  difficultyBarChart.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { type: 'category', data: chartData.map(d => d.name) },
    yAxis: { type: 'value' },
    series: [{
      type: 'bar',
      data: chartData.map((d, i) => ({
        value: d.value,
        itemStyle: { color: ['#67c23a', '#e6a23c', '#f56c6c'][i % 3] },
      })),
      barWidth: '50%',
      label: { show: true, position: 'top' },
    }],
  })
}

// 更新单词掌握率饼图
const updateWordMasteryPieChart = (data) => {
  if (!wordMasteryPieChart) return

  const chartData = Object.entries(data).map(([name, value]) => ({
    name,
    value,
  }))

  wordMasteryPieChart.setOption({
    tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
    legend: { bottom: 10, left: 'center' },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['50%', '50%'],
      avoidLabelOverlap: true,
      itemStyle: { borderRadius: 10, borderColor: '#fff', borderWidth: 2 },
      label: { show: true, formatter: '{b}: {d}%' },
      emphasis: { scaleSize: 10 },
      data: chartData.length ? chartData : [{ name: '暂无数据', value: 0 }],
    }],
    color: ['#67c23a', '#e6a23c', '#f56c6c', '#909399'],
  })
}

// 更新单词数量柱状图
const updateWordCountBarChart = (data) => {
  if (!wordCountBarChart) return

  const chartData = Object.entries(data).map(([name, value]) => ({
    name,
    value,
  }))

  wordCountBarChart.setOption({
    tooltip: { trigger: 'axis' },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: { type: 'category', data: chartData.map(d => d.name) },
    yAxis: { type: 'value' },
    series: [{
      type: 'bar',
      data: chartData.map(d => d.value),
      itemStyle: {
        color: new echarts.graphic.LinearGradient(0, 0, 0, 1, [
          { offset: 0, color: '#9a60b4' },
          { offset: 1, color: '#c68ce6' },
        ]),
        borderRadius: [4, 4, 0, 0],
      },
      label: { show: true, position: 'top' },
    }],
  })
}

// 掌握程度颜色
const getMasteryType = (level) => {
  const map = { '掌握': 'success', '基本掌握': 'warning', '未掌握': 'danger' }
  return map[level] || 'info'
}

// 建议优先级颜色
const getSuggestionType = (priority) => {
  const map = { 'high': 'danger', 'medium': 'warning', 'low': 'info' }
  return map[priority] || 'info'
}

// 窗口resize时重绘图表
const handleResize = () => {
  overviewPieChart?.resize()
  overviewLineChart?.resize()
  weakPointBarChart?.resize()
  errorTypePieChart?.resize()
  accuracyLineChart?.resize()
  learningHeatmap?.resize()
  subjectTimeBarChart?.resize()
  difficultyBarChart?.resize()
  wordMasteryPieChart?.resize()
  wordCountBarChart?.resize()
}

// 监听tab切换，加载对应数据
watch(activeTab, async (newTab) => {
  await nextTick()

  if (newTab === 'overview') {
    fetchOverviewData()
  } else if (newTab === 'weak-points') {
    fetchWeakPointData()
  } else if (newTab === 'behavior') {
    fetchBehaviorData()
  } else if (newTab === 'words') {
    fetchWordMasteryData()
  } else if (newTab === 'suggestions') {
    fetchLlmSuggestions()
  }
})

// 初始化
onMounted(async () => {
  loading.value = true

  // 初始化图表
  initCharts()

  // 获取概览数据
  await fetchOverviewData()

  // 监听窗口resize
  window.addEventListener('resize', handleResize)

  loading.value = false
})
</script>

<style scoped>
.learning-analysis {
  max-width: 1400px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-cards-row {
  margin-bottom: 20px;
}

.stat-card {
  border-radius: 16px;
  padding: 28px 20px;
  text-align: center;
  color: #fff;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
}

.gradient-green { background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%); }
.gradient-orange { background: linear-gradient(135deg, #e6a23c 0%, #f5a623 100%); }
.gradient-purple { background: linear-gradient(135deg, #9a60b4 0%, #b472c6 100%); }
.gradient-blue { background: linear-gradient(135deg, #409eff 0%, #66b1ff 100%); }

.stat-number {
  font-size: 48px;
  font-weight: bold;
  line-height: 1;
  text-shadow: 0 2px 8px rgba(0, 0, 0, 0.15);
}

.stat-text {
  font-size: 14px;
  margin-top: 10px;
  opacity: 0.9;
}

.chart-card {
  border-radius: 16px;
  overflow: hidden;
}

.chart-card :deep(.el-card__header) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 14px 20px;
  border: none;
}

.card-title {
  color: #fff;
  font-size: 15px;
  font-weight: 600;
}

.chart-container {
  height: 280px;
  padding: 10px;
}

.chart-container-long {
  height: 320px;
  padding: 10px;
}

.word-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.word-tag {
  font-size: 14px;
  padding: 8px 12px;
}

.suggestions-container {
  max-width: 900px;
  margin: 0 auto;
}

.suggestion-card {
  margin-bottom: 20px;
  border-radius: 12px;
}

.suggestion-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.suggestion-title {
  font-size: 16px;
  font-weight: 600;
  color: #303133;
}

.suggestion-content {
  padding: 10px 0;
}

.suggestion-text {
  font-size: 14px;
  color: #606266;
  line-height: 1.8;
  margin: 0;
}

.suggestion-actions {
  margin-top: 15px;
  padding: 15px;
  background: #f5f7fa;
  border-radius: 8px;
}

.action-title {
  font-size: 14px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 10px;
}

.suggestion-actions ul {
  margin: 0;
  padding-left: 20px;
}

.suggestion-actions li {
  font-size: 14px;
  color: #606266;
  line-height: 1.8;
}

.text-danger {
  color: #f56c6c;
  font-weight: bold;
}

.text-warning {
  color: #e6a23c;
  font-weight: bold;
}
</style>
