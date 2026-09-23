<template>
  <div class="words">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>单词本</span>
          <div class="review-buttons">
            <el-button type="info" plain @click="openLearnPage">
              <el-icon><Reading /></el-icon>
              学习本页
            </el-button>
            <el-button type="danger" @click="startReview(3)">
              <el-icon><Microphone /></el-icon>
              听写
            </el-button>
            <el-button type="success" @click="startReview(1)">
              <el-icon><Edit /></el-icon>
              中-英
            </el-button>
            <el-button type="primary" @click="startReview(2)">
              <el-icon><Select /></el-icon>
              英-中
            </el-button>
            <el-button type="warning" @click="showPrintDialog">
              <el-icon><Printer /></el-icon>
              打印默写
            </el-button>
          </div>
        </div>
      </template>

      <!-- 今日任务大入口（四维记忆调度 · 三分类） -->
      <div class="daily-task-card">
        <div class="dt-header">
          <div class="dt-title">📅 今日任务 <span v-if="dailyTask.loaded" class="dt-count">{{ dailyTask.total }} 词</span></div>
          <el-button text size="small" class="dt-config" @click="openDimConfig">⚙ 记忆设置</el-button>
        </div>
        <div class="dt-desc">
          <template v-if="dailyTask.loaded">
            <span class="dt-dims">记忆维度：{{ dimNames(dailyTask.enabled_dimensions) }}</span>
          </template>
          <template v-else>按记忆曲线 + 错词池自动排今天的单词任务</template>
        </div>
        <div class="dt-sections">
          <div class="dt-section wrong" @click="openDailyTask('wrong')">
            <span class="ds-dot"></span>
            <span class="ds-name">错词复习</span>
            <b class="ds-num">{{ dailyTask.wrong_count }}</b>
            <span class="ds-tip">记错的维度</span>
            <span class="ds-go">开始 ›</span>
          </div>
          <div class="dt-section due" @click="openDailyTask('due')">
            <span class="ds-dot"></span>
            <span class="ds-name">到期复习</span>
            <b class="ds-num">{{ dailyTask.due_count }}</b>
            <span class="ds-tip">记忆曲线到期</span>
            <span class="ds-go">开始 ›</span>
          </div>
          <div class="dt-section new" @click="openDailyTask('new')">
            <span class="ds-dot"></span>
            <span class="ds-name">新词学习</span>
            <b class="ds-num">{{ dailyTask.new_count }}</b>
            <span class="ds-tip">今天学新词</span>
            <span class="ds-go">开始 ›</span>
          </div>
        </div>
      </div>

      <!-- 筛选条件 -->
      <div class="filters">
        <el-input
          v-model="filters.keyword"
          placeholder="搜索单词"
          clearable
          @change="fetchWords"
          style="width: 180px"
        />
        <el-select v-if="subjectStore.isAllGrade" v-model="filters.grade" placeholder="年级" clearable @change="fetchWords" style="width: 120px">
          <el-option v-for="g in gradeOptions" :key="g.value" :label="g.label" :value="g.value" />
        </el-select>
        <el-select v-model="filters.semester" placeholder="学期" clearable @change="fetchWords" style="width: 100px">
          <el-option label="上学期" :value="1" />
          <el-option label="下学期" :value="2" />
        </el-select>
        <el-select v-model="filters.tag_id" placeholder="标签" clearable @change="fetchWords" style="width: 150px">
          <el-option v-for="t in allTags" :key="t.id" :label="t.name" :value="t.id" />
        </el-select>
      </div>

      <!-- 正确率等级快速筛选 -->
      <div class="accuracy-level-filter" style="margin-top: 10px">
        <el-tag
          v-for="level in accuracyLevelOptions"
          :key="level.value"
          :type="filters.accuracy_level === level.value ? 'primary' : 'info'"
          class="accuracy-level-tag"
          @click="toggleAccuracyLevel(level.value)"
          style="cursor: pointer; margin-right: 8px"
        >
          {{ level.label }}
        </el-tag>
      </div>

      <!-- 单词列表 -->
      <el-table
        ref="tableRef"
        :data="words.items"
        stripe
        style="width: 100%; margin-top: 20px"
        @selection-change="handleSelectionChange"
        @sort-change="handleSortChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="english" label="英文" width="210">
          <template #default="{ row }">
            <div class="word-cell">
              <span class="word-english">{{ row.english }}</span>
              <el-button class="audio-btn-table" @click.stop="playWordAudio(row.id)" :loading="isAudioLoading(row.id)" circle>
                <span v-if="!isAudioLoading(row.id)">🔊</span>
              </el-button>
            </div>
          </template>
        </el-table-column>
        <el-table-column label="中文" min-width="200">
          <template #default="{ row }">
            <span class="cn-wrap">
              {{ row.chinese }}
              <el-button v-if="dimConfigForm.zhReadAloud" size="small" text class="zh-speak-btn" title="朗读中文" @click.stop="speakZh(row.chinese)">🔊</el-button>
              <span v-if="zhPinyin(row.chinese)" class="cn-pinyin">{{ zhPinyin(row.chinese) }}</span>
            </span>
          </template>
        </el-table-column>
        <el-table-column prop="phonetic" label="音标" width="150">
          <template #default="{ row }">
            <span class="phonetic">{{ row.phonetic || '-' }}</span>
          </template>
        </el-table-column>
        <el-table-column label="属性" width="150">
          <template #default="{ row }">
            <el-tag v-if="row.grade" :style="{ fontSize: '14px' }">{{ row.grade }}年级</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="复习" width="100">
          <template #default="{ row }">
            <span class="review-info">
              <span class="correct">{{ row.correct_count || 0 }}</span> /
              <span class="total">{{ row.review_count || 0 }}</span>
            </span>
          </template>
        </el-table-column>
        <el-table-column label="正确率" width="120" sortable prop="accuracy">
          <template #default="{ row }">
            <span :style="{ color: getAccuracyColor(row) }">{{ getAccuracyText(row) }}</span>
            <el-tag v-if="row.accuracy_level" :type="getAccuracyLevelTagType(row.accuracy_level)" :style="{ marginLeft: '5px', fontSize: '14px' }">
              {{ getAccuracyLevelText(row.accuracy_level) }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="120" fixed="right">
          <template #default="{ row }">
            <el-button type="info" size="default" @click="viewDetail(row)">详情</el-button>
          </template>
        </el-table-column>
      </el-table>

      <!-- 分页 -->
      <div class="pagination">
        <el-pagination
          v-model:current-page="pagination.page"
          v-model:page-size="pagination.limit"
          :page-sizes="[10, 20, 50, 100]"
          :total="words.total"
          layout="total, sizes, prev, pager, next"
          @change="fetchWords"
        />
      </div>
    </el-card>

    <!-- 详情弹窗 -->
    <el-dialog v-model="detailVisible" title="单词详情" width="600px">
      <el-tabs v-if="detailVisible" v-model="activeTab">
        <el-tab-pane label="基本信息" name="info">
          <el-form label-width="80px" size="default">
            <el-form-item label="英文">
              {{ detailWord.english }}
              <el-button class="audio-btn" @click="playWordAudio(detailWord.id)" :loading="isAudioLoading(detailWord.id)" size="small">🔊</el-button>
            </el-form-item>
            <el-form-item label="中文">
              {{ detailWord.chinese }}
              <el-button v-if="dimConfigForm.zhReadAloud" size="small" text class="zh-speak-btn" title="朗读中文" @click="speakZh(detailWord.chinese)">🔊</el-button>
              <span v-if="zhPinyin(detailWord.chinese)" class="cn-pinyin">{{ zhPinyin(detailWord.chinese) }}</span>
            </el-form-item>
            <el-form-item label="音标">{{ detailWord.phonetic || '-' }}</el-form-item>
            <el-form-item label="年级">{{ detailWord.grade ? detailWord.grade + '年级' : '-' }}</el-form-item>
            <el-form-item label="学期">{{ detailWord.semester === 1 ? '上学期' : detailWord.semester === 2 ? '下学期' : '-' }}</el-form-item>
            <el-form-item label="标签">
              <el-tag v-for="t in detailWord.tags" :key="t.id" style="margin-right: 5px">{{ t.name }}</el-tag>
              <span v-if="!detailWord.tags || detailWord.tags.length === 0">-</span>
            </el-form-item>
            <el-form-item label="拼读规律" v-if="detailWord.phonetic_rule">{{ detailWord.phonetic_rule }}</el-form-item>
            <el-form-item label="词根词源" v-if="detailWord.word_root">{{ detailWord.word_root }}</el-form-item>
            <el-form-item label="联想词" v-if="detailWord.related_words && detailWord.related_words.length">
              <el-tag
                v-for="(rw, i) in detailWord.related_words"
                :key="i"
                style="margin-right: 5px; cursor: pointer"
                @click="searchRelatedWord(rw)"
              >{{ rw.en || rw.english }}（{{ rw.cn || rw.chinese }}）</el-tag>
            </el-form-item>
            <el-form-item label="复习次数">{{ detailWord.review_count || 0 }}</el-form-item>
            <el-form-item label="正确次数">{{ detailWord.correct_count || 0 }}</el-form-item>
            <el-form-item label="正确率">{{ getAccuracyText(detailWord) }}</el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="记忆曲线" name="curve">
          <div v-if="memoryCurve" class="memory-curve">
            <!-- 阶段进度条 -->
            <div class="phase-bar">
              <div class="phase-track">
                <div
                  class="phase-dot"
                  v-for="(phase, idx) in ['新学', '在途', '遗忘点', '牢记']"
                  :key="phase"
                  :class="{ active: memoryCurve.learning_phase === phase }"
                  :style="{ left: phasePosition[phase] + '%', borderColor: memoryCurve.learning_phase === phase ? phaseColors[phase] : '#ddd' }"
                >
                  {{ phase }}
                </div>
              </div>
            </div>

            <!-- 下次复习时间 -->
            <div class="next-review">
              <span v-if="memoryCurve.learning_phase === '遗忘点'">即将到期</span>
              <span v-else-if="memoryCurve.next_review_at">下次复习：{{ formatDate(memoryCurve.next_review_at) }}</span>
              <span v-else>暂未安排复习</span>
            </div>

            <!-- 复习历史 -->
            <div class="review-history">
              <div class="history-title">复习历史：</div>
              <div v-if="memoryCurve.review_history.length === 0" class="history-empty">暂无复习记录</div>
              <div v-else class="history-item">
                <span class="history-date">今天（待复习）</span>
              </div>
              <div v-for="(log, idx) in memoryCurve.review_history" :key="idx" class="history-item">
                <span class="history-date">{{ formatDate(log.reviewed_at) }}</span>
                <span v-if="log.is_correct" class="history-correct">正确</span>
                <span v-else class="history-wrong">错误 【{{ log.user_answer }}】</span>
              </div>
            </div>
          </div>
          <div v-else class="no-curve">加载中...</div>
        </el-tab-pane>
      </el-tabs>
      <template #footer>
        <el-button @click="detailVisible = false">关闭</el-button>
      </template>
    </el-dialog>

    <!-- 复习弹窗 -->
    <el-dialog v-model="reviewVisible" :title="reviewConfig.isDaily ? '今日任务 · ' + (DAILY_CATEGORY_NAMES[reviewConfig.dailyCategory] || '复习') : '单词复习'" width="1200px" :close-on-click-modal="false" class="review-dialog">
      <!-- 学习模式：先学后复习 -->
      <div v-if="reviewStep === 'learn'" class="learn-flow">
        <div class="learn-header">
          <span class="learn-title">{{ learnMode === 'daily' ? '📖 先学习，再复习' : '📖 单词学习' }}</span>
          <span class="learn-progress">{{ learnIndex + 1 }} / {{ learnWords.length }}</span>
        </div>
        <div class="learn-tip">{{ learnMode === 'daily' ? '把这一批词看一遍、听一遍，再开始复习' : '整页单词集中学习，不用一个个点开详情' }}</div>
        <div class="learn-card" v-if="learnWords.length">
          <div class="lc-english">
            {{ learnWord.english }}
            <el-button class="audio-btn" @click="playWordAudio(learnWord.word_id)" :loading="isAudioLoading(learnWord.word_id)">🔊</el-button>
          </div>
          <div class="lc-phonetic" v-if="learnWord.phonetic">/{{ learnWord.phonetic }}/</div>
          <div class="lc-chinese">
            {{ learnWord.chinese }}
            <el-button v-if="dimConfigForm.zhReadAloud" size="small" text class="zh-speak-btn" title="朗读中文" @click="speakZh(learnWord.chinese)">🔊</el-button>
            <span v-if="zhPinyin(learnWord.chinese)" class="cn-pinyin">{{ zhPinyin(learnWord.chinese) }}</span>
          </div>
          <div class="lc-section" v-if="learnWord.phonetic_rule">
            <div class="lc-section-label">🔤 拼读规律</div>
            <div class="lc-section-body">{{ learnWord.phonetic_rule }}</div>
          </div>
          <div class="lc-section" v-if="learnWord.word_root">
            <div class="lc-section-label">🔎 词根词源</div>
            <div class="lc-section-body">{{ learnWord.word_root }}</div>
          </div>
          <div class="lc-section" v-if="learnWord.related_words && learnWord.related_words.length">
            <div class="lc-section-label">🔗 联想词</div>
            <div class="lc-section-body">
              <el-tag v-for="(r, i) in learnWord.related_words" :key="i" style="margin-right: 6px; cursor: pointer" @click="playAudioByEnglish(r.en)">
                🔊 {{ r.en }} {{ r.cn }}
              </el-tag>
            </div>
          </div>
          <div class="lc-section" v-if="visibleSentences(learnWord).length">
            <div class="lc-section-label">💬 例句</div>
            <div class="lc-section-body">
              <div v-for="(s, i) in visibleSentences(learnWord)" :key="i" class="lc-ex">
                <div class="lc-ex-en">{{ s.en }} <el-button size="small" text class="zh-speak-btn" title="朗读句子" @click.stop="speakEn(s.en)">🔊</el-button></div>
                <div class="lc-ex-zh" v-if="sentenceZhVisible()">{{ s.zh }}</div>
              </div>
            </div>
          </div>
        </div>
        <div class="learn-nav">
          <el-button :disabled="learnIndex === 0" @click="learnIndex--">← 上一张</el-button>
          <el-button :disabled="learnIndex >= learnWords.length - 1" @click="learnIndex++">下一张 →</el-button>
        </div>
        <div class="learn-footer">
          <el-button v-if="learnMode === 'daily'" type="primary" size="large" @click="startLearnPractice">开始复习 ›</el-button>
          <el-button v-else type="primary" size="large" @click="reviewVisible = false">完成</el-button>
          <span v-if="learnMode === 'daily'" class="learn-skip" @click="startLearnPractice">跳过学习直接复习</span>
        </div>
      </div>
      <div v-if="reviewStep === 'question'" class="review-question">
        <div class="question-header">
          <span class="progress">{{ currentIndex + 1 }} / {{ reviewQuestions.length }}</span>
          <span v-if="currentQuestion.dimension" class="dim-tag" :class="currentQuestion.dimension">{{ dimName(currentQuestion.dimension) }}</span>
          <span class="timer">用时: {{ Math.floor(reviewElapsed / 60) }}:{{ String(reviewElapsed % 60).padStart(2, '0') }}</span>
        </div>

        <div class="question-content">
          <!-- 学习新词：展示 词/音标/拼读/词根 + 认得题 -->
          <div v-if="currentQuestion.is_new" class="new-word-learn">
            <div class="nw-english">
              {{ currentQuestion.english }}
              <el-button class="audio-btn" @click="playWordAudio(currentQuestion.word_id)" :loading="isAudioLoading(currentQuestion.word_id)">🔊</el-button>
            </div>
            <div class="nw-meta">
              <span v-if="currentQuestion.phonetic" class="nw-phonetic">/{{ currentQuestion.phonetic }}/</span>
            </div>
            <div class="nw-root" v-if="currentQuestion.word_root">
              <span class="nw-root-label">🔎 词根词源</span> {{ currentQuestion.word_root }}
            </div>
            <div class="nw-root" v-if="currentQuestion.phonetic_rule">
              <span class="nw-root-label">🔤 拼读规律</span> {{ currentQuestion.phonetic_rule }}
            </div>
            <div v-if="visibleSentences(currentQuestion).length" class="nw-example">
              <div class="nw-root">
                <span class="nw-root-label">💬 例句</span>
                <span class="nw-ex-hint">听一听，猜猜意思（不显示中文，练听力理解）</span>
              </div>
              <div v-for="(s, i) in visibleSentences(currentQuestion)" :key="i" class="nw-ex-item">
                <span class="nw-ex-en">{{ s.en }}</span>
                <el-button size="small" text class="zh-speak-btn" title="朗读句子" @click.stop="speakEn(s.en)">🔊</el-button>
              </div>
            </div>
            <div class="nw-question">认一认：选出对应的中文意思<el-button v-if="dimConfigForm.zhReadAloud" size="small" text class="zh-speak-btn" title="朗读题目" @click.stop="speakZh('认一认：选出对应的中文意思')">🔊</el-button></div>
            <el-radio-group v-model="selectedOption" @change="submitAnswer">
              <el-radio v-for="(opt, idx) in currentQuestion.options" :key="idx" :value="opt" :disabled="currentQuestion.correct !== undefined">
                <span class="opt-cn">{{ opt }}<el-button v-if="dimConfigForm.zhReadAloud" size="small" text class="zh-speak-btn" title="朗读中文" @click.stop="speakZh(opt)">🔊</el-button></span>
                <span v-if="zhPinyin(opt)" class="cn-pinyin">{{ zhPinyin(opt) }}</span>
              </el-radio>
            </el-radio-group>
          </div>

          <!-- 默写模式：显示中文 + 喇叭按钮 + 字母格输入（说得维度） -->
          <div v-else-if="currentType === 1" class="dictation">
            <div class="chinese" :style="{ fontSize: chineseFontSize }">
              {{ currentQuestion.chinese }}
              <el-button v-if="dimConfigForm.zhReadAloud" size="small" text class="zh-speak-btn zh-speak-inline" title="朗读中文" @click="speakZh(currentQuestion.chinese)">🔊</el-button>
              <span v-if="zhPinyin(currentQuestion.chinese)" class="cn-pinyin">{{ zhPinyin(currentQuestion.chinese) }}</span>
            </div>
            <div class="audio-row">
              <el-button class="audio-btn" @click="playWordAudio(currentQuestion.word_id)" :loading="isAudioLoading(currentQuestion.word_id)">🔊</el-button>
            </div>
            <div class="hint-box">
              <div class="hint">提示：{{ letterBlankCount }}个字母</div>
            </div>
            <div
              ref="letterInputBoxRef"
              class="letter-input"
              tabindex="0"
              @click="focusLetterInput"
              @keydown="handleLetterKeydown"
            >
              <div class="letter-cells">
                <div
                  v-for="(cell, i) in dictationCells"
                  :key="i"
                  class="letter-cell"
                  :class="{
                    fixed: cell.fixed,
                    filled: !!letterAnswers[i],
                    active: i === activeLetterIdx && currentQuestion.correct === undefined,
                    correct: currentQuestion.correct === true && !cell.fixed,
                    wrong: currentQuestion.correct === false && !cell.fixed
                  }"
                >
                  {{ cell.fixed ? cell.char : (letterAnswers[i] || '') }}
                </div>
              </div>
              <input
                ref="letterInputRef"
                class="letter-hidden-input"
                autocomplete="off"
                autocapitalize="off"
                spellcheck="false"
              />
            </div>
          </div>

          <!-- 选择模式：显示英文 + 喇叭按钮（认得维度） -->
          <div v-else-if="currentType === 2" class="choice">
            <div class="english">
              {{ currentQuestion.english }}
              <el-button class="audio-btn" @click="playWordAudio(currentQuestion.word_id)" :loading="isAudioLoading(currentQuestion.word_id)">🔊</el-button>
            </div>
            <el-radio-group v-model="selectedOption" @change="submitAnswer">
              <el-radio v-for="(opt, idx) in currentQuestion.options" :key="idx" :value="opt" :disabled="currentQuestion.correct !== undefined">
                <span class="opt-cn">{{ opt }}<el-button v-if="dimConfigForm.zhReadAloud" size="small" text class="zh-speak-btn" title="朗读中文" @click.stop="speakZh(opt)">🔊</el-button></span>
                <span v-if="zhPinyin(opt)" class="cn-pinyin">{{ zhPinyin(opt) }}</span>
              </el-radio>
            </el-radio-group>
          </div>

          <!-- 听音选中文：喇叭按钮 + 中文选项（听得维度） -->
          <div v-else-if="currentType === 4" class="listening-choice">
            <div class="audio-controls">
              <el-button @click="playWordAudio(currentQuestion.word_id)" :loading="isAudioLoading(currentQuestion.word_id)" class="audio-btn-large" type="primary" size="large">
                🔊 播放发音
              </el-button>
              <el-button @click="playWordAudio(currentQuestion.word_id)" :loading="isAudioLoading(currentQuestion.word_id)" class="audio-btn-replay" size="small">
                重播
              </el-button>
            </div>
            <div class="lc-tip">听发音，选出对应的中文意思<el-button v-if="dimConfigForm.zhReadAloud" size="small" text class="zh-speak-btn" title="朗读题目" @click.stop="speakZh('听发音，选出对应的中文意思')">🔊</el-button></div>
            <el-radio-group v-model="selectedOption" @change="submitAnswer">
              <el-radio v-for="(opt, idx) in currentQuestion.options" :key="idx" :value="opt" :disabled="currentQuestion.correct !== undefined">
                <span class="opt-cn">{{ opt }}<el-button v-if="dimConfigForm.zhReadAloud" size="small" text class="zh-speak-btn" title="朗读中文" @click.stop="speakZh(opt)">🔊</el-button></span>
                <span v-if="zhPinyin(opt)" class="cn-pinyin">{{ zhPinyin(opt) }}</span>
              </el-radio>
            </el-radio-group>
          </div>

          <!-- 听力模式：仅喇叭按钮 + 输入框（写得维度） -->
          <div v-else class="listening">
            <div class="audio-controls">
              <el-button @click="playWordAudio(currentQuestion.word_id)" :loading="isAudioLoading(currentQuestion.word_id)" class="audio-btn-large" type="primary" size="large">
                🔊 播放发音
              </el-button>
              <el-button @click="playWordAudio(currentQuestion.word_id)" :loading="isAudioLoading(currentQuestion.word_id)" class="audio-btn-replay" size="small">
                重播
              </el-button>
            </div>
            <div class="hint-box">
              <div class="hint">提示：{{ currentQuestion.word_length }}个字母</div>
            </div>
            <el-input
              ref="answerInputRef"
              v-model="userAnswer"
              placeholder="输入听到的英文单词"
              @keyup.enter="submitAnswer"
              :disabled="currentQuestion.correct !== undefined"
              class="answer-input"
            />
          </div>
        </div>

        <div class="question-actions">
          <el-button type="danger" @click="terminateReview">终止答题</el-button>
          <el-button v-if="currentQuestion.correct === undefined" type="primary" @click="submitAnswer">提交</el-button>
          <el-button v-else type="success" @click="finishReview">完成</el-button>
        </div>
      </div>

      <div v-else-if="reviewStep === 'result'" class="review-result">
        <!-- 顶部统计区 -->
        <div class="result-header">
          <div class="accuracy-display">
            <div class="accuracy-big">{{ reviewResult.accuracy }}%</div>
            <div class="accuracy-label">正确率</div>
          </div>
          <div class="stats-panel">
            <div class="stat-item">
              <span class="stat-value">{{ reviewResult.total }}</span>
              <span class="stat-label">总题数</span>
            </div>
            <div class="stat-item correct">
              <span class="stat-value">{{ reviewResult.correct }}</span>
              <span class="stat-label">正确</span>
            </div>
            <div class="stat-item error">
              <span class="stat-value">{{ reviewResult.error }}</span>
              <span class="stat-label">错误</span>
            </div>
            <div class="stat-item">
              <span class="stat-value">{{ Math.floor(reviewResult.duration / 60) }}:{{ String(reviewResult.duration % 60).padStart(2, '0') }}</span>
              <span class="stat-label">用时</span>
            </div>
          </div>
        </div>

        <!-- 错误单词列表 -->
        <div v-if="reviewResult.error > 0" class="error-word-list">
          <div class="error-words-scroll">
            <div v-for="(q, idx) in reviewQuestions.filter(q => !q.correct)" :key="idx" class="error-word-item">
              <div class="correct-side">
                <span class="correct-en">
                  {{ q.english }}
                  <el-button class="audio-btn" @click="playWordAudio(q.word_id)" :loading="isAudioLoading(q.word_id)" size="small">🔊</el-button>
                </span>
                <span class="correct-cn">{{ q.chinese }}</span>
              </div>
              <div class="wrong-side">
                <span class="wrong-tag">错误</span>
                <span class="wrong-answer">{{ q.userAnswer || '(未作答)' }}</span>
              </div>
            </div>
          </div>
        </div>

        <el-button type="primary" @click="reviewVisible = false" class="finish-btn">完成</el-button>
      </div>
    </el-dialog>

    <!-- 记忆维度配置 -->
    <el-dialog v-model="dimConfigVisible" title="记忆设置（科学记忆）" width="480px">
      <p class="dim-config-tip">单词要「记住」，按 4 个维度记忆（认得 → 听得 → 说得 → 写得，从易到难）。低年级或刚开始可只开部分维度。</p>
      <div class="dim-config-list">
        <div class="dim-config-item">
          <el-checkbox v-model="dimConfigForm.recognize" border>👀 认得（英→中）</el-checkbox>
        </div>
        <div class="dim-config-item">
          <el-checkbox v-model="dimConfigForm.listen" border>👂 听得（听音选中文）</el-checkbox>
        </div>
        <div class="dim-config-item">
          <el-checkbox v-model="dimConfigForm.speak" border>🗣 说得（中→英）</el-checkbox>
        </div>
        <div class="dim-config-item">
          <el-checkbox v-model="dimConfigForm.write" border>✍️ 写得（听写）</el-checkbox>
        </div>
        <div class="dim-config-item dim-config-row">
          <span class="dc-label">每词每轮记忆维度</span>
          <el-radio-group v-model="dimConfigForm.perWordDims">
            <el-radio :value="1">1 个（推荐，间隔轮转）</el-radio>
            <el-radio :value="2">2 个</el-radio>
          </el-radio-group>
          <div class="dc-hint">1 个词只记最弱的一维，四维隔天轮转，记忆更牢、不枯燥</div>
        </div>
        <div class="dim-config-item dim-config-row">
          <span class="dc-label">单类任务词数上限</span>
          <el-radio-group v-model="dimConfigForm.categoryCap">
            <el-radio :value="10">10</el-radio>
            <el-radio :value="15">15（推荐）</el-radio>
            <el-radio :value="20">20</el-radio>
            <el-radio :value="30">30</el-radio>
          </el-radio-group>
          <div class="dc-hint">错词复习/到期复习各最多这么多词，避免一次任务过重</div>
        </div>
        <div class="dim-config-item dim-config-row">
          <span class="dc-label">🔉 低年级辅助（识字量少时开启）</span>
          <div class="dc-check-row">
            <el-checkbox v-model="dimConfigForm.showPinyin">🔡 中文显示拼音</el-checkbox>
            <el-checkbox v-model="dimConfigForm.zhReadAloud">🔊 中文可朗读（点中文旁喇叭）</el-checkbox>
            <el-checkbox v-model="dimConfigForm.autoRead">📖 自动带读（学习时自动朗读 英语→中文→词根）</el-checkbox>
          </div>
          <div class="dc-hint">不认识的字看拼音、点喇叭听读音；自动带读像老师一样带着读一遍</div>
        </div>
        <div class="dim-config-item dim-config-row">
          <span class="dc-label">📚 学习模式（例句深浅）</span>
          <el-radio-group v-model="dimConfigForm.learnMode">
            <el-radio value="easy">入门（只看词）</el-radio>
            <el-radio value="standard">标准（1 条例句）</el-radio>
            <el-radio value="advanced">进阶（2 条例句）</el-radio>
          </el-radio-group>
          <div class="dc-hint">例句把单词放进句子里学，不孤立背词；跟读时先听英语例句、再看中文</div>
          <div v-if="dimConfigForm.learnMode === 'advanced'" class="dc-check-row">
            <el-checkbox v-model="dimConfigForm.showSentenceZh">例句显示中文翻译（关掉=只看英文练理解）</el-checkbox>
          </div>
        </div>
      </div>
      <template #footer>
        <el-button @click="dimConfigVisible = false">取消</el-button>
        <el-button type="primary" @click="saveDimConfig">保存</el-button>
      </template>
    </el-dialog>

    <!-- 打印弹窗 -->
    <el-dialog v-model="printDialogVisible" title="打印默写" width="400px">
      <el-form :model="printForm" label-width="80px">
        <el-form-item label="单词数量">
          <el-input-number v-model="printForm.count" :min="5" :max="100" />
        </el-form-item>
        <el-form-item v-if="subjectStore.isAllGrade" label="年级筛选">
          <el-select v-model="printForm.grade" placeholder="全部" clearable style="width: 100%">
            <el-option v-for="g in gradeOptions" :key="g.value" :label="g.label" :value="g.value" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="printDialogVisible = false">取消</el-button>
        <el-button type="primary" @click="generatePrintPdf">生成PDF</el-button>
      </template>
    </el-dialog>

  </div>
</template>

<script setup>
import { ref, reactive, onMounted, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Edit, Printer, Upload, Reading } from '@element-plus/icons-vue'
import { wordApi } from '@/api/word'
import { questionApi } from '@/api/question'
import { motivationApi } from '@/api/motivation'
import { useSubjectStore } from '@/stores/subject'
import { useKidStore } from '@/stores/kid'

const route = useRoute()
const subjectStore = useSubjectStore()
const kidStore = useKidStore()
const words = ref({ total: 0, items: [] })
const allTags = ref([])
const filters = reactive({
  keyword: '',
  grade: null,
  semester: null,
  tag_id: null,
  accuracy_level: null,
  sort_by: null,
  sort_order: 'desc',
})
const pagination = reactive({
  page: 1,
  limit: 20,
})

const dialogVisible = ref(false)
const dialogTitle = ref('新增单词')
const isEdit = ref(false)
const currentWordId = ref(null)

const form = reactive({
  english: '',
  chinese: '',
  phonetic: '',
  grade: null,
  semester: null,
  tag_ids: [],
})

const gradeOptions = [
  { label: '一年级', value: 1 },
  { label: '二年级', value: 2 },
  { label: '三年级', value: 3 },
  { label: '四年级', value: 4 },
  { label: '五年级', value: 5 },
  { label: '六年级', value: 6 },
  { label: '初一', value: 7 },
  { label: '初二', value: 8 },
  { label: '初三', value: 9 },
  { label: '高一', value: 10 },
  { label: '高二', value: 11 },
  { label: '高三', value: 12 },
]

// 正确率等级选项
const accuracyLevelOptions = ref([
  { label: '全部', value: null },
  { label: '新词', value: 'new' },
  { label: '需加强', value: 'weak' },
  { label: '薄弱', value: 'learning' },
  { label: '一般', value: 'good' },
  { label: '掌握', value: 'mastered' },
])

// 切换正确率等级筛选
const toggleAccuracyLevel = (level) => {
  if (filters.accuracy_level === level) {
    filters.accuracy_level = null
  } else {
    filters.accuracy_level = level
  }
  pagination.page = 1
  fetchWords()
}

// 复习相关
const reviewVisible = ref(false)
const reviewStarting = ref(false) // 防止重复点击开始复习
const reviewStep = ref('config')
// 学习模式（先学后练）：学词卡流
const learnWords = ref([])
const learnIndex = ref(0)
const learnMode = ref('daily') // daily=今日任务先学习 / list=列表页学习本页
const learnWord = computed(() => learnWords.value[learnIndex.value] || {})
// 从题目列表提取去重学习词（同词多维度只学一次）
const buildLearnWords = (questions) => {
  const seen = new Set()
  const out = []
  for (const q of questions) {
    if (seen.has(q.word_id)) continue
    seen.add(q.word_id)
    out.push({
      word_id: q.word_id,
      english: q.english,
      chinese: q.chinese,
      phonetic: q.phonetic,
      phonetic_rule: q.phonetic_rule,
      word_root: q.word_root,
      related_words: q.related_words || [],
      example_sentences: q.example_sentences || [],
    })
  }
  return out
}
// 列表页「学习本页」：整页单词批量学习
const openLearnPage = () => {
  const items = (words.value.items || []).filter(w => w.english)
  if (!items.length) {
    ElMessage.info('当前没有可学习的单词')
    return
  }
  if (dimConfigForm.showPinyin) fetchPinyin(items.map(w => w.chinese).filter(Boolean))
  learnWords.value = items.map(w => ({
    word_id: w.id,
    english: w.english,
    chinese: w.chinese,
    phonetic: w.phonetic,
    phonetic_rule: w.phonetic_rule,
    word_root: w.word_root,
    related_words: w.related_words || [],
    example_sentences: w.example_sentences || [],
  }))
  learnIndex.value = 0
  learnMode.value = 'list'
  reviewStep.value = 'learn'
  reviewVisible.value = true
  // 自动带读第一张
  setTimeout(() => autoTeach(learnWord.value), 500)
}
// 从学习模式进入复习（今日任务）
const startLearnPractice = () => {
  // 停止自动带读
  ++teachToken
  window.speechSynthesis.cancel()
  if (learnMode.value === 'list') {
    reviewVisible.value = false
    return
  }
  startDailyQuestion()
}
// 关闭学习/复习弹窗时停止带读
watch(reviewVisible, (v) => {
  if (!v) {
    ++teachToken
    window.speechSynthesis.cancel()
  }
})
// 学习卡自动带读：切卡时自动朗读新词（英语→中文→词根词源）
watch(learnIndex, () => {
  autoTeach(learnWord.value)
})
const reviewConfig = reactive({
  count: 20,
  grade: null,
  type: 1,
  isDaily: false, // 今日任务模式：四维混合出题
  dailyCategory: 'due', // wrong/due/new
})
const reviewQuestions = ref([])
const currentIndex = ref(0)
// 当前题渲染类型：今日任务混合模式按维度映射，普通复习用配置类型
const currentType = computed(() => {
  const q = reviewQuestions.value[currentIndex.value]
  if (q && q.dimension) return DIM_TYPE[q.dimension] || reviewConfig.type
  return reviewConfig.type
})
const userAnswer = ref('')
const letterAnswers = ref([])
const activeLetterIdx = ref(0)
const letterInputRef = ref(null)
const letterInputBoxRef = ref(null)
const autoPlayToken = ref(0)
const selectedOption = ref('')
const currentSessionId = ref(null)
// 正在加载/播放音频的单词 id（按单词隔离 loading，避免点击一个全部图标转圈）
const audioLoadingMap = reactive({})
const isAudioLoading = (wordId) => !!audioLoadingMap[wordId]
const reviewResult = reactive({
  total: 0,
  correct: 0,
  error: 0,
  accuracy: 0,
  duration: 0,
})

// ===== 今日任务（四维记忆）=====
const DIMENSION_NAMES = { recognize: '认得', listen: '听得', speak: '说得', write: '写得' }
const DIM_TYPE = { recognize: 2, listen: 4, speak: 1, write: 3 } // 维度 → 复习题型
const dailyTask = reactive({ loaded: false, total: 0, wrong_count: 0, due_count: 0, new_count: 0, enabled_dimensions: ['recognize', 'listen', 'speak', 'write'] })
const dimConfigVisible = ref(false)
const dimConfigForm = reactive({ recognize: true, listen: true, speak: true, write: true, perWordDims: 1, categoryCap: 15, showPinyin: false, zhReadAloud: false, autoRead: true, learnMode: 'standard', showSentenceZh: true })
// 低年级辅助：中文 → 拼音缓存映射
const pinyinMap = reactive({})
const zhSpeaking = ref('') // 正在朗读的中文

const dimName = (d) => DIMENSION_NAMES[d] || d
const dimNames = (dims) => (dims || []).map(d => DIMENSION_NAMES[d] || d).join(' / ')

// 中文拼音（批量请求 /api/zh/pinyin）
async function fetchPinyin(texts) {
  const need = [...new Set((texts || []).filter(t => t && !pinyinMap[t]))]
  if (!need.length || !dimConfigForm.showPinyin) return
  try {
    const res = await fetch(`/api/zh/pinyin?texts=${encodeURIComponent(need.join(','))}`)
    if (!res.ok) return
    const data = await res.json()
    for (const [t, py] of Object.entries(data.texts || {})) pinyinMap[t] = py
  } catch (e) { /* 忽略拼音失败 */ }
}
const zhPinyin = (t) => dimConfigForm.showPinyin ? (pinyinMap[t] || '') : ''

// 中文朗读（SpeechSynthesis zh-CN）；force=true 时忽略 zhReadAloud 开关（自动带读用）
function speakZh(text, opts = {}) {
  const force = !!opts.force
  if ((!force && !dimConfigForm.zhReadAloud) || !text) return Promise.resolve()
  if (!('speechSynthesis' in window)) {
    if (!force) ElMessage.warning('当前浏览器不支持中文朗读')
    return Promise.resolve()
  }
  if (!force && zhSpeaking.value === text) {
    window.speechSynthesis.cancel()
    zhSpeaking.value = ''
    return Promise.resolve()
  }
  window.speechSynthesis.cancel()
  const u = new SpeechSynthesisUtterance(text)
  u.lang = 'zh-CN'
  u.rate = 0.9
  const voices = window.speechSynthesis.getVoices()
  const zh = voices.find(v => v.lang && v.lang.toLowerCase().startsWith('zh'))
  if (zh) u.voice = zh
  return new Promise((resolve) => {
    u.onend = () => { zhSpeaking.value = ''; resolve() }
    u.onerror = () => { zhSpeaking.value = ''; resolve() }
    zhSpeaking.value = text
    window.speechSynthesis.speak(u)
  })
}

// 英文朗读（SpeechSynthesis en-US；例句发音用，不走 TTS 文件缓存，避免污染 audio_dir）
function speakEn(text) {
  if (!text || !('speechSynthesis' in window)) return
  window.speechSynthesis.cancel()
  const u = new SpeechSynthesisUtterance(text)
  u.lang = 'en-US'
  u.rate = 0.85
  const voices = window.speechSynthesis.getVoices()
  const en = voices.find(v => v.lang && v.lang.toLowerCase().startsWith('en'))
  if (en) u.voice = en
  window.speechSynthesis.speak(u)
}

// 按学习模式取可见例句：入门=无、标准=1 条、进阶=2 条
const visibleSentences = (word) => {
  const list = (word?.example_sentences || []).slice()
  if (!list.length || dimConfigForm.learnMode === 'easy') return []
  const max = dimConfigForm.learnMode === 'advanced' ? 2 : 1
  return list.slice(0, max)
}
// 例句中文翻译显示：进阶模式可独立关掉（只看英文练理解）
const sentenceZhVisible = () => dimConfigForm.learnMode !== 'advanced' || dimConfigForm.showSentenceZh

// 自动带读：学习卡自动依次朗读 英语 → 中文 → 词根词源（老师带学，可配置关闭）
let teachToken = 0
async function autoTeach(word) {
  if (!dimConfigForm.autoRead || !word?.english) return
  const token = ++teachToken
  window.speechSynthesis.cancel()
  try {
    await playWordAudio(word.word_id) // 1. 英语
    if (token !== teachToken) return
    await speakZh(word.chinese, { force: true }) // 2. 中文
    if (token !== teachToken) return
    if (word.word_root) await speakZh(word.word_root, { force: true }) // 3. 词根词源
  } catch (e) { /* 带读失败不打断学习 */ }
}

// 当前小孩的维度配置（localStorage 按小孩存）
function loadDimConfig() {
  const kidId = kidStore.activeKid?.id || 'default'
  try {
    const saved = JSON.parse(localStorage.getItem(`easyfix_dims_${kidId}`) || 'null')
    if (saved) {
      dimConfigForm.recognize = saved.recognize !== false
      dimConfigForm.listen = saved.listen !== false
      dimConfigForm.speak = saved.speak !== false
      dimConfigForm.write = saved.write !== false
      dimConfigForm.perWordDims = saved.perWordDims || 1
      dimConfigForm.categoryCap = saved.categoryCap || 15
      dimConfigForm.showPinyin = !!saved.showPinyin
      dimConfigForm.zhReadAloud = !!saved.zhReadAloud
      dimConfigForm.autoRead = saved.autoRead !== false
      dimConfigForm.learnMode = saved.learnMode || 'standard'
      dimConfigForm.showSentenceZh = saved.showSentenceZh !== false
    }
  } catch (e) { /* 默认 */ }
  dailyTask.enabled_dimensions = enabledDims()
}
const enabledDims = () => {
  const dims = []
  if (dimConfigForm.recognize) dims.push('recognize')
  if (dimConfigForm.listen) dims.push('listen')
  if (dimConfigForm.speak) dims.push('speak')
  if (dimConfigForm.write) dims.push('write')
  return dims.length ? dims : ['recognize']
}
const openDimConfig = () => { dimConfigVisible.value = true }
const saveDimConfig = () => {
  const kidId = kidStore.activeKid?.id || 'default'
  try {
    localStorage.setItem(`easyfix_dims_${kidId}`, JSON.stringify({
      recognize: dimConfigForm.recognize,
      listen: dimConfigForm.listen,
      speak: dimConfigForm.speak,
      write: dimConfigForm.write,
      perWordDims: dimConfigForm.perWordDims,
      categoryCap: dimConfigForm.categoryCap,
      showPinyin: dimConfigForm.showPinyin,
      zhReadAloud: dimConfigForm.zhReadAloud,
      autoRead: dimConfigForm.autoRead,
      learnMode: dimConfigForm.learnMode,
      showSentenceZh: dimConfigForm.showSentenceZh,
    }))
  } catch (e) { /* 忽略 */ }
  dailyTask.enabled_dimensions = enabledDims()
  dimConfigVisible.value = false
  loadDailyTask()
  if (dimConfigForm.showPinyin) {
    // 立即为当前列表词补拼音
    const texts = (words.value.items || []).map(w => w.chinese).filter(Boolean)
    fetchPinyin(texts)
  }
  ElMessage.success('记忆设置已保存，今日任务已按新配置更新')
}

async function loadDailyTask() {
  try {
    const params = { new_quota: 5, dimensions: enabledDims().join(','), per_word_dims: dimConfigForm.perWordDims, category_cap: dimConfigForm.categoryCap }
    if (kidStore.activeKid?.id) params.user_id = kidStore.activeKid.id
    const qs = Object.entries(params).map(([k, v]) => `${k}=${encodeURIComponent(v)}`).join('&')
    const res = await fetch(`/api/words/daily-task?${qs}`)
    if (!res.ok) return
    const data = await res.json()
    dailyTask.loaded = true
    dailyTask.total = data.total || 0
    dailyTask.wrong_count = data.wrong_count || 0
    dailyTask.due_count = data.due_count || 0
    dailyTask.new_count = data.new_count || 0
    dailyTask.enabled_dimensions = data.enabled_dimensions || enabledDims()
  } catch (e) { /* 静默 */ }
}

// 今日任务：按分类生成题目
// category: wrong=错词复习(错池词×错池维度优先) / due=到期复习(到期词×薄弱维度) / new=新词学习(学习卡)
const DAILY_CATEGORY_NAMES = { wrong: '错词复习', due: '到期复习', new: '新词学习' }
function buildDailyQuestions(data, category) {
  const qs = []
  const usedWordIds = new Set()
  const makeOptions = (word, poolWords, getLabel) => {
    const wrongs = poolWords.filter(w => w.word_id !== word.word_id)
    const opts = [word]
    for (const w of wrongs) {
      if (opts.length >= 4) break
      if (!opts.some(o => getLabel(o) === getLabel(w))) opts.push(w)
    }
    while (opts.length < 4 && poolWords.length) {
      const w = poolWords[Math.floor(Math.random() * poolWords.length)]
      if (!opts.some(o => getLabel(o) === getLabel(w))) opts.push(w)
    }
    return shuffleArr(opts.map(getLabel))
  }
  const all = [...(data.task || []), ...(data.new_words || [])]
  const pool = all
  const pushWord = (w, dims, isNew) => {
    usedWordIds.add(w.word_id)
    const dim = dims[0] || 'recognize'
    const type = DIM_TYPE[dim]
    const isChoice = type === 2 || type === 4
    qs.push({
      word_id: w.word_id,
      english: w.english,
      chinese: w.chinese,
      phonetic: w.phonetic,
      phonetic_rule: w.phonetic_rule,
      word_root: w.word_root,
      related_words: w.related_words,
      example_sentences: w.example_sentences || [],
      dimension: dim,
      is_new: isNew,
      ...(isChoice ? { options: makeOptions(w, pool, x => x.chinese) } : {}),
    })
  }

  if (category === 'new') {
    // 新词学习：学习卡（认一认）
    for (const w of data.new_words || []) pushWord(w, ['recognize'], true)
    return qs
  }

  for (const w of data.task || []) {
    const isWrong = category === 'wrong' ? !!w.in_attempt : !w.in_attempt
    if (!isWrong) continue
    let dims
    if (category === 'wrong') {
      // 错词复习：只记错过的维度（in_pool=true 的优先）
      dims = (Object.entries(w.dimensions || {}).filter(([d, v]) => v.in_pool).map(([d]) => d))
      if (!dims.length) dims = w.recommended_dimensions || ['recognize']
    } else {
      dims = w.recommended_dimensions || ['recognize']
    }
    for (const dim of dims) pushWord(w, [dim], false)
  }
  return qs
}

function shuffleArr(arr) {
  const a = [...arr]
  for (let i = a.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[a[i], a[j]] = [a[j], a[i]]
  }
  return a
}

// 打开今日任务某分类（先取 session_id，再按分类出题）
async function openDailyTask(category = 'due') {
  loadDimConfig()
  if (reviewStarting.value) return
  reviewStarting.value = true
  try {
    const params = { count: 10 }
    if (kidStore.activeKid?.id) params.user_id = kidStore.activeKid.id
    const { data } = await wordApi.startReview(params)
    currentSessionId.value = data.session_id

    const qp = { new_quota: 5, dimensions: enabledDims().join(','), per_word_dims: dimConfigForm.perWordDims, category_cap: dimConfigForm.categoryCap }
    if (kidStore.activeKid?.id) qp.user_id = kidStore.activeKid.id
    const qs = Object.entries(qp).map(([k, v]) => `${k}=${encodeURIComponent(v)}`).join('&')
    const res = await fetch(`/api/words/daily-task?${qs}`)
    const task = await res.json()
    const built = buildDailyQuestions(task, category)
    if (!built.length) {
      ElMessage.info(DAILY_CATEGORY_NAMES[category] + '已清空，明天再来吧')
      return
    }
    reviewQuestions.value = built.map(q => ({ ...q, correct: undefined }))
    reviewConfig.type = reviewQuestions.value[0]?.dimension === 'listen' ? 4 : (DIM_TYPE[reviewQuestions.value[0]?.dimension] || 2)
    reviewConfig.isDaily = true
    reviewConfig.dailyCategory = category
    // 先学习，再复习：进入学词卡流（去重展示本批词），点「开始复习」才进入测验
    learnWords.value = buildLearnWords(reviewQuestions.value)
    learnIndex.value = 0
    learnMode.value = 'daily'
    if (dimConfigForm.showPinyin) {
      fetchPinyin(learnWords.value.map(w => w.chinese).filter(Boolean))
    }
    reviewStep.value = 'learn'
    reviewVisible.value = true
    // 自动带读第一张
    setTimeout(() => autoTeach(learnWord.value), 500)
  } catch (error) {
    ElMessage.error('今日任务加载失败')
  } finally {
    reviewStarting.value = false
  }
}

// 今日任务从学习模式进入测验
function startDailyQuestion() {
  currentIndex.value = 0
  userAnswer.value = ''
  selectedOption.value = ''
  currentQuestion.value = reviewQuestions.value[0]
  if (dimConfigForm.showPinyin) {
    const q0 = currentQuestion.value
    fetchPinyin([...(q0.options || []), q0.chinese].filter(Boolean))
  }
  reviewStep.value = 'question'
  // 启动计时
  if (reviewTimer.value) clearInterval(reviewTimer.value)
  reviewStartTime.value = Date.now()
  reviewElapsed.value = 0
  reviewTimer.value = setInterval(() => {
    reviewElapsed.value = Math.floor((Date.now() - reviewStartTime.value) / 1000)
  }, 1000)
  // 听音/听写题自动播放
  if (currentQuestion.value.dimension === 'listen' || currentQuestion.value.dimension === 'write') {
    setTimeout(() => autoPlayWithReplay(currentQuestion.value.word_id), 400)
  }
}

// 复习计时器
const reviewStartTime = ref(null)
const reviewTimer = ref(null)
const reviewElapsed = ref(0) // 秒
const answerInputRef = ref(null)
const letterBlankCount = computed(() => {
  const cells = dictationCells.value
  return cells.filter(c => !c.fixed).length
})

// 长中文自适应字号，避免溢出
const chineseFontSize = computed(() => {
  const len = (currentQuestion.value?.chinese || '').length
  if (len <= 6) return '64px'
  if (len <= 10) return '48px'
  if (len <= 16) return '36px'
  if (len <= 24) return '28px'
  if (len <= 36) return '22px'
  return '18px'
})

// 默写字母格：空格/符号预填，字母留空
const dictationCells = computed(() => {
  const en = currentQuestion.value?.english || ''
  return en.split('').map(ch => ({
    char: ch,
    fixed: !/[a-zA-Z]/.test(ch),
  }))
})

const resetLetterInput = () => {
  letterAnswers.value = dictationCells.value.map(c => (c.fixed ? c.char : ''))
  const firstBlank = dictationCells.value.findIndex(c => !c.fixed)
  activeLetterIdx.value = firstBlank >= 0 ? firstBlank : 0
}

const focusLetterInput = () => {
  if (currentQuestion.value?.correct !== undefined) return
  letterInputBoxRef.value?.focus()
}

const fillBuiltAnswer = () => {
  // 按格子拼出完整答案（含预置空格/符号）
  return dictationCells.value
    .map((c, i) => (c.fixed ? c.char : (letterAnswers.value[i] || '')))
    .join('')
}

const handleLetterKeydown = (e) => {
  if (currentQuestion.value?.correct !== undefined) return

  if (e.key === 'Backspace') {
    e.preventDefault()
    const cells = dictationCells.value
    let idx = activeLetterIdx.value
    // 当前格有内容则清空；否则回退到上一个可填格
    if (idx < cells.length && !cells[idx].fixed && letterAnswers.value[idx]) {
      letterAnswers.value[idx] = ''
      return
    }
    let i = idx - 1
    while (i >= 0 && cells[i].fixed) i--
    if (i >= 0) {
      letterAnswers.value[i] = ''
      activeLetterIdx.value = i
    }
    return
  }

  if (e.key === 'Enter') {
    e.preventDefault()
    submitAnswer()
    return
  }

  if (/^[a-zA-Z]$/.test(e.key)) {
    e.preventDefault()
    const cells = dictationCells.value
    let idx = activeLetterIdx.value
    while (idx < cells.length && cells[idx].fixed) idx++
    if (idx >= cells.length) return
    letterAnswers.value[idx] = e.key.toLowerCase()
    // 跳到下一个可填格
    let next = idx + 1
    while (next < cells.length && cells[next].fixed) next++
    activeLetterIdx.value = Math.min(next, cells.length - 1)
  }
}

// 打印相关
const printDialogVisible = ref(false)
const printForm = reactive({
  count: 25,
  grade: null,
})

// 导入相关
const importDialogVisible = ref(false)
const importing = ref(false)
const uploadRef = ref()
const imageUploadRef = ref()
const importForm = reactive({
  mode: 'text',
  text: '',
  file: null,
  image: null,
  ocrText: '',
  parsedWords: [],  // 解析后的单词预览
  grade: null,
  semester: null,
  tag_ids: [],
})

const currentQuestion = ref({})
// 新词学习题：进入时自动带读（英语→中文→词根词源），同学习卡带读
watch(currentQuestion, (q) => {
  if (q && q.is_new && reviewStep.value === 'question' && dimConfigForm.autoRead) {
    setTimeout(() => autoTeach(q), 600)
  }
})
const tableRef = ref()
const selectedWords = ref([])

// 记忆曲线相关
const memoryCurve = ref(null)
const memoryCurveLoading = ref(false)

const fetchMemoryCurve = async (wordId) => {
  memoryCurveLoading.value = true
  try {
    const params = {}
    if (kidStore.activeKid?.id) params.user_id = kidStore.activeKid.id
    const { data } = await wordApi.getMemoryCurve(wordId, params)
    memoryCurve.value = data
  } catch (error) {
    console.error('获取记忆曲线失败:', error)
  } finally {
    memoryCurveLoading.value = false
  }
}

// 阶段对应的颜色
const phaseColors = {
  '新学': '#909399',
  '在途': '#409eff',
  '遗忘点': '#e6a23c',
  '牢记': '#67c23a'
}

// 阶段对应的进度位置
const phasePosition = {
  '新学': 12.5,
  '在途': 37.5,
  '遗忘点': 62.5,
  '牢记': 87.5
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  const month = date.getMonth() + 1
  const day = date.getDate()
  return `${month}月${day}日`
}

// 详情弹窗相关
const detailVisible = ref(false)
const detailWord = ref({})
const activeTab = ref('info')

const viewDetail = async (row) => {
  detailWord.value = row
  activeTab.value = 'info'
  memoryCurve.value = null
  detailVisible.value = true
  if (dimConfigForm.showPinyin && row.chinese) fetchPinyin([row.chinese])
  // 获取记忆曲线
  await fetchMemoryCurve(row.id)
}

// 点击联想词 → 搜索该词
const searchRelatedWord = (rw) => {
  detailVisible.value = false
  filters.keyword = rw.en || rw.english || ''
  pagination.page = 1
  fetchWords()
}

// 计算单词正确率
const getAccuracy = (row) => {
  if (!row.review_count || row.review_count === 0) return 0
  return (row.correct_count / row.review_count) * 100
}

// 获取正确率显示文本
const getAccuracyText = (row) => {
  if (!row.review_count || row.review_count === 0) return '--'
  return getAccuracy(row).toFixed(0) + '%'
}

// 获取正确率颜色（100%绿色，0%红色，渐变）
const getAccuracyColor = (row) => {
  if (!row.review_count || row.review_count === 0) return '#909399'
  const accuracy = getAccuracy(row)
  if (accuracy >= 100) return '#67c23a'  // 绿色
  if (accuracy <= 0) return '#f56c6c'    // 红色
  // 渐变色：从红到黄到绿
  if (accuracy < 50) {
    // 红到黄
    const ratio = accuracy / 50
    const r = 245
    const g = Math.round(67 + (183 - 67) * ratio)
    const b = Math.round(108 + (58 - 108) * ratio)
    return `rgb(${r}, ${g}, ${b})`
  } else {
    // 黄到绿
    const ratio = (accuracy - 50) / 50
    const r = Math.round(245 - (245 - 103) * ratio)
    const g = Math.round(183 + (194 - 183) * ratio)
    const b = Math.round(58 + (58 - 58) * ratio)
    return `rgb(${r}, ${g}, ${b})`
  }
}

// 获取正确率等级文字
const getAccuracyLevelText = (level) => {
  const map = {
    'new': '新词',
    'weak': '需加强',
    'learning': '薄弱',
    'good': '一般',
    'mastered': '掌握',
  }
  return map[level] || level
}

// 获取正确率等级标签类型
const getAccuracyLevelTagType = (level) => {
  const map = {
    'new': 'info',
    'weak': 'danger',
    'learning': 'warning',
    'good': '',
    'mastered': 'success',
  }
  return map[level] || 'info'
}

// 处理表格排序变化（使用后端排序）
const handleSortChange = ({ prop, order }) => {
  if (!prop) {
    // 取消排序
    filters.sort_by = null
    filters.sort_order = 'desc'
  } else if (prop === 'accuracy') {
    // 正确率排序需要后端处理
    filters.sort_by = 'accuracy'
    filters.sort_order = order === 'ascending' ? 'asc' : 'desc'
  } else {
    // 其他字段使用后端排序
    filters.sort_by = prop
    filters.sort_order = order === 'ascending' ? 'asc' : 'desc'
  }
  pagination.page = 1 // 重置到第一页
  fetchWords()
}

const fetchWords = async () => {
  try {
    const params = {
      skip: (pagination.page - 1) * pagination.limit,
      limit: pagination.limit,
    }
    if (filters.keyword) params.keyword = filters.keyword
    if (filters.grade) params.grade = filters.grade
    if (filters.semester) params.semester = filters.semester
    if (filters.tag_id) params.tag_ids = filters.tag_id
    if (filters.accuracy_level) params.accuracy_level = filters.accuracy_level
    if (filters.sort_by) {
      params.sort_by = filters.sort_by
      params.sort_order = filters.sort_order
    }
    // 复习情况/正确率按当前小孩隔离
    if (kidStore.activeKid?.id) params.user_id = kidStore.activeKid.id

    const { data } = await wordApi.list(params)
    words.value = data
    // 低年级辅助：开启拼音时批量补当前页中文拼音
    if (dimConfigForm.showPinyin && data.items && data.items.length) {
      fetchPinyin(data.items.map(w => w.chinese).filter(Boolean))
    }
  } catch (error) {
    ElMessage.error('获取单词列表失败')
  }
}

const fetchTags = async () => {
  try {
    const { data } = await questionApi.listTags()
    allTags.value = data
  } catch (error) {
    console.error('获取标签失败:', error)
  }
}

const showAddDialog = () => {
  dialogTitle.value = '新增单词'
  isEdit.value = false
  resetForm()
  dialogVisible.value = true
}

const editWord = (row) => {
  dialogTitle.value = '编辑单词'
  isEdit.value = true
  currentWordId.value = row.id
  form.english = row.english
  form.chinese = row.chinese
  form.phonetic = row.phonetic || ''
  form.grade = row.grade
  form.semester = row.semester
  form.tag_ids = row.tags ? row.tags.map(t => t.id) : []
  dialogVisible.value = true
}

const resetForm = () => {
  form.english = ''
  form.chinese = ''
  form.phonetic = ''
  form.grade = null
  form.semester = null
  form.tag_ids = []
}

const saveWord = async () => {
  if (!form.english || !form.chinese) {
    ElMessage.warning('请填写必填项')
    return
  }

  try {
    if (isEdit.value) {
      await wordApi.update(currentWordId.value, form)
      ElMessage.success('更新成功')
    } else {
      await wordApi.create(form)
      ElMessage.success('创建成功')
    }
    dialogVisible.value = false
    fetchWords()
  } catch (error) {
    ElMessage.error('保存失败')
  }
}

const deleteWord = async (row) => {
  try {
    await ElMessageBox.confirm('确定删除该单词吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    await wordApi.delete(row.id)
    ElMessage.success('删除成功')
    fetchWords()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

// 复习（铺平：听写=3 中-英=1 英-中=2，点击直达）
const startReview = (type) => {
  reviewConfig.type = type
  reviewStep.value = 'question'
  // 如果有选中单词，默认数量为选中数量
  if (selectedWords.value.length > 0) {
    reviewConfig.count = selectedWords.value.length
  }
  reviewVisible.value = true
  startReviewGame()
}

const handleSelectionChange = (selection) => {
  selectedWords.value = selection
}

const startReviewGame = async () => {
  if (reviewStarting.value) return
  reviewStarting.value = true
  try {
    const params = {
      count: reviewConfig.count,
    }
    if (reviewConfig.grade) params.grade = reviewConfig.grade
    // 如果有选中单词，传递单词ID列表
    if (selectedWords.value.length > 0) {
      params.word_ids = selectedWords.value.map(w => w.id).join(',')
    }
    // 复习进度按当前小孩
    if (kidStore.activeKid?.id) params.user_id = kidStore.activeKid.id

    const { data } = await wordApi.startReview(params)
    reviewQuestions.value = data.questions.map(q => ({
      ...q,
      correct: undefined,
    }))
    currentSessionId.value = data.session_id
    currentIndex.value = 0
    userAnswer.value = ''
    selectedOption.value = ''
    currentQuestion.value = reviewQuestions.value[0]
    if (dimConfigForm.showPinyin) {
      const q0 = currentQuestion.value
      fetchPinyin([...(q0.options || []), q0.chinese].filter(Boolean))
    }
    reviewStep.value = 'question'
    if (currentType.value === 1) {
      resetLetterInput()
      setTimeout(() => focusLetterInput(), 100)
    }

    // 默写/听力：自动播放（播完停3秒再播一次）
    if (currentType.value === 1 || currentType.value === 3) {
      setTimeout(() => autoPlayWithReplay(reviewQuestions.value[0].word_id), 400)
    }

    // 启动计时器 - 先清除可能存在的旧计时器
    if (reviewTimer.value) {
      clearInterval(reviewTimer.value)
    }
    reviewStartTime.value = Date.now()
    reviewElapsed.value = 0
    reviewTimer.value = setInterval(() => {
      reviewElapsed.value = Math.floor((Date.now() - reviewStartTime.value) / 1000)
    }, 1000)
  } catch (error) {
    ElMessage.error('获取复习内容失败')
  } finally {
    reviewStarting.value = false
  }
}

// 播放单词音频（Promise 在播放结束/失败时 resolve）
const playWordAudio = async (wordId) => {
  if (!wordId || audioLoadingMap[wordId]) return
  audioLoadingMap[wordId] = true

  try {
    const response = await fetch(`/api/words/${wordId}/audio`)
    if (!response.ok) {
      throw new Error(`HTTP ${response.status}`)
    }

    const blob = await response.blob()
    const audioUrl = URL.createObjectURL(blob)
    const audio = new Audio(audioUrl)

    await new Promise((resolve) => {
      audio.onended = () => {
        audioLoadingMap[wordId] = false
        URL.revokeObjectURL(audioUrl)
        resolve()
      }
      audio.onerror = () => {
        audioLoadingMap[wordId] = false
        URL.revokeObjectURL(audioUrl)
        resolve()
      }
      audio.play().catch(() => {
        audioLoadingMap[wordId] = false
        URL.revokeObjectURL(audioUrl)
        resolve()
      })
    })
  } catch (e) {
    console.error('音频播放失败:', e)
    ElMessage.warning('音频播放失败')
    audioLoadingMap[wordId] = false
  }
}

// 按英文播放（联想词标签用，直接走 TTS 接口）
const playAudioByEnglish = (en) => {
  if (!en) return
  const audio = new Audio('/api/words/audio?english=' + encodeURIComponent(en))
  audio.play().catch(() => {})
}

// 进入新题时：自动播放，暂停3秒后再播一次
const autoPlayWithReplay = async (wordId) => {
  if (!wordId) return
  const token = ++autoPlayToken.value
  await playWordAudio(wordId)
  if (autoPlayToken.value !== token) return
  await new Promise(r => setTimeout(r, 3000))
  if (autoPlayToken.value !== token) return
  await playWordAudio(wordId)
}

const submitAnswer = () => {
  const q = currentQuestion.value
  if (currentType.value === 1) {
    // 默写：从字母格拼答案
    userAnswer.value = fillBuiltAnswer()
    q.correct = userAnswer.value.toLowerCase() === q.english.toLowerCase()
    q.userAnswer = userAnswer.value
  } else if (currentType.value === 3) {
    // 听力：比较英文输入
    q.correct = userAnswer.value.toLowerCase().trim() === q.english.toLowerCase().trim()
    q.userAnswer = userAnswer.value
  } else {
    // 选择（英-中 / 听音选中文 / 新学词）
    q.correct = selectedOption.value === q.chinese
    q.userAnswer = selectedOption.value
  }
  // 显示toast提示
  if (q.correct) {
    ElMessage({ message: '✓ 正确', type: 'success', duration: 3000, showClose: false, customClass: 'toast-large' })
  } else {
    ElMessage({
      message: `✗ 错误 - 正确答案: ${q.english}`,
      type: 'error',
      duration: 3000,
      showClose: false,
      customClass: 'toast-large',
    })
  }
  // 显示答案后自动进入下一题
  if (currentIndex.value < reviewQuestions.value.length - 1) {
    setTimeout(() => {
      nextQuestion()
    }, 1500)
  }
}

const nextQuestion = () => {
  currentIndex.value++
  currentQuestion.value = reviewQuestions.value[currentIndex.value]
  if (dimConfigForm.showPinyin) {
    const qn = currentQuestion.value
    fetchPinyin([...(qn.options || []), qn.chinese].filter(Boolean))
  }
  userAnswer.value = ''
  selectedOption.value = ''
  if (currentType.value === 1) {
    resetLetterInput()
    setTimeout(() => focusLetterInput(), 100)
  }
  // 听音/听写/中英拼写自动播放
  if (currentType.value === 1 || currentType.value === 3 || currentType.value === 4) {
    setTimeout(() => autoPlayWithReplay(currentQuestion.value.word_id), 300)
  }
  setTimeout(() => {
    if (currentType.value === 1) {
      focusLetterInput()
      return
    }
    if (currentType.value === 2 || currentType.value === 4) return // 选择题无需焦点
    const input = answerInputRef.value?.$el?.querySelector('input')
    if (input) {
      input.focus()
    } else {
      answerInputRef.value?.focus()
    }
  }, 100)
}

// 终止答题，结算已答题目
const terminateReview = async () => {
  try {
    await ElMessageBox.confirm('确定要终止答题吗？已答题目将按实际结果结算。', '终止确认', {
      confirmButtonText: '确定终止',
      cancelButtonText: '继续答题',
      type: 'warning',
    })
    // 将未作答的题目标记为错误
    for (const q of reviewQuestions.value) {
      if (q.correct === undefined) {
        q.correct = false
      }
    }
    await finishReview()
  } catch (error) {
    // 用户取消，继续答题
  }
}

const finishReview = async () => {
  autoPlayToken.value++
  // 停止计时器
  if (reviewTimer.value) {
    clearInterval(reviewTimer.value)
    reviewTimer.value = null
  }
  const duration = reviewElapsed.value

  const results = reviewQuestions.value.map(q => ({
    word_id: q.word_id,
    is_correct: q.correct,
    user_answer: q.userAnswer || '',
    review_type: q.dimension ? (DIM_TYPE[q.dimension] || 2) : reviewConfig.type,
  }))

  try {
    const { data } = await wordApi.submitReview({
      session_id: currentSessionId.value,
      results,
      duration,
      user_id: kidStore.activeKid?.id,
    })
    reviewResult.total = data.total
    reviewResult.correct = data.correct
    reviewResult.error = data.error
    reviewResult.accuracy = data.accuracy
    reviewResult.duration = duration
    reviewStep.value = 'result'
    loadDailyTask() // 刷新今日任务（错词池变化）

    // 调用单词正确率成就检查
    try {
      await motivationApi.triggerWordAccuracy({
        total_count: data.total,
        correct_count: data.correct,
        reason: '单词复习'
      })
    } catch (error) {
      console.error('激励触发失败:', error)
    }
  } catch (error) {
    ElMessage.error('提交结果失败')
  }
}

// 打印
const showPrintDialog = () => {
  printDialogVisible.value = true
}

const generatePrintPdf = async () => {
  try {
    const params = { count: printForm.count }
    if (printForm.grade) params.grade = printForm.grade

    const { data } = await wordApi.printPdf(params)
    window.open(data.pdf_url, '_blank')
    printDialogVisible.value = false
    ElMessage.success('PDF已生成')
  } catch (error) {
    ElMessage.error('生成PDF失败')
  }
}

// 导入
const showImportDialog = () => {
  importForm.mode = 'text'
  importForm.text = ''
  importForm.file = null
  importForm.image = null
  importForm.ocrText = ''
  importForm.parsedWords = []
  importForm.grade = null
  importForm.semester = null
  importForm.tag_ids = []
  importDialogVisible.value = true
}

const handleFileChange = (file) => {
  onFileChange(file)
}

const handleImageChange = async (file) => {
  importForm.image = file.raw
  // 自动调用OCR识别
  await recognizeImage(file.raw)
}

const handleImageRemove = () => {
  importForm.image = null
  importForm.ocrText = ''
  importForm.parsedWords = []
}

// 文本模式变化时更新预览
const onTextChange = () => {
  if (importForm.mode === 'text' && importForm.text.trim()) {
    importForm.parsedWords = smartParseWords(importForm.text)
  }
}

// 文件模式变化时
const onFileChange = (file) => {
  importForm.file = file.raw
  if (file.raw) {
    const reader = new FileReader()
    reader.onload = e => {
      importForm.parsedWords = smartParseWords(e.target.result)
    }
    reader.readAsText(file.raw)
  }
}

const recognizeImage = async (file) => {
  try {
    const formData = new FormData()
    formData.append('file', file)

    const response = await fetch('/api/upload/image', {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      throw new Error('OCR识别失败')
    }

    const result = await response.json()
    if (result.ocr_result && result.ocr_result.full_text) {
      importForm.ocrText = result.ocr_result.full_text
      // 智能分隔单词并更新预览
      importForm.parsedWords = smartParseWords(result.ocr_result.full_text)
      ElMessage.success('图片识别成功，请检查识别结果')
    } else {
      ElMessage.warning('未识别到文字，请上传更清晰的图片')
    }
  } catch (error) {
    console.error('OCR error:', error)
    ElMessage.error('图片识别失败，请尝试其他方式导入')
  }
}

// 智能分隔单词 - 自动识别英文和中文
const smartParseWords = (text) => {
  // 清理OCR噪声字符（保留\n\r）
  const cleaned = text
    .replace(/[\u0001-\u0009\u000B\u000C\u000E-\u001F\u007F-\u009F]/g, '') // 移除控制字符（保留\n\r即10和13）
    .replace(/['']/g, "'")  // 规范化撇号
    .replace(/[""]/g, '"')
    .replace(/（/g, '(').replace(/）/g, ')')  // 规范化中文括号
    .replace(/[ \t]+/g, ' ')   // 规范化空格（保留换行）

  const words = []

  // 按行分割
  const lines = cleaned.split('\n')

  for (const line of lines) {
    const trimmed = line.trim()
    if (!trimmed) continue

    // 分割本行的各个单词（按制表符或连续空格分割）
    // 格式如: "1.mess 杂乱  2.whose 谁的" 或 "1.mess 杂乱\t2.whose 谁的"
    const entries = trimmed.split(/(?:\t|  +)(?=\d+\.)/)

    for (const entry of entries) {
      if (!entry.trim()) continue

      // 去掉序号前缀，如 "1.mess" 或 "1. mess"
      let content = entry.replace(/^\d+\.?\s*/, '').trim()
      if (!content) continue

      let phonetic = ''
      let english = ''
      let chinese = ''

      // 先提取音标 /eɪ/ 或 [音标] 格式（可能在末尾或中间）
      // 提取末尾的 /音标/ 格式
      const phoneticMatch = content.match(/\/([^\/]+)\/$/)
      if (phoneticMatch) {
        phonetic = phoneticMatch[1]
        content = content.replace(/\/[^\/]+\/$/, '').trim()
      }
      // 提取 [音标] 格式
      const bracketPhonetic = content.match(/\[([^\]]+)\]/)
      if (bracketPhonetic) {
        phonetic = bracketPhonetic[1]
        content = content.replace(/\[[^\]]+\]/, '').trim()
      }

      // 去掉末尾的括号注释如 (复数)
      content = content.replace(/\s*\([^)]*\)\s*$/, '').trim()

      // 分离英文和中文
      // 格式1: 英文 + 空格 + 中文（如 "mess 杂乱" 或 "school bag 书包"）
      // 格式2: 只有英文或只有中文
      // 格式3: 英文 + 空格 + 音标（如 "baby /eɪ/"）

      // 尝试按空格分割
      const parts = content.split(/\s+/)

      if (parts.length >= 2) {
        // 检查第一部分是否是纯英文
        const firstPart = parts[0]
        const isEnglish = /^[a-zA-Z][a-zA-Z'-]*$/.test(firstPart) ||
                          /^[a-zA-Z][a-zA-Z'-]*(?:\s+[a-zA-Z][a-zA-Z'-]*)+$/.test(firstPart)

        if (isEnglish) {
          english = firstPart
          // 剩余部分是中文或其他
          const rest = parts.slice(1).join(' ').trim()
          if (rest) {
            // 检查是否是音标格式
            if (rest.startsWith('/') && rest.endsWith('/')) {
              phonetic = rest.slice(1, -1)
            } else {
              chinese = rest
            }
          }
        } else {
          // 第一部分不是纯英文，可能是中文
          chinese = content
        }
      } else if (parts.length === 1) {
        // 只有一个部分
        const part = parts[0]
        if (/^[a-zA-Z][a-zA-Z'-]*$/.test(part) || /^[a-zA-Z][a-zA-Z'-]*(?:\s+[a-zA-Z][a-zA-Z'-]*)+$/.test(part)) {
          // 纯英文
          english = part
        } else {
          // 纯中文
          chinese = part
        }
      }

      if (english || chinese) {
        words.push({
          english: english || '',
          chinese: chinese || '',
          phonetic: phonetic || '',
          original: entry
        })
      }
    }
  }

  return words
}

const parseTextToWords = (text) => {
  const lines = text.trim().split('\n')
  const words = []
  for (const line of lines) {
    const trimmed = line.trim()
    if (!trimmed) continue
    // 智能分隔
    const parsed = smartParseWords(trimmed)
    if (parsed.length > 0) {
      words.push(parsed[0])
    }
  }
  return words
}

const importWords = async () => {
  let words = []

  // 优先使用预览表格中的数据（用户可能已编辑）
  if (importForm.parsedWords && importForm.parsedWords.length > 0) {
    words = importForm.parsedWords.filter(w => w.english && w.chinese)
  } else if (importForm.mode === 'text') {
    if (!importForm.text.trim()) {
      ElMessage.warning('请输入单词内容')
      return
    }
    words = smartParseWords(importForm.text)
  } else if (importForm.mode === 'file') {
    if (!importForm.file) {
      ElMessage.warning('请选择文件')
      return
    }
    // 读取文件内容
    try {
      const reader = new FileReader()
      const fileContent = await new Promise((resolve, reject) => {
        reader.onload = e => resolve(e.target.result)
        reader.onerror = reject
        reader.readAsText(importForm.file)
      })
      words = smartParseWords(fileContent)
    } catch (error) {
      ElMessage.error('读取文件失败')
      return
    }
  } else if (importForm.mode === 'image') {
    if (!importForm.ocrText.trim()) {
      ElMessage.warning('请先上传图片并等待识别完成')
      return
    }
    words = smartParseWords(importForm.ocrText)
  }

  if (words.length === 0) {
    ElMessage.warning('未解析到有效单词')
    return
  }

  importing.value = true
  let successCount = 0
  let failCount = 0

  for (const word of words) {
    try {
      await wordApi.create({
        english: word.english,
        chinese: word.chinese,
        phonetic: word.phonetic || undefined,
        grade: importForm.grade,
        semester: importForm.semester,
        tag_ids: importForm.tag_ids,
      })
      successCount++
    } catch (error) {
      failCount++
    }
  }

  importing.value = false
  importDialogVisible.value = false

  ElMessage.success(`导入完成：成功 ${successCount} 个，失败 ${failCount} 个`)
  fetchWords()
}

onMounted(async () => {
  // 首页年级维度跳转：/words?grade=6；学习空间指定年级优先
  const routeGrade = Number(route.query.grade)
  // 学习空间指定年级优先，其次路由参数；否则留空=全部（不再套用系统配置「默认年级」）
  if (subjectStore.activeGrade !== null) {
    filters.grade = subjectStore.activeGrade
  } else if (routeGrade) {
    filters.grade = routeGrade
  } else {
    filters.grade = null
  }
  // 表单默认年级只跟随当前学习空间
  if (reviewConfig.grade == null) reviewConfig.grade = subjectStore.activeGrade
  if (printForm.grade == null) printForm.grade = subjectStore.activeGrade
  if (importForm.grade == null) importForm.grade = subjectStore.activeGrade
  loadDimConfig()
  fetchWords()
  fetchTags()
  loadDailyTask()
})
</script>

<style scoped>
.words {
  max-width: 1400px;
  margin: 0 auto;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.filters {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

/* 今日任务大入口（三分类） */
.daily-task-card {
  padding: 16px 20px;
  margin-bottom: 14px;
  border-radius: 12px;
  background: linear-gradient(135deg, #f0f7ff 0%, #e8f1ff 100%);
  border: 1px solid #cfe3ff;
}
.dt-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.dt-title {
  font-size: 17px;
  font-weight: 700;
  color: #1f3d7a;
  display: flex;
  align-items: center;
  gap: 10px;
}
.dt-count {
  font-size: 14px;
  color: #3a7afe;
  background: #fff;
  border-radius: 20px;
  padding: 2px 12px;
  font-weight: 600;
}
.dt-config {
  margin-left: auto;
}
.dt-desc {
  margin-top: 4px;
  color: #5b6c8f;
  font-size: 12px;
}
.dt-dims {
  color: #3a7afe;
}
.dt-sections {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-top: 12px;
}
.dt-section {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px 14px;
  border-radius: 10px;
  cursor: pointer;
  background: #fff;
  border: 1px solid #e6eefb;
  transition: transform 0.15s, box-shadow 0.15s;
}
.dt-section:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 14px rgba(64, 128, 255, 0.16);
}
.ds-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}
.dt-section.wrong .ds-dot { background: #e64a4a; }
.dt-section.due .ds-dot { background: #e6a23c; }
.dt-section.new .ds-dot { background: #67c23a; }
.ds-name {
  font-size: 15px;
  font-weight: 600;
  color: #333;
}
.ds-num {
  font-size: 17px;
  color: #3a7afe;
  margin-left: auto;
}
.ds-tip {
  font-size: 11px;
  color: #9aa7bd;
  display: none;
}
.ds-go {
  font-size: 12px;
  color: #3a7afe;
  font-weight: 600;
  flex-shrink: 0;
}

/* 复习弹窗：维度标签 */
.dim-tag {
  font-size: 12px;
  padding: 2px 10px;
  border-radius: 20px;
  font-weight: 600;
}
.dim-tag.recognize { background: #ecf5ff; color: #3a7afe; }
.dim-tag.listen { background: #fdf6ec; color: #b88230; }
.dim-tag.speak { background: #f0f9eb; color: #529b2e; }
.dim-tag.write { background: #fef0f0; color: #d85c5c; }

/* 新学词学习卡 */
.new-word-learn {
  padding: 16px;
  border-radius: 12px;
  background: #f7faff;
  border: 1px dashed #cfe3ff;
}
.nw-english {
  font-size: 30px;
  font-weight: 700;
  color: #1f3d7a;
  display: flex;
  align-items: center;
  gap: 10px;
}
.nw-meta {
  margin: 8px 0;
  display: flex;
  gap: 12px;
  flex-wrap: wrap;
  align-items: center;
}
.nw-phonetic {
  color: #5b6c8f;
  font-size: 15px;
}
.nw-question {
  margin: 12px 0 8px;
  color: #5b6c8f;
  font-size: 14px;
}
.nw-root {
  margin: 6px 0;
  color: #5b6c8f;
  font-size: 13px;
  background: #fff;
  border: 1px solid #e6eefb;
  border-radius: 8px;
  padding: 6px 10px;
}
.nw-root-label {
  color: #3a7afe;
  font-weight: 600;
  margin-right: 4px;
}
.nw-example {
  margin: 6px 0;
}
.nw-ex-hint {
  color: #909399;
  font-size: 12px;
}
.nw-ex-item {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-top: 4px;
  padding: 4px 10px;
  background: #fff;
  border: 1px solid #e6eefb;
  border-radius: 8px;
}
.nw-ex-en {
  font-size: 15px;
  color: #2c3e50;
}

/* 听音选中文 */
.listening-choice {
  text-align: center;
  padding: 12px 0;
}
.lc-tip {
  color: #5b6c8f;
  font-size: 14px;
  margin: 10px 0;
}

/* 维度配置 */
.dim-config-tip {
  color: #5b6c8f;
  font-size: 13px;
  margin-bottom: 12px;
}
.dim-config-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}
.dim-config-item .el-checkbox {
  width: 100%;
  justify-content: center;
  padding: 10px 0;
}
.dim-config-row {
  border-top: 1px dashed #e6eefb;
  padding-top: 12px;
}
.dc-label {
  font-size: 14px;
  font-weight: 600;
  color: #333;
  display: block;
  margin-bottom: 8px;
}
.dc-hint {
  font-size: 12px;
  color: #9aa7bd;
  margin-top: 6px;
}
.dc-check-row {
  display: flex;
  flex-wrap: wrap;
  gap: 18px;
  align-items: center;
}
/* 低年级辅助：中文拼音小字 */
.cn-wrap {
  display: inline-flex;
  align-items: baseline;
  flex-wrap: wrap;
  gap: 2px 6px;
}
.cn-pinyin {
  font-size: 12px;
  color: #8a94a6;
  letter-spacing: 0.5px;
  font-weight: 400;
  display: block;
}
.zh-speak-btn {
  font-size: 14px;
  padding: 0 4px;
  margin-left: 2px;
}
.zh-speak-inline {
  font-size: 30px;
  margin-left: 8px;
  vertical-align: middle;
}
.opt-cn {
  margin-right: 6px;
}
.review-question .cn-pinyin {
  display: inline-block;
  margin-left: 6px;
  font-size: 13px;
}
.dictation .cn-pinyin {
  font-size: 22px;
  margin-top: 4px;
  color: #8a94a6;
}
.word-english {
  font-weight: bold;
  color: #409eff;
  font-size: 16px;
}

.word-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}

.word-cell .word-english {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.phonetic {
  color: #909399;
  font-family: monospace;
}

.review-info .correct {
  color: #67c23a;
  font-weight: bold;
}

.review-info .total {
  color: #909399;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

/* 复习弹窗样式 */
:deep(.review-dialog) {
  --review-scale: 1;
  transform: scale(var(--review-scale));
  transform-origin: center center;
}

:deep(.review-dialog .el-dialog__body) {
  padding: 0;
}

/* 复习弹窗背景虚化 */
:deep(.el-overlay-dialog) {
  backdrop-filter: blur(8px);
  background: rgba(0, 0, 0, 0.3) !important;
}

.review-config {
  padding: 40px;
  font-size: 20px;
}

.review-question {
  padding: 40px;
  display: flex;
  flex-direction: column;
  height: 70vh;
  max-height: 600px;
}

/* ===== 学习模式（先学后练） ===== */
.learn-flow {
  padding: 20px 30px 10px;
  display: flex;
  flex-direction: column;
  min-height: 60vh;
}
.learn-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}
.learn-title {
  font-size: 22px;
  font-weight: 700;
  color: #303133;
}
.learn-progress {
  font-size: 22px;
  font-weight: bold;
  color: #409eff;
}
.learn-tip {
  font-size: 13px;
  color: #909399;
  margin-bottom: 18px;
}
.learn-card {
  background: #f8fafd;
  border: 1px solid #e6eefb;
  border-radius: 16px;
  padding: 28px 34px;
  flex: 1;
}
.lc-english {
  font-size: 42px;
  font-weight: 800;
  color: #2b6cb0;
  display: flex;
  align-items: center;
  gap: 10px;
}
.lc-english .audio-btn {
  font-size: 24px;
  padding: 4px 10px;
}
.lc-phonetic {
  font-size: 18px;
  color: #5b6c8f;
  margin: 6px 0 14px;
}
.lc-chinese {
  font-size: 28px;
  color: #303133;
  margin-bottom: 18px;
  display: flex;
  align-items: baseline;
  flex-wrap: wrap;
  gap: 0 8px;
}
.lc-chinese .cn-pinyin {
  font-size: 16px;
  display: inline-block;
  margin-left: 4px;
}
.lc-section {
  margin-top: 12px;
  background: #fff;
  border: 1px solid #e6eefb;
  border-radius: 10px;
  padding: 12px 16px;
}
.lc-section-label {
  font-size: 13px;
  font-weight: 600;
  color: #2b6cb0;
  margin-bottom: 4px;
}
.lc-section-body {
  font-size: 15px;
  color: #4b5a74;
  line-height: 1.7;
  white-space: pre-line;
}
.lc-ex {
  margin-top: 6px;
}
.lc-ex:first-child {
  margin-top: 0;
}
.lc-ex-en {
  font-size: 16px;
  color: #2c3e50;
  display: flex;
  align-items: center;
  gap: 2px;
}
.lc-ex-zh {
  font-size: 13px;
  color: #909399;
  margin-top: 2px;
}
.learn-nav {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin: 18px 0 6px;
}
.learn-footer {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 18px;
  padding-top: 6px;
}
.learn-skip {
  font-size: 13px;
  color: #909399;
  cursor: pointer;
  text-decoration: underline;
}

.question-header {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 40px;
  margin-bottom: 30px;
  flex-shrink: 0;
  position: sticky;
  top: 0;
  background: #fff;
  z-index: 10;
  padding: 10px 0;
}

.progress {
  font-size: 36px;
  font-weight: bold;
  color: #409eff;
}

.timer {
  font-size: 32px;
  color: #909399;
  font-family: monospace;
  font-weight: 600;
}

.result-display {
  text-align: center;
  padding: 24px 48px;
  border-radius: 16px;
  margin-bottom: 30px;
}

.correct-display {
  background: linear-gradient(135deg, #67c23a 0%, #5daf34 100%);
  color: #fff;
}

.wrong-display {
  background: linear-gradient(135deg, #f56c6c 0%, #e64242 100%);
  color: #fff;
}

.result-status {
  font-size: 32px;
  font-weight: bold;
  margin-bottom: 8px;
}

.result-answer-large {
  font-size: 36px;
  font-weight: bold;
}

.your-answer {
  font-size: 24px;
  margin-top: 8px;
  opacity: 0.9;
}

.question-content {
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.dictation {
  text-align: center;
  padding: 20px;
}

.dictation .chinese {
  font-weight: bold;
  color: #303133;
  margin-bottom: 16px;
  letter-spacing: 4px;
  line-height: 1.45;
  word-break: break-word;
  overflow-wrap: anywhere;
  padding: 0 12px;
  max-width: 100%;
  box-sizing: border-box;
}

.dictation .audio-row {
  margin-bottom: 12px;
}

.dictation .hint-box {
  margin-bottom: 28px;
}

.dictation .hint {
  font-size: 24px;
  color: #606266;
  background: #f5f7fa;
  padding: 10px 28px;
  border-radius: 8px;
  display: inline-block;
  margin-bottom: 12px;
}

.letter-input {
  outline: none;
  cursor: text;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  position: relative;
  min-height: 80px;
  width: 100%;
}

.letter-cells {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 8px;
  max-width: 100%;
  padding: 8px 4px;
}

.letter-cell {
  width: 42px;
  height: 52px;
  border-bottom: 3px solid #c0c4cc;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 28px;
  font-weight: 600;
  color: #303133;
  text-transform: lowercase;
  box-sizing: border-box;
  background: #fafafa;
  border-radius: 6px 6px 0 0;
}

.letter-cell.fixed {
  border-bottom-color: transparent;
  background: transparent;
  color: #909399;
  font-size: 24px;
  min-width: 20px;
  width: auto;
  padding: 0 4px;
}

.letter-cell.active {
  border-bottom-color: #409eff;
  box-shadow: 0 2px 0 #409eff;
  background: #ecf5ff;
}

.letter-cell.filled {
  background: #fff;
}

.letter-cell.correct {
  border-bottom-color: #67c23a;
  color: #67c23a;
  background: #f0f9eb;
}

.letter-cell.wrong {
  border-bottom-color: #f56c6c;
  color: #f56c6c;
  background: #fef0f0;
}

.letter-hidden-input {
  position: absolute;
  opacity: 0;
  width: 1px;
  height: 1px;
  pointer-events: none;
}

.dictation .answer-input {
  max-width: 600px;
  margin: 0 auto;
}

.dictation .answer-input :deep(.el-input__wrapper) {
  padding: 20px 30px;
  border-radius: 12px;
  border: 3px solid #dcdfe6;
  box-shadow: none;
  transition: all 0.3s;
}

.dictation .answer-input :deep(.el-input__wrapper.is-focus) {
  border-color: #409eff;
  box-shadow: 0 0 0 4px rgba(64, 158, 255, 0.1);
}

.dictation .answer-input :deep(.el-input__inner) {
  font-size: 48px;
  text-align: center;
  letter-spacing: 5px;
  height: 80px;
  line-height: 80px;
}

.result {
  margin-top: 30px;
  padding: 16px 32px;
  border-radius: 12px;
  display: inline-block;
  font-size: 28px;
}

.result.correct-result {
  background: #f0f9eb;
  color: #67c23a;
  border: 2px solid #67c23a;
}

.result.wrong-result {
  background: #fef0f0;
  color: #f56c6c;
  border: 2px solid #f56c6c;
}

.correct-answer {
  font-size: 28px;
  font-weight: bold;
}

.wrong-result .correct-answer {
  color: #67c23a;
}

.correct-result .correct-answer {
  color: #909399;
}

/* 答题正确动画 */
@keyframes correctPulse {
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
}

@keyframes correctGlow {
  0% { box-shadow: 0 0 0 0 rgba(103, 194, 58, 0.4); }
  50% { box-shadow: 0 0 30px 10px rgba(103, 194, 58, 0.2); }
  100% { box-shadow: 0 0 0 0 rgba(103, 194, 58, 0); }
}

.result.correct-result {
  animation: correctPulse 0.5s ease-out, correctGlow 0.8s ease-out;
}

.result.correct-result .correct-answer {
  color: #67c23a;
}

/* 答题错误动画 */
@keyframes wrongShake {
  0%, 100% { transform: translateX(0); }
  20%, 60% { transform: translateX(-10px); }
  40%, 80% { transform: translateX(10px); }
}

.result.wrong-result {
  animation: wrongShake 0.5s ease-out;
}

.result.wrong-result .correct-answer {
  color: #f56c6c;
}

.choice {
  text-align: center;
}

.choice .english {
  font-size: 64px;
  font-weight: bold;
  color: #409eff;
  margin-bottom: 50px;
}

.choice .el-radio-group {
  display: flex;
  flex-direction: column;
  gap: 25px;
  align-items: center;
}

.choice .el-radio {
  font-size: 28px;
  padding: 20px 40px;
  min-width: 400px;
}

.choice .el-radio .el-radio__label {
  font-size: 28px;
}

/* 听力模式 */
.listening {
  text-align: center;
  padding: 20px;
}

.listening .audio-controls {
  margin-bottom: 40px;
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 16px;
}

.listening .audio-btn-large {
  font-size: 32px;
  padding: 30px 60px;
}

.listening .audio-btn-replay {
  font-size: 18px;
}

.listening .hint-box {
  margin-bottom: 40px;
}

.listening .hint {
  font-size: 28px;
  color: #606266;
  background: #f5f7fa;
  padding: 12px 32px;
  border-radius: 8px;
  display: inline-block;
  margin-bottom: 20px;
}

.listening .answer-input {
  max-width: 600px;
  margin: 0 auto;
}

.listening .answer-input :deep(.el-input__wrapper) {
  border-radius: 12px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.listening .answer-input :deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 2px 12px rgba(64, 158, 255, 0.3);
}

.listening .answer-input :deep(.el-input__inner) {
  font-size: 28px;
  text-align: center;
  letter-spacing: 8px;
  height: 60px;
}

/* 喇叭按钮通用样式 */
.audio-btn {
  font-size: 20px;
  padding: 8px 12px;
  border-radius: 50%;
  margin-left: 8px;
  vertical-align: middle;
}

.audio-btn-table {
  font-size: 13px;
  flex-shrink: 0;
  margin-left: 0;
}

.question-actions {
  margin-top: 40px;
  text-align: center;
  flex-shrink: 0;
}

.question-actions .el-button {
  font-size: 28px;
  padding: 25px 80px;
}

.review-result {
  padding: 24px;
  display: flex;
  flex-direction: column;
  height: 100%;
  max-height: 75vh;
  overflow: hidden;
}

.result-header {
  display: flex;
  gap: 20px;
  margin-bottom: 16px;
  flex-shrink: 0;
}

.accuracy-display {
  flex: 1;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 20px;
  padding: 32px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.accuracy-big {
  font-size: 80px;
  font-weight: bold;
  color: #fff;
  line-height: 1;
}

.accuracy-label {
  font-size: 20px;
  color: rgba(255,255,255,0.85);
  margin-top: 8px;
}

.stats-panel {
  flex: 1.1;
  background: linear-gradient(145deg, #f5f7fa 0%, #e8ecf1 100%);
  border-radius: 20px;
  padding: 20px 24px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  grid-template-rows: 1fr 1fr;
  gap: 14px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background: #fff;
  border-radius: 12px;
  padding: 12px;
}

.stat-item.correct .stat-value { color: #67c23a; }
.stat-item.error .stat-value { color: #f56c6c; }

.stat-value {
  font-size: 32px;
  font-weight: bold;
  color: #409eff;
  line-height: 1;
}

.stat-label {
  font-size: 13px;
  color: #909399;
  margin-top: 4px;
}

.error-word-list {
  flex: 1;
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.error-word-list .error-words-scroll {
  flex: 1;
  overflow-y: auto;
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(240px, 1fr));
  gap: 10px;
  padding: 4px;
}

.error-word-item {
  display: flex;
  background: #fff;
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 1px 4px rgba(0,0,0,0.08);
}

.correct-side {
  flex: 1;
  background: linear-gradient(135deg, #67c23a 0%, #5daf34 100%);
  padding: 12px;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.correct-en {
  font-size: 18px;
  font-weight: bold;
  color: #fff;
}

.correct-cn {
  font-size: 13px;
  color: rgba(255,255,255,0.9);
  margin-top: 2px;
}

.wrong-side {
  width: 100px;
  background: #fef0f0;
  padding: 12px 8px;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  border-left: 2px solid #f56c6c;
}

.wrong-tag {
  font-size: 10px;
  color: #f56c6c;
  font-weight: bold;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}

.wrong-answer {
  font-size: 14px;
  font-weight: bold;
  color: #f56c6c;
  text-align: center;
  word-break: break-all;
  margin-top: 4px;
}

.finish-btn {
  margin-top: 12px;
  flex-shrink: 0;
  height: 44px;
  font-size: 16px;
}

.ocr-preview {
  margin-top: 15px;
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.ocr-label {
  font-weight: bold;
  margin-bottom: 8px;
  color: #409eff;
}

.words-preview {
  margin-top: 10px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
  padding: 10px;
  background-color: #fafafa;
}

.preview-summary {
  margin-top: 10px;
  text-align: right;
  color: #909399;
  font-size: 14px;
}

/* 记忆曲线样式 */
.memory-curve {
  padding: 20px;
}
.phase-bar {
  margin-bottom: 20px;
}
.phase-track {
  position: relative;
  height: 40px;
  background: #f0f0f0;
  border-radius: 20px;
}
.phase-dot {
  position: absolute;
  top: 50%;
  transform: translate(-50%, -50%);
  padding: 4px 8px;
  background: #fff;
  border-radius: 4px;
  font-size: 12px;
  border: 2px solid #ddd;
}
.phase-dot.active {
  background: #409eff;
  color: #fff;
  border-color: #409eff;
}
.next-review {
  margin-bottom: 20px;
  font-size: 16px;
  color: #666;
}
.review-history {
  border-top: 1px solid #eee;
  padding-top: 15px;
}
.history-title {
  font-weight: bold;
  margin-bottom: 10px;
}
.history-item {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 6px 0;
  font-size: 14px;
}
.history-date {
  min-width: 100px;
}
.history-correct {
  color: #67c23a;
}
.history-wrong {
  color: #f56c6c;
}

/* 禁用卡片的hover效果 */
.words :deep(.el-card) {
  transition: none;
}
.words :deep(.el-card:hover) {
  transform: none;
  box-shadow: var(--shadow-sm) !important;
}
</style>

<style>
.toast-large.el-message {
  font-size: 24px !important;
  padding: 20px 30px !important;
  min-width: 300px !important;
}
.toast-large.el-message .el-message__content {
  font-size: 24px !important;
}
</style>
