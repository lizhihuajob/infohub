<template>
  <div class="admin-dashboard">
    <div class="dashboard-header">
      <h1>文章管理</h1>
      <button class="add-btn" @click="openAddModal">+ 新建文章</button>
    </div>
    
    <div v-if="loading" class="loading">加载中...</div>
    <div v-else-if="error" class="error">{{ error }}</div>
    <div v-else>
      <table class="posts-table">
        <thead>
          <tr>
            <th>标题</th>
            <th>作者</th>
            <th>发布时间</th>
            <th>状态</th>
            <th>浏览量</th>
            <th>操作</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="post in posts" :key="post.id">
            <td class="post-title">{{ post.title }}</td>
            <td>{{ post.author }}</td>
            <td>{{ post.created_time }}</td>
            <td>
              <span :class="['status', post.is_published ? 'published' : 'draft']">
                {{ post.is_published ? '已发布' : '草稿' }}
              </span>
            </td>
            <td>{{ post.views }}</td>
            <td class="actions">
              <button class="edit-btn" @click="openEditModal(post)">编辑</button>
              <button class="delete-btn" @click="handleDelete(post.id)">删除</button>
            </td>
          </tr>
          <tr v-if="posts.length === 0">
            <td colspan="6" class="empty">暂无文章</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- 新增/编辑模态框 -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <h2>{{ editingPost ? '编辑文章' : '新建文章' }}</h2>
        <form @submit.prevent="handleSubmit">
          <div class="form-group">
            <label for="title">标题</label>
            <input
              type="text"
              id="title"
              v-model="form.title"
              placeholder="请输入文章标题"
              required
            />
          </div>
          <div class="form-group">
            <label for="author">作者</label>
            <input
              type="text"
              id="author"
              v-model="form.author"
              placeholder="请输入作者名"
              required
            />
          </div>
          <div class="form-group">
            <label for="content">内容</label>
            <textarea
              id="content"
              v-model="form.content"
              placeholder="请输入文章内容"
              rows="10"
              required
            ></textarea>
          </div>
          <div class="form-group checkbox-group">
            <label>
              <input type="checkbox" v-model="form.is_published" />
              立即发布
            </label>
          </div>
          <div class="modal-actions">
            <button type="button" class="cancel-btn" @click="closeModal">取消</button>
            <button type="submit" class="submit-btn" :disabled="submitting">
              {{ submitting ? '保存中...' : '保存' }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, reactive } from 'vue'
import { getAdminPosts, createPost, updatePost, deletePost } from '../api/posts'

const posts = ref([])
const loading = ref(true)
const error = ref('')
const showModal = ref(false)
const editingPost = ref(null)
const submitting = ref(false)

const form = reactive({
  title: '',
  author: 'admin',
  content: '',
  is_published: true,
})

const loadPosts = async () => {
  try {
    loading.value = true
    const response = await getAdminPosts()
    posts.value = response.data
    error.value = ''
  } catch (err) {
    error.value = '加载文章失败，请稍后重试'
    console.error(err)
  } finally {
    loading.value = false
  }
}

const openAddModal = () => {
  editingPost.value = null
  form.title = ''
  form.author = 'admin'
  form.content = ''
  form.is_published = true
  showModal.value = true
}

const openEditModal = (post) => {
  editingPost.value = post
  form.title = post.title
  form.author = post.author
  form.content = post.content
  form.is_published = post.is_published
  showModal.value = true
}

const closeModal = () => {
  showModal.value = false
  editingPost.value = null
}

const handleSubmit = async () => {
  submitting.value = true
  try {
    if (editingPost.value) {
      await updatePost(editingPost.value.id, {
        title: form.title,
        author: form.author,
        content: form.content,
        is_published: form.is_published,
      })
    } else {
      await createPost({
        title: form.title,
        author: form.author,
        content: form.content,
        is_published: form.is_published,
      })
    }
    closeModal()
    await loadPosts()
  } catch (err) {
    console.error('保存失败:', err)
    alert('保存失败，请确保已登录管理员账户')
  } finally {
    submitting.value = false
  }
}

const handleDelete = async (id) => {
  if (confirm('确定要删除这篇文章吗？')) {
    try {
      await deletePost(id)
      await loadPosts()
    } catch (err) {
      console.error('删除失败:', err)
      alert('删除失败，请确保已登录管理员账户')
    }
  }
}

onMounted(() => {
  loadPosts()
})
</script>

<style scoped>
.admin-dashboard {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.dashboard-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 30px;
}

.dashboard-header h1 {
  color: #333;
  margin: 0;
}

.add-btn {
  background: #27ae60;
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.add-btn:hover {
  background: #219a52;
}

.posts-table {
  width: 100%;
  background: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-collapse: collapse;
  overflow: hidden;
}

.posts-table th,
.posts-table td {
  padding: 15px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.posts-table th {
  background: #f8f9fa;
  color: #333;
  font-weight: 600;
}

.posts-table tbody tr:hover {
  background: #f8f9fa;
}

.post-title {
  max-width: 300px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.status {
  padding: 4px 12px;
  border-radius: 20px;
  font-size: 0.85rem;
  font-weight: 500;
}

.status.published {
  background: #d4edda;
  color: #155724;
}

.status.draft {
  background: #fff3cd;
  color: #856404;
}

.actions {
  display: flex;
  gap: 10px;
}

.edit-btn,
.delete-btn {
  padding: 6px 12px;
  border: none;
  border-radius: 4px;
  font-size: 0.9rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.edit-btn {
  background: #3498db;
  color: #fff;
}

.edit-btn:hover {
  background: #2980b9;
}

.delete-btn {
  background: #e74c3c;
  color: #fff;
}

.delete-btn:hover {
  background: #c0392b;
}

.empty {
  text-align: center;
  color: #7f8c8d;
  padding: 40px !important;
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

/* 模态框样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.modal-content {
  background: #fff;
  padding: 30px;
  border-radius: 8px;
  width: 90%;
  max-width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.modal-content h2 {
  color: #333;
  margin-top: 0;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 20px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  color: #555;
  font-weight: 500;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 1rem;
  font-family: inherit;
  transition: border-color 0.2s;
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: #3498db;
}

.form-group textarea {
  resize: vertical;
  min-height: 150px;
}

.checkbox-group label {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.checkbox-group input[type="checkbox"] {
  width: auto;
}

.modal-actions {
  display: flex;
  gap: 15px;
  justify-content: flex-end;
  margin-top: 30px;
}

.cancel-btn,
.submit-btn {
  padding: 10px 24px;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.2s;
}

.cancel-btn {
  background: #95a5a6;
  color: #fff;
}

.cancel-btn:hover {
  background: #7f8c8d;
}

.submit-btn {
  background: #3498db;
  color: #fff;
}

.submit-btn:hover:not(:disabled) {
  background: #2980b9;
}

.submit-btn:disabled {
  background: #95a5a6;
  cursor: not-allowed;
}
</style>