/**
 * Vite 配置文件
 * 定义项目的构建和开发服务器配置
 */

import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import { resolve } from 'path'

// https://vitejs.dev/config/
export default defineConfig({
  // 注册插件
  plugins: [vue()],
  
  // 路径别名配置
  resolve: {
    alias: {
      // @ 指向 src 目录
      '@': resolve(__dirname, 'src'),
    },
  },
  
  // 开发服务器配置
  server: {
    // 监听所有网络接口
    host: '0.0.0.0',
    // 开发服务器端口
    port: 5173,
    // 严格端口，如果被占用则报错
    strictPort: true,
    // 启用热更新
    hmr: {
      // HMR 客户端端口
      clientPort: 5173,
    },
    // 代理配置
    proxy: {
      // 将 /api 开头的请求代理到后端服务
      // 后端 API 路径格式: /api/blog/...
      '/api': {
        target: 'http://backend:8000',
        changeOrigin: true,
      },
    },
  },
  
  // 构建配置
  build: {
    // 输出目录
    outDir: 'dist',
    // 生成 source map
    sourcemap: true,
  },
})
