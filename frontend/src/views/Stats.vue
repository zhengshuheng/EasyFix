<template>
  <div class="stats">
    <!-- 顶部统计卡片 -->
    <el-row :gutter="20" class="stat-cards-row">
      <el-col :span="6">
        <div class="stat-card gradient-red">
          <div class="stat-number">{{ stats.total_questions }}</div>
          <div class="stat-text">错题总数</div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card gradient-orange">
          <div class="stat-number">{{ stats.total_subjects }}</div>
          <div class="stat-text">学科数</div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card gradient-purple">
          <div class="stat-number">{{ stats.total_error_books }}</div>
          <div class="stat-text">错题本数</div>
        </div>
      </el-col>
      <el-col :span="6">
        <div class="stat-card gradient-blue">
          <div class="stat-number">{{ averageDifficulty }}</div>
          <div class="stat-text">平均难度</div>
        </div>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span class="card-title">难度分布</span>
            </div>
          </template>
          <div class="gauge-container">
            <v-chart :option="difficultyGaugeOption" autoresize style="height: 200px" />
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card class="chart-card">
          <template #header>
            <div class="card-header">
              <span class="card-title">错误类型分布</span>
            </div>
          </template>
          <div class="gauge-container">
            <v-chart :option="errorTypeGaugeOption" autoresize style="height: 200px" />
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" style="margin-top: 20px">
      <el-col :span="24">
        <el-card>
          <template #header>
            <span>按学科统计</span>
          </template>
          <el-table :data="stats.by_subject || []" stripe style="width: 100%">
            <el-table-column prop="subject_name" label="学科" />
            <el-table-column prop="question_count" label="错题数量" />
            <el-table-column label="错误类型分布">
              <template #default="{ row }">
                <div v-if="Object.keys(row.error_type_counts || {}).length">
                  <el-tag
                    v-for="(count, type) in row.error_type_counts"
                    :key="type"
                    :style="{ marginRight: '5px', marginBottom: '5px', fontSize: '14px' }"
                  >
                    {{ type }}: {{ count }}
                  </el-tag>
                </div>
                <span v-else>暂无</span>
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
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, LegendComponent } from 'echarts/components'

use([CanvasRenderer, PieChart, TitleComponent, TooltipComponent, LegendComponent])

const stats = ref({
  total_questions: 0,
  total_subjects: 0,
  total_error_books: 0,
  difficulty_distribution: {},
  error_type_distribution: {},
  by_subject: [],
})

const averageDifficulty = computed(() => {
  const dist = stats.value.difficulty_distribution || {}
  const entries = Object.entries(dist)
  if (!entries.length) return '0'

  let totalScore = 0
  let totalCount = 0
  for (const [level, count] of entries) {
    totalScore += parseInt(level) * count
    totalCount += count
  }
  return totalCount ? (totalScore / totalCount).toFixed(1) : '0'
})

const totalCount = computed(() => {
  return Object.values(stats.value.difficulty_distribution || {}).reduce((a, b) => a + b, 0)
})

const getPercentage = (count) => {
  return totalCount.value ? Math.round((count / totalCount.value) * 100) : 0
}

const getDifficultyColor = (level) => {
  const colors = ['', '#67c23a', '#85ce61', '#e6a23c', '#f56c6c', '#f78989']
  return colors[parseInt(level)] || '#409eff'
}

// 难度仪表盘配置
const difficultyGaugeOption = computed(() => {
  const dist = stats.value.difficulty_distribution || {}
  const entries = Object.entries(dist)
  const total = entries.reduce((sum, [, v]) => sum + v, 0)

  const colors = ['#67c23a', '#85ce61', '#e6a23c', '#f56c6c', '#f78989']
  const data = entries.map(([level, count]) => ({
    name: `难度${level}`,
    value: count,
    itemStyle: { color: colors[parseInt(level) - 1] || '#409eff' }
  }))

  return {
    tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
    series: [{
      type: 'pie',
      radius: ['50%', '70%'],
      center: ['50%', '60%'],
      startAngle: 180,
      endAngle: 0,
      avoidLabelOverlap: true,
      itemStyle: { borderRadius: 8, borderColor: '#fff', borderWidth: 2 },
      label: { show: false },
      emphasis: { scaleSize: 8 },
      labelLine: { show: false },
      data: data.length ? data : [{ name: '无数据', value: 0 }]
    }]
  }
})

// 错误类型仪表盘配置
const errorTypeGaugeOption = computed(() => {
  const dist = stats.value.error_type_distribution || {}
  const entries = Object.entries(dist)

  const colors = ['#5470c6', '#91cc75', '#fac858', '#ee6666', '#73c0de', '#3ba272', '#fc8452', '#9a60b4']
  const data = entries.map(([type, count], i) => ({
    name: type,
    value: count,
    itemStyle: { color: colors[i % colors.length] }
  }))

  return {
    tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
    series: [{
      type: 'pie',
      radius: ['50%', '70%'],
      center: ['50%', '60%'],
      startAngle: 180,
      endAngle: 0,
      avoidLabelOverlap: true,
      itemStyle: { borderRadius: 8, borderColor: '#fff', borderWidth: 2 },
      label: { show: false },
      emphasis: { scaleSize: 8 },
      labelLine: { show: false },
      data: data.length ? data : [{ name: '无数据', value: 0 }]
    }]
  }
})

const fetchStats = async () => {
  try {
    const { data } = await statsApi.getSummary()
    stats.value = data
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

onMounted(fetchStats)
</script>

<style scoped>
.stats {
  max-width: 1200px;
  margin: 0 auto;
}

.stat-cards-row {
  margin-bottom: 20px;
}

.stat-card {
  border-radius: 16px;
  padding: 28px 20px;
  text-align: center;
  color: #fff;
  box-shadow: 0 4px 16px rgba(0,0,0,0.1);
}

.gradient-red { background: linear-gradient(135deg, #ff6b6b 0%, #ee5a5a 100%); }
.gradient-orange { background: linear-gradient(135deg, #ffa502 0%, #ff9500 100%); }
.gradient-purple { background: linear-gradient(135deg, #8e44ad 0%, #7d3c98 100%); }
.gradient-blue { background: linear-gradient(135deg, #409eff 0%, #3c8af0 100%); }

.stat-number {
  font-size: 48px;
  font-weight: bold;
  line-height: 1;
  text-shadow: 0 2px 8px rgba(0,0,0,0.15);
}

.stat-text {
  font-size: 14px;
  margin-top: 10px;
  opacity: 0.9;
}

.chart-container {
  padding: 10px;
}

.bar-item {
  display: flex;
  align-items: center;
  margin-bottom: 15px;
}

.bar-label {
  width: 80px;
  font-size: 14px;
}

.bar-wrapper {
  flex: 1;
  height: 20px;
  background-color: #f0f0f0;
  border-radius: 10px;
  overflow: hidden;
  margin: 0 10px;
}

.bar {
  height: 100%;
  border-radius: 10px;
  transition: width 0.3s ease;
}

.bar-value {
  width: 80px;
  text-align: right;
  font-size: 14px;
  color: #666;
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

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-title {
  color: #fff;
  font-size: 15px;
  font-weight: 600;
}

.gauge-container {
  padding: 10px 0;
}
</style>
