<template>
  <div v-if="scene" class="scene-visual">
    <!-- count：一排物品 -->
    <div v-if="scene.type === 'count'" class="scene-count">
      <span
        v-for="i in scene.count"
        :key="i"
        class="scene-emoji"
        :style="{ fontSize: emojiSize }"
      >{{ scene.emoji }}</span>
      <span v-if="scene.count > 6" class="scene-more">……</span>
    </div>
    <!-- group：几组×每组几个（袋子/盒子容器） -->
    <div v-else-if="scene.type === 'group'" class="scene-group">
      <div v-for="g in scene.groups" :key="g" class="group-box">
        <span
          v-for="i in scene.per_group"
          :key="i"
          class="scene-emoji"
          :style="{ fontSize: emojiSize }"
        >{{ scene.emoji }}</span>
      </div>
    </div>
    <!-- count-split：图示算式（两堆物品 + 运算符 + 等号 + 问号） -->
    <div v-else-if="scene.type === 'count-split'" class="scene-split">
      <span v-if="scene.operator === '×'" class="split-side">
        <!-- 乘法意义：组数 × 每组个数，用盒子分组展示 -->
        <span v-for="g in scene.right_count" :key="g" class="group-box split-box">
          <span
            v-for="i in scene.left_count"
            :key="i"
            class="scene-emoji"
            :style="{ fontSize: emojiSize }"
          >{{ scene.left_emoji }}</span>
        </span>
      </span>
      <template v-else>
        <span class="split-side" :class="{ 'split-unknown': scene.left_count == null }">
          <span v-if="scene.left_count == null" class="split-q">？</span>
          <span
            v-for="i in scene.left_count"
            v-else
            :key="i"
            class="scene-emoji"
            :style="{ fontSize: emojiSize }"
          >{{ scene.left_emoji }}</span>
        </span>
        <span class="split-op">{{ scene.operator }}</span>
        <span class="split-side" :class="{ 'split-unknown': scene.right_count == null }">
          <span v-if="scene.right_count == null" class="split-q">？</span>
          <span
            v-for="i in scene.right_count"
            v-else
            :key="i"
            class="scene-emoji"
            :style="{ fontSize: emojiSize }"
          >{{ scene.right_emoji }}</span>
        </span>
      </template>
      <span class="split-op">=</span>
      <span class="split-side split-answer">
        <span class="split-q">{{ splitAnswer }}</span>
      </span>
    </div>
    <!-- shape：几何图形 SVG -->
    <div v-else-if="scene.type === 'shape'" class="scene-shape">
      <svg width="120" height="90" viewBox="0 0 120 90">
        <template v-if="scene.shape === '三角形'">
          <polygon :points="shapePoints.triangle" :fill="shapeFill" stroke="#409eff" stroke-width="2" />
        </template>
        <template v-else-if="scene.shape === '正方形'">
          <rect x="30" y="10" width="60" height="60" :fill="shapeFill" stroke="#409eff" stroke-width="2" />
        </template>
        <template v-else-if="scene.shape === '长方形'">
          <rect x="10" y="25" width="100" height="45" :fill="shapeFill" stroke="#409eff" stroke-width="2" />
        </template>
        <template v-else-if="scene.shape === '圆'">
          <circle cx="60" cy="40" r="32" :fill="shapeFill" stroke="#409eff" stroke-width="2" />
        </template>
        <template v-else-if="scene.shape === '正方体'">
          <g stroke="#409eff" stroke-width="2">
            <rect x="25" y="25" width="50" height="50" :fill="shapeFill" />
            <polygon points="75,25 95,10 95,60 75,75" fill="#a0cfff" />
            <polygon points="25,75 45,60 95,60 75,75" fill="#d9ecff" />
            <line x1="25" y1="25" x2="45" y2="10" />
            <line x1="45" y1="10" x2="95" y2="10" />
          </g>
        </template>
        <template v-else-if="scene.shape === '长方体'">
          <g stroke="#409eff" stroke-width="2">
            <rect x="10" y="30" width="70" height="40" :fill="shapeFill" />
            <polygon points="80,30 100,18 100,58 80,70" fill="#a0cfff" />
            <polygon points="10,70 30,58 100,58 80,70" fill="#d9ecff" />
            <line x1="10" y1="30" x2="30" y2="18" />
            <line x1="30" y1="18" x2="100" y2="18" />
          </g>
        </template>
        <template v-else-if="scene.shape === '圆柱'">
          <g stroke="#409eff" stroke-width="2">
            <ellipse cx="60" cy="22" rx="35" ry="10" :fill="shapeFill" />
            <rect x="25" y="22" width="70" height="45" :fill="shapeFill" />
            <ellipse cx="60" cy="67" rx="35" ry="10" fill="none" />
          </g>
        </template>
        <template v-else-if="scene.shape === '球'">
          <circle cx="60" cy="42" r="30" :fill="shapeFill" stroke="#409eff" stroke-width="2" />
        </template>
        <template v-else-if="scene.shape === '五角星'">
          <polygon :points="shapePoints.star" :fill="shapeFill" stroke="#409eff" stroke-width="2" />
        </template>
        <template v-else-if="scene.shape === '梯形'">
          <polygon :points="shapePoints.trapezoid" :fill="shapeFill" stroke="#409eff" stroke-width="2" />
        </template>
        <template v-else-if="scene.shape === '平行四边形'">
          <polygon :points="shapePoints.parallelogram" :fill="shapeFill" stroke="#409eff" stroke-width="2" />
        </template>
      </svg>
    </div>
    <div class="scene-label" v-if="scene.label && !['shape', 'count-split'].includes(scene.type)">{{ scene.label }}</div>
  </div>
</template>

<script setup>
import { computed } from 'vue'

const props = defineProps({
  scene: { type: Object, default: null },
  size: { type: String, default: '28px' },
})

const emojiSize = computed(() => props.size)

const shapeFill = '#d9ecff'

const shapePoints = {
  triangle: '60,8 100,80 20,80',
  star: '60,5 69,32 98,32 75,50 84,80 60,62 36,80 45,50 22,32 51,32',
  trapezoid: '25,70 95,70 80,25 40,25',
  parallelogram: '20,70 100,70 90,25 10,25',
}

// 图示算式的答案区显示：
// sum/remainder/mul_sum → ？填结果；addend_left/addend_right/minuend/subtrahend → 显示已知总数或结果
const splitAnswer = computed(() => {
  const s = props.scene
  if (!s) return ''
  if (s.unknown === 'sum' || s.unknown === 'remainder' || s.unknown === 'mul_sum') return '？'
  if (s.unknown === 'decompose') return '？'
  // 求未知加数/被减数/减数：右边是已知总数
  return s.max_count != null ? s.max_count : '？'
})
</script>

<style scoped>
.scene-visual {
  background: #f7faff;
  border: 1px dashed #c6d9f5;
  border-radius: 12px;
  padding: 14px 16px;
  margin: 12px 0 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  flex-wrap: wrap;
  min-height: 64px;
}
.scene-emoji {
  display: inline-block;
  margin: 2px 3px;
}
.scene-count {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
}
.scene-more {
  color: #909399;
  font-size: 18px;
  margin-left: 4px;
}
.scene-group {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: center;
}
.group-box {
  background: #fff;
  border: 2px solid #409eff;
  border-radius: 10px;
  padding: 8px 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  min-width: 48px;
}
.scene-shape {
  padding: 4px;
}
.scene-label {
  font-size: 13px;
  color: #909399;
  text-align: center;
}
/* count-split：图示算式（两堆物品 + 运算符 + 等号 + 问号） */
.scene-split {
  display: flex;
  align-items: center;
  gap: 10px;
  flex-wrap: wrap;
  justify-content: center;
  padding: 4px 0;
}
.split-side {
  display: inline-flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: center;
  gap: 2px;
  max-width: 220px;
  min-height: 44px;
  padding: 4px 6px;
  border-radius: 8px;
}
.split-box {
  margin: 0 2px;
}
.split-unknown {
  background: #fff7e6;
  border: 2px dashed #e6a23c;
}
.split-answer {
  background: #f0f9eb;
  border: 2px dashed #67c23a;
}
.split-q {
  font-size: 26px;
  font-weight: 700;
  color: #e6a23c;
  line-height: 1;
  padding: 0 6px;
}
.split-answer .split-q {
  color: #67c23a;
}
.split-op {
  font-size: 26px;
  font-weight: 700;
  color: #409eff;
  line-height: 1;
}
</style>
