/**
 * HTTP 请求工具
 * 基于 axios 封装，统一处理请求和响应
 */

import axios from 'axios'
import { ElMessage } from 'element-plus'

// 获取 API 基础 URL
// 开发环境使用空字符串，让 Vite 代理处理
// 生产环境使用环境变量配置
const baseURL = import.meta.env.DEV ? '' : (import.meta.env.VITE_API_URL || '/api')

// 创建 axios 实例
const request = axios.create({
  // 基础 URL
  baseURL: baseURL,
  // 请求超时时间（毫秒）
  timeout: 10000,
  // 请求头配置
  headers: {
    'Content-Type': 'application/json'
  }
})

// 请求拦截器
request.interceptors.request.use(
  (config) => {
    /**
     * 请求发送前的处理
     * 可以在这里添加认证 token、loading 状态等
     */
    // 从 localStorage 获取 token（如果有的话）
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error) => {
    /**
     * 请求发送失败的处理
     */
    console.error('请求发送失败:', error)
    return Promise.reject(error)
  }
)

// 响应拦截器
request.interceptors.response.use(
  (response) => {
    /**
     * 响应成功的处理
     * 直接返回响应数据
     */
    return response.data
  },
  (error) => {
    /**
     * 响应错误的处理
     * 统一处理错误提示
     */
    const { response } = error
    
    if (response) {
      // 根据 HTTP 状态码处理不同错误
      switch (response.status) {
        case 400:
          ElMessage.error('请求参数错误')
          break
        case 401:
          ElMessage.error('未授权，请登录')
          // 可以在这里处理登录过期，跳转到登录页
          localStorage.removeItem('token')
          window.location.href = '/login'
          break
        case 403:
          ElMessage.error('拒绝访问')
          break
        case 404:
          ElMessage.error('请求的资源不存在')
          break
        case 500:
          ElMessage.error('服务器内部错误')
          break
        default:
          ElMessage.error(`请求失败: ${response.statusText}`)
      }
    } else {
      // 网络错误或请求超时
      ElMessage.error('网络连接失败，请检查网络')
    }
    
    return Promise.reject(error)
  }
)

export default request
