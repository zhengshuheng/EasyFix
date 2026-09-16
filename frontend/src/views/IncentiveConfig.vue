<template>
  <div class="incentive-config">
    <el-card shadow="never">
      <el-tabs v-model="activeTab" class="mgmt-tabs">
        <!-- 行为配置 -->
        <el-tab-pane label="行为配置" name="starActions">
          <div class="tab-content">
            <!-- 积分调整区块 -->
            <div class="stars-adjust-section">
              <h4>积分调整</h4>
              <el-form :model="starsAdjustForm" :inline="true" size="default">
                <el-form-item label="积分变动">
                  <el-input-number
                    v-model="starsAdjustForm.delta"
                    :min="-9999"
                    :max="9999"
                    controls-position="right"
                    style="width: 120px"
                  />
                  <span style="margin-left: 8px; color: #909399;">（正数增加，负数减少）</span>
                </el-form-item>
                <el-form-item label="调整原因" required>
                  <el-input
                    v-model="starsAdjustForm.reason"
                    placeholder="请输入调整原因"
                    maxlength="200"
                    show-word-limit
                    style="width: 300px"
                  />
                </el-form-item>
                <el-form-item>
                  <el-button type="primary" @click="handleStarsAdjust" :loading="starsAdjustLoading">
                    确认调整
                  </el-button>
                </el-form-item>
              </el-form>
              <div v-if="starsAdjustResult !== null" class="adjust-result">
                调整后积分余额：<span class="balance-value">{{ starsAdjustResult }}</span>
              </div>
            </div>

            <div class="action-bar">
              <el-button type="primary" @click="showStarActionDialog = true">
                <el-icon><Plus /></el-icon>
                新增行为
              </el-button>
            </div>
            <el-table :data="starActions" stripe style="width: 100%; margin-top: 15px">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="code" label="行为代码" width="150" />
              <el-table-column prop="name" label="行为名称" width="120" />
              <el-table-column prop="star_value" label="积分值" width="100">
                <template #default="{ row }">
                  <span :class="row.star_value >= 0 ? 'text-success' : 'text-danger'">
                    {{ row.star_value >= 0 ? '+' : '' }}{{ row.star_value }}
                  </span>
                </template>
              </el-table-column>
              <el-table-column prop="enabled" label="启用" width="80">
                <template #default="{ row }">
                  <el-tag :type="row.enabled ? 'success' : 'info'">{{ row.enabled ? '是' : '否' }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="is_custom" label="类型" width="100">
                <template #default="{ row }">
                  <el-tag :type="row.is_custom ? 'warning' : 'primary'">{{ row.is_custom ? '自定义' : '预设' }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="180">
                <template #default="{ row }">
                  <el-button link type="primary" size="small" @click="editStarAction(row)">编辑</el-button>
                  <el-button link type="danger" size="small" @click="deleteStarAction(row)" :disabled="row.is_preset">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>

        <!-- 成就管理 -->
        <el-tab-pane label="成就管理" name="achievements">
          <div class="tab-content">
            <div class="action-bar">
              <el-button type="primary" @click="showAchievementDialog = true">
                <el-icon><Plus /></el-icon>
                新增成就
              </el-button>
            </div>
            <el-table :data="achievements" stripe style="width: 100%; margin-top: 15px">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="name" label="成就名称" width="120" />
              <el-table-column prop="level" label="等级" width="80" />
              <el-table-column prop="trigger_action" label="触发行为" width="150" />
              <el-table-column prop="trigger_count" label="触发次数" width="100" />
              <el-table-column prop="reward_stars" label="奖励积分" width="100" />
              <el-table-column prop="is_preset" label="类型" width="100">
                <template #default="{ row }">
                  <el-tag :type="row.is_preset ? 'primary' : 'warning'">{{ row.is_preset ? '预设' : '自定义' }}</el-tag>
                </template>
              </el-table-column>
              <el-table-column label="操作" width="180">
                <template #default="{ row }">
                  <el-button link type="primary" size="small" @click="editAchievement(row)" :disabled="row.is_preset">编辑</el-button>
                  <el-button link type="danger" size="small" @click="deleteAchievement(row)" :disabled="row.is_preset">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>

        <!-- 奖励管理 -->
        <el-tab-pane label="奖励管理" name="rewards">
          <div class="tab-content">
            <div class="action-bar">
              <el-button type="primary" @click="showRewardDialog = true">
                <el-icon><Plus /></el-icon>
                新增奖励
              </el-button>
            </div>
            <el-table :data="rewards" stripe style="width: 100%; margin-top: 15px">
              <el-table-column prop="id" label="ID" width="80" />
              <el-table-column prop="name" label="奖励名称" width="150" />
              <el-table-column prop="cost_stars" label="所需积分" width="100" />
              <el-table-column prop="total_stock" label="总库存" width="100">
                <template #default="{ row }">
                  {{ row.total_stock === -1 ? '无限' : row.total_stock }}
                </template>
              </el-table-column>
              <el-table-column prop="remaining_stock" label="剩余库存" width="100">
                <template #default="{ row }">
                  {{ row.remaining_stock === -1 ? '无限' : row.remaining_stock }}
                </template>
              </el-table-column>
              <el-table-column label="操作" width="180">
                <template #default="{ row }">
                  <el-button link type="primary" size="small" @click="editReward(row)">编辑</el-button>
                  <el-button link type="danger" size="small" @click="deleteReward(row)">删除</el-button>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>

    <!-- 新增/编辑行为弹窗 -->
    <el-dialog v-model="showStarActionDialog" :title="editStarActionData ? '编辑行为' : '新增行为'" width="500px">
      <el-form :model="starActionForm" label-width="100px">
        <el-form-item label="行为代码" required>
          <el-input v-model="starActionForm.code" placeholder="如: upload_question" :disabled="!!editStarActionData" />
        </el-form-item>
        <el-form-item label="行为名称" required>
          <el-input v-model="starActionForm.name" placeholder="如: 上传错题" />
        </el-form-item>
        <el-form-item label="积分值" required>
          <el-input-number v-model="starActionForm.star_value" :min="-999" :max="999" />
        </el-form-item>
        <el-form-item label="启用">
          <el-switch v-model="starActionForm.enabled" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showStarActionDialog = false">取消</el-button>
        <el-button type="primary" @click="createOrUpdateStarAction">保存</el-button>
      </template>
    </el-dialog>

    <!-- 新增/编辑成就弹窗 -->
    <el-dialog v-model="showAchievementDialog" :title="editAchievementData ? '编辑成就' : '新增成就'" width="500px">
      <el-form :model="achievementForm" label-width="100px">
        <el-form-item label="成就名称" required>
          <el-input v-model="achievementForm.name" placeholder="如: 学习达人" />
        </el-form-item>
        <el-form-item label="等级" required>
          <el-input-number v-model="achievementForm.level" :min="1" :max="10" />
        </el-form-item>
        <el-form-item label="触发行为" required>
          <el-select v-model="achievementForm.trigger_action" placeholder="选择触发行为" style="width: 100%">
            <el-option v-for="a in starActions" :key="a.code" :label="a.name" :value="a.code" />
          </el-select>
        </el-form-item>
        <el-form-item label="触发次数" required>
          <el-input-number v-model="achievementForm.trigger_count" :min="1" :max="9999" />
        </el-form-item>
        <el-form-item label="奖励积分" required>
          <el-input-number v-model="achievementForm.reward_stars" :min="0" :max="9999" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showAchievementDialog = false">取消</el-button>
        <el-button type="primary" @click="createOrUpdateAchievement">保存</el-button>
      </template>
    </el-dialog>

    <!-- 新增/编辑奖励弹窗 -->
    <el-dialog v-model="showRewardDialog" :title="editRewardData ? '编辑奖励' : '新增奖励'" width="500px">
      <el-form :model="rewardForm" label-width="100px">
        <el-form-item label="奖励名称" required>
          <el-input v-model="rewardForm.name" placeholder="如: 免作业卡" />
        </el-form-item>
        <el-form-item label="奖励描述">
          <el-input v-model="rewardForm.description" type="textarea" :rows="2" placeholder="描述奖励的用途或详情" />
        </el-form-item>
        <el-form-item label="所需积分" required>
          <el-input-number v-model="rewardForm.cost_stars" :min="0" :max="99999" />
        </el-form-item>
        <el-form-item label="总库存">
          <el-input-number v-model="rewardForm.total_stock" :min="-1" :max="99999" placeholder="-1表示无限" />
        </el-form-item>
        <el-form-item label="剩余库存">
          <el-input-number v-model="rewardForm.remaining_stock" :min="-1" :max="99999" placeholder="-1表示无限" />
        </el-form-item>
        <el-form-item label="奖励图片">
          <div v-if="rewardForm.image_url" class="reward-image-preview">
            <img :src="rewardForm.image_url" style="width:100px;height:100px;object-fit:contain;border:1px solid #ddd;" />
            <el-button type="danger" size="small" @click="removeRewardImage" style="margin-top:8px;">删除图片</el-button>
          </div>
          <el-upload
            v-else
            ref="rewardImageRef"
            :auto-upload="false"
            :limit="1"
            accept="image/*"
            :on-change="uploadRewardImage"
          >
            <el-button size="small" type="primary">点击上传图片</el-button>
          </el-upload>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="showRewardDialog = false">取消</el-button>
        <el-button type="primary" @click="createOrUpdateReward">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { uploadApi } from '@/api/question'
import { motivationApi } from '@/api/motivation'

const activeTab = ref('starActions')

// 行为配置
const starActions = ref([])
const showStarActionDialog = ref(false)
const editStarActionData = ref(null)
const starActionForm = reactive({ code: '', name: '', star_value: 0, enabled: true })

// 积分调整相关
const starsAdjustForm = reactive({
  delta: 0,
  reason: ''
})
const starsAdjustLoading = ref(false)
const starsAdjustResult = ref(null)

const fetchBalance = async () => {
  try {
    const { data } = await motivationApi.getBalance()
    starsAdjustResult.value = data.balance
  } catch (e) {
    console.error('获取积分余额失败:', e)
  }
}

const handleStarsAdjust = async () => {
  if (!starsAdjustForm.reason.trim()) {
    ElMessage.warning('请输入调整原因')
    return
  }
  try {
    starsAdjustLoading.value = true
    const { data } = await motivationApi.adjustStars({
      delta: starsAdjustForm.delta,
      reason: starsAdjustForm.reason
    })
    starsAdjustResult.value = data.new_balance
    starsAdjustForm.delta = 0
    starsAdjustForm.reason = ''
    ElMessage.success('积分调整成功')
    fetchBalance()
  } catch (error) {
    ElMessage.error(error.detail || '调整失败')
  } finally {
    starsAdjustLoading.value = false
  }
}

// 成就管理
const achievements = ref([])
const showAchievementDialog = ref(false)
const editAchievementData = ref(null)
const achievementForm = reactive({ name: '', level: 1, trigger_action: '', trigger_count: 1, reward_stars: 0 })

// 奖励管理
const rewards = ref([])
const showRewardDialog = ref(false)
const editRewardData = ref(null)
const rewardForm = reactive({ name: '', description: '', cost_stars: 0, total_stock: -1, remaining_stock: -1, image_url: '' })

// 获取行为列表
const fetchStarActions = async () => {
  try {
    const { data } = await motivationApi.getActions()
    starActions.value = Array.isArray(data) ? data : (data.items || [])
  } catch (e) {
    console.error('获取行为列表失败:', e)
  }
}

// 创建或更新行为
const createOrUpdateStarAction = async () => {
  if (!starActionForm.code.trim()) {
    ElMessage.warning('请输入行为代码')
    return
  }
  if (!starActionForm.name.trim()) {
    ElMessage.warning('请输入行为名称')
    return
  }
  try {
    if (editStarActionData.value) {
      await motivationApi.updateAction(editStarActionData.value.id, starActionForm)
      ElMessage.success('更新成功')
    } else {
      await motivationApi.createAction(starActionForm)
      ElMessage.success('创建成功')
    }
    showStarActionDialog.value = false
    editStarActionData.value = null
    starActionForm.code = ''
    starActionForm.name = ''
    starActionForm.star_value = 0
    starActionForm.enabled = true
    fetchStarActions()
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

// 编辑行为
const editStarAction = (row) => {
  editStarActionData.value = row
  starActionForm.code = row.code
  starActionForm.name = row.name
  starActionForm.star_value = row.star_value
  starActionForm.enabled = row.enabled
  showStarActionDialog.value = true
}

// 删除行为
const deleteStarAction = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该行为吗？', '删除确认', { type: 'warning' })
    await motivationApi.deleteAction(row.id)
    ElMessage.success('删除成功')
    fetchStarActions()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('删除失败')
  }
}

// 获取成就列表
const fetchAchievements = async () => {
  try {
    const { data } = await motivationApi.getAchievements()
    achievements.value = Array.isArray(data) ? data : (data.items || [])
  } catch (e) {
    console.error('获取成就列表失败:', e)
  }
}

// 创建或更新成就
const createOrUpdateAchievement = async () => {
  if (!achievementForm.name.trim()) {
    ElMessage.warning('请输入成就名称')
    return
  }
  if (!achievementForm.trigger_action) {
    ElMessage.warning('请选择触发行为')
    return
  }
  try {
    if (editAchievementData.value) {
      await motivationApi.updateAchievement(editAchievementData.value.id, achievementForm)
      ElMessage.success('更新成功')
    } else {
      await motivationApi.createAchievement(achievementForm)
      ElMessage.success('创建成功')
    }
    showAchievementDialog.value = false
    editAchievementData.value = null
    achievementForm.name = ''
    achievementForm.level = 1
    achievementForm.trigger_action = ''
    achievementForm.trigger_count = 1
    achievementForm.reward_stars = 0
    fetchAchievements()
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

// 编辑成就
const editAchievement = (row) => {
  editAchievementData.value = row
  achievementForm.name = row.name
  achievementForm.level = row.level
  achievementForm.trigger_action = row.trigger_action
  achievementForm.trigger_count = row.trigger_count
  achievementForm.reward_stars = row.reward_stars
  showAchievementDialog.value = true
}

// 删除成就
const deleteAchievement = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该成就吗？', '删除确认', { type: 'warning' })
    await motivationApi.deleteAchievement(row.id)
    ElMessage.success('删除成功')
    fetchAchievements()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('删除失败')
  }
}

// 获取奖励列表
const fetchRewards = async () => {
  try {
    const { data } = await motivationApi.getRewards()
    rewards.value = Array.isArray(data) ? data : (data.items || [])
  } catch (e) {
    console.error('获取奖励列表失败:', e)
  }
}

// 创建或更新奖励
const createOrUpdateReward = async () => {
  if (!rewardForm.name.trim()) {
    ElMessage.warning('请输入奖励名称')
    return
  }
  try {
    if (editRewardData.value) {
      await motivationApi.updateReward(editRewardData.value.id, rewardForm)
      ElMessage.success('更新成功')
    } else {
      await motivationApi.createReward(rewardForm)
      ElMessage.success('创建成功')
    }
    showRewardDialog.value = false
    editRewardData.value = null
    rewardForm.name = ''
    rewardForm.description = ''
    rewardForm.cost_stars = 0
    rewardForm.total_stock = -1
    rewardForm.remaining_stock = -1
    rewardForm.image_url = ''
    fetchRewards()
  } catch (e) {
    ElMessage.error('保存失败')
  }
}

// 上传奖励图片
const rewardImageRef = ref(null)
const uploadRewardImage = async (file) => {
  try {
    const { data } = await uploadApi.uploadFile(file.raw)
    rewardForm.image_url = '/uploads/' + data.path
    ElMessage.success('图片上传成功')
  } catch (e) {
    console.error('上传失败:', e)
    ElMessage.error('图片上传失败')
  }
  return false
}

const removeRewardImage = () => {
  rewardForm.image_url = ''
}

// 编辑奖励
const editReward = (row) => {
  editRewardData.value = row
  rewardForm.name = row.name
  rewardForm.description = row.description || ''
  rewardForm.cost_stars = row.cost_stars
  rewardForm.total_stock = row.total_stock
  rewardForm.remaining_stock = row.remaining_stock
  rewardForm.image_url = row.image_url || ''
  showRewardDialog.value = true
}

// 删除奖励
const deleteReward = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除该奖励吗？', '删除确认', { type: 'warning' })
    await motivationApi.deleteReward(row.id)
    ElMessage.success('删除成功')
    fetchRewards()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('删除失败')
  }
}

onMounted(() => {
  fetchStarActions()
  fetchAchievements()
  fetchRewards()
  fetchBalance()
})
</script>

<style scoped>
.incentive-config {
  width: 100%;
}

.tab-content {
  padding: 10px 0;
}

.action-bar {
  margin-bottom: 10px;
}

.text-success {
  color: #67c23a;
  font-weight: bold;
}

.text-danger {
  color: #f56c6c;
  font-weight: bold;
}

.stars-adjust-section {
  background: #f5f7fa;
  border-radius: 8px;
  padding: 16px;
  margin-bottom: 20px;
}

.stars-adjust-section h4 {
  margin: 0 0 12px 0;
  color: #303133;
}

.adjust-result {
  margin-top: 12px;
  color: #606266;
}

.balance-value {
  font-size: 18px;
  font-weight: bold;
  color: #409eff;
}

/* 激励配置子导航：顶部横向 tabs */
.mgmt-tabs :deep(.el-tabs__item) {
  height: 44px;
  line-height: 44px;
  font-size: 14px;
}

.mgmt-tabs :deep(.el-tabs__content) {
  padding: 12px 2px 0;
  overflow: visible;
}

.incentive-config :deep(.el-card) {
  transition: none;
}
.incentive-config :deep(.el-card:hover) {
  transform: none;
  box-shadow: var(--shadow-sm) !important;
}
</style>
