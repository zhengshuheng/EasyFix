<template>
  <div class="user-manage">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>账号管理</span>
          <div>
            <el-tag size="small" type="info" class="limit-tag">家长最多 2 个</el-tag>
            <el-tag size="small" type="info">小孩最多 5 个</el-tag>
            <el-button type="primary" size="small" style="margin-left: 12px" @click="openCreate('child')">
              添加小孩
            </el-button>
            <el-button type="warning" size="small" @click="openCreate('admin')">添加家长</el-button>
          </div>
        </div>
      </template>

      <el-table :data="users" v-loading="loading" stripe>
        <el-table-column prop="id" label="ID" width="60" />
        <el-table-column label="用户名" min-width="150">
          <template #default="{ row }">
            <span>{{ row.username }}</span>
            <el-tag v-if="row.is_owner" size="small" type="warning" style="margin-left: 6px">主账号</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="display_name" label="显示名" min-width="110" />
        <el-table-column label="角色" width="90">
          <template #default="{ row }">
            <el-tag :type="row.role === 'admin' ? 'danger' : 'success'" size="small">
              {{ row.role === 'admin' ? '家长' : '小孩' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="状态" width="90">
          <template #default="{ row }">
            <el-tag :type="row.enabled ? 'primary' : 'info'" size="small" effect="plain">
              {{ row.enabled ? '启用' : '禁用' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="入学日期 / 当前年级" width="170">
          <template #default="{ row }">
            <template v-if="row.role === 'child'">
              <div>{{ row.enrollment_date || '未设置' }}</div>
              <el-tag size="small" type="success" effect="plain">{{ gradeName(row.current_grade) }}</el-tag>
            </template>
            <span v-else>-</span>
          </template>
        </el-table-column>
        <el-table-column prop="created_at" label="创建时间" min-width="160">
          <template #default="{ row }">
            {{ (row.created_at || '').replace('T', ' ').slice(0, 19) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="240" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="openEdit(row)">编辑</el-button>
            <el-button v-if="row.role === 'admin'" link type="warning" size="small" @click="openPassword(row)">改密码</el-button>
            <el-button
              v-if="authStore.user?.is_owner"
              link
              type="danger"
              size="small"
              :disabled="row.id === authStore.user?.id || row.is_owner"
              @click="handleDelete(row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 创建用户 -->
    <el-dialog v-model="createVisible" :title="createForm.role === 'admin' ? '添加家长' : '添加小孩'" width="420px">
      <el-form label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="createForm.username" placeholder="登录用户名" />
        </el-form-item>
        <el-form-item label="显示名">
          <el-input v-model="createForm.display_name" placeholder="可选，默认同用户名" />
        </el-form-item>
        <el-form-item v-if="createForm.role === 'admin'" label="密码">
          <el-input v-model="createForm.password" type="password" placeholder="至少 4 位" show-password />
        </el-form-item>
        <el-form-item v-else label="入学日期">
          <el-date-picker
            v-model="createForm.enrollment_date"
            type="date"
            value-format="YYYY-MM-DD"
            placeholder="一年级入学日期（9月开学）"
            :clearable="true"
            style="width: 100%"
          />
          <div class="grade-tip">系统按 9 月 1 日开学自动推断当前年级（例如 2024-09-01 入学 → 现在三年级）</div>
        </el-form-item>
        <el-form-item v-if="createForm.role === 'child'" label="教材版本">
          <div style="width: 100%">
            <div v-for="s in subjects" :key="s.id" class="tb-row">
              <span class="tb-label">{{ s.name }}</span>
              <el-select
                v-model="tbMap[s.id]"
                placeholder="不绑定（用全部知识点）"
                clearable
                style="flex: 1"
              >
                <el-option v-for="v in versionOptions[s.name] || []" :key="v" :label="v" :value="v" />
              </el-select>
            </div>
            <div class="grade-tip">
              绑定后，AI 出题按该教材版本筛选知识点（未导入该版本时仍可见通用/自定义知识点）；可随时在「编辑」里修改。
            </div>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="createVisible = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="handleCreate">创建</el-button>
      </template>
    </el-dialog>

    <!-- 编辑显示名/状态/当前年级 -->
    <el-dialog v-model="editVisible" title="编辑用户" width="420px">
      <el-form label-width="80px">
        <el-form-item label="显示名">
          <el-input v-model="editForm.display_name" />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="editForm.enabled" active-text="启用" inactive-text="禁用" />
        </el-form-item>
        <el-form-item v-if="editForm.role === 'child'" label="入学日期">
          <el-date-picker
            v-model="editForm.enrollment_date"
            type="date"
            value-format="YYYY-MM-DD"
            placeholder="一年级入学日期（9月开学）"
            :clearable="true"
            style="width: 100%"
          />
          <div class="grade-tip">
            系统按 9 月 1 日开学自动推断当前年级：{{ gradeName(editForm.current_grade) }}。
            小孩点选进入后，默认就是该年级的学习空间。
          </div>
        </el-form-item>
        <el-form-item v-if="editForm.role === 'child'" label="教材版本">
          <div style="width: 100%">
            <div v-for="s in subjects" :key="s.id" class="tb-row">
              <span class="tb-label">{{ s.name }}</span>
              <el-select
                v-model="tbMap[s.id]"
                placeholder="不绑定（用全部知识点）"
                clearable
                style="flex: 1"
              >
                <el-option v-for="v in versionOptions[s.name] || []" :key="v" :label="v" :value="v" />
              </el-select>
            </div>
            <div class="grade-tip">修改后立即生效，AI 出题按新版本筛选知识点。</div>
          </div>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="editVisible = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="handleEdit">保存</el-button>
      </template>
    </el-dialog>

    <!-- 改密码/PIN -->
    <el-dialog v-model="pwVisible" :title="pwForm.role === 'admin' ? '修改密码' : '修改 PIN'" width="420px">
      <el-form label-width="80px">
        <el-form-item v-if="pwForm.role === 'admin'" label="新密码">
          <el-input v-model="pwForm.password" type="password" placeholder="至少 4 位" show-password />
        </el-form-item>
        <el-form-item v-else label="新 PIN">
          <el-input v-model="pwForm.pin" placeholder="4 位数字" maxlength="4" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="pwVisible = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="handlePassword">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { onMounted, reactive, ref } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { usersApi } from '@/api/users'
import { questionApi } from '@/api/question'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const users = ref([])
const loading = ref(false)
const saving = ref(false)

// 教材版本选项（按学科；建小孩/编辑时选择）
const subjects = ref([])
const versionOptions = ref({}) // 学科名 -> 版本列表
const tbMap = reactive({})     // subject_id -> 选中的版本名

async function loadTextbookOptions() {
  try {
    const [sub, ver] = await Promise.all([
      questionApi.listSubjects(),
      questionApi.getTextbookVersions(),
    ])
    subjects.value = (sub.data || []).filter((s) => !s.deleted)
    versionOptions.value = ver.data?.versions || {}
  } catch (e) {
    // 版本选项加载失败不阻塞建小孩；仅不显示教材绑定
    console.error('加载教材版本选项失败:', e)
  }
}

function initTbMap(textbooks = []) {
  Object.keys(tbMap).forEach((k) => delete tbMap[k])
  for (const t of textbooks || []) {
    if (t.subject_id) tbMap[t.subject_id] = t.version_name
  }
}

function buildTextbooks() {
  const list = []
  for (const s of subjects.value) {
    const v = tbMap[s.id]
    if (!v) continue
    list.push({ subject_id: s.id, version_name: v, source: 'package' })
  }
  return list
}

const createVisible = ref(false)
const createForm = reactive({ role: 'child', username: '', display_name: '', password: '', pin: '', enrollment_date: null })

const editVisible = ref(false)
const editForm = reactive({ id: null, role: 'child', display_name: '', enabled: true, enrollment_date: null, current_grade: 1 })

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

function gradeName(g) {
  if (g == null || g === '') return '未设置'
  const item = gradeOptions.find((x) => x.value === Number(g))
  return item ? item.label : g + '年级'
}

const pwVisible = ref(false)
const pwForm = reactive({ id: null, role: 'child', password: '', pin: '' })

async function load() {
  loading.value = true
  try {
    const { data } = await usersApi.list()
    users.value = data.users || []
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '加载用户失败')
  } finally {
    loading.value = false
  }
}

function openCreate(role) {
  Object.assign(createForm, { role, username: '', display_name: '', password: '', pin: '', enrollment_date: null })
  initTbMap()
  createVisible.value = true
}

async function handleCreate() {
  const payload = {
    username: createForm.username.trim(),
    role: createForm.role,
    display_name: createForm.display_name || undefined,
  }
  if (createForm.role === 'admin') payload.password = createForm.password
  else {
    payload.enrollment_date = createForm.enrollment_date || undefined
    const tbs = buildTextbooks()
    if (tbs.length) payload.textbooks = tbs
  }
  saving.value = true
  try {
    await usersApi.create(payload)
    ElMessage.success('创建成功')
    createVisible.value = false
    load()
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '创建失败')
  } finally {
    saving.value = false
  }
}

function openEdit(row) {
  Object.assign(editForm, {
    id: row.id,
    role: row.role,
    display_name: row.display_name,
    enabled: !!row.enabled,
    enrollment_date: row.enrollment_date || null,
    current_grade: row.current_grade || 1,
  })
  initTbMap(row.textbooks)
  editVisible.value = true
}

async function handleEdit() {
  saving.value = true
  try {
    const payload = {
      display_name: editForm.display_name,
      enabled: editForm.enabled,
    }
    if (editForm.role === 'child') payload.enrollment_date = editForm.enrollment_date || null
    await usersApi.update(editForm.id, payload)
    // 教材版本偏好单独保存（全量替换）
    if (editForm.role === 'child') {
      await usersApi.putTextbooks(editForm.id, buildTextbooks())
    }
    ElMessage.success('已保存')
    editVisible.value = false
    load()
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '保存失败')
  } finally {
    saving.value = false
  }
}

function openPassword(row) {
  Object.assign(pwForm, { id: row.id, role: row.role, password: '', pin: '' })
  pwVisible.value = true
}

async function handlePassword() {
  const payload = pwForm.role === 'admin' ? { password: pwForm.password } : { pin: pwForm.pin }
  saving.value = true
  try {
    await usersApi.updatePassword(pwForm.id, payload)
    ElMessage.success('已修改')
    pwVisible.value = false
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '修改失败')
  } finally {
    saving.value = false
  }
}

async function handleDelete(row) {
  try {
    await ElMessageBox.confirm(
      `确定删除用户「${row.username}」吗？该操作不可恢复。`,
      '删除确认',
      { type: 'warning', confirmButtonText: '删除', cancelButtonText: '取消' }
    )
  } catch {
    return
  }
  try {
    await usersApi.remove(row.id)
    ElMessage.success('已删除')
    load()
  } catch (e) {
    ElMessage.error(e.response?.data?.detail || '删除失败')
  }
}

onMounted(() => {
  load()
  loadTextbookOptions()
  // 刷新当前用户信息（确保 is_owner 等字段为最新；旧登录态 localStorage 可能缺该字段）
  authStore.refreshMe().catch(() => {})
})
</script>

<style scoped>
.no-pin-tip {
  font-size: 13px;
  color: #909399;
  line-height: 32px;
}

.tb-row {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}

.tb-label {
  width: 44px;
  font-size: 13px;
  color: #606266;
  flex-shrink: 0;
}

.grade-tip {
  font-size: 12px;
  color: #909399;
  line-height: 1.5;
  margin-top: 4px;
}

.card-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  flex-wrap: wrap;
  gap: 8px;
}

.limit-tag {
  margin-right: 6px;
}
</style>
