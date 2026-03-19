<template>
  <!--
    登录页面
    管理员登录入口
  -->
  <div class="login-page">
    <div class="login-box">
      <!-- 标题 -->
      <div class="login-header">
        <h2>管理员登录</h2>
        <p>请输入您的账号和密码</p>
      </div>
      
      <!-- 登录表单 -->
      <el-form
        ref="loginFormRef"
        :model="loginForm"
        :rules="loginRules"
        class="login-form"
        @keyup.enter="handleLogin"
      >
        <el-form-item prop="username">
          <el-input
            v-model="loginForm.username"
            placeholder="用户名"
            size="large"
            :prefix-icon="User"
            clearable
          />
        </el-form-item>
        
        <el-form-item prop="password">
          <el-input
            v-model="loginForm.password"
            type="password"
            placeholder="密码"
            size="large"
            :prefix-icon="Lock"
            show-password
            clearable
          />
        </el-form-item>
        
        <el-form-item>
          <el-button
            type="primary"
            size="large"
            class="login-button"
            :loading="loading"
            @click="handleLogin"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
      
      <!-- 提示信息 -->
      <div class="login-tips">
        <el-alert
          title="提示：请使用 Django 管理员账号登录"
          type="info"
          :closable="false"
          show-icon
        />
      </div>
      
      <!-- 返回首页 -->
      <div class="back-home">
        <router-link to="/">
          <el-button link>
            <el-icon><ArrowLeft /></el-icon>
            返回首页
          </el-button>
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
/**
 * 登录页面组件
 * 
 * 功能：
 * - 管理员登录表单
 * - 表单验证
 * - 登录后跳转到管理后台
 * 
 * 注意：这是一个简化版登录页面，实际项目中需要对接后端认证接口
 */
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, ArrowLeft } from '@element-plus/icons-vue'

// 路由实例
const router = useRouter()

// 响应式数据
const loading = ref(false)
const loginFormRef = ref(null)

// 登录表单数据
const loginForm = reactive({
  username: '',
  password: ''
})

// 表单验证规则
const loginRules = {
  username: [
    { required: true, message: '请输入用户名', trigger: 'blur' },
    { min: 3, max: 20, message: '用户名长度应在 3-20 个字符之间', trigger: 'blur' }
  ],
  password: [
    { required: true, message: '请输入密码', trigger: 'blur' },
    { min: 6, max: 20, message: '密码长度应在 6-20 个字符之间', trigger: 'blur' }
  ]
}

/**
 * 处理登录
 * 
 * 注意：这是一个简化实现，实际项目中需要：
 * 1. 调用后端登录接口
 * 2. 保存返回的 token
 * 3. 处理登录失败的情况
 */
const handleLogin = async () => {
  // 表单验证
  const valid = await loginFormRef.value?.validate().catch(() => false)
  if (!valid) return
  
  loading.value = true
  
  try {
    // TODO: 调用后端登录接口
    // const response = await loginApi(loginForm)
    // localStorage.setItem('token', response.token)
    
    // 模拟登录成功
    ElMessage.success('登录成功')
    
    // 跳转到管理后台
    router.push('/admin')
  } catch (error) {
    ElMessage.error('登录失败，请检查用户名和密码')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.login-box {
  width: 100%;
  max-width: 400px;
  background-color: #fff;
  border-radius: 12px;
  padding: 40px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.2);
}

.login-header {
  text-align: center;
  margin-bottom: 30px;
}

.login-header h2 {
  font-size: 24px;
  color: #303133;
  margin-bottom: 10px;
}

.login-header p {
  color: #909399;
  font-size: 14px;
}

.login-form {
  margin-bottom: 20px;
}

.login-button {
  width: 100%;
}

.login-tips {
  margin-bottom: 20px;
}

.back-home {
  text-align: center;
}
</style>
