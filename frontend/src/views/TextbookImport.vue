<template>
  <el-dialog v-model="visible" title="按教材同步知识点" width="720px" :close-on-click-modal="false" @open="onOpen">
    <el-alert type="info" :closable="false" style="margin-bottom: 14px">
      <template #title>
        <span v-if="importCfg.enable_online_ctsf"><b>在线知识大纲</b>（数学人教版 / 语文统编 / 英语PEP / 科学教科版，免下载秒级导入，推荐）；</span>
        <span v-if="importCfg.enable_online_pdf"><b>教材 PDF 提取</b>（支持北师大 / 苏教 / 冀教 / 青岛等 30+ 版本，应用内下载 PDF → 本地 OCR → AI 提取，约 10~15 分钟/册）；</span>
        <span v-else><b>教材 PDF 提取</b>（默认不提供下载，请自行通过合法渠道获取 PDF 后导入）；</span>
        <span v-if="importCfg.enable_photo"><b>拍照教材同步</b>（拍你自己手上的纸质教材页面，AI 识别提取知识点，照片用完即删）；</span>
        <span v-if="importCfg.enable_user_pdf"><b>自备教材 PDF</b>（上传你自己持有的电子教材 PDF，不经过任何在线下载源）。</span>
      </template>
    </el-alert>

    <!-- 使用协议：教材同步由用户自主发起 -->
    <div class="tb-agreement">
      <el-checkbox v-model="agreed">
        <span>我已阅读并同意</span>
        <el-link type="primary" :underline="false" @click.prevent="showAgreement">《教材同步使用协议》</el-link>
        <span>：教材由我本人持有，同步由我自主发起，仅用于个人学习；原始影像/文件识别后自动删除。</span>
      </el-checkbox>
    </div>

    <el-tabs v-model="activeTab">
      <!-- ============ Tab 1：在线知识大纲 ============ -->
      <el-tab-pane v-if="importCfg.enable_online_ctsf" label="在线知识大纲（推荐）" name="ctsf">
        <el-form :model="form" label-width="90px" @submit.prevent>
          <el-form-item label="学科" required>
            <el-select v-model="form.subject" placeholder="选择学科" style="width: 220px" @change="onSubjectChange">
              <el-option v-for="s in subjects" :key="s" :label="s" :value="s" />
            </el-select>
          </el-form-item>
          <el-form-item label="版本" required>
            <el-select v-model="form.version" placeholder="先选学科" style="width: 220px" @change="onVersionChange">
              <el-option v-for="v in versions" :key="v" :label="v" :value="v" />
            </el-select>
          </el-form-item>
          <el-form-item label="年级" required>
            <el-select v-model="form.grade" placeholder="先选版本" style="width: 220px" @change="onGradeChange">
              <el-option v-for="g in grades" :key="g" :label="g" :value="g" />
            </el-select>
          </el-form-item>
          <el-form-item label="册次" required>
            <el-select v-model="form.semester" placeholder="先选年级" style="width: 220px">
              <el-option v-for="s in semesters" :key="s" :label="s" :value="s" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <span v-if="selectedCtsfBook" class="tb-hint">
              {{ selectedCtsfBook.file.replace('.json', '') }} ·
              <span v-if="selectedCtsfBook.imported > 0">已导入 {{ selectedCtsfBook.imported }} 个知识点（重复自动跳过）</span>
              <span v-else>未导入</span>
            </span>
          </el-form-item>
        </el-form>
      </el-tab-pane>

      <!-- ============ Tab 2：教材 PDF 提取 ============ -->
      <el-tab-pane label="教材 PDF 提取" name="pdf">
        <div v-if="!importCfg.enable_online_pdf" class="tb-pdf-guide">
          <p class="tb-hint">本工具<b>不提供教材下载</b>。教材版权归出版社所有，请自行通过<b>合法渠道</b>获取教材 PDF
            （如出版社官网、学校或教育局提供的官方电子教材平台），再导入本工具提取知识点。</p>
          <div class="tb-photo-actions">
            <el-button type="primary" @click="activeTab = 'user_pdf'">前往「自备教材 PDF」导入</el-button>
            <el-button @click="activeTab = 'photo'">或使用「拍照教材同步」</el-button>
          </div>
        </div>
        <template v-else>
        <el-form :model="form" label-width="90px" @submit.prevent>
          <el-form-item label="学科" required>
            <el-select v-model="form.subject" placeholder="选择学科" style="width: 220px" @change="onSubjectChange">
              <el-option v-for="s in pdfSubjects" :key="s" :label="s" :value="s" />
            </el-select>
          </el-form-item>
          <el-form-item label="版本" required>
            <el-select v-model="form.version" placeholder="先选学科" style="width: 220px" @change="onVersionChange">
              <el-option v-for="v in pdfVersions" :key="v" :label="v" :value="v" />
            </el-select>
          </el-form-item>
          <el-form-item label="年级" required>
            <el-select v-model="form.grade" placeholder="先选版本" style="width: 220px" @change="onGradeChange">
              <el-option v-for="g in pdfGrades" :key="g" :label="g" :value="g" />
            </el-select>
          </el-form-item>
          <el-form-item label="册次" required>
            <el-select v-model="form.semester" placeholder="先选年级" style="width: 220px">
              <el-option v-for="s in pdfSemesters" :key="s" :label="s" :value="s" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <span v-if="selectedPdfBook" class="tb-hint">
              {{ selectedPdfBook.version }} {{ selectedPdfBook.subject }} {{ selectedPdfBook.grade }}{{ selectedPdfBook.semester }}
              · <span v-if="selectedPdfBook.local">PDF 已在本地</span>
              <span v-else-if="selectedPdfBook.local_only">⚠ 无在线资源，需手动放置 PDF</span>
              <span v-else>需下载（约 5~30MB）</span> · 源：{{ sourceLabels(selectedPdfBook) }}
            </span>
          </el-form-item>
        </el-form>
        <div class="tb-manual">
          <el-button size="small" type="primary" plain :disabled="!canManual" @click="doOpenManualDir">
            创建并打开该教材文件夹
          </el-button>
          <el-button size="small" @click="doOpenFolder">打开教材总目录</el-button>
          <el-button size="small" @click="doScan">扫描本地 PDF</el-button>
        </div>
        <div class="tb-hint tb-manual-hint">
          <template v-if="canManual">
            网络全部失败时：手动下载 PDF，<b>重命名为下方文件名</b>后放进该文件夹，再点「扫描本地 PDF」导入：
            <div class="tb-path">
              <code>{{ manualInfo.pdf_name }}</code>
              <el-button link type="primary" size="small" @click="doCopyPath">复制完整路径</el-button>
              <span v-if="manualInfo.exists" class="tb-ok">· 该文件已就位 ✅</span>
            </div>
            <div class="tb-path"><span class="tb-path-label">放置路径：</span><code>{{ displayPath }}</code></div>
          </template>
          <template v-else>
            网络全部失败时：先选好 <b>学科</b> 和 <b>版本</b>，这里会自动显示对应的放置文件夹与文件名（文件夹会自动创建）。
          </template>
        </div>
        </template>
      </el-tab-pane>

      <!-- ============ Tab 3：拍照教材同步 ============ -->
      <el-tab-pane v-if="importCfg.enable_photo" label="📷 拍照教材同步" name="photo">
        <div class="tb-photo">
          <p class="tb-hint">拍下你<b>自己合法购买的纸质教材</b>的页面（每页一张，建议从单元起始页开始拍），
            AI 自动识别文字并按单元提取知识点入库。照片仅用于本次识别，任务结束后自动删除，不长期保存。</p>
          <el-form :model="photoForm" label-width="70px" @submit.prevent>
            <el-form-item label="学科" required>
              <el-select v-model="photoForm.subject" placeholder="选择学科" style="width: 200px">
                <el-option v-for="s in photoSubjects" :key="s" :label="s" :value="s" />
              </el-select>
            </el-form-item>
            <el-form-item label="年级" required>
              <el-select v-model="photoForm.grade" placeholder="选择年级" style="width: 200px">
                <el-option v-for="g in GRADES" :key="g" :label="g" :value="g" />
              </el-select>
            </el-form-item>
            <el-form-item label="册次" required>
              <el-select v-model="photoForm.semester" placeholder="选择册次" style="width: 200px">
                <el-option v-for="s in SEMESTERS" :key="s" :label="s" :value="s" />
              </el-select>
            </el-form-item>
          </el-form>
          <div class="tb-photo-actions">
            <el-button type="primary" @click="openPhotoCamera">📷 用电脑摄像头拍摄</el-button>
            <el-button @click="triggerPhotoFile">📱 手机/平板拍照或选照片</el-button>
            <input ref="photoFileInput" type="file" accept="image/*" capture="environment" multiple
                   style="display:none" @change="onPhotoFileChange" />
          </div>
          <div v-if="photoCameraVisible" class="tb-camera">
            <video ref="photoVideo" autoplay playsinline muted></video>
            <div class="tb-camera-actions">
              <el-button type="success" :disabled="!!photoCameraError" @click="capturePhotoShot">拍摄这一页</el-button>
              <el-button @click="closePhotoCamera">关闭摄像头</el-button>
              <span v-if="photoCameraError" class="tb-camera-error">{{ photoCameraError }}</span>
            </div>
          </div>
          <div v-if="photoShots.length" class="tb-shots">
            <div v-for="(shot, idx) in photoShots" :key="shot.key" class="tb-shot">
              <img :src="shot.url" alt="教材照片" />
              <div class="tb-shot-meta">
                <span>第 {{ idx + 1 }} 页</span>
                <el-button link type="danger" @click="removePhotoShot(idx)">删除</el-button>
              </div>
            </div>
          </div>
          <div v-if="photoShots.length" class="tb-photo-submit">
            <el-button type="primary" :loading="!!runningTask && runningTask.status === 'pending'"
                       :disabled="!agreed || !photoForm.subject || !photoForm.grade || !photoForm.semester" @click="doPhotoImport">
              上传并识别（{{ photoShots.length }} 张）
            </el-button>
            <span v-if="!agreed" class="tb-hint"> 请先勾选同意《教材同步使用协议》</span>
            <span v-else-if="!photoForm.subject || !photoForm.grade || !photoForm.semester" class="tb-hint"> 请先选好 学科/年级/册次</span>
          </div>
        </div>
      </el-tab-pane>

      <!-- ============ Tab 4：自备教材 PDF ============ -->
      <el-tab-pane v-if="importCfg.enable_user_pdf" label="📄 自备教材 PDF" name="user_pdf">
        <div class="tb-photo">
          <p class="tb-hint">上传你<b>自己持有的电子教材 PDF</b>（正版电子版 / 出版社授权 / 自购扫描均可），不经过任何在线下载源；
            本地 OCR → AI 按单元提取知识点入库；PDF 会保存到本地教材库（<code>data/textbooks/自备教材/…</code>），
            供预览与对照，仅限个人学习、不得传播。</p>
          <el-form :model="userPdfForm" label-width="70px" @submit.prevent>
            <el-form-item label="学科" required>
              <el-select v-model="userPdfForm.subject" placeholder="选择学科" style="width: 200px">
                <el-option v-for="s in photoSubjects" :key="s" :label="s" :value="s" />
              </el-select>
            </el-form-item>
            <el-form-item label="版本">
              <el-input v-model="userPdfForm.version" placeholder="选填，如：人教版" style="width: 200px" />
            </el-form-item>
            <el-form-item label="年级" required>
              <el-select v-model="userPdfForm.grade" placeholder="选择年级" style="width: 200px">
                <el-option v-for="g in GRADES" :key="g" :label="g" :value="g" />
              </el-select>
            </el-form-item>
            <el-form-item label="册次" required>
              <el-select v-model="userPdfForm.semester" placeholder="选择册次" style="width: 200px">
                <el-option v-for="s in SEMESTERS" :key="s" :label="s" :value="s" />
              </el-select>
            </el-form-item>
          </el-form>
          <div class="tb-photo-actions">
            <el-button type="primary" @click="triggerUserPdfFile">📄 选择本地 PDF 文件</el-button>
            <input ref="userPdfInput" type="file" accept="application/pdf,.pdf" style="display:none" @change="onUserPdfFile" />
            <span v-if="userPdfFile" class="tb-file-info">
              {{ userPdfFile.name }}（{{ (userPdfFile.size / 1024 / 1024).toFixed(1) }}MB）
              <el-button link type="danger" @click="clearUserPdfFile">移除</el-button>
            </span>
          </div>
          <div v-if="userPdfFile" class="tb-photo-submit">
            <el-button type="primary" :loading="!!runningTask && runningTask.status === 'pending'"
                       :disabled="!agreed || !userPdfForm.subject || !userPdfForm.grade || !userPdfForm.semester" @click="doUserPdfImport">
              上传并提取（{{ (userPdfFile.size / 1024 / 1024).toFixed(1) }}MB）
            </el-button>
            <span v-if="!agreed" class="tb-hint"> 请先勾选同意《教材同步使用协议》</span>
            <span v-else-if="!userPdfForm.subject || !userPdfForm.grade || !userPdfForm.semester" class="tb-hint"> 请先选好 学科/年级/册次</span>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>

    <!-- 进度条 -->
    <div v-if="runningTask" style="margin-top: 12px">
      <el-progress :percentage="runningTask.progress" :status="runningTask.status === 'failed' ? 'exception' : undefined" />
      <div class="tb-hint" style="margin-top: 6px">
        {{ runningTask.message }}<span v-if="runningTask.status === 'done' && runningTask.result">（共 {{ runningTask.result.units || '' }} 个单元）</span>
      </div>
    </div>

    <template #footer>
      <el-button @click="visible = false" :disabled="!!runningTask && runningTask.status === 'pending'">取消</el-button>
      <el-button type="primary" v-if="activeTab === 'ctsf' || (activeTab === 'pdf' && importCfg.enable_online_pdf)" :disabled="!agreed" :loading="!!runningTask && runningTask.status === 'pending'" @click="doImport">
        {{ activeTab === 'ctsf' ? '导入在线大纲' : '下载并提取' }}
      </el-button>
      <el-button v-else-if="activeTab === 'photo'" :disabled="!agreed || !photoShots.length" :loading="!!runningTask && runningTask.status === 'pending'" @click="doPhotoImport">
        上传并识别（{{ photoShots.length }} 张）
      </el-button>
      <el-button v-else :disabled="!agreed || !userPdfFile" :loading="!!runningTask && runningTask.status === 'pending'" @click="doUserPdfImport">
        上传并提取
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup>
import { ref, reactive, computed, watch, nextTick, onBeforeUnmount } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { textbookApi } from '@/api/textbook'

const props = defineProps({
  modelValue: Boolean,
})
const emit = defineEmits(['update:modelValue', 'imported'])

const visible = computed({
  get: () => props.modelValue,
  set: (v) => emit('update:modelValue', v),
})

const activeTab = ref('ctsf')
const form = reactive({ subject: '', version: '', grade: '', semester: '' })

// ---- 导入入口配置（backend/textbook_import_config.json）----
const importCfg = ref({ enable_online_ctsf: true, enable_online_pdf: false, enable_photo: true, enable_user_pdf: true })

// ---- 使用协议（教材同步由用户自主发起）----
const AGREED_KEY = 'easyfix_textbook_agreed_v1'
const agreed = ref(localStorage.getItem(AGREED_KEY) === '1')
watch(agreed, (v) => {
  if (v) localStorage.setItem(AGREED_KEY, '1')
})
const AGREEMENT_TEXT = '《教材同步使用协议》<br><br>' +
  '一、定义与功能性质<br>' +
  '1.1 本软件提供的“教材同步功能”包括：拍照教材同步、自备教材 PDF、在线知识大纲、教材 PDF 提取。本功能仅向用户提供技术处理服务，即：从用户提供或指定的教材影像、PDF 文件中识别文字、提取并整理知识点。<br>' +
  '1.2 本软件不生产、不销售、不传播任何教材内容，不以任何形式向用户提供教材文件本身；教材内容之著作权及邻接权归原权利人（出版社、作者等）所有。<br><br>' +
  '二、用户自主发起与内容来源<br>' +
  '2.1 教材同步所处理之教材影像与文件，均由用户本人持有并提供：拍照教材同步为用户对自购纸质教材拍摄之页面影像；自备教材 PDF 为用户合法取得之电子教材文件；在线知识大纲与教材 PDF 提取，仅在用户明确选择并主动操作时，软件方联网获取教材目录信息或下载对应资源。<br>' +
  '2.2 教材同步之发起、内容之选择与提供，均系用户自主行为。本软件运行于用户本地设备：对于拍照教材同步与自备教材 PDF，本软件不主动获取、不汇总、不对外提供任何教材内容；对于在线知识大纲与教材 PDF 提取，本软件仅在用户明确选择并主动操作时联网获取教材目录信息或下载对应资源（教材 PDF 下载入口默认关闭），相关资源均来源于第三方公开网络，其合法性与适用性由用户自行评估，本软件不对第三方资源的合法性作任何保证。<br><br>' +
  '三、权利声明与保证<br>' +
  '3.1 用户保证其对所上传或指定之教材影像/文件享有合法持有与个人学习使用之权利（包括但不限于：自购纸质教材、出版社授权的电子版、自行扫描的自有教材等）。<br>' +
  '3.2 用户保证上传内容不违反中华人民共和国法律法规，不侵害任何第三方之著作权、出版权、隐私权及其他合法权益。因用户提供之内容引发的任何纠纷、索赔或行政处罚，由用户自行承担全部责任，与本软件及开发者无关。<br>' +
  '3.3 用户不得上传非法复制、盗版、破解或未经授权共享之电子教材文件。开发者发现用户违反本条约定时，有权拒绝提供服务或关闭相应功能。<br><br>' +
  '四、使用限制<br>' +
  '4.1 同步生成之知识点及留存之教材文件，仅限用户本人及家庭成员个人学习使用。<br>' +
  '4.2 未经权利人许可，用户不得将教材内容或其衍生内容用于任何商业用途，不得通过任何形式（包括但不限于复制、转发、上传、出售、共享链接）向任何第三方传播、分发教材影像/文件及其识别成果。<br>' +
  '4.3 因用户违反本条约定的传播、商用等行为所产生的一切法律责任，由用户自行承担；本软件及开发者不承担任何形式的连带责任。<br><br>' +
  '五、数据存储与处理<br>' +
  '5.1 教材影像/文件及识别成果（知识点文本）均存储于用户本地设备。本软件不将教材内容上传至任何云端服务器，不向任何第三方分发、共享、转让教材文件及其识别成果。<br>' +
  '5.2 拍照教材同步上传之页面影像属临时处理数据，识别完成后由本软件自动清理；原始照片由用户自行保管于其个人设备。自备教材 PDF 及在线/手动导入之教材 PDF 保存于用户本地教材库目录，供教材预览与知识点对照使用，由用户自行保管。<br>' +
  '5.3 用户有权随时删除本地教材库中的教材文件及其识别成果。<br><br>' +
  '六、免责声明<br>' +
  '6.1 本软件按“现状”提供教材同步功能，不对识别与提取结果的准确性、完整性作任何明示或默示保证。<br>' +
  '6.2 因教材文件质量、来源、合法性问题，或因用户自行传播、商用教材内容所产生之任何损失或争议，由用户自行负责，本软件及开发者不承担责任。<br><br>' +
  '七、协议变更与适用<br>' +
  '7.1 开发者可适时更新本协议，更新内容于软件内公示；用户继续使用本功能即视为接受更新后之协议。<br>' +
  '7.2 本协议之订立、解释与争议解决适用中华人民共和国法律。<br><br>' +
  '勾选“我已阅读并同意”即表示你已阅读、理解并接受上述全部条款。'
const showAgreement = () => {
  ElMessageBox.alert(AGREEMENT_TEXT, '使用协议', {
    dangerouslyUseHTMLString: true,
    confirmButtonText: '我已了解',
    customClass: 'tb-agreement-box',
    width: '620px',
  })
}

// ---- 拍照教材同步 ----
const photoForm = reactive({ subject: '', grade: '', semester: '' })
const photoSubjects = computed(() => {
  // 优先用目录里的学科；目录不可用（离线/关闭在线入口）时退化为常见学科
  const fromCatalog = [...new Set(pdfBooks.value.map(b => b.subject))].filter(Boolean)
  return fromCatalog.length ? fromCatalog : ['数学', '语文', '英语', '科学']
})
const photoShots = ref([])
let photoShotSeq = 0
const photoCameraVisible = ref(false)
const photoCameraError = ref('')
const photoCameraStream = ref(null)
const photoVideo = ref(null)
const photoFileInput = ref(null)

const clearPhotoShots = () => {
  photoShots.value.forEach(s => s.url && URL.revokeObjectURL(s.url))
  photoShots.value = []
  photoShotSeq = 0
}
const stopPhotoCamera = () => {
  const stream = photoCameraStream.value
  if (stream) {
    try { stream.getTracks().forEach(t => t.stop()) } catch (e) { /* 忽略 */ }
    photoCameraStream.value = null
  }
  if (photoVideo.value) {
    try { photoVideo.value.srcObject = null } catch (e) { /* 忽略 */ }
  }
}
const closePhotoCamera = () => {
  photoCameraVisible.value = false
  stopPhotoCamera()
}
const openPhotoCamera = async () => {
  photoCameraError.value = ''
  photoCameraVisible.value = true
  await nextTick()
  try {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      throw new Error('当前页面无法直接调用摄像头（需要 http://localhost 或 https 打开）')
    }
    const stream = await navigator.mediaDevices.getUserMedia({
      video: { facingMode: 'environment', width: { ideal: 1920 }, height: { ideal: 1080 } },
      audio: false,
    })
    photoCameraStream.value = stream
    if (photoVideo.value) {
      photoVideo.value.srcObject = stream
      if (photoVideo.value.play) await photoVideo.value.play()
    }
  } catch (error) {
    const name = error?.name || ''
    if (name === 'NotAllowedError' || name === 'SecurityError') {
      photoCameraError.value = '摄像头权限被拒绝，请点地址栏左侧的锁形图标重新允许后再试'
    } else if (name === 'NotFoundError' || name === 'DevicesNotFoundError') {
      photoCameraError.value = '没有检测到可用摄像头'
    } else {
      photoCameraError.value = error?.message || '摄像头调用失败'
    }
    stopPhotoCamera()
  }
}
const capturePhotoShot = () => {
  const video = photoVideo.value
  if (!video || !video.videoWidth) {
    ElMessage.warning('摄像头还没准备好，请稍等一秒再拍')
    return
  }
  const canvas = document.createElement('canvas')
  const maxWidth = 2000 // 控体积，同时保证 OCR 看得清
  const scale = Math.min(1, maxWidth / video.videoWidth)
  canvas.width = Math.round(video.videoWidth * scale)
  canvas.height = Math.round(video.videoHeight * scale)
  canvas.getContext('2d').drawImage(video, 0, 0, canvas.width, canvas.height)
  canvas.toBlob(blob => {
    if (!blob) {
      ElMessage.error('拍照失败，请重试')
      return
    }
    const file = new File([blob], `photo_${Date.now()}.jpg`, { type: 'image/jpeg' })
    photoShotSeq += 1
    photoShots.value.push({ key: `shot-${photoShotSeq}`, url: URL.createObjectURL(blob), file })
    ElMessage.success(`已拍第 ${photoShots.value.length} 张，可继续拍下一页`)
  }, 'image/jpeg', 0.92)
}
const removePhotoShot = (index) => {
  const shot = photoShots.value[index]
  if (shot?.url) URL.revokeObjectURL(shot.url)
  photoShots.value.splice(index, 1)
}
const triggerPhotoFile = () => photoFileInput.value?.click()
const onPhotoFileChange = (event) => {
  const files = Array.from(event.target?.files || [])
  files.forEach(file => {
    photoShotSeq += 1
    photoShots.value.push({ key: `shot-${photoShotSeq}`, url: URL.createObjectURL(file), file })
  })
  if (files.length) ElMessage.success(`已加入 ${files.length} 张照片`)
  if (event.target) event.target.value = ''
}
const doPhotoImport = async () => {
  if (!agreed.value) {
    ElMessage.warning('请先勾选同意《教材同步使用协议》')
    return
  }
  if (!photoForm.subject || !photoForm.grade || !photoForm.semester) {
    ElMessage.warning('请先选择 学科/年级/册次')
    return
  }
  if (!photoShots.value.length) {
    ElMessage.warning('请先拍摄或选择教材照片')
    return
  }
  try {
    await ElMessageBox.confirm(
      `将上传 ${photoShots.value.length} 张教材照片，识别并按单元提取《${photoForm.subject} ${photoForm.grade}${photoForm.semester}》知识点入库。\n\n照片仅用于本次识别，任务结束后自动删除。继续？`,
      '拍照教材同步', { type: 'info' }
    )
  } catch {
    return
  }
  const fd = new FormData()
  fd.append('subject', photoForm.subject)
  fd.append('grade', photoForm.grade)
  fd.append('semester', photoForm.semester)
  photoShots.value.forEach(s => fd.append('files', s.file))
  try {
    const { data } = await textbookApi.photoImport(fd)
    closePhotoCamera()
    startPoll(data.task_id)
  } catch (e) {
    ElMessage.error(e.detail || e.message || '上传失败')
  }
}

// ---- 自备教材 PDF ----
const userPdfForm = reactive({ subject: '', grade: '', semester: '', version: '' })
const userPdfFile = ref(null)
const userPdfInput = ref(null)
const triggerUserPdfFile = () => userPdfInput.value?.click()
const onUserPdfFile = (event) => {
  const f = event.target?.files?.[0]
  if (!f) return
  if (!/\.pdf$/i.test(f.name)) {
    ElMessage.warning('仅支持 PDF 文件')
    if (event.target) event.target.value = ''
    return
  }
  userPdfFile.value = f
  if (event.target) event.target.value = ''
}
const clearUserPdfFile = () => { userPdfFile.value = null }
const doUserPdfImport = async () => {
  if (!agreed.value) {
    ElMessage.warning('请先勾选同意《教材同步使用协议》')
    return
  }
  if (!userPdfForm.subject || !userPdfForm.grade || !userPdfForm.semester) {
    ElMessage.warning('请先选择 学科/年级/册次')
    return
  }
  if (!userPdfFile.value) {
    ElMessage.warning('请先选择要上传的教材 PDF')
    return
  }
  try {
    await ElMessageBox.confirm(
      `将上传《${userPdfFile.value.name}》并按单元提取《${userPdfForm.subject} ${userPdfForm.grade}${userPdfForm.semester}》知识点入库。\n\n该 PDF 将保存到你的本地教材库（data/textbooks/自备教材/…），仅限个人学习使用，请勿传播。继续？`,
      '自备教材 PDF 同步', { type: 'info' }
    )
  } catch {
    return
  }
  const fd = new FormData()
  fd.append('subject', userPdfForm.subject)
  fd.append('grade', userPdfForm.grade)
  fd.append('semester', userPdfForm.semester)
  if (userPdfForm.version) fd.append('version', userPdfForm.version)
  fd.append('file', userPdfFile.value)
  try {
    const { data } = await textbookApi.userPdfImport(fd)
    startPoll(data.task_id)
  } catch (e) {
    ElMessage.error(e.detail || e.message || '上传失败')
  }
}

// ---- 目录数据 ----
const ctsfBooks = ref([])   // 在线大纲 44 本
const pdfBooks = ref([])    // 教材 PDF 369 本

// ---- 当前任务（轮询） ----
const runningTask = ref(null)
let pollTimer = null

const GRADES = ['一年级', '二年级', '三年级', '四年级', '五年级', '六年级']
const SEMESTERS = ['上册', '下册']

const tabVisible = (name) => {
  if (name === 'ctsf') return !!importCfg.value.enable_online_ctsf
  if (name === 'pdf') return true // PDF tab 常显；关闭在线下载时显示「自行获取」引导
  if (name === 'photo') return !!importCfg.value.enable_photo
  if (name === 'user_pdf') return !!importCfg.value.enable_user_pdf
  return true
}
const fixActiveTab = () => {
  if (!tabVisible(activeTab.value)) {
    const order = ['ctsf', 'pdf', 'photo', 'user_pdf']
    activeTab.value = order.find(t => tabVisible(t)) || 'ctsf'
  }
}

const onOpen = async () => {
  try {
    const { data } = await textbookApi.importConfig()
    importCfg.value = Object.assign({ enable_online_ctsf: true, enable_online_pdf: false, enable_photo: true, enable_user_pdf: true }, data || {})
  } catch (e) {
    importCfg.value = { enable_online_ctsf: true, enable_online_pdf: false, enable_photo: true, enable_user_pdf: true }
  }
  // 默认 tab 被配置隐藏时，切到第一个可见 tab
  fixActiveTab()
  if (importCfg.value.enable_online_ctsf && !ctsfBooks.value.length) {
    try {
      const { data } = await textbookApi.ctsfCatalog()
      ctsfBooks.value = data.books || []
    } catch (e) {
      ElMessage.error('获取在线大纲目录失败（需要联网）')
    }
  }
  if (importCfg.value.enable_online_pdf && !pdfBooks.value.length) {
    try {
      const { data } = await textbookApi.catalog()
      pdfBooks.value = data.books || []
    } catch (e) {
      ElMessage.error('获取教材目录失败')
    }
  }
  clearPhotoShots()
  closePhotoCamera()
  refreshManualDir(false)  // 打开时按上次选择补一次文件夹信息（自动建目录）
}

// ---- 选择器联动 ----
const subjects = computed(() => [...new Set(ctsfBooks.value.map(b => b.subject))])
const pdfSubjects = computed(() => [...new Set(pdfBooks.value.map(b => b.subject))])

const versions = computed(() => [...new Set(ctsfBooks.value.filter(b => b.subject === form.subject).map(b => b.version))])
const grades = computed(() => {
  const base = ctsfBooks.value.filter(b => b.subject === form.subject && b.version === form.version)
  return GRADES.filter(g => base.some(b => b.grade === g))
})
const semesters = computed(() => {
  const base = ctsfBooks.value.filter(b => b.subject === form.subject && b.version === form.version && b.grade === form.grade)
  return SEMESTERS.filter(s => base.some(b => b.semester === s))
})

const pdfVersions = computed(() => [...new Set(pdfBooks.value.filter(b => b.subject === form.subject).map(b => b.version))])
const pdfGrades = computed(() => {
  const base = pdfBooks.value.filter(b => b.subject === form.subject && b.version === form.version)
  return GRADES.filter(g => base.some(b => b.grade === g))
})
const pdfSemesters = computed(() => {
  const base = pdfBooks.value.filter(b => b.subject === form.subject && b.version === form.version && b.grade === form.grade)
  return SEMESTERS.filter(s => base.some(b => b.semester === s))
})

const selectedCtsfBook = computed(() =>
  ctsfBooks.value.find(b => b.subject === form.subject && b.version === form.version
    && b.grade === form.grade && b.semester === form.semester) || null)
const selectedPdfBook = computed(() =>
  pdfBooks.value.find(b => b.subject === form.subject && b.version === form.version
    && b.grade === form.grade && b.semester === form.semester) || null)

const sourceLabels = (book) => {
  const srcs = (book.downloads || []).map(d => d.source === 'freepep' ? '直连' : 'GitHub')
  return srcs.join(' + ')
}

const onSubjectChange = () => { form.version = ''; form.grade = ''; form.semester = '' }
const onVersionChange = () => { form.grade = ''; form.semester = '' }
const onGradeChange = () => { form.semester = '' }

// ---- 手动放置路径：随选择动态显示 + 目录自动创建 ----
const manualInfo = ref({ dir: '', dir_rel: '', pdf_path: '', pdf_name: '', exists: false })
let manualDirTimer = null

const canManual = computed(() => !!form.version && !!form.subject)
// 后端返回前先用相对路径兜底，避免闪空
const displayPath = computed(() => manualInfo.value.pdf_path
  || `data/textbooks/${form.version}/${form.subject}/${form.grade}${form.semester}.pdf`)

const refreshManualDir = async (open = false) => {
  if (!canManual.value) {
    manualInfo.value = { dir: '', dir_rel: '', pdf_path: '', pdf_name: '', exists: false }
    return
  }
  try {
    const { data } = await textbookApi.manualDir({
      version: form.version, subject: form.subject, grade: form.grade, semester: form.semester, open,
    })
    manualInfo.value = data
  } catch (e) {
    if (open) ElMessage.error(e.detail || e.message || '创建/打开教材文件夹失败')
  }
}

// 选择变化 → 去抖后静默创建目标目录（不弹资源管理器）
watch(() => [form.subject, form.version, form.grade, form.semester], () => {
  if (manualDirTimer) clearTimeout(manualDirTimer)
  manualDirTimer = setTimeout(() => refreshManualDir(false), 300)
})

// ---- 导入 ----
const doImport = async () => {
  if (!agreed.value) {
    ElMessage.warning('请先勾选同意《教材同步使用协议》')
    return
  }
  if (!form.subject || !form.version || !form.grade || !form.semester) {
    ElMessage.warning('请完整选择 学科/版本/年级/册次')
    return
  }
  if (activeTab.value === 'ctsf' && !selectedCtsfBook.value) {
    ElMessage.warning('在线大纲中未找到该教材')
    return
  }
  if (activeTab.value === 'pdf' && !selectedPdfBook.value) {
    ElMessage.warning('教材目录中未找到该教材')
    return
  }
  const tip = activeTab.value === 'ctsf'
    ? `从在线大纲导入《${form.version} ${form.subject} ${form.grade}${form.semester}》知识点（教材 PDF 将保存到本地教材库目录供对照）。`
    : selectedPdfBook.value?.local_only
      ? `《${form.version} ${form.subject} ${form.grade}${form.semester}》暂无在线资源。\n\n请手动下载教材 PDF，命名为 ${manualInfo.value.pdf_name || `${form.grade}${form.semester}.pdf`}，\n放到：${displayPath.value}\n然后点「扫描本地 PDF」再导入。\n\n现在就打开该文件夹？`
      : `下载并提取《${form.version} ${form.subject} ${form.grade}${form.semester}》？PDF 下载 + OCR 识别 + AI 提取约需 10~15 分钟，期间可关闭本窗口，任务会继续。`
  try {
    await ElMessageBox.confirm(tip, '确认导入', { type: 'info' })
  } catch {
    return
  }
  if (selectedPdfBook.value?.local_only) {
    // 无在线源：创建并打开「当前选择」对应的文件夹，引导手动放置
    await refreshManualDir(true)
    ElMessage.info(`已打开教材文件夹，把 PDF 命名为「${manualInfo.value.pdf_name || `${form.grade}${form.semester}.pdf`}」放进去，再点「扫描本地 PDF」`)
    return
  }
  try {
    let res
    if (activeTab.value === 'ctsf') {
      res = await textbookApi.ctsfImport({
        subject: form.subject, version: form.version, grade: form.grade, semester: form.semester,
      })
    } else {
      res = await textbookApi.importBook({
        subject: form.subject, version: form.version, grade: form.grade, semester: form.semester,
      })
    }
    startPoll(res.data.task_id)
  } catch (e) {
    ElMessage.error(e.detail || e.message || '启动导入失败')
  }
}

const startPoll = (taskId) => {
  runningTask.value = { id: taskId, progress: 0, message: '排队中', status: 'pending' }
  pollTimer = setInterval(async () => {
    try {
      const { data } = await textbookApi.task(taskId)
      runningTask.value = data
      if (data.status === 'done') {
        clearInterval(pollTimer)
        ElMessage.success(data.message || '导入完成')
        emit('imported')
        setTimeout(() => { runningTask.value = null }, 4000)
      } else if (data.status === 'failed') {
        clearInterval(pollTimer)
        ElMessage.error(data.error || data.message || '导入失败')
        setTimeout(() => { runningTask.value = null }, 8000)
      }
    } catch {
      clearInterval(pollTimer)
      ElMessage.error('查询任务进度失败')
    }
  }, 1500)
}

// ---- 手动放置兜底 ----
const doOpenFolder = async () => {
  try {
    await textbookApi.openFolder()
  } catch (e) {
    ElMessage.error(e.detail || '打开文件夹失败')
  }
}

// 打开「当前选择」对应的文件夹（不存在则先创建）
const doOpenManualDir = async () => {
  if (!canManual.value) {
    ElMessage.warning('请先选择 学科 和 版本')
    return
  }
  await refreshManualDir(true)
  if (manualInfo.value.dir) {
    ElMessage.info(`请把 PDF 命名为「${manualInfo.value.pdf_name}」放进该文件夹，再点「扫描本地 PDF」`)
  }
}

const doCopyPath = async () => {
  const text = displayPath.value
  try {
    await navigator.clipboard.writeText(text)
    ElMessage.success('完整路径已复制')
  } catch {
    ElMessage.info(`复制失败，请手动选择：${text}`)
  }
}

const doScan = async () => {
  try {
    // 已选 学科+版本 → 只扫当前教材目录；未选 → 全树扫描兜底
    const scoped = canManual.value
    const { data } = await textbookApi.scanLocal(scoped
      ? { version: form.version, subject: form.subject }
      : {})
    const files = data.files || []
    const scanDir = data.dir || ''
    if (!files.length) {
      ElMessage.info(scoped
        ? `「${form.version}/${form.subject}」文件夹里没有 PDF：\n${scanDir}\n\n请把 ${manualInfo.value.pdf_name || '教材 PDF'} 放进去，再点「扫描本地 PDF」（可先点「创建并打开该教材文件夹」）`
        : '未发现本地教材 PDF')
      return
    }
    // 优先精确文件名 <年级><册次>.pdf，其次模糊 年级+册次 匹配，最后取第一个
    const expectName = `${form.grade}${form.semester}.pdf`
    const exact = form.grade && form.semester
      ? files.find(f => f.path.replace(/\\/g, '/').endsWith(expectName)) : null
    const fuzzy = form.grade && form.semester
      ? files.find(f => f.grade === form.grade && f.semester === form.semester) : null
    const target = exact || fuzzy || files[0]
    const list = files.map(f => `${f.grade}${f.semester || ''}.pdf（${(f.size / 1024 / 1024).toFixed(1)}MB）`).join('\n')
    const choose = await ElMessageBox.confirm(
      `扫描「${form.version}/${form.subject}」文件夹，找到 ${files.length} 个 PDF：\n${list}\n\n${(exact || fuzzy) ? '已选中当前教材：' : '将导入第一个：'}${target.grade}${target.semester || ''}.pdf`,
      '扫描结果', { type: 'info', confirmButtonText: '导入该册', cancelButtonText: '暂不' }
    ).catch(() => null)
    if (!choose) return
    const f = target
    const res = await textbookApi.importBook({
      subject: f.subject === '未分类' ? form.subject || '数学' : f.subject,
      version: f.version === '未分类' ? form.version || '手动放置' : f.version,
      grade: f.grade || form.grade || '三年级',
      semester: f.semester || form.semester || '上册',
      local_pdf: f.path,
    })
    startPoll(res.data.task_id)
  } catch (e) {
    if (e === 'cancel' || e?.message?.includes('cancel')) return
    ElMessage.error(e.detail || e.message || '扫描失败')
  }
}

onBeforeUnmount(() => {
  if (pollTimer) clearInterval(pollTimer)
  if (manualDirTimer) clearTimeout(manualDirTimer)
  stopPhotoCamera()
})
</script>

<style scoped>
.tb-hint {
  font-size: 12px;
  color: #909399;
}
.tb-manual {
  margin-top: 4px;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}
.tb-manual-hint {
  margin-top: 8px;
  line-height: 1.8;
}
.tb-path {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}
.tb-path code {
  background: #f5f7fa;
  border: 1px solid #e4e7ed;
  border-radius: 4px;
  padding: 1px 6px;
  color: #606266;
  font-size: 12px;
  word-break: break-all;
  user-select: all;
}
.tb-path-label {
  flex: 0 0 auto;
}
.tb-ok {
  color: #67c23a;
}
.tb-photo-actions {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
  margin: 4px 0 10px;
}
.tb-camera {
  margin: 8px 0;
  padding: 10px;
  border: 1px solid #e4e7ed;
  border-radius: 6px;
  background: #fafafa;
  text-align: center;
}
.tb-camera video {
  max-width: 100%;
  max-height: 300px;
  border-radius: 4px;
  background: #000;
}
.tb-camera-actions {
  margin-top: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  flex-wrap: wrap;
}
.tb-camera-error {
  color: #f56c6c;
  font-size: 12px;
}
.tb-shots {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
  margin: 10px 0;
}
.tb-shot {
  width: 120px;
  border: 1px solid #e4e7ed;
  border-radius: 6px;
  overflow: hidden;
  background: #fff;
}
.tb-shot img {
  width: 100%;
  height: 90px;
  object-fit: cover;
  display: block;
}
.tb-shot-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 4px 8px;
  font-size: 12px;
  color: #909399;
}
.tb-photo-submit {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-top: 4px;
}
.tb-agreement {
  margin-bottom: 10px;
  padding: 8px 12px;
  border: 1px solid #ebeef5;
  border-radius: 6px;
  background: #fafcff;
  font-size: 12px;
  color: #606266;
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}
.tb-file-info {
  font-size: 12px;
  color: #606266;
}
.tb-pdf-guide {
  padding: 14px 16px;
  border: 1px dashed #c0c4cc;
  border-radius: 6px;
  background: #fbfcfe;
}
/* 协议勾选：长文案允许换行，不超出弹窗边界 */
.tb-agreement {
  margin-bottom: 12px;
}
.tb-agreement .el-checkbox {
  height: auto;
  align-items: flex-start;
  white-space: normal;
  margin-right: 0;
}
.tb-agreement .el-checkbox__label {
  white-space: normal;
  line-height: 1.6;
  padding-left: 8px;
}
</style>

<style>
/* ElMessageBox 挂到 body 上，需非 scoped */
.tb-agreement-box .el-message-box__message {
  max-height: 420px;
  overflow: auto;
  font-size: 13px;
  line-height: 1.9;
  color: #303133;
}
</style>
