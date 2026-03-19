<template>
  <!--
    首页
    展示博客概览和最新文章
  -->
  <div class="home-page">
    <!-- 欢迎区域 -->
    <section class="hero-section">
      <h1>欢迎来到我的个人博客</h1>
      <p>分享技术、记录生活、沉淀思考</p>
    </section>
    
    <!-- 统计信息 -->
    <section class="stats-section" v-if="stats">
      <el-row :gutter="20">
        <el-col :span="6">
          <div class="stat-card">
            <el-icon :size="32"><Document /></el-icon>
            <div class="stat-number">{{ stats.total_posts }}</div>
            <div class="stat-label">文章</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <el-icon :size="32"><Folder /></el-icon>
            <div class="stat-number">{{ stats.total_categories }}</div>
            <div class="stat-label">分类</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <el-icon :size="32"><CollectionTag /></el-icon>
            <div class="stat-number">{{ stats.total_tags }}</div>
            <div class="stat-label">标签</div>
          </div>
        </el-col>
        <el-col :span="6">
          <div class="stat-card">
            <el-icon :size="32"><View /></el-icon>
            <div class="stat-number">{{ stats.total_views }}</div>
            <div class="stat-label">阅读</div>
          </div>
        </el-col>
      </el-row>
    </section>
    
    <!-- 最新文章 -->
    <section class="latest-posts">
      <div class="section-header">
        <h2>最新文章</h2>
        <router-link to="/posts">
          <el-button type="primary" link>查看更多</el-button>
        </router-link>
      </div>
      
      <!-- 加载状态 -->
      <div v-if="loading" class="loading-state">
        <el-skeleton :rows="3" animated />
      </div>
      
      <!-- 文章列表 -->
      <div v-else-if="posts.length > 0" class="posts-list">
        <PostCard v-for="post in posts" :key="post.id" :post="post" />
      </div>
      
      <!-- 空状态 -->
      <el-empty v-else description="暂无文章" />
    </section>
  </div>
</template>

<script setup>
/**
 * 首页组件
 * 
 * 功能：
 * - 展示博客欢迎信息
 * - 显示博客统计数据（文章数、分类数、标签数、阅读数）
 * - 展示最新文章列表
 */
import { ref, onMounted } from 'vue'
import { Document, Folder, CollectionTag, View } from '@element-plus/icons-vue'
import { getPosts, getBlogStats } from '@/api/blog'
import PostCard from '@/components/PostCard.vue'

// 响应式数据
const posts = ref([])       // 文章列表
const stats = ref(null)     // 统计数据
const loading = ref(false)  // 加载状态

/**
 * 获取最新文章
 */
const fetchLatestPosts = async () => {
  loading.value = true
  try {
    const response = await getPosts({ page: 1 })
    // 只取前 5 篇文章
    posts.value = response.results?.slice(0, 5) || []
  } catch (error) {
    console.error('获取文章失败:', error)
  } finally {
    loading.value = false
  }
}

/**
 * 获取统计数据
 */
const fetchStats = async () => {
  try {
    stats.value = await getBlogStats()
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

// 组件挂载时获取数据
onMounted(() => {
  fetchLatestPosts()
  fetchStats()
})
</script>

<style scoped>
.home-page {
  padding: 20px 0;
}

.hero-section {
  text-align: center;
  padding: 60px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: 12px;
  color: #fff;
  margin-bottom: 40px;
}

.hero-section h1 {
  font-size: 36px;
  margin-bottom: 16px;
}

.hero-section p {
  font-size: 18px;
  opacity: 0.9;
}

.stats-section {
  margin-bottom: 40px;
}

.stat-card {
  background-color: #fff;
  padding: 30px;
  border-radius: 8px;
  text-align: center;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s;
}

.stat-card:hover {
  transform: translateY(-4px);
}

.stat-card .el-icon {
  color: #409eff;
  margin-bottom: 10px;
}

.stat-number {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.latest-posts {
  background-color: #fff;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #e4e7ed;
}

.section-header h2 {
  margin: 0;
  font-size: 24px;
  color: #303133;
}

.loading-state {
  padding: 20px;
}
</style>
