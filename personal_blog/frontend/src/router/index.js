/**
 * 路由配置文件
 * 定义应用的所有路由规则
 */

import { createRouter, createWebHistory } from 'vue-router'

// 路由配置
const routes = [
  // =========================================================================
  // 公开路由
  // =========================================================================
  {
    path: '/',
    name: 'Home',
    component: () => import('@/views/Home.vue'),
    meta: {
      title: '首页',
      public: true
    }
  },
  {
    path: '/posts',
    name: 'PostList',
    component: () => import('@/views/PostList.vue'),
    meta: {
      title: '文章列表',
      public: true
    }
  },
  {
    path: '/posts/:slug',
    name: 'PostDetail',
    component: () => import('@/views/PostDetail.vue'),
    meta: {
      title: '文章详情',
      public: true
    }
  },
  {
    path: '/categories',
    name: 'CategoryList',
    component: () => import('@/views/CategoryList.vue'),
    meta: {
      title: '分类',
      public: true
    }
  },
  {
    path: '/tags',
    name: 'TagList',
    component: () => import('@/views/TagList.vue'),
    meta: {
      title: '标签',
      public: true
    }
  },
  
  // =========================================================================
  // 管理员路由
  // =========================================================================
  {
    path: '/admin',
    name: 'Admin',
    component: () => import('@/views/admin/AdminLayout.vue'),
    meta: {
      title: '管理后台',
      requiresAuth: true
    },
    children: [
      {
        path: '',
        name: 'AdminDashboard',
        component: () => import('@/views/admin/Dashboard.vue'),
        meta: { title: '仪表盘' }
      },
      {
        path: 'posts',
        name: 'AdminPostList',
        component: () => import('@/views/admin/PostList.vue'),
        meta: { title: '文章管理' }
      },
      {
        path: 'posts/create',
        name: 'AdminPostCreate',
        component: () => import('@/views/admin/PostEdit.vue'),
        meta: { title: '创建文章' }
      },
      {
        path: 'posts/:id/edit',
        name: 'AdminPostEdit',
        component: () => import('@/views/admin/PostEdit.vue'),
        meta: { title: '编辑文章' }
      },
      {
        path: 'categories',
        name: 'AdminCategoryList',
        component: () => import('@/views/admin/CategoryList.vue'),
        meta: { title: '分类管理' }
      },
      {
        path: 'tags',
        name: 'AdminTagList',
        component: () => import('@/views/admin/TagList.vue'),
        meta: { title: '标签管理' }
      }
    ]
  },
  
  // =========================================================================
  // 登录路由
  // =========================================================================
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta: {
      title: '登录',
      public: true
    }
  },
  
  // =========================================================================
  // 404 页面
  // =========================================================================
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('@/views/NotFound.vue'),
    meta: {
      title: '页面未找到',
      public: true
    }
  }
]

// 创建路由实例
const router = createRouter({
  history: createWebHistory(),
  routes,
  // 滚动行为：切换路由时滚动到页面顶部
  scrollBehavior() {
    return { top: 0 }
  }
})

// 路由守卫：设置页面标题
router.beforeEach((to, from, next) => {
  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - 个人博客` : '个人博客'
  next()
})

export default router
