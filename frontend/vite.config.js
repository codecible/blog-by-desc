import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 3000,
    host: true,
    proxy: {
      '/blog': {
        target: 'http://localhost:8000',
        changeOrigin: true
      }
    }
  }
}) 