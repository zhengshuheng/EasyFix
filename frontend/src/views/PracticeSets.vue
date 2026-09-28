<template>
  <div class="practice-sets">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>练习集管理</span>
          <div class="header-actions">
            <el-button type="warning" size="large" @click="openSelectPracticeSet('do')">
              <el-icon><EditPen /></el-icon>
              去做题
            </el-button>
            <el-button type="warning" size="large" plain @click="openSelectPracticeSet('photo')">
              <el-icon><Camera /></el-icon>
              线下做题·拍照交卷
            </el-button>
            <el-button type="success" size="large" @click="openSelectPracticeSet('grade')">
              <el-icon><MagicStick /></el-icon>
              批改
            </el-button>
            <el-button type="primary" size="large" @click="generateDialogRef?.open()">
              <el-icon><Plus /></el-icon>
              出题
            </el-button>
          </div>
        </div>
      </template>

      <!-- 筛选条件 -->
      <div class="filters">
        <el-select v-if="subjectStore.isAll" v-model="filters.subject_id" placeholder="选择学科" clearable @change="fetchPracticeSets" style="width: 130px">
          <el-option v-for="s in subjects" :key="s.id" :label="s.name" :value="s.id" />
        </el-select>
        <el-select v-model="filters.reviewed" placeholder="复习状态" clearable @change="fetchPracticeSets" style="width: 120px">
          <el-option label="未复习" :value="false" />
          <el-option label="已复习" :value="true" />
        </el-select>
        <el-select v-model="filters.source_type" placeholder="卷子类型" clearable @change="fetchPracticeSets" style="width: 130px">
          <el-option label="语法专项" value="grammar" />
          <el-option label="单词复习" value="word" />
          <el-option label="阅读理解" value="reading" />
          <el-option label="AI练习" value="ai" />
          <el-option label="错题练习" value="error" />
        </el-select>
        <el-date-picker
          v-model="filters.date_range"
          type="daterange"
          range-separator="至"
          start-placeholder="开始日期"
          end-placeholder="结束日期"
          value-format="YYYY-MM-DD"
          style="width: 400px"
          @change="fetchPracticeSets"
        />
      </div>

      <!-- 批量操作栏 -->
      <div class="batch-actions">
        <span class="selected-count">已选择 {{ selectedIds.length }} 项</span>
        <el-button
          type="primary"
          size="default"
          :disabled="selectedIds.length === 0"
          @click="batchDownloadPdf"
        >
          批量下载PDF
        </el-button>
        <el-button
          type="danger"
          size="default"
          :disabled="selectedIds.length === 0"
          @click="batchDelete"
        >
          批量删除
        </el-button>
      </div>

      <!-- 练习集列表 -->
      <el-table
        v-if="practiceSets.length"
        :data="practiceSets"
        row-key="id"
        @selection-change="handleSelectionChange"
        style="width: 100%"
      >
        <el-table-column type="selection" width="40" />
        <el-table-column prop="name" label="名称" min-width="300">
          <template #default="{ row }">
            <div class="ps-name-cell">
              <span class="ps-name" :title="row.name">{{ row.name }}</span>
              <el-tag :type="row.question_type === 'original' ? 'primary' : 'success'" :style="{ marginLeft: '8px', fontSize: '14px', flexShrink: 0 }">
                {{ row.question_type === 'original' ? '原题' : '相似题' }}
              </el-tag>
            </div>
          </template>
        </el-table-column>
        <el-table-column prop="subject_name" label="学科" width="100" />
        <el-table-column prop="source_type" label="类型" width="100">
          <template #default="{ row }">
            {{ getSourceTypeLabel(row.source_type) }}
          </template>
        </el-table-column>
        <el-table-column prop="total_questions" label="题目数" width="80" align="center" />
        <el-table-column prop="review_count" label="复习次数" width="80" align="center" />
        <el-table-column prop="accuracy" label="正确率" width="80" align="center">
          <template #default="{ row }">
            <span v-if="row.source_type === 'word' && row.word_review_stats?.accuracy != null">
              {{ row.word_review_stats.accuracy }}%
            </span>
            <span v-else-if="row.accuracy != null">{{ row.accuracy }}%</span>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="reviewed" label="状态" width="110" align="center">
          <template #default="{ row }">
            <el-tag v-if="row.source_type === 'word'" :type="row.reviewed ? 'success' : 'info'" :style="{ fontSize: '14px' }">
              {{ row.reviewed ? '已复习' : '未复习' }}
            </el-tag>
            <el-tag v-else-if="row.reviewed" type="success" :style="{ fontSize: '14px' }">已批改</el-tag>
            <el-tag v-else-if="row.student_answered_count > 0" type="warning" :style="{ fontSize: '14px' }">已作答待批改</el-tag>
            <el-tag v-else type="info" :style="{ fontSize: '14px' }">未作答</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" min-width="150">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column :width="isMobile ? 90 : 400" fixed="right" label="操作">
          <template #default="{ row }">
            <template v-if="!isMobile">
              <el-button type="primary" size="default" @click="showDetail(row)">查看详情</el-button>
              <el-button v-if="row.pdf_path" type="primary" size="default" @click="downloadPdf(row)">下载PDF</el-button>
              <el-button v-else type="info" size="default" disabled>无PDF</el-button>
              <el-button type="danger" size="default" @click="deletePracticeSet(row)">删除</el-button>
            </template>
            <el-dropdown v-else trigger="click" @command="(cmd) => handleMobileAction(cmd, row)">
              <el-button type="primary" size="small">
                操作<el-icon class="el-icon--right"><ArrowDown /></el-icon>
              </el-button>
              <template #dropdown>
                <el-dropdown-menu>
                  <el-dropdown-item command="detail">查看详情</el-dropdown-item>
                  <el-dropdown-item v-if="row.pdf_path" command="pdf">下载PDF</el-dropdown-item>
                  <el-dropdown-item v-else command="pdf" disabled>无PDF</el-dropdown-item>
                  <el-dropdown-item command="delete" divided>删除</el-dropdown-item>
                </el-dropdown-menu>
              </template>
            </el-dropdown>
          </template>
        </el-table-column>
      </el-table>

      <el-empty v-else description="暂无练习集" />

      <!-- 分页 -->
      <div v-if="total > 0" class="pagination">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.limit"
          :page-sizes="[20, 50, 100, 500]"
          :total="total"
          layout="total, sizes, prev, pager, next"
          @change="fetchPracticeSets"
        />
      </div>
    </el-card>

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
          <el-button
            type="primary"
            plain
            :loading="aiGradingLoading"
            @click="runAIGrading"
          >
            <el-icon style="margin-right: 4px"><MagicStick /></el-icon>
            AI 一键批改
          </el-button>
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
            <div class="question-student-answer-readonly">
              <span class="student-answer-label">学生作答：</span>
              <span :class="question.student_answer ? 'student-answer-value' : 'student-answer-empty'">
                {{ question.student_answer || '未作答（AI 批改将判为错误）' }}
              </span>
            </div>
            <div
              v-if="aiComments[question.question_id]"
              :class="['ai-comment', aiComments[question.question_id].is_correct ? 'ai-comment-correct' : 'ai-comment-wrong']"
            >
              <el-icon style="margin-right: 4px">
                <component :is="aiComments[question.question_id].is_correct ? 'CircleCheck' : 'CircleClose'" />
              </el-icon>
              {{ aiComments[question.question_id].comment }}
            </div>
            <div v-else-if="!question.original_question_text && question.original_image" class="ai-unsupported">
              图片题暂不支持 AI 批改，请人工批改
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
              @click="submitGrading"
              :disabled="gradedCount < currentPsQuestions.length"
            >提交批改结果</el-button>
          </div>
        </div>
      </template>
    </el-dialog>

    <!-- 选择卷子弹窗（做题/拍照交卷/批改） -->
    <el-dialog
      v-model="selectPsDialogVisible"
      :title="selectPsMode === 'do' ? '选择卷子 - 学生做题'
        : (selectPsMode === 'photo' ? '选择卷子 - 线下做题（拍照交卷）' : '选择卷子 - 家长批改')"
      width="760px"
      destroy-on-close
    >
      <div class="do-tip">
        {{ selectPsMode === 'do'
          ? '选择一份卷子开始做题，完成后提交作答，家长可在「批改」中查看结果'
          : (selectPsMode === 'photo'
            ? '孩子在打印出来的卷子上线下作答，做完后拍照上传，系统自动识别手写作答并自动批改交卷'
            : '选择一份未批改的卷子，查看学生作答并批改（可 AI 一键批改）') }}
      </div>
      <div class="select-ps-list" v-loading="selectPsLoading">
        <div
          v-for="ps in selectPsList"
          :key="ps.id"
          class="select-ps-row"
          @click="enterSelectedPracticeSet(ps)"
        >
          <div class="select-ps-info">
            <div class="select-ps-name">
              {{ ps.name }}
              <el-tag size="small" :type="ps.question_type === 'original' ? 'primary' : 'success'">
                {{ ps.question_type === 'original' ? '原题' : '相似题' }}
              </el-tag>
              <el-tag size="small" :type="ps.reviewed ? 'success' : 'info'">
                {{ ps.reviewed ? '已批改' : '未批改' }}
              </el-tag>
            </div>
            <div class="select-ps-meta">
              <span>{{ ps.subject_name || '未分类' }}</span>
              <span>{{ getSourceTypeLabel(ps.source_type) }}</span>
              <span>{{ ps.total_questions }} 题</span>
              <span :class="ps.student_answered_count > 0 ? 'meta-answered' : 'meta-empty'">
                {{ ps.student_answered_count > 0 ? `已作答 ${ps.student_answered_count}/${ps.total_questions}` : '未作答' }}
              </span>
            </div>
          </div>
          <el-button type="primary" size="default" @click.stop="enterSelectedPracticeSet(ps)">
            {{ selectPsMode === 'do' ? '开始做题'
              : (selectPsMode === 'photo' ? '上传照片交卷' : (ps.reviewed ? '重新批改' : '去批改')) }}
          </el-button>
        </div>
        <el-empty v-if="!selectPsLoading && selectPsList.length === 0" description="暂无可用卷子" />
      </div>
      <template #footer>
        <el-button @click="selectPsDialogVisible = false">关闭</el-button>
      </template>
    </el-dialog>

    <!-- 拍照交卷弹窗（线下做题：拍照 → 自动识别手写作答 → 自动批改交卷） -->
    <el-dialog
      v-model="photoDialogVisible"
      title="线下做题 · 拍照交卷"
      width="1000px"
      destroy-on-close
      :close-on-click-modal="false"
    >
      <div class="photo-ps-name" v-if="photoPs?.name">📄 {{ photoPs.name }}</div>

      <!-- 步骤一：拍照 / 上传照片 -->
      <div v-if="photoStep === 'upload'">
        <div class="do-tip">
          把孩子在纸上做完的整份卷子拍清楚（正对、光线均匀、每题都拍到，可多张：正面/反面分别拍）。
          系统会自动识别手写作答，按卷面题号对号入座。
        </div>
        <div class="photo-actions">
          <el-button type="primary" plain @click="openCamera">
            <el-icon><Camera /></el-icon> 用电脑摄像头拍摄
          </el-button>
          <el-button plain @click="mobileCaptureInput?.click()">
            📱 手机 / 平板拍照
          </el-button>
          <span class="photo-hint">也可以直接在下面选框里选已有照片</span>
        </div>
        <input
          ref="mobileCaptureInput"
          type="file"
          accept="image/*"
          capture="environment"
          multiple
          style="display: none"
          @change="handleMobileCapture"
        />
        <!-- 摄像头/手机拍到的照片 -->
        <div v-if="cameraShots.length" class="photo-shots">
          <div v-for="(shot, i) in cameraShots" :key="shot.key" class="photo-shot">
            <img :src="shot.url" alt="拍摄的卷子照片" />
            <span class="photo-shot-del" @click="removeCameraShot(i)">✕</span>
            <span class="photo-shot-badge">已拍 {{ i + 1 }}</span>
          </div>
        </div>
        <el-upload
          :auto-upload="false"
          :multiple="true"
          :limit="9"
          accept="image/*"
          list-type="picture-card"
          :on-change="handlePhotoFileChange"
          :on-remove="handlePhotoFileChange"
          :file-list="photoFiles"
        >
          <el-icon><Plus /></el-icon>
        </el-upload>
        <el-checkbox v-model="photoAutoSubmit" style="margin-top: 8px">
          识别完成后立即自动交卷并批改（不勾选则先核对识别结果）
        </el-checkbox>
      </div>

      <!-- 步骤二：核对识别结果 -->
      <div v-else-if="photoStep === 'review'">
        <el-alert
          :title="photoSummary"
          :type="photoMissingCount ? 'warning' : 'success'"
          :closable="false"
          show-icon
          style="margin-bottom: 10px"
        />
        <el-table :data="photoQuestions" max-height="460" size="small" border>
          <el-table-column prop="no" label="题号" width="60" align="center" />
          <el-table-column label="题型" width="92">
            <template #default="{ row }">{{ QUESTION_TYPE_NAMES[row.question_type] || '题目' }}</template>
          </el-table-column>
          <el-table-column label="题干" min-width="260">
            <template #default="{ row }">
              <span class="photo-stem">{{ row.question_text || '（图片题）' }}</span>
            </template>
          </el-table-column>
          <el-table-column label="识别到的作答（可修改）" width="290">
            <template #default="{ row }">
              <el-input v-model="row.recognized_answer" size="small" placeholder="未识别到，可手动填写" />
            </template>
          </el-table-column>
          <el-table-column label="识别把握" width="90" align="center">
            <template #default="{ row }">
              <el-tag v-if="!row.recognized_answer" type="info" size="small">未识别</el-tag>
              <el-tag v-else-if="row.confidence === 'high'" type="success" size="small">高</el-tag>
              <el-tag v-else-if="row.confidence === 'low'" type="warning" size="small">低</el-tag>
              <el-tag v-else type="primary" size="small">中</el-tag>
            </template>
          </el-table-column>
        </el-table>
        <div class="photo-tip-small">提示：识别不准的题可以直接在上面改，空着的题会被判为「未作答」。</div>
      </div>

      <!-- 步骤三：交卷结果 -->
      <div v-else>
        <div class="photo-result">
          <div class="photo-score">
            <span class="photo-score-num">{{ photoResult?.accuracy ?? 0 }}%</span>
            <span class="photo-score-label">正确率</span>
          </div>
          <div class="photo-result-stats">
            <span class="text-green-600">✅ 对 {{ photoResult?.correct ?? 0 }} 题</span>
            <span class="text-red-500">❌ 错 {{ photoResult?.wrong ?? 0 }} 题</span>
            <span class="muted">共批改 {{ photoResult?.graded ?? 0 }} / {{ photoResult?.total ?? 0 }} 题</span>
            <span v-if="photoResult?.wrong" class="muted">错题已自动进入错题库</span>
          </div>
        </div>
        <el-table :data="photoResultRows" max-height="420" size="small" border>
          <el-table-column prop="no" label="题号" width="60" align="center" />
          <el-table-column label="题型" width="92">
            <template #default="{ row }">{{ QUESTION_TYPE_NAMES[row.question_type] || '题目' }}</template>
          </el-table-column>
          <el-table-column label="孩子写的" width="200">
            <template #default="{ row }">{{ row.answer || '（未作答）' }}</template>
          </el-table-column>
          <el-table-column label="判定" width="80" align="center">
            <template #default="{ row }">
              <el-tag v-if="row.is_correct === true" type="success" size="small">对</el-tag>
              <el-tag v-else-if="row.is_correct === false" type="danger" size="small">错</el-tag>
              <el-tag v-else type="info" size="small">未批</el-tag>
            </template>
          </el-table-column>
          <el-table-column label="评语" min-width="240">
            <template #default="{ row }">{{ row.comment }}</template>
          </el-table-column>
        </el-table>
        <div v-if="photoUnsupported.length" class="photo-tip-small">
          有 {{ photoUnsupported.length }} 道图片题不支持自动批改，请到「批改」里人工确认。
        </div>
      </div>

      <!-- 摄像头拍摄窗口 -->
      <el-dialog
        v-model="cameraVisible"
        title="用摄像头拍卷子"
        width="720px"
        append-to-body
        destroy-on-close
        @closed="stopCamera"
      >
        <div v-if="cameraError" class="camera-error">
          <el-alert :title="cameraError" type="warning" :closable="false" show-icon />
          <div class="photo-tip-small">
            摄像头需要浏览器授权，且页面必须是 http://localhost 或 https 打开；
            如果用的是手机或无法授权，请改用「📱 手机 / 平板拍照」或直接选已有照片。
          </div>
        </div>
        <div v-else class="camera-wrap">
          <video ref="cameraVideo" autoplay playsinline muted class="camera-video"></video>
          <div class="camera-hint">把整张卷子放进取景框，一页一张，拍完可继续拍下一页</div>
        </div>
        <div v-if="cameraShots.length" class="photo-shots">
          <div v-for="(shot, i) in cameraShots" :key="shot.key" class="photo-shot">
            <img :src="shot.url" alt="已拍照片" />
            <span class="photo-shot-del" @click="removeCameraShot(i)">✕</span>
          </div>
        </div>
        <template #footer>
          <el-button @click="cameraVisible = false">拍好了</el-button>
          <el-button type="warning" :disabled="!!cameraError" @click="captureShot">
            📸 拍这一页
          </el-button>
        </template>
      </el-dialog>

      <template #footer>
        <el-button @click="photoDialogVisible = false">关闭</el-button>
        <el-button v-if="photoStep === 'upload'" type="warning" :disabled="!photoTotalFiles" :loading="photoRecognizing" @click="startPhotoRecognize">
          {{ photoAutoSubmit ? '识别并自动交卷' : '开始识别' }}
        </el-button>
        <el-button v-else-if="photoStep === 'review'" @click="photoStep = 'upload'">重新拍照</el-button>
        <el-button v-if="photoStep === 'review'" type="primary" :loading="photoSubmitting" @click="submitPhotoPaper">确认交卷（自动批改）</el-button>
        <el-button v-if="photoStep === 'result'" @click="photoStep = 'review'">修正作答后重新判分</el-button>
      </template>
    </el-dialog>

    <!-- 做题弹窗（学生做题，全屏便于一年级操作） -->
    <el-dialog v-model="studentDoDialogVisible" title="学生做题" fullscreen class="student-do-dialog" destroy-on-close>
      <div class="do-tip">
        <span class="do-tip-text">请逐题作答，完成后点「提交作答」。提交后家长可在「批改」中查看并确认结果。</span>
        <span class="do-tip-actions">
          <span class="do-tip-switch">🔊 自动读题 <el-switch v-model="autoReadPractice" size="small" /></span>
          <el-button
            size="small"
            circle
            :type="speakAllReading ? 'danger' : 'primary'"
            plain
            @click="speakAllPending"
            :title="speakAllReading ? '停止朗读全部' : '朗读全部题目（未作答）'"
          >🔊</el-button>
        </span>
      </div>
      <div class="do-question-list">
        <template v-for="(group, gi) in groupedQuestions" :key="'group-' + gi">
          <!-- 试卷式大题标题：一、选择题（共2题，每题3分） -->
          <div v-if="group.name" class="do-question-group-header">
            <span class="do-group-title">{{ group.name }}</span>
            <span class="do-group-meta">共{{ group.items.length }}题<template v-if="group.score">，每题{{ group.score }}分</template></span>
          </div>
          <div
            v-for="(question, index) in group.items"
            :key="question.question_id"
            class="do-question-row"
          >
            <SceneVisual v-if="question.scene" :scene="question.scene" />
            <div class="do-question-header">
              <span class="do-question-number">{{ question.globalIndex }}.</span>
              <span v-if="group.score" class="do-question-score">({{ group.score }}分)</span>
              <span class="do-question-text">
                <template v-if="question.original_question_text">{{ question.original_question_text }}</template>
                <template v-else-if="question.original_image">
                  <el-image
                    :src="'/uploads/' + question.original_image"
                    fit="contain"
                    style="max-width: 120px; max-height: 120px; cursor: pointer;"
                    @click="previewImage(question.original_image)"
                  />
                </template>
                <template v-else><span class="text-gray-400">无题目内容</span></template>
              </span>
              <el-button
                size="small"
                circle
                :type="ttsReadingId === question.question_id ? 'danger' : 'primary'"
                plain
                @click="speakQuestion(question)"
                :title="ttsReadingId === question.question_id ? '停止朗读' : '语音读题'"
              >🔊</el-button>
            </div>
            <div class="do-answer-row">
              <!-- 选择题：直接点选项作答（一年级也能操作，无需键盘） -->
              <div v-if="getQuestionOptions(question).length" class="do-option-list">
                <button
                  v-for="opt in getQuestionOptions(question)"
                  :key="opt.letter"
                  type="button"
                  :class="['do-option-btn', { active: studentAnswers[question.question_id] === opt.letter }]"
                  @click="pickOption(question.question_id, opt.letter)"
                >
                  <span class="do-option-letter">{{ opt.letter }}.</span>
                  <span class="do-option-text">{{ opt.text }}</span>
                </button>
              </div>
              <!-- 判断题：对/错一键选择 -->
              <div v-else-if="question.question_type === 'judge'" class="do-option-list judge">
                <button
                  type="button"
                  :class="['do-option-btn judge', { active: studentAnswers[question.question_id] === '对' }]"
                  @click="pickOption(question.question_id, '对')"
                >✓ 对</button>
                <button
                  type="button"
                  :class="['do-option-btn judge', { active: studentAnswers[question.question_id] === '错' }]"
                  @click="pickOption(question.question_id, '错')"
                >× 错</button>
              </div>
              <template v-else>
                <!-- 填空题：题面有几个空就渲染几个输入框，逐空填写 -->
                <div v-if="countBlanks(question) >= 2" class="do-blank-list">
                  <div v-for="(_, bi) in countBlanks(question)" :key="bi" class="do-blank-item">
                    <span class="do-blank-index">{{ bi + 1 }}</span>
                    <el-input
                      v-model="getBlankModel(question)[bi]"
                      :placeholder="'第' + (bi + 1) + '空'"
                      size="default"
                      class="do-blank-input"
                      @focus="readOnFocus(question)"
                    />
                  </div>
                </div>
                <el-input
                  v-else
                  v-model="studentAnswers[question.question_id]"
                  :placeholder="doPlaceholder(question)"
                  size="default"
                  @focus="readOnFocus(question)"
                />
                <el-button
                  size="small"
                  circle
                  :type="voiceInputingId === question.question_id ? 'danger' : 'success'"
                  plain
                  :disabled="!speechRecognitionSupported"
                  @click="startVoiceInput(question.question_id)"
                  :title="!speechRecognitionSupported ? '当前浏览器不支持语音输入' : '语音输入答案'"
                >🎤</el-button>
              </template>
            </div>
          </div>
        </template>
      </div>
      <template #footer>
        <el-button @click="studentDoDialogVisible = false">返回</el-button>
        <el-button type="warning" :loading="studentDoSubmitting" @click="submitStudentAnswers">提交作答</el-button>
      </template>
    </el-dialog>

    <!-- 查看原题弹层（二合一） -->
    <el-dialog v-model="gradingDetailDialogVisible" :title="isEditingGradingQuestion ? '编辑原题' : '查看原题'" width="800px" destroy-on-close>
      <!-- 查看模式 -->
      <div v-if="gradingQuestionDetail && !isEditingGradingQuestion" class="question-detail-content">
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
            <!-- 阅读理解选项 -->
            <div v-if="gradingQuestionDetail.is_reading_question" class="detail-block mt-4">
              <div class="detail-label">选项</div>
              <div class="detail-value reading-options">
                <div class="option-row">{{ formatOption('A', gradingQuestionDetail.option_a) }}</div>
                <div class="option-row">{{ formatOption('B', gradingQuestionDetail.option_b) }}</div>
                <div class="option-row">{{ formatOption('C', gradingQuestionDetail.option_c) }}</div>
                <div class="option-row">{{ formatOption('D', gradingQuestionDetail.option_d) }}</div>
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

      <!-- 编辑模式 -->
      <div v-if="gradingQuestionDetail && isEditingGradingQuestion" class="question-edit-content">
        <el-form :model="gradingQuestionEditForm" label-width="80px">
          <el-form-item label="题目内容">
            <el-input v-model="gradingQuestionEditForm.original_question_text" type="textarea" :rows="3" placeholder="请输入题目内容" />
          </el-form-item>
          <el-form-item label="题目图片">
            <div v-if="gradingQuestionDetail.original_image" class="mb-2">
              <el-image
                :src="'/uploads/' + gradingQuestionDetail.original_image"
                fit="contain"
                style="max-width: 200px; max-height: 150px;"
              />
            </div>
            <el-input v-model="gradingQuestionEditForm.original_image" placeholder="图片路径（可选）" />
          </el-form-item>
          <el-form-item label="答案">
            <el-input v-model="gradingQuestionEditForm.original_answer" type="textarea" :rows="3" placeholder="请输入答案" />
          </el-form-item>
          <el-form-item label="知识点">
            <el-input v-model="gradingQuestionEditForm.knowledge_point" placeholder="请输入知识点" />
          </el-form-item>
          <el-form-item label="错误类型">
            <el-input v-model="gradingQuestionEditForm.error_type" placeholder="请输入错误类型" />
          </el-form-item>
          <el-form-item label="难度">
            <el-rate v-model="gradingQuestionEditForm.difficulty" :max="5" show-text :texts="['1星', '2星', '3星', '4星', '5星']" />
          </el-form-item>
        </el-form>
      </div>

      <template #footer>
        <el-button @click="gradingDetailDialogVisible = false">关闭</el-button>
        <template v-if="!isEditingGradingQuestion">
          <el-button type="primary" @click="startEditGradingQuestion">编辑此题</el-button>
        </template>
        <template v-else>
          <el-button @click="cancelEditGradingQuestion">取消</el-button>
          <el-button type="success" @click="saveGradingQuestion" :loading="gradingEditLoading">保存</el-button>
        </template>
      </template>
    </el-dialog>

    <!-- 复习完成上传图片弹窗 -->
    <el-dialog v-model="uploadDialogVisible" title="上传复习完成图片" width="600px" destroy-on-close>
      <div class="upload-tips">请上传复习完成的图片（可上传多张）</div>
      <el-upload
        ref="uploadRef"
        :auto-upload="false"
        :multiple="true"
        :limit="9"
        accept="image/*"
        list-type="picture-card"
        :on-change="handleImageChange"
        :on-remove="handleImageRemove"
        :file-list="reviewImages"
      >
        <el-icon><Plus /></el-icon>
      </el-upload>
      <template #footer>
        <el-button @click="uploadDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="confirmMarkReviewed" :loading="uploadLoading">确认</el-button>
      </template>
    </el-dialog>

    <!-- 练习集详情弹窗 -->
    <el-dialog v-model="detailDialogVisible" :title="detailData.name || '练习集详情'" width="1200px" class="practice-detail-dialog" @opened="onDetailDialogOpened">
      <el-tabs v-model="detailActiveTab">
        <!-- 详情页 -->
﻿        <el-tab-pane label="详情" name="detail">
          <!-- 单词复习：保留原卡片式（统计为主） -->
          <div v-if="detailData.source_type === 'word'" class="detail-info">
            <div class="detail-card">
              <div class="card-header-gray">基本信息</div>
              <div class="card-content">
                <el-descriptions :column="2" border size="small">
                  <el-descriptions-item label="名称">{{ detailData.name }}</el-descriptions-item>
                  <el-descriptions-item label="学科">{{ detailData.subject_name }}</el-descriptions-item>
                  <el-descriptions-item label="类型">{{ getSourceTypeLabel(detailData.source_type) }}</el-descriptions-item>
                  <el-descriptions-item label="题目数">{{ detailData.total_questions }}</el-descriptions-item>
                  <el-descriptions-item label="复习次数">{{ detailData.review_count }}</el-descriptions-item>
                  <el-descriptions-item label="出卷时间">{{ detailData.created_at ? formatDate(detailData.created_at) : '—' }}</el-descriptions-item>
                  <el-descriptions-item label="备注" :span="2">{{ detailData.notes || '无' }}</el-descriptions-item>
                </el-descriptions>
              </div>
            </div>
            <div v-if="detailData.word_review_stats" class="word-stats">
              <div class="detail-card">
                <div class="card-header-green">单词复习统计</div>
                <div class="card-content">
                  <el-descriptions :column="4" border size="small">
                    <el-descriptions-item label="复习类型">{{ getReviewTypeLabel(detailData.word_review_stats.review_type) }}</el-descriptions-item>
                    <el-descriptions-item label="总单词数">{{ detailData.word_review_stats.total_count }}</el-descriptions-item>
                    <el-descriptions-item label="正确数">{{ detailData.word_review_stats.correct_count }}</el-descriptions-item>
                    <el-descriptions-item label="准确率">{{ detailData.word_review_stats.accuracy }}%</el-descriptions-item>
                  </el-descriptions>
                </div>
              </div>
            </div>
          </div>

          <!-- 试卷式详情：题目列表是主角，其他信息折叠为次要 -->
          <div v-else class="exam-paper">
            <div class="paper-head">
              <div class="paper-title">{{ detailData.name || '练习集' }}</div>
              <div class="paper-meta">
                <span v-if="detailData.subject_name" class="pm-item">{{ detailData.subject_name }}</span>
                <span class="pm-item">共 {{ detailData.total_questions || 0 }} 题</span>
                <span v-if="showPaperScore && paperTotalScore" class="pm-item">满分 {{ paperTotalScore }} 分</span>
                <span class="pm-item">{{ getSourceTypeLabel(detailData.source_type) }}</span>
                <span v-if="detailData.created_at" class="pm-item">出卷时间 {{ formatDate(detailData.created_at) }}</span>
                <span v-if="detailData.show_ai_author" class="pm-item">出题人 AI 出题助手</span>
              </div>
              <div v-if="paperMarkSummary.total" class="paper-marks">
                <span class="pm ok">✓ 正确 {{ paperMarkSummary.correct }}</span>
                <span class="pm bad">✗ 错误 {{ paperMarkSummary.wrong }}</span>
                <span v-if="paperMarkSummary.pending" class="pm muted">— 未批改 {{ paperMarkSummary.pending }}</span>
                <span v-if="detailData.accuracy !== null && detailData.accuracy !== undefined" class="pm muted">正确率 {{ detailData.accuracy }}%</span>
              </div>
            </div>

            <div class="paper-toolbar">
              <div class="paper-toolbar-left">
                <el-switch v-model="detailShowAnswers" active-text="显示答案与解析" />
                <el-switch v-model="detailShowWorkSpace" active-text="答题留白" />
              </div>
              <div class="paper-toolbar-right">
                <el-button v-if="detailData.pdf_path" size="small" plain @click="downloadPdf(detailData)">下载 PDF</el-button>
                <el-button size="small" plain :loading="pdfRegenerating" @click="regeneratePdf">重新生成 PDF</el-button>
              </div>
            </div>

            <template v-if="detailData.questions && detailData.questions.length > 0">
              <div v-for="(group, gi) in groupedDetailQuestions" :key="'dg-' + gi" class="paper-section">
                <div class="paper-section-head">
                  <span class="sec-no">{{ cnNumber(gi + 1) }}</span>
                  <span class="sec-name">{{ group.name || '题目' }}</span>
                  <span class="sec-meta">
                    <template v-if="showPaperScore">
                      <template v-if="group.uniform">共 {{ group.items.length }} 题，每题 {{ group.perScore }} 分，本大题 {{ group.sectionTotal }} 分</template>
                      <template v-else>共 {{ group.items.length }} 题，本大题 {{ group.sectionTotal }} 分</template>
                    </template>
                    <template v-else>共 {{ group.items.length }} 题</template>
                  </span>
                </div>
                <div
                  v-for="row in group.items"
                  :key="row.id"
                  class="paper-question"
                  :class="row.is_correct === false ? 'q-wrong' : ''"
                >
                  <div class="q-no">{{ row.globalIndex }}.</div>
                  <div class="q-body">
                    <div class="q-text">{{ row.original_question_text || '（题干缺失）' }}</div>
                    <div v-if="row.original_image" class="q-image">
                      <el-image
                        :src="'/uploads/' + row.original_image"
                        fit="contain"
                        style="max-width: 220px; max-height: 150px; cursor: pointer;"
                        @click="previewImage(row.original_image)"
                      />
                    </div>
                    <div v-if="row.is_reading_question || row.option_a" class="q-options">
                      <div v-for="opt in detailOptionList(row)" :key="opt.letter" class="q-option">{{ opt.text }}</div>
                    </div>
                    <!-- 答题留白：主观题（计算/应用/操作/写作）留出书写空间，与打印出来的卷子一致 -->
                    <div
                      v-if="detailShowWorkSpace && writingSpacePx(row)"
                      class="q-write-space"
                      :style="{ height: writingSpacePx(row) + 'px' }"
                    ></div>
                    <div v-if="detailShowAnswers" class="q-answer-block">
                      <div class="q-answer-line">
                        <span class="qa-label">答案</span>
                        <span class="qa-text">{{ row.original_answer || '—' }}</span>
                      </div>
                      <div v-if="row.explanation" class="q-answer-line">
                        <span class="qa-label">解析</span>
                        <span class="qa-text explanation">{{ row.explanation }}</span>
                      </div>
                    </div>
                  </div>
                  <div class="q-side">
                    <span v-if="showPaperScore && !group.uniform && row.score" class="q-score">{{ row.score }}分</span>
                    <span class="q-result" :class="row.is_correct === true ? 'ok' : row.is_correct === false ? 'bad' : 'muted'">
                      {{ row.is_correct === true ? '✓' : row.is_correct === false ? '✗' : '—' }}
                    </span>
                  </div>
                </div>
              </div>
            </template>
            <el-empty v-else description="暂无题目" :image-size="80" />

            <!-- 次要信息：默认收起，不抢题目列表的视线 -->
            <el-collapse class="paper-extra">
              <el-collapse-item name="info">
                <template #title>
                  <span class="extra-title">试卷信息</span>
                  <span class="extra-hint">学科 / 类型 / 题数 / 复习次数 / 备注</span>
                </template>
                <el-descriptions :column="2" border size="small">
                  <el-descriptions-item label="名称">{{ detailData.name }}</el-descriptions-item>
                  <el-descriptions-item label="学科">{{ detailData.subject_name }}</el-descriptions-item>
                  <el-descriptions-item label="类型">{{ getSourceTypeLabel(detailData.source_type) }}</el-descriptions-item>
                  <el-descriptions-item label="题目数">{{ detailData.total_questions }}</el-descriptions-item>
                  <el-descriptions-item label="复习次数">{{ detailData.review_count }}</el-descriptions-item>
                  <el-descriptions-item label="出卷时间">{{ detailData.created_at ? formatDate(detailData.created_at) : '—' }}</el-descriptions-item>
                  <el-descriptions-item label="正确率">{{ detailData.accuracy !== null && detailData.accuracy !== undefined ? detailData.accuracy + '%' : '未批改' }}</el-descriptions-item>
                  <el-descriptions-item label="备注" :span="2">{{ detailData.notes || '无' }}</el-descriptions-item>
                </el-descriptions>
              </el-collapse-item>
              <el-collapse-item name="images">
                <template #title>
                  <span class="extra-title">复习完成图片</span>
                  <span class="extra-hint">{{ (detailData.review_images || []).length }} 张</span>
                </template>
                <div class="extra-images">
                  <div class="extra-images-toolbar">
                    <template v-if="!isEditingImages">
                      <el-button type="primary" size="small" @click="startEditImages">编辑图片</el-button>
                    </template>
                    <template v-else>
                      <el-button type="primary" size="small" @click="saveEditImages" :loading="imageEditLoading">保存</el-button>
                      <el-button size="small" @click="cancelEditImages">取消</el-button>
                    </template>
                  </div>
                  <div v-if="!isEditingImages" class="image-grid">
                    <template v-if="detailData.review_images && detailData.review_images.length > 0">
                      <div v-for="(img, idx) in detailData.review_images" :key="idx" class="image-item">
                        <el-image
                          :src="'/uploads/' + img"
                          :preview-src-list="detailData.review_images.map(i => '/uploads/' + i)"
                          fit="cover"
                          style="width: 110px; height: 110px; border-radius: 8px; cursor: pointer;"
                        />
                      </div>
                    </template>
                    <el-empty v-else description="暂无复习图片" :image-size="60" />
                  </div>
                  <div v-else class="image-edit-grid">
                    <el-upload
                      ref="imageEditUploadRef"
                      :auto-upload="false"
                      :multiple="true"
                      :limit="9"
                      accept="image/*"
                      list-type="picture-card"
                      :on-change="handleEditImageChange"
                      :on-remove="handleEditImageRemove"
                      :file-list="editImagesFileList"
                    >
                      <el-icon><Plus /></el-icon>
                    </el-upload>
                  </div>
                </div>
              </el-collapse-item>
            </el-collapse>
          </div>
        </el-tab-pane>

        <!-- 单词练习页（仅单词复习类型显示） -->
        <el-tab-pane v-if="detailData.source_type === 'word'" label="单词练习" name="words">
          <div class="word-practice">
            <div class="detail-card">
              <div class="card-header-green">复习统计</div>
              <div class="card-content">
                <div class="word-stats-summary">
                  <el-descriptions :column="4" border size="small">
                    <el-descriptions-item label="复习类型">{{ getReviewTypeLabel(detailData.word_review_stats?.review_type) }}</el-descriptions-item>
                    <el-descriptions-item label="总单词数">{{ detailData.word_review_stats?.total_count || 0 }}</el-descriptions-item>
                    <el-descriptions-item label="正确">{{ detailData.word_review_stats?.correct_count || 0 }}</el-descriptions-item>
                    <el-descriptions-item label="用时">{{ formatDuration(detailData.word_review_stats?.duration || 0) }}</el-descriptions-item>
                  </el-descriptions>
                </div>
              </div>
            </div>

            <div class="detail-card">
              <div class="card-header-purple">单词列表</div>
              <div class="card-content">
                <div class="word-cards-grid">
                  <div
                    v-for="(q, idx) in detailData.questions"
                    :key="q.id"
                    :class="['word-card', q.is_correct ? 'card-correct' : 'card-wrong']"
                  >
                    <div class="word-card-header">
                      <span class="word-index">{{ idx + 1 }}</span>
                      <el-tag :type="q.is_correct ? 'success' : 'danger'" size="small">
                        {{ q.is_correct ? '正确' : '错误' }}
                      </el-tag>
                    </div>
                    <div class="word-card-body">
                      <div class="word-main">
                        <div class="word-english">{{ q.question_text }}</div>
                        <div class="word-chinese">{{ q.answer }}</div>
                      </div>
                      <div class="word-result">
                        <div class="result-label">实际默写</div>
                        <div :class="['result-value', q.is_correct ? 'text-success' : 'text-danger']">
                          {{ q.user_answer || '-' }}
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </el-tab-pane>

        <!-- 编辑页 -->
        <el-tab-pane label="编辑" name="edit">
          <el-form :model="detailForm" label-width="80px">
            <el-form-item label="名称">
              <el-input v-model="detailForm.name" placeholder="请输入练习集名称" />
            </el-form-item>
            <el-form-item label="备注">
              <el-input v-model="detailForm.notes" type="textarea" :rows="4" placeholder="请输入备注" />
            </el-form-item>
          </el-form>
          <div style="text-align: right;">
            <el-button type="primary" @click="saveDetail" :loading="detailLoading">保存</el-button>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-dialog>

    <GenerateDialog ref="generateDialogRef" :subjects="subjects" @created="onPracticeGenerated" />

    <!-- 家长验证：学生删除练习需家长认证 -->
    <ParentLockDialog
      v-model="parentGuardVisible"
      title="家长验证"
      tip="删除练习需要家长验证"
      confirm-text="验证并删除"
      @success="onParentVerified"
      @update:model-value="!$event && onParentGuardCancel()"
    />
  </div>
</template>

<script setup>
import { ref, reactive, computed, watch, onMounted, onBeforeUnmount, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox, ElLoading } from 'element-plus'
import { Plus, Collection, Search, Camera, ArrowDown, ArrowRight } from '@element-plus/icons-vue'
import { questionApi } from '@/api/question'
import { useSubjectStore } from '@/stores/subject'
import { useKidStore } from '@/stores/kid'
import ParentLockDialog from '@/components/ParentLockDialog.vue'
import GenerateDialog from '@/components/GenerateDialog.vue'
import { QUESTION_TYPE_SCORES, QUESTION_TYPE_NAMES, QUESTION_TYPE_ORDER } from '@/constants/questionTypes'
import { useParentGuard } from '@/composables/useParentGuard'
import SceneVisual from '@/components/SceneVisual.vue'
import { speak, stopSpeech, installSpeechUnlock } from '@/utils/speech'

const subjectStore = useSubjectStore()
const kidStore = useKidStore()
const route = useRoute()
const practiceSets = ref([])
const subjects = ref([])
const total = ref(0)
const selectedIds = ref([])
const filters = reactive({
  subject_id: null,
  reviewed: null,
  source_type: null,
  date_range: null,
})
const pagination = reactive({
  page: 1,
  limit: 1000,
})

// 出题（生成练习）相关

// 题目按题型分组（做题/详情展示，试卷式大题结构）
const groupedQuestions = computed(() => {
  const qs = currentPsQuestions.value || []
  const hasType = qs.some(q => q.question_type)
  if (!hasType) return [{ key: '', name: '', score: null, items: qs.map((q, i) => ({ ...q, globalIndex: i + 1 })) }]
  const groups = {}
  for (const q of qs) {
    const t = q.question_type || '__other'
    if (!groups[t]) groups[t] = []
    groups[t].push(q)
  }
  const keys = Object.keys(groups).sort((a, b) => {
    const oa = a === '__other' ? 99 : QUESTION_TYPE_ORDER.indexOf(a) === -1 ? 98 : QUESTION_TYPE_ORDER.indexOf(a)
    const ob = b === '__other' ? 99 : QUESTION_TYPE_ORDER.indexOf(b) === -1 ? 98 : QUESTION_TYPE_ORDER.indexOf(b)
    return oa - ob
  })
  let gi = 1
  return keys.map(k => {
    const items = groups[k].map(q => ({ ...q, globalIndex: gi++ }))
    return { key: k, name: QUESTION_TYPE_NAMES[k] || '其他', score: QUESTION_TYPE_SCORES[k] || null, items }
  })
})

// 详情弹窗题目分组（基于 detailData.questions）
const groupedDetailQuestions = computed(() => {
  const qs = detailData.value.questions || []
  const hasType = qs.some(q => q.question_type)
  if (!hasType) {
    const items = qs.map((q, i) => ({ ...q, globalIndex: i + 1 }))
    const scores = items.map(q => q.score).filter(s => s !== null && s !== undefined)
    const perScore = scores.length === items.length && items.length ? scores[0] : null
    const uniform = perScore !== null && scores.every(s => s === scores[0])
    const sectionTotal = scores.reduce((a, b) => a + b, 0)
    return [{ key: '', name: '', score: perScore, perScore, uniform, sectionTotal, items }]
  }
  const groups = {}
  for (const q of qs) {
    const t = q.question_type || '__other'
    if (!groups[t]) groups[t] = []
    groups[t].push(q)
  }
  const keys = Object.keys(groups).sort((a, b) => {
    const oa = a === '__other' ? 99 : QUESTION_TYPE_ORDER.indexOf(a) === -1 ? 98 : QUESTION_TYPE_ORDER.indexOf(a)
    const ob = b === '__other' ? 99 : QUESTION_TYPE_ORDER.indexOf(b) === -1 ? 98 : QUESTION_TYPE_ORDER.indexOf(b)
    return oa - ob
  })
  let gi = 1
  return keys.map(k => {
    const items = groups[k].map(q => ({ ...q, globalIndex: gi++ }))
    // 分值取后端算好的（与打印出来的 PDF 一致）：同一大题内每题分值相同才算「每题X分」
    const scores = items.map(q => q.score).filter(s => s !== null && s !== undefined)
    const perScore = scores.length === items.length ? scores[0] : (QUESTION_TYPE_SCORES[k] || null)
    const uniform = scores.length === items.length && scores.every(s => s === scores[0])
    const sectionTotal = scores.length === items.length
      ? scores.reduce((a, b) => a + b, 0)
      : (perScore ? perScore * items.length : 0)
    return { key: k, name: QUESTION_TYPE_NAMES[k] || '其他', score: perScore, perScore, uniform, sectionTotal, items }
  })
})
// 默认显示答案与解析（可一键隐藏，方便直接拿卷子给孩子做）
const detailShowAnswers = ref(true)
// 答题留白开关（主观题书写区，默认显示，与打印出来的卷子一致）
const detailShowWorkSpace = ref(true)
// 主观题答题留白高度（px，约按 1mm≈3.4px 对应 PDF 里的留白：计算26mm/应用42mm/写话70mm）
const WRITING_SPACE_PX = {
  fill: 34, calc: 90, application: 145, operation: 115,
  reading: 48, sentence: 55, writing: 240,
}
const writingSpacePx = (row) => (row ? WRITING_SPACE_PX[row.question_type] || 0 : 0)
const CN_NUMBERS = ['一', '二', '三', '四', '五', '六', '七', '八', '九', '十', '十一', '十二', '十三', '十四', '十五']
const cnNumber = (n) => CN_NUMBERS[n - 1] || String(n)
// 题目选项（A/B/C/D，空选项自动过滤）
const detailOptionList = (row) => ['A', 'B', 'C', 'D']
  .map(letter => ({ letter, text: formatOption(letter, row['option_' + letter.toLowerCase()]) }))
  .filter(o => o.text)
// 卷面是否显示分值（练习卷可以不出分数）
const showPaperScore = computed(() => detailData.value.show_score !== false)
// 试卷总分（后端按计分方式算好；旧数据兜底按题型默认分值 × 题数）
const paperTotalScore = computed(() => {
  if (!showPaperScore.value) return 0
  if (detailData.value.total_score) return detailData.value.total_score
  let sum = 0
  for (const g of groupedDetailQuestions.value) {
    if (g.score) sum += g.score * g.items.length
  }
  return sum
})
// 批改概况（正确/错误/未批改）
const paperMarkSummary = computed(() => {
  const qs = detailData.value.questions || []
  let correct = 0, wrong = 0, pending = 0
  for (const q of qs) {
    if (q.is_correct === true) correct++
    else if (q.is_correct === false) wrong++
    else pending++
  }
  return { correct, wrong, pending, total: qs.length }
})


// 复习完成上传相关
const uploadDialogVisible = ref(false)
const uploadLoading = ref(false)
const reviewImages = ref([])
const currentReviewPs = ref(null)
const uploadRef = ref()

// 详情弹窗相关
const detailDialogVisible = ref(false)
const detailActiveTab = ref('detail')
const detailData = ref({})
const detailLoading = ref(false)
const detailForm = reactive({
  name: '',
  notes: ''
})

// 图片编辑相关
const isEditingImages = ref(false)
const imageEditLoading = ref(false)
const editImagesFileList = ref([])
const editImagesUploaded = ref([])
const imageEditUploadRef = ref()


const fetchPracticeSets = async () => {
  try {
    const params = {
      skip: (pagination.page - 1) * pagination.limit,
      limit: pagination.limit,
      subject_id: subjectStore.activeSubjectId !== null ? subjectStore.activeSubjectId : filters.subject_id,
      reviewed: filters.reviewed,
      source_type: filters.source_type || undefined,
    }
    if (subjectStore.activeGrade !== null) params.grade = subjectStore.activeGrade
    if (filters.date_range && filters.date_range.length === 2) {
      params.start_date = filters.date_range[0]
      params.end_date = filters.date_range[1]
    }
    const { data } = await questionApi.listPracticeSets(params)
    practiceSets.value = data.items
    total.value = data.total
    // 语法专项等入口生成练习卷后直达做题：/practice-sets?auto_do=<id>
    const autoDoId = Number(route.query.auto_do || '')
    if (autoDoId > 0) {
      const ps = practiceSets.value.find(p => p.id === autoDoId)
      if (ps) {
        selectPsMode.value = 'do'
        openStudentDo(ps)
      } else {
        ElMessage.info('卷子已生成，可在列表中找到后开始做题')
      }
    }
  } catch (error) {
    ElMessage.error('获取练习集列表失败')
  }
}

const fetchSubjects = async () => {
  try {
    const { data } = await questionApi.listSubjects()
    subjects.value = data
  } catch (error) {
    console.error('获取学科失败:', error)
  }
}

const handleSelectionChange = (selection) => {
  selectedIds.value = selection.map(row => row.id)
}

// 移动端窄屏：操作列从 400px 固定列收敛为「操作」下拉菜单（列宽 90px），
// 避免固定列占满 375px 屏导致数据列不可见、无法操作（9/28 反馈）
const isMobile = ref(window.innerWidth <= 768)
const mobileMq = window.matchMedia('(max-width: 768px)')
const onMobileMq = (e) => { isMobile.value = e.matches }
mobileMq.addEventListener('change', onMobileMq)
onBeforeUnmount(() => mobileMq.removeEventListener('change', onMobileMq))

const handleMobileAction = (cmd, row) => {
  if (cmd === 'detail') showDetail(row)
  else if (cmd === 'pdf') downloadPdf(row)
  else if (cmd === 'delete') deletePracticeSet(row)
}

const downloadPdf = (ps) => {
  if (ps.pdf_path) {
    window.open(`/uploads/${ps.pdf_path}`, '_blank')
  }
}

// 按最新的试卷样式重新生成 PDF（旧练习集的 PDF 还是老排版，点这里刷新）
const pdfRegenerating = ref(false)
const regeneratePdf = async () => {
  const ps = detailData.value
  if (!ps || !ps.id) return
  pdfRegenerating.value = true
  try {
    const res = await questionApi.generatePracticeSetPdf(ps.id)
    const url = res?.data?.pdf_url || res?.pdf_url
    if (url) {
      ps.pdf_path = url.replace(/^\/uploads\//, '')
      window.open(url, '_blank')
    }
    ElMessage.success('已按试卷样式重新生成 PDF')
  } catch (e) {
    ElMessage.error('生成 PDF 失败')
  } finally {
    pdfRegenerating.value = false
  }
}

const markReviewed = async (ps) => {
  currentReviewPs.value = ps

  // 单词练习集直接标记已复习
  if (ps.source_type === 'word') {
    try {
      await questionApi.markPracticeSetReviewed(ps.id)
      ElMessage.success('已标记为复习')
      fetchPracticeSets()
    } catch (error) {
      ElMessage.error('操作失败')
    }
    return
  }

  // 错题练习集进入批改流程
  gradingDialogVisible.value = true
  initGrading(ps)
}

// ============ 批改相关 ============
const gradingDialogVisible = ref(false)
const gradingStep = ref('overall') // 'overall' | 'detail' | 'upload'
const gradingCurrentIndex = ref(0)
const gradingResults = ref({}) // { questionId: true/false }
const currentPsQuestions = ref([])
const aiComments = ref({}) // { questionId: { is_correct, comment } }
const aiGradingLoading = ref(false)
// 做题（学生）状态
const studentDoDialogVisible = ref(false)
const studentAnswers = ref({}) // { questionId: 学生作答 }
const studentDoSubmitting = ref(false)
const currentDoPsId = ref(null)
const currentDoPsMeta = ref(null) // 做题中的练习集：{ subject_id, grade }

// 做题自动带读（低年级数学默认开，家长可关；选择存 localStorage）
const AUTO_READ_PRACTICE_KEY = 'easyfix_practice_autoread'
function readPracticeAutoReadDefault() {
  try {
    const saved = localStorage.getItem(AUTO_READ_PRACTICE_KEY)
    if (saved !== null) return saved === '1'
  } catch (e) { /* ignore */ }
  return true // 默认开；实际只在低年级数学自动生效
}
const autoReadPractice = ref(readPracticeAutoReadDefault())
watch(autoReadPractice, (v) => {
  try { localStorage.setItem(AUTO_READ_PRACTICE_KEY, v ? '1' : '0') } catch (e) { /* ignore */ }
})
// 低年级数学（1-2 年级）：自动带读 + 图文场景
const isLowGradeMathDo = computed(() => {
  const m = currentDoPsMeta.value
  return !!(m && m.subject_id === 1 && m.grade && m.grade <= 2)
})

// 做题无障碍：语音读题 / 语音输入答案
const ttsReadingId = ref(null)          // 正在朗读的题目 id
const voiceInputingId = ref(null)       // 正在语音识别的题目 id
const speechRecognitionSupported = ref(typeof window !== 'undefined' && !!(window.SpeechRecognition || window.webkitSpeechRecognition))
let recognitionInstance = null          // 语音识别实例

// 中文数字转阿拉伯数字（"二十六" -> 26，语音识别结果增强）
const convertCnToArabic = (text) => {
  const digits = { '零': 0, '一': 1, '二': 2, '两': 2, '三': 3, '四': 4, '五': 5, '六': 6, '七': 7, '八': 8, '九': 9 }
  if (!/[\d]/.test(text) && !/[零一二两三四五六七八九十百千万]/.test(text)) return text
  const parseCn = (s) => {
    if (!/[十百千万]/.test(s)) {
      // 纯单个数字字（如 二零一零 / 二十六以外的编号）按位拼接
      return s.split('').map(c => (digits[c] != null ? digits[c] : c)).join('')
    }
    let total = 0, section = 0, num = 0
    for (const ch of s) {
      if (ch === '万') { section = (section + num) * 10000; total += section; section = 0; num = 0 }
      else if (ch === '千') { section += (num || 1) * 1000; num = 0 }
      else if (ch === '百') { section += (num || 1) * 100; num = 0 }
      else if (ch === '十') { section += (num || 1) * 10; num = 0 }
      else { num = digits[ch] ?? 0 }
    }
    return total + section + num
  }
  return text.replace(/[零一二两三四五六七八九十百千万]+/g, m => String(parseCn(m)))
}

// 语音读题（SpeechSynthesis 本地中文朗读）
const getQuestionSpeakText = (q) => {
  let t = q.original_question_text || q.question_text || ''
  if (q.option_a) {
    t += '。选项A：' + (q.option_a || '')
    if (q.option_b) t += '；选项B：' + q.option_b
    if (q.option_c) t += '；选项C：' + q.option_c
    if (q.option_d) t += '；选项D：' + q.option_d
  }
  // 低年级数学：应用题要求写算式+答案（单位可省略），操作题按题目要求操作
  if (isLowGradeMathDo.value) {
    if (q.question_type === 'application') t += '。想一想，写出算式和答案，不用写单位'
    else if (q.question_type === 'operation') t += '。想一想，按题目要求操作，填上答案就行，不用写单位'
    else if (!q.option_a && (q.question_type === 'fill' || q.question_type === 'calc')) t += '。把算出的答案填进去就可以'
  }
  return t.trim()
}
// 语音读题：统一走 utils/speech（Chrome 中文语音不可用时自动降级服务器 TTS）
const speakQuestion = (q) => {
  if (ttsReadingId.value === q.question_id) { // 再点一次 = 停止
    stopSpeech()
    ttsReadingId.value = null
    return
  }
  const text = getQuestionSpeakText(q)
  if (!text) {
    ElMessage.warning('该题没有可朗读的文字内容')
    return
  }
  const id = q.question_id
  ttsReadingId.value = id
  speak(text, { lang: 'zh-CN', rate: 0.9 }).then((ok) => {
    if (ttsReadingId.value === id) ttsReadingId.value = null
    if (!ok) ElMessage.warning('朗读失败，请检查网络后重试')
  })
}

// 依次朗读全部未作答题（间隔 0.8s；再点一次停止）
const speakAllReading = ref(false)
let speakAllQueue = []
const speakNextInQueue = () => {
  if (!speakAllReading.value || !speakAllQueue.length) { speakAllReading.value = false; return }
  const q = speakAllQueue.shift()
  const text = getQuestionSpeakText(q)
  if (!text) { speakNextInQueue(); return }
  ttsReadingId.value = q.question_id
  speak(text, { lang: 'zh-CN', rate: 0.9 }).then(() => {
    ttsReadingId.value = null
    if (speakAllReading.value) setTimeout(speakNextInQueue, 800)
  })
}
const speakAllPending = () => {
  if (speakAllReading.value) {
    stopSpeech()
    speakAllQueue = []
    speakAllReading.value = false
    return
  }
  const qs = currentPsQuestions.value.filter(q => {
    const v = studentAnswers.value[q.question_id]
    return !v || (Array.isArray(v) && v.every(x => !(x || '').trim()))
  })
  if (!qs.length) { ElMessage.info('题目都已作答完成'); return }
  speakAllQueue = qs.slice()
  speakAllReading.value = true
  speakNextInQueue()
}
// 做题输入框占位提示（低年级数学：应用题写算式+答案，单位可省略）
const doPlaceholder = (q) => {
  if (isLowGradeMathDo.value && ['fill', 'calc', 'application', 'operation'].includes(q.question_type || '')) {
    if (q.question_type === 'application') return '写出算式和答案，不用写单位（可点右边麦克风语音输入）'
    if (q.question_type === 'operation') return '按题目要求操作，填上答案就行（可点右边麦克风语音输入）'
    return '填数字就行（可点右边麦克风语音输入）'
  }
  return '请输入你的作答（可点右边麦克风语音输入）'
}
// 聚焦填空输入框时自动带读（低年级数学）
const readOnFocus = (q) => {
  if (autoReadPractice.value && isLowGradeMathDo.value) speakQuestion(q)
}

// 语音输入答案（Web Speech Recognition，需 Chrome/Edge 且可联网）
const startVoiceInput = (qid) => {
  if (!speechRecognitionSupported.value) {
    ElMessage.warning('当前浏览器不支持语音输入，请使用 Chrome 或 Edge 浏览器')
    return
  }
  if (voiceInputingId.value === qid) {
    recognitionInstance && recognitionInstance.stop()
    return
  }
  if (recognitionInstance) recognitionInstance.stop()
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition
  const rec = new SR()
  recognitionInstance = rec
  rec.lang = 'zh-CN'
  rec.interimResults = true
  rec.continuous = false
  voiceInputingId.value = qid
  rec.onresult = (e) => {
    let final = ''
    for (let i = e.resultIndex; i < e.results.length; i++) {
      if (e.results[i].isFinal) final += e.results[i][0].transcript
    }
    if (final) {
      const converted = convertCnToArabic(final)
      const cur = studentAnswers.value[qid]
      if (Array.isArray(cur)) {
        // 多空填空：语音内容追加到第一个未填的空，全填则追加到最后一空
        let idx = cur.findIndex(x => !(x || '').trim())
        if (idx === -1) idx = cur.length - 1
        cur[idx] = (cur[idx] || '') + converted
      } else {
        studentAnswers.value[qid] = (cur || '') + converted
      }
    }
  }
  rec.onerror = (e) => {
    voiceInputingId.value = null
    if (e.error === 'not-allowed') ElMessage.warning('未获得麦克风权限，请在浏览器地址栏允许麦克风后重试')
    else if (e.error === 'network') ElMessage.error('语音识别服务不可用（需联网），请改用键盘输入')
    else ElMessage.warning('语音识别失败：' + e.error)
  }
  rec.onend = () => { voiceInputingId.value = null; recognitionInstance = null }
  try { rec.start() } catch (err) {
    voiceInputingId.value = null
    ElMessage.warning('语音识别启动失败，请手动输入')
  }
}

// 选择题选项（AI 出题的选择题选项独立返回；无选项返回空数组）
const getQuestionOptions = (q) => {
  const letters = ['A', 'B', 'C', 'D']
  return [q.option_a, q.option_b, q.option_c, q.option_d]
    .map((text, i) => ({ letter: letters[i], text }))
    .filter(o => o.text)
}
// 点选作答（选择题点选项、判断题点对错；再点一次取消）
const pickOption = (qid, value) => {
  studentAnswers.value[qid] = studentAnswers.value[qid] === value ? '' : value
}

// ===== 填空题多空逐空填写 =====
// 统计题面空位数量（支持（　）/（ ）/( )/____ 等占位写法）
const countBlanks = (q) => {
  const text = q.original_question_text || q.parsed_question || ''
  const m = text.match(/（\s*）|\(\s*\)|_{2,}/g)
  return m ? m.length : 0
}
// 把已保存的字符串答案按常见分隔符切回各空（重做卷子时预填用）
const splitSavedBlank = (text, n) => {
  const parts = (text || '').split(/[、；;，,和\s]+/).filter(p => p.trim() !== '')
  const arr = new Array(Math.max(n, 1)).fill('')
  for (let i = 0; i < n && i < parts.length; i++) arr[i] = parts[i].trim()
  return arr
}
// 确保多空题的答案数组已初始化并返回（模板 v-model 绑定数组元素用）
const getBlankModel = (q) => {
  const qid = q.question_id
  if (!Array.isArray(studentAnswers.value[qid])) {
    const saved = typeof studentAnswers.value[qid] === 'string' ? studentAnswers.value[qid] : ''
    studentAnswers.value[qid] = splitSavedBlank(saved, countBlanks(q))
  }
  return studentAnswers.value[qid]
}
// 提交时把多空数组合并成「空1、空2」字符串（批改/展示均按同一格式；全空视为未作答）
const formatAnswer = (v) => {
  if (Array.isArray(v)) {
    const trimmed = v.map(x => (x || '').trim())
    if (trimmed.every(x => !x)) return ''
    return trimmed.join('、')
  }
  return (v || '').trim()
}
// 选择卷子（做题/批改入口）
const selectPsDialogVisible = ref(false)
const selectPsMode = ref('do') // 'do' | 'grade'
const selectPsList = ref([])
const selectPsLoading = ref(false)

// 计算属性
const gradedCount = computed(() => Object.keys(gradingResults.value).length)
const correctCount = computed(() => Object.values(gradingResults.value).filter(v => v === true).length)
const wrongCount = computed(() => Object.values(gradingResults.value).filter(v => v === false).length)

const gradingDetailDialogVisible = ref(false)
const gradingQuestionDetail = ref(null)
const isEditingGradingQuestion = ref(false)
const gradingEditLoading = ref(false)
const gradingQuestionEditForm = reactive({
  original_question_text: '',
  original_image: '',
  original_answer: '',
  knowledge_point: '',
  error_type: '',
  difficulty: 3
})

const showQuestionDetail = (question) => {
  gradingQuestionDetail.value = question
  isEditingGradingQuestion.value = false
  gradingDetailDialogVisible.value = true
}

const startEditGradingQuestion = () => {
  // 填充编辑表单
  gradingQuestionEditForm.original_question_text = gradingQuestionDetail.value.original_question_text || ''
  gradingQuestionEditForm.original_image = gradingQuestionDetail.value.original_image || ''
  gradingQuestionEditForm.original_answer = gradingQuestionDetail.value.original_answer || ''
  gradingQuestionEditForm.knowledge_point = gradingQuestionDetail.value.knowledge_point || ''
  gradingQuestionEditForm.error_type = gradingQuestionDetail.value.error_type || ''
  gradingQuestionEditForm.difficulty = gradingQuestionDetail.value.difficulty || 3
  isEditingGradingQuestion.value = true
}

const cancelEditGradingQuestion = () => {
  isEditingGradingQuestion.value = false
}

const saveGradingQuestion = async () => {
  gradingEditLoading.value = true
  try {
    await questionApi.update(gradingQuestionDetail.value.question_id, {
      parsed_question: gradingQuestionEditForm.original_question_text,
      original_image: gradingQuestionEditForm.original_image,
      answer: gradingQuestionEditForm.original_answer,
      knowledge_point: gradingQuestionEditForm.knowledge_point,
      error_type: gradingQuestionEditForm.error_type,
      difficulty: gradingQuestionEditForm.difficulty
    })
    ElMessage.success('保存成功')
    isEditingGradingQuestion.value = false
    // 更新列表中的题目数据
    const idx = currentPsQuestions.value.findIndex(q => q.question_id === gradingQuestionDetail.value.question_id)
    if (idx !== -1) {
      currentPsQuestions.value[idx] = {
        ...currentPsQuestions.value[idx],
        ...gradingQuestionEditForm
      }
    }
  } catch (error) {
    ElMessage.error('保存失败')
  } finally {
    gradingEditLoading.value = false
  }
}

const initGrading = async (ps) => {
  // 获取练习集详情（含题目）
  try {
    const { data } = await questionApi.getPracticeSet(ps.id)
    // 练习集无 grade 列：详情接口从题目快照推导（低年级数学自动带读/图文场景判定用）
    currentDoPsMeta.value = { subject_id: data.subject_id ?? ps.subject_id, grade: data.grade ?? ps.grade }
    currentPsQuestions.value = data.questions || []
    gradingResults.value = {}
    aiComments.value = {}
    gradingStep.value = 'list' // 直接进入列表视图
  } catch (error) {
    ElMessage.error('获取练习集详情失败')
    gradingDialogVisible.value = false
  }
}

// ============ 做题（学生） ============
const openSelectPracticeSet = async (mode) => {
  selectPsMode.value = mode
  selectPsDialogVisible.value = true
  selectPsLoading.value = true
  try {
    const params = { limit: 500 }
    if (subjectStore.activeSubjectId !== null) params.subject_id = subjectStore.activeSubjectId
    if (subjectStore.activeGrade !== null) params.grade = subjectStore.activeGrade
    const { data } = await questionApi.listPracticeSets(params)
    let items = data.items || []
    if (mode === 'do' || mode === 'photo') {
      // 做题/拍照交卷只针对错题练习/阅读理解卷，单词复习卷走独立流程
      items = items.filter(ps => ps.source_type !== 'word')
    }
    selectPsList.value = items
  } catch (error) {
    ElMessage.error('获取卷子列表失败')
    selectPsList.value = []
  } finally {
    selectPsLoading.value = false
  }
}

const enterSelectedPracticeSet = (ps) => {
  selectPsDialogVisible.value = false
  if (selectPsMode.value === 'do') {
    openStudentDo(ps)
  } else if (selectPsMode.value === 'photo') {
    openPhotoSubmit(ps)
  } else {
    markReviewed(ps)
  }
}

const openStudentDo = async (ps) => {
  studentDoDialogVisible.value = true
  currentDoPsId.value = ps.id
  currentDoPsMeta.value = { subject_id: ps.subject_id, grade: ps.grade }
  try {
    const { data } = await questionApi.getPracticeSet(ps.id)
    // 练习集无 grade 列：详情接口从题目快照推导（低年级数学自动带读/图文场景判定用）
    currentDoPsMeta.value = { subject_id: data.subject_id ?? ps.subject_id, grade: data.grade ?? ps.grade }
    currentPsQuestions.value = data.questions || []
    studentAnswers.value = {}
    ttsReadingId.value = null
    stopSpeech()
    speakAllQueue = []
    speakAllReading.value = false
    if (recognitionInstance) { recognitionInstance.stop(); recognitionInstance = null }
    voiceInputingId.value = null
    // 预填已保存的作答（重新做题可修改；多空填空题切回逐空数组）
    currentPsQuestions.value.forEach(q => {
      if (q.student_answer) {
        const n = countBlanks(q)
        if (n >= 2) studentAnswers.value[q.question_id] = splitSavedBlank(q.student_answer, n)
        else studentAnswers.value[q.question_id] = q.student_answer
      }
    })
    // 低年级数学自动带读第一题（家长无需陪读）
    if (autoReadPractice.value && isLowGradeMathDo.value && currentPsQuestions.value.length) {
      speakQuestion(currentPsQuestions.value[0])
    }
  } catch (error) {
    ElMessage.error('获取练习集详情失败')
    studentDoDialogVisible.value = false
  }
}

const submitStudentAnswers = async () => {
  const answers = currentPsQuestions.value
    .map(q => ({
      question_id: q.question_id,
      answer: formatAnswer(studentAnswers.value[q.question_id])
    }))
    .filter(a => a.answer)

  if (answers.length === 0) {
    ElMessage.warning('请至少完成一道题再提交')
    return
  }

  studentDoSubmitting.value = true
  try {
    const { data } = await questionApi.submitAnswersPracticeSet(currentDoPsId.value, answers)
    ElMessage.success(`作答已保存（${data.saved}/${data.total} 题）`)
    studentDoDialogVisible.value = false
    fetchPracticeSets()
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '提交失败，请重试')
  } finally {
    studentDoSubmitting.value = false
  }
}

// ============ 线下做题 · 拍照交卷 ============
const photoDialogVisible = ref(false)
const generateDialogRef = ref(null)
// 出题弹窗（GenerateDialog.vue）生成成功回调：清筛选 + 切空间 + 刷新 + 打开详情
const onPracticeGenerated = async (e) => {
  const { data, kind, grade, subjectId } = e
  if (kind === 'ai') {
    // 新卷刚创建，任何筛选都可能把它挡在列表外（日期范围、复习状态、学习空间的学科/年级）
    filters.date_range = null
    filters.reviewed = null
    filters.source_type = null
    let switched = false
    if (grade && subjectStore.activeGrade !== null && subjectStore.activeGrade !== grade) {
      subjectStore.setGrade(grade)
      switched = true
    }
    if (subjectId && subjectStore.activeSubjectId !== null && subjectStore.activeSubjectId !== subjectId) {
      subjectStore.select(subjectId)
      switched = true
    }
    if (switched) ElMessage.info('已切换到新卷所在的学科/年级，方便查看')
  }
  await fetchPracticeSets()
  // 兜底提示：新卷仍不在列表里时明确告知，避免“生成完却不见了”
  if (data.id && !practiceSets.value.some((x) => x.id === data.id)) {
    ElMessage.warning(`新卷「${data.name}」已生成，但当前筛选条件下没显示出来，请检查列表筛选`)
  }
  if (data.id) {
    showDetail(data)
  }
}
const photoPs = ref(null)
const photoStep = ref('upload') // upload | review | result
const photoFiles = ref([])
const photoAutoSubmit = ref(true)
const photoRecognizing = ref(false)
const photoSubmitting = ref(false)
const photoQuestions = ref([])      // [{no, question_id, question_type, question_text, recognized_answer, confidence}]
const photoImages = ref([])         // 已上传保存的照片路径
const photoSummary = ref('')
const photoMissingCount = ref(0)
const photoPages = ref([])
const photoResult = ref(null)
const photoUnsupported = ref([])
// 摄像头/手机拍照
const cameraVisible = ref(false)
const cameraError = ref('')
const cameraShots = ref([])         // [{key, url, file}] 摄像头或手机拍到的照片
const cameraVideo = ref(null)       // <video> 模板引用
const cameraStream = ref(null)
const mobileCaptureInput = ref(null)
let shotSeq = 0

const photoTotalFiles = computed(() =>
  photoFiles.value.filter(f => f.raw).length + cameraShots.value.length)

const photoResultRows = computed(() => {
  if (!photoResult.value) return []
  const byQid = {}
  photoQuestions.value.forEach(q => { byQid[q.question_id] = q })
  const results = photoResult.value.results || []
  const rows = results.map(r => {
    const q = byQid[r.question_id] || {}
    return {
      no: q.no ?? '-',
      question_type: q.question_type,
      answer: (q.recognized_answer || '').trim(),
      is_correct: r.is_correct,
      comment: r.comment || ''
    }
  })
  // 未参与批改的题（如图片题）也列出来
  const gradedIds = new Set(results.map(r => r.question_id))
  photoQuestions.value.forEach(q => {
    if (!gradedIds.has(q.question_id)) {
      rows.push({
        no: q.no, question_type: q.question_type,
        answer: (q.recognized_answer || '').trim(),
        is_correct: null, comment: '未参与自动批改'
      })
    }
  })
  return rows.sort((a, b) => (a.no === '-' ? 999 : a.no) - (b.no === '-' ? 999 : b.no))
})

const handlePhotoFileChange = (file, fileList) => {
  photoFiles.value = fileList
}

// ---- 摄像头 / 手机拍照 ----
const clearCameraShots = () => {
  cameraShots.value.forEach(s => s.url && URL.revokeObjectURL(s.url))
  cameraShots.value = []
}

const stopCamera = () => {
  const stream = cameraStream.value
  if (stream) {
    try { stream.getTracks().forEach(t => t.stop()) } catch (e) { /* 忽略 */ }
    cameraStream.value = null
  }
  if (cameraVideo.value) {
    try { cameraVideo.value.srcObject = null } catch (e) { /* 忽略 */ }
  }
}

const openCamera = async () => {
  cameraError.value = ''
  cameraVisible.value = true
  await nextTick()
  try {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      throw new Error('当前页面无法直接调用摄像头（需要 http://localhost 或 https 打开）')
    }
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: 'environment', width: { ideal: 1920 }, height: { ideal: 1080 } },
      audio: false
    })
    cameraStream.value = stream
    if (cameraVideo.value) {
      cameraVideo.value.srcObject = stream
      if (cameraVideo.value.play) await cameraVideo.value.play()
    }
  } catch (error) {
    const name = error?.name || ''
    if (name === 'NotAllowedError' || name === 'SecurityError') {
      cameraError.value = '摄像头权限被拒绝，请点地址栏左侧的锁形图标重新允许后再试'
    } else if (name === 'NotFoundError' || name === 'DevicesNotFoundError') {
      cameraError.value = '没有检测到可用摄像头'
    } else {
      cameraError.value = error?.message || '摄像头调用失败'
    }
    stopCamera()
  }
}

const captureShot = () => {
  const video = cameraVideo.value
  if (!video || !video.videoWidth) {
    ElMessage.warning('摄像头还没准备好，请稍等一秒再拍')
    return
  }
  const canvas = document.createElement('canvas')
  const maxWidth = 2000 // 控一下体积，同时保证 OCR 看得清
  const scale = Math.min(1, maxWidth / video.videoWidth)
  canvas.width = Math.round(video.videoWidth * scale)
  canvas.height = Math.round(video.videoHeight * scale)
  canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height)
  canvas.toBlob(blob => {
    if (!blob) {
      ElMessage.error('拍照失败，请重试')
      return
    }
    const file = new File([blob], `camera_${Date.now()}.jpg`, { type: 'image/jpeg' })
    shotSeq += 1
    cameraShots.value.push({ key: `shot-${shotSeq}`, url: URL.createObjectURL(blob), file })
    ElMessage.success(`已拍第 ${cameraShots.value.length} 张，可继续拍下一页`)
  }, 'image/jpeg', 0.92)
}

const removeCameraShot = (index) => {
  const shot = cameraShots.value[index]
  if (shot?.url) URL.revokeObjectURL(shot.url)
  cameraShots.value.splice(index, 1)
}

// 手机/平板：<input capture> 直接唤起系统相机（不需要 HTTPS）
const handleMobileCapture = (event) => {
  const files = Array.from(event.target?.files || [])
  files.forEach(file => {
    shotSeq += 1
    cameraShots.value.push({ key: `shot-${shotSeq}`, url: URL.createObjectURL(file), file })
  })
  if (files.length) ElMessage.success(`已加入 ${files.length} 张照片`)
  if (event.target) event.target.value = ''
}

const openPhotoSubmit = (ps) => {
  photoPs.value = ps
  photoStep.value = 'upload'
  photoFiles.value = []
  clearCameraShots()
  cameraVisible.value = false
  stopCamera()
  photoQuestions.value = []
  photoImages.value = []
  photoResult.value = null
  photoUnsupported.value = []
  photoSummary.value = ''
  photoMissingCount.value = 0
  photoDialogVisible.value = true
}

const startPhotoRecognize = async () => {
  if (!photoTotalFiles.value) {
    ElMessage.warning('请先拍照或选择卷子照片')
    return
  }
  stopCamera()
  cameraVisible.value = false
  photoRecognizing.value = true
  try {
    const files = [
      ...photoFiles.value.map(f => f.raw).filter(Boolean),
      ...cameraShots.value.map(s => s.file)
    ]
    const { data } = await questionApi.recognizePaperAnswers(photoPs.value.id, files)
    photoQuestions.value = data.questions || []
    photoImages.value = data.images || []
    photoPages.value = data.pages || []
    photoMissingCount.value = data.missing_count || 0
    photoSummary.value = data.message || ''
    if (data.pages?.some(p => !p.ok)) {
      ElMessage.warning('有照片识别不完整，请核对识别结果')
    }
    if (!data.recognized_count) {
      // 一题都没识别出来时不要直接交卷（否则整卷被判未作答）
      photoStep.value = 'review'
      ElMessage.warning('没有识别到手写作答，请核对照片是否清晰、是否拍全')
      return
    }
    if (photoAutoSubmit.value) {
      await submitPhotoPaper()
    } else {
      photoStep.value = 'review'
      ElMessage.success(photoSummary.value)
    }
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '识别失败，请重试或换张更清晰的照片')
  } finally {
    photoRecognizing.value = false
  }
}

const submitPhotoPaper = async () => {
  photoSubmitting.value = true
  try {
    const answers = photoQuestions.value
      .map(q => ({ question_id: q.question_id, answer: (q.recognized_answer || '').trim() }))
      .filter(a => a.answer)
    const { data } = await questionApi.submitPaperPhotos(photoPs.value.id, {
      answers,
      images: photoImages.value,
      auto_grade: true
    })
    photoResult.value = data
    photoUnsupported.value = data.unsupported || []
    photoStep.value = 'result'
    ElMessage.success(`交卷完成：正确率 ${data.accuracy ?? 0}%，错 ${data.wrong ?? 0} 题已进错题库`)
    fetchPracticeSets()
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || '交卷失败，请稍后重试')
  } finally {
    photoSubmitting.value = false
  }
}

const runAIGrading = async () => {
  const ps = currentReviewPs.value
  if (!ps) return

  // 未保存任何学生作答时提示先做题
  const hasAnswers = currentPsQuestions.value.some(q => q.student_answer)
  if (!hasAnswers) {
    ElMessage.warning('学生还没有提交作答，请先在列表点「去做题」完成作答')
    return
  }

  aiGradingLoading.value = true
  try {
    const { data } = await questionApi.aiGradePracticeSet(ps.id)
    // 回填 AI 批改结果（家长仍可手动修正）
    ;(data.results || []).forEach(r => {
      if (r.question_id) {
        gradingResults.value[r.question_id] = r.is_correct
        aiComments.value[r.question_id] = { is_correct: r.is_correct, comment: r.comment || '' }
      }
    })
    if (data.unsupported && data.unsupported.length) {
      ElMessage.warning(`有 ${data.unsupported.length} 道图片题已跳过，请人工批改`)
    }
    ElMessage.success(`AI 批改完成，共批改 ${(data.results || []).length} 题`)
  } catch (error) {
    ElMessage.error(error.response?.data?.detail || 'AI 批改失败，请检查 LLM 配置后重试')
  } finally {
    aiGradingLoading.value = false
  }
}

const handleOverallGrading = (isAllCorrect) => {
  if (isAllCorrect) {
    // 整体全对
    currentPsQuestions.value.forEach(q => {
      gradingResults.value[q.question_id] = true
    })
    gradingStep.value = 'upload'
  } else {
    // 进入逐题批改
    gradingStep.value = 'detail'
  }
}

const handleQuestionGrading = (questionId, isCorrect) => {
  gradingResults.value[questionId] = isCorrect
  // 移除自动前进逻辑，支持跳序批改
}

const getQuestionRowClass = (questionId) => {
  if (gradingResults.value[questionId] === true) return 'graded-correct'
  if (gradingResults.value[questionId] === false) return 'graded-wrong'
  return 'graded-pending'
}

const getGradingAccuracy = () => {
  const total = currentPsQuestions.value.length
  if (total === 0) return 0
  const correct = Object.values(gradingResults.value).filter(v => v === true).length
  return Math.round(correct / total * 100)
}

const submitGrading = async () => {
  // 构建批改结果
  const questionResults = Object.entries(gradingResults.value).map(([question_id, is_correct]) => ({
    question_id: parseInt(question_id),
    is_correct
  }))

  // 先提交批改
  try {
    await questionApi.markPracticeSetReviewedWithGrading(
      currentReviewPs.value.id,
      questionResults
    )
    ElMessage.success('批改完成')
    gradingDialogVisible.value = false

    // 如果有图片，进入图片上传；否则完成
    if (reviewImages.value.length > 0) {
      uploadDialogVisible.value = true
    } else {
      fetchPracticeSets()
    }
  } catch (error) {
    ElMessage.error('批改提交失败')
  }
}

const handleImageChange = (file, fileList) => {
  reviewImages.value = fileList
}

const handleImageRemove = (file, fileList) => {
  reviewImages.value = fileList
}

const confirmMarkReviewed = async () => {
  if (!currentReviewPs.value) return

  try {
    uploadLoading.value = true

    // 如果有图片，先上传（使用简单上传接口，不调用OCR/LLM）
    let imagePaths = []
    if (reviewImages.value.length > 0) {
      const formData = new FormData()
      reviewImages.value.forEach(file => {
        formData.append('files', file.raw)
      })

      // 使用简单批量上传接口，不进行OCR识别
      const uploadRes = await fetch('/api/upload/batch-simple', {
        method: 'POST',
        body: formData,
      })
      const uploadData = await uploadRes.json()
      if (uploadData.images) {
        // 只提取图片路径
        imagePaths = uploadData.images
          .filter(img => img.success)
          .map(img => img.image_path)
      }
    }

    // 更新练习集图片（不重复标记已复习）
    await questionApi.updatePracticeSetReviewImages(currentReviewPs.value.id, imagePaths)

    uploadDialogVisible.value = false

    // 显示完成庆祝
    await ElMessageBox.alert(
      '<div style="text-align: center;">' +
      '<div style="font-size: 80px; margin-bottom: 10px;">🎉</div>' +
      '<div style="font-size: 24px; font-weight: bold; color: #67c23a;">复习完成！</div>' +
      '<div style="font-size: 16px; color: #909399; margin-top: 10px;">继续保持，下次会更棒！</div>' +
      '</div>',
      '恭喜',
      {
        confirmButtonText: '确定',
        dangerouslyUseHTMLString: true,
      }
    )

    fetchPracticeSets()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('操作失败')
    }
  } finally {
    uploadLoading.value = false
  }
}

// 查看详情
const showDetail = async (ps) => {
  try {
    const { data } = await questionApi.getPracticeSetDetail(ps.id)
    detailData.value = data
    detailForm.name = data.name
    detailForm.notes = data.notes || ''
    detailDialogVisible.value = true
  } catch (error) {
    ElMessage.error('获取详情失败')
  }
}

// 弹窗打开后确保详情tab选中
const onDetailDialogOpened = async () => {
  await nextTick()
  detailActiveTab.value = 'detail'
}

// 保存详情
const saveDetail = async () => {
  try {
    detailLoading.value = true
    await questionApi.updatePracticeSet(detailData.value.id, {
      name: detailForm.name,
      notes: detailForm.notes,
    })
    ElMessage.success('保存成功')
    detailDialogVisible.value = false
    fetchPracticeSets()
  } catch (error) {
    ElMessage.error('保存失败')
  } finally {
    detailLoading.value = false
  }
}

// 格式化选项（带字母前缀，避免重复）
const formatOption = (letter, text) => {
  if (!text) return ''
  text = text.trim()
  // 去除已有的选项前缀（A. B. C. D. / A、B、C、D、 / (A) / A) 等各种格式）
  text = text.replace(/^[A-Da-d]\s*[.、．]\s*/, '')
  text = text.replace(/^\([A-Da-d]\)\s*/, '')
  text = text.replace(/^[A-Da-d]\)\s*/, '')
  return letter + '. ' + text
}

// 格式化时长
const formatDuration = (seconds) => {
  if (!seconds && seconds !== 0) return '-'
  if (seconds === 0) return '0秒'
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}分${secs}秒`
}

// 获取复习类型标签
const getReviewTypeLabel = (type) => {
  const labels = { 1: '默写英文', 2: '选择中文', 3: '听力' }
  return labels[type] || '默写英文'
}

// 获取练习集类型标签
const getSourceTypeLabel = (type) => {
  if (type === 'word') return '单词复习'
  if (type === 'reading') return '阅读理解'
  if (type === 'grammar') return '语法专项'
  if (type === 'ai') return 'AI练习'
  return '错题练习'
}

// 家长认证守卫：学生删除练习需家长验证
const {
  visible: parentGuardVisible,
  guard,
  onVerified: onParentVerified,
  onCancel: onParentGuardCancel,
} = useParentGuard()

const deletePracticeSet = async (ps) => {
  try {
    await ElMessageBox.confirm('确定要删除这个练习集吗？', '删除确认', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    // 家长认证：学生（child）删除练习需家长验证
    await guard(() => questionApi.deletePracticeSet(ps.id))
    ElMessage.success('删除成功')
    fetchPracticeSets()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 批量下载PDF
const batchDownloadPdf = async () => {
  if (selectedIds.value.length === 0) {
    ElMessage.warning('请先选择要下载的练习集')
    return
  }
  try {
    const { data } = await questionApi.batchDownloadPracticeSetsPdf(selectedIds.value)
    const results = data.results || []
    const successCount = results.filter(r => r.pdf_url).length

    if (successCount === 0) {
      ElMessage.warning('所选练习集都没有可下载的PDF')
      return
    }

    // 逐个打开PDF链接
    for (const result of results) {
      if (result.pdf_url) {
        window.open(result.pdf_url, '_blank')
      }
    }
    ElMessage.success(`已开始下载 ${successCount} 个PDF文件`)
  } catch (error) {
    ElMessage.error('批量下载失败')
  }
}

// 批量删除
const batchDelete = async () => {
  if (selectedIds.value.length === 0) {
    ElMessage.warning('请先选择要删除的练习集')
    return
  }
  try {
    await ElMessageBox.confirm(
      `确定要删除选中的 ${selectedIds.value.length} 个练习集吗？此操作不可恢复。`,
      '批量删除确认',
      {
        confirmButtonText: '确定删除',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    // 家长认证：学生（child）批量删除练习需家长验证
    await guard(() => questionApi.batchDeletePracticeSets(selectedIds.value))
    ElMessage.success('批量删除成功')
    selectedIds.value = []
    fetchPracticeSets()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('批量删除失败')
    }
  }
}

const previewImage = (imagePath) => {
  if (imagePath) {
    window.open('/uploads/' + imagePath, '_blank')
  }
}

// 图片编辑相关
const startEditImages = () => {
  // 初始化已上传的图片列表
  editImagesUploaded.value = [...(detailData.value.review_images || [])]
  editImagesFileList.value = (detailData.value.review_images || []).map((img, idx) => ({
    name: img,
    url: '/uploads/' + img,
    status: 'success',
    isOld: true,
  }))
  isEditingImages.value = true
}

const handleEditImageChange = (file, fileList) => {
  editImagesFileList.value = fileList
}

const handleEditImageRemove = (file, fileList) => {
  editImagesFileList.value = fileList
}

const cancelEditImages = () => {
  isEditingImages.value = false
  editImagesFileList.value = []
  editImagesUploaded.value = []
}

const saveEditImages = async () => {
  try {
    imageEditLoading.value = true

    // 分离新上传的文件和已有的图片
    const newFiles = editImagesFileList.value.filter(f => !f.isOld)
    // 获取仍然保留的旧图片（从 editImagesFileList 中筛选 isOld 为 true 的）
    const keptOldImages = editImagesFileList.value
      .filter(f => f.isOld)
      .map(f => f.name)
    // 上传新文件
    let newImagePaths = [...keptOldImages]
    if (newFiles.length > 0) {
      const formData = new FormData()
      newFiles.forEach(file => {
        formData.append('files', file.raw)
      })

      const uploadRes = await fetch('/api/upload/batch-simple', {
        method: 'POST',
        body: formData,
      })
      const uploadData = await uploadRes.json()
      if (uploadData.images) {
        const uploadedPaths = uploadData.images
          .filter(img => img.success)
          .map(img => img.image_path)
        newImagePaths = [...keptOldImages, ...uploadedPaths]
      }
    }

    // 更新练习集图片
    await questionApi.updatePracticeSetReviewImages(detailData.value.id, newImagePaths)

    ElMessage.success('图片更新成功')
    isEditingImages.value = false

    // 刷新详情
    const { data } = await questionApi.getPracticeSetDetail(detailData.value.id)
    detailData.value = data
  } catch (error) {
    ElMessage.error('更新图片失败')
  } finally {
    imageEditLoading.value = false
  }
}

const formatDate = (dateStr) => {
  if (!dateStr) return ''
  return new Date(dateStr).toLocaleString('zh-CN')
}

onMounted(() => {
  installSpeechUnlock() // 首次手势解锁 AudioContext：服务器 TTS 降级音任意时刻可播
  fetchPracticeSets()
  fetchSubjects()
})
</script>

<style scoped>
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.card-header-inner {
  display: flex;
  align-items: center;
}

.card-header-inner .ps-name {
  flex: 1;
  margin-right: 8px;
}

.ps-name {
  font-weight: bold;
  font-size: 14px;
}

.filters {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 20px;
}

:deep(.el-range-separator) {
  width: 5% !important;
}

:deep(.el-date-editor) {
  width: 400px !important;
}

:deep(.el-date-editor .el-input__wrapper) {
  width: 400px !important;
}

:deep(.el-date-editor.el-range-editor) {
  width: 400px !important;
  max-width: 400px !important;
  min-width: 400px !important;
}

:deep(.el-date-editor.el-range-editor .el-range-input) {
  width: 100% !important;
}

.batch-actions {
  display: flex;
  align-items: center;
  gap: 15px;
  padding: 12px 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
  margin-bottom: 20px;
}

.selected-count {
  color: #606266;
  font-size: 13px;
  margin-right: auto;
}

.practice-set-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.practice-set-card {
  margin-bottom: 0;
}

.ps-content {
  padding: 10px 0;
}

.ps-info {
  margin-bottom: 15px;
}

.ps-info p {
  margin: 5px 0;
  font-size: 13px;
  color: #606266;
}

.ps-actions {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.upload-tips {
  margin-bottom: 15px;
  color: #909399;
  font-size: 14px;
}

.detail-info {
  padding: 10px 0;
}

.detail-info h4 {
  margin: 20px 0 10px;
  color: #303133;
  font-size: 16px;
}

.word-stats {
  margin-top: 20px;
}

.review-images {
  margin-top: 20px;
}

.image-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.image-item {
  position: relative;
}

.image-edit-grid {
  min-height: 150px;
}

.question-list-section {
  margin-top: 20px;
}

.original-question {
  font-size: 13px;
  color: #606266;
  line-height: 1.4;
}

/* 单词练习样式 */
.word-practice {
  padding: 10px 0;
}

.word-stats-bar {
  display: flex;
  gap: 20px;
  padding: 12px 15px;
  background-color: #f5f7fa;
  border-radius: 4px;
  margin-bottom: 20px;
  font-size: 14px;
  color: #606266;
}

.word-stats-bar span {
  margin-right: 15px;
}

.word-list {
  max-height: 500px;
  overflow-y: auto;
}

.word-item {
  border: 1px solid #ebeef5;
  border-radius: 8px;
  padding: 12px 15px;
  margin-bottom: 10px;
  background-color: #fff;
}

.word-item.is-correct {
  border-left: 4px solid #67c23a;
}

.word-item.is-wrong {
  border-left: 4px solid #f56c6c;
}

.word-header {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.word-index {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  width: 24px;
  height: 24px;
  background-color: #409eff;
  color: #fff;
  border-radius: 50%;
  font-size: 12px;
  margin-right: 10px;
}

.word-english {
  font-weight: bold;
  font-size: 16px;
  color: #303133;
}

.word-phonetic {
  margin-left: 8px;
  color: #909399;
  font-size: 13px;
}

.word-result {
  margin-left: auto;
  font-weight: bold;
  font-size: 14px;
}

.word-result.correct {
  color: #67c23a;
}

.word-result.wrong {
  color: #f56c6c;
}

.word-content {
  padding-left: 34px;
}

.word-answer {
  margin-bottom: 4px;
}

.word-answer .label,
.word-user-answer .label {
  color: #909399;
  font-size: 13px;
}

.word-answer .value {
  color: #303133;
  font-size: 14px;
}

.word-user-answer .value.wrong {
  color: #f56c6c;
}

/* 批改弹窗样式 */
.grading-overall {
  text-align: center;
  padding: 30px 0;
}

.grading-tip {
  font-size: 16px;
  color: #606266;
  margin-bottom: 20px;
}

.grading-subtip {
  font-size: 14px;
  color: #909399;
  margin-bottom: 15px;
}

.grading-question {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 30px;
}

.grading-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
}

.grading-detail {
  padding: 10px 0;
}

.grading-progress {
  font-size: 16px;
  color: #606266;
  margin-bottom: 20px;
  display: flex;
  justify-content: space-between;
}

.grading-accuracy {
  color: #409eff;
  font-weight: bold;
}

.grading-question-item {
  background: #f5f7fa;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.grading-question-item .question-text {
  font-size: 16px;
  margin-bottom: 10px;
  color: #303133;
}

.grading-question-item .question-answer {
  font-size: 14px;
  color: #67c23a;
  white-space: pre-wrap;
  word-break: break-word;
}

.original-question-block,
.original-answer-block {
  margin-bottom: 16px;
}

.original-question-block:last-child,
.original-answer-block:last-child {
  margin-bottom: 0;
}

.block-label {
  font-size: 12px;
  color: #909399;
  margin-bottom: 6px;
  font-weight: bold;
}

.block-content {
  background: #fff;
  padding: 12px;
  border-radius: 6px;
}

.answer-text {
  font-size: 16px;
  color: #67c23a;
  font-weight: bold;
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.8;
}

.grading-question-buttons {
  display: flex;
  gap: 20px;
  justify-content: center;
}

.grading-upload {
  padding: 10px 0;
}

/* 禁用卡片的hover效果 */
.practice-sets :deep(.el-card) {
  transition: none;
}
.practice-sets :deep(.el-card:hover) {
  transform: none;
  box-shadow: var(--shadow-sm) !important;
}

.text-success {
  color: #67c23a;
}

.text-danger {
  color: #f56c6c;
}

.el-descriptions--small .el-descriptions__body .el-descriptions__table .el-descriptions__cell {
  font-size: 16px !important;
}
.el-descriptions--small .el-descriptions__body .el-descriptions__table .el-descriptions__label,
.el-descriptions--small .el-descriptions__body .el-descriptions__table .el-descriptions__content {
  font-size: 16px !important;
}

/* ===== 试卷式详情（题目列表为主，其他信息为辅） ===== */
.exam-paper {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  padding: 24px 28px 18px;
  max-width: 1060px;
  margin: 0 auto;
}
/* 弹窗底色在非 scoped 样式块里设置（el-dialog__body 是组件库内部节点） */
.paper-head {
  text-align: center;
  padding-bottom: 12px;
  border-bottom: 2px solid #303133;
}
.paper-title {
  font-size: 20px;
  font-weight: 700;
  color: #303133;
  line-height: 1.6;
  letter-spacing: 0.5px;
}
.paper-meta {
  margin-top: 6px;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 4px 16px;
  font-size: 13px;
  color: #606266;
}
.paper-marks {
  margin-top: 8px;
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 6px 16px;  font-size: 13px;
}
.paper-marks .pm.ok { color: #67c23a; font-weight: 600; }
.paper-marks .pm.bad { color: #f56c6c; font-weight: 600; }
.paper-marks .pm.muted { color: #909399; }
.paper-toolbar {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 12px;
  padding: 10px 2px;
  border-bottom: 1px dashed #dcdfe6;
}
.paper-toolbar .paper-toolbar-left {
  display: flex;
  align-items: center;
  gap: 18px;
}
/* 主观题答题留白：淡色横线，像卷子上的书写区 */
.q-write-space {
  margin: 10px 0 4px;
  border-radius: 4px;
  background-image: repeating-linear-gradient(
    to bottom,
    transparent 0,
    transparent 27px,
    #e9eef5 27px,
    #e9eef5 28px
  );
}
.paper-section {
  margin-top: 18px;
}
.paper-section-head {
  display: flex;
  align-items: baseline;
  gap: 8px;
  margin-bottom: 6px;
  font-size: 16px;
  font-weight: 700;
  color: #303133;
}
.paper-section-head .sec-no { min-width: 22px; text-align: right; }
.paper-section-head .sec-meta {
  font-size: 12px;
  font-weight: 400;
  color: #909399;
}
.paper-question {
  display: flex;
  gap: 8px;
  padding: 10px 10px 10px 4px;
  border-bottom: 1px solid #f0f2f5;
  border-radius: 6px;
}
.paper-question:hover { background: #fafcff; }
.paper-question.q-wrong { background: #fef7f7; }
.paper-question .q-no {
  flex: none;
  min-width: 28px;
  text-align: right;
  font-weight: 700;
  font-size: 16px;
  color: #303133;
  line-height: 1.9;
}
.paper-question .q-body { flex: 1; min-width: 0; }
.paper-question .q-text {
  font-size: 16px;
  line-height: 1.9;
  color: #303133;
  white-space: pre-wrap;
  word-break: break-word;
}
.paper-question .q-image { margin: 8px 0; }
.paper-question .q-options { margin: 8px 0 4px; }
.paper-question .q-option {
  padding-left: 10px;
  font-size: 15px;
  line-height: 1.9;
  color: #303133;
}
.q-answer-block {
  margin-top: 8px;
  padding: 8px 12px;
  background: #f6ffed;
  border-left: 3px solid #b7eb8f;
  border-radius: 4px;
}
.q-answer-line {
  display: flex;
  gap: 8px;
  font-size: 15px;
  line-height: 1.8;
}
.q-answer-line .qa-label {
  flex: none;
  color: #67c23a;
  font-weight: 600;
}
.q-answer-line .qa-text {
  color: #303133;
  white-space: pre-wrap;
  word-break: break-word;
}
.q-answer-line .qa-text.explanation {
  color: #606266;
  font-size: 14px;
}
.paper-question .q-side {
  flex: none;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
  gap: 4px;
}
.paper-question .q-score {
  font-size: 12px;
  color: #e6a23c;
  font-weight: 600;
}
.q-result {
  font-size: 18px;
  font-weight: 700;
  line-height: 1.2;
}
.q-result.ok { color: #67c23a; }
.q-result.bad { color: #f56c6c; }
.q-result.muted { color: #c0c4cc; }
.paper-extra {
  margin-top: 22px;
  border-top: 1px solid #ebeef5;
  padding-top: 6px;
}
.paper-extra .extra-title {
  font-size: 14px;
  font-weight: 600;
  color: #606266;
}
.paper-extra .extra-hint {
  margin-left: 10px;
  font-size: 12px;
  color: #b1b3b8;
}
.paper-extra .extra-images-toolbar {
  margin-bottom: 10px;
}

/* 卡片通用样式 */
.detail-card {
  background: #fff;
  border-radius: 12px;
  box-shadow: 0 4px 16px rgba(0,0,0,0.08);
  margin-bottom: 16px;
  overflow: hidden;
}

.card-header-blue {
  background: linear-gradient(135deg, #409eff 0%, #3a8ee6 100%);
  color: #fff;
  padding: 14px 20px;
  font-weight: bold;
  font-size: 18px;
}

.card-header-green {
  background: linear-gradient(135deg, #67c23a 0%, #5daf34 100%);
  color: #fff;
  padding: 14px 20px;
  font-weight: bold;
  font-size: 18px;
}

.card-header-orange {
  background: linear-gradient(135deg, #e6a23c 0%, #db8b2e 100%);
  color: #fff;
  padding: 14px 20px;
  font-weight: bold;
  font-size: 18px;
}

.card-header-purple {
  background: linear-gradient(135deg, #9c27b0 0%, #862491 100%);
  color: #fff;
  padding: 14px 20px;
  font-weight: bold;
  font-size: 18px;
}

.card-header-gray {
  background: linear-gradient(135deg, #606266 0%, #555558 100%);
  color: #fff;
  padding: 14px 20px;
  font-weight: bold;
  font-size: 18px;
}

.card-header-small {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.card-content {
  padding: 20px;
}

/* 题目卡片 */
.question-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 16px;
}

.question-card {
  background: #f5f7fa;
  border-radius: 8px;
  padding: 16px;
  border-left: 4px solid #67c23a;
}

.question-card.card-wrong {
  background: #fef0f0;
  border-left-color: #f56c6c;
}

.question-card.card-pending {
  background: #f5f7fa;
  border-left-color: #909399;
}

.card-index {
  font-weight: bold;
  color: #606266;
}

.card-body {
  display: flex;
  justify-content: space-between;
  gap: 12px;
}

.question-info {
  flex: 1;
}

.info-row {
  margin-bottom: 10px;
}

.info-row .label {
  color: #909399;
  font-size: 16px;
}

.info-row .value {
  color: #303133;
  font-size: 16px;
}

.info-row .value.answer {
  color: #67c23a;
  font-weight: bold;
  white-space: pre-wrap;
  word-break: break-word;
  line-height: 1.8;
}

.reading-options {
  margin: 10px 0;
  padding: 10px;
  background: #f5f7fa;
  border-radius: 4px;
  font-size: 14px;
  line-height: 1.8;
}

.reading-options .option-row {
  margin: 4px 0;
}

.info-row .value.explanation {
  color: #909399;
  font-size: 13px;
  white-space: pre-wrap;
  line-height: 1.6;
}

/* 单词卡片网格 */
.word-cards-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 16px;
}

.word-card {
  background: #f5f7fa;
  border-radius: 8px;
  padding: 12px;
  border-left: 4px solid #67c23a;
}

.word-card.card-wrong {
  background: #fef0f0;
  border-left-color: #f56c6c;
}

.word-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 8px;
}

.word-index {
  font-weight: bold;
  color: #606266;
}

.word-card-body {
  display: flex;
  justify-content: space-between;
}

.word-main {
  flex: 1;
}

.word-english {
  font-size: 20px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 6px;
}

.word-chinese {
  font-size: 16px;
  color: #606266;
}

.word-result {
  text-align: right;
}

.result-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 6px;
}

.result-value {
  font-size: 18px;
  font-weight: bold;
}

/* 统计摘要 */
.word-stats-summary {
  margin-bottom: 0;
}

/* 查看原题弹层样式 */
.question-detail-content {
  padding: 10px 0;
}

.detail-block {
  margin-bottom: 16px;
}

.detail-label {
  font-size: 14px;
  color: #909399;
  margin-bottom: 8px;
  font-weight: bold;
}

.detail-value {
  font-size: 14px;
  color: #303133;
  line-height: 1.6;
}

.detail-value.answer-value {
  font-size: 16px;
  color: #67c23a;
  font-weight: bold;
  white-space: pre-wrap;
  word-break: break-word;
}

.detail-meta {
  display: flex;
  gap: 20px;
  padding: 12px 0;
  border-top: 1px solid #ebeef5;
  margin-top: 16px;
  font-size: 13px;
  color: #606266;
}

.text-gray-400 {
  color: #909399;
}

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
  display: inline-block;
  white-space: pre-wrap;
  word-break: break-word;
}

.question-student-answer-readonly {
  margin-top: 8px;
  font-size: 13px;
  line-height: 1.5;
}

.student-answer-label {
  color: #909399;
}

.student-answer-value {
  color: #303133;
  background: #f5f7fa;
  padding: 2px 8px;
  border-radius: 4px;
  word-break: break-word;
}

.student-answer-empty {
  color: #e6a23c;
}

.ai-comment {
  margin-top: 8px;
  padding: 6px 10px;
  border-radius: 6px;
  font-size: 13px;
  line-height: 1.5;
  display: flex;
  align-items: flex-start;
}

.ai-comment-correct {
  background: #f0f9eb;
  color: #529b2e;
}

.ai-comment-wrong {
  background: #fef0f0;
  color: #c45656;
}

.ai-unsupported {
  margin-top: 8px;
  font-size: 12px;
  color: #e6a23c;
  background: #fdf6ec;
  padding: 4px 10px;
  border-radius: 6px;
  display: inline-block;
}

.grading-header-right {
  display: flex;
  align-items: center;
  gap: 12px;
}

/* 做题弹窗 */
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.header-actions {
  display: flex;
  gap: 12px;
}

/* 练习集名称列：超长省略 */
.ps-name-cell {
  display: flex;
  align-items: center;
  min-width: 0;
}

.ps-name {
  display: inline-block;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
  flex: 1;
  min-width: 0;
}

.do-tip {
  font-size: 13px;
  color: #e6a23c;
  background: #fdf6ec;
  border-radius: 6px;
  padding: 8px 12px;
  margin-bottom: 12px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
}
.do-tip-actions {
  display: flex;
  align-items: center;
  gap: 8px;
}
.do-tip-switch {
  display: flex;
  align-items: center;
  gap: 4px;
  color: #606266;
}

.do-question-list {
  max-height: 60vh;
  overflow-y: auto;
}

.do-question-row {
  padding: 12px 0;
  border-bottom: 1px solid #ebeef5;
}

.do-question-row:last-child {
  border-bottom: none;
}

/* 试卷式大题分组标题（做题/详情） */
.do-question-group-header,
.detail-question-group-header {
  display: flex;
  align-items: baseline;
  gap: 10px;
  margin: 14px 0 4px;
  padding: 6px 10px;
  background: #f0faf9;
  border-left: 4px solid #4ECDC4;
  border-radius: 4px;
}
.do-group-title,
.detail-group-title {
  font-weight: 700;
  font-size: 15px;
  color: #303133;
}
.do-group-meta,
.detail-group-meta {
  font-size: 12px;
  color: #909399;
}
.do-question-score,
.card-score {
  color: #e6a23c;
  font-size: 12px;
  font-weight: 600;
}

/* 做题无障碍：语音读题 / 语音输入 */
.do-question-text {
  flex: 1;
  line-height: 1.6;
}

.do-answer-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 6px;
}

/* 选择题点选作答（无需键盘） */
.do-option-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  width: 100%;
}

.do-option-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  min-width: 130px;
  padding: 10px 14px;
  font-size: 16px;
  text-align: left;
  background: #fff;
  border: 2px solid #dcdfe6;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.15s;
}

.do-option-btn:hover {
  border-color: #4ECDC4;
  background: #f0fffd;
}

.do-option-btn.active {
  border-color: #4ECDC4;
  background: #e6fffb;
  box-shadow: 0 0 0 2px rgba(78, 205, 196, 0.25);
}

.do-option-letter {
  font-weight: 700;
  color: #4ECDC4;
}

.do-option-btn.judge {
  min-width: 90px;
  justify-content: center;
  font-weight: 600;
}

/* 填空题多空逐空输入 */
.do-blank-list {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  align-items: center;
  flex: 1;
}

.do-blank-item {
  display: flex;
  align-items: center;
  gap: 6px;
}

.do-blank-index {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #ecf5ff;
  color: #409eff;
  font-size: 12px;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.do-blank-input {
  width: 140px;
}

.do-question-header {
  display: flex;
  align-items: flex-start;
  gap: 6px;
  margin-bottom: 8px;
}

.do-question-number {
  color: #e6a23c;
  font-weight: bold;
  flex-shrink: 0;
}

.do-question-text {
  font-size: 14px;
  color: #303133;
  line-height: 1.5;
  word-break: break-word;
}

/* 选择卷子弹窗 */
.select-ps-list {
  max-height: 55vh;
  overflow-y: auto;
}

.select-ps-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 12px 14px;
  border: 1px solid #ebeef5;
  border-radius: 8px;
  margin-bottom: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.select-ps-row:hover {
  border-color: #409eff;
  background: #f5f9ff;
}

.select-ps-info {
  min-width: 0;
}

.select-ps-name {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
  display: flex;
  align-items: center;
  gap: 6px;
  flex-wrap: wrap;
}

.select-ps-meta {
  margin-top: 6px;
  font-size: 13px;
  color: #909399;
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
}

.meta-answered {
  color: #67c23a;
}

.meta-empty {
  color: #e6a23c;
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
  white-space: pre-wrap;
  word-break: break-word;
}

.reading-options .option-row {
  margin: 4px 0;
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
</style>
<style>
/* 详情弹窗：白卷面放在浅灰底上，更像一张真实的卷子 */
.practice-detail-dialog .el-dialog__body {
  background: #f2f4f7;
  padding-top: 10px;
}

.practice-detail-dialog .el-descriptions--small .el-descriptions__body .el-descriptions__table .el-descriptions__cell {
  font-size: 16px !important;
}
.practice-detail-dialog .el-descriptions--small .el-descriptions__body .el-descriptions__table .el-descriptions__label,
.practice-detail-dialog .el-descriptions--small .el-descriptions__body .el-descriptions__table .el-descriptions__content {
  font-size: 16px !important;
}

/* 做题弹窗全屏布局：题目列表滚动区 */
.student-do-dialog .el-dialog__body {
  max-height: calc(100vh - 190px);
  overflow-y: auto;
  padding-bottom: 8px;
}

/* 列表不独立滚动，全部展开在 body 流内（覆盖 scoped 的 max-height:60vh） */
.student-do-dialog .do-question-list {
  max-height: none;
  overflow: visible;
}

/* ===== 线下做题 · 拍照交卷 ===== */
.photo-ps-name {
  font-size: 15px;
  font-weight: 600;
  color: #303133;
  margin-bottom: 10px;
}
.photo-actions {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  margin-bottom: 12px;
}
.photo-hint {
  font-size: 12px;
  color: #909399;
}
.photo-shots {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 12px;
}
.photo-shot {
  position: relative;
  width: 108px;
  height: 108px;
  border: 1px solid #dcdfe6;
  border-radius: 6px;
  overflow: hidden;
  background: #f5f7fa;
}
.photo-shot img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.photo-shot-del {
  position: absolute;
  top: 2px;
  right: 2px;
  width: 18px;
  height: 18px;
  line-height: 18px;
  text-align: center;
  font-size: 12px;
  color: #fff;
  background: rgba(0, 0, 0, 0.55);
  border-radius: 50%;
  cursor: pointer;
}
.photo-shot-badge {
  position: absolute;
  left: 0;
  bottom: 0;
  padding: 0 6px;
  font-size: 11px;
  color: #fff;
  background: rgba(0, 0, 0, 0.5);
}
.camera-wrap {
  display: flex;
  flex-direction: column;
  align-items: center;
}
.camera-video {
  width: 100%;
  max-height: 420px;
  background: #000;
  border-radius: 6px;
  object-fit: contain;
}
.camera-hint {
  margin-top: 8px;
  font-size: 12px;
  color: #909399;
}
.camera-error {
  padding: 4px 0;
}
.photo-tip-small {
  margin-top: 8px;
  font-size: 12px;
  color: #909399;
  line-height: 1.6;
}
.photo-stem {
  font-size: 13px;
  color: #303133;
}
.photo-result {
  display: flex;
  align-items: center;
  gap: 24px;
  padding: 12px 16px;
  margin-bottom: 12px;
  background: #f5f7fa;
  border-radius: 8px;
}
.photo-score {
  display: flex;
  align-items: baseline;
  gap: 6px;
}
.photo-score-num {
  font-size: 34px;
  font-weight: 700;
  color: #e6a23c;
}
.photo-score-label {
  font-size: 13px;
  color: #909399;
}
.photo-result-stats {
  display: flex;
  gap: 18px;
  flex-wrap: wrap;
  font-size: 14px;
}
.photo-result-stats .text-green-600 {
  color: #67c23a;
}
.photo-result-stats .text-red-500 {
  color: #f56c6c;
}
.photo-result-stats .muted {
  color: #909399;
}

/* ============ 移动端 ============
 * 日期范围选择器桌面强制 400px（inline style + :deep min-width:400px!important），
 * 375px 屏必然横向溢出被裁；移动端改为 100% 全宽。
 * 注意：本 @media 必须在文件末尾，保证 !important 同权重时后出现者生效。 */
@media screen and (max-width: 768px) {
  :deep(.el-date-editor.el-range-editor) {
    width: 100% !important;
    min-width: 0 !important;
    max-width: 100% !important;
  }
  .filters {
    display: flex;
    flex-wrap: wrap;
    gap: 8px;
  }
  /* 卡片头：隐藏"练习集管理"标题 + 按钮图标，
     去做题/线下做题·拍照交卷/批改/出题 4 个按钮单行放下（不再第二行） */
  .card-header > span:first-child {
    display: none;
  }
  :deep(.header-actions .el-icon) {
    display: none;
  }
}
</style>
