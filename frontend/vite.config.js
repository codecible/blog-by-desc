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
        target: 'http://127.0.0.1:3001',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ''),
        configure: (proxy, options) => {
          proxy.on('error', (err, req, res) => {
            console.error('proxy error', err);
            if (!res.headersSent && res.writeHead) {
              res.writeHead(500, {
                'Content-Type': 'application/json'
              });
              res.end(JSON.stringify({ error: 'Proxy error', details: err.message }));
            }
          });
          proxy.on('proxyReq', (proxyReq, req, res) => {
            console.log('Sending Request to the Target:', req.method, req.url);
          });
          proxy.on('proxyRes', (proxyRes, req, res) => {
            console.log('Received Response from the Target:', proxyRes.statusCode, req.url);
          });
        },
        timeout: 300000,
        secure: false,
        ws: true,
        proxyTimeout: 300000,
      }
    }
  },

  build: {
    // 启用源码映射用于生产环境调试
    sourcemap: true,
    
    // CSS 代码分割
    cssCodeSplit: true,
    
    // 配置 Rollup 打包选项
    rollupOptions: {
      output: {
        // 手动配置代码分割
        manualChunks: {
          'vue-vendor': ['vue', '@vue/runtime-core', '@vue/runtime-dom', '@vue/reactivity'],
          'element-vendor': ['element-plus']
        }
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
        drop_debugger: true,
        pure_funcs: ['console.log']
      }
    }
  }
})