<template>
  <div class="incentive-rules-page">
    <el-card shadow="never" class="header-card">
      <div class="header-row">
        <div>
          <h2>激励规则</h2>
          <p class="desc">这里配置的是<b>全部空间的默认值</b>：孩子做哪些事加多少分、成就在什么条件解锁，改完保存后成为所有空间的新默认。每个家长可在自己空间的「行为规则 / 成就规则」中调整积分值、触发次数、奖励积分（仅对该空间生效）；未自定义的规则自动跟随这里的默认值。</p>
        </div>
        <div class="actions">
          <el-button :disabled="loading" @click="load">刷新</el-button>
          <el-button :disabled="loading || !hasCustom" @click="restoreAll">恢复全部默认</el-button>
          <el-button type="primary" :loading="saving" @click="save">保存规则</el-button>
        </div>
      </div>
    </el-card>

    <el-card shadow="never">
      <el-tabs v-model="activeTab">
        <el-tab-pane label="行为规则" name="actions">
          <div class="hint">
            孩子完成某个学习动作时自动加/减积分。预设触发点由程序内置，这里只调积分值与启停。
            「行为代码」是程序内部标识，不在运营界面展示。
          </div>
          <el-table :data="actions" stripe style="width: 100%; margin-top: 12px">
            <el-table-column prop="name" label="行为名称" min-width="140" />
            <el-table-column label="积分值" width="200">
              <template #default="{ row }">
                <el-input-number v-model="row.star_value" :min="-999" :max="999" :step="1" controls-position="right" />
              </template>
            </el-table-column>
            <el-table-column label="启用" width="120">
              <template #default="{ row }">
                <el-switch v-model="row.enabled" />
              </template>
            </el-table-column>
            <el-table-column label="状态" width="120">
              <template #default="{ row }">
                <el-tag v-if="!row.is_default" type="warning" size="small">已自定义</el-tag>
                <el-tag v-else type="info" size="small">默认</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>

        <el-tab-pane label="成就规则" name="achievements">
          <div class="hint">
            成就按「触发行为 + 触发次数」自动解锁并发放奖励积分，分等级递进（需先解锁上一级）。
          </div>
          <el-table :data="achievements" stripe style="width: 100%; margin-top: 12px">
            <el-table-column prop="name" label="成就名称" min-width="110" />
            <el-table-column label="等级" width="70">
              <template #default="{ row }">Lv{{ row.level }}</template>
            </el-table-column>
            <el-table-column label="触发行为" min-width="120">
              <template #default="{ row }">{{ actionName(row.trigger_action) }}</template>
            </el-table-column>
            <el-table-column label="触发次数" width="150">
              <template #default="{ row }">
                <el-input-number v-model="row.trigger_count" :min="1" :max="9999" :step="1" controls-position="right" />
              </template>
            </el-table-column>
            <el-table-column label="奖励积分" width="150">
              <template #default="{ row }">
                <el-input-number v-model="row.reward_stars" :min="0" :max="9999" :step="1" controls-position="right" />
              </template>
            </el-table-column>
            <el-table-column label="启用" width="100">
              <template #default="{ row }">
                <el-switch v-model="row.is_active" />
              </template>
            </el-table-column>
            <el-table-column label="状态" width="110">
              <template #default="{ row }">
                <el-tag v-if="!row.is_default" type="warning" size="small">已自定义</el-tag>
                <el-tag v-else type="info" size="small">默认</el-tag>
              </template>
            </el-table-column>
          </el-table>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script>
import { opsIncentiveRules, opsSaveIncentiveRules } from '../api/ops.js'
import { ElMessage, ElMessageBox } from 'element-plus'

const ACTION_NAMES = {
  'upload_question': '上传错题',
  'review_practice_set': '复习练习集',
  'generate_similar': '生成相似题',
  'review_word': '背单词',
  'create_practice_set': '创建练习集',
  'daily_login': '每日登录',
  'continuous_7day': '连续学习7天',
  'continuous_14day': '连续学习14天',
  'continuous_30day': '连续学习30天',
  'review_word_accuracy': '单词正确率达标',
}

export default {
  name: 'IncentiveRulesManage',
  data() {
    return {
      activeTab: 'actions',
      actions: [],
      achievements: [],
      loading: false,
      saving: false,
    }
  },
  computed: {
    hasCustom() {
      return this.actions.some(i => !i.is_default) || this.achievements.some(i => !i.is_default)
    },
  },
  mounted() {
    this.load()
  },
  methods: {
    actionName(code) {
      return ACTION_NAMES[code] || code
    },
    async load() {
      this.loading = true
      try {
        const res = await opsIncentiveRules()
        this.actions = res.actions || []
        this.achievements = res.achievements || []
      } catch (e) {
        /* 拦截器已提示 */
      } finally {
        this.loading = false
      }
    },
    async save() {
      this.saving = true
      try {
        await opsSaveIncentiveRules({
          actions: this.actions.map(i => ({ code: i.code, star_value: i.star_value, enabled: i.enabled })),
          achievements: this.achievements.map(i => ({
            code: i.code, level: i.level, trigger_count: i.trigger_count,
            reward_stars: i.reward_stars, is_active: i.is_active,
          })),
        })
        ElMessage.success('已保存为全部空间的默认值（未自定义的空间自动跟随）')
        await this.load()
      } catch (e) {
        /* 拦截器已提示 */
      } finally {
        this.saving = false
      }
    },
    async restoreAll() {
      try {
        await ElMessageBox.confirm('将清空全部已保存激励规则（恢复内置默认），确定？', '恢复默认', { type: 'warning' })
      } catch (e) {
        return
      }
      this.saving = true
      try {
        await opsSaveIncentiveRules({ restore_all: true })
        ElMessage.success('已恢复内置默认')
        await this.load()
      } catch (e) {
        /* 拦截器已提示 */
      } finally {
        this.saving = false
      }
    },
  },
}
</script>

<style scoped>
.incentive-rules-page {
  padding: 4px;
}
.header-card {
  margin-bottom: 14px;
}
.header-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: 16px;
}
.header-row h2 {
  margin: 0 0 6px;
  font-size: 18px;
}
.desc {
  margin: 0;
  color: #6b7280;
  font-size: 13px;
}
.actions {
  flex-shrink: 0;
}
.hint {
  color: #9ca3af;
  font-size: 13px;
  line-height: 1.6;
}
</style>
