from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'blog'

urlpatterns = [
    # 健康检查
    path('health/', views.health_check, name='health_check'),
    
    # 首页
    path('', views.HomeView.as_view(), name='home'),

    # 文章详情
    path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),

    # 分类
    path('category/<slug:slug>/', views.CategoryView.as_view(), name='category'),

    # 标签
    path('tag/<slug:slug>/', views.TagView.as_view(), name='tag'),

    # 搜索
    path('search/', views.SearchView.as_view(), name='search'),

    # 静态页面
    path('page/<slug:slug>/', views.PageView.as_view(), name='page'),

    # 评论
    path('post/<slug:slug>/comment/', views.CommentView.as_view(), name='add_comment'),

    # 认证
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]
