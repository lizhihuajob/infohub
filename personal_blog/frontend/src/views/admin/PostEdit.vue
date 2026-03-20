<template>
  <!--
    文章编辑页
    用于创建新文章或编辑已有文章
  -->
  <div class="post-edit-page">
    <!-- 页面标题 -->
    <div class="page-header">
      <h2>{{ isEdit ? '编辑文章' : '创建文章' }}</h2>
      <div class="header-actions">
        <el-button @click="$router.back()">取消</el-button>
        <el-button type="primary" :loading="saving" @click="handleSave">
          保存
        </el-button>
      </div>
    </div>

    <!-- 文章表单 -->
    <el-card>
      <el-form
        ref="formRef"
        :model="form"
        :rules="rules"
        label-position="top"
      >
        <!-- 标题 -->
        <el-form-item label="文章标题" prop="title">
          <el-input
            v-model="form.title"
            placeholder="请输入文章标题"
            maxlength="200"
            show-word-limit
          />
        </el-form-item>

        <!-- URL 标识 -->
        <el-form-item label="URL 标识" prop="slug">
          <el-input
            v-model="form.slug"
            placeholder="请输入 URL 标识，如 my-first-post"
            maxlength="200"
          />
        </el-form-item>

        <!-- 分类和标签 -->
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="分类">
              <el-select
                v-model="form.category_id"
                placeholder="选择分类"
                clearable
                style="width: 100%"
              >
                <el-option
                  v-for="category in categories"
                  :key="category.id"
                  :label="category.name"
                  :value="category.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="标签">
              <el-select
                v-model="form.tag_ids"
                multiple
                placeholder="选择标签"
                style="width: 100%"
              >
                <el-option
                  v-for="tag in tags"
                  :key="tag.id"
                  :label="tag.name"
                  :value="tag.id"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <!-- 摘要 -->
        <el-form-item label="文章摘要">
          <el-input
            v-model="form.summary"
            type="textarea"
            :rows="3"
            placeholder="请输入文章摘要，用于列表展示"
            maxlength="500"
            show-word-limit
          />
        </el-form-item>

        <!-- 内容 -->
        <el-form-item label="文章内容" prop="content">
          <el-tabs type="border-card">
            <el-tab-pane label="编辑">
              <el-input
                v-model="form.content"
                type="textarea"
                :rows="15"
                placeholder="支持 Markdown 格式"
              />
            </el-tab-pane>
            <el-tab-pane label="预览">
              <div class="markdown-preview" v-html="renderedContent"></div>
            </el-tab-pane>
          </el-tabs>
        </el-form-item>

        <!-- 其他设置 -->
        <el-row :gutter="20">
          <el-col :span="12">
            <el-form-item label="发布状态">
              <el-radio-group v-model="form.status">
                <el-radio label="draft">草稿</el-radio>
                <el-radio label="published">立即发布</el-radio>
              </el-radio-group>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item>
              <el-checkbox v-model="form.is_top">置顶文章</el-checkbox>
            </el-form-item>
          </el-col>
        </el-row>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
/**
 * 文章编辑页组件
 *
 * 功能：
 * - 创建新文章
 * - 编辑已有文章
 * - 支持 Markdown 预览
 */
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import MarkdownIt from 'markdown-it'
import hljs from 'highlight.js'
import { createPost, updatePost, getPostDetail } from '@/api/blog'
import { getCategories, getTags } from '@/api/blog'

// 路由实例
const route = useRoute()
const router = useRouter()

// 判断是否为编辑模式
const isEdit = computed(() => !!route.params.id)
const postId = computed(() => route.params.id)

// 响应式数据
const formRef = ref(null)
const saving = ref(false)
const categories = ref([])
const tags = ref([])

// 表单数据
const form = ref({
  title: '',
  slug: '',
  category_id: null,
  tag_ids: [],
  summary: '',
  content: '',
  status: 'draft',
  is_top: false
})

// 表单验证规则
const rules = {
  title: [
    { required: true, message: '请输入文章标题', trigger: 'blur' },
    { min: 2, max: 200, message: '标题长度应在 2-200 个字符之间', trigger: 'blur' }
  ],
  slug: [
    { required: true, message: '请输入 URL 标识', trigger: 'blur' },
    { pattern: /^[a-z0-9-]+$/, message: 'URL 标识只能包含小写字母、数字和连字符', trigger: 'blur' }
  ],
  content: [
    { required: true, message: '请输入文章内容', trigger: 'blur' }
  ]
}

// Markdown 渲染器
const md = new MarkdownIt({
  html: true,
  linkify: true,
  typographer: true,
  highlight: function (str, lang) {
    if (lang && hljs.getLanguage(lang)) {
      try {
        return hljs.highlight(str, { language: lang }).value
      } catch (__) {}
    }
    return ''
  }
})

// 渲染后的内容
const renderedContent = computed(() => {
  return md.render(form.value.content || '')
})

/**
 * 获取分类和标签列表
 */
const fetchCategoriesAndTags = async () => {
  try {
    categories.value = await getCategories()
    tags.value = await getTags()
  } catch (error) {
    console.error('获取分类标签失败:', error)
  }
}

/**
 * 获取文章详情（编辑模式）
 */
const fetchPostDetail = async () => {
  if (!isEdit.value) return

  try {
    const post = await getPostDetail(postId.value)
    form.value = {
      title: post.title,
      slug: post.slug,
      category_id: post.category?.id || null,
      tag_ids: post.tags?.map(tag => tag.id) || [],
      summary: post.summary || '',
      content: post.content,
      status: post.status,
      is_top: post.is_top
    }
  } catch (error) {
    console.error('获取文章详情失败:', error)
    ElMessage.error('获取文章详情失败')
  }
}

/**
 * 保存文章
 */
const handleSave = async () => {
  const valid = await formRef.value?.validate().catch(() => false)
  if (!valid) return

  saving.value = true
  try {
    if (isEdit.value) {
      await updatePost(postId.value, form.value)
      ElMessage.success('更新成功')
    } else {
      await createPost(form.value)
      ElMessage.success('创建成功')
    }
    router.push('/admin/posts')
  } catch (error) {
    console.error('保存失败:', error)
    ElMessage.error('保存失败')
  } finally {
    saving.value = false
  }
}

// 组件挂载时获取数据
onMounted(() => {
  fetchCategoriesAndTags()
  fetchPostDetail()
})
</script>

<style scoped>
.post-edit-page {
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

.markdown-preview {
  padding: 20px;
  background-color: #f5f7fa;
  border-radius: 4px;
  min-height: 300px;
}

.markdown-preview :deep(h1),
.markdown-preview :deep(h2),
.markdown-preview :deep(h3),
.markdown-preview :deep(h4),
.markdown-preview :deep(h5),
.markdown-preview :deep(h6) {
  margin-top: 20px;
  margin-bottom: 10px;
}

.markdown-preview :deep(p) {
  margin-bottom: 10px;
}

.markdown-preview :deep(pre) {
  background-color: #fff;
  padding: 10px;
  border-radius: 4px;
}
</style>
