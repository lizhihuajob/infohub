<template>
  <!--
    管理后台布局组件
    提供管理后台的整体布局结构
  -->
  <div class="admin-layout">
    <!-- 侧边栏 -->
    <aside class="admin-sidebar">
      <div class="sidebar-header">
        <h3>管理后台</h3>
      </div>
      
      <el-menu
        :default-active="$route.path"
        router
        class="admin-menu"
        background-color="#304156"
        text-color="#bfcbd9"
        active-text-color="#409eff"
      >
        <el-menu-item index="/admin">
          <el-icon><Odometer /></el-icon>
          <span>仪表盘</span>
        </el-menu-item>
        
        <el-sub-menu index="/admin/posts">
          <template #title>
            <el-icon><Document /></el-icon>
            <span>文章管理</span>
          </template>
          <el-menu-item index="/admin/posts">文章列表</el-menu-item>
          <el-menu-item index="/admin/posts/create">创建文章</el-menu-item>
        </el-sub-menu>
        
        <el-menu-item index="/admin/categories">
          <el-icon><Folder /></el-icon>
          <span>分类管理</span>
        </el-menu-item>
        
        <el-menu-item index="/admin/tags">
          <el-icon><CollectionTag /></el-icon>
          <span>标签管理</span>
        </el-menu-item>
      </el-menu>
      
      <!-- 返回前台 -->
      <div class="sidebar-footer">
        <router-link to="/">
          <el-button type="info" link>
            <el-icon><HomeFilled /></el-icon>
            返回前台
          </el-button>
        </router-link>
      </div>
    </aside>
    
    <!-- 主内容区 -->
    <main class="admin-main">
      <!-- 顶部栏 -->
      <header class="admin-header">
        <div class="breadcrumb">
          <el-breadcrumb>
            <el-breadcrumb-item>管理后台</el-breadcrumb-item>
            <el-breadcrumb-item>{{ $route.meta.title }}</el-breadcrumb-item>
          </el-breadcrumb>
        </div>
        <div class="header-actions">
          <el-button type="danger" link @click="handleLogout">
            <el-icon><SwitchButton /></el-icon>
            退出登录
          </el-button>
        </div>
      </header>
      
      <!-- 内容区 -->
      <div class="admin-content">
        <router-view />
      </div>
    </main>
  </div>
</template>

<script setup>
/**
 * 管理后台布局组件
 *
 * 功能：
 * - 提供侧边栏导航
 * - 提供顶部栏（面包屑、退出登录）
 * - 包含管理后台的所有子路由
 */
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import {
  Odometer,
  Document,
  Folder,
  CollectionTag,
  HomeFilled,
  SwitchButton
} from '@element-plus/icons-vue'

// 路由实例
const router = useRouter()

/**
 * 处理退出登录
 */
const handleLogout = async () => {
  try {
    await ElMessageBox.confirm('确定要退出登录吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })

    // 清除登录状态
    localStorage.removeItem('token')
    ElMessage.success('已退出登录')

    // 跳转到登录页
    router.push('/login')
  } catch {
    // 用户取消
  }
}
</script>

<style scoped>
.admin-layout {
  display: flex;
  min-height: 100vh;
}

.admin-sidebar {
  width: 210px;
  background-color: #304156;
  position: fixed;
  height: 100vh;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 20px;
  text-align: center;
  border-bottom: 1px solid #1f2d3d;
}

.sidebar-header h3 {
  color: #fff;
  margin: 0;
  font-size: 18px;
}

.admin-menu {
  flex: 1;
  border-right: none;
}

.sidebar-footer {
  padding: 20px;
  border-top: 1px solid #1f2d3d;
  text-align: center;
}

.admin-main {
  flex: 1;
  margin-left: 210px;
  background-color: #f0f2f5;
  min-height: 100vh;
}

.admin-header {
  background-color: #fff;
  padding: 0 20px;
  height: 50px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 1px 4px rgba(0, 0, 0, 0.1);
}

.admin-content {
  padding: 20px;
}
</style>
