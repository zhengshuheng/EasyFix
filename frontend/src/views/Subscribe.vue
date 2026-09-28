<template>
  <div class="subscribe-page">
    <div class="subscribe-card">
      <div class="expired-badge">⏳</div>
      <h1>体验已到期</h1>
      <p class="sub">你的学习空间体验期已于 <b class="end-date">{{ expiresText }}</b> 结束</p>

      <div class="plan-box">
        <div class="plan-title">升级为正式版</div>
        <div class="plan-desc">不受体验期限制，全部功能继续使用</div>
        <div class="plan-price">¥{{ onlinePrice }}<span class="unit"> 一次性买断</span></div>
      </div>

      <el-button class="renew-btn" type="primary" size="large" @click="goRenew">
        前往官网续费
      </el-button>

      <p class="hint">续费成功后返回空间即可继续使用，无需重新配置</p>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useTrialStore } from '@/stores/trial'

const trialStore = useTrialStore()

const expiresText = computed(() => {
  const e = trialStore.expires_at
  return e ? String(e).slice(0, 16) : '—'
})

const onlinePrice = computed(() => trialStore.config.online_price || '50')

function goRenew() {
  // 官网登录后点「升级正式版」即可续费；升级成功后空间自动转正式（trial_end_at=NULL）
  window.location.href = '/site/'
}
</script>

<style scoped>
.subscribe-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
  box-sizing: border-box;
  background:
    radial-gradient(1200px 500px at 15% -10%, rgba(235, 183, 191, 0.22), transparent 60%),
    radial-gradient(1000px 460px at 90% 0%, rgba(245, 158, 184, 0.18), transparent 55%),
    linear-gradient(180deg, #fff7f7 0%, #fdeef2 100%);
}

.subscribe-card {
  width: 420px;
  max-width: 100%;
  background: #fff;
  border-radius: 20px;
  padding: 40px 34px 32px;
  box-shadow: 0 12px 40px rgba(120, 40, 60, 0.14);
  text-align: center;
}

.expired-badge {
  width: 60px;
  height: 60px;
  margin: 0 auto 14px;
  border-radius: 50%;
  font-size: 30px;
  line-height: 60px;
  background: linear-gradient(135deg, #f59e9e, #e8566d);
  box-shadow: 0 8px 20px rgba(232, 86, 109, 0.35);
}

.subscribe-card h1 {
  font-size: 22px;
  margin: 0 0 8px;
  color: #303133;
}

.subscribe-card .sub {
  color: #909399;
  font-size: 13px;
  margin: 0 0 22px;
}

.end-date {
  color: #e8566d;
}

.plan-box {
  background: linear-gradient(135deg, #fdf2f4, #fef7f8);
  border: 1px solid rgba(232, 86, 109, 0.25);
  border-radius: 14px;
  padding: 16px 20px;
  margin-bottom: 22px;
}

.plan-title {
  font-size: 16px;
  font-weight: 700;
  color: #c2404f;
}

.plan-desc {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.plan-price {
  font-size: 28px;
  font-weight: 800;
  color: #303133;
  margin-top: 10px;
}

.plan-price .unit {
  font-size: 12px;
  font-weight: 400;
  color: #909399;
}

.renew-btn {
  width: 100%;
  border-radius: 12px;
  font-weight: 600;
}

.hint {
  margin-top: 16px;
  font-size: 12px;
  color: #b0b6c4;
}
</style>
