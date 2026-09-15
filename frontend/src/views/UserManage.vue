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
        <el-table-column prop="username" label="用户名" min-width="110" />
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
        <el-table-column prop="created_at" label="创建时间" min-width="160">
          <template #default="{ row }">
            {{ (row.created_at || '').replace('T', ' ').slice(0, 19) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="240" fixed="right">
          <template #default="{ row }">
            <el-button link type="primary" size="small" @click="openEdit(row)">编辑</el-button>
            <el-button link type="warning" size="small" @click="openPassword(row)">
              {{ row.role === 'admin' ? '改密码' : '改PIN' }}
            </el-button>
            <el-button
              link
              type="danger"
              size="small"
              :disabled="row.id === authStore.user?.id"
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
        <el-form-item v-else label="PIN 码">
          <el-input v-model="createForm.pin" placeholder="4 位数字" maxlength="4" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="createVisible = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="handleCreate">创建</el-button>
      </template>
    </el-dialog>

    <!-- 编辑显示名/状态 -->
    <el-dialog v-model="editVisible" title="编辑用户" width="420px">
      <el-form label-width="80px">
        <el-form-item label="显示名">
          <el-input v-model="editForm.display_name" />
        </el-form-item>
        <el-form-item label="状态">
          <el-switch v-model="editForm.enabled" active-text="启用" inactive-text="禁用" />
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
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const users = ref([])
const loading = ref(false)
const saving = ref(false)

const createVisible = ref(false)
const createForm = reactive({ role: 'child', username: '', display_name: '', password: '', pin: '' })

const editVisible = ref(false)
const editForm = reactive({ id: null, display_name: '', enabled: true })

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
  Object.assign(createForm, { role, username: '', display_name: '', password: '', pin: '' })
  createVisible.value = true
}

async function handleCreate() {
  const payload = {
    username: createForm.username.trim(),
    role: createForm.role,
    display_name: createForm.display_name || undefined,
  }
  if (createForm.role === 'admin') payload.password = createForm.password
  else payload.pin = createForm.pin
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
  Object.assign(editForm, { id: row.id, display_name: row.display_name, enabled: !!row.enabled })
  editVisible.value = true
}

async function handleEdit() {
  saving.value = true
  try {
    await usersApi.update(editForm.id, {
      display_name: editForm.display_name,
      enabled: editForm.enabled,
    })
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

onMounted(load)
</script>

<style scoped>
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
