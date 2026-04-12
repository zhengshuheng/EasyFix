# 练习集批改页面重构实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 重构练习集批改页面，将逐题批改改为列表展示，支持跳序批改，全部批改完成后可提交。

**Architecture:** 修改 `frontend/src/views/PracticeSets.vue`，重构批改弹层模板和逻辑。移除"整体批改"步骤，直接进入列表视图。支持跳序批改，提交按钮在全部批改完成后才能点击。

**Tech Stack:** Vue 3 + Element Plus + ECharts

---

## 文件结构

```
frontend/src/views/PracticeSets.vue   # 修改：批改弹层重构
```

---

## Task 1: 按钮文案修改

**Files:**
- Modify: `frontend/src/views/PracticeSets.vue:103`

- [ ] **Step 1: 修改按钮文案和颜色**

将第103行的：
```vue
<el-button type="warning" size="default" @click="markReviewed(row)" :disabled="row.reviewed">标记已复习</el-button>
```

修改为：
```vue
<el-button type="success" size="default" @click="markReviewed(row)" :disabled="row.reviewed">批改</el-button>
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/views/PracticeSets.vue
git commit -m "feat(practice-sets): change button text to '批改' with green color"
```

---

## Task 2: 重构批改弹层模板

**Files:**
- Modify: `frontend/src/views/PracticeSets.vue:124-196` (批改弹层部分)

- [ ] **Step 1: 替换批改弹层模板**

将原有的批改弹层（124-196行）：
```vue
<!-- 批改弹窗 -->
<el-dialog v-model="gradingDialogVisible" title="批改练习集" width="600px" destroy-on-close>
  <!-- 整体批改 -->
  <div v-if="gradingStep === 'overall'" class="grading-overall">
    ...
  </div>

  <!-- 逐题批改 -->
  <div v-if="gradingStep === 'detail'" class="grading-detail">
    ...
  </div>

  <!-- 图片上传（批改完成后） -->
  <div v-if="gradingStep === 'upload'" class="grading-upload">
    ...
  </div>

  <template #footer>
    ...
  </template>
</el-dialog>
```

替换为新的列表视图弹层：
```vue
<!-- 批改弹窗 -->
<el-dialog v-model="gradingDialogVisible" title="批改练习集" width="900px" destroy-on-close>
  <!-- 进度头部 -->
  <div class="grading-header">
    <div class="grading-header-left">
      <div class="grading-title">批改进度</div>
      <div class="grading-progress-text">
        <span class="text-green-600 font-bold">{{ gradedCount }}</span> / {{ currentPsQuestions.length }} 已批改
      </div>
    </div>
    <div class="grading-header-right">
      <div class="accuracy-display">
        <span class="accuracy-value">{{ getGradingAccuracy() }}%</span>
        <span class="accuracy-label">正确率</span>
      </div>
    </div>
  </div>

  <!-- 进度条 -->
  <div class="grading-progress-bar">
    <div class="progress-bar">
      <div class="progress-fill" :style="{ width: (gradedCount / currentPsQuestions.length * 100) + '%' }"></div>
    </div>
    <div class="grading-stats">
      <span class="stat-correct">✓ 正确 {{ correctCount }}</span>
      <span class="stat-wrong">✗ 错误 {{ wrongCount }}</span>
      <span class="stat-pending">○ 待批改 {{ currentPsQuestions.length - gradedCount }}</span>
    </div>
  </div>

  <!-- 题目列表 -->
  <div class="grading-question-list">
    <div
      v-for="(question, index) in currentPsQuestions"
      :key="question.question_id"
      :class="['question-row', getQuestionRowClass(question.question_id)]"
    >
      <div class="question-number">{{ index + 1 }}</div>
      <div class="question-content">
        <div class="question-text">
          <template v-if="question.original_question_text">{{ question.original_question_text }}</template>
          <template v-else-if="question.original_image">
            <el-image
              :src="'/uploads/' + question.original_image"
              fit="contain"
              style="max-width: 60px; max-height: 60px; cursor: pointer;"
              @click="previewImage(question.original_image)"
            />
          </template>
          <template v-else><span class="text-gray-400">无题目内容</span></template>
        </div>
        <div class="question-answer">
          <span class="answer-label">答案：</span>
          <span class="answer-badge">{{ question.original_answer || '-' }}</span>
        </div>
      </div>
      <div class="question-actions">
        <button
          :class="['btn-correct', { active: gradingResults[question.question_id] === true }]"
          @click="handleQuestionGrading(question.question_id, true)"
        >✓ 正确</button>
        <button
          :class="['btn-wrong', { active: gradingResults[question.question_id] === false }]"
          @click="handleQuestionGrading(question.question_id, false)"
        >✗ 错误</button>
        <el-button type="primary" @click="showQuestionDetail(question)">查看原题</el-button>
      </div>
    </div>
  </div>

  <template #footer>
    <div class="grading-footer">
      <div class="footer-stats">
        <span class="text-green-600 font-bold">{{ correctCount }}</span> 正确,
        <span class="text-red-600 font-bold">{{ wrongCount }}</span> 错误
      </div>
      <div class="footer-buttons">
        <el-button @click="gradingDialogVisible = false">返回</el-button>
        <el-button
          type="primary"
          @click="gradingStep = 'upload'"
          :disabled="gradedCount < currentPsQuestions.length"
        >提交批改结果</el-button>
      </div>
    </div>
  </template>
</el-dialog>
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/views/PracticeSets.vue
git commit -m "feat(practice-sets): restructure grading dialog to list view"
```

---

## Task 3: 添加批改相关变量和方法

**Files:**
- Modify: `frontend/src/views/PracticeSets.vue` (script section)

- [ ] **Step 1: 添加计算属性**

在 `gradingResults` 附近添加计算属性：
```javascript
// 批改相关
const gradingDialogVisible = ref(false)
const gradingStep = ref('list') // 'list' | 'upload'
const gradingResults = ref({}) // { questionId: true/false }
const currentPsQuestions = ref([])
const currentReviewPs = ref(null)

const gradedCount = computed(() => Object.keys(gradingResults.value).length)
const correctCount = computed(() => Object.values(gradingResults.value).filter(v => v === true).length)
const wrongCount = computed(() => Object.values(gradingResults.value).filter(v => v === false).length)
```

- [ ] **Step 2: 修改 `handleQuestionGrading` 方法**

将逐题前进改为可跳序批改：
```javascript
const handleQuestionGrading = (questionId, isCorrect) => {
  gradingResults.value[questionId] = isCorrect
  // 移除自动前进逻辑，支持跳序批改
}

const getQuestionRowClass = (questionId) => {
  if (gradingResults.value[questionId] === true) return 'graded-correct'
  if (gradingResults.value[questionId] === false) return 'graded-wrong'
  return 'graded-pending'
}
```

- [ ] **Step 3: 添加查看原题方法**

```javascript
const showQuestionDetail = (question) => {
  // 打开查看原题弹层
  gradingQuestionDetail.value = question
  gradingDetailDialogVisible.value = true
}

const gradingDetailDialogVisible = ref(false)
const gradingQuestionDetail = ref(null)
```

- [ ] **Step 4: Commit**

```bash
git add frontend/src/views/PracticeSets.vue
git commit -m "feat(practice-sets): add grading computed properties and skip grading support"
```

---

## Task 4: 添加查看原题弹层（二合一）

**Files:**
- Modify: `frontend/src/views/PracticeSets.vue`

- [ ] **Step 1: 添加查看原题弹层模板**

在批改弹层后添加：
```vue
<!-- 查看原题弹层（二合一） -->
<el-dialog v-model="gradingDetailDialogVisible" title="查看原题" width="700px" destroy-on-close>
  <div v-if="gradingQuestionDetail" class="question-detail-content">
    <el-row :gutter="20">
      <el-col :span="12">
        <div class="detail-block">
          <div class="detail-label">原题</div>
          <div class="detail-value">
            <p v-if="gradingQuestionDetail.original_question_text">{{ gradingQuestionDetail.original_question_text }}</p>
            <el-image
              v-if="gradingQuestionDetail.original_image"
              :src="'/uploads/' + gradingQuestionDetail.original_image"
              fit="contain"
              style="max-width: 100%; max-height: 200px;"
              :preview-src-list="['/uploads/' + gradingQuestionDetail.original_image]"
            />
            <span v-if="!gradingQuestionDetail.original_question_text && !gradingQuestionDetail.original_image" class="text-gray-400">无</span>
          </div>
        </div>
      </el-col>
      <el-col :span="12">
        <div class="detail-block">
          <div class="detail-label">答案</div>
          <div class="detail-value answer-value">
            {{ gradingQuestionDetail.original_answer || '-' }}
          </div>
        </div>
      </el-col>
    </el-row>
    <div class="detail-meta">
      <span>题目ID: {{ gradingQuestionDetail.question_id }}</span>
      <span v-if="gradingQuestionDetail.knowledge_point">知识点: {{ gradingQuestionDetail.knowledge_point }}</span>
      <span v-if="gradingQuestionDetail.error_type">错误类型: {{ gradingQuestionDetail.error_type }}</span>
    </div>
  </div>
  <template #footer>
    <el-button @click="gradingDetailDialogVisible = false">关闭</el-button>
    <el-button type="primary" @click="editQuestionFromGrading">编辑此题</el-button>
  </template>
</el-dialog>
```

- [ ] **Step 2: 添加编辑方法**

```javascript
const editQuestionFromGrading = () => {
  // 关闭当前弹层，打开练习集详情弹层的编辑tab
  gradingDetailDialogVisible.value = false
  detailDialogVisible.value = true
  detailActiveTab.value = 'edit'
  // 加载题目详情到编辑表单
}
```

- [ ] **Step 3: Commit**

```bash
git add frontend/src/views/PracticeSets.vue
git commit -m "feat(practice-sets): add view/edit question modal in grading flow"
```

---

## Task 5: 添加样式

**Files:**
- Modify: `frontend/src/views/PracticeSets.vue` (style section)

- [ ] **Step 1: 添加批改页面样式**

在文件末尾的 `<style scoped>` 中添加：

```css
/* 批改弹层样式 */
.grading-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: linear-gradient(135deg, #67c23a 0%, #5daf34 100%);
  color: white;
  border-radius: 8px 8px 0 0;
}

.grading-header-left {
  display: flex;
  align-items: center;
  gap: 20px;
}

.grading-title {
  font-size: 18px;
  font-weight: bold;
}

.grading-progress-text {
  font-size: 14px;
  opacity: 0.9;
}

.accuracy-display {
  text-align: right;
}

.accuracy-value {
  font-size: 28px;
  font-weight: bold;
  display: block;
}

.accuracy-label {
  font-size: 12px;
  opacity: 0.8;
}

.grading-progress-bar {
  padding: 16px 20px;
  background: #f5f7fa;
  border-bottom: 1px solid #ebeef5;
}

.progress-bar {
  height: 8px;
  background: #e4e7ed;
  border-radius: 4px;
  overflow: hidden;
}

.progress-fill {
  height: 100%;
  background: linear-gradient(90deg, #67c23a, #85ce61);
  transition: width 0.3s;
}

.grading-stats {
  display: flex;
  gap: 20px;
  margin-top: 10px;
  font-size: 13px;
}

.stat-correct { color: #67c23a; }
.stat-wrong { color: #f56c6c; }
.stat-pending { color: #909399; }

/* 题目列表 */
.grading-question-list {
  max-height: 500px;
  overflow-y: auto;
  padding: 16px 20px;
}

.question-row {
  background: white;
  border-radius: 8px;
  margin-bottom: 12px;
  padding: 16px 20px;
  display: flex;
  align-items: center;
  gap: 16px;
  box-shadow: 0 2px 8px rgba(0,0,0,0.06);
  transition: all 0.2s;
  border-left: 4px solid #e4e7ed;
}

.question-row:hover {
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}

.question-row.graded-correct {
  border-left-color: #67c23a;
  background: linear-gradient(90deg, #f0f9eb 0%, white 30%);
}

.question-row.graded-wrong {
  border-left-color: #f56c6c;
  background: linear-gradient(90deg, #fef0f0 0%, white 30%);
}

.question-row.graded-pending {
  border-left-color: #e4e7ed;
}

.question-number {
  width: 40px;
  height: 40px;
  background: #409eff;
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  flex-shrink: 0;
}

.question-content {
  flex: 1;
  min-width: 0;
}

.question-text {
  font-size: 14px;
  color: #303133;
  margin-bottom: 8px;
  line-height: 1.5;
  word-break: break-word;
}

.question-answer {
  display: flex;
  align-items: center;
  gap: 8px;
}

.answer-label {
  font-size: 13px;
  color: #909399;
}

.answer-badge {
  background: #67c23a;
  color: white;
  padding: 2px 10px;
  border-radius: 4px;
  font-size: 13px;
  font-weight: 500;
}

.question-actions {
  display: flex;
  gap: 8px;
  flex-shrink: 0;
}

.btn-correct,
.btn-wrong {
  border: none;
  padding: 8px 16px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
  color: white;
}

.btn-correct {
  background: #67c23a;
}

.btn-correct:hover {
  background: #5daf34;
  transform: scale(1.02);
}

.btn-correct.active {
  background: #529b2e;
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.15);
}

.btn-wrong {
  background: #f56c6c;
}

.btn-wrong:hover {
  background: #e64242;
  transform: scale(1.02);
}

.btn-wrong.active {
  background: #d93636;
  box-shadow: inset 0 2px 4px rgba(0,0,0,0.15);
}

/* 底部栏 */
.grading-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.footer-stats {
  font-size: 14px;
  color: #606266;
}

.footer-buttons {
  display: flex;
  gap: 10px;
}

/* 查看原题弹层 */
.question-detail-content {
  padding: 10px 0;
}

.detail-block {
  margin-bottom: 16px;
}

.detail-label {
  font-size: 13px;
  color: #909399;
  font-weight: bold;
  margin-bottom: 8px;
}

.detail-value {
  background: #f5f7fa;
  padding: 12px;
  border-radius: 6px;
  font-size: 14px;
  color: #303133;
  line-height: 1.6;
}

.detail-value.answer-value {
  background: #f0f9eb;
  color: #67c23a;
  font-weight: bold;
  font-size: 16px;
}

.detail-meta {
  display: flex;
  gap: 20px;
  padding: 12px 0;
  border-top: 1px solid #ebeef5;
  font-size: 13px;
  color: #606266;
}

.detail-meta span {
  display: flex;
  align-items: center;
  gap: 4px;
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/views/PracticeSets.vue
git commit -m "style(practice-sets): add grading dialog styles with gradient backgrounds"
```

---

## Task 6: 调整图片上传步骤

**Files:**
- Modify: `frontend/src/views/PracticeSets.vue`

- [ ] **Step 1: 修改 gradingStep 初始值和相关逻辑**

将 `gradingStep` 的初始值从 `'overall'` 改为 `'list'`，并确保进入批改弹层时直接显示列表。

同时调整提交逻辑，`submitGrading` 在 upload 步骤时被调用。

```javascript
// 确保 gradingStep 初始为 'list'
const initGrading = async (ps) => {
  try {
    const { data } = await questionApi.getPracticeSet(ps.id)
    currentPsQuestions.value = data.questions || []
    gradingResults.value = {}
    gradingStep.value = 'list'  // 直接进入列表视图
  } catch (error) {
    ElMessage.error('获取练习集详情失败')
    gradingDialogVisible.value = false
  }
}
```

- [ ] **Step 2: Commit**

```bash
git add frontend/src/views/PracticeSets.vue
git commit -m "feat(practice-sets): adjust grading flow to start with list view"
```

---

## Task 7: 构建并测试

- [ ] **Step 1: 构建前端**

```bash
cd frontend && npm run build
```

预期：构建成功，无错误

- [ ] **Step 2: 手动测试**

1. 进入练习集列表页
2. 点击未复习练习集的"批改"按钮（绿色）
3. 验证：弹层显示所有题目的列表
4. 验证：可以跳序批改（先批改第3题，再批改第1题）
5. 验证：批改后整行有渐变背景色效果
6. 验证：全部批改完成后"提交批改结果"按钮可用
7. 验证：点击"查看原题"弹层显示完整信息
8. 验证：图片上传为可选步骤

- [ ] **Step 3: Commit**

```bash
git add frontend/src/views/PracticeSets.vue
git commit -m "fix(practice-sets): final adjustments and bug fixes"
```

---

## 验收标准检查清单

- [ ] 按钮文案改为"批改"，颜色为绿色
- [ ] 列表展示所有题目
- [ ] 批改状态有渐变背景色效果
- [ ] 支持跳序批改
- [ ] 全部批改完成后才能提交
- [ ] 查看原题弹层包含完整元信息
- [ ] 编辑功能可从弹层触发
- [ ] 图片上传为可选操作
