<template>
  <div class="tbl-container">
    <!-- ============ 教材列表 ============ -->
    <div v-if="!currentBook">
      <div class="tbl-header">
        <h3>📚 教材知识库</h3>
        <span class="tbl-sub">已下载到本地的教材，可在线预览；已提取知识点的教材支持按单元 / 关键词定位</span>
      </div>
      <el-empty v-if="!libraryBooks.length && !loading" description="还没有教材，请到 家长中心 → 题库管理 → 按教材同步导入 下载教材" />
      <div v-loading="loading" class="tbl-grid">
        <el-card v-for="b in libraryBooks" :key="b.version + b.subject + b.grade + b.semester"
                 class="tbl-card" shadow="hover" @click="openBook(b)">
          <div class="tbl-card-title">{{ b.subject }} · {{ b.grade }}{{ b.semester }}</div>
          <div class="tbl-card-version">{{ b.version }}</div>
          <div class="tbl-card-meta">
            <el-tag size="small" :type="b.ocr ? 'success' : 'info'" effect="plain">
              {{ b.ocr ? '已提取知识点' : '仅预览' }}
            </el-tag>
            <span class="tbl-size">{{ (b.size / 1024 / 1024).toFixed(1) }}MB</span>
          </div>
          <div class="tbl-card-btn">
            <el-button size="small" type="primary" text>在线预览 →</el-button>
          </div>
        </el-card>
      </div>
    </div>

    <!-- ============ 预览器 ============ -->
    <div v-else class="tbl-viewer">
      <div class="tbl-toolbar">
        <el-button size="small" @click="backToList">← 返回</el-button>
        <span class="tbl-toolbar-title">{{ currentBook.subject }} · {{ currentBook.grade }}{{ currentBook.semester }}（{{ currentBook.version }}）</span>
        <el-button-group style="margin-left: auto">
          <el-button size="small" :disabled="page <= 1" @click="goto(page - 1)">上一页</el-button>
          <el-button size="small" :disabled="page >= totalPages" @click="goto(page + 1)">下一页</el-button>
        </el-button-group>
        <span class="tbl-page-input">
          <el-input-number v-model="pageInput" :min="1" :max="totalPages" size="small" controls-position="right"
                           style="width: 90px" @change="goto" />
          <span class="tbl-sub">/ {{ totalPages }} 页</span>
        </span>
        <el-button size="small" @click="goto(totalPages)" :disabled="page >= totalPages">末页</el-button>
      </div>

      <div class="tbl-body">
        <!-- 左侧：知识点导航 + 搜索 -->
        <div class="tbl-side">
          <div class="tbl-search">
            <el-input v-model="keyword" size="small" placeholder="搜索知识点 / 单元关键词"
                      clearable @keyup.enter="doLocate" @clear="clearLocate">
              <template #append>
                <el-button size="small" @click="doLocate">定位</el-button>
              </template>
            </el-input>
            <div v-if="locateResult.length" class="tbl-locate-hint">
              命中 {{ locateResult.length }} 页：
              <el-tag v-for="p in locateResult" :key="p" size="small" class="tbl-page-tag"
                      :type="p === page ? 'primary' : 'info'" effect="plain" @click="goto(p)">
                第 {{ p }} 页
              </el-tag>
            </div>
            <div v-else-if="keyword && searched" class="tbl-locate-hint tbl-miss">未找到，试试短关键词（如“时分秒”）</div>
          </div>

          <!-- 已导入知识点：章节树导航 -->
          <template v-if="kpChapters.length">
            <div class="tbl-units">
              <div class="tbl-units-title">📖 按知识点导航（{{ kpTotal }} 个）</div>
              <div v-for="c in kpChapters" :key="c.chapter" class="tbl-kp-chapter">
                <div class="tbl-kp-chapter-head" @click="goto(c.page)">
                  <span class="tbl-unit-page">P{{ c.page }}</span>
                  <span class="tbl-kp-chapter-title">{{ c.chapter }}</span>
                </div>
                <div class="tbl-kp-list">
                  <div v-for="p in c.points" :key="p.name" class="tbl-kp-item" @click="goto(c.page)">
                    <span class="tbl-kp-dot">•</span>
                    <span class="tbl-kp-name">{{ p.name }}</span>
                  </div>
                </div>
              </div>
            </div>
          </template>

          <!-- 无知识点但有 OCR 文本：单元目录 -->
          <template v-else-if="ocrUnits.length">
            <div class="tbl-units">
              <div class="tbl-units-title">📖 单元目录</div>
              <div v-for="u in ocrUnits" :key="u.page + u.title"
                   class="tbl-unit-item" :class="{ active: page >= u.page && page < nextUnitPage(u.page) }"
                   @click="goto(u.page)">
                <span class="tbl-unit-page">P{{ u.page }}</span>
                <span class="tbl-unit-title">{{ u.title }}</span>
              </div>
            </div>
          </template>

          <!-- 都没有 -->
          <div v-else class="tbl-side-tip">
            本教材还没有关联的知识点。<br>
            <span class="tbl-sub">到 家长中心 → 题库管理 → 按教材同步导入 提取知识点后，即可按章节导航到对应页。</span>
          </div>
        </div>

        <!-- 主体：页面图片 -->
        <div class="tbl-main">
          <div v-loading="loadingPage" class="tbl-page-wrap">
            <img v-if="pageImage" :src="'data:image/png;base64,' + pageImage" class="tbl-page-img" alt="教材页面" />
            <div v-else class="tbl-sub">加载中…</div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { textbookApi } from '@/api/textbook'

const route = useRoute()
const router = useRouter()

const loading = ref(false)
const libraryBooks = ref([])
const currentBook = ref(null)   // 当前预览的教材
const page = ref(1)
const pageInput = ref(1)
const totalPages = ref(0)
const pageImage = ref('')
const loadingPage = ref(false)
const ocrUnits = ref([])
const kpChapters = ref([])
const kpTotal = ref(0)
const keyword = ref('')
const locateResult = ref([])
const searched = ref(false)

const nextUnitPage = (p) => {
  const pages = ocrUnits.value.map(u => u.page)
  for (const q of pages) {
    if (q > p) return q
  }
  return totalPages.value + 1
}

const loadLibrary = async () => {
  loading.value = true
  try {
    const { data } = await textbookApi.library()
    libraryBooks.value = data.books || []
  } catch (e) {
    ElMessage.error('获取教材知识库失败')
  } finally {
    loading.value = false
  }
}

const openBook = async (b) => {
  currentBook.value = { ...b }
  page.value = 1
  pageInput.value = 1
  locateResult.value = []
  keyword.value = ''
  searched.value = false
  loadUnits()
  loadKnowledgePoints()
  await loadPage(1)
}

const loadUnits = async () => {
  ocrUnits.value = []
  try {
    const { data } = await textbookApi.units({
      version: currentBook.value.version, subject: currentBook.value.subject,
      grade: currentBook.value.grade, semester: currentBook.value.semester,
    })
    ocrUnits.value = data.units || []
  } catch {
    ocrUnits.value = []
  }
}

const loadKnowledgePoints = async () => {
  kpChapters.value = []
  kpTotal.value = 0
  try {
    const { data } = await textbookApi.knowledgePoints({
      version: currentBook.value.version, subject: currentBook.value.subject,
      grade: currentBook.value.grade, semester: currentBook.value.semester,
    })
    kpChapters.value = data.chapters || []
    kpTotal.value = data.total || 0
  } catch {
    kpChapters.value = []
  }
}

const loadPage = async (p) => {
  if (!currentBook.value) return
  loadingPage.value = true
  try {
    const { data } = await textbookApi.preview({
      version: currentBook.value.version, subject: currentBook.value.subject,
      grade: currentBook.value.grade, semester: currentBook.value.semester, page: p,
    })
    page.value = data.page
    pageInput.value = data.page
    totalPages.value = data.total_pages
    pageImage.value = data.image
  } catch (e) {
    ElMessage.error(e.detail || e.message || '预览失败')
  } finally {
    loadingPage.value = false
  }
}

const goto = (p) => {
  if (!p || p < 1) p = 1
  if (p > totalPages) p = totalPages
  if (p !== page.value) loadPage(p)
  else pageInput.value = p
}

const doLocate = async () => {
  const kw = keyword.value.trim()
  if (!kw) return
  searched.value = true
  try {
    const { data } = await textbookApi.locate({
      version: currentBook.value.version, subject: currentBook.value.subject,
      grade: currentBook.value.grade, semester: currentBook.value.semester, keyword: kw,
    })
    locateResult.value = data.pages || []
    if (locateResult.value.length) goto(locateResult.value[0])
  } catch {
    locateResult.value = []
  }
}

const clearLocate = () => {
  locateResult.value = []
  searched.value = false
}

const backToList = () => {
  currentBook.value = null
  pageImage.value = ''
}

// 从知识点管理跳转：query 携带 subject/grade/semester/version/kw
const autoOpenFromQuery = async () => {
  const q = route.query
  if (!q.subject && !q.version) return
  if (!libraryBooks.value.length) await loadLibrary()
  const baseMatch = (b) =>
    b.subject === (q.subject || '') && b.grade === (q.grade || '') && b.semester === (q.semester || '')
  // 优先精确版本匹配，其次降级到学科+年级+册次（旧数据版本名可能未规范化）
  let match = null
  if (q.version) {
    match = libraryBooks.value.find(b => baseMatch(b) && b.version === q.version)
  }
  if (!match) {
    match = libraryBooks.value.find(baseMatch)
  }
  if (match) {
    await openBook(match)
    if (q.kw) {
      keyword.value = q.kw
      await doLocate()
    }
  } else if (q.subject) {
    ElMessage.info('本地暂无匹配教材，请先在家长中心下载对应教材')
  }
}

onMounted(async () => {
  await loadLibrary()
  await autoOpenFromQuery()
})

watch(() => route.query, () => autoOpenFromQuery())
</script>

<style scoped>
.tbl-container { padding: 6px 4px; }
.tbl-header { display: flex; align-items: baseline; gap: 12px; margin-bottom: 14px; }
.tbl-header h3 { margin: 0; font-size: 18px; }
.tbl-sub { font-size: 12px; color: #909399; }
.tbl-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(230px, 1fr)); gap: 14px; min-height: 200px; }
.tbl-card { cursor: pointer; }
.tbl-card-title { font-size: 15px; font-weight: 600; }
.tbl-card-version { font-size: 12px; color: #606266; margin: 6px 0; }
.tbl-card-meta { display: flex; align-items: center; justify-content: space-between; }
.tbl-size { font-size: 12px; color: #909399; }
.tbl-card-btn { margin-top: 8px; text-align: right; }
.tbl-viewer { display: flex; flex-direction: column; gap: 10px; }
.tbl-toolbar { display: flex; align-items: center; gap: 10px; flex-wrap: wrap; }
.tbl-toolbar-title { font-weight: 600; font-size: 14px; }
.tbl-page-input { display: inline-flex; align-items: center; gap: 6px; }
.tbl-body { display: flex; gap: 14px; align-items: flex-start; }
.tbl-side { width: 230px; flex-shrink: 0; }
.tbl-search { margin-bottom: 10px; }
.tbl-locate-hint { margin-top: 6px; font-size: 12px; color: #606266; line-height: 2; }
.tbl-locate-hint .el-tag { cursor: pointer; margin-right: 4px; }
.tbl-miss { color: #f56c6c; }
.tbl-side-tip { font-size: 12px; color: #909399; background: #f4f4f5; border-radius: 6px; padding: 10px; line-height: 1.8; }
.tbl-units-title { font-size: 13px; font-weight: 600; margin-bottom: 8px; color: #303133; }
.tbl-unit-item { display: flex; gap: 8px; padding: 6px 8px; border-radius: 6px; cursor: pointer; font-size: 13px; align-items: baseline; }
.tbl-unit-item:hover { background: #f0f2f5; }
.tbl-unit-item.active { background: #ecf5ff; color: #409eff; }
.tbl-unit-page { flex-shrink: 0; color: #909399; font-size: 12px; }
.tbl-kp-chapter { margin-bottom: 8px; }
.tbl-kp-chapter-head { display: flex; gap: 8px; padding: 6px 8px; border-radius: 6px; cursor: pointer; font-size: 13px; font-weight: 600; align-items: baseline; }
.tbl-kp-chapter-head:hover { background: #f0f2f5; }
.tbl-kp-chapter-title { color: #303133; }
.tbl-kp-list { padding-left: 26px; }
.tbl-kp-item { display: flex; gap: 6px; padding: 3px 6px; border-radius: 5px; cursor: pointer; font-size: 12px; color: #606266; align-items: baseline; }
.tbl-kp-item:hover { background: #ecf5ff; color: #409eff; }
.tbl-kp-dot { color: #c0c4cc; flex-shrink: 0; }
.tbl-kp-name { line-height: 1.5; }
.tbl-main { flex: 1; min-width: 0; }
.tbl-page-wrap { display: flex; justify-content: center; min-height: 400px; }
.tbl-page-img { max-width: 100%; box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15); border-radius: 4px; }
</style>
