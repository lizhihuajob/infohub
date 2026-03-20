"""
WSGI 配置文件
用于生产环境部署，定义 WSGI 应用入口
"""

import os

from django.core.wsgi import get_wsgi_application

# 设置默认的 Django 设置模块
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')

# 获取 WSGI 应用实例
application = get_wsgi_application()
