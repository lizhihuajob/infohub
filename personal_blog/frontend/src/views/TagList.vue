<template>
  <!--
    标签列表页
    展示所有文章标签
  -->
  <div class="tag-list-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h1>文章标签</h1>
      <p>以标签云形式浏览所有标签</p>
    </div>
    
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <el-skeleton :rows="3" animated />
    </div>
    
    <!-- 标签云 -->
    <div v-else-if="tags.length > 0" class="tags-cloud">
      <div
        v-for="tag in tags"
        :key="tag.id"
        class="tag-item"
        :style="getTagStyle(tag)"
        @click="goToTag(tag.slug)"
      >
        <el-tag
          :type="getTagType(tag)"
          effect="light"
          size="large"
          class="tag-button"
        >
          {{ tag.name }}
          <span class="tag-count">({{ getPostCount(tag.slug) }})</span>
        </el-tag>
      </div>
    </div>
    
    <!-- 空状态 -->
    <el-empty v-else description="暂无标签" />
  </div>
</template>

<script setup>
/**
 * 标签列表页组件
 * 
 * 功能：
 * - 以标签云形式展示所有标签
 * - 标签大小根据文章数量变化
 * - 点击标签可查看该标签下的文章
 */
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { getTags, getPosts } from '@/api/blog'

// 路由实例
const router = useRouter()

// 响应式数据
const tags = ref([])            // 标签列表
const tagCounts = ref({})       // 标签文章数量
const loading = ref(false)      // 加载状态
const maxCount = ref(0)         // 最大文章数（用于计算标签大小）

/**
 * 获取标签列表
 */
const fetchTags = async () => {
  loading.value = true
  try {
    tags.value = await getTags()
    // 获取每个标签的文章数量
    await fetchTagCounts()
  } catch (error) {
    console.error('获取标签失败:', error)
  } finally {
    loading.value = false
  }
}

/**
 * 获取各标签的文章数量
 */
const fetchTagCounts = async () => {
  let max = 0
  for (const tag of tags.value) {
    try {
      const response = await getPosts({ tag: tag.slug })
      const count = response.count || 0
      tagCounts.value[tag.slug] = count
      if (count > max) {
        max = count
      }
    } catch (error) {
      tagCounts.value[tag.slug] = 0
    }
  }
  maxCount.value = max
}

/**
 * 获取标签文章数量
 */
const getPostCount = (slug) => {
  return tagCounts.value[slug] || 0
}

/**
 * 获取标签样式（根据文章数量调整大小）
 */
const getTagStyle = (tag) => {
  const count = getPostCount(tag.slug)
  const ratio = maxCount.value > 0 ? count / maxCount.value : 0
  
  // 根据比例计算字体大小
  const fontSize = 14 + ratio * 10  // 14px 到 24px
  
  return {
    fontSize: `${fontSize}px`
  }
}

/**
 * 获取标签类型（根据文章数量）
 */
const getTagType = (tag) => {
  const count = getPostCount(tag.slug)
  if (count >= 10) return 'danger'
  if (count >= 5) return 'warning'
  if (count >= 2) return 'success'
  return 'info'
}

/**
 * 跳转到标签文章列表
 */
const goToTag = (slug) => {
  router.push({
    path: '/posts',
    query: { tag: slug }
  })
}

// 组件挂载时获取数据
onMounted(() => {
  fetchTags()
})
</script>

<style scoped>
.tag-list-page {
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

.tags-cloud {
  background-color: #fff;
  border-radius: 8px;
  padding: 40px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 15px;
}

.tag-item {
  cursor: pointer;
  transition: transform 0.3s;
}

.tag-item:hover {
  transform: scale(1.1);
}

.tag-button {
  cursor: pointer;
}

.tag-count {
  margin-left: 4px;
  opacity: 0.7;
}
</style>
