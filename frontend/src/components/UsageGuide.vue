<template>
  <el-dialog v-model="visible" title="📖 使用指南" width="640px" :close-on-click-modal="true">
    <div class="ug-body">
      <div class="ug-item">
        <div class="ug-icon">📱</div>
        <div class="ug-text">
          <b>注册与登录</b>
          <span>用 <b>手机号</b> 注册，一个号码一个学习空间；登录用「手机号 + 密码」，家长也可在空间里添加辅账号（另一套手机号/用户名 + 密码）。</span>
        </div>
      </div>
      <div class="ug-item">
        <div class="ug-icon">👦</div>
        <div class="ug-text">
          <b>选择孩子</b>
          <span>进空间先选今天谁学习；每个孩子数据完全独立（错题、练习、单词、报告互不干扰）。可添加多个孩子。</span>
        </div>
      </div>
      <div class="ug-item">
        <div class="ug-icon">📷</div>
        <div class="ug-text">
          <b>拍照收录错题</b>
          <span>在「数学 / 英语」页把做错的题目拍照上传，系统自动切题、识别知识点并归类，错题本自动整理。</span>
        </div>
      </div>
      <div class="ug-item">
        <div class="ug-icon">✏️</div>
        <div class="ug-text">
          <b>做练习巩固</b>
          <span>按知识点/单元做专项练习，AI 按孩子教材版本出题，错题自动进入错题本并推荐同类巩固。</span>
        </div>
      </div>
      <div class="ug-item">
        <div class="ug-icon">🔤</div>
        <div class="ug-text">
          <b>背单词</b>
          <span>英语单词按教材单元学习，中英互测、听写、默写打印，闯关式坚持每天进步。</span>
        </div>
      </div>
      <div class="ug-item">
        <div class="ug-icon">🛠️</div>
        <div class="ug-text">
          <b>家长中心</b>
          <span>点「家长设置」进入：添加/管理孩子、一键同步教材知识点与单词、查看学习报告与激励中心，所有家长操作都在这里。</span>
        </div>
      </div>
      <div class="ug-item">
        <div class="ug-icon">💳</div>
        <div class="ug-text">
          <b>续费与支持</b>
          <span>空间到期会在选择页提示并引导续费；忘记密码请联系管理员重置，账号安全由系统保障。</span>
        </div>
      </div>
    </div>
  </el-dialog>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  modelValue: { type: Boolean, default: false },
})
const emit = defineEmits(['update:modelValue'])
const visible = computed({
  get: () => props.modelValue,
  set: (v) => emit('update:modelValue', v),
})
</script>

<style scoped>
.ug-body {
  display: flex;
  flex-direction: column;
  gap: 14px;
  max-height: 60vh;
  overflow: auto;
}
.ug-item {
  display: flex;
  gap: 12px;
  align-items: flex-start;
  padding: 12px 14px;
  border-radius: 10px;
  background: #f7f9fd;
  border: 1px solid #eef2fb;
}
.ug-icon {
  font-size: 22px;
  line-height: 1.4;
}
.ug-text {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: 13px;
  color: #4b5563;
  line-height: 1.7;
}
.ug-text b {
  color: #303133;
  font-size: 14px;
}
</style>
