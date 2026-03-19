<template>
  <!--
    文章列表页
    展示所有已发布的文章，支持搜索和筛选
  -->
  <div class="post-list-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>文章列表</h1>
      <p>探索所有精彩文章</p>
    </div>
    
    <!-- 搜索和筛选 -->
    <div class="filter-section">
      <el-input
        v-model="searchQuery"
        placeholder="搜索文章..."
        clearable
        @keyup.enter="handleSearch"
        class="search-input"
      >
        <template #prefix>
          <el-icon><Search /></el-icon>
        </template>
        <template #append>
          <el-button @click="handleSearch">搜索</el-button>
        </template>
      </el-input>
    </div>
    
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <el-skeleton :rows="5" animated />
    </div>
    
    <!-- 文章列表 -->
    <div v-else-if="posts.length > 0" class="posts-container">
      <PostCard v-for="post in posts" :key="post.id" :post="post" />
    </div>
    
    <!-- 空状态 -->
    <el-empty v-else description="暂无文章" />
    
    <!-- 分页 -->
    <div v-if="total > pageSize" class="pagination-wrapper">
      <el-pagination
        v-model:current-page="currentPage"
        v-model:page-size="pageSize"
        :total="total"
        :page-sizes="[10, 20, 50]"
        layout="total, sizes, prev, pager, next"
        @size-change="handleSizeChange"
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script setup>
/**
 * 文章列表页组件
 * 
 * 功能：
 * - 展示所有已发布文章
 * - 支持关键词搜索
 * - 支持分页浏览
 */
import { ref, onMounted, watch } from 'vue'
import { Search } from '@element-plus/icons-vue'
import { getPosts } from '@/api/blog'
import PostCard from '@/components/PostCard.vue'

// 响应式数据
const posts = ref([])           // 文章列表
const loading = ref(false)      // 加载状态
const searchQuery = ref('')     // 搜索关键词
const currentPage = ref(1)      // 当前页码
const pageSize = ref(10)        // 每页数量
const total = ref(0)            // 总文章数

/**
 * 获取文章列表
 */
const fetchPosts = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      // 注意：Django REST Framework 使用 page_size 参数
      page_size: pageSize.value
    }
    
    // 如果有搜索关键词，添加到参数
    if (searchQuery.value.trim()) {
      params.search = searchQuery.value.trim()
    }
    
    const response = await getPosts(params)
    posts.value = response.results || []
    total.value = response.count || 0
  } catch (error) {
    console.error('获取文章失败:', error)
  } finally {
    loading.value = false
  }
}

/**
 * 处理搜索
 */
const handleSearch = () => {
  currentPage.value = 1  // 重置到第一页
  fetchPosts()
}

/**
 * 处理页码变化
 */
const handlePageChange = (page) => {
  currentPage.value = page
  fetchPosts()
  // 滚动到页面顶部
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

/**
 * 处理每页数量变化
 */
const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  fetchPosts()
}

// 组件挂载时获取数据
onMounted(() => {
  fetchPosts()
})
</script>

<style scoped>
.post-list-page {
  padding: 20px 0;
}

.page-header {
  text-align: center;
  margin-bottom: 30px;
}

.page-header h1 {
  font-size: 32px;
  color: #303133;
  margin-bottom: 10px;
}

.page-header p {
  color: #909399;
  font-size: 16px;
}

.filter-section {
  margin-bottom: 30px;
  display: flex;
  justify-content: center;
}

.search-input {
  max-width: 500px;
  width: 100%;
}

.loading-state {
  padding: 40px;
  background-color: #fff;
  border-radius: 8px;
}

.posts-container {
  margin-bottom: 30px;
}

.pagination-wrapper {
  display: flex;
  justify-content: center;
  padding: 20px;
  background-color: #fff;
  border-radius: 8px;
}
</style>
