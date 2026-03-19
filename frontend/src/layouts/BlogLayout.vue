/**
 * 博客前台布局组件
 */
<template>
  <div class="blog-layout">
    <!-- 顶部导航栏 -->
    <header class="blog-header">
      <div class="container">
        <div class="header-content">
          <h1 class="logo">
            <router-link to="/">我的博客</router-link>
          </h1>
          <nav class="nav-menu">
            <router-link to="/" class="nav-item">首页</router-link>
            <router-link to="/admin" class="nav-item">管理后台</router-link>
          </nav>
        </div>
      </div>
    </header>

    <!-- 主内容区域 -->
    <main class="blog-main">
      <div class="container">
        <div class="main-content">
          <!-- 左侧内容区 -->
          <div class="content-area">
            <router-view />
          </div>
          <!-- 右侧边栏 -->
          <aside class="sidebar">
            <Sidebar />
          </aside>
        </div>
      </div>
    </main>

    <!-- 底部信息 -->
    <footer class="blog-footer">
      <div class="container">
        <p>&copy; 2024 我的博客. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
import Sidebar from '@/components/Sidebar.vue'
</script>

<style scoped>
.blog-layout {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.blog-header {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 60px;
}

.logo a {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
}

.nav-menu {
  display: flex;
  gap: 20px;
}

.nav-item {
  padding: 8px 16px;
  color: #333;
  border-radius: 4px;
  transition: all 0.3s;
}

.nav-item:hover,
.nav-item.router-link-active {
  background: #409eff;
  color: #fff;
}

.blog-main {
  flex: 1;
  padding: 30px 0;
}

.main-content {
  display: flex;
  gap: 30px;
}

.content-area {
  flex: 1;
  min-width: 0;
}

.sidebar {
  width: 300px;
  flex-shrink: 0;
}

.blog-footer {
  background: #333;
  color: #fff;
  padding: 20px 0;
  text-align: center;
}

@media (max-width: 768px) {
  .main-content {
    flex-direction: column;
  }

  .sidebar {
    width: 100%;
  }
}
</style>
