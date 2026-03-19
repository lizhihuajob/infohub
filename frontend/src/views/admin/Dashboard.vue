/**
 * 管理后台仪表盘
 */
<template>
  <div class="dashboard">
    <h2 class="page-title">仪表盘</h2>

    <!-- 统计卡片 -->
    <div class="stats-cards">
      <div class="stat-card">
        <div class="stat-icon" style="background: #409eff;">
          <el-icon><Document /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.article_count }}</div>
          <div class="stat-label">文章总数</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon" style="background: #67c23a;">
          <el-icon><Folder /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.category_count }}</div>
          <div class="stat-label">分类数量</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon" style="background: #e6a23c;">
          <el-icon><PriceTag /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.tag_count }}</div>
          <div class="stat-label">标签数量</div>
        </div>
      </div>

      <div class="stat-card">
        <div class="stat-icon" style="background: #f56c6c;">
          <el-icon><ChatDotRound /></el-icon>
        </div>
        <div class="stat-info">
          <div class="stat-value">{{ stats.comment_count }}</div>
          <div class="stat-label">评论数量</div>
        </div>
      </div>
    </div>

    <!-- 快捷操作 -->
    <div class="quick-actions">
      <h3>快捷操作</h3>
      <div class="action-buttons">
        <router-link to="/admin/articles/create">
          <el-button type="primary">
            <el-icon><Plus /></el-icon>
            新建文章
          </el-button>
        </router-link>
        <router-link to="/admin/categories">
          <el-button type="success">
            <el-icon><Folder /></el-icon>
            管理分类
          </el-button>
        </router-link>
        <router-link to="/admin/tags">
          <el-button type="warning">
            <el-icon><PriceTag /></el-icon>
            管理标签
          </el-button>
        </router-link>
        <router-link to="/admin/comments">
          <el-button type="info">
            <el-icon><ChatDotRound /></el-icon>
            管理评论
          </el-button>
        </router-link>
      </div>
    </div>

    <!-- 最近文章 -->
    <div class="recent-articles">
      <h3>最近文章</h3>
      <el-table :data="recentArticles" style="width: 100%">
        <el-table-column prop="title" label="标题" />
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'published' ? 'success' : 'info'">
              {{ row.status === 'published' ? '已发布' : '草稿' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="view_count" label="阅读量" width="100" />
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/utils/api'

// 统计数据
const stats = ref({
  article_count: 0,
  category_count: 0,
  tag_count: 0,
  comment_count: 0
})

// 最近文章
const recentArticles = ref([])

// 获取统计数据
const fetchStats = async () => {
  try {
    // 并行获取各模块数据
    const [articlesRes, categoriesRes, tagsRes, commentsRes] = await Promise.all([
      api.get('/articles/'),
      api.get('/categories/'),
      api.get('/tags/'),
      api.get('/comments/')
    ])

    stats.value = {
      article_count: articlesRes.count || 0,
      category_count: categoriesRes.count || 0,
      tag_count: tagsRes.count || 0,
      comment_count: commentsRes.count || 0
    }

    // 获取最近5篇文章
    recentArticles.value = (articlesRes.results || articlesRes).slice(0, 5)
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

// 格式化日期
const formatDate = (dateStr) => {
  if (!dateStr) return ''
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

onMounted(() => {
  fetchStats()
})
</script>

<style scoped>
.dashboard {
  padding: 20px;
}

.page-title {
  font-size: 24px;
  margin-bottom: 20px;
  color: #333;
}

.stats-cards {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 20px;
  margin-bottom: 30px;
}

.stat-card {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  display: flex;
  align-items: center;
  gap: 15px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.stat-icon {
  width: 60px;
  height: 60px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #fff;
  font-size: 28px;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #333;
}

.stat-label {
  color: #999;
  font-size: 14px;
  margin-top: 5px;
}

.quick-actions {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  margin-bottom: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.quick-actions h3 {
  margin-bottom: 15px;
  color: #333;
}

.action-buttons {
  display: flex;
  gap: 15px;
  flex-wrap: wrap;
}

.recent-articles {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.recent-articles h3 {
  margin-bottom: 15px;
  color: #333;
}
</style>
