/**
 * Vue 应用入口文件
 * 初始化 Vue 应用并挂载到 DOM
 */

import { createApp } from 'vue'
import { createPinia } from 'pinia'
import ElementPlus from 'element-plus'
import * as ElementPlusIconsVue from '@element-plus/icons-vue'
import 'element-plus/dist/index.css'

import App from './App.vue'
import router from './router'

// 创建 Vue 应用实例
const app = createApp(App)

// 注册所有 Element Plus 图标
for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component)
}

// 使用插件
app.use(createPinia())  // 状态管理
app.use(router)         // 路由
app.use(ElementPlus)    // UI 组件库

// 挂载应用到 DOM
app.mount('#app')
