<template>
  <!--
    管理后台仪表盘
    展示博客的整体统计数据和快捷操作
  -->
  <div class="admin-dashboard">
    <!-- 统计卡片 -->
    <el-row :gutter="20" class="stats-row">
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-icon" style="background-color: #409eff;">
            <el-icon :size="32" color="#fff"><Document /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.total_posts || 0 }}</div>
            <div class="stat-label">已发布文章</div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-icon" style="background-color: #67c23a;">
            <el-icon :size="32" color="#fff"><Folder /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.total_categories || 0 }}</div>
            <div class="stat-label">分类数量</div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-icon" style="background-color: #e6a23c;">
            <el-icon :size="32" color="#fff"><CollectionTag /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.total_tags || 0 }}</div>
            <div class="stat-label">标签数量</div>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="6">
        <el-card class="stat-card">
          <div class="stat-icon" style="background-color: #f56c6c;">
            <el-icon :size="32" color="#fff"><View /></el-icon>
          </div>
          <div class="stat-info">
            <div class="stat-value">{{ stats.total_views || 0 }}</div>
            <div class="stat-label">总阅读量</div>
          </div>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 快捷操作 -->
    <el-row :gutter="20" class="actions-row">
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>快捷操作</span>
          </template>
          <div class="quick-actions">
            <router-link to="/admin/posts/create">
              <el-button type="primary" size="large">
                <el-icon><Plus /></el-icon>
                创建新文章
              </el-button>
            </router-link>
            <router-link to="/admin/posts">
              <el-button type="success" size="large">
                <el-icon><List /></el-icon>
                管理文章
              </el-button>
            </router-link>
            <router-link to="/admin/categories">
              <el-button type="warning" size="large">
                <el-icon><Folder /></el-icon>
                管理分类
              </el-button>
            </router-link>
            <router-link to="/admin/tags">
              <el-button type="info" size="large">
                <el-icon><CollectionTag /></el-icon>
                管理标签
              </el-button>
            </router-link>
          </div>
        </el-card>
      </el-col>
      
      <el-col :span="12">
        <el-card>
          <template #header>
            <span>系统信息</span>
          </template>
          <div class="system-info">
            <div class="info-item">
              <span class="info-label">前端框架：</span>
              <span class="info-value">Vue 3 + Element Plus</span>
            </div>
            <div class="info-item">
              <span class="info-label">后端框架：</span>
              <span class="info-value">Django + Django REST Framework</span>
            </div>
            <div class="info-item">
              <span class="info-label">数据库：</span>
              <span class="info-value">SQLite</span>
            </div>
            <div class="info-item">
              <span class="info-label">部署方式：</span>
              <span class="info-value">Docker</span>
            </div>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
/**
 * 管理后台仪表盘组件
 *
 * 功能：
 * - 展示博客统计数据
 * - 提供快捷操作入口
 * - 显示系统信息
 */
import { ref, onMounted } from 'vue'
import {
  Document,
  Folder,
  CollectionTag,
  View,
  Plus,
  List
} from '@element-plus/icons-vue'
import { getBlogStats } from '@/api/blog'

// 响应式数据
const stats = ref({})

/**
 * 获取统计数据
 */
const fetchStats = async () => {
  try {
    stats.value = await getBlogStats()
  } catch (error) {
    console.error('获取统计数据失败:', error)
  }
}

// 组件挂载时获取数据
onMounted(() => {
  fetchStats()
})
</script>

<style scoped>
.admin-dashboard {
  padding: 20px 0;
}

.stats-row {
  margin-bottom: 20px;
}

.stat-card {
  display: flex;
  align-items: center;
  padding: 10px;
}

.stat-icon {
  width: 64px;
  height: 64px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 15px;
}

.stat-info {
  flex: 1;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
  line-height: 1;
  margin-bottom: 5px;
}

.stat-label {
  font-size: 14px;
  color: #909399;
}

.actions-row {
  margin-top: 20px;
}

.quick-actions {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.quick-actions a {
  text-decoration: none;
}

.system-info {
  line-height: 2;
}

.info-item {
  display: flex;
  padding: 8px 0;
  border-bottom: 1px solid #ebeef5;
}

.info-item:last-child {
  border-bottom: none;
}

.info-label {
  color: #909399;
  width: 100px;
  flex-shrink: 0;
}

.info-value {
  color: #606266;
  font-weight: 500;
}
</style>
