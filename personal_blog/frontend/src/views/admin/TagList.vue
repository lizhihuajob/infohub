<template>
  <!--
    标签管理页
    管理文章标签
  -->
  <div class="admin-tag-list">
    <div class="page-header">
      <h2>标签管理</h2>
      <el-button type="primary" @click="handleCreate">
        <el-icon><Plus /></el-icon>
        新建标签
      </el-button>
    </div>

    <el-card>
      <el-table :data="tags" v-loading="loading" stripe>
        <el-table-column prop="name" label="标签名称" />
        <el-table-column prop="slug" label="URL 标识" />
        <el-table-column prop="created_at" label="创建时间" width="180">
          <template #default="{ row }">
            {{ formatDate(row.created_at) }}
          </template>
        </el-table-column>
        <el-table-column label="操作" width="150" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link @click="handleEdit(row)">编辑</el-button>
            <el-button type="danger" link @click="handleDelete(row)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <!-- 编辑对话框 -->
    <el-dialog
      v-model="dialogVisible"
      :title="isEdit ? '编辑标签' : '新建标签'"
      width="500px"
    >
      <el-form ref="formRef" :model="form" :rules="rules" label-width="80px">
        <el-form-item label="名称" prop="name">
          <el-input v-model="form.name" placeholder="请输入标签名称" />
        </el-form-item>
        <el-form-item label="URL标识" prop="slug">
          <el-input v-model="form.slug" placeholder="请输入 URL 标识" />
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" :loading="saving" @click="handleSave">保存</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<script setup>
/**
 * 标签管理页组件
 *
 * 功能：
 * - 展示所有标签
 * - 创建、编辑、删除标签
 */
import { ref, onMounted } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus } from '@element-plus/icons-vue'
import { getTags } from '@/api/blog'

// 响应式数据
const tags = ref([])
const loading = ref(false)
const dialogVisible = ref(false)
const isEdit = ref(false)
const saving = ref(false)
const formRef = ref(null)
const currentId = ref(null)

// 表单数据
const form = ref({
  name: '',
  slug: ''
})

// 表单验证规则
const rules = {
  name: [
    { required: true, message: '请输入标签名称', trigger: 'blur' }
  ],
  slug: [
    { required: true, message: '请输入 URL 标识', trigger: 'blur' },
    { pattern: /^[a-z0-9-]+$/, message: '只能包含小写字母、数字和连字符', trigger: 'blur' }
  ]
}

/**
 * 获取标签列表
 */
const fetchTags = async () => {
  loading.value = true
  try {
    tags.value = await getTags()
  } catch (error) {
    console.error('获取标签失败:', error)
    ElMessage.error('获取标签列表失败')
  } finally {
    loading.value = false
  }
}

/**
 * 处理创建
 */
const handleCreate = () => {
  isEdit.value = false
  currentId.value = null
  form.value = { name: '', slug: '' }
  dialogVisible.value = true
}

/**
 * 处理编辑
 */
const handleEdit = (row) => {
  isEdit.value = true
  currentId.value = row.id
  form.value = { ...row }
  dialogVisible.value = true
}

/**
 * 处理保存
 */
const handleSave = async () => {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  saving.value = true
  try {
    // TODO: 调用保存 API
    ElMessage.success(isEdit.value ? '更新成功' : '创建成功')
    dialogVisible.value = false
    fetchTags()
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

/**
 * 处理删除
 */
const handleDelete = async (row) => {
  try {
    await ElMessageBox.confirm(`确定要删除标签 "${row.name}" 吗？`, '警告', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    // TODO: 调用删除 API
    ElMessage.success('删除成功')
    fetchTags()
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
  return new Date(dateString).toLocaleString('zh-CN')
}

// 组件挂载时获取数据
onMounted(() => {
  fetchTags()
})
</script>

<style scoped>
.admin-tag-list {
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
</style>
