/**
 * 首页组件 - 展示文章列表
 */
<template>
  <div class="home-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2>最新文章</h2>
    </div>

    <!-- 搜索框 -->
    <div class="search-box">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索文章..."
        clearable
        @keyup.enter="handleSearch"
      >
        <template #append>
          <el-button @click="handleSearch">
            <el-icon><Search /></el-icon>
          </el-button>
        </template>
      </el-input>
    </div>

    <!-- 文章列表 -->
    <div class="article-list" v-if="articles.length">
      <ArticleCard
        v-for="article in articles"
        :key="article.id"
        :article="article"
      />
    </div>

    <!-- 空状态 -->
    <el-empty v-else-if="!loading" description="暂无文章" />

    <!-- 加载中 -->
    <div class="loading" v-if="loading">
      <el-icon class="is-loading"><Loading /></el-icon>
      <span>加载中...</span>
    </div>

    <!-- 分页 -->
    <div class="pagination" v-if="total > pageSize">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        layout="prev, pager, next"
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/utils/api'
import ArticleCard from '@/components/ArticleCard.vue'

// 文章列表
const articles = ref([])
// 当前页码
const currentPage = ref(1)
// 每页数量
const pageSize = ref(10)
// 总数量
const total = ref(0)
// 搜索关键词
const searchKeyword = ref('')
// 加载状态
const loading = ref(false)

// 获取文章列表
const fetchArticles = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      search: searchKeyword.value
    }
    const response = await api.get('/articles/', { params })
    articles.value = response.results || response
    total.value = response.count || articles.value.length
  } catch (error) {
    console.error('获取文章列表失败:', error)
  } finally {
    loading.value = false
  }
}

// 搜索处理
const handleSearch = () => {
  currentPage.value = 1
  fetchArticles()
}

// 分页处理
const handlePageChange = (page) => {
  currentPage.value = page
  fetchArticles()
  // 滚动到顶部
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

onMounted(() => {
  fetchArticles()
})
</script>

<style scoped>
.home-page {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.page-header {
  margin-bottom: 20px;
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.page-header h2 {
  font-size: 20px;
  color: #333;
}

.search-box {
  margin-bottom: 20px;
}

.article-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 40px;
  color: #999;
}

.pagination {
  margin-top: 30px;
  display: flex;
  justify-content: center;
}
</style>
