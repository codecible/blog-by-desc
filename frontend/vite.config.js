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
    
    // CSS 代码分割
    cssCodeSplit: true,
    
    // 配置 Rollup 打包选项
    rollupOptions: {
      output: {
        // 手动配置代码分割
        manualChunks(id) {
          // node_modules 依赖包分割
          if (id.includes('node_modules')) {
            // vue相关包
            if (id.includes('vue') || id.includes('pinia')) {
              return 'vendor-vue'
            }
            // UI组件库
            if (id.includes('element-plus') || id.includes('@element-plus')) {
              return 'vendor-element'
            }
            // 工具库
            if (id.includes('lodash') || id.includes('axios') || id.includes('moment')) {
              return 'vendor-utils'
            }
            // 其他第三方库
            return 'vendor-others'
          }
          // 根据文件路径分割业务代码
          if (id.includes('src/')) {
            if (id.includes('/components/')) {
              return 'components'
            }
            if (id.includes('/views/')) {
              return 'views'
            }
            if (id.includes('/store/')) {
              return 'store'
            }
          }
        },
        // 配置chunk文件名格式
        chunkFileNames: 'assets/js/[name]-[hash].js',
        // 配置入口文件名格式
        entryFileNames: 'assets/js/[name]-[hash].js',
        // 配置资源文件名格式
        assetFileNames: (assetInfo) => {
          const info = assetInfo.name.split('.')
          let extType = info[info.length - 1]
          if (/\.(mp4|webm|ogg|mp3|wav|flac|aac)(\?.*)?$/i.test(assetInfo.name)) {
            extType = 'media'
          } else if (/\.(png|jpe?g|gif|svg|ico|webp)(\?.*)?$/i.test(assetInfo.name)) {
            extType = 'img'
          } else if (/\.(woff2?|eot|ttf|otf)(\?.*)?$/i.test(assetInfo.name)) {
            extType = 'fonts'
          }
          return `assets/${extType}/[name]-[hash][extname]`
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