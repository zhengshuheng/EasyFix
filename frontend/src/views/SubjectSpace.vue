<template>
  <div class="subject-space">
    <div class="space-head">
      <h2 class="space-title">{{ subjectName }} 学习空间</h2>
      <span class="space-sub">{{ subjectStore.isAllGrade ? '全部年级' : subjectStore.activeGradeName }}</span>
    </div>
    <el-tabs v-model="activeTab" class="space-tabs" type="border-card">
      <el-tab-pane label="错题" name="questions" lazy>
        <QuestionsView />
      </el-tab-pane>
      <el-tab-pane label="练习" name="practice" lazy>
        <PracticeSetsView />
      </el-tab-pane>
      <template v-if="isEnglish">
        <el-tab-pane label="单词" name="words" lazy>
          <WordsView />
        </el-tab-pane>
        <el-tab-pane label="阅读" name="reading" lazy>
          <ReadingView />
        </el-tab-pane>
        <el-tab-pane label="学习报告" name="reports" lazy>
          <LearningReportsView />
        </el-tab-pane>
      </template>
    </el-tabs>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useSubjectStore } from '@/stores/subject'
import QuestionsView from './Questions.vue'
import PracticeSetsView from './PracticeSets.vue'
import WordsView from './Words.vue'
import ReadingView from './Reading.vue'
import LearningReportsView from './LearningReports.vue'

const route = useRoute()
const subjectStore = useSubjectStore()

const subjectId = computed(() => Number(route.params.id))
const subject = computed(() => subjectStore.subjects.find((s) => s.id === subjectId.value))
const subjectName = computed(() => subject.value?.name || '学科')
const isEnglish = computed(() => subject.value?.name === '英语')

const activeTab = ref('questions')

// 学科变化时：同步空间学科并回到第一个 tab
watch(
  subjectId,
  () => {
    activeTab.value = 'questions'
    if (subjectId.value) subjectStore.select(subjectId.value)
  },
  { immediate: true }
)
</script>

<style scoped>
.subject-space {
  padding: 12px 4px;
}
.space-head {
  display: flex;
  align-items: baseline;
  gap: 10px;
  margin-bottom: 12px;
}
.space-title {
  margin: 0;
  font-size: 18px;
  color: #303133;
}
.space-sub {
  font-size: 13px;
  color: #909399;
}
.space-tabs :deep(.el-tabs__content) {
  padding: 12px 8px 4px;
}
</style>
