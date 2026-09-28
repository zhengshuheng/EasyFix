<template>
  <!-- 出题弹窗：错题组卷 / AI 出题（自动生成PDF） -->
  <el-dialog v-model="generateDialogVisible" title="出题" width="480px">
    <el-tabs v-model="generateTab">
      <el-tab-pane label="错题组卷" name="pool">
        <el-form :model="generateForm" label-width="70px">
          <el-form-item label="学科" required>
            <el-select v-model="generateForm.subject_id" placeholder="选择学科" style="width: 100%" :disabled="!subjectStore.isAll">
              <el-option
                v-for="subject in subjects"
                :key="subject.id"
                :label="subject.name"
                :value="subject.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="年级">
            <el-select v-model="generateForm.grade" placeholder="全部" clearable style="width: 100%" :disabled="!subjectStore.isAllGrade">
              <el-option v-for="g in gradeOptions" :key="g.value" :label="g.label" :value="g.value" />
            </el-select>
          </el-form-item>
          <el-form-item label="数量">
            <el-input-number v-model="generateForm.count" :min="1" :max="99" />
          </el-form-item>
          <el-form-item label="卷面分数">
            <el-radio-group v-model="poolScoreSetting" style="display: flex; flex-direction: column; gap: 6px; align-items: flex-start">
              <el-radio value="hundred">百分制（满分 100 分）</el-radio>
              <el-radio value="default">按题型默认分值</el-radio>
              <el-radio value="none">不显示分数（纯练习卷）</el-radio>
            </el-radio-group>
          </el-form-item>
          <el-form-item>
            <span style="color: #909399; font-size: 12px">优先选择未复习、低正确率的题目，生成后自动打印 PDF</span>
          </el-form-item>
        </el-form>
      </el-tab-pane>
      <el-tab-pane label="AI 出题" name="ai">
        <el-form :model="aiGenerateForm" label-width="70px">
          <el-form-item label="学科" required>
            <el-select v-model="aiGenerateForm.subject_id" placeholder="选择学科" style="width: 100%" :disabled="!subjectStore.isAll" @change="loadAiKnowledgePoints">
              <el-option
                v-for="subject in subjects"
                :key="subject.id"
                :label="subject.name"
                :value="subject.id"
              />
            </el-select>
          </el-form-item>
          <el-form-item label="年级">
            <el-select v-model="aiGenerateForm.grade" placeholder="全部" clearable style="width: 100%" :disabled="!subjectStore.isAllGrade" @change="loadAiKnowledgePoints">
              <el-option v-for="g in gradeOptions" :key="g.value" :label="g.label" :value="g.value" />
            </el-select>
          </el-form-item>
          <el-form-item v-if="currentAiTextbook" label="教材版本">
            <div style="width: 100%; display: flex; align-items: center; gap: 8px; flex-wrap: wrap">
              <el-tag size="small" type="warning" effect="plain">{{ currentAiTextbook.version_name }}</el-tag>
              <span style="font-size: 12px; color: #909399">AI 出题按该版本筛选知识点（{{ kidStore.kidName }}）</span>
            </div>
          </el-form-item>
          <el-form-item label="知识点">
            <el-radio-group v-model="aiGenerateForm.knowledge_mode">
              <el-radio value="auto">自动（按错题薄弱点）</el-radio>
              <el-radio value="select">从知识点库选择</el-radio>
              <el-radio value="manual">手动输入</el-radio>
            </el-radio-group>
            <div v-if="aiGenerateForm.knowledge_mode === 'select'" style="width: 100%; margin-top: 8px">
              <el-button type="primary" plain style="width: 100%" @click="openKpPicker" :loading="aiKpLoading">
                <el-icon><Collection /></el-icon>
                &nbsp;选择知识点（{{ aiGenerateForm.selected_kp_ids.length }}）
              </el-button>
              <div v-if="aiSelectedKp.length" style="display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px">
                <el-tag
                  v-for="kp in aiSelectedKp"
                  :key="kp.id"
                  closable
                  size="small"
                  @close="toggleAiKp(kp.id)"
                >{{ kp.chapter ? kp.chapter + ' · ' : '' }}{{ kp.name }}</el-tag>
              </div>
              <div v-else-if="!aiKpLoading" style="color: #e6a23c; font-size: 12px; margin-top: 6px; line-height: 1.6">
                当前学科/年级暂无知识点{{ currentAiTextbook ? `（${currentAiTextbook.version_name}）` : '' }}：请在家长中心 → 题库管理 → 知识点管理用「按教材同步导入」，或切换到其他年级
              </div>
            </div>
            <div v-else-if="aiGenerateForm.knowledge_mode === 'auto'" style="color: #909399; font-size: 12px; margin-top: 8px; line-height: 1.6">
              自动统计当前学科错误最多的知识点出题（需有错题记录，否则请选择/输入知识点）
            </div>
            <el-input
              v-if="aiGenerateForm.knowledge_mode === 'manual'"
              v-model="aiGenerateForm.knowledge_text"
              placeholder="多个知识点用逗号分隔，如：分数加减法,乘法分配律"
              style="margin-top: 8px"
            />
          </el-form-item>
          <el-form-item label="数量">
            <el-select v-model="aiGenerateForm.count" style="width: 100%">
              <el-option v-for="n in [3, 5, 10, 15, 20]" :key="n" :label="`${n} 题`" :value="n" />
            </el-select>
          </el-form-item>
          <el-form-item label="难度">
            <el-select v-model="aiGenerateForm.difficulty" placeholder="中等（默认）" clearable style="width: 100%">
              <el-option label="简单" :value="1" />
              <el-option label="基础" :value="2" />
              <el-option label="中等" :value="3" />
              <el-option label="偏难" :value="4" />
              <el-option label="困难" :value="5" />
            </el-select>
          </el-form-item>
          <el-form-item label="试卷结构">
            <div style="width: 100%">
              <el-select v-model="aiPaperStructure" placeholder="不选 = 默认均衡结构" clearable style="width: 100%" @change="applyPaperStructure">
                <el-option v-for="(s, key) in paperStructuresForSubject" :key="key" :label="s.label" :value="key">
                  <span style="font-weight: 600">{{ s.label }}</span>
                  <span style="color: #909399; font-size: 12px; margin-left: 8px">{{ s.desc }}</span>
                </el-option>
              </el-select>
              <div v-if="currentPaperStructure" style="margin-top: 6px; font-size: 12px; color: #909399; line-height: 1.6">
                已套用「{{ currentPaperStructure.label }}」：题型 {{ currentPaperStructure.types.map(t => QUESTION_TYPE_NAMES[t]).join('、') }} · 难度 {{ ['简单','基础','中等','偏难','困难'][currentPaperStructure.difficulty - 1] }}；可在下方高级设置微调
              </div>
            </div>
          </el-form-item>
          <!-- 高级设置：卷面分数/出题人署名/题型/类型（默认收起，减少弹窗高度） -->
          <el-form-item>
            <div style="width: 100%">
              <div class="ai-advanced-header" @click="aiAdvancedOpen = !aiAdvancedOpen">
                <el-icon :style="{ transition: 'transform .2s' }">
                  <ArrowDown v-if="aiAdvancedOpen" />
                  <ArrowRight v-else />
                </el-icon>
                <span style="font-weight: 600">高级设置</span>
                <span style="color: #909399; font-size: 12px">卷面分数 · 出题人署名 · 题型 · 类型</span>
              </div>
              <template v-if="aiAdvancedOpen">
                <div class="ai-adv-row">
                  <span class="ai-adv-label">卷面分数</span>
                  <div style="flex: 1; min-width: 0">
                    <el-radio-group v-model="aiScoreSetting" style="display: flex; flex-wrap: wrap; gap: 4px 12px">
                      <el-radio value="hundred">百分制100分</el-radio>
                      <el-radio value="default">题型默认分值</el-radio>
                      <el-radio value="none">不显示分数</el-radio>
                    </el-radio-group>
                  </div>
                </div>
                <div class="ai-adv-row">
                  <span class="ai-adv-label">出题人署名</span>
                  <div style="flex: 1; min-width: 0; display: flex; align-items: center; gap: 8px; flex-wrap: wrap">
                    <el-switch v-model="aiShowAiAuthor" />
                    <span style="font-size: 12px; color: #909399">显示「AI 出题助手」（默认留空白让孩子自己写）</span>
                  </div>
                </div>
                <div class="ai-adv-row">
                  <span class="ai-adv-label">题型</span>
                  <div style="flex: 1; min-width: 0">
                    <el-checkbox-group v-model="aiGenerateForm.question_types" style="display: flex; flex-wrap: wrap; gap: 4px 12px">
                      <el-checkbox
                        v-for="t in filteredQuestionTypes"
                        :key="t.value"
                        :value="t.value"
                        style="margin-right: 0"
                      >{{ t.label }}</el-checkbox>
                    </el-checkbox-group>
                    <div style="display: flex; justify-content: space-between; margin-top: 4px">
                      <span style="color: #c0c4cc; font-size: 12px">不选 = 混合出题</span>
                      <el-link
                        v-if="aiGenerateForm.question_types.length"
                        type="primary"
                        :underline="false"
                        style="font-size: 12px"
                        @click="aiGenerateForm.question_types = []"
                      >清空</el-link>
                    </div>
                  </div>
                </div>
                <div class="ai-adv-row">
                  <span class="ai-adv-label">类型</span>
                  <div style="flex: 1; min-width: 0">
                    <el-checkbox-group v-model="aiGenerateForm.question_categories" style="display: flex; flex-wrap: wrap; gap: 4px 12px">
                      <el-checkbox
                        v-for="c in questionCategoriesForSubject"
                        :key="c.value"
                        :value="c.value"
                        style="margin-right: 0"
                      >
                        <span style="font-weight: 600">{{ c.label }}</span>
                        <span style="color: #909399; font-size: 12px; margin-left: 4px">{{ c.desc }}</span>
                      </el-checkbox>
                    </el-checkbox-group>
                    <div style="display: flex; justify-content: space-between; margin-top: 4px">
                      <span style="color: #c0c4cc; font-size: 12px">不选 = 按课标梯度（基础→情境→综合→拓展）编排</span>
                      <el-link
                        v-if="aiGenerateForm.question_categories.length"
                        type="primary"
                        :underline="false"
                        style="font-size: 12px"
                        @click="aiGenerateForm.question_categories = []"
                      >清空</el-link>
                    </div>
                  </div>
                </div>
              </template>
            </div>
          </el-form-item>
        </el-form>
      </el-tab-pane>
    </el-tabs>
    <template #footer>
      <el-button @click="generateDialogVisible = false">取消</el-button>
      <el-button
        type="primary"
        :loading="generating"
        @click="generateTab === 'ai' ? generateAiPractice() : generatePractice()"
      >
        {{ generateTab === 'ai' ? 'AI 生成' : '生成并打印' }}
      </el-button>
    </template>
  </el-dialog>

  <!-- 知识点选择弹窗（按单元分组标签点选） -->
  <el-dialog v-model="kpPickerVisible" title="选择知识点" width="640px" append-to-body>
    <div style="display: flex; gap: 10px; margin-bottom: 12px; align-items: center">
      <el-input v-model="kpSearch" placeholder="搜索知识点名称" clearable style="flex: 1">
        <template #prefix><el-icon><Search /></el-icon></template>
      </el-input>
      <el-button v-if="aiGenerateForm.selected_kp_ids.length" size="default" @click="clearAiKpSelection">清空已选</el-button>
      <span v-if="aiGenerateForm.selected_kp_ids.length" style="color: #409eff; font-size: 13px; white-space: nowrap">已选 {{ aiGenerateForm.selected_kp_ids.length }} 个</span>
    </div>
    <div v-if="aiKpLoading" style="text-align: center; padding: 30px; color: #909399">知识点加载中…</div>
    <div v-else style="max-height: 400px; overflow-y: auto">
      <div v-for="g in filteredAiKpGroups" :key="g.key" style="margin-bottom: 10px">
        <div
          style="display: flex; align-items: center; gap: 8px; padding: 6px 10px; background: #f5f7fa; border-radius: 6px; cursor: pointer; user-select: none"
          @click="toggleGroup(g)"
        >
          <el-checkbox :model-value="isGroupAllChecked(g)" @click.stop @change="toggleGroup(g)" />
          <span style="font-weight: 600; font-size: 13px">{{ g.label }}</span>
          <span style="color: #909399; font-size: 12px">{{ g.items.length }} 个</span>
          <span v-if="isGroupAllChecked(g)" style="color: #409eff; font-size: 12px; margin-left: auto">已全选</span>
          <span v-else style="color: #c0c4cc; font-size: 12px; margin-left: auto">全选本单元</span>
        </div>
        <div style="display: flex; flex-wrap: wrap; gap: 6px; padding: 8px 6px 0 6px">
          <el-check-tag
            v-for="kp in g.items"
            :key="kp.id"
            :checked="aiGenerateForm.selected_kp_ids.includes(kp.id)"
            @change="toggleAiKp(kp.id)"
          >{{ kp.name }}</el-check-tag>
        </div>
      </div>
      <div v-if="!filteredAiKpGroups.length" style="text-align: center; padding: 30px; color: #909399">
        没有匹配的知识点，可在家长中心导入教材或切换学科/年级
      </div>
    </div>
    <template #footer>
      <el-button @click="kpPickerVisible = false">取消</el-button>
      <el-button type="primary" @click="kpPickerVisible = false">确定（已选 {{ aiGenerateForm.selected_kp_ids.length }}）</el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, computed } from 'vue'
import { ElMessage } from 'element-plus'
import { Collection, Search, ArrowDown, ArrowRight } from '@element-plus/icons-vue'
import { questionApi } from '@/api/question'
import { useSubjectStore } from '@/stores/subject'
import { useKidStore } from '@/stores/kid'

const props = defineProps({
  subjects: { type: Array, default: () => [] },
})
const emit = defineEmits(['created'])

const subjectStore = useSubjectStore()
const kidStore = useKidStore()

const generateDialogVisible = ref(false)
const generating = ref(false)
const generateTab = ref('pool') // pool=错题组卷 ai=AI出题
const generateForm = reactive({
  subject_id: null,
  grade: null,
  count: 5,
})
// 错题组卷卷面分数：hundred=百分制 / default=题型默认分值 / none=不显示
const poolScoreSetting = ref('hundred')
const aiGenerateForm = reactive({
  subject_id: null,
  grade: null,
  knowledge_mode: 'auto', // auto=按错题薄弱点 select