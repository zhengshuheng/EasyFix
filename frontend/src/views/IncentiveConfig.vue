<template>
  <div class="incentive-config">
    <el-card shadow="never">
      <el-tabs v-model="activeTab" class="mgmt-tabs">
        <!-- 奖励管理（家长自主配置） -->
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

        <!-- 积分调整（家长家务奖励/惩罚） -->
        <el-tab-pane label="积分调整" name="starsAdjust">
          <div class="tab-content">
            <div class="stars-adjust-section">
              <h4>手动调整孩子积分</h4>
              <el-form :model="starsAdjustForm" :inline="true" size="default">
                <el-form-item label="选择小孩" required>
                  <el-select
                    v-model="starsAdjustForm.kid_id"
                    placeholder="请选择小孩"
                    style="width: 150px"
                    @change="fetchBalance"
                  >
                    <el-option
                      v-for="kid in kidsList"
                      :key="kid.id"
                      :label="kid.display_name || kid.username"
                      :value="kid.id"
                    />
                  </el-select>
                </el-form-item>
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
                    placeholder="如: 帮忙做家务奖励"
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
                当前积分余额：<span class="balance-value">{{ starsAdjustResult }}</span>
              </div>
            </div>
          </div>
        </el-tab-pane>

        <!-- 兑换记录（家长查看孩子兑换并线下发放） -->
        <el-tab-pane label="兑换记录" name="redemptions">
          <div class="tab-content">
            <div class="stars-adjust-section" style="margin-bottom: 15px;">
              <el-form :inline="true" size="default">
                <el-form-item label="选择小孩">
                  <el-select v-model="redemptionKidId" placeholder="请选择小孩" style="width: 150px" @change="fetchRedemptions">
                    <el-option
                      v-for="kid in kidsList"
                      :key="kid.id"
                      :label="kid.display_name || kid.username"
                      :value="kid.id"
                    />
                  </el-select>
                </el-form-item>
              </el-form>
            </div>
            <el-table :data="redemptions" stripe style="width: 100%; margin-top: 15px">
              <el-table-column prop="reward_name" label="奖励" width="160" />
              <el-table-column prop="star_cost" label="消耗积分" width="110" />
              <el-table-column prop="redeemed_at" label="兑换时间" width="200" />
            </el-table>
            <el-empty v-if="!loading && redemptions.length === 0" description="暂无兑换记录" />
          </div>
        </el-tab-pane>

        <!-- 行为规则（家长可调整积分值，默认值由运营中心同步） -->
        <el-tab-pane label="行为规则" name="starRules">
          <div class="tab-content">
            <div class="rule-tip">
              默认值由运营中心统一配置；每个家长可在本空间调整积分值并保存，保存后仅对本空间生效。
              运营中心更新默认值后，未自定义的规则自动跟随新默认。
            </div>
            <div class="action-bar">
              <el-button type="primary" @click="saveStarActions" :loading="savingActions">保存修改</el-button>
              <el-button @click="restoreAll">恢复全部默认</el-button>
            </div>
            <el-table :data="starActions" stripe style="width: 100%; margin-top: 15px">
              <el-table-column prop="name" label="行为名称" width="180" />
              <el-table-column label="积分值" width="170">
                <template #default="{ row }">
                  <el-input-number v-model="row.star_value" :min="-9999" :max="9999" controls-position="right" style="width: 130px" />
                </template>
              </el-table-column>
              <el-table-column label="来源" width="120">
                <template #default="{ row }">
                  <el-tag v-if="row.ops_override" type="warning" size="small">本空间自定义</el-tag>
                  <el-tag v-else type="info" size="small">运营默认</el-tag>
                </template>
              </el-table-column>
              <el-table-column prop="enabled" label="状态" width="120">
                <template #default="{ row }">
                  <el-tag :type="row.enabled ? 'success' : 'info'">{{ row.enabled ? '启用中' : '已停用' }}</el-tag>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>

        <!-- 成就规则（家长可调整触发次数/奖励积分，默认值由运营中心同步） -->
        <el-tab-pane label="成就规则" name="achievementRules">
          <div class="tab-content">
            <div class="rule-tip">
              成就的触发次数与奖励积分默认值由运营中心统一配置；每个家长可在本空间调整并保存，
              保存后仅对本空间生效。运营中心更新默认值后，未自定义的规则自动跟随新默认。
            </div>
            <div class="action-bar">
              <el-button type="primary" @click="saveAchievements" :loading="savingAchievements">保存修改</el-button>
              <el-button @click="restoreAll">恢复全部默认</el-button>
            </div>
            <el-table :data="achievements" stripe style="width: 100%; margin-top: 15px">
              <el-table-column prop="name" label="成就名称" width="170" />
              <el-table-column prop="level" label="等级" width="60" />
              <el-table-column label="触发行为" width="150">
                <template #default="{ row }">{{ actionName(row.trigger_action) }}</template>
              </el-table-column>
              <el-table-column label="触发次数" width="150">
                <template #default="{ row }">
                  <el-input-number v-model="row.trigger_count" :min="1" :max="9999" controls-position="right" style="width: 120px" />
                </template>
              </el-table-column>
              <el-table-column label="奖励积分" width="150">
                <template #default="{ row }">
                  <el-input-number v-model="row.reward_stars" :min="0" :max="9999" controls-position="right" style="width: 120px" />
                </template>
              </el-table-column>
              <el-table-column label="来源" width="120">
                <template #default="{ row }">
                  <el-tag v-if="row.ops_override" type="warning" size="small">本空间自定义</el-tag>
                  <el-tag v-else type="info" size="small">运营默认</el-tag>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>

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
import { usersApi } from '@/api/users'

const activeTab = ref('rewards')

// 积分调整相关
const starsAdjustForm = reactive({
  kid_id: null,
  delta: 0,
  reason: ''
})
const starsAdjustLoading = ref(false)
const starsAdjustResult = ref(null)
const kidsList = ref([])

// 兑换记录
const redemptionKidId = ref(null)
const redemptions = ref([])
const loading = ref(false)

const loadKids = async () => {
  try {
    const { data } = await usersApi.listKids()
    kidsList.value = data || []
    if (kidsList.value.length > 0) {
      if (!starsAdjustForm.kid_id) starsAdjustForm.kid_id = kidsList.value[0].id
      if (!redemptionKidId.value) redemptionKidId.value = kidsList.value[0].id
    }
    if (starsAdjustForm.kid_id) {
      fetchBalance()
    }
    if (redemptionKidId.value) {
      fetchRedemptions()
    }
  } catch (e) {
    console.error('获取小孩列表失败:', e)
  }
}

const fetchBalance = async () => {
  if (!starsAdjustForm.kid_id) return
  try {
    const { data } = await motivationApi.getBalance({ kid_id: starsAdjustForm.kid_id })
    starsAdjustResult.value = data.balance
  } catch (e) {
    console.error('获取积分余额失败:', e)
  }
}

const handleStarsAdjust = async () => {
  if (!starsAdjustForm.kid_id) {
    ElMessage.warning('请先选择小孩')
    return
  }
  if (!starsAdjustForm.reason.trim()) {
    ElMessage.warning('请输入调整原因')
    return
  }
  try {
    starsAdjustLoading.value = true
    const { data } = await motivationApi.adjustStars({
      kid_id: starsAdjustForm.kid_id,
      delta: starsAdjustForm.delta,
      reason: starsAdjustForm.reason
    })
    starsAdjustResult.value = data.new_balance
    starsAdjustForm.delta = 0
    starsAdjustForm.reason = ''
    ElMessage.success('积分调整成功')
    fetchBalance()
  } catch (error) {
    ElMessage.error(error.detail || error?.response?.data?.detail || '调整失败')
  } finally {
    starsAdjustLoading.value = false
  }
}

const fetchRedemptions = async () => {
  if (!redemptionKidId.value) return
  loading.value = true
  try {
    const { data } = await motivationApi.getRedemptions({ kid_id: redemptionKidId.value })
    redemptions.value = Array.isArray(data) ? data : (data.items || [])
  } catch (e) {
    console.error('获取兑换记录失败:', e)
  } finally {
    loading.value = false
  }
}

// 行为规则（家长可调整积分值，默认值运营中心同步）
const starActions = ref([])
const savingActions = ref(false)
const fetchStarActions = async () => {
  try {
    const { data } = await motivationApi.getActions()
    starActions.value = Array.isArray(data) ? data : (data.items || [])
  } catch (e) {
    console.error('获取行为规则失败:', e)
  }
}

// 成就规则（家长可调整触发次数/奖励积分，默认值运营中心同步）
const achievements = ref([])
const savingAchievements = ref(false)
const fetchAchievements = async () => {
  try {
    const { data } = await motivationApi.getAchievements()
    achievements.value = Array.isArray(data) ? data : (data.items || [])
  } catch (e) {
    console.error('获取成就规则失败:', e)
  }
}

const actionName = (code) => {
  const hit = starActions.value.find((a) => a.code === code)
  return hit ? hit.name : (code || '-')
}

const saveStarActions = async () => {
  savingActions.value = true
  try {
    await motivationApi.saveIncentiveSettings({
      actions: starActions.value.map((a) => ({ code: a.code, star_value: a.star_value })),
      achievements: []
    })
    ElMessage.success('行为规则已保存，本空间生效')
    fetchStarActions()
    fetchAchievements()
  } catch (e) {
    ElMessage.error(e?.response?.data?.detail || '保存失败')
  } finally {
    savingActions.value = false
  }
}

const saveAchievements = async () => {
  savingAchievements.value = true
  try {
    await motivationApi.saveIncentiveSettings({
      actions: [],
      achievements: achievements.value.map((a) => ({
        code: a.code,
        level: a.level,
        trigger_count: a.trigger_count,
        reward_stars: a.reward_stars
      }))
    })
    ElMessage.success('成就规则已保存，本空间生效')
    fetchStarActions()
    fetchAchievements()
  } catch (e) {
    ElMessage.error(e?.response?.data?.detail || '保存失败')
  } finally {
    savingAchievements.value = false
  }
}

const restoreAll = async () => {
  try {
    await ElMessageBox.confirm('将把本空间所有行为/成就恢复为运营中心默认值，确定吗？', '恢复默认', { type: 'warning' })
    await motivationApi.saveIncentiveSettings({ actions: [], achievements: [], restore_all: true })
    ElMessage.success('已恢复为运营中心默认')
    fetchStarActions()
    fetchAchievements()
  } catch (e) {
    if (e !== 'cancel') ElMessage.error('恢复默认失败')
  }
}

// 奖励管理
const rewards = ref([])
const showRewardDialog = ref(false)
const editRewardData = ref(null)
const rewardForm = reactive({ name: '', description: '', cost_stars: 0, total_stock: -1, remaining_stock: -1, image_url: '' })

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
  loadKids()
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

.rule-tip {
  background: #f5f7fa;
  border-radius: 8px;
  padding: 12px 16px;
  color: #909399;
  font-size: 13px;
  line-height: 1.6;
}

/* 激励配置子导航：顶部横向 tabs */
.mgmt-tabs :deep(.el-tabs__item) {
  height: 44px;
  line-height: 44px;
  font-size: 14px;
}

/* 移动端适配：tab 多时横向滑动，避免展示不全 */
@media (max-width: 768px) {
  .mgmt-tabs :deep(.el-tabs__nav-wrap) {
    overflow-x: auto;
    overflow-y: hidden;
  }

  .mgmt-tabs :deep(.el-tabs__nav) {
    min-width: max-content;
  }

  .mgmt-tabs :deep(.el-tabs__item) {
    padding: 0 14px;
    font-size: 13px;
  }
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
