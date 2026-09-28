<template>
  <div class="onboarding">
    <div class="ob-card">
      <div class="ob-head">
        <h1>🚀 初始化你的学习空间</h1>
        <p>按顺序完成四步，孩子马上就能开始学习（每步都可跳过，之后在家长中心补做）</p>
      </div>

      <!-- ============ 快速体验：跳过初始化，直接用空间里的孩子进入学习 ============ -->
      <div class="ob-quick">
        <div class="ob-quick-text">
          <b>⚡ 快速体验</b>
          <span>不想配置？直接用空间里的体验小朋友立即开始学习，配置可随时在家长中心补做。</span>
        </div>
        <el-button type="success" size="large" :loading="quickLoading" @click="quickEnter">
          跳过初始化，直接进入学习 →
        </el-button>
      </div>

      <el-steps :active="step" finish-status="success" align-center class="ob-steps">
        <el-step title="添加小孩" />
        <el-step title="添加家长" />
        <el-step title="科目知识点" />
        <el-step title="英语单词" />
      </el-steps>

      <!-- ============ 第 1 步：选小孩数量 + 批量添加 ============ -->
      <div v-show="step === 0" class="ob-body">
        <h2>👦 第 1 步：添加小孩</h2>
        <p class="ob-sub">家里有几个孩子需要学习？按数量一次性添加（最多 {{ kidMax }} 个，之后也能在家长中心加）。</p>
        <div class="ob-counts" v-if="kidMax >= 1">
          <button v-for="n in kidMaxNums" :key="n" type="button"
                  :class="['ob-count', { on: kidCount === n }]" @click="kidCount = n">
            <b>{{ n }}</b><span>{{ n === 1 ? '个孩子' : '个孩子' }}</span>
          </button>
        </div>
        <el-alert v-else type="warning" :closable="false" show-icon
                  title="小孩名额已满（最多 5 个），可在家长中心删除后继续添加" />
        <div class="ob-actions" v-if="kidMax < 1">
          <el-button type="primary" @click="step = 1">已有小孩，跳过此步 →</el-button>
        </div>
        <el-form label-width="90px" class="ob-form" @submit.prevent>
          <el-form-item v-for="k in kidForms" :key="k.i" :label="`孩子${k.i}`" required>
            <div class="ob-kid-row">
              <el-input v-model="k.display_name" placeholder="怎么称呼孩子？" maxlength="20" style="width: 170px" />
              <el-date-picker v-model="k.enrollment_date" type="date" value-format="YYYY-MM-DD"
                              placeholder="小学入学日期" style="width: 200px" />
            </div>
            <div class="ob-tip" v-if="k.enrollment_date">
              入学 {{ k.enrollment_date }} → 当前 <b>{{ gradeLabel(k.enrollment_date) }}</b>
            </div>
          </el-form-item>
        </el-form>
        <div class="ob-actions">
          <el-button type="primary" :loading="kidSaving" :disabled="!canSaveKids" @click="saveKids">
            批量保存（{{ kidCount }} 个）并下一步
          </el-button>
        </div>
      </div>

      <!-- ============ 第 2 步：添加家长 ============ -->
      <div v-show="step === 1" class="ob-body">
        <h2>👩 第 2 步：添加家长（辅账号）</h2>
        <p class="ob-sub">你的官网账号已是主账号；可再添加一位家长（如爸爸/妈妈），ta 用这套用户名密码也能登录空间。</p>
        <el-form label-width="90px" class="ob-form" @submit.prevent>
          <el-form-item label="用户名" required>
            <el-input v-model="parentForm.username" placeholder="登录用户名（字母开头，4~20位）" maxlength="20" />
          </el-form-item>
          <el-form-item label="显示名">
            <el-input v-model="parentForm.display_name" placeholder="可选，默认同用户名" maxlength="20" />
          </el-form-item>
          <el-form-item label="密码" required>
            <el-input v-model="parentForm.password" type="password" placeholder="至少 4 位" show-password />
          </el-form-item>
        </el-form>
        <div class="ob-actions">
          <el-button @click="step = 0">上一步</el-button>
          <el-button plain @click="skipTo(2)">跳过（之后可加）</el-button>
          <el-button type="primary" :loading="parentSaving" :disabled="!canSaveParent" @click="saveParent">
            保存并下一步
          </el-button>
        </div>
      </div>

      <!-- ============ 第 3 步：科目知识点（数学/英语 一键同步全年级） ============ -->
      <div v-show="step === 2" class="ob-body">
        <h2>📚 第 3 步：科目知识点</h2>
        <p class="ob-sub">选择孩子学习的科目与教材版本，一键导入 1~6 年级全部知识点（内置知识库，秒级完成）。语文已内置，后续版本开放。</p>
        <el-form label-width="90px" class="ob-form" @submit.prevent>
          <el-form-item label="科目">
            <div class="ob-subjects">
              <button v-for="s in kpSubjects" :key="s" type="button"
                      :class="['ob-subject', { on: kpForm.subject === s }]" @click="onKpSubject(s)">
                {{ s }}
              </button>
            </div>
          </el-form-item>
          <el-form-item label="教材版本" required>
            <el-select v-model="kpForm.version" style="width: 280px" placeholder="选择版本">
              <el-option v-for="v in kpVersions" :key="v" :label="v" :value="v" />
            </el-select>
          </el-form-item>
          <el-form-item v-if="kpBusy" label="进度">
            <div class="ob-progress">
              <el-progress :percentage="kpProgress" style="width: 260px" />
              <div class="ob-tip">{{ kpMsg }}</div>
            </div>
          </el-form-item>
          <el-form-item v-else-if="kpDone" label="结果">
            <el-tag type="success" size="large" style="font-size: 14px">✅ {{ kpMsg }}</el-tag>
          </el-form-item>
        </el-form>
        <div class="ob-actions">
          <el-button @click="step = 1">上一步</el-button>
          <el-button plain @click="skipTo(3)">跳过（之后可同步）</el-button>
          <el-button v-if="kpDone" type="success" @click="step = 3">下一步 →</el-button>
          <el-button v-else type="primary" :loading="kpBusy" :disabled="!canImportKp" @click="importKp">
            ⚡ 一键导入（1~6 年级全部）
          </el-button>
        </div>
      </div>

      <!-- ============ 第 4 步：英语单词 一键同步 1-6 年级 ============ -->
      <div v-show="step === 3" class="ob-body">
        <h2>🔤 第 4 步：英语单词</h2>
        <p class="ob-sub">选择孩子英语教材版本，一键同步 1~6 年级全部单元单词（内置教材词汇表，秒级完成）。</p>
        <el-form label-width="90px" class="ob-form" @submit.prevent>
          <el-form-item label="教材版本" required>
            <el-select v-model="wordForm.version" style="width: 280px" placeholder="选择版本">
              <el-option v-for="v in wordVersions" :key="v" :label="v" :value="v" />
            </el-select>
          </el-form-item>
          <el-form-item v-if="wordBusy" label="进度">
            <div class="ob-progress">
              <el-progress :percentage="wordProgress" style="width: 260px" />
              <div class="ob-tip">{{ wordMsg }}</div>
            </div>
          </el-form-item>
          <el-form-item v-else-if="wordDone" label="结果">
            <el-tag type="success" size="large" style="font-size: 14px">✅ {{ wordMsg }}</el-tag>
          </el-form-item>
        </el-form>
        <div class="ob-actions">
          <el-button @click="step = 2">上一步</el-button>
          <el-button plain @click="finish()">跳过（之后可同步）</el-button>
          <el-button v-if="wordDone" type="success" @click="finish">✅ 完成引导，进入空间</el-button>
          <el-button v-else type="primary" :loading="wordBusy" :disabled="!canImportWord" @click="importWords">
            ⚡ 一键同步（1~6 年级全部）
          </el-button>
        </div>
      </div>

      <!-- ============ 完成 ============ -->
      <div v-if="step === 4" class="ob-body ob-done">
        <h2>🎉 初始化完成！</h2>
        <p class="ob-sub">空间已准备好，去选择孩子开始学习吧。</p>
        <div class="ob-actions">
          <el-button type="primary" size="large" @click="finish">进入学习空间</el-button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed, watch, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { usersApi } from '@/api/users'
import { syncApi } from '@/api/sync'
import { useKidStore } from '@/stores/kid'
import { useSubjectStore } from '@/stores/subject'

const router = useRouter()
const kidStore = useKidStore()
const subjectStore = useSubjectStore()
const step = ref(0)

const gradeOptions = [
  { label: '一年级', value: 1 },
  { label: '二年级', value: 2 },
  { label: '三年级', value: 3 },
  { label: '四年级', value: 4 },
  { label: '五年级', value: 5 },
  { label: '六年级', value: 6 },
]

const gradeLabel = (enr) => {
  if (!enr) return ''
  const today = new Date()
  const curYear = today.getMonth() >= 8 ? today.getFullYear() : today.getFullYear() - 1
  const enrDate = new Date(enr)
  const g = Math.min(6, Math.max(1, curYear - enrDate.getFullYear() + 1))
  return gradeOptions.find(o => o.value === g)?.label || ''
}

// ---------------- 第 1 步：数量 + 批量小孩 ----------------
const kidCount = ref(1)
const kidForms = ref([])
const kidSaving = ref(false)
const kidMax = ref(3) // 动态上限：5 - 现有小孩数（模板自带演示小孩占位）
const kidMaxNums = computed(() =>
  kidMax.value >= 1 ? Array.from({ length: kidMax.value }, (_, i) => i + 1) : [])

async function loadExistingKids() {
  try {
    const { data } = await usersApi.list()
    const kids = (data.users || []).filter(u => u.role === 'child')
    kidMax.value = Math.max(0, 5 - kids.length)
    if (kidCount.value > kidMax.value) kidCount.value = Math.max(1, kidMax.value)
    if (kidForms.value.length !== kidCount.value) {
      const list = []
      for (let i = 1; i <= kidCount.value; i++) {
        list.push({ i, display_name: '', enrollment_date: null })
      }
      kidForms.value = list
    }
  } catch {
    kidMax.value = 3
  }
}

watch(kidCount, (n) => {
  const list = []
  for (let i = 1; i <= n; i++) {
    list.push(kidForms.value[i - 1] || { i, display_name: '', enrollment_date: null })
  }
  kidForms.value = list
})
kidForms.value = [{ i: 1, display_name: '', enrollment_date: null }]

const canSaveKids = computed(() =>
  kidForms.value.every(k => k.display_name.trim() && k.enrollment_date))

async function saveKids() {
  if (!canSaveKids.value || kidSaving.value) return
  kidSaving.value = true
  let ok = 0
  for (const k of kidForms.value) {
    try {
      await usersApi.create({
        username: `kid_${Date.now()}_${ok}`,
        role: 'child',
        display_name: k.display_name.trim(),
        enrollment_date: k.enrollment_date,
      })
      ok++
    } catch (e) {
      ElMessage.error(`孩子${k.i}添加失败：${e.response?.data?.detail || '创建失败'}`)
    }
  }
  kidSaving.value = false
  if (ok > 0) {
    ElMessage.success(`已添加 ${ok} 个孩子`)
    step.value = 1
  }
}

// ---------------- 第 2 步：家长 ----------------
const parentForm = reactive({ username: '', display_name: '', password: '' })
const parentSaving = ref(false)
const canSaveParent = computed(() => {
  const u = parentForm.username.trim()
  return /^[A-Za-z][A-Za-z0-9_]{3,19}$/.test(u) && parentForm.password.length >= 4
})

async function saveParent() {
  parentSaving.value = true
  try {
    await usersApi.create({
      username: parentForm.username.trim(),
      role: 'admin',
      display_name: parentForm.display_name.trim() || undefined,
      password: parentForm.password,
    })
    ElMessage.success('家长添加成功')
    step.value = 2
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '创建失败')
  } finally {
    parentSaving.value = false
  }
}

// ---------------- 第 3 步：科目知识点一键同步 ----------------
const kpSubjects = ['数学', '英语']
const kpForm = reactive({ subject: '数学', version: '' })
const kpVersions = ref([])
const kpBusy = ref(false)
const kpDone = ref(false)
const kpProgress = ref(0)
const kpMsg = ref('')
const canImportKp = computed(() => !!kpForm.subject && !!kpForm.version)

async function loadOpsCatalog() {
  try {
    const { data } = await syncApi.status()
    const subjects = data.catalog?.subjects || {}
    const versions = Object.keys(subjects[kpForm.subject] || {})
    kpVersions.value = versions
    if (versions.length && !versions.includes(kpForm.version)) {
      kpForm.version = versions[0]
    }
    return data
  } catch (e) {
    kpVersions.value = []
    return null
  }
}

const onKpSubject = async (s) => {
  kpForm.subject = s
  kpForm.version = ''
  kpDone.value = false
  await loadOpsCatalog()
}

async function importKp() {
  if (!canImportKp.value || kpBusy.value || kpDone.value) return
  kpBusy.value = true
  kpProgress.value = 20
  kpMsg.value = '正在同步…'
  try {
    const { data } = await syncApi.syncKp({ subject: kpForm.subject, version: kpForm.version })
    kpProgress.value = 100
    kpDone.value = true
    kpMsg.value = `已同步 ${data.added} 条知识点（${kpForm.subject}《${kpForm.version}》1~6 年级）`
    ElMessage.success(kpMsg.value)
  } catch (e) {
    kpMsg.value = e.response?.data?.detail || '同步失败，可稍后在 家长中心 重试'
    ElMessage.error(kpMsg.value)
  } finally {
    kpBusy.value = false
  }
}

// ---------------- 第 4 步：英语单词一键同步 ----------------
const wordForm = reactive({ version: '' })
const wordVersions = ref([])
const wordBusy = ref(false)
const wordDone = ref(false)
const wordProgress = ref(0)
const wordMsg = ref('')
const canImportWord = computed(() => !!wordForm.version)

async function loadWordVersions() {
  try {
    const { data } = await syncApi.status()
    const subjects = data.catalog?.subjects || {}
    const versions = Object.keys(subjects['英语'] || {})
    wordVersions.value = versions.filter(v => {
      const books = subjects['英语'][v] || {}
      return Object.values(books).some(b => (b.words || 0) > 0)
    })
    if (wordVersions.value.length && !wordVersions.value.includes(wordForm.version)) {
      wordForm.version = wordVersions.value[0]
    }
  } catch {
    wordVersions.value = []
  }
}

async function importWords() {
  if (!canImportWord.value || wordBusy.value || wordDone.value) return
  wordBusy.value = true
  wordProgress.value = 20
  wordMsg.value = '正在同步 1~6 年级全部英语单词…'
  try {
    const { data } = await syncApi.syncWordsAll({ version: wordForm.version })
    wordProgress.value = 100
    wordDone.value = true
    wordMsg.value = `已同步 ${data.added} 个单词（${wordForm.version} 1~6 年级 ${data.books?.length || 8} 册）`
    ElMessage.success(wordMsg.value)
  } catch (e) {
    wordMsg.value = e.response?.data?.detail || '同步失败，可稍后在 单词学习 重试'
    ElMessage.error(wordMsg.value)
  } finally {
    wordBusy.value = false
  }
}

// ---------------- 通用 ----------------
const skipTo = (s) => {
  if (s < 4) step.value = s
  else finish()
}
const markOnboarded = () => {
  const trialKey = localStorage.getItem('easyfix_trial_key') || ''
  localStorage.setItem('easyfix_onboarded_' + trialKey, '1')
  sessionStorage.removeItem('easyfix_new_space')
}
const finish = () => {
  markOnboarded()
  router.push('/')
}

// ---------------- 快速体验：跳过初始化，直接用空间第一个小孩进入学习 ----------------
const quickLoading = ref(false)
async function quickEnter() {
  if (quickLoading.value) return
  quickLoading.value = true
  try {
    const { data } = await usersApi.list()
    const kids = (data.users || []).filter((u) => u.role === 'child')
    if (!kids.length) {
      ElMessage.warning('空间还没有孩子，请先在上方「第 1 步」添加一个')
      return
    }
    const kid = kids[0]
    kidStore.select(kid)
    subjectStore.select(null)
    subjectStore.applyKidDefaultGrade(kid)
    markOnboarded()
    ElMessage.success('已进入「' + (kid.display_name || kid.username) + '」的学习空间')
    router.push('/home')
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '进入失败，请稍后重试')
  } finally {
    quickLoading.value = false
  }
}

onMounted(() => {
  loadExistingKids()
  loadOpsCatalog()
  loadWordVersions()
})
</script>

<style scoped>
.onboarding {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 32px 16px;
  box-sizing: border-box;
  background:
    radial-gradient(1200px 500px at 15% -10%, rgba(102, 126, 234, 0.16), transparent 60%),
    radial-gradient(1000px 460px at 90% 0%, rgba(79, 172, 254, 0.14), transparent 55%),
    linear-gradient(180deg, #f6f9ff 0%, #eef4ff 100%);
}
.ob-card {
  width: 100%;
  max-width: 760px;
  background: #fff;
  border-radius: 20px;
  padding: 36px 44px 32px;
  box-shadow: 0 10px 40px rgba(36, 60, 120, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.9);
}
.ob-head { text-align: center; margin-bottom: 18px; }
.ob-head h1 { font-size: 26px; margin: 0 0 8px; color: #303133; }
.ob-head p { color: #909399; font-size: 13px; margin: 0; }
.ob-quick {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 14px;
  flex-wrap: wrap;
  background: linear-gradient(120deg, #f0fdf4, #ecfdf5);
  border: 1px solid #bbf7d0;
  border-radius: 14px;
  padding: 14px 18px;
  margin-bottom: 20px;
}
.ob-quick-text b { display: block; font-size: 16px; color: #166534; margin-bottom: 2px; }
.ob-quick-text span { font-size: 12px; color: #3f6212; line-height: 1.6; }
.ob-steps { margin-bottom: 26px; }
.ob-body { min-height: 300px; }
.ob-body h2 { font-size: 20px; margin: 0 0 6px; color: #303133; }
.ob-sub { color: #909399; font-size: 13px; margin: 0 0 18px; line-height: 1.7; }
.ob-form { max-width: 560px; margin: 0 auto; }
.ob-tip { font-size: 12px; color: #909399; line-height: 1.6; margin-top: 4px; }
.ob-progress { width: 260px; }
.ob-actions {
  margin-top: 24px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  flex-wrap: wrap;
}
.ob-counts { display: flex; justify-content: center; gap: 10px; margin: 6px 0 18px; }
.ob-count {
  width: 64px; padding: 10px 0 8px; border: 2px solid #e5e7eb; border-radius: 12px;
  background: #fff; cursor: pointer; text-align: center; transition: all .15s;
}
.ob-count b { display: block; font-size: 22px; color: #374151; }
.ob-count span { font-size: 11px; color: #9ca3af; }
.ob-count.on { border-color: #2563eb; background: #eff6ff; }
.ob-count.on b { color: #2563eb; }
.ob-kid-row { display: flex; gap: 8px; width: 100%; }
.ob-subjects { display: flex; gap: 10px; }
.ob-subject {
  padding: 9px 26px; border: 2px solid #e5e7eb; border-radius: 999px; background: #fff;
  cursor: pointer; font-size: 15px; color: #374151; transition: all .15s;
}
.ob-subject.on { border-color: #2563eb; background: #eff6ff; color: #2563eb; font-weight: 600; }
.ob-done { text-align: center; padding-top: 60px; }
</style>