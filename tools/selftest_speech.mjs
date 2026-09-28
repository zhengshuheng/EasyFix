/**
 * 统一读音模块行为测试（Node + 浏览器 API stub）
 *
 * 目的：浏览器里需要登录才能点到语法页喇叭，这里改为对 frontend/src/utils/speech.js
 * 做行为断言，覆盖真实决策逻辑：
 *   Chrome（有语音也强制）→ 服务器 TTS / 非 Chrome 有语音 → 浏览器朗读 /
 *   浏览器朗读报错 → 降级服务器 TTS / 语音列表为空 → 服务器 TTS
 * 服务器 TTS 的 URL 与真实音频字节均打到真实后端 127.0.0.1:8012 校验。
 *
 * 运行（需后端已在 127.0.0.1:8012 运行）：node tools/selftest_speech.mjs
 */

import http from 'node:http'
import path from 'node:path'
import { pathToFileURL } from 'node:url'

const BASE = 'http://127.0.0.1:8012'
let pass = 0
let fail = 0
const check = (name, ok, extra = '') => {
  if (ok) { pass++; console.log(`  PASS  ${name}${extra ? ' | ' + extra : ''}`) }
  else { fail++; console.log(`  FAIL  ${name}${extra ? ' | ' + extra : ''}`) }
}

// Node 16 无全局 fetch：用 node:http 造最小 fetch（ok/status/arrayBuffer 够模块用）
const REAL_FETCH = (url) => new Promise((resolve, reject) => {
  http.get(url, (res) => {
    const chunks = []
    res.on('data', (c) => chunks.push(c))
    res.on('end', () => {
      const buf = Buffer.concat(chunks)
      resolve({
        ok: res.statusCode >= 200 && res.statusCode < 300,
        status: res.statusCode,
        headers: { get: (k) => res.headers[String(k).toLowerCase()] || null },
        arrayBuffer: async () => buf.buffer.slice(buf.byteOffset, buf.byteOffset + buf.byteLength),
      })
    })
  }).on('error', reject)
})

// ---------- 浏览器环境 stub ----------
const fetched = []      // 走 Web Audio 分支时模块自己发的请求
const audioSrcs = []    // 走 Audio 元素分支时交给浏览器的 URL（浏览器会自行请求）
const uttered = []      // 浏览器语音朗读
const synthEvents = { cancel: 0, speak: 0 }
let voices = []
let failSpeak = false

globalThis.window = globalThis
globalThis.navigator = { userAgent: '' }
globalThis.fetch = async (url) => { fetched.push(url); return await REAL_FETCH(BASE + url) }
globalThis.Audio = class {
  constructor(src) { this.src = src; audioSrcs.push(src) }
  play() { return Promise.reject(new Error('node: no audio device')) } // 模拟「播不出声」判定
}
globalThis.SpeechSynthesisUtterance = class {
  constructor(text) { this.text = text }
}
globalThis.speechSynthesis = {
  getVoices: () => voices,
  cancel: () => { synthEvents.cancel++ },
  speak(u) {
    synthEvents.speak++
    uttered.push(u)
    setTimeout(() => (failSpeak ? u.onerror && u.onerror() : u.onend && u.onend()), 1)
  },
}
// 模拟「已解锁的 AudioContext」：走 Web Audio 分支（模块会自己 fetch）
class FakeAudioContext {
  constructor() { this.state = 'running'; this.destination = {} }
  resume() { return Promise.resolve() }
  decodeAudioData() { return Promise.resolve({ duration: 1 }) }
  createBufferSource() {
    const src = { buffer: null, onended: null, connect() {}, stop() {}, start() { setTimeout(() => src.onended && src.onended(), 1) } }
    return src
  }
}

const speech = await import(pathToFileURL(
  path.resolve(path.dirname(new URL(import.meta.url).pathname.slice(1)), '..', 'frontend/src/utils/speech.js')
).href)

console.log('== 1. 判定函数 ==')
globalThis.navigator.userAgent = 'Mozilla/5.0 Chrome/120.0.0.0 Safari/537.36'
check('Chrome UA → isChromeNoEdge()=true', speech.isChromeNoEdge() === true)
globalThis.navigator.userAgent = 'Mozilla/5.0 Chrome/120.0.0.0 Safari/537.36 Edg/120.0'
check('Edge UA → isChromeNoEdge()=false', speech.isChromeNoEdge() === false)
globalThis.navigator.userAgent = 'Mozilla/5.0 Chrome/120.0.0.0 Safari/537.36 OPR/106.0'
check('Opera UA → isChromeNoEdge()=false', speech.isChromeNoEdge() === false)
globalThis.navigator.userAgent = 'Mozilla/5.0 Firefox/121.0'
check('Firefox UA → isChromeNoEdge()=false', speech.isChromeNoEdge() === false)

voices = [{ lang: 'en-US', name: 'dummy' }, { lang: 'zh-CN', name: 'dummy-zh' }]
globalThis.navigator.userAgent = 'Mozilla/5.0 Chrome/120.0.0.0 Safari/537.36'
check('Chrome 即使列表有 en 语音也判定「无可用语音」', speech.hasVoiceFor('en') === false)
globalThis.navigator.userAgent = 'Mozilla/5.0 Firefox/121.0'
check('Firefox 有 en 语音 → hasVoiceFor(en)=true', speech.hasVoiceFor('en') === true)
check('Firefox 无 ja 语音 → hasVoiceFor(ja)=false', speech.hasVoiceFor('ja') === false)
voices = []
check('语音列表为空 → hasVoiceFor(en)=false（首次进页面兜底）', speech.hasVoiceFor('en') === false)

console.log('== 2. 语法例句：Chrome + 有 en 语音 → 必须走服务器 TTS（Audio 元素分支）==')
voices = [{ lang: 'en-US', name: 'dummy' }, { lang: 'zh-CN', name: 'dummy-zh' }]
globalThis.navigator.userAgent = 'Mozilla/5.0 Chrome/120.0.0.0 Safari/537.36'
audioSrcs.length = 0; fetched.length = 0; uttered.length = 0
await speech.speakEn('She is a student.')
check('交给浏览器播放 1 个服务器 TTS URL', audioSrcs.length === 1, audioSrcs[0] || '(无)')
check('URL 带 lang=en-US', (audioSrcs[0] || '').includes('lang=en-US'))
check('URL 文本正确编码', (audioSrcs[0] || '').includes('english=She%20is%20a%20student.'))
check('压根没走浏览器语音（这正是原来无声的原因）', uttered.length === 0)

console.log('== 2b. 同一场景 + 已解锁 AudioContext → 模块自己 fetch（Web Audio 分支）==')
globalThis.AudioContext = FakeAudioContext
audioSrcs.length = 0; fetched.length = 0
await speech.speakEn('She is a student.')
check('模块发起 1 次 /api/words/audio 请求', fetched.length === 1, fetched[0] || '(无)')
check('请求带 lang=en-US', (fetched[0] || '').includes('lang=en-US'))
check('不再退 Audio 元素', audioSrcs.length === 0)
delete globalThis.AudioContext

console.log('== 3. 非 Chrome 有语音 → 走浏览器朗读，不请求服务器 ==')
globalThis.navigator.userAgent = 'Mozilla/5.0 Firefox/121.0'
audioSrcs.length = 0; fetched.length = 0; uttered.length = 0
await speech.speakEn('She is a student.')
check('无服务器请求/音频 URL', audioSrcs.length === 0 && fetched.length === 0)
check('调用浏览器 speechSynthesis 1 次', uttered.length === 1)
check('utterance.lang=en-US', !!(uttered[0] && uttered[0].lang === 'en-US'))
check('绑定 en 语音', !!(uttered[0] && uttered[0].voice && uttered[0].voice.lang === 'en-US'))
check('语速 0.85', !!(uttered[0] && uttered[0].rate === 0.85))

console.log('== 4. 浏览器朗读报错 → 自动降级服务器 TTS（原来只会静默复位）==')
failSpeak = true
audioSrcs.length = 0
await speech.speakEn('fallback test')
check('报错后仍发出服务器音频 URL', audioSrcs.length === 1, audioSrcs[0] || '(无)')
failSpeak = false

console.log('== 5. 中文读题场景（Chrome）==')
globalThis.navigator.userAgent = 'Mozilla/5.0 Chrome/120.0.0.0 Safari/537.36'
audioSrcs.length = 0
await speech.speakZh('把算出的答案填进去')
check('中文走服务器 TTS 且 lang=zh-CN', audioSrcs.length === 1 && audioSrcs[0].includes('lang=zh-CN'), audioSrcs[0] || '(无)')

console.log('== 6. speakSequence：先英文后中文（语法例句形态）==')
audioSrcs.length = 0
const seqOk = await speech.speakSequence([
  { text: 'She is a student.', lang: 'en-US', rate: 0.85 },
  { text: '，她是一名学生。', lang: 'zh-CN', rate: 0.95 },
])
check('依次产生两条音频 URL', audioSrcs.length === 2, JSON.stringify(audioSrcs))
check('顺序 en → zh', (audioSrcs[0] || '').includes('lang=en-US') && (audioSrcs[1] || '').includes('lang=zh-CN'))
check('返回布尔（是否播过）', typeof seqOk === 'boolean')
audioSrcs.length = 0
await speech.speakSequence([null, { text: '' }, { text: 'only zh', lang: 'zh-CN' }], { lang: 'zh-CN' })
check('空项自动跳过，只播一条', audioSrcs.length === 1, JSON.stringify(audioSrcs))

console.log('== 7. stopSpeech ==')
const beforeCancel = synthEvents.cancel
speech.stopSpeech()
check('stopSpeech 调用 speechSynthesis.cancel()', synthEvents.cancel === beforeCancel + 1)

console.log('== 8. 真实后端音频字节（降级通路确实有声音）==')
const r1 = await REAL_FETCH(`${BASE}/api/words/audio?english=${encodeURIComponent('She is a student.')}&lang=en-US`)
const b1 = Buffer.from(await r1.arrayBuffer())
const r2 = await REAL_FETCH(`${BASE}/api/words/audio?english=${encodeURIComponent('，她是一名学生。')}&lang=zh-CN`)
const b2 = Buffer.from(await r2.arrayBuffer())
check('英文句子 TTS 200 + audio/*', r1.status === 200 && (r1.headers.get('content-type') || '').includes('audio'), `${r1.status} ${r1.headers.get('content-type')} ${b1.length}B`)
check('中文句子 TTS 200 + audio/*', r2.status === 200 && (r2.headers.get('content-type') || '').includes('audio'), `${r2.status} ${r2.headers.get('content-type')} ${b2.length}B`)
const isMp3 = (b) => b.length > 2000 && (b.slice(0, 3).toString() === 'ID3' || (b[0] === 0xff && (b[1] & 0xe0) === 0xe0))
check('英文音频是合法 MP3', isMp3(b1), b1.slice(0, 3).toString('hex'))
check('中文音频是合法 MP3', isMp3(b2), b2.slice(0, 3).toString('hex'))

console.log(`\n结果：${pass} 通过 / ${fail} 失败`)
process.exit(fail ? 1 : 0)
