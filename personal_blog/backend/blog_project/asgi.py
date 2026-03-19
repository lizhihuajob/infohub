"""
ASGI 配置文件
用于异步部署和 WebSocket 支持
"""

import os

from django.core.asgi import get_asgi_application

# 设置默认的 Django 设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')

# 获取 ASGI 应用实例
application = get_asgi_application()
