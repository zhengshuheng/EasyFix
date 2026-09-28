import { ref } from 'vue'
import { useAuthStore } from '@/stores/auth'

const TOKEN_KEY = 'easyfix_token'
const USER_KEY = 'easyfix_user'

/**
 * 家长认证守卫：学生端删除等敏感操作需要家长验证。
 *
 * 用法：
 *   const { visible, guard, onVerified, onCancel } = useParentGuard()
 *   await guard(() => questionApi.delete(row.id))   // 家长直通；学生弹窗验证后执行
 *
 * 模板里挂一个 ParentLockDialog：
 *   <ParentLockDialog v-model="visible" title="家长验证" tip="删除操作需要家长验证" confirm-text="验证并删除" @success="onVerified" @update:model-value="!$event && onCancel()" />
 *
 * 行为：
 * - 家长（admin）会话：直接执行 action
 * - 学生（child）会话：弹出家长密码框 → 验证通过（临时切换为家长 token）→ 执行 action → 恢复孩子会话
 */
export function useParentGuard() {
  const authStore = useAuthStore()
  const visible = ref(false)

  let pendingAction = null
  let resolveFn = null
  let rejectFn = null
  let savedSession = null

  /** 执行受家长保护的动作；返回 Promise（家长直通 / 学生验证通过后执行） */
  function guard(action) {
    // 家长会话直接放行
    if (authStore.isAdmin) {
      return action()
    }
    // 学生会话：保存当前会话，弹家长验证（验证会临时切换成家长 token）
    savedSession = { token: authStore.token, user: authStore.user }
    visible.value = true
    return new Promise((resolve, reject) => {
      pendingAction = action
      resolveFn = resolve
      rejectFn = reject
    })
  }

  /** 家长验证成功回调：执行待办动作并恢复孩子会话 */
  async function onVerified() {
    const action = pendingAction
    const resolve = resolveFn
    const reject = rejectFn
    pendingAction = null
    resolveFn = null
    rejectFn = null
    try {
      const result = await action()
      resolve(result)
    } catch (e) {
      reject(e)
    } finally {
      visible.value = false
      restoreSession()
    }
  }

  /** 弹窗取消：清空待办（此时会话尚未被切换，无需恢复） */
  function onCancel() {
    pendingAction = null
    resolveFn = null
    rejectFn = null
    visible.value = false
  }

  function restoreSession() {
    if (!savedSession) return
    authStore.token = savedSession.token
    authStore.user = savedSession.user
    localStorage.setItem(TOKEN_KEY, savedSession.token)
    localStorage.setItem(USER_KEY, JSON.stringify(savedSession.user))
    savedSession = null
  }

  return { visible, guard, onVerified, onCancel }
}
