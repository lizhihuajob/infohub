"""
URL configuration for myblog project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('markdownx/', include('markdownx.urls')),
    path('', include('blog.urls')),
]

# 媒体文件服务（开发和生产环境都需要）
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# 静态文件服务（仅在开发环境，生产环境使用whitenoise或nginx）
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
