<template>
  <!--
    分类列表页
    展示所有文章分类
  -->
  <div class="category-list-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>文章分类</h1>
      <p>按分类浏览文章</p>
    </div>
    
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <el-skeleton :rows="3" animated />
    </div>
    
    <!-- 分类列表 -->
    <div v-else-if="categories.length > 0" class="categories-grid">
      <div
        v-for="category in categories"
        :key="category.id"
        class="category-card"
        @click="goToCategory(category.slug)"
      >
        <el-icon :size="40" class="category-icon"><FolderOpened /></el-icon>
        <h3 class="category-name">{{ category.name }}</h3>
        <p class="category-description">{{ category.description || '暂无描述' }}</p>
        <div class="category-meta">
          <el-tag size="small" type="info">
            {{ getPostCount(category.slug) }} 篇文章
          </el-tag>
        </div>
      </div>
    </div>
    
    <!-- 空状态 -->
    <el-empty v-else description="暂无分类" />
  </div>
</template>

<script setup>
/**
 * 分类列表页组件
 * 
 * 功能：
 * - 展示所有文章分类
 * - 点击分类可查看该分类下的文章
 */
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { FolderOpened } from '@element-plus/icons-vue'
import { getCategories, getPosts } from '@/api/blog'

// 路由实例
const router = useRouter()

// 响应式数据
const categories = ref([])      // 分类列表
const categoryCounts = ref({})  // 分类文章数量
const loading = ref(false)      // 加载状态

/**
 * 获取分类列表
 */
const fetchCategories = async () => {
  loading.value = true
  try {
    categories.value = await getCategories()
    // 获取每个分类的文章数量
    await fetchCategoryCounts()
  } catch (error) {
    console.error('获取分类失败:', error)
  } finally {
    loading.value = false
  }
}

/**
 * 获取各分类的文章数量
 */
const fetchCategoryCounts = async () => {
  for (const category of categories.value) {
    try {
      const response = await getPosts({ category: category.slug })
      categoryCounts.value[category.slug] = response.count || 0
    } catch (error) {
      categoryCounts.value[category.slug] = 0
    }
  }
}

/**
 * 获取分类文章数量
 */
const getPostCount = (slug) => {
  return categoryCounts.value[slug] || 0
}

/**
 * 跳转到分类文章列表
 */
const goToCategory = (slug) => {
  router.push({
    path: '/posts',
    query: { category: slug }
  })
}

// 组件挂载时获取数据
onMounted(() => {
  fetchCategories()
})
</script>

<style scoped>
.category-list-page {
  padding: 20px 0;
}

.page-header {
  text-align: center;
  margin-bottom: 40px;
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

.loading-state {
  padding: 40px;
  background-color: #fff;
  border-radius: 8px;
}

.categories-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 20px;
}

.category-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 30px;
  text-align: center;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  cursor: pointer;
  transition: transform 0.3s, box-shadow 0.3s;
}

.category-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.category-icon {
  color: #409eff;
  margin-bottom: 15px;
}

.category-name {
  font-size: 20px;
  color: #303133;
  margin: 0 0 10px 0;
}

.category-description {
  color: #606266;
  font-size: 14px;
  margin-bottom: 15px;
  min-height: 40px;
}

.category-meta {
  margin-top: 15px;
}
</style>
