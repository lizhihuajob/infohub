<template>
  <!--
    文章管理列表页
    管理员查看和管理所有文章（包括草稿）
  -->
  <div class="admin-post-list">
    <!-- 页面标题和操作栏 -->
    <div class="page-header">
      <h2>文章管理</h2>
      <div class="header-actions">
        <el-input
          v-model="searchQuery"
          placeholder="搜索文章..."
          clearable
          style="width: 250px; margin-right: 10px;"
          @keyup.enter="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-select
          v-model="statusFilter"
          placeholder="筛选状态"
          clearable
          style="width: 150px; margin-right: 10px;"
          @change="handleFilterChange"
        >
          <el-option label="全部" value="" />
          <el-option label="已发布" value="published" />
          <el-option label="草稿" value="draft" />
        </el-select>
        <router-link to="/admin/posts/create">
          <el-button type="primary">
            <el-icon><Plus /></el-icon>
            创建文章
          </el-button>
        </router-link>
      </div>
    </div>
    
    <!-- 文章列表表格 -->
    <el-card>
      <el-table
        v-loading="loading"
        :data="posts"
        stripe
        style="width: 100%"
      >
        <el-table-column prop="title" label="标题" min-width="200">
          <template #default="{ row }">
            <div class="post-title-cell">
              <el-tag v-if="row.is_top" type="danger" size="small" style="margin-right: 8px;">置顶</el-tag>
              <span>{{ row.title }}</span>
            </div>
          </template>
        </el-table-column>
        
        <el-table-column prop="author_name" label="作者" width="100" />
        
        <el-table-column prop="category_name" label="分类" width="120">
          <template #default="{ row }">
            <span v-if="row.category_name">{{ row.category_name }}</span>
            <span v-else style="color: #909399;">-</span>
          </template>
        </el-table-column>
        
        <el-table-column prop="status" label="状态" width="100">
          <template #default="{ row }">
            <el-tag :type="row.status === 'published' ? 'success' : 'info'" size="small">
              {{ row.status === 'published' ? '已发布' : '草稿' }}
            </el-tag>
          </template>
        </el-table-column>
        
        <el-table-column prop="views" label="阅读" width="80" />
        
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="{ row }">
            <el-button
              v-if="row.status === 'draft'"
              type="success"
              link
              size="small"
              @click="handlePublish(row)"
            >
              发布
            </el-button>
            <el-button
              type="primary"
              link
              size="small"
              @click="handleEdit(row)"
            >
              编辑
            </el-button>
            <el-button
              type="danger"
              link
              size="small"
              @click="handleDelete(row)"
            >
              删除
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      
      <!-- 分页 -->
      <div class="pagination-wrapper">
        <el-pagination
          v-model:current-page="currentPage"
          v-model:page-size="pageSize"
          :total="total"
          :page-sizes="[10, 20, 50]"
          layout="total, sizes, prev, pager, next"
          @size-change="handleSizeChange"
          @current-change="handlePageChange"
        />
      </div>
    </el-card>
  </div>
</template>

<script setup>
/**
 * 文章管理列表页组件
 *
 * 功能：
 * - 展示所有文章（包括草稿）
 * - 支持搜索和状态筛选
 * - 支持发布、编辑、删除操作
 */
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Search, Plus } from '@element-plus/icons-vue'
import { getAdminPosts, publishPost, deletePost } from '@/api/blog'

// 路由实例
const router = useRouter()

// 响应式数据
const posts = ref([])
const loading = ref(false)
const searchQuery = ref('')
const statusFilter = ref('')
const currentPage = ref(1)
const pageSize = ref(10)
const total = ref(0)

/**
 * 获取文章列表
 */
const fetchPosts = async () => {
  loading.value = true
  try {
    const params = {
      page: currentPage.value,
      page_size: pageSize.value
    }
    
    if (searchQuery.value.trim()) {
      params.search = searchQuery.value.trim()
    }
    
    if (statusFilter.value) {
      params.status = statusFilter.value
    }
    
    const response = await getAdminPosts(params)
    posts.value = response.results || []
    total.value = response.count || 0
  } catch (error) {
    console.error('获取文章失败:', error)
    ElMessage.error('获取文章列表失败')
  } finally {
    loading.value = false
  }
}

/**
 * 处理搜索
 */
const handleSearch = () => {
  currentPage.value = 1
  fetchPosts()
}

/**
 * 处理筛选变化
 */
const handleFilterChange = () => {
  currentPage.value = 1
  fetchPosts()
}

/**
 * 处理页码变化
 */
const handlePageChange = (page) => {
  currentPage.value = page
  fetchPosts()
}

/**
 * 处理每页数量变化
 */
const handleSizeChange = (size) => {
  pageSize.value = size
  currentPage.value = 1
  fetchPosts()
}

/**
 * 处理发布
 */
const handlePublish = async (row) => {
  try {
    await ElMessageBox.confirm('确定要发布这篇文章吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    
    await publishPost(row.id)
    ElMessage.success('发布成功')
    fetchPosts()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('发布失败:', error)
      ElMessage.error('发布失败')
    }
  }
}

/**
 * 处理编辑
 */
const handleEdit = (row) => {
  router.push(`/admin/posts/${row.id}/edit`)
}

/**
 * 处理删除
 */
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm('确定要删除这篇文章吗？此操作不可恢复！', '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'danger'
    })
    
    await deletePost(row.id)
    ElMessage.success('删除成功')
    fetchPosts()
  } catch (error) {
    if (error !== 'cancel') {
      console.error('删除失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

/**
 * 格式化日期
 */
const formatDate = (dateString) => {
  if (!dateString) return ''
  const date = new Date(dateString)
  return date.toLocaleString('zh-CN')
}

// 组件挂载时获取数据
onMounted(() => {
  fetchPosts()
})
</script>

<style scoped>
.admin-post-list {
  padding: 20px 0;
}

.page-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.page-header h2 {
  margin: 0;
}

.header-actions {
  display: flex;
  align-items: center;
}

.post-title-cell {
  display: flex;
  align-items: center;
}

.pagination-wrapper {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}
</style>
