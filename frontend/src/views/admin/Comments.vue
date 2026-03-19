/**
 * 评论管理页面
 */
<template>
  <div class="comments-page">
    <div class="page-header">
      <h2>评论管理</h2>
    </div>

    <!-- 筛选 -->
    <div class="filter-bar">
      <el-select v-model="visibilityFilter" placeholder="显示状态" clearable @change="fetchComments">
        <el-option label="全部" value="" />
        <el-option label="已显示" :value="true" />
        <el-option label="已隐藏" :value="false" />
      </el-select>
    </div>

    <!-- 评论列表 -->
    <el-table :data="comments" style="width: 100%" v-loading="loading">
      <el-table-column prop="nickname" label="昵称" width="120" />
      <el-table-column prop="article" label="所属文章" width="150">
        <template #default="{ row }">
          文章ID: {{ row.article }}
        </template>
      </el-table-column>
      <el-table-column prop="content" label="评论内容" min-width="200">
        <template #default="{ row }">
          <div class="comment-content">{{ row.content }}</div>
        </template>
      </el-table-column>
      <el-table-column prop="is_visible" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.is_visible ? 'success' : 'info'">
            {{ row.is_visible ? '已显示' : '已隐藏' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="created_at" label="评论时间" width="180">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="150">
        <template #default="{ row }">
          <el-button
            :type="row.is_visible ? 'warning' : 'success'"
            size="small"
            @click="toggleVisibility(row)"
          >
            {{ row.is_visible ? '隐藏' : '显示' }}
          </el-button>
          <el-button type="danger" size="small" @click="deleteComment(row)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>

    <!-- 分页 -->
    <div class="pagination">
      <el-pagination
        v-model:current-page="currentPage"
        :page-size="pageSize"
        :total="total"
        layout="total, prev, pager, next"
        @current-change="handlePageChange"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/utils/api'
import { ElMessage, ElMessageBox } from 'element-plus'

const comments = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const loading = ref(false)
const visibilityFilter = ref('')

const fetchComments = async () => {
  loading.value = true
  try {
    const params = { page: currentPage.value }
    if (visibilityFilter.value !== '') {
      params.is_visible = visibilityFilter.value
    }
    const response = await api.get('/comments/', { params })
    comments.value = response.results || response
    total.value = response.count || 0
  } catch (error) {
    console.error('获取评论失败:', error)
  } finally {
    loading.value = false
  }
}

const handlePageChange = (page) => {
  currentPage.value = page
  fetchComments()
}

const toggleVisibility = async (comment) => {
  try {
    await api.patch(`/comments/${comment.id}/`, {
      is_visible: !comment.is_visible
    })
    ElMessage.success(comment.is_visible ? '已隐藏' : '已显示')
    fetchComments()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const deleteComment = async (comment) => {
  try {
    await ElMessageBox.confirm('确定要删除该评论吗？', '提示', {
      type: 'warning'
    })
    await api.delete(`/comments/${comment.id}/`)
    ElMessage.success('删除成功')
    fetchComments()
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败')
    }
  }
}

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
  fetchComments()
})
</script>

<style scoped>
.comments-page {
  background: #fff;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  font-size: 20px;
  color: #333;
}

.filter-bar {
  margin-bottom: 20px;
}

.comment-content {
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
