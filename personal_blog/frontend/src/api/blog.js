/**
 * 博客 API 接口
 * 封装所有与博客相关的后端接口调用
 */

import request from '@/utils/request'

// =========================================================================
// 文章相关接口
// =========================================================================

/**
 * 获取文章列表
 * 
 * @param {Object} params - 查询参数
 * @param {string} params.search - 搜索关键词
 * @param {string} params.category - 分类 slug
 * @param {string} params.tag - 标签 slug
 * @param {number} params.page - 页码
 * @returns {Promise} 文章列表数据
 */
export function getPosts(params = {}) {
  return request({
    url: '/blog/posts/',
    method: 'get',
    params
  })
}

/**
 * 获取文章详情
 * 
 * @param {string} slug - 文章 URL 标识
 * @returns {Promise} 文章详情数据
 */
export function getPostDetail(slug) {
  return request({
    url: `/blog/posts/${slug}/`,
    method: 'get'
  })
}

/**
 * 创建文章
 * 
 * @param {Object} data - 文章数据
 * @returns {Promise} 创建的文章数据
 */
export function createPost(data) {
  return request({
    url: '/blog/posts/create/',
    method: 'post',
    data
  })
}

/**
 * 更新文章
 * 
 * @param {number} id - 文章 ID
 * @param {Object} data - 文章数据
 * @returns {Promise} 更新后的文章数据
 */
export function updatePost(id, data) {
  return request({
    url: `/blog/posts/${id}/update/`,
    method: 'put',
    data
  })
}

/**
 * 删除文章
 * 
 * @param {number} id - 文章 ID
 * @returns {Promise}
 */
export function deletePost(id) {
  return request({
    url: `/blog/posts/${id}/delete/`,
    method: 'delete'
  })
}

/**
 * 发布文章
 * 
 * @param {number} id - 文章 ID
 * @returns {Promise}
 */
export function publishPost(id) {
  return request({
    url: `/blog/posts/${id}/publish/`,
    method: 'post'
  })
}

// =========================================================================
// 分类相关接口
// =========================================================================

/**
 * 获取分类列表
 * 
 * @returns {Promise} 分类列表数据
 */
export function getCategories() {
  return request({
    url: '/blog/categories/',
    method: 'get'
  })
}

/**
 * 获取分类详情
 * 
 * @param {string} slug - 分类 URL 标识
 * @returns {Promise} 分类详情数据
 */
export function getCategoryDetail(slug) {
  return request({
    url: `/blog/categories/${slug}/`,
    method: 'get'
  })
}

// =========================================================================
// 标签相关接口
// =========================================================================

/**
 * 获取标签列表
 * 
 * @returns {Promise} 标签列表数据
 */
export function getTags() {
  return request({
    url: '/blog/tags/',
    method: 'get'
  })
}

/**
 * 获取标签详情
 * 
 * @param {string} slug - 标签 URL 标识
 * @returns {Promise} 标签详情数据
 */
export function getTagDetail(slug) {
  return request({
    url: `/blog/tags/${slug}/`,
    method: 'get'
  })
}

// =========================================================================
// 管理员接口
// =========================================================================

/**
 * 获取管理员文章列表（包含草稿）
 * 
 * @param {Object} params - 查询参数
 * @returns {Promise} 文章列表数据
 */
export function getAdminPosts(params = {}) {
  return request({
    url: '/blog/admin/posts/',
    method: 'get',
    params
  })
}

// =========================================================================
// 统计接口
// =========================================================================

/**
 * 获取博客统计信息
 * 
 * @returns {Promise} 统计数据
 */
export function getBlogStats() {
  return request({
    url: '/blog/stats/',
    method: 'get'
  })
}
