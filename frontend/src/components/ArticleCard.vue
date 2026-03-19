/**
 * 文章卡片组件
 */
<template>
  <div class="article-card" @click="goToDetail">
    <!-- 封面图片 -->
    <div class="cover" v-if="article.cover_image">
      <img :src="article.cover_image" :alt="article.title" />
    </div>

    <!-- 文章信息 -->
    <div class="article-info">
      <h3 class="title">
        <el-tag v-if="article.is_top" type="danger" size="small" style="margin-right: 8px;">置顶</el-tag>
        {{ article.title }}
      </h3>

      <p class="summary">{{ article.summary || '暂无摘要' }}</p>

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
        <span class="category" v-if="article.category_name">
          <el-icon><Folder /></el-icon>
          {{ article.category_name }}
        </span>
      </div>

      <div class="tags" v-if="article.tags_list && article.tags_list.length">
        <el-tag
          v-for="tag in article.tags_list"
          :key="tag.id"
          size="small"
          type="info"
        >
          {{ tag.name }}
        </el-tag>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

const props = defineProps({
  article: {
    type: Object,
    required: true
  }
})

const router = useRouter()

// 跳转到文章详情
const goToDetail = () => {
  router.push(`/article/${props.article.id}`)
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
</script>

<style scoped>
.article-card {
  background: #fff;
  border-radius: 8px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s;
  border: 1px solid #eee;
}

.article-card:hover {
  transform: translateY(-3px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.cover {
  width: 100%;
  height: 200px;
  overflow: hidden;
}

.cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.article-card:hover .cover img {
  transform: scale(1.05);
}

.article-info {
  padding: 20px;
}

.title {
  font-size: 18px;
  font-weight: bold;
  color: #333;
  margin-bottom: 10px;
  display: flex;
  align-items: center;
}

.summary {
  color: #666;
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 15px;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.meta {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  color: #999;
  font-size: 12px;
  margin-bottom: 10px;
}

.meta span {
  display: flex;
  align-items: center;
  gap: 4px;
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}
</style>
