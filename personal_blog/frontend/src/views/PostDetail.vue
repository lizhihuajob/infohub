<template>
  <!--
    文章详情页
    展示单篇文章的完整内容
  -->
  <div class="post-detail-page">
    <!-- 加载状态 -->
    <div v-if="loading" class="loading-state">
      <el-skeleton :rows="10" animated />
    </div>
    
    <!-- 文章内容 -->
    <article v-else-if="post" class="post-article">
      <!-- 文章头部 -->
      <header class="post-header">
        <!-- 置顶标识 -->
        <el-tag v-if="post.is_top" type="danger" class="top-tag">置顶</el-tag>
        
        <!-- 标题 -->
        <h1 class="post-title">{{ post.title }}</h1>
        
        <!-- 元信息 -->
        <div class="post-meta">
          <span class="meta-item">
            <el-icon><User /></el-icon>
            {{ post.author_name }}
          </span>
          <span v-if="post.category" class="meta-item">
            <el-icon><Folder /></el-icon>
            {{ post.category.name }}
          </span>
          <span class="meta-item">
            <el-icon><Clock /></el-icon>
            {{ formatDate(post.published_at || post.created_at) }}
          </span>
          <span class="meta-item">
            <el-icon><View /></el-icon>
            {{ post.views }} 次阅读
          </span>
        </div>
        
        <!-- 标签 -->
        <div v-if="post.tags && post.tags.length > 0" class="post-tags">
          <el-tag
            v-for="tag in post.tags"
            :key="tag.id"
            size="small"
            effect="plain"
          >
            {{ tag.name }}
          </el-tag>
        </div>
      </header>
      
      <!-- 封面图 -->
      <div v-if="post.cover_image" class="post-cover">
        <img :src="post.cover_image" :alt="post.title" />
      </div>
      
      <!-- 文章内容 -->
      <div class="post-content" v-html="renderedContent"></div>
      
      <!-- 文章底部 -->
      <footer class="post-footer">
        <el-divider />
        <div class="post-nav">
          <router-link to="/posts">
            <el-button type="primary" link>
              <el-icon><ArrowLeft /></el-icon>
              返回文章列表
            </el-button>
          </router-link>
        </div>
      </footer>
    </article>
    
    <!-- 文章不存在 -->
    <el-empty v-else description="文章不存在或已被删除" />
  </div>
</template>

<script setup>
/**
 * 文章详情页组件
 * 
 * 功能：
 * - 展示单篇文章的完整内容
 * - 支持 Markdown 渲染
 * - 显示文章元信息和标签
 */
import { ref, onMounted, computed } from 'vue'
import { useRoute } from 'vue-router'
import { User, Folder, Clock, View, ArrowLeft } from '@element-plus/icons-vue'
import { getPostDetail } from '@/api/blog'
import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js'
import 'highlight.js/styles/github.css'

// 路由实例
const route = useRoute()

// 响应式数据
const post = ref(null)      // 文章数据
const loading = ref(false)  // 加载状态

// 创建 Markdown 渲染器
const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
  highlight: function (str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(str, { language: lang }).value
      } catch (__) {}
    }
    return ''
  }
})

// 渲染后的内容
const renderedContent = computed(() => {
  if (!post.value?.content) return ''
  return md.render(post.value.content)
})

/**
 * 获取文章详情
 */
const fetchPostDetail = async () => {
  const slug = route.params.slug
  if (!slug) return
  
  loading.value = true
  try {
    post.value = await getPostDetail(slug)
  } catch (error) {
    console.error('获取文章详情失败:', error)
  } finally {
    loading.value = false
  }
}

/**
 * 格式化日期
 */
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: 'long',
    day: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 组件挂载时获取数据
onMounted(() => {
  fetchPostDetail()
})
</script>

<style scoped>
.post-detail-page {
  padding: 20px 0;
}

.loading-state {
  padding: 40px;
  background-color: #fff;
  border-radius: 8px;
}

.post-article {
  background-color: #fff;
  border-radius: 8px;
  padding: 40px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.post-header {
  margin-bottom: 30px;
}

.top-tag {
  margin-bottom: 15px;
}

.post-title {
  font-size: 32px;
  line-height: 1.4;
  color: #303133;
  margin: 0 0 20px 0;
}

.post-meta {
  display: flex;
  flex-wrap: wrap;
  gap: 20px;
  margin-bottom: 15px;
  color: #909399;
  font-size: 14px;
}

.meta-item {
  display: flex;
  align-items: center;
  gap: 5px;
}

.post-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.post-cover {
  margin-bottom: 30px;
  border-radius: 8px;
  overflow: hidden;
}

.post-cover img {
  width: 100%;
  height: auto;
  display: block;
}

.post-content {
  font-size: 16px;
  line-height: 1.8;
  color: #303133;
}

.post-content :deep(h1),
.post-content :deep(h2),
.post-content :deep(h3),
.post-content :deep(h4),
.post-content :deep(h5),
.post-content :deep(h6) {
  margin-top: 30px;
  margin-bottom: 15px;
  color: #303133;
}

.post-content :deep(p) {
  margin-bottom: 16px;
}

.post-content :deep(code) {
  background-color: #f5f7fa;
  padding: 2px 6px;
  border-radius: 3px;
  font-family: 'Courier New', monospace;
}

.post-content :deep(pre) {
  background-color: #f5f7fa;
  padding: 16px;
  border-radius: 8px;
  overflow-x: auto;
  margin-bottom: 16px;
}

.post-content :deep(pre code) {
  background-color: transparent;
  padding: 0;
}

.post-content :deep(blockquote) {
  border-left: 4px solid #409eff;
  padding-left: 16px;
  margin-left: 0;
  color: #606266;
}

.post-content :deep(ul),
.post-content :deep(ol) {
  margin-bottom: 16px;
  padding-left: 24px;
}

.post-content :deep(li) {
  margin-bottom: 8px;
}

.post-content :deep(img) {
  max-width: 100%;
  height: auto;
  border-radius: 4px;
}

.post-content :deep(table) {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 16px;
}

.post-content :deep(th),
.post-content :deep(td) {
  border: 1px solid #e4e7ed;
  padding: 12px;
  text-align: left;
}

.post-content :deep(th) {
  background-color: #f5f7fa;
}

.post-footer {
  margin-top: 40px;
}

.post-nav {
  display: flex;
  justify-content: center;
}
</style>
