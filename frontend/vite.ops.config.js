import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// 运营后台独立构建：root=ops/（入口 ops/index.html）→ dist-ops 产物，后端 mount /ops
export default defineConfig({
  plugins: [vue()],
  root: 'ops',
  base: '/ops/',
  build: {
    outDir: '../dist-ops',
    emptyOutDir: true,
  },
})
