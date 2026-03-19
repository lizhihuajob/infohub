/**
 * 分类文章列表页
 */
<template>
  <div class="category-articles">
    <div class="page-header">
      <h2>分类: {{ category?.name || '加载中...' }}</h2>
      <p class="description" v-if="category?.description">{{ category.description }}</p>
    </div>

    <div class="article-list" v-if="articles.length">
      <ArticleCard
        v-for="article in articles"
        :key="article.id"
        :article="article"
      />
    </div>

    <el-empty v-else-if="!loading" description="该分类下暂无文章" />

    <div class="loading" v-if="loading">
      <el-icon class="is-loading"><Loading /></el-icon>
      <span>加载中...</span>
    </div>

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
import { ref, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/utils/api'
import ArticleCard from '@/components/ArticleCard.vue'

const route = useRoute()

const category = ref(null)
const articles = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const loading = ref(false)

const fetchCategory = async () => {
  try {
    const response = await api.get(`/categories/${route.params.id}/`)
    category.value = response
  } catch (error) {
    console.error('获取分类失败:', error)
  }
}

const fetchArticles = async () => {
  loading.value = true
  try {
    const response = await api.get('/articles/', {
      params: {
        page: currentPage.value,
        category: route.params.id
      }
    })
    articles.value = response.results || response
    total.value = response.count || articles.value.length
  } catch (error) {
    console.error('获取文章失败:', error)
  } finally {
    loading.value = false
  }
}

const handlePageChange = (page) => {
  currentPage.value = page
  fetchArticles()
  window.scrollTo({ top: 0, behavior: 'smooth' })
}

watch(() => route.params.id, () => {
  currentPage.value = 1
  fetchCategory()
  fetchArticles()
})

onMounted(() => {
  fetchCategory()
  fetchArticles()
})
</script>

<style scoped>
.category-articles {
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
  margin-bottom: 10px;
}

.description {
  color: #666;
  font-size: 14px;
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
