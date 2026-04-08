# 错题页生成练习 + PDF标注增强实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 实现错题页生成练习功能，并增强练习集PDF显示ID/知识点/错误类型标注

**Architecture:**
- 后端新增 `/api/practice-sets/generate-from-questions` 接口，按优先级选择题目
- PDF模板修改 `add_question` 方法，支持显示 id/knowledge_point/error_type
- 前端错题列表页添加"生成练习"按钮和配置弹窗

**Tech Stack:** Python FastAPI, Vue 3, Element Plus, fpdf2

---

### Task 1: 后端 - 新增生成练习API

**Files:**
- Modify: `backend/app/routers/practice_set.py`

**Steps:**

- [ ] **Step 1: 添加请求Schema**

在 `practice_set.py` 约第20行（`class PracticeSetCreate` 之后）添加：

```python
class GenerateFromQuestionsRequest(BaseModel):
    """根据条件生成练习集请求"""
    subject_id: int
    grade: Optional[int] = None
    count: int = 5

    class Config:
        schema_extra = {
            "example": {
                "subject_id": 1,
                "grade": 1,
                "count": 5
            }
        }
```

- [ ] **Step 2: 添加生成练习API**

在 `practice_set.py` 约第90行（`create_practice_set` 函数之前）添加：

```python
@router.post("/generate-from-questions", response_model=PracticeSetResponse, status_code=201)
def generate_practice_from_questions(data: GenerateFromQuestionsRequest, db: Session = Depends(get_db)):
    """
    根据条件生成练习集

    选择逻辑（优先级）：
    1. review_count = 0 的题目（未复习）
    2. 不足时按正确率低排序补充
    3. 仍不足时随机补充
    """
    # 构建基础查询
    query = db.query(Question).filter(
        Question.subject_id == data.subject_id,
        Question.deleted == False
    )
    if data.grade:
        query = query.filter(Question.grade == data.grade)

    # 1. 优先取未复习题目
    unvisited = query.filter(Question.review_count == 0).all()
    selected_ids = [q.id for q in unvisited]

    # 2. 不足时取低正确率题目
    remaining = data.count - len(selected_ids)
    if remaining > 0:
        reviewed = query.filter(Question.review_count > 0).all()
        # 按正确率升序排序
        reviewed_sorted = sorted(reviewed, key=lambda q: q.correct_count / q.review_count if q.review_count > 0 else 0)
        for q in reviewed_sorted[:remaining]:
            selected_ids.append(q.id)
            remaining -= 1

    # 3. 仍不足时随机补充
    if remaining > 0:
        all_ids = [q.id for q in query.all() if q.id not in selected_ids]
        import random
        random.shuffle(all_ids)
        selected_ids.extend(all_ids[:remaining])

    # 实际取出的数量
    actual_count = len(selected_ids)
    if actual_count == 0:
        raise HTTPException(status_code=400, detail="没有符合条件的题目")

    # 获取题目详情
    selected_questions = db.query(Question).filter(Question.id.in_(selected_ids)).all()
    # 保持优先级顺序
    question_map = {q.id: q for q in selected_questions}
    ordered_questions = [question_map[qid] for qid in selected_ids if qid in question_map]

    # 创建练习集
    from datetime import datetime
    practice_set = PracticeSet(
        name=f"练习集_{datetime.now().strftime('%Y%m%d%H%M%S')}",
        subject_id=data.subject_id,
        source_type="question",
        question_type="original",
        total_questions=actual_count,
    )
    db.add(practice_set)
    db.commit()
    db.refresh(practice_set)

    # 创建关联记录
    for idx, question in enumerate(ordered_questions):
        psq = PracticeSetQuestion(
            practice_set_id=practice_set.id,
            question_id=question.id,
            display_order=idx,
        )
        db.add(psq)

    db.commit()
    db.refresh(practice_set)

    # 获取学科名称
    subject_name = db.query(Subject).filter(Subject.id == data.subject_id).first().name if data.subject_id else ""

    return {
        "id": practice_set.id,
        "name": practice_set.name,
        "subject_id": practice_set.subject_id,
        "subject_name": subject_name,
        "source_type": "question",
        "question_type": "original",
        "total_questions": actual_count,
        "reviewed": False,
        "review_count": 0,
        "created_at": practice_set.created_at,
        "questions": [],
    }
```

- [ ] **Step 3: 验证导入**

运行: `cd backend && python -c "from app.routers.practice_set import generate_practice_from_questions; print('OK')"`
预期: OK（无输出表示成功）

- [ ] **Step 4: 提交**

```bash
git add backend/app/routers/practice_set.py
git commit -m "feat(practice-set): add generate-from-questions API with priority selection"
```

---

### Task 2: PDF增强 - add_question方法支持标注字段

**Files:**
- Modify: `backend/app/services/pdf.py`

**Steps:**

- [ ] **Step 1: 修改 add_question 方法签名和实现**

将 `PracticeSetPDF.add_question` 方法（约第97-160行）替换为：

```python
def add_question(self, index: int, question_text: str, difficulty: int, question_id: int = None,
                 knowledge_point: str = None, error_type: str = None):
    """添加一道题目"""
    # 难度星号配色
    STAR_COLORS = {
        1: (103, 194, 58),    # 绿
        2: (133, 206, 97),    # 浅绿
        3: (230, 162, 60),    # 橙
        4: (245, 108, 108),   # 红
        5: (245, 108, 108),   # 红
    }
    EMPTY_STAR_COLOR = (220, 223, 230)  # 灰

    difficulty = max(1, min(5, difficulty))
    star_color = STAR_COLORS.get(difficulty, (245, 108, 108))

    # 第一行：ID标注 + 序号 + 星号
    self.set_font('chinese_b', size=10)
    self.set_fill_color(78, 205, 196)  # #4ECDC4
    self.set_text_color(255, 255, 255)

    # ID标注
    if question_id is not None:
        self.cell(0, 7, f'ID:{question_id}', new_x=XPos.RIGHT, new_y=YPos.TOP, align='L', fill=False)

    # 序号
    self.cell(0, 7, f'第{index}题', new_x=XPos.RIGHT, new_y=YPos.TOP, align='C', fill=True)

    # 星号（分两段渲染：填充+空白）
    self.set_fill_color(248, 249, 250)
    self.set_text_color(*star_color)
    self.set_font('chinese_b', size=10)
    self.cell(15, 7, '★' * difficulty, new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
    self.set_text_color(*EMPTY_STAR_COLOR)
    self.set_font('chinese', size=10)
    self.cell(25, 7, '★' * (5 - difficulty), new_x=XPos.RIGHT, new_y=YPos.TOP, align='C')
    self.set_text_color(51, 51, 51)
    self.ln(1)

    # 第二行：知识点 + 错误类型
    self.set_font('chinese', size=9)
    self.set_text_color(128, 128, 128)
    parts = []
    if knowledge_point:
        parts.append(f'知识点: {knowledge_point}')
    if error_type:
        parts.append(f'错误类型: {error_type}')
    if parts:
        self.cell(0, 5, '  |  '.join(parts), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')

    self.ln(2)

    # 分隔线
    self.set_draw_color(189, 195, 199)
    self.set_line_width(0.3)
    self.line(10, self.get_y(), 200, self.get_y())
    self.ln(4)

    # 题目内容
    self.set_font('chinese', size=11)
    self.set_text_color(51, 51, 51)
    safe_text = decode_html(question_text) if question_text else '暂无题目内容'
    self.multi_cell(0, 6, safe_text)
    self.ln(6)
```

- [ ] **Step 2: 验证**

运行: `cd backend && python -c "from app.services.pdf import PracticeSetPDF; print('OK')"`

- [ ] **Step 3: 提交**

```bash
git add backend/app/services/pdf.py
git commit -m "feat(pdf): add id/knowledge_point/error_type to add_question method"
```

---

### Task 3: PDF生成 - 传递完整字段

**Files:**
- Modify: `backend/app/services/pdf.py` - `generate()` 方法
- Modify: `backend/app/routers/practice_set.py` - `generate_pdf()` 接口

**Steps:**

- [ ] **Step 1: 修改 generate 方法**

找到 `PracticeSetPDF.generate()` 方法（约第168-183行），将 `questions_data.append` 部分替换为：

```python
# 获取关联的题目
ps_questions = db.query(PracticeSetQuestion).filter(
    PracticeSetQuestion.practice_set_id == practice_set_id
).order_by(PracticeSetQuestion.display_order).all()

questions_data = []
for psq in ps_questions:
    question = db.query(Question).filter(Question.id == psq.question_id).first()
    if not question:
        continue

    if ps.question_type == "similar" and psq.similar_question_id:
        similar = db.query(SimilarQuestion).filter(SimilarQuestion.id == psq.similar_question_id).first()
        question_text = similar.similar_text if similar else ""
    else:
        question_text = question.parsed_question or question.original_text or ""

    questions_data.append({
        "question_text": question_text,
        "difficulty": question.difficulty or 3,
        "id": question.id,
        "knowledge_point": question.knowledge_point or "",
        "error_type": question.error_type or "",
    })
```

- [ ] **Step 2: 修改 generate_pdf 路由**

找到 `generate_pdf()` 函数（约第459-521行），将 `questions_data.append` 部分替换为上面的代码（同样获取 id, knowledge_point, error_type）

- [ ] **Step 3: 验证**

运行: `cd backend && python -c "from app.routers.practice_set import generate_pdf; print('OK')"`

- [ ] **Step 4: 提交**

```bash
git add backend/app/routers/practice_set.py
git commit -m "feat(pdf): pass id/knowledge_point/error_type when generating questions_data"
```

---

### Task 4: 前端 - 错题列表添加生成练习功能

**Files:**
- Modify: `frontend/src/views/Questions.vue`

**Steps:**

- [ ] **Step 1: 添加生成练习弹窗**

在 Questions.vue 模板中找到操作列（约第105行），在现有按钮之后添加"生成练习"按钮：

```vue
<el-button type="success" size="default" @click="showGenerateDialog">生成练习</el-button>
```

- [ ] **Step 2: 添加生成练习弹窗模板**

在 `<el-dialog v-model="printDialogVisible"` 之后（约第414行）添加：

```vue
<!-- 生成练习弹窗 -->
<el-dialog v-model="generateDialogVisible" title="生成练习" width="400px">
  <el-form :model="generateForm" label-width="80px">
    <el-form-item label="学科" required>
      <el-select v-model="generateForm.subject_id" placeholder="选择学科" style="width: 100%">
        <el-option
          v-for="subject in subjectOptions"
          :key="subject.id"
          :label="subject.name"
          :value="subject.id"
        />
      </el-select>
    </el-form-item>
    <el-form-item label="年级">
      <el-select v-model="generateForm.grade" placeholder="全部" clearable style="width: 100%">
        <el-option v-for="g in gradeOptions" :key="g.value" :label="g.label" :value="g.value" />
      </el-select>
    </el-form-item>
    <el-form-item label="数量">
      <el-input-number v-model="generateForm.count" :min="1" :max="99" />
    </el-form-item>
    <el-form-item>
      <span style="color: #909399; font-size: 12px">优先选择未复习、低正确率的题目</span>
    </el-form-item>
  </el-form>
  <template #footer>
    <el-button @click="generateDialogVisible = false">取消</el-button>
    <el-button type="primary" @click="generatePractice" :loading="generating">生成</el-button>
  </template>
</el-dialog>
```

- [ ] **Step 3: 添加相关数据和方法**

在 `<script setup>` 中添加：

```javascript
// 生成练习相关
const generateDialogVisible = ref(false)
const generating = ref(false)
const generateForm = reactive({
  subject_id: null,
  grade: null,
  count: 5,
})

const subjectOptions = ref([])

const showGenerateDialog = () => {
  generateForm.subject_id = null
  generateForm.grade = null
  generateForm.count = 5
  generateDialogVisible.value = true
}

const generatePractice = async () => {
  if (!generateForm.subject_id) {
    ElMessage.warning('请选择学科')
    return
  }
  generating.value = true
  try {
    const { data } = await practiceSetApi.generateFromQuestions({
      subject_id: generateForm.subject_id,
      grade: generateForm.grade,
      count: generateForm.count,
    })
    ElMessage.success('练习集已生成')
    generateDialogVisible.value = false
    // 跳转到练习集详情
    window.location.href = `/practice-sets?id=${data.id}`
  } catch (error) {
    ElMessage.error('生成失败')
  } finally {
    generating.value = false
  }
}

// 获取学科列表
const fetchSubjects = async () => {
  try {
    const { data } = await questionApi.listSubjects()
    subjectOptions.value = data
  } catch (error) {
    console.error('获取学科失败:', error)
  }
}
```

- [ ] **Step 4: 添加API方法**

在 `frontend/src/api/question.js` 中添加：

```javascript
export const practiceSetApi = {
  // ... 现有方法 ...
  generateFromQuestions(params) {
    return api.post('/practice-sets/generate-from-questions', params)
  },
}
```

- [ ] **Step 5: 在 onMounted 中调用 fetchSubjects**

```javascript
onMounted(() => {
  fetchWords()
  fetchSubjects()  // 添加这行
})
```

- [ ] **Step 6: 验证构建**

运行: `cd frontend && npm run build 2>&1 | tail -10`
预期: 无错误

- [ ] **Step 7: 提交**

```bash
git add frontend/src/views/Questions.vue frontend/src/api/question.js
git commit -m "feat(questions): add generate practice dialog with subject/grade/count selection"
```

---

### Task 5: 前端 - 添加练习集API封装

**Files:**
- Modify: `frontend/src/api/practiceSet.js`（如果存在）或 `frontend/src/api/question.js`

**Steps:**

- [ ] **Step 1: 如果 practiceSet.js 不存在，创建它**

```javascript
import api from './index'

export const practiceSetApi = {
  list(params) {
    return api.get('/practice-sets', { params })
  },
  get(id) {
    return api.get(`/practice-sets/${id}`)
  },
  generateFromQuestions(params) {
    return api.post('/practice-sets/generate-from-questions', params)
  },
  generatePdf(id) {
    return api.post(`/practice-sets/${id}/generate-pdf`)
  },
  markReviewed(id, data) {
    return api.post(`/practice-sets/${id}/mark-reviewed`, data)
  },
  delete(id) {
    return api.delete(`/practice-sets/${id}`)
  },
}
```

如果 `practiceSet.js` 已存在，只添加 `generateFromQuestions` 方法。

- [ ] **Step 2: 在 Questions.vue 中更新 import**

```javascript
// 将
import { questionApi } from '@/api/question'
// 改为
import { questionApi } from '@/api/question'
import { practiceSetApi } from '@/api/practiceSet'
```

- [ ] **Step 3: 提交**

```bash
git add frontend/src/api/practiceSet.js 2>/dev/null; git add frontend/src/api/question.js frontend/src/views/Questions.vue
git commit -m "feat(api): add practiceSet API with generateFromQuestions"
```

---

**验证方式：**
1. 启动后端 `python -m uvicorn app.main:app --host 0.0.0.0 --port 8000`
2. 启动前端 `npm run dev`
3. 访问错题列表页，点击"生成练习"按钮
4. 选择学科，点击生成
5. 检查生成的练习集PDF是否包含 ID/知识点/错误类型

**Spec 核对：**
- [x] 后端 API `/api/practice-sets/generate-from-questions` 实现
- [x] 优先级选择逻辑：未复习 → 低正确率 → 随机
- [x] PDF `add_question` 支持 id/knowledge_point/error_type
- [x] 前端生成练习弹窗：学科必填、年级选填、数量默认5上限99
- [x] 生成后跳转练习集详情
