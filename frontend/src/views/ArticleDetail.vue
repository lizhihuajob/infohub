/**
 * 文章详情页组件
 */
<template>
  <div class="article-detail">
    <!-- 加载中 -->
    <div class="loading" v-if="loading">
      <el-icon class="is-loading"><Loading /></el-icon>
      <span>加载中...</span>
    </div>

    <!-- 文章内容 -->
    <div class="article-content" v-else-if="article">
      <!-- 文章标题 -->
      <h1 class="title">
        <el-tag v-if="article.is_top" type="danger" size="small" style="margin-right: 8px;">置顶</el-tag>
        {{ article.title }}
      </h1>

      <!-- 文章元信息 -->
      <div class="meta">
        <span class="author">
          <el-icon><User /></el-icon>
          {{ article.author_name }}
        </span>
        <span class="date">
          <el-icon><Calendar /></el-icon>
          {{ formatDate(article.created_at) }}
        </span>
        <span class="views">
          <el-icon><View /></el-icon>
          {{ article.view_count }} 阅读
        </span>
        <span class="category" v-if="article.category">
          <el-icon><Folder /></el-icon>
          {{ article.category.name }}
        </span>
      </div>

      <!-- 封面图片 -->
      <div class="cover" v-if="article.cover_image">
        <img :src="article.cover_image" :alt="article.title" />
      </div>

      <!-- 文章摘要 -->
      <div class="summary" v-if="article.summary">
        <strong>摘要：</strong>{{ article.summary }}
      </div>

      <!-- 文章正文 -->
      <div class="content" v-html="article.content"></div>

      <!-- 标签 -->
      <div class="tags" v-if="article.tags && article.tags.length">
        <span class="label">标签：</span>
        <el-tag
          v-for="tag in article.tags"
          :key="tag.id"
          type="info"
        >
          {{ tag.name }}
        </el-tag>
      </div>
    </div>

    <!-- 空状态 -->
    <el-empty v-else description="文章不存在或已删除" />

    <!-- 评论区 -->
    <div class="comments-section" v-if="article">
      <CommentSection :article-id="article.id" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import api from '@/utils/api'
import CommentSection from '@/components/CommentSection.vue'

const route = useRoute()

// 文章数据
const article = ref(null)
// 加载状态
const loading = ref(false)

// 获取文章详情
const fetchArticle = async () => {
  loading.value = true
  try {
    const response = await api.get(`/articles/${route.params.id}/`)
    article.value = response
  } catch (error) {
    console.error('获取文章详情失败:', error)
  } finally {
    loading.value = false
  }
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit'
  })
}

onMounted(() => {
  fetchArticle()
})
</script>

<style scoped>
.article-detail {
  background: #fff;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 10px;
  padding: 40px;
  color: #999;
}

.title {
  font-size: 28px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.meta {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  color: #999;
  font-size: 14px;
  margin-bottom: 20px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
}

.meta span {
  display: flex;
  align-items: center;
  gap: 5px;
}

.cover {
  margin-bottom: 20px;
  border-radius: 8px;
  overflow: hidden;
}

.cover img {
  width: 100%;
  display: block;
}

.summary {
  background: #f5f5f5;
  padding: 15px;
  border-radius: 8px;
  margin-bottom: 20px;
  color: #666;
  line-height: 1.6;
}

.content {
  line-height: 1.8;
  color: #333;
  margin-bottom: 30px;
}

.content :deep(p) {
  margin-bottom: 15px;
}

.content :deep(h1),
.content :deep(h2),
.content :deep(h3) {
  margin: 20px 0 10px;
}

.content :deep(img) {
  max-width: 100%;
  border-radius: 4px;
}

.tags {
  display: flex;
  align-items: center;
  gap: 10px;
  padding-top: 20px;
  border-top: 1px solid #eee;
}

.tags .label {
  color: #666;
}

.comments-section {
  margin-top: 30px;
  padding-top: 30px;
  border-top: 1px solid #eee;
}
</style>
