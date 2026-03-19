import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  headers: {
    'Content-Type': 'application/json',
  },
})

// 获取所有已发布的文章
export const getPosts = () => {
  return api.get('/posts/')
}

// 获取单篇文章详情
export const getPost = (id) => {
  return api.get(`/posts/${id}/`)
}

// 创建文章（需要管理员权限）
export const createPost = (data) => {
  return api.post('/posts/', data, {
    withCredentials: true,
  })
}

// 更新文章（需要管理员权限）
export const updatePost = (id, data) => {
  return api.put(`/posts/${id}/`, data, {
    withCredentials: true,
  })
}

// 删除文章（需要管理员权限）
export const deletePost = (id) => {
  return api.delete(`/posts/${id}/`, {
    withCredentials: true,
  })
}

// 获取所有文章（管理员，包括未发布的）
export const getAdminPosts = () => {
  return api.get('/posts/admin_list/', {
    withCredentials: true,
  })
}

export default api