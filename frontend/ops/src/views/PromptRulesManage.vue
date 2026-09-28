<template>
  <div class="prompt-rules-page">
    <el-card shadow="never" class="header-card">
      <div class="header-row">
        <div>
          <h2>出题规则（Prompt）</h2>
          <p class="desc">AI 评测出题规则集中维护：改规则不用改代码，保存后下次评测立即生效；清空某条规则 = 恢复内置默认。</p>
        </div>
        <div class="actions">
          <el-button :disabled="loading" @click="load">刷新</el-button>
          <el-button :disabled="loading || !hasCustom" @click="restoreAll">恢复全部默认</el-button>
          <el-button type="primary" :loading="saving" @click="save">保存规则</el-button>
        </div>
      </div>
    </el-card>

    <el-card shadow="never" class="rule-card">
      <el-tabs v-model="activeTab" class="rule-tabs">
        <el-tab-pane label="🧾 通用" name="通用">
          <div v-for="item in generalItems" :key="item.scope" class="scope-block">
            <div class="scope-head">
              <b>{{ item.title }}</b>
              <el-tag v-if="!item.is_default" type="warning" size="small">已自定义</el-tag>
              <el-tag v-else type="info" size="small">内置默认</el-tag>
            </div>
            <el-input type="textarea" :rows="10" v-model="item.rule_text" :placeholder="item.title" />
            <div class="tip">{{ item.tip }}</div>
          </div>
        </el-tab-pane>
        <el-tab-pane v-for="g in subjectGroups" :key="g.group" :label="g.group" :name="g.group">
          <div v-for="item in g.items" :key="item.scope" class="scope-block">
            <div class="scope-head">
              <b>{{ item.title }}</b>
              <el-tag v-if="!item.is_default" type="warning" size="small">已自定义</el-tag>
              <el-tag v-else type="info" size="small">内置默认</el-tag>
            </div>
            <el-input type="textarea" :rows="6" v-model="item.rule_text" :placeholder="item.title" />
            <div class="tip">{{ item.tip }}</div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-card>
  </div>
</template>

<script>
import { opsPromptRules, opsSavePromptRules } from '../api/ops.js'
import { ElMessage, ElMessageBox } from 'element-plus'

export default {
  name: 'PromptRulesManage',
  data() {
    return {
      items: [],
      loading: false,
      saving: false,
      activeTab: '通用',
    }
  },
  computed: {
    // 通用 tab：通用出题规则 + 默认科目基础段
    generalItems() {
      return this.items.filter(i => i.group === '通用')
    },
    // 学科 tab：数学 / 语文 / 英语（科目基础段 + 各学段真题段）
    subjectGroups() {
      const map = {}
      for (const it of this.items) {
        if (it.group === '通用') continue
        if (!map[it.group]) map[it.group] = []
        map[it.group].push(it)
      }
      return ['数学', '语文', '英语'].filter(g => map[g]).map(g => ({ group: g, items: map[g] }))
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
        const res = await opsPromptRules()
        this.items = res.items || []
      } catch (e) {
        /* 拦截器已提示 */
      } finally {
        this.loading = false
      }
    },
    async save() {
      const rules = this.items.map(i => ({ scope: i.scope, rule_text: (i.rule_text || '').trim() }))
      this.saving = true
      try {
        await opsSavePromptRules(rules)
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
        await ElMessageBox.confirm('将清空全部已保存规则（恢复内置默认），确定？', '恢复默认', { type: 'warning' })
      } catch (e) {
        return
      }
      this.saving = true
      try {
        await opsSavePromptRules(this.items.map(i => ({ scope: i.scope, rule_text: '' })))
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
.prompt-rules-page {
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
.rule-head {
  display: flex;
  align-items: center;
  gap: 10px;
}
.scope-block {
  margin-bottom: 12px;
  padding: 10px 12px;
  border: 1px solid #e5e7eb;
  border-radius: 8px;
  background: #fafafa;
}
.scope-head {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}
.tip {
  margin-top: 6px;
  color: #9ca3af;
  font-size: 12px;
  line-height: 1.5;
}
</style>
