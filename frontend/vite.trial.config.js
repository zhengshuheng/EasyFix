import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import path from 'path'

// 试用版前端构建：部署在 /{trial_key}/ 下（见 backend/app/main.py 的 trial_spa 路由）
// - base='./'：index.html 与 JS 内资源引用使用相对路径，适配任意 /{key}/ 前缀
// - VITE_TRIAL=true：路由切 hash 模式（router/index.js 据此选择）
// - outDir=dist-trial：与正式 dist 分开，互不影响
// 构建：npm run build:trial（package.json scripts）
export default defineConfig({
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src'),
    },
  },
  base: './',
  define: {
    'import.meta.env.VITE_TRIAL': '"true"',
  },
  build: {
    outDir: 'dist-trial',
    emptyOutDir: true,
  },
})
