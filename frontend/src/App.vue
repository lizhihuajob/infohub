<template>
  <div class="app">
    <header class="header">
      <div class="container">
        <div class="header-content">
          <router-link to="/" class="logo">我的博客</router-link>
          <nav class="nav">
            <router-link to="/" class="nav-link">首页</router-link>
            <a href="/admin/" target="_blank" class="nav-link">Django管理</a>
            <router-link to="/admin/login" class="nav-link">管理员登录</router-link>
          </nav>
        </div>
      </div>
    </header>
    
    <main class="main">
      <router-view />
    </main>
    
    <footer class="footer">
      <div class="container">
        <p>&copy; 2024 我的博客. All rights reserved.</p>
      </div>
    </footer>
  </div>
</template>

<script setup>
</script>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  line-height: 1.6;
  color: #333;
  background-color: #f5f5f5;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
}

/* 头部样式 */
.header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  padding: 20px 0;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

.header-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.logo {
  font-size: 1.8rem;
  font-weight: 700;
  color: #fff;
  text-decoration: none;
  transition: opacity 0.2s;
}

.logo:hover {
  opacity: 0.9;
}

.nav {
  display: flex;
  gap: 30px;
}

.nav-link {
  color: #fff;
  text-decoration: none;
  font-weight: 500;
  font-size: 1rem;
  transition: opacity 0.2s;
}

.nav-link:hover {
  opacity: 0.8;
}

/* 主要内容区域 */
.main {
  min-height: calc(100vh - 140px);
  padding: 30px 0;
}

/* 底部样式 */
.footer {
  background: #2c3e50;
  color: #ecf0f1;
  padding: 30px 0;
  text-align: center;
}

.footer p {
  margin: 0;
  font-size: 0.9rem;
}

/* 响应式设计 */
@media (max-width: 768px) {
  .header-content {
    flex-direction: column;
    gap: 15px;
  }
  
  .nav {
    gap: 20px;
  }
  
  .logo {
    font-size: 1.5rem;
  }
}
</style>