<template>
  <!--
    导航栏组件
    提供全站导航功能
  -->
  <nav class="navbar">
    <div class="nav-container">
      <!-- 网站 Logo/名称 -->
      <router-link to="/" class="nav-brand">
        <el-icon :size="24"><Document /></el-icon>
        <span>个人博客</span>
      </router-link>
      
      <!-- 导航菜单 -->
      <div class="nav-menu">
        <router-link to="/" class="nav-item" :class="{ active: $route.path === '/' }">
          首页
        </router-link>
        <router-link to="/posts" class="nav-item" :class="{ active: $route.path.startsWith('/posts') }">
          文章
        </router-link>
        <router-link to="/categories" class="nav-item" :class="{ active: $route.path === '/categories' }">
          分类
        </router-link>
        <router-link to="/tags" class="nav-item" :class="{ active: $route.path === '/tags' }">
          标签
        </router-link>
      </div>
      
      <!-- 右侧操作区 -->
      <div class="nav-actions">
        <router-link to="/admin" class="admin-link">
          <el-button type="primary" size="small">
            <el-icon><Setting /></el-icon>
            管理
          </el-button>
        </router-link>
      </div>
    </div>
  </nav>
</template>

<script setup>
/**
 * 导航栏组件
 * 
 * 功能：
 * - 显示网站 Logo 和名称
 * - 提供主导航链接
 * - 提供管理后台入口
 */
import { Document, Setting } from '@element-plus/icons-vue'
</script>

<style scoped>
.navbar {
  background-color: #fff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 0 20px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.nav-brand {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 20px;
  font-weight: bold;
  color: #409eff;
  text-decoration: none;
}

.nav-menu {
  display: flex;
  gap: 30px;
}

.nav-item {
  text-decoration: none;
  color: #606266;
  font-size: 16px;
  padding: 8px 0;
  position: relative;
  transition: color 0.3s;
}

.nav-item:hover,
.nav-item.active {
  color: #409eff;
}

.nav-item.active::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  right: 0;
  height: 2px;
  background-color: #409eff;
}

.nav-actions {
  display: flex;
  align-items: center;
  gap: 15px;
}

.admin-link {
  text-decoration: none;
}
</style>
