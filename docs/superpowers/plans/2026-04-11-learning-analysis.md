# Learning Analysis Enhancement Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement enhanced learning analysis with full data aggregation, LLM-powered insights, and interactive charts page.

**Architecture:** Backend aggregates all learning data (questions, words, practice) into a single API endpoint, then LLM analyzes to generate structured insights. Frontend renders charts and insights in a tabbed page.

**Tech Stack:** Python FastAPI backend, Vue 3 + ECharts frontend, Anthropic LLM for analysis.

---

## File Structure

```
backend/
├── app/
│   ├── routers/
│   │   └── stats.py          # Add /api/stats/analysis endpoints
│   └── services/
│       └── learning_analysis.py  # NEW: Data aggregation & LLM analysis
frontend/
└── src/
    ├── api/
    │   └── learning_analysis.js  # NEW: API client
    └── views/
        └── LearningAnalysis.vue  # NEW: Main analysis page
```

---

## Task 1: Backend Data Aggregation Service

**Files:**
- Create: `backend/app/services/learning_analysis.py`
- Modify: `backend/app/routers/stats.py`

- [ ] **Step 1: Create learning_analysis.py with data aggregation**

```python
# backend/app/services/learning_analysis.py
"""学习分析服务 - 数据聚合"""
from sqlalchemy.orm import Session
from sqlalchemy import func, Integer
from app.models import Question, Subject, Word, WordReviewLog, PracticeSet, PracticeSetQuestion, KnowledgePoint
from app.models.tag import Tag
from typing import List, Dict, Any
from datetime import datetime, timedelta
from collections import Counter

class LearningAnalysisService:
    def __init__(self, db: Session):
        self.db = db

    def get_full_stats(self) -> Dict[str, Any]:
        """获取完整学习统计数据"""
        return {
            "question_stats": self._get_question_stats(),
            "word_stats": self._get_word_stats(),
            "practice_stats": self._get_practice_stats(),
            "knowledge_graph": self._get_knowledge_graph(),
        }

    def _get_question_stats(self) -> Dict[str, Any]:
        """获取错题统计"""
        questions = self.db.query(Question).filter(Question.deleted == False).all()

        # 难度分布
        by_difficulty = Counter([q.difficulty for q in questions if q.difficulty])

        # 错误类型分布
        error_types = Counter()
        for q in questions:
            if q.error_type:
                for et in q.error_type.split(','):
                    et = et.strip()
                    if et:
                        error_types[et] += 1

        # 知识点错误排行
        kp_errors = Counter()
        for q in questions:
            if q.knowledge_point:
                kp_errors[q.knowledge_point] += 1
        top_kp = [{"point": k, "count": v} for k, v in kp_errors.most_common(10)]

        # 复习效果
        not_reviewed = sum(1 for q in questions if (q.review_count or 0) == 0)
        reviewed_once = sum(1 for q in questions if q.review_count == 1)
        reviewed_multiple = sum(1 for q in questions if (q.review_count or 0) > 1)

        # 正确率趋势
        accuracy_trend = self._get_question_accuracy_trend()

        return {
            "total": len(questions),
            "by_difficulty": dict(by_difficulty),
            "by_error_type": dict(error_types),
            "top_error_knowledge_points": top_kp,
            "review_effectiveness": {
                "not_reviewed": not_reviewed,
                "reviewed_once": reviewed_once,
                "reviewed_multiple": reviewed_multiple,
            },
            "accuracy_trend": accuracy_trend,
        }

    def _get_question_accuracy_trend(self) -> List[Dict]:
        """获取错题正确率趋势"""
        from app.models import PracticeSetQuestion
        logs = (
            self.db.query(
                func.date(PracticeSet.created_at).label('date'),
                func.sum(func.cast(PracticeSetQuestion.is_correct, Integer)).label('correct'),
                func.count(PracticeSetQuestion.id).label('total')
            )
            .join(PracticeSet, PracticeSet.id == PracticeSetQuestion.practice_set_id)
            .filter(
                PracticeSet.deleted == False,
                PracticeSet.source_type == 'question',
                PracticeSet.reviewed == True,
                PracticeSetQuestion.is_correct.isnot(None)
            )
            .group_by(func.date(PracticeSet.created_at))
            .order_by(func.date(PracticeSet.created_at))
            .all()
        )

        cumulative_correct = 0
        cumulative_total = 0
        trend = []
        for log in logs:
            cumulative_correct += log.correct or 0
            cumulative_total += log.total or 0
            accuracy = round(cumulative_correct / cumulative_total * 100, 1) if cumulative_total > 0 else 0
            trend.append({
                "date": log.date.strftime('%Y-%m-%d') if hasattr(log.date, 'strftime') else str(log.date),
                "accuracy": accuracy
            })
        return trend

    def _get_word_stats(self) -> Dict[str, Any]:
        """获取单词统计"""
        words = self.db.query(Word).filter(Word.deleted == False).all()

        # 掌握分布
        unmastered = sum(1 for w in words if (w.review_count or 0) == 0)
        learning = sum(1 for w in words if 0 < (w.review_count or 0) <= 3)
        mastered = sum(1 for w in words if (w.review_count or 0) > 3)

        # 低准确率单词
        low_acc = []
        for w in words:
            if w.review_count and w.correct_count is not None:
                acc = w.correct_count / w.review_count * 100
                if acc < 70:
                    low_acc.append({"word": w.word, "accuracy": round(acc, 1)})

        # 记忆曲线状态
        now = datetime.now()
        due_review = sum(1 for w in words if w.next_review_at and w.next_review_at <= now)
        on_track = len(words) - due_review

        # 复习频率趋势
        frequency = self._get_word_frequency_trend()

        return {
            "total": len(words),
            "mastery_distribution": {
                "unmastered": unmastered,
                "learning": learning,
                "mastered": mastered,
            },
            "low_accuracy_words": low_acc[:20],
            "memory_curve_status": {
                "due_review": due_review,
                "on_track": on_track,
            },
            "frequency_trend": frequency,
        }

    def _get_word_frequency_trend(self) -> List[Dict]:
        """获取单词复习频率趋势"""
        logs = (
            self.db.query(
                func.date(WordReviewLog.reviewed_at).label('date'),
                func.count(WordReviewLog.id).label('count')
            )
            .filter(WordReviewLog.deleted == False)
            .group_by(func.date(WordReviewLog.reviewed_at))
            .order_by(func.date(WordReviewLog.reviewed_at))
            .all()
        )
        return [
            {"date": log.date.strftime('%Y-%m-%d') if hasattr(log.date, 'strftime') else str(log.date), "count": log.count}
            for log in logs
        ]

    def _get_practice_stats(self) -> Dict[str, Any]:
        """获取练习统计"""
        practice_sets = self.db.query(PracticeSet).filter(
            PracticeSet.deleted == False
        ).all()

        # 频率热力图（按星期）
        weekday_counts = Counter()
        for ps in practice_sets:
            weekday = ps.created_at.strftime('%a')
            weekday_counts[weekday] += 1

        # 正确率趋势
        accuracy_trend = self._get_practice_accuracy_trend()

        return {
            "total_practices": len(practice_sets),
            "frequency_heatmap": dict(weekday_counts),
            "accuracy_trend": accuracy_trend,
        }

    def _get_practice_accuracy_trend(self) -> List[Dict]:
        """获取练习正确率趋势"""
        from app.models import WordReviewSession
        sessions = (
            self.db.query(WordReviewSession)
            .filter(WordReviewSession.deleted == False)
            .order_by(WordReviewSession.reviewed_at)
            .all()
        )

        cumulative_correct = 0
        cumulative_total = 0
        trend = []
        for s in sessions:
            cumulative_correct += s.correct_count or 0
            cumulative_total += s.total_count or 0
            accuracy = round(cumulative_correct / cumulative_total * 100, 1) if cumulative_total > 0 else 0
            trend.append({
                "date": s.reviewed_at.strftime('%Y-%m-%d') if hasattr(s.reviewed_at, 'strftime') else str(s.reviewed_at),
                "accuracy": accuracy
            })
        return trend

    def _get_knowledge_graph(self) -> Dict[str, Any]:
        """获取知识点关联图"""
        # 获取所有知识点
        kps = self.db.query(KnowledgePoint).filter(
            KnowledgePoint.deleted == False
        ).all()

        nodes = []
        edges = []

        # 获取每个知识点的错误次数
        kp_error_count = Counter()
        questions = self.db.query(Question).filter(
            Question.deleted == False,
            Question.knowledge_point.isnot(None)
        ).all()
        for q in questions:
            if q.knowledge_point:
                kp_error_count[q.knowledge_point] += 1

        # 构建节点
        for kp in kps:
            nodes.append({
                "id": str(kp.id),
                "name": kp.name,
                "error_count": kp_error_count.get(kp.name, 0),
                "category": kp.subject_id or 0
            })

        return {"nodes": nodes, "edges": edges}
```

- [ ] **Step 2: Add stats router endpoints**

Modify `backend/app/routers/stats.py` - add to end of file:

```python
from app.services.learning_analysis import LearningAnalysisService

@router.get("/analysis/full")
def get_full_analysis(db: Session = Depends(get_db)):
    """获取完整学习分析数据"""
    service = LearningAnalysisService(db)
    return service.get_full_stats()
```

- [ ] **Step 3: Test the API**

Run: `curl http://localhost:8000/api/stats/analysis/full`
Expected: JSON with question_stats, word_stats, practice_stats, knowledge_graph

- [ ] **Step 4: Commit**

```bash
git add backend/app/services/learning_analysis.py backend/app/routers/stats.py
git commit -m "feat(stats): add full learning analysis data aggregation API"
```

---

## Task 2: LLM Analysis Service

**Files:**
- Modify: `backend/app/services/learning_analysis.py`
- Modify: `backend/app/routers/stats.py`

- [ ] **Step 1: Add LLM analysis method to LearningAnalysisService**

Add to `backend/app/services/learning_analysis.py`:

```python
def analyze_with_llm(self, stats: Dict[str, Any]) -> Dict[str, Any]:
    """使用LLM分析学习数据，生成结构化建议"""
    from app.services.llm import LLMService

    prompt = self._build_analysis_prompt(stats)

    llm = LLMService()
    response = llm.analyze_learning_data(prompt)

    return self._parse_llm_response(response)

def _build_analysis_prompt(self, stats: Dict[str, Any]) -> str:
    """构建分析提示词"""
    q = stats.get("question_stats", {})
    w = stats.get("word_stats", {})
    p = stats.get("practice_stats", {})

    prompt = f"""基于以下学习数据，生成结构化分析报告：

## 错题统计
- 总数: {q.get('total', 0)}
- 难度分布: {q.get('by_difficulty', {})}
- 错误类型: {q.get('by_error_type', {})}
- 高频错误知识点: {q.get('top_error_knowledge_points', [])}
- 复习效果: 未复习{q.get('review_effectiveness', {}).get('not_reviewed', 0)}题, 已复习多次{q.get('review_effectiveness', {}).get('reviewed_multiple', 0)}题

## 单词统计
- 总数: {w.get('total', 0)}
- 掌握分布: 未掌握{w.get('mastery_distribution', {}).get('unmastered', 0)}, 学习中{w.get('mastery_distribution', {}).get('learning', 0)}, 已牢记{w.get('mastery_distribution', {}).get('mastered', 0)}
- 待复习: {w.get('memory_curve_status', {}).get('due_review', 0)}个
- 低准确率单词: {w.get('low_accuracy_words', [])[:5]}

## 练习统计
- 总练习次数: {p.get('total_practices', 0)}
- 周频率: {p.get('frequency_heatmap', {})}

请生成JSON格式的分析报告，包含：
{{
  "weak_points": [{{"point": "知识点名", "reason": "原因分析", "suggestion": "改进建议"}}],  // TOP3薄弱点
  "trends": {{"pattern": "趋势描述", "cause": "原因分析", "prediction": "趋势预测"}},
  "suggestions": [{{"type": "练习|记忆|复习|策略", "content": "建议内容", "priority": 1-3}}],  // 3-5条建议
  "learning_plan": {{"daily_time": "每日建议时长", "focus_areas": ["重点领域"], "priority_order": ["优先级排序"]}}
}}

只返回JSON，不要其他内容。"""
    return prompt

def _parse_llm_response(self, response: str) -> Dict[str, Any]:
    """解析LLM响应"""
    import json
    import re

    # 提取JSON
    match = re.search(r'\{[\s\S]*\}', response)
    if match:
        try:
            return json.loads(match.group())
        except json.JSONDecodeError:
            return {"error": "解析失败", "raw": response}
    return {"error": "未找到JSON", "raw": response}
```

- [ ] **Step 2: Add LLM method to LLMService**

Modify `backend/app/services/llm.py` - add method:

```python
def analyze_learning_data(self, prompt: str) -> str:
    """分析学习数据"""
    response = self._client.messages.create(
        model=self._get_config("model", "claude-sonnet-4-20250514"),
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )
    return response.content[0].text
```

- [ ] **Step 3: Add LLM router endpoint**

Modify `backend/app/routers/stats.py`:

```python
@router.get("/analysis/llm")
def get_llm_analysis(db: Session = Depends(get_db)):
    """获取LLM学习分析"""
    service = LearningAnalysisService(db)
    stats = service.get_full_stats()
    analysis = service.analyze_with_llm(stats)
    return analysis
```

- [ ] **Step 4: Commit**

```bash
git add backend/app/services/learning_analysis.py backend/app/services/llm.py backend/app/routers/stats.py
git commit -m "feat(stats): add LLM-powered learning analysis"
```

---

## Task 3: Frontend API Client

**Files:**
- Create: `frontend/src/api/learning_analysis.js`

- [ ] **Step 1: Create API client**

```javascript
// frontend/src/api/learning_analysis.js
import api from './question.js'

export const learningAnalysisApi = {
  // 获取完整分析数据
  getFullStats() {
    return api.get('/stats/analysis/full')
  },

  // 获取LLM分析
  getLlmAnalysis() {
    return api.get('/stats/analysis/llm')
  },
}

export default learningAnalysisApi
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/api/learning_analysis.js
git commit -m "feat(api: add learning analysis API client"
```

---

## Task 4: Frontend LearningAnalysis Page

**Files:**
- Create: `frontend/src/views/LearningAnalysis.vue`
- Modify: `frontend/src/router/index.js` (add route)

- [ ] **Step 1: Create LearningAnalysis.vue**

```vue
<template>
  <div class="learning-analysis">
    <el-card v-loading="loading">
      <template #header>
        <div class="card-header">
          <span>学习分析</span>
          <el-button type="primary" @click="refreshData">
            <el-icon><Refresh /></el-icon>
            刷新
          </el-button>
        </div>
      </template>

      <el-tabs v-model="activeTab">
        <!-- 概览 -->
        <el-tab-pane label="概览" name="overview">
          <el-row :gutter="20">
            <el-col :span="6">
              <div class="stat-card">
                <div class="stat-value">{{ overviewStats.healthScore }}</div>
                <div class="stat-label">健康度</div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-card">
                <div class="stat-value">{{ overviewStats.weakPoints }}</div>
                <div class="stat-label">薄弱点</div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-card">
                <div class="stat-value">{{ overviewStats.suggestions }}</div>
                <div class="stat-label">建议</div>
              </div>
            </el-col>
            <el-col :span="6">
              <div class="stat-card">
                <div class="stat-value">{{ overviewStats.accuracy }}%</div>
                <div class="stat-label">整体正确率</div>
              </div>
            </el-col>
          </el-row>
        </el-tab-pane>

        <!-- 薄弱点分析 -->
        <el-tab-pane label="薄弱点分析" name="weakpoints">
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="chart-container">
                <h4>知识点错误排行</h4>
                <div ref="knowledgeChart" style="height: 300px"></div>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="chart-container">
                <h4>错误类型分布</h4>
                <div ref="errorTypeChart" style="height: 300px"></div>
              </div>
            </el-col>
          </el-row>
          <el-row :gutter="20" style="margin-top: 20px">
            <el-col :span="24">
              <div class="chart-container">
                <h4>知识图谱</h4>
                <div ref="knowledgeGraphChart" style="height: 400px"></div>
              </div>
            </el-col>
          </el-row>
        </el-tab-pane>

        <!-- 学习行为 -->
        <el-tab-pane label="学习行为" name="behavior">
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="chart-container">
                <h4>正确率趋势</h4>
                <div ref="accuracyTrendChart" style="height: 300px"></div>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="chart-container">
                <h4>学习频率热力图</h4>
                <div ref="frequencyChart" style="height: 300px"></div>
              </div>
            </el-col>
          </el-row>
        </el-tab-pane>

        <!-- 单词掌握 -->
        <el-tab-pane label="单词掌握" name="words">
          <el-row :gutter="20">
            <el-col :span="12">
              <div class="chart-container">
                <h4>掌握率分布</h4>
                <div ref="masteryChart" style="height: 300px"></div>
              </div>
            </el-col>
            <el-col :span="12">
              <div class="chart-container">
                <h4>复习待办</h4>
                <div class="due-review">
                  <el-tag type="warning" size="large">
                    待复习: {{ wordStats.dueReview }}个
                  </el-tag>
                </div>
              </div>
            </el-col>
          </el-row>
          <el-row :gutter="20" style="margin-top: 20px">
            <el-col :span="24">
              <h4>低准确率单词</h4>
              <el-tag v-for="w in wordStats.lowAccuracyWords" :key="w.word" type="danger" style="margin: 5px">
                {{ w.word }} ({{ w.accuracy }}%)
              </el-tag>
            </el-col>
          </el-row>
        </el-tab-pane>

        <!-- 改进建议 -->
        <el-tab-pane label="改进建议" name="suggestions">
          <el-card v-if="llmAnalysis.loading" loading>AI分析中...</el-card>
          <div v-else-if="llmAnalysis.data">
            <el-divider>薄弱点</el-divider>
            <el-card v-for="(wp, idx) in llmAnalysis.data.weak_points" :key="idx" class="suggestion-card">
              <h4>{{ wp.point }}</h4>
              <p>{{ wp.reason }}</p>
              <el-tag type="success">{{ wp.suggestion }}</el-tag>
            </el-card>

            <el-divider>学习建议</el-divider>
            <el-card v-for="(s, idx) in llmAnalysis.data.suggestions" :key="idx" class="suggestion-card">
              <el-tag :type="getSuggestionType(s.type)">{{ s.type }}</el-tag>
              <p>{{ s.content }}</p>
            </el-card>

            <el-divider>学习计划</el-divider>
            <el-card v-if="llmAnalysis.data.learning_plan">
              <p><strong>每日时长:</strong> {{ llmAnalysis.data.learning_plan.daily_time }}</p>
              <p><strong>重点领域:</strong> {{ llmAnalysis.data.learning_plan.focus_areas?.join(', ') }}</p>
            </el-card>
          </div>
          <el-empty v-else description="暂无分析数据" />
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted, nextTick } from 'vue'
import { ElMessage } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'
import * as echarts from 'echarts'
import { learningAnalysisApi } from '@/api/learning_analysis'

const loading = ref(false)
const activeTab = ref('overview')

// 数据
const overviewStats = reactive({
  healthScore: 0,
  weakPoints: 0,
  suggestions: 0,
  accuracy: 0
})

const questionStats = ref({})
const wordStats = ref({
  dueReview: 0,
  lowAccuracyWords: []
})
const practiceStats = ref({})
const knowledgeGraph = ref({ nodes: [], edges: [] })

const llmAnalysis = reactive({
  loading: false,
  data: null
})

// 图表引用
const knowledgeChart = ref(null)
const errorTypeChart = ref(null)
const accuracyTrendChart = ref(null)
const frequencyChart = ref(null)
const masteryChart = ref(null)
const knowledgeGraphChart = ref(null)

// 获取数据
const refreshData = async () => {
  loading.value = true
  try {
    const { data } = await learningAnalysisApi.getFullStats()
    questionStats.value = data.question_stats || {}
    wordStats.value = {
      ...data.word_stats || {},
      dueReview: data.word_stats?.memory_curve_status?.due_review || 0,
      lowAccuracyWords: data.word_stats?.low_accuracy_words || []
    }
    practiceStats.value = data.practice_stats || {}
    knowledgeGraph.value = data.knowledge_graph || { nodes: [], edges: [] }

    // 更新概览
    const q = questionStats.value
    overviewStats.accuracy = q.accuracy_trend?.slice(-1)[0]?.accuracy || 0
    overviewStats.weakPoints = q.top_error_knowledge_points?.length || 0

    // 渲染图表
    await nextTick()
    renderCharts()

    // 获取LLM分析
    fetchLlmAnalysis()
  } catch (error) {
    ElMessage.error('获取数据失败')
  } finally {
    loading.value = false
  }
}

const fetchLlmAnalysis = async () => {
  llmAnalysis.loading = true
  try {
    const { data } = await learningAnalysisApi.getLlmAnalysis()
    llmAnalysis.data = data
    overviewStats.suggestions = data.suggestions?.length || 0
    overviewStats.healthScore = calculateHealthScore()
  } catch (error) {
    console.error('LLM分析失败:', error)
  } finally {
    llmAnalysis.loading = false
  }
}

const calculateHealthScore = () => {
  const acc = overviewStats.accuracy
  if (acc >= 80) return 90
  if (acc >= 60) return 70
  return 50
}

const getSuggestionType = (type) => {
  const map = { '练习': 'primary', '记忆': 'success', '复习': 'warning', '策略': 'info' }
  return map[type] || 'info'
}

// 渲染图表
const renderCharts = () => {
  renderKnowledgeChart()
  renderErrorTypeChart()
  renderAccuracyTrendChart()
  renderFrequencyChart()
  renderMasteryChart()
  renderKnowledgeGraph()
}

const renderKnowledgeChart = () => {
  if (!knowledgeChart.value) return
  const chart = echarts.init(knowledgeChart.value)
  const data = questionStats.value.top_error_knowledge_points || []
  chart.setOption({
    tooltip: {},
    xAxis: { type: 'value' },
    yAxis: { type: 'category', data: data.map(d => d.point) },
    series: [{
      type: 'bar',
      data: data.map(d => d.count),
      itemStyle: { color: '#f56c6c' }
    }]
  })
}

const renderErrorTypeChart = () => {
  if (!errorTypeChart.value) return
  const chart = echarts.init(errorTypeChart.value)
  const data = questionStats.value.by_error_type || {}
  chart.setOption({
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      data: Object.entries(data).map(([name, value]) => ({ name, value }))
    }]
  })
}

const renderAccuracyTrendChart = () => {
  if (!accuracyTrendChart.value) return
  const chart = echarts.init(accuracyTrendChart.value)
  const trend = questionStats.value.accuracy_trend || []
  chart.setOption({
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: trend.map(t => t.date) },
    yAxis: { type: 'value', min: 0, max: 100 },
    series: [{
      type: 'line',
      data: trend.map(t => t.accuracy),
      smooth: true,
      areaStyle: {}
    }]
  })
}

const renderFrequencyChart = () => {
  if (!frequencyChart.value) return
  const chart = echarts.init(frequencyChart.value)
  const heatmap = practiceStats.value.frequency_heatmap || {}
  const days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
  chart.setOption({
    tooltip: {},
    xAxis: { type: 'category', data: days },
    yAxis: { type: 'value' },
    series: [{
      type: 'bar',
      data: days.map(d => heatmap[d] || 0),
      itemStyle: { color: '#409eff' }
    }]
  })
}

const renderMasteryChart = () => {
  if (!masteryChart.value) return
  const chart = echarts.init(masteryChart.value)
  const dist = wordStats.value.mastery_distribution || {}
  chart.setOption({
    tooltip: { trigger: 'item' },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      data: [
        { name: '未掌握', value: dist.unmastered || 0, itemStyle: { color: '#f56c6c' } },
        { name: '学习中', value: dist.learning || 0, itemStyle: { color: '#e6a23c' } },
        { name: '已牢记', value: dist.mastered || 0, itemStyle: { color: '#67c23a' } }
      ]
    }]
  })
}

const renderKnowledgeGraph = () => {
  if (!knowledgeGraphChart.value) return
  const chart = echarts.init(knowledgeGraphChart.value)
  const graph = knowledgeGraph.value
  chart.setOption({
    tooltip: {},
    series: [{
      type: 'graph',
      layout: 'force',
      nodes: graph.nodes?.map(n => ({
        name: n.name,
        value: n.error_count,
        symbolSize: Math.max(20, n.error_count * 2)
      })) || [],
      links: graph.edges?.map(e => ({ source: e.source, target: e.target })) || [],
      label: { show: true }
    }]
  })
}

onMounted(() => {
  refreshData()
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

.stat-card {
  text-align: center;
  padding: 20px;
  background: #f5f7fa;
  border-radius: 8px;
}

.stat-card .stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #409eff;
}

.stat-card .stat-label {
  font-size: 14px;
  color: #909399;
  margin-top: 5px;
}

.chart-container {
  background: #fff;
  padding: 15px;
  border-radius: 8px;
}

.chart-container h4 {
  margin: 0 0 15px 0;
  color: #606266;
}

.due-review {
  text-align: center;
  padding: 30px;
}

.suggestion-card {
  margin-bottom: 15px;
}

.suggestion-card h4 {
  margin: 0 0 10px 0;
  color: #409eff;
}

.suggestion-card p {
  margin: 10px 0;
  color: #606266;
}
</style>
```

- [ ] **Step 2: Add route to router**

Modify `frontend/src/router/index.js` - add route:

```javascript
{
  path: '/learning-analysis',
  name: 'LearningAnalysis',
  component: () => import('../views/LearningAnalysis.vue')
}
```

- [ ] **Step 3: Build and test**

Run: `cd frontend && npm run build`
Expected: Successful build

- [ ] **Step 4: Commit**

```bash
git add frontend/src/views/LearningAnalysis.vue frontend/src/api/learning_analysis.js frontend/src/router/index.js
git commit -m "feat: add LearningAnalysis page with charts and LLM insights"
```

---

## Verification

After implementation, verify:
1. Backend: `curl http://localhost:8000/api/stats/analysis/full` returns full stats
2. Frontend: `/learning-analysis` page loads with charts
3. LLM: Analysis tab shows generated suggestions
