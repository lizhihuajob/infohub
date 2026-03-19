/**
 * 评论组件
 */
<template>
  <div class="comment-section">
    <h3 class="section-title">评论区 ({{ comments.length }})</h3>

    <!-- 发表评论 -->
    <div class="comment-form">
      <el-form :model="form" label-width="80px">
        <el-form-item label="昵称">
          <el-input v-model="form.nickname" placeholder="请输入昵称" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form.email" placeholder="请输入邮箱（选填）" />
        </el-form-item>
        <el-form-item label="评论内容">
          <el-input
            v-model="form.content"
            type="textarea"
            :rows="4"
            placeholder="请输入评论内容"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitComment" :loading="submitting">
            发表评论
          </el-button>
        </el-form-item>
      </el-form>
    </div>

    <!-- 评论列表 -->
    <div class="comment-list">
      <div
        v-for="comment in comments"
        :key="comment.id"
        class="comment-item"
      >
        <div class="comment-avatar">
          <el-avatar :size="40">{{ comment.nickname.charAt(0) }}</el-avatar>
        </div>
        <div class="comment-content">
          <div class="comment-header">
            <span class="nickname">{{ comment.nickname }}</span>
            <span class="date">{{ formatDate(comment.created_at) }}</span>
          </div>
          <div class="comment-text">{{ comment.content }}</div>

          <!-- 子评论 -->
          <div class="replies" v-if="comment.replies && comment.replies.length">
            <div
              v-for="reply in comment.replies"
              :key="reply.id"
              class="reply-item"
            >
              <span class="nickname">{{ reply.nickname }}</span>:
              <span class="text">{{ reply.content }}</span>
              <span class="date">{{ formatDate(reply.created_at) }}</span>
            </div>
          </div>
        </div>
      </div>

      <el-empty v-if="!comments.length" description="暂无评论" :image-size="60" />
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/utils/api'
import { ElMessage } from 'element-plus'

const props = defineProps({
  articleId: {
    type: [Number, String],
    required: true
  }
})

// 评论列表
const comments = ref([])
// 表单数据
const form = ref({
  nickname: '',
  email: '',
  content: ''
})
// 提交状态
const submitting = ref(false)

// 获取评论列表
const fetchComments = async () => {
  try {
    const response = await api.get('/comments/', {
      params: { article: props.articleId }
    })
    comments.value = response.results || response
  } catch (error) {
    console.error('获取评论失败:', error)
  }
}

// 提交评论
const submitComment = async () => {
  if (!form.value.nickname.trim()) {
    ElMessage.warning('请输入昵称')
    return
  }
  if (!form.value.content.trim()) {
    ElMessage.warning('请输入评论内容')
    return
  }

  submitting.value = true
  try {
    await api.post('/comments/', {
      ...form.value,
      article: props.articleId
    })
    ElMessage.success('评论发表成功')
    form.value.content = ''
    fetchComments()
  } catch (error) {
    ElMessage.error('评论发表失败')
  } finally {
    submitting.value = false
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
  fetchComments()
})
</script>

<style scoped>
.comment-section {
  margin-top: 20px;
}

.section-title {
  font-size: 18px;
  font-weight: bold;
  margin-bottom: 20px;
  padding-bottom: 10px;
  border-bottom: 2px solid #409eff;
}

.comment-form {
  background: #f9f9f9;
  padding: 20px;
  border-radius: 8px;
  margin-bottom: 30px;
}

.comment-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.comment-item {
  display: flex;
  gap: 15px;
}

.comment-avatar {
  flex-shrink: 0;
}

.comment-content {
  flex: 1;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 15px;
  margin-bottom: 8px;
}

.nickname {
  font-weight: bold;
  color: #333;
}

.date {
  color: #999;
  font-size: 12px;
}

.comment-text {
  color: #666;
  line-height: 1.6;
}

.replies {
  margin-top: 15px;
  padding-left: 20px;
  border-left: 2px solid #eee;
}

.reply-item {
  padding: 8px 0;
  color: #666;
  font-size: 14px;
}

.reply-item .nickname {
  color: #409eff;
  font-weight: normal;
}

.reply-item .text {
  margin: 0 8px;
}

.reply-item .date {
  font-size: 12px;
}
</style>
