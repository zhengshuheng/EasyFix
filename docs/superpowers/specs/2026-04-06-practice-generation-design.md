# 错题页生成练习功能 + PDF标注增强

## 功能概述

1. 错题列表页添加"生成练习"功能，根据学科/年级筛选错题
2. 练习集PDF增加 ID、知识点、错误类型 标注

---

## 功能1：错题页生成练习

### 前端（Questions.vue）

**入口：**
- 错题列表操作栏添加"生成练习"按钮

**配置弹窗：**
```
┌─────────────────────────────────┐
│  生成练习                    [X] │
├─────────────────────────────────┤
│  学科：  [数学            ▼] 必填 │
│  年级：  [全部            ▼] 选填 │
│  数量：  [5] 题  (1-99)        │
│                                 │
│  说明：优先选择未复习、低正确率题目 │
│                          [取消] [生成] │
└─────────────────────────────────┘
```

**交互流程：**
1. 选择学科（必填）、年级（选填）、数量（默认5）
2. 点击"生成"调用后端API
3. 返回后跳转练习集详情页

### 后端API

**接口：**
```
POST /api/practice-sets/generate-from-questions
```

**请求参数：**
| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| subject_id | int | 是 | 学科ID |
| grade | int | 否 | 年级 |
| count | int | 否 | 数量，默认5，最大99 |

**响应：** 创建的 `PracticeSetResponse`

**查询逻辑（优先级）：**
1. `review_count = 0` 的题目 → 未复习题目优先
2. 不足时按 `correct_count / review_count` 升序排列，取低正确率题目
3. 仍不足时随机补充
4. 超出可用数量时按实际数量生成

**数据库查询：**
```sql
-- 优先：未复习题目
SELECT * FROM question
WHERE subject_id = ? AND grade = ? AND review_count = 0 AND deleted = false

-- 不足时：低正确率
SELECT * FROM question
WHERE subject_id = ? AND grade = ? AND review_count > 0 AND deleted = false
ORDER BY (correct_count / review_count) ASC
LIMIT ?
```

---

## 功能2：练习集PDF增加标注字段

### 当前状态

`generate_practice_set_pdf(questions: List[Dict])` 当前只使用：
- `question_text`
- `difficulty`

### 修改后的参数

```python
def generate_practice_set_pdf(
    practice_set_name: str,
    questions: List[Dict[str, Any]],  # 包含以下字段:
    # - question_text: str
    # - difficulty: int
    # - id: int  # 新增
    # - knowledge_point: str  # 新增
    # - error_type: str  # 新增
) -> str
```

### PDF头部布局

```
┌──────────────────────────────────────────────────────┐
│ [ID: 123]  第1题   ★★★☆☆   知识点: 方程   错误类型: 计算 │
│──────────────────────────────────────────────────────│
│ 题目内容文本                                          │
└──────────────────────────────────────────────────────┘
```

- `ID`：白色背景青绿色方块
- 题目序号：`★` 彩色星号表示难度（1-5星）
- 知识点、错误类型：灰色小字
- 下方分隔线后是题目内容

### 星号配色（复用已有）

| 难度 | 填充色 RGB |
|------|------------|
| 1 | (103, 194, 58) 绿 |
| 2 | (133, 206, 97) 浅绿 |
| 3 | (230, 162, 60) 橙 |
| 4-5 | (245, 108, 108) 红 |
| 空白 | (220, 223, 230) 灰 |

---

## 文件改动

### 后端
- `backend/app/routers/practice_set.py` - 新增 `/generate-from-questions` 接口
- `backend/app/services/pdf.py` - `add_question()` 增加 id/knowledge_point/error_type 参数
- `backend/app/services/pdf.py` - `generate()` 传递完整字段

### 前端
- `frontend/src/views/Questions.vue` - 添加"生成练习"按钮和弹窗

---

## 依赖

- 已有 `PracticeSetPDF` 类
- 已有星号配色方案（来自错题列表打印）
