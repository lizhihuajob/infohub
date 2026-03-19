<template>
  <!--
    根组件
    包含全局布局和路由视图
  -->
  <div id="app">
    <!-- 导航栏组件 -->
    <NavBar />
    
    <!-- 主内容区域 -->
    <main class="main-content">
      <!-- 路由视图，根据当前路由显示不同页面 -->
      <router-view />
    </main>
    
    <!-- 页脚组件 -->
    <Footer />
  </div>
</template>

<script setup>
/**
 * 根组件脚本
 * 
 * 导入全局使用的子组件
 */
import NavBar from './components/NavBar.vue'
import Footer from './components/Footer.vue'
</script>

<style>
/**
 * 全局样式
 */

/* 重置默认样式 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

/* 页面基础样式 */
body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 
               'Helvetica Neue', Arial, sans-serif;
  line-height: 1.6;
  color: #333;
  background-color: #f5f5f5;
}

/* 应用容器 */
#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

/* 主内容区域 */
.main-content {
  flex: 1;
  padding: 20px;
  max-width: 1200px;
  margin: 0 auto;
  width: 100%;
}

/* 链接样式 */
a {
  text-decoration: none;
  color: inherit;
}

/* 图片响应式 */
img {
  max-width: 100%;
  height: auto;
}
</style>
