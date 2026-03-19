/**
 * 文章编辑页面（创建和编辑共用）
 */
<template>
  <div class="article-edit">
    <div class="page-header">
      <h2>{{ isEdit ? '编辑文章' : '创建文章' }}</h2>
      <el-button @click="router.back()">返回</el-button>
    </div>

    <el-form
      ref="formRef"
      :model="form"
      :rules="rules"
      label-width="100px"
      v-loading="loading"
    >
      <el-form-item label="文章标题" prop="title">
        <el-input v-model="form.title" placeholder="请输入文章标题" />
      </el-form-item>

      <el-form-item label="文章摘要" prop="summary">
        <el-input
          v-model="form.summary"
          type="textarea"
          :rows="3"
          placeholder="请输入文章摘要"
        />
      </el-form-item>

      <el-form-item label="文章内容" prop="content">
        <el-input
          v-model="form.content"
          type="textarea"
          :rows="15"
          placeholder="请输入文章内容（支持HTML格式）"
        />
      </el-form-item>

      <el-form-item label="封面图片">
        <el-input v-model="form.cover_image" placeholder="请输入封面图片URL" />
      </el-form-item>

      <el-form-item label="所属分类">
        <el-select v-model="form.category" placeholder="请选择分类" clearable>
          <el-option
            v-for="category in categories"
            :key="category.id"
            :label="category.name"
            :value="category.id"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="标签">
        <el-select v-model="form.tags" multiple placeholder="请选择标签">
          <el-option
            v-for="tag in tags"
            :key="tag.id"
            :label="tag.name"
            :value="tag.id"
          />
        </el-select>
      </el-form-item>

      <el-form-item label="发布状态">
        <el-radio-group v-model="form.status">
          <el-radio value="draft">草稿</el-radio>
          <el-radio value="published">发布</el-radio>
        </el-radio-group>
      </el-form-item>

      <el-form-item label="是否置顶">
        <el-switch v-model="form.is_top" />
      </el-form-item>

      <el-form-item>
        <el-button type="primary" @click="handleSubmit" :loading="submitting">
          {{ isEdit ? '保存修改' : '创建文章' }}
        </el-button>
        <el-button @click="router.back()">取消</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import api from '@/utils/api'
import { ElMessage } from 'element-plus'

const route = useRoute()
const router = useRouter()

const isEdit = computed(() => !!route.params.id)
const formRef = ref(null)
const loading = ref(false)
const submitting = ref(false)

const form = ref({
  title: '',
  summary: '',
  content: '',
  cover_image: '',
  category: null,
  tags: [],
  status: 'draft',
  is_top: false
})

const rules = {
  title: [{ required: true, message: '请输入文章标题', trigger: 'blur' }],
  content: [{ required: true, message: '请输入文章内容', trigger: 'blur' }]
}

const categories = ref([])
const tags = ref([])

const fetchCategories = async () => {
  try {
    const response = await api.get('/categories/')
    categories.value = response.results || response
  } catch (error) {
    console.error('获取分类失败:', error)
  }
}

const fetchTags = async () => {
  try {
    const response = await api.get('/tags/')
    tags.value = response.results || response
  } catch (error) {
    console.error('获取标签失败:', error)
  }
}

const fetchArticle = async () => {
  if (!isEdit.value) return

  loading.value = true
  try {
    const response = await api.get(`/articles/${route.params.id}/`)
    form.value = {
      title: response.title,
      summary: response.summary,
      content: response.content,
      cover_image: response.cover_image || '',
      category: response.category?.id || response.category,
      tags: response.tags?.map(t => t.id || t) || [],
      status: response.status,
      is_top: response.is_top
    }
  } catch (error) {
    ElMessage.error('获取文章失败')
    router.back()
  } finally {
    loading.value = false
  }
}

const handleSubmit = async () => {
  if (!formRef.value) return

  await formRef.value.validate(async (valid) => {
    if (!valid) return

    submitting.value = true
    try {
      if (isEdit.value) {
        await api.put(`/articles/${route.params.id}/`, form.value)
        ElMessage.success('文章更新成功')
      } else {
        await api.post('/articles/', form.value)
        ElMessage.success('文章创建成功')
      }
      router.push('/admin/articles')
    } catch (error) {
      ElMessage.error(isEdit.value ? '更新失败' : '创建失败')
    } finally {
      submitting.value = false
    }
  })
}

onMounted(() => {
  fetchCategories()
  fetchTags()
  fetchArticle()
})
</script>

<style scoped>
.article-edit {
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
  padding-bottom: 15px;
  border-bottom: 1px solid #eee;
}

.page-header h2 {
  font-size: 20px;
  color: #333;
}
</style>
