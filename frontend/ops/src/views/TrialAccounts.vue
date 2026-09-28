<template>
  <el-card shadow="never">
    <div class="head">
      <h2>🧑‍🤝‍🧑 体验账号管理</h2>
    </div>
    <p class="hint">管理官网注册的体验账号：查看基本信息（账号 / 小孩数量 / 创建时间 / 到期时间），延长体验期，或删除账号（将连带删除其名下全部空间数据，不可恢复）。</p>

    <el-table :data="items" border stripe v-loading="loading">
      <el-table-column prop="username" label="账号" min-width="130" />
      <el-table-column prop="subscription_plan" label="订阅" width="90">
        <template #default="{ row }">
          <el-tag v-if="row.status === 'pro'" type="success" size="small">正式版</el-tag>
          <el-tag v-else type="warning" size="small">体验</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="children_count" label="小孩数量" width="90" align="center" />
      <el-table-column label="创建时间" width="175">
        <template #default="{ row }">{{ row.created_at }}</template>
      </el-table-column>
      <el-table-column label="到期时间" width="175">
        <template #default="{ row }">
          <span v-if="row.status === 'pro'" style="color:#16a34a;">不限</span>
          <span v-else-if="row.status === 'expired'" style="color:#dc2626;">{{ row.trial_end_at }}</span>
          <span v-else>{{ row.trial_end_at }}</span>
        </template>
      </el-table-column>
      <el-table-column label="状态" width="90" align="center">
        <template #default="{ row }">
          <el-tag v-if="row.status === 'pro'" type="success" size="small">正式版</el-tag>
          <el-tag v-else-if="row.status === 'expired'" type="danger" size="small">已过期</el-tag>
          <el-tag v-else type="primary" size="small">体验中</el-tag>
        </template>
      </el-table-column>
      <el-table-column label="操作" width="170" fixed="right">
        <template #default="{ row }">
          <el-button size="small" @click="openExtend(row)">延长体验</el-button>
          <el-button size="small" type="danger" @click="confirmDelete(row)">删除</el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 延长体验弹窗 -->
    <el-dialog v-model="extendVisible" title="延长体验时间" width="480px" destroy-on-close>
      <template v-if="current">
        <el-form label-width="90px">
          <el-form-item label="账号">
            <span>{{ current.username }}</span>
          </el-form-item>
          <el-form-item label="当前到期">
            <span v-if="current.status === 'pro'" style="color:#16a34a;">不限（正式版）</span>
            <span v-else>{{ current.trial_end_at }}</span>
          </el-form-item>
          <el-form-item label="延长天数">
            <el-input-number v-model="extendDays" :min="1" :max="3650" style="width: 180px" />
            <el-button-group style="margin-left: 12px;">
              <el-button size="small" @click="extendDays = 7">+7</el-button>
              <el-button size="small" @click="extendDays = 15">+15</el-button>
              <el-button size="small" @click="extendDays = 30">+30</el-button>
              <el-button size="small" @click="extendDays = 90">+90</el-button>
            </el-button-group>
          </el-form-item>
          <el-form-item v-if="current.status !== 'pro'" label="延长后到期">
            <span style="font-weight: 600;">{{ previewEnd }}</span>
          </el-form-item>
        </el-form>
        <el-alert v-if="current.status === 'pro'" type="warning" :closable="false" show-icon
          title="该账号已是正式版（不限体验期），无需延长。" />
      </template>
      <template #footer>
        <el-button @click="extendVisible = false">取消</el-button>
        <el-button type="primary" :loading="saving" :disabled="current?.status === 'pro'" @click="doExtend">
          确认延长
        </el-button>
      </template>
    </el-dialog>

    <!-- 删除确认弹窗 -->
    <el-dialog v-model="deleteVisible" title="删除体验账号" width="480px">
      <p>
        确定删除账号 <b>{{ current?.username }}</b>？<br />
        将同时删除其名下空间（{{ current?.children_count }} 个小孩的全部学习数据），<b>不可恢复</b>。
      </p>
      <template #footer>
        <el-button @click="deleteVisible = false">取消</el-button>
        <el-button type="danger" :loading="saving" @click="doDelete">确认删除</el-button>
      </template>
    </el-dialog>
  </el-card>
</template>

<script setup>
import { computed, onMounted, ref } from 'vue'
import { ElMessage } from 'element-plus'
import { opsApi } from '../api/ops.js'

const api = opsApi()
const items = ref([])
const loading = ref(false)
const saving = ref(false)
const extendVisible = ref(false)
const deleteVisible = ref(false)
const extendDays = ref(7)
const current = ref(null)

async function load() {
  loading.value = true
  try {
    const d = await api.get('/trial-accounts')
    items.value = d.items || []
  } catch {
    // 拦截器已提示
  } finally {
    loading.value = false
  }
}

function openExtend(row) {
  current.value = row
  extendDays.value = 7
  extendVisible.value = true
}

const previewEnd = computed(() => {
  if (!current.value || current.value.status === 'pro') return ''
  const end = new Date(current.value.trial_end_at.replace(' ', 'T'))
  if (isNaN(end.getTime())) return ''
  const d = new Date(end.getTime() + extendDays.value * 86400000)
  const p = (n) => String(n).padStart(2, '0')
  return `${d.getFullYear()}-${p(d.getMonth() + 1)}-${p(d.getDate())} ${p(d.getHours())}:${p(d.getMinutes())}:${p(d.getSeconds())}`
})

async function doExtend() {
  saving.value = true
  try {
    const d = await api.post(`/trial-accounts/${current.value.account_id}/extend`, { days: extendDays.value })
    ElMessage.success(`已延长 ${d.extended_days} 天，到期时间：${d.trial_end_at}`)
    extendVisible.value = false
    await load()
  } catch {
    // 拦截器已提示
  } finally {
    saving.value = false
  }
}

function confirmDelete(row) {
  current.value = row
  deleteVisible.value = true
}

async function doDelete() {
  saving.value = true
  try {
    await api.delete(`/trial-accounts/${current.value.account_id}`)
    ElMessage.success(`已删除账号 ${current.value.username}`)
    deleteVisible.value = false
    await load()
  } catch {
    // 拦截器已提示
  } finally {
    saving.value = false
  }
}

onMounted(load)
</script>

<style scoped>
.head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 4px;
}
.head h2 {
  font-size: 16px;
  margin: 0 0 4px;
}
.hint {
  color: #6b7280;
  font-size: 13px;
  margin: 0 0 14px;
}
</style>
