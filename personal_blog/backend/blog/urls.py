"""
博客应用 URL 配置
定义博客应用的所有 API 路由
"""

from django.urls import path
from . import views

# URL 路由配置
urlpatterns = [
    # =========================================================================
    # 分类相关路由
    # =========================================================================
    # 分类列表
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    # 分类详情
    path('categories/<slug:slug>/', views.CategoryDetailView.as_view(), name='category-detail'),
    
    # =========================================================================
    # 标签相关路由
    # =========================================================================
    # 标签列表
    path('tags/', views.TagListView.as_view(), name='tag-list'),
    # 标签详情
    path('tags/<slug:slug>/', views.TagDetailView.as_view(), name='tag-detail'),
    
    # =========================================================================
    # 文章相关路由（公开访问）
    # =========================================================================
    # 文章列表（支持搜索和筛选）
    path('posts/', views.PostListView.as_view(), name='post-list'),
    # 文章详情
    path('posts/<slug:slug>/', views.PostDetailView.as_view(), name='post-detail'),
    # 增加浏览次数
    path('posts/<slug:slug>/view/', views.increment_views, name='post-increment-views'),
    
    # =========================================================================
    # 文章管理路由（需要认证）
    # =========================================================================
    # 创建文章
    path('posts/create/', views.PostCreateView.as_view(), name='post-create'),
    # 更新文章
    path('posts/<int:pk>/update/', views.PostUpdateView.as_view(), name='post-update'),
    # 删除文章
    path('posts/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    # 发布文章
    path('posts/<int:pk>/publish/', views.publish_post, name='post-publish'),
    
    # =========================================================================
    # 管理员路由
    # =========================================================================
    # 管理员文章列表（包含草稿）
    path('admin/posts/', views.AdminPostListView.as_view(), name='admin-post-list'),
    
    # =========================================================================
    # 统计路由
    # =========================================================================
    # 博客统计信息
    path('stats/', views.blog_stats, name='blog-stats'),
]
