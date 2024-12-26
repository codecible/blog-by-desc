import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [
    vue()
  ],
  
  server: {
    port: 3000,
    host: true,
    proxy: {
      '/api': {
        target: 'http://backend:3001',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
        configure: (proxy, options) => {
          proxy.on('error', (err, req, res) => {
            console.error('proxy error', err);
          });
          proxy.on('proxyReq', (proxyReq, req, res) => {
            console.log('Sending Request to the Target:', req.method, req.url);
          });
          proxy.on('proxyRes', (proxyRes, req, res) => {
            console.log('Received Response from the Target:', proxyRes.statusCode, req.url);
          });
        },
        timeout: 5000,
        secure: false,
        ws: true
      }
    }
  },

  build: {
    // 启用源码映射用于生产环境调试
    sourcemap: true,
    
    // 配置 Rollup 打包选项
    rollupOptions: {
      output: {
        // 手动配置代码分割
        manualChunks: {
          // 将 Vue 相关库打包到一个chunk
          'vue-vendor': ['vue', 'vue-router', 'pinia'],
          // 将其他第三方库打包到另一个chunk
          'vendor': ['axios', 'lodash', 'moment'],
        },
        // 配置chunk文件名格式
        chunkFileNames: 'assets/[name]-[hash].js',
        // 配置入口文件名格式
        entryFileNames: 'assets/[name]-[hash].js',
        // 配置资源文件名格式
        assetFileNames: 'assets/[name]-[hash][extname]'
      }
    },
    
    // 配置chunk大小警告限制
    chunkSizeWarningLimit: 800,
    
    // 压缩配置
    minify: 'terser',
    terserOptions: {
      compress: {
        // 生产环境移除console
        drop_console: true,
        drop_debugger: true
      }
    }
  }
})