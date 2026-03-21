"""
初始化脚本 - 创建示例数据
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myblog.settings')
django.setup()

from django.contrib.auth.models import User
from blog.models import Category, Post, StaticPage, Link

def create_superuser():
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
        print('超级用户创建成功: admin / admin123')
    else:
        print('超级用户已存在')

def create_categories():
    categories = [
        {'name': 'Python', 'slug': 'python', 'description': 'Python编程相关文章'},
        {'name': 'Django', 'slug': 'django', 'description': 'Django框架相关文章'},
        {'name': '前端开发', 'slug': 'frontend', 'description': '前端开发技术文章'},
        {'name': '数据库', 'slug': 'database', 'description': '数据库相关文章'},
        {'name': '运维', 'slug': 'devops', 'description': '运维相关文章'},
    ]
    
    for cat_data in categories:
        Category.objects.get_or_create(slug=cat_data['slug'], defaults=cat_data)
    print('分类创建完成')

def create_sample_posts():
    admin = User.objects.get(username='admin')
    python_cat = Category.objects.get(slug='python')
    django_cat = Category.objects.get(slug='django')
    
    posts = [
        {
            'title': 'Django博客开发入门指南',
            'slug': 'django-blog-tutorial',
            'category': django_cat,
            'content': '''# Django博客开发入门指南

## 简介

Django是一个高级Python Web框架，鼓励快速开发和干净、实用的设计。

## 安装Django

```bash
pip install django
```

## 创建项目

```bash
django-admin startproject myblog
cd myblog
python manage.py startapp blog
```

## 创建模型

在`blog/models.py`中定义数据模型：

```python
from django.db import models

class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
```

## 总结

Django让Web开发变得简单高效！
''',
            'status': 'published',
            'author': admin,
        },
        {
            'title': 'Python装饰器详解',
            'slug': 'python-decorators',
            'category': python_cat,
            'content': '''# Python装饰器详解

## 什么是装饰器

装饰器是一种特殊的函数，用于修改其他函数的行为。

## 基本语法

```python
@decorator
def my_function():
    pass
```

## 示例

```python
def my_decorator(func):
    def wrapper():
        print("函数执行前")
        func()
        print("函数执行后")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")
```

## 常见应用

1. 日志记录
2. 权限验证
3. 缓存
4. 计时
''',
            'status': 'published',
            'author': admin,
        },
        {
            'title': 'SQLite数据库基础',
            'slug': 'sqlite-basics',
            'category': Category.objects.get(slug='database'),
            'content': '''# SQLite数据库基础

## 简介

SQLite是一个轻量级的嵌入式数据库，非常适合小型项目和原型开发。

## 特点

- 无需服务器
- 零配置
- 单文件存储
- 跨平台

## Python中使用SQLite

```python
import sqlite3

conn = sqlite3.connect('example.db')
cursor = conn.cursor()

cursor.execute(\'\'\'
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT,
        email TEXT
    )
\'\'\')

conn.commit()
conn.close()
```
''',
            'status': 'published',
            'author': admin,
        },
    ]
    
    for post_data in posts:
        post, created = Post.objects.get_or_create(
            slug=post_data['slug'],
            defaults=post_data
        )
        if created:
            post.tags.add('Python', 'Tutorial')
    print('示例文章创建完成')

def create_static_pages():
    pages = [
        {
            'title': '关于我',
            'slug': 'about',
            'page_type': 'about',
            'content': '''# 关于我

## 个人简介

我是一名热爱编程的开发者，专注于Python和Web开发。

## 技术栈

- Python / Django
- JavaScript / Vue.js
- PostgreSQL / MySQL
- Docker / Linux

## 联系方式

- Email: example@example.com
- GitHub: https://github.com
''',
            'is_published': True,
        },
    ]
    
    for page_data in pages:
        StaticPage.objects.get_or_create(slug=page_data['slug'], defaults=page_data)
    print('静态页面创建完成')

def create_links():
    links = [
        {'name': 'Django官网', 'url': 'https://www.djangoproject.com/', 'description': 'Django官方文档'},
        {'name': 'Python官网', 'url': 'https://www.python.org/', 'description': 'Python官方网站'},
    ]
    
    for link_data in links:
        Link.objects.get_or_create(url=link_data['url'], defaults=link_data)
    print('友情链接创建完成')

def main():
    print('开始初始化数据...')
    create_superuser()
    create_categories()
    create_sample_posts()
    create_static_pages()
    create_links()
    print('初始化完成！')

if __name__ == '__main__':
    main()
