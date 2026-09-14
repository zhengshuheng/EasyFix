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

          <el-row :gutter="20" style="margin-top: 20px">
            <el-col :span="24">
              <el-card class="chart-card">
                <template #header>
                  <div class="card-header">
                    <span class="card-title">知识图谱</span>
                  </div>
                </template>
                <div ref="knowledgeGraphRef" class="chart-container-long"></div>
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
            <el-col :span="24">
              <el-card class="chart-card">
                <template #header>
                  <div class="card-header">
                    <span class="card-title">投入产出分析</span>
                  </div>
                </template>
                <div ref="inputOutputChartRef" class="chart-container-long"></div>
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
          <!-- 记忆曲线状态 -->
          <el-row :gutter="20" style="margin-bottom: 20px">
            <el-col :span="8">
              <div class="memory-status-card status-due">
                <div class="memory-status-number">{{ memoryCurveStatus.due || 0 }}</div>
                <div class="memory-status-text">待复习</div>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="memory-status-card status-on-track">
                <div class="memory-status-number">{{ memoryCurveStatus.on_track || 0 }}</div>
                <div class="memory-status-text">正常</div>
              </div>
            </el-col>
            <el-col :span="8">
              <div class="memory-status-card status-overdue">
                <div class="memory-status-number">{{ memoryCurveStatus.overdue || 0 }}</div>
                <div class="memory-status-text">已逾期</div>
              </div>
            </el-col>
          </el-row>

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
import { ref, reactive, onMounted, onUnmounted, nextTick, watch } from 'vue'
import * as echarts from 'echarts'
import { ElMessage } from 'element-plus'
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
const memoryCurveStatus = ref({ due: 0, on_track: 0, overdue: 0 })

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
const knowledgeGraphRef = ref(null)
const inputOutputChartRef = ref(null)

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
let knowledgeGraph = null
let inputOutputChart = null
let isResizing = false

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

    // 更新知识图谱
    if (data.knowledge_graph) {
      updateKnowledgeGraph(data.knowledge_graph)
    } else if (data.weak_points && data.weak_points.length > 0) {
      // 从薄弱点构造知识图谱数据
      const graphData = constructKnowledgeGraph(data.weak_points)
      updateKnowledgeGraph(graphData)
    }
  } catch (error) {
    console.error('获取概览数据失败:', error)
    ElMessage.error('获取概览数据失败')
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
    ElMessage.error('获取薄弱点数据失败')
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

    // 更新投入产出分析图
    if (data.input_output_analysis) {
      updateInputOutputChart(data.input_output_analysis)
    } else {
      // 根据学习时间与正确率数据构造投入产出数据
      const studyTime = data.subject_time || {}
      const accuracyBySubject = data.accuracy_by_subject || {}
      const inputOutputData = Object.keys(studyTime).map(subject => ({
        study_time: studyTime[subject] || 0,
        accuracy_improvement: accuracyBySubject[subject] || 0,
        subject: subject,
      }))
      if (inputOutputData.length > 0) {
        updateInputOutputChart(inputOutputData)
      }
    }
  } catch (error) {
    console.error('获取学习行为数据失败:', error)
    ElMessage.error('获取学习行为数据失败')
  }
}

// 获取单词掌握数据
const fetchWordMasteryData = async () => {
  try {
    const res = await learningAnalysisApi.getFullStats()
    const data = res.data || {}

    // 低准确率单词
    lowAccuracyWords.value = data.low_accuracy_words || []

    // 记忆曲线状态
    if (data.memory_curve_status) {
      memoryCurveStatus.value = data.memory_curve_status
    } else {
      // 从单词复习数据计算记忆曲线状态
      const wordReviewData = data.word_review_stats || {}
      memoryCurveStatus.value = {
        due: wordReviewData.due_count || 0,
        on_track: wordReviewData.on_track_count || 0,
        overdue: wordReviewData.overdue_count || 0,
      }
    }

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
    ElMessage.error('获取单词掌握数据失败')
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
    ElMessage.error('获取LLM建议失败')
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

  // 知识图谱
  if (knowledgeGraphRef.value) {
    knowledgeGraph = echarts.init(knowledgeGraphRef.value)
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

  // 投入产出分析图
  if (inputOutputChartRef.value) {
    inputOutputChart = echarts.init(inputOutputChartRef.value)
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

// 更新学习频率热力图（日历形式）
const updateLearningHeatmap = (data) => {
  if (!learningHeatmap) return

  // 转换数据为 [date, count] 格式
  const heatmapData = Object.entries(data).map(([date, count]) => [date, count])

  if (heatmapData.length === 0) {
    heatmapData.push([new Date().toISOString().split('T')[0], 0])
  }

  // 获取日期范围
  const dates = heatmapData.map(d => d[0])
  const minDate = dates.length > 0 ? new Date(Math.min(...dates.map(d => new Date(d).getTime()))) : new Date()
  const maxDate = dates.length > 0 ? new Date(Math.max(...dates.map(d => new Date(d).getTime()))) : new Date()

  // 补齐整月显示
  const startDate = new Date(minDate)
  startDate.setDate(1)

  const endDate = new Date(maxDate)
  endDate.setMonth(endDate.getMonth() + 1, 0)

  const cellSize = 15
  const calendarWidth = cellSize * 7 + 40
  const monthsCount = (endDate.getFullYear() - startDate.getFullYear()) * 12 + endDate.getMonth() - startDate.getMonth() + 1

  learningHeatmap.setOption({
    tooltip: {
      formatter: (params) => {
        const date = params.data[0]
        const value = params.data[1]
        return `${date}<br/>学习题数: ${value} 题`
      },
    },
    visualMap: {
      min: 0,
      max: Math.max(...heatmapData.map(d => d[1]), 10),
      calculable: false,
      orient: 'horizontal',
      left: 'center',
      bottom: '0%',
      inRange: {
        color: ['#ebedee', '#c6e48b', '#7bc96f', '#239a3b', '#196127'],
      },
      textStyle: { fontSize: 11 },
    },
    calendar: {
      top: 30,
      left: 50,
      cellSize: [cellSize, cellSize],
      range: [startDate.toISOString().split('T')[0], endDate.toISOString().split('T')[0]],
      itemStyle: { borderWidth: 2, borderColor: '#fff' },
      dayLabel: {
        firstDay: 1,
        nameMap: ['日', '一', '二', '三', '四', '五', '六'],
        fontSize: 10,
      },
      monthLabel: {
        show: true,
        nameMap: 'ZH',
        fontSize: 11,
        margin: 5,
      },
      yearLabel: { show: false },
    },
    series: [{
      type: 'heatmap',
      coordinateSystem: 'calendar',
      data: heatmapData,
      label: { show: false },
      emphasis: {
        itemStyle: { shadowBlur: 5, shadowColor: 'rgba(0, 0, 0, 0.3)' },
      },
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

// 更新知识图谱
const updateKnowledgeGraph = (data) => {
  if (!knowledgeGraph) return

  const { nodes = [], links = [] } = data

  // 如果没有传入nodes和links，尝试从其他格式构造
  if (nodes.length === 0 && links.length === 0) {
    return
  }

  knowledgeGraph.setOption({
    tooltip: {
      trigger: 'item',
      formatter: (params) => {
        if (params.dataType === 'node') {
          return `${params.name}<br/>掌握度: ${params.value || 0}%`
        }
        return `${params.source} → ${params.target}`
      },
    },
    series: [{
      type: 'graph',
      layout: 'force',
      symbolSize: 50,
      roam: true,
      draggable: true,
      label: {
        show: true,
        formatter: '{b}',
        fontSize: 12,
      },
      edgeSymbol: ['circle', 'arrow'],
      edgeSymbolSize: [4, 10],
      data: nodes.map(n => ({
        name: n.name || n.id,
        value: n.value || n.mastery || 50,
        symbolSize: Math.max(30, (n.value || n.mastery || 50) * 0.6),
        itemStyle: {
          color: getMasteryColor(n.value || n.mastery || 50),
        },
      })),
      links: links.map(l => ({
        source: l.source,
        target: l.target,
        lineStyle: { width: 2, color: '#999' },
      })),
      lineStyle: { width: 2, curveness: 0.3 },
      emphasis: {
        focus: 'adjacency',
        lineStyle: { width: 4 },
      },
      force: {
        repulsion: 200,
        gravity: 0.1,
        edgeLength: [80, 150],
        layoutAnimation: true,
      },
    }],
  })
}

// 根据掌握度获取颜色
const getMasteryColor = (mastery) => {
  if (mastery >= 80) return '#67c23a'
  if (mastery >= 60) return '#e6a23c'
  if (mastery >= 40) return '#f56c6c'
  return '#909399'
}

// 构造知识图谱数据
const constructKnowledgeGraph = (weakPoints) => {
  const nodes = weakPoints.slice(0, 12).map((wp, i) => ({
    id: String(i),
    name: wp.knowledge_point || wp.name || `知识点${i + 1}`,
    mastery: wp.accuracy_rate || (100 - (wp.error_count || 0) * 5),
  }))

  // 构造知识点之间的关联（相邻知识点相连）
  const links = []
  for (let i = 0; i < nodes.length - 1; i++) {
    if (Math.random() > 0.4) {
      links.push({ source: String(i), target: String(i + 1) })
    }
    if (i < nodes.length - 2 && Math.random() > 0.6) {
      links.push({ source: String(i), target: String(i + 2) })
    }
  }

  return { nodes, links }
}

// 更新投入产出分析图
const updateInputOutputChart = (data) => {
  if (!inputOutputChart) return

  const chartData = Array.isArray(data) ? data : Object.entries(data).map(([subject, val]) => ({
    subject,
    study_time: val.study_time || val.time || 0,
    accuracy_improvement: val.accuracy_improvement || val.accuracy || 0,
  }))

  inputOutputChart.setOption({
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'cross' },
      formatter: (params) => {
        const item = params[0]
        const dataItem = chartData[item.dataIndex]
        return `${dataItem.subject || '科目'}<br/>学习时间: ${dataItem.study_time} 分钟<br/>正确率提升: ${dataItem.accuracy_improvement}%`
      },
    },
    grid: { left: '3%', right: '8%', bottom: '3%', top: '10%', containLabel: true },
    xAxis: {
      type: 'value',
      name: '学习时间 (分钟)',
      axisLabel: { formatter: '{value} min' },
    },
    yAxis: {
      type: 'value',
      name: '正确率提升 (%)',
      axisLabel: { formatter: '{value}%' },
      min: 0,
      max: 100,
    },
    series: [{
      type: 'scatter',
      symbolSize: 20,
      data: chartData.map(d => [d.study_time, d.accuracy_improvement]),
      itemStyle: {
        color: new echarts.graphic.RadialGradient(0.5, 0.5, 0.5, [
          { offset: 0, color: 'rgba(64, 158, 255, 0.8)' },
          { offset: 1, color: 'rgba(64, 158, 255, 0.2)' },
        ]),
      },
      emphasis: {
        scale: 1.5,
        itemStyle: {
          color: new echarts.graphic.RadialGradient(0.5, 0.5, 0.5, [
            { offset: 0, color: 'rgba(103, 194, 58, 0.9)' },
            { offset: 1, color: 'rgba(103, 194, 58, 0.3)' },
          ]),
        },
      },
      markLine: {
        silent: true,
        lineStyle: { color: '#f56c6c', type: 'dashed' },
        data: [{ yAxis: 60, name: '目标提升' }],
      },
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

// 窗口resize时重绘图表（带防抖）
const handleResize = () => {
  if (isResizing) return
  isResizing = true

  overviewPieChart?.resize()
  overviewLineChart?.resize()
  knowledgeGraph?.resize()
  weakPointBarChart?.resize()
  errorTypePieChart?.resize()
  accuracyLineChart?.resize()
  learningHeatmap?.resize()
  inputOutputChart?.resize()
  subjectTimeBarChart?.resize()
  difficultyBarChart?.resize()
  wordMasteryPieChart?.resize()
  wordCountBarChart?.resize()

  setTimeout(() => {
    isResizing = false
  }, 100)
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

// 清理函数 - 防止内存泄漏
onUnmounted(() => {
  // 移除resize监听
  window.removeEventListener('resize', handleResize)
  // 销毁所有图表实例
  overviewPieChart?.dispose()
  overviewLineChart?.dispose()
  weakPointBarChart?.dispose()
  errorTypePieChart?.dispose()
  accuracyLineChart?.dispose()
  learningHeatmap?.dispose()
  subjectTimeBarChart?.dispose()
  difficultyBarChart?.dispose()
  wordMasteryPieChart?.dispose()
  wordCountBarChart?.dispose()
  inputOutputChart?.dispose()
  knowledgeGraph?.dispose()
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

/* 记忆曲线状态卡片 */
.memory-status-card {
  border-radius: 12px;
  padding: 20px;
  text-align: center;
  color: #fff;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.memory-status-number {
  font-size: 36px;
  font-weight: bold;
  line-height: 1;
}

.memory-status-text {
  font-size: 14px;
  margin-top: 8px;
  opacity: 0.9;
}

.status-due {
  background: linear-gradient(135deg, #e6a23c 0%, #f5a623 100%);
}

.status-on-track {
  background: linear-gradient(135deg, #67c23a 0%, #85ce61 100%);
}

.status-overdue {
  background: linear-gradient(135deg, #f56c6c 0%, #f78989 100%);
}
</style>
