import { createRouter, createWebHashHistory } from 'vue-router'
import OpsLayout from './layout/OpsLayout.vue'
import KpManage from './views/KpManage.vue'
import WordManage from './views/WordManage.vue'
import EditionsManage from './views/EditionsManage.vue'
import SystemSettings from './views/SystemSettings.vue'
import AiMarket from './views/AiMarket.vue'
import TrialAccounts from './views/TrialAccounts.vue'
import PromptRulesManage from './views/PromptRulesManage.vue'
import AssessRulesManage from './views/AssessRulesManage.vue'
import IncentiveRulesManage from './views/IncentiveRulesManage.vue'
import GrammarTutorialsManage from './views/GrammarTutorialsManage.vue'

export default createRouter({
  history: createWebHashHistory('/ops/'),
  routes: [
    {
      path: '/',
      component: OpsLayout,
      children: [
        { path: '', redirect: '/kp' },
        { path: 'kp', component: KpManage, meta: { title: '知识点管理' } },
        { path: 'word', component: WordManage, meta: { title: '英语单词管理' } },
        { path: 'editions', component: EditionsManage, meta: { title: '教材版本' } },
        { path: 'config', component: SystemSettings, meta: { title: '系统设置' } },
        { path: 'ai-market', component: AiMarket, meta: { title: 'AI 模型市场' } },
        { path: 'prompt-rules', component: PromptRulesManage, meta: { title: '出题规则' } },
        { path: 'assess-rules', component: AssessRulesManage, meta: { title: '评测规则' } },
        { path: 'incentive-rules', component: IncentiveRulesManage, meta: { title: '激励规则' } },
        { path: 'grammar-tutorials', component: GrammarTutorialsManage, meta: { title: '语法教程' } },
        { path: 'trial-accounts', component: TrialAccounts, meta: { title: '体验账号管理' } },
      ],
    },
  ],
})
