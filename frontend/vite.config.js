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
    // 禁用源码映射
    sourcemap: false,
    
    // 禁用代码分割
    cssCodeSplit: false,
    
    // 配置 Rollup 打包选项
    rollupOptions: {
      output: {
        // 禁用代码分割，将所有代码打包到一起
        manualChunks: undefined
      }
    },
    
    // 禁用压缩
    minify: false
  }
})