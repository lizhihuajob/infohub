"""
项目级 URL 配置
定义整个项目的 URL 路由规则
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# 定义 URL 路由模式
urlpatterns = [
    # Django 管理后台
    path('admin/', admin.site.urls),
    
    # 博客应用 API 路由
    # 所有以 api/blog/ 开头的请求都会转发到 blog 应用的 URL 配置
    path('api/blog/', include('blog.urls')),
]

# 开发环境下提供媒体文件服务
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
