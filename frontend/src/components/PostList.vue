<template>
  <div class="post-list">
    <h1 class="page-title">博客文章</h1>
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <div v-for="post in posts" :key="post.id" class="post-card">
        <h2 class="post-title">
          <router-link :to="`/posts/${post.id}`">{{ post.title }}</router-link>
        </h2>
        <div class="post-meta">
          <span class="author">作者: {{ post.author }}</span>
          <span class="date">发布时间: {{ post.created_time }}</span>
          <span class="views">浏览: {{ post.views }}次</span>
        </div>
        <p class="post-excerpt">{{ post.content.substring(0, 200) }}...</p>
        <router-link :to="`/posts/${post.id}`" class="read-more">阅读全文 →</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { getPosts } from '../api/posts'

const posts = ref([])
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const response = await getPosts()
    posts.value = response.data
    loading.value = false
  } catch (err) {
    error.value = '加载文章失败，请稍后重试'
    loading.value = false
    console.error(err)
  }
})
</script>

<style scoped>
.post-list {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.page-title {
  font-size: 2rem;
  color: #333;
  margin-bottom: 30px;
  text-align: center;
}

.post-card {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: transform 0.2s, box-shadow 0.2s;
}

.post-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.post-title {
  font-size: 1.5rem;
  margin: 0 0 10px 0;
}

.post-title a {
  color: #2c3e50;
  text-decoration: none;
  transition: color 0.2s;
}

.post-title a:hover {
  color: #3498db;
}

.post-meta {
  font-size: 0.9rem;
  color: #7f8c8d;
  margin-bottom: 15px;
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.post-excerpt {
  color: #555;
  line-height: 1.6;
  margin-bottom: 15px;
}

.read-more {
  color: #3498db;
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.read-more:hover {
  color: #2980b9;
}

.loading,
.error {
  text-align: center;
  padding: 40px;
  font-size: 1.1rem;
}

.error {
  color: #e74c3c;
}
</style>