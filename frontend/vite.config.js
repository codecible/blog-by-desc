import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  // 配置 Vite 插件
  plugins: [
    vue() // 提供 Vue 3 单文件组件支持
  ],
  
  // 开发服务器配置
  server: {
    port: 8001,        // 指定开发服务器端口
    host: true,        // 监听所有地址，包括局域网和公网地址
    
    // 代理配置，用于解决跨域问题
    proxy: {
      '/blog': {  // 匹配所有 /blog 开头的请求
        target: 'http://127.0.0.1:8000',  // 后端服务器地址
        changeOrigin: true,               // 修改请求头中的 Origin
        secure: false,                    // 支持 https
        ws: true,                         // 支持 websocket
        
        // 代理请求的详细配置
        configure: (proxy, options) => {
          // 错误处理
          proxy.on('error', (err, req, res) => {
            console.log('proxy error', err);
          });
          
          // 请求日志记录
          proxy.on('proxyReq', (proxyReq, req, res) => {
            console.log('Proxying:', req.method, req.url, '→', options.target + proxyReq.path);
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