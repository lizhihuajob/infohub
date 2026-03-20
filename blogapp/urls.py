from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'blogapp'

urlpatterns = [
    # 首页
    path('', views.HomeView.as_view(), name='home'),
    
    # 文章详情
    path('post/<int:year>/<int:month>/<int:day>/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    
    # 分类和标签
    path('category/<slug:slug>/', views.CategoryDetailView.as_view(), name='category_detail'),
    path('tag/<slug:slug>/', views.TagDetailView.as_view(), name='tag_detail'),
    
    # 搜索
    path('search/', views.SearchView.as_view(), name='search'),
    
    # 静态页面
    path('page/<slug:slug>/', views.PageDetailView.as_view(), name='page_detail'),
    path('about/', views.AboutView.as_view(), name='about'),
    path('links/', views.LinksView.as_view(), name='links'),
    path('guestbook/', views.GuestbookView.as_view(), name='guestbook'),
    
    # 评论
    path('comment/<int:post_id>/', views.CommentCreateView.as_view(), name='comment_create'),
    
    # 用户认证
    path('login/', auth_views.LoginView.as_view(template_name='blogapp/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]
