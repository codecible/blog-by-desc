import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    port: 8001,
    host: true,
    proxy: {
      '/blog': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        secure: false,
        ws: true,
        configure: (proxy, options) => {
          // 打印代理请求日志，方便调试
          proxy.on('error', (err, req, res) => {
            console.log('proxy error', err);
          });
          proxy.on('proxyReq', (proxyReq, req, res) => {
            console.log('Proxying:', req.method, req.url, '→', options.target + proxyReq.path);
            // 打印请求头和请求体
            console.log('Headers:', proxyReq.getHeaders());
            if (req.body) {
              console.log('Body:', req.body);
            }
          });
        }
      }
    }
  }
})