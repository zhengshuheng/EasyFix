<template>
  <div class="grammar-manager">
    <!-- 顶部操作条 -->
    <div class="action-bar">
      <el-select v-model="categoryFilter" placeholder="全部板块" clearable style="width: 180px" @change="fetchLessons">
        <el-option v-for="c in categories" :key="c.category" :label="c.category" :value="c.category" />
      </el-select>
      <el-select v-model="gradeFilter" placeholder="全部年级" clearable style="width: 120px" @change="fetchLessons">
        <el-option v-for="g in 12" :key="g" :label="g + '年级'" :value="g" />
      </el-select>
      <el-button type="primary" plain :loading="syncing" @click="syncTutorials">🔄 同步官方教程</el-button>
    </div>

    <div class="manager-tip">
      语法教程由运营中心统一维护（全部语法点带讲解 / 例句 / 易错点 / 口诀，语法点固化、全空间一致），本页只读。
      若某语法点显示「教程内容暂缺」，点「同步官方教程」从运营中心拉取最新内容即可。
    </div>

    <!-- 表格 -->
    <el-table :data="lessons" v-loading="loading" size="default" border stripe>
      <el-table-column prop="id" label="ID" width="60" />
      <el-table-column prop="category" label="板块" width="130" />
      <el-table-column prop="title" label="语法点" min-width="220" />
      <el-table-column label="年级" width="80">
        <template #default="{ row }">{{ row.grade ? row.grade + '年级' : '通用' }}</template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { ElMessage } from 'element-plus'
import { grammarApi } from '@/api/grammar'

const categories = ref([])
const lessons = ref([])
const loading = ref(false)
const syncing = ref(false)
const categoryFilter = ref(null)
const gradeFilter = ref(null)

async function syncTutorials() {
  syncing.value = true
  try {
    const { data } = await grammarApi.syncTutorials()
    ElMessage.success(`同步完成：新增 ${data.created || 0} 个、更新 ${data.updated || 0} 个语法点教程`)
    await fetchLessons()
  } catch (e) {
    ElMessage.error('同步失败：' + (e.response?.data?.detail || e.message))
  } finally {
    syncing.value = false
  }
}

async function fetchCategories() {
  try {
    const { data } = await grammarApi.categories()
    categories.value = data || []
  } catch (e) {
    ElMessage.error('加载板块失败：' + (e.response?.data?.detail || e.message))
  }
}

async function fetchLessons() {
  loading.value = true
  try {
    const params = {}
    if (categoryFilter.value) params.category = categoryFilter.value
    if (gradeFilter.value) params.grade = gradeFilter.value
    const { data } = await grammarApi.lessons(params)
    lessons.value = data || []
  } catch (e) {
    ElMessage.error('加载语法点失败：' + (e.response?.data?.detail || e.message))
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  fetchCategories()
  fetchLessons()
})
</script>

<style scoped>
.action-bar {
  display: flex;
  gap: 10px;
  align-items: center;
  margin-bottom: 12px;
  flex-wrap: wrap;
}
.manager-tip {
  background: #f0f9ff;
  border-left: 3px solid #409eff;
  padding: 8px 12px;
  font-size: 12px;
  color: #1d4e7a;
  border-radius: 4px;
  margin-bottom: 12px;
  line-height: 1.7;
}
</style>
