#!/usr/bin/env python
"""
创建超级用户脚本
使用方法: docker-compose run web python create_superuser.py
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
django.setup()

from django.contrib.auth.models import User

username = 'admin'
email = 'admin@example.com'
password = 'admin123456'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username=username, email=email, password=password)
    print(f'超级用户创建成功!')
    print(f'用户名: {username}')
    print(f'密码: {password}')
    print(f'请登录后修改密码!')
else:
    print(f'用户 {username} 已存在!')
