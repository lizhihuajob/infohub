<template>
  <div class="post-detail">
    <router-link to="/" class="back-link">← 返回列表</router-link>
    
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else class="post-content">
      <h1 class="post-title">{{ post.title }}</h1>
      <div class="post-meta">
        <span class="author">作者: {{ post.author }}</span>
        <span class="date">发布时间: {{ post.created_time }}</span>
        <span class="views">浏览: {{ post.views }}次</span>
      </div>
      <div class="post-body">
        <p v-for="(paragraph, index) in post.content.split('\n')" :key="index">
          {{ paragraph }}
        </p>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { getPost } from '../api/posts'

const route = useRoute()
const post = ref({})
const loading = ref(true)
const error = ref('')

onMounted(async () => {
  try {
    const response = await getPost(route.params.id)
    post.value = response.data
    loading.value = false
  } catch (err) {
    error.value = '加载文章失败，请稍后重试'
    loading.value = false
    console.error(err)
  }
})
</script>

<style scoped>
.post-detail {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.back-link {
  display: inline-block;
  color: #3498db;
  text-decoration: none;
  margin-bottom: 20px;
  font-weight: 500;
  transition: color 0.2s;
}

.back-link:hover {
  color: #2980b9;
}

.post-content {
  background: #fff;
  border-radius: 8px;
  padding: 30px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.post-title {
  font-size: 2rem;
  color: #2c3e50;
  margin: 0 0 20px 0;
  line-height: 1.3;
}

.post-meta {
  font-size: 0.95rem;
  color: #7f8c8d;
  margin-bottom: 30px;
  padding-bottom: 20px;
  border-bottom: 1px solid #eee;
  display: flex;
  gap: 20px;
  flex-wrap: wrap;
}

.post-body {
  color: #444;
  line-height: 1.8;
  font-size: 1.05rem;
}

.post-body p {
  margin-bottom: 15px;
  text-indent: 2em;
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