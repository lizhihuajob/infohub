import { createRouter, createWebHistory } from 'vue-router'
import PostList from '../components/PostList.vue'
import PostDetail from '../components/PostDetail.vue'
import AdminLogin from '../components/AdminLogin.vue'
import AdminDashboard from '../components/AdminDashboard.vue'

const routes = [
  {
    path: '/',
    name: 'PostList',
    component: PostList,
  },
  {
    path: '/posts/:id',
    name: 'PostDetail',
    component: PostDetail,
  },
  {
    path: '/admin/login',
    name: 'AdminLogin',
    component: AdminLogin,
  },
  {
    path: '/admin/dashboard',
    name: 'AdminDashboard',
    component: AdminDashboard,
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router