# 统计页面重构 - 仪表盘风格实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 重构 `/stats` 页面，使用仪表盘风格：顶部大字统计卡片、两个半圆仪表盘图表、底部学科表格

**Architecture:** 纯前端Vue组件重构，使用ECharts半圆饼图实现仪表盘效果，保持现有API接口不变

**Tech Stack:** Vue 3, Element Plus, ECharts, vue-echarts

---

### Task 1: 重构 Stats.vue 顶部统计卡片

**Files:**
- Modify: `frontend/src/views/Stats.vue`

**Steps:**

- [ ] **Step 1: 替换顶部4格统计为横向大字卡片**

将原来的 `el-row :gutter="20"` 统计部分替换为：

```vue
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
```

- [ ] **Step 2: 添加CSS样式**

在 `<style scoped>` 中添加：

```css
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
```

- [ ] **Step 3: 提交**

```bash
git add frontend/src/views/Stats.vue
git commit -m "feat(stats): add gradient stat cards to top row"
```

---

### Task 2: 添加ECharts半圆仪表盘

**Files:**
- Modify: `frontend/src/views/Stats.vue`

**Steps:**

- [ ] **Step 1: 添加ECharts import**

在 `<script setup>` 开头添加：

```javascript
import VChart from 'vue-echarts'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart } from 'echarts/charts'
import { TitleComponent, TooltipComponent, LegendComponent } from 'echarts/components'

use([CanvasRenderer, PieChart, TitleComponent, TooltipComponent, LegendComponent])
```

- [ ] **Step 2: 添加仪表盘配置函数**

在 `getDifficultyColor` 函数后添加：

```javascript
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
```

- [ ] **Step 3: 替换难度分布和错误类型分布卡片为仪表盘**

将原来的两个 `el-card` (span=12 each) 替换为：

```vue
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
```

- [ ] **Step 4: 添加图表卡片CSS**

```css
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
```

- [ ] **Step 5: 提交**

```bash
git add frontend/src/views/Stats.vue
git commit -m "feat(stats): add semi-circle gauge charts for difficulty and error type distribution"
```

---

### Task 3: 美化学科表格样式

**Files:**
- Modify: `frontend/src/views/Stats.vue`

**Steps:**

- [ ] **Step 1: 更新学科表格卡片样式**

替换原来的 `el-card` (span=24) 表格部分，添加样式类：

```vue
<el-row :gutter="20" style="margin-top: 20px">
  <el-col :span="24">
    <el-card class="table-card">
      <template #header>
        <div class="card-header">
          <span class="card-title">按学科统计</span>
        </div>
      </template>
      <el-table :data="stats.by_subject || []" stripe class="subject-table">
        <!-- ... 保持现有列不变 ... -->
      </el-table>
    </el-card>
  </el-col>
</el-row>
```

- [ ] **Step 2: 添加表格样式**

```css
.table-card {
  border-radius: 16px;
  overflow: hidden;
}

.table-card :deep(.el-card__header) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 14px 20px;
  border: none;
}

.table-card .card-title {
  color: #fff;
  font-size: 15px;
  font-weight: 600;
}

.subject-table :deep(.el-table__header-wrapper th) {
  background: #f5f7fa !important;
  color: #303133;
  font-weight: 600;
}

.subject-table :deep(.el-table__row:hover td) {
  background: #f0f4ff !important;
}
```

- [ ] **Step 3: 提交**

```bash
git add frontend/src/views/Stats.vue
git commit -m "feat(stats): style subject table with consistent card styling"
```

---

**验证方式：**
1. 访问 `/stats` 页面
2. 验证顶部4个统计卡片显示正常
3. 验证难度分布和错误类型分布显示为半圆仪表盘
4. 验证学科表格样式统一

**Spec 核对：**
- [x] 顶部统计卡片 - 4个大字横向排列
- [x] 半圆仪表盘 - 难度分布和错误类型分布
- [x] 底部学科表格 - 样式统一
- [x] 卡片圆角+渐变头部
