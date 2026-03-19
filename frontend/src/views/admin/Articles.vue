/**
 * 文章管理页面
 */
<template>
  <div class="articles-page">
    <div class="page-header">
      <h2>文章管理</h2>
      <router-link to="/admin/articles/create">
        <el-button type="primary">
          <el-icon><Plus /></el-icon>
          新建文章
        </el-button>
      </router-link>
    </div>

    <!-- 搜索和筛选 -->
    <div class="filter-bar">
      <el-input
        v-model="searchKeyword"
        placeholder="搜索文章标题..."
        clearable
        style="width: 300px;"
        @keyup.enter="handleSearch"
      >
        <template #append>
          <el-button @click="handleSearch">
            <el-icon><Search /></el-icon>
          </el-button>
        </template>
      </el-input>

      <el-select v-model="statusFilter" placeholder="状态筛选" clearable @change="fetchArticles">
        <el-option label="全部" value="" />
        <el-option label="已发布" value="published" />
        <el-option label="草稿" value="draft" />
      </el-select>
    </div>

    <!-- 文章列表 -->
    <el-table :data="articles" style="width: 100%" v-loading="loading">
      <el-table-column prop="title" label="标题" min-width="200" />
      <el-table-column prop="category_name" label="分类" width="120" />
      <el-table-column prop="status" label="状态" width="100">
        <template #default="{ row }">
          <el-tag :type="row.status === 'published' ? 'success' : 'info'">
            {{ row.status === 'published' ? '已发布' : '草稿' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="is_top" label="置顶" width="80">
        <template #default="{ row }">
          <el-tag v-if="row.is_top" type="danger">置顶</el-tag>
        </template>
      </el-table-column>
      <el-table-column prop="view_count" label="阅读量" width="100" />
      <el-table-column prop="created_at" label="创建时间" width="180">
        <template #default="{ row }">
          {{ formatDate(row.created_at) }}
        </template>
      </el-table-column>
      <el-table-column label="操作" width="200" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" size="small" @click="editArticle(row.id)">
            编辑
          </el-button>
          <el-button
            :type="row.status === 'published' ? 'warning' : 'success'"
            size="small"
            @click="toggleStatus(row)"
          >
            {{ row.status === 'published' ? '取消发布' : '发布' }}
          </el-button>
          <el-button type="danger" size="small" @click="deleteArticle(row)">
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
import { useRouter } from 'vue-router'
import api from '@/utils/api'
import { ElMessage, ElMessageBox } from 'element-plus'

const router = useRouter()

const articles = ref([])
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)
const loading = ref(false)
const searchKeyword = ref('')
const statusFilter = ref('')

const fetchArticles = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      search: searchKeyword.value
    }
    if (statusFilter.value) {
      params.status = statusFilter.value
    }
    const response = await api.get('/articles/', { params })
    articles.value = response.results || response
    total.value = response.count || 0
  } catch (error) {
    console.error('获取文章列表失败:', error)
  } finally {
    loading.value = false
  }
}

const handleSearch = () => {
  currentPage.value = 1
  fetchArticles()
}

const handlePageChange = (page) => {
  currentPage.value = page
  fetchArticles()
}

const editArticle = (id) => {
  router.push(`/admin/articles/${id}/edit`)
}

const toggleStatus = async (article) => {
  try {
    const action = article.status === 'published' ? 'unpublish' : 'publish'
    await api.post(`/articles/${article.id}/${action}/`)
    ElMessage.success(article.status === 'published' ? '已取消发布' : '已发布')
    fetchArticles()
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const deleteArticle = async (article) => {
  try {
    await ElMessageBox.confirm('确定要删除这篇文章吗？', '提示', {
      type: 'warning'
    })
    await api.delete(`/articles/${article.id}/`)
    ElMessage.success('删除成功')
    fetchArticles()
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
    day: '2-digit'
  })
}

onMounted(() => {
  fetchArticles()
})
</script>

<style scoped>
.articles-page {
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
  display: flex;
  gap: 15px;
  margin-bottom: 20px;
}

.pagination {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
