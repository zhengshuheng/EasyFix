<template>
  <div class="assess-rules-page">
    <el-card shadow="never" class="header-card">
      <div class="header-row">
        <div>
          <h2>评测规则</h2>
          <p class="desc">AI 评测组卷/排重/坏题校验策略集中维护：改参数不用改代码，保存后下次评测立即生效；清空某项 = 恢复内置默认。</p>
        </div>
        <div class="actions">
          <el-button :disabled="loading" @click="load">刷新</el-button>
          <el-button :disabled="loading || !hasCustom" @click="restoreAll">恢复全部默认</el-button>
          <el-button type="primary" :loading="saving" @click="save">保存规则</el-button>
        </div>
      </div>
    </el-card>

    <el-card v-for="g in groups" :key="g.group" shadow="never" class="rule-card">
      <template #header><b>{{ g.group }}</b></template>
      <div v-for="item in g.items" :key="item.key" class="rule-row">
        <div class="rule-info">
          <div class="rule-title">
            {{ item.title }}
            <el-tag v-if="!item.is_default" type="warning" size="small">已自定义</el-tag>
            <el-tag v-else type="info" size="small">默认 {{ item.default }}</el-tag>
          </div>
          <div v-if="item.tip" class="tip">{{ item.tip }}</div>
        </div>
        <div class="rule-input">
          <el-input-number
            v-if="item.value_type === 'int'"
            v-model="item.value" :min="0" :max="99" :step="1" controls-position="right" />
          <el-input-number
            v-else
            v-model="item.value" :min="0" :max="1" :step="0.05" :precision="2" controls-position="right" />
        </div>
      </div>
    </el-card>
  </div>
</template>

<script>
import { opsAssessRules, opsSaveAssessRules } from '../api/ops.js'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  name: 'AssessRulesManage',
  data() {
    return {
      items: [],
      loading: false,
      saving: false,
    }
  },
  computed: {
    groups() {
      const order = ['组卷策略', '补题难度档', '变式难度', '坏题校验', '配图控制',
                     '卷型难度占比·标准', '卷型难度占比·挑战', '卷型难度占比·拓展']
      const map = {}
      for (const it of this.items) {
        if (!map[it.group]) map[it.group] = []
        map[it.group].push(it)
      }
      return order.filter(g => map[g]).map(g => ({ group: g, items: map[g] }))
    },
    hasCustom() {
      return this.items.some(i => !i.is_default)
    },
  },
  mounted() {
    this.load()
  },
  methods: {
    async load() {
      this.loading = true
      try {
        const res = await opsAssessRules()
        this.items = res.items || []
      } catch (e) {
        /* 拦截器已提示 */
      } finally {
        this.loading = false
      }
    },
    async save() {
      const rules = this.items.map(i => ({ key: i.key, value: i.value == null || i.value === '' ? '' : String(i.value) }))
      this.saving = true
      try {
        await opsSaveAssessRules(rules)
        ElMessage.success('已保存，下次评测生效')
        await this.load()
      } catch (e) {
        /* 拦截器已提示 */
      } finally {
        this.saving = false
      }
    },
    async restoreAll() {
      try {
        await ElMessageBox.confirm('将清空全部已保存评测规则（恢复内置默认），确定？', '恢复默认', { type: 'warning' })
      } catch (e) {
        return
      }
      this.saving = true
      try {
        await opsSaveAssessRules(this.items.map(i => ({ key: i.key, value: '' })))
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
.assess-rules-page {
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
.rule-card {
  margin-bottom: 14px;
}
.rule-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 16px;
  padding: 10px 4px;
  border-bottom: 1px solid #f3f4f6;
}
.rule-row:last-child {
  border-bottom: none;
}
.rule-info {
  flex: 1;
}
.rule-title {
  font-size: 14px;
  font-weight: 600;
  display: flex;
  align-items: center;
  gap: 8px;
}
.tip {
  margin-top: 4px;
  color: #9ca3af;
  font-size: 12px;
  line-height: 1.5;
}
.rule-input {
  flex-shrink: 0;
  width: 160px;
}
</style>
