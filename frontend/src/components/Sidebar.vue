/**
 * 侧边栏组件 - 显示分类、标签等信息
 */
<template>
  <div class="sidebar-wrapper">
    <!-- 分类列表 -->
    <div class="sidebar-section">
      <h3 class="section-title">文章分类</h3>
      <div class="category-list" v-if="categories.length">
        <router-link
          v-for="category in categories"
          :key="category.id"
          :to="`/category/${category.id}`"
          class="category-item"
        >
          <span class="name">{{ category.name }}</span>
          <span class="count">{{ category.article_count }}</span>
        </router-link>
      </div>
      <el-empty v-else description="暂无分类" :image-size="60" />
    </div>

    <!-- 标签云 -->
    <div class="sidebar-section">
      <h3 class="section-title">标签云</h3>
      <div class="tag-cloud" v-if="tags.length">
        <router-link
          v-for="tag in tags"
          :key="tag.id"
          :to="`/tag/${tag.id}`"
          class="tag-item"
        >
          {{ tag.name }}
        </router-link>
      </div>
      <el-empty v-else description="暂无标签" :image-size="60" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/utils/api'

// 分类列表
const categories = ref([])
// 标签列表
const tags = ref([])

// 获取分类列表
const fetchCategories = async () => {
  try {
    const response = await api.get('/categories/')
    categories.value = response.results || response
  } catch (error) {
    console.error('获取分类失败:', error)
  }
}

// 获取标签列表
const fetchTags = async () => {
  try {
    const response = await api.get('/tags/')
    tags.value = response.results || response
  } catch (error) {
    console.error('获取标签失败:', error)
  }
}

onMounted(() => {
  fetchCategories()
  fetchTags()
})
</script>

<style scoped>
.sidebar-wrapper {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.sidebar-section {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.section-title {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 15px;
  padding-bottom: 10px;
  border-bottom: 2px solid #409eff;
}

.category-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.category-item {
  display: flex;
  justify-content: space-between;
  padding: 8px 12px;
  background: #f5f5f5;
  border-radius: 4px;
  transition: all 0.3s;
}

.category-item:hover {
  background: #409eff;
  color: #fff;
}

.category-item .count {
  background: rgba(0, 0, 0, 0.1);
  padding: 2px 8px;
  border-radius: 10px;
  font-size: 12px;
}

.tag-cloud {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-item {
  display: inline-block;
  padding: 4px 12px;
  background: #f0f0f0;
  border-radius: 4px;
  font-size: 12px;
  color: #666;
  transition: all 0.3s;
}

.tag-item:hover {
  background: #409eff;
  color: #fff;
}
</style>
