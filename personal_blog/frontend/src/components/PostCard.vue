<template>
  <!--
    文章卡片组件
    在文章列表中展示单篇文章的摘要信息
  -->
  <div class="post-card" :class="{ 'is-top': post.is_top }">
    <!-- 置顶标识 -->
    <div v-if="post.is_top" class="top-badge">
      <el-tag type="danger" size="small">置顶</el-tag>
    </div>
    
    <!-- 文章封面 -->
    <div v-if="post.cover_image" class="post-cover">
      <img :src="post.cover_image" :alt="post.title" />
    </div>
    
    <!-- 文章内容 -->
    <div class="post-content">
      <!-- 标题 -->
      <h3 class="post-title">
        <router-link :to="`/posts/${post.slug}`">
          {{ post.title }}
        </router-link>
      </h3>
      
      <!-- 摘要 -->
      <p class="post-summary">{{ post.summary || '暂无摘要' }}</p>
      
      <!-- 元信息 -->
      <div class="post-meta">
        <!-- 作者 -->
        <span class="meta-item">
          <el-icon><User /></el-icon>
          {{ post.author_name }}
        </span>
        
        <!-- 分类 -->
        <span v-if="post.category_name" class="meta-item">
          <el-icon><Folder /></el-icon>
          {{ post.category_name }}
        </span>
        
        <!-- 发布时间 -->
        <span class="meta-item">
          <el-icon><Clock /></el-icon>
          {{ formatDate(post.published_at || post.created_at) }}
        </span>
        
        <!-- 浏览次数 -->
        <span class="meta-item">
          <el-icon><View /></el-icon>
          {{ post.views }} 次阅读
        </span>
      </div>
      
      <!-- 标签 -->
      <div v-if="post.tag_list && post.tag_list.length > 0" class="post-tags">
        <el-tag
          v-for="tag in post.tag_list"
          :key="tag.id"
          size="small"
          effect="plain"
          class="tag-item"
        >
          {{ tag.name }}
        </el-tag>
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * 文章卡片组件
 * 
 * 功能：
 * - 展示文章标题、摘要、封面
 * - 显示作者、分类、发布时间、浏览次数等元信息
 * - 显示文章标签
 * - 支持置顶标识
 * 
 * Props:
 *   post: 文章数据对象
 */
import { User, Folder, Clock, View } from '@element-plus/icons-vue'

// 定义组件属性
const props = defineProps({
  post: {
    type: Object,
    required: true
  }
})

/**
 * 格式化日期
 * 
 * @param {string} dateString - ISO 格式的日期字符串
 * @returns {string} 格式化后的日期字符串
 */
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}
</script>

<style scoped>
.post-card {
  background-color: #fff;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
  position: relative;
}

.post-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.post-card.is-top {
  border-left: 4px solid #f56c6c;
}

.top-badge {
  position: absolute;
  top: 10px;
  right: 10px;
}

.post-cover {
  width: 100%;
  height: 200px;
  overflow: hidden;
  border-radius: 4px;
  margin-bottom: 15px;
}

.post-cover img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s;
}

.post-cover:hover img {
  transform: scale(1.05);
}

.post-title {
  margin: 0 0 10px 0;
  font-size: 20px;
  line-height: 1.4;
}

.post-title a {
  color: #303133;
  text-decoration: none;
  transition: color 0.3s;
}

.post-title a:hover {
  color: #409eff;
}

.post-summary {
  color: #606266;
  font-size: 14px;
  line-height: 1.6;
  margin-bottom: 15px;
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.post-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  margin-bottom: 10px;
  font-size: 13px;
  color: #909399;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 4px;
}

.post-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.tag-item {
  cursor: pointer;
}
</style>
