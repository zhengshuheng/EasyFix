/**
 * 统一读音模块：浏览器 SpeechSynthesis + 服务器 edge-tts 降级（全站唯一实现点）
 *
 * 为什么需要：
 *   Chrome（非 Edge）在国内拿不到可用的 Google 在线语音 —— 即使 getVoices() 里能看到
 *   en-US，speak() 也发不出声；Edge 用 Windows 本地语音正常。所以只要出现
 *   「Chrome / 语音列表未加载 / 没有对应语种语音 / 朗读报错」，一律降级走服务器 TTS
 *   （GET /api/words/audio?english=...&lang=...，edge-tts，稳定），孩子永远能听到音。
 *
 * 统一用法：
 *   import { speakEn, speakZh, speak, speakSequence, playServerTts, stopSpeech, installSpeechUnlock } from '@/utils/speech'
 *   await speakEn('She is a student.')            // 英文朗读（自动降级）
 *   await speakZh('她是一名学生。')                // 中文朗读（自动降级）
 *   await speak('…', { lang: 'zh-CN', rate: 0.9 })
 *   await speakSequence([{ text: 'I am…', lang: 'en-US' }, { text: '，我是…', lang: 'zh-CN' }])
 *   await playServerTts('apple')                  // 只要服务器音频（拼读示例词/组合）
 *   installSpeechUnlock()                         // 自动带读页面：首次手势解锁 AudioContext
 *   stopSpeech()                                  // 停止当前朗读
 *
 * 返回值：Promise<boolean> —— true 表示确实播出了（浏览器语音或服务器音频）。
 */

let audioCtx = null // 复用同一个 AudioContext（Chrome 自动播放策略要求手势内解锁）
let currentSource = null // 正在播放的 Web Audio 源（stopSpeech 用）
let currentAudioEl = null // 退化为 Audio 元素时的当前实例
let unlockInstalled = false

/** Chrome（非 Edge/Opera）：Google 在线语音在国内不可用，强制走服务器 TTS */
export function isChromeNoEdge() {
  try {
    return /Chrome\//.test(navigator.userAgent) && !/Edg\//.test(navigator.userAgent) && !/OPR\//.test(navigator.userAgent)
  } catch (e) {
    return false
  }
}

/** 浏览器是否有可用语音；返回 false 时朗读降级走服务器 TTS */
export function hasVoiceFor(langPrefix) {
  if (typeof window === 'undefined' || !('speechSynthesis' in window) || isChromeNoEdge()) return false
  try {
    const voices = window.speechSynthesis.getVoices()
    if (!voices.length) return false // 语音列表还没加载（首次为空），走服务器 TTS 兜底
    return voices.some(v => v.lang && v.lang.toLowerCase().startsWith(langPrefix))
  } catch (e) {
    return false
  }
}

/** 复用/创建 AudioContext（suspended 时尝试 resume；非手势内调用可能仍保持 suspended） */
export function ensureAudioCtx() {
  const AC = window.AudioContext || window.webkitAudioContext
  if (!AC) return null
  if (!audioCtx || audioCtx.state === 'closed') {
    try { audioCtx = new AC() } catch (e) { return null }
  }
  if (audioCtx.state === 'suspended') audioCtx.resume().catch(() => {})
  return audioCtx
}

export function unlockAudioOnGesture() {
  ensureAudioCtx()
}

/**
 * 首次用户手势解锁 AudioContext（并在之后每次手势保持解锁）。
 * 自动带读场景必须调用：Chrome Autoplay Policy 只给「用户激活后约 5 秒」的窗口，
 * 几秒后自动播放的句子会被拦掉；提前 unlock 后任意时刻都能播。
 */
export function installSpeechUnlock() {
  if (unlockInstalled || typeof window === 'undefined') return
  unlockInstalled = true
  const unlock = () => unlockAudioOnGesture()
  window.addEventListener('pointerdown', unlock, { passive: true })
  window.addEventListener('keydown', unlock, { passive: true })
}

/** 停止当前朗读（浏览器语音 + 服务器音频） */
export function stopSpeech() {
  if (typeof window !== 'undefined' && 'speechSynthesis' in window) {
    try { window.speechSynthesis.cancel() } catch (e) { /* 忽略 */ }
  }
  if (currentSource) {
    try { currentSource.stop() } catch (e) { /* 已结束 */ }
    currentSource = null
  }
  if (currentAudioEl) {
    try { currentAudioEl.pause() } catch (e) { /* 忽略 */ }
    currentAudioEl = null
  }
}

/** Audio 元素兜底播放（AudioContext 不可用/未解锁时） */
function playWithAudioElement(url) {
  return new Promise((resolve) => {
    let audio
    try { audio = new Audio(url) } catch (e) { return resolve(false) }
    let done = false
    const finish = (ok) => {
      if (done) return
      done = true
      if (currentAudioEl === audio) currentAudioEl = null
      resolve(ok)
    }
    audio.onended = () => finish(true)
    audio.onerror = () => finish(false)
    currentAudioEl = audio
    const p = audio.play()
    if (p && p.catch) p.catch(() => finish(false))
  })
}

/**
 * 播放服务器音频 URL（优先 Web Audio：绕开 Chrome 5 秒自动播放窗口；失败退 Audio 元素）。
 * 返回 Promise<boolean>，true = 播放完成。
 */
export function playServerAudio(url) {
  const ctx = ensureAudioCtx()
  if (!ctx || ctx.state !== 'running') return playWithAudioElement(url)
  return fetch(url)
    .then(resp => (resp.ok ? resp.arrayBuffer() : Promise.reject(new Error('HTTP ' + resp.status))))
    .then(arr => ctx.decodeAudioData(arr))
    .then(buf => new Promise((resolve) => {
      const src = ctx.createBufferSource()
      let done = false
      const finish = (ok) => {
        if (done) return
        done = true
        if (currentSource === src) currentSource = null
        resolve(ok)
      }
      src.buffer = buf
      src.connect(ctx.destination)
      currentSource = src
      src.onended = () => finish(true)
      // 兜底：极端情况（切页/被 cancel）onended 不回调时按音频时长收尾，避免调用方 await 卡死
      setTimeout(() => finish(true), ((buf.duration || 3) * 1000) + 2000)
      src.start(0)
    }))
    .catch(() => playWithAudioElement(url))
}

/** 服务器 TTS 朗读文本（句子/中文/单词都可；edge-tts） */
export function playServerTts(text, lang = 'en-US') {
  const t = String(text == null ? '' : text).trim()
  if (!t) return Promise.resolve(false)
  return playServerAudio(`/api/words/audio?english=${encodeURIComponent(t)}&lang=${encodeURIComponent(lang)}`)
}

/** 浏览器 SpeechSynthesis 朗读；resolve(false) 表示没读成（调用方降级服务器 TTS） */
function speakWithBrowser(text, lang, rate) {
  return new Promise((resolve) => {
    let u
    try { u = new SpeechSynthesisUtterance(text) } catch (e) { return resolve(false) }
    u.lang = lang
    if (rate) u.rate = rate
    try {
      const voices = window.speechSynthesis.getVoices()
      const prefix = String(lang).toLowerCase().slice(0, 2)
      const v = voices.find(x => x.lang && x.lang.toLowerCase().startsWith(prefix))
      if (v) u.voice = v
    } catch (e) { /* 忽略：用浏览器默认 */ }
    let done = false
    const finish = (ok) => {
      if (done) return
      done = true
      clearTimeout(timer)
      resolve(ok)
    }
    // 兜底：被 cancel 或浏览器不回调时按预估时长收尾，避免调用方 await 卡死
    const timer = setTimeout(() => finish(true), Math.max(4000, text.length * 220))
    u.onend = () => finish(true)
    u.onerror = () => finish(false)
    try { window.speechSynthesis.speak(u) } catch (e) { finish(false) }
  })
}

/**
 * 朗读文本：浏览器语音可用就用它，否则/失败则降级服务器 TTS。
 * opts.lang 语言（默认 zh-CN）、opts.rate 语速、opts.forceServer 强制走服务器。
 */
export async function speak(text, opts = {}) {
  const t = String(text == null ? '' : text).trim()
  if (!t) return false
  const lang = opts.lang || 'zh-CN'
  const prefix = lang.toLowerCase().slice(0, 2)
  stopSpeech()
  if (!opts.forceServer && hasVoiceFor(prefix)) {
    if (await speakWithBrowser(t, lang, opts.rate)) return true
  }
  return playServerTts(t, lang)
}

/** 英文朗读（含降级），默认语速 0.85 */
export function speakEn(text, opts = {}) {
  return speak(text, { lang: 'en-US', rate: 0.85, ...opts })
}

/** 中文朗读（含降级），默认语速 0.9 */
export function speakZh(text, opts = {}) {
  return speak(text, { lang: 'zh-CN', rate: 0.9, ...opts })
}

/**
 * 依次朗读多条（如「英文例句 → 中文翻译」）。
 * items: [{ text, lang?, rate? }]，空项自动跳过；返回 Promise<boolean>（是否至少播出一条）。
 */
export async function speakSequence(items, opts = {}) {
  let played = false
  for (const item of items || []) {
    if (!item) continue
    const text = typeof item === 'string' ? item : item.text
    if (!text) continue
    const lang = (typeof item === 'object' && item.lang) || opts.lang || 'zh-CN'
    const rate = (typeof item === 'object' && item.rate) || opts.rate
    if (await speak(text, { lang, rate })) played = true
  }
  return played
}
