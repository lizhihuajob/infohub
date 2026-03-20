#!/usr/bin/env python
"""
创建测试数据脚本
使用方法: docker-compose run web python create_test_data.py
"""
import os
import django
from django.utils import timezone
from django.utils.text import slugify

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')
django.setup()

from django.contrib.auth.models import User
from blogapp.models import Category, Tag, Post, Link, Page

def create_test_data():
    # 创建管理员用户（如果不存在）
    admin_user, created = User.objects.get_or_create(
        username='admin',
        email='admin@example.com',
        is_staff=True,
        is_superuser=True
    )
    if created:
        admin_user.set_password('admin123456')
        admin_user.save()
        print('创建管理员用户: admin / admin123456')
    else:
        print('管理员用户已存在')

    # 创建分类
    categories_data = [
        ('技术', 'tech', '技术相关文章'),
        ('生活', 'life', '生活随笔'),
        ('教程', 'tutorial', '教程分享'),
        ('随笔', 'essay', '随笔杂谈'),
    ]
    
    categories = {}
    for name, slug, desc in categories_data:
        cat, created = Category.objects.get_or_create(
            name=name,
            slug=slug,
            defaults={'description': desc}
        )
        categories[slug] = cat
        if created:
            print(f'创建分类: {name}')

    # 创建子分类
    sub_categories_data = [
        ('Python', 'python', 'Python相关文章', 'tech'),
        ('Django', 'django', 'Django框架学习', 'tech'),
        ('JavaScript', 'javascript', '前端技术', 'tech'),
    ]
    
    for name, slug, desc, parent_slug in sub_categories_data:
        parent = categories.get(parent_slug)
        if parent:
            cat, created = Category.objects.get_or_create(
                name=name,
                slug=slug,
                defaults={'description': desc, 'parent': parent}
            )
            if created:
                print(f'创建子分类: {name}')

    # 创建标签
    tags_data = ['Django', 'Python', 'JavaScript', 'Vue', 'React', 'CSS', 'HTML', 'Docker', 'Linux', 'MySQL']
    tags = {}
    for tag_name in tags_data:
        tag, created = Tag.objects.get_or_create(
            name=tag_name,
            slug=slugify(tag_name)
        )
        tags[tag_name] = tag
        if created:
            print(f'创建标签: {tag_name}')

    # 创建示例文章
    posts_data = [
        {
            'title': 'Django 入门教程：从零开始搭建博客',
            'slug': 'django-intro-blog-tutorial',
            'category': 'django',
            'tags': ['Django', 'Python'],
            'content': '''# Django 入门教程

这是一篇关于Django框架的入门教程。

## 环境准备

首先，你需要安装Python和Django。

```bash
pip install django
```

## 创建项目

使用以下命令创建Django项目：

```bash
django-admin startproject myblog
```

## 运行开发服务器

```bash
python manage.py runserver
```

现在你可以在浏览器中访问 http://localhost:8000 查看你的Django应用。

## 总结

Django是一个强大的Web框架，适合快速开发高质量的Web应用。
''',
        },
        {
            'title': 'Python 列表推导式详解',
            'slug': 'python-list-comprehension',
            'category': 'python',
            'tags': ['Python'],
            'content': '''# Python 列表推导式

列表推导式是Python中一种优雅的语法，可以让你用一行代码创建列表。

## 基本语法

```python
[expression for item in iterable]
```

## 示例

创建一个包含1到10平方的列表：

```python
squares = [x**2 for x in range(1, 11)]
print(squares)  # [1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
```

## 带条件的列表推导式

```python
even_squares = [x**2 for x in range(1, 11) if x % 2 == 0]
print(even_squares)  # [4, 16, 36, 64, 100]
```

## 总结

列表推导式是Python中非常强大的特性，掌握它可以让你的代码更加简洁和高效。
''',
        },
        {
            'title': 'Docker 容器化部署 Django 应用',
            'slug': 'docker-django-deployment',
            'category': 'tech',
            'tags': ['Docker', 'Django'],
            'content': '''# Docker 容器化部署 Django 应用

本文将介绍如何使用Docker容器化部署Django应用。

## 什么是Docker？

Docker是一个开源的容器化平台，可以让开发者将应用及其依赖打包到一个轻量级、可移植的容器中。

## 创建Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
```

## 创建docker-compose.yml

```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
```

## 启动容器

```bash
docker-compose up -d
```

## 总结

使用Docker部署Django应用可以确保应用在不同环境中一致运行，简化部署流程。
''',
        },
        {
            'title': '我的2023年终总结',
            'slug': '2023-year-review',
            'category': 'life',
            'tags': ['随笔'],
            'content': '''# 我的2023年终总结

时光飞逝，2023年已经接近尾声。

## 技术成长

这一年，我深入学习了多个技术栈：

- Django框架的高级用法
- Docker容器化技术
- 前端Vue框架

## 生活感悟

技术之外，我也有很多生活上的感悟。学会了平衡工作和生活，学会了慢下来享受过程。

## 展望2024

新的一年，我希望：

1. 深入学习云计算和DevOps
2. 多读一些非技术类书籍
3. 保持健康的作息和锻炼

感谢所有关注我的朋友们，我们明年再见！
''',
        },
        {
            'title': 'CSS Flexbox 布局完全指南',
            'slug': 'css-flexbox-guide',
            'category': 'tech',
            'tags': ['CSS', 'JavaScript'],
            'content': '''# CSS Flexbox 布局完全指南

Flexbox是CSS3中新增的一种布局模式，可以轻松实现各种复杂的布局需求。

## 基本概念

Flex布局由容器（flex container）和项目（flex item）组成。

```css
.container {
    display: flex;
}
```

## 容器属性

### flex-direction

控制主轴方向：

```css
.container {
    flex-direction: row | row-reverse | column | column-reverse;
}
```

### justify-content

控制主轴对齐方式：

```css
.container {
    justify-content: flex-start | flex-end | center | space-between | space-around;
}
```

### align-items

控制交叉轴对齐方式：

```css
.container {
    align-items: flex-start | flex-end | center | baseline | stretch;
}
```

## 项目属性

### flex-grow

控制项目的放大比例：

```css
.item {
    flex-grow: 1; /* 默认0，即不放大 */
}
```

## 总结

Flexbox是现代CSS布局的利器，掌握它可以让你轻松应对各种布局挑战。
''',
        },
    ]

    for post_data in posts_data:
        category = categories.get(post_data['category'])
        post, created = Post.objects.get_or_create(
            slug=post_data['slug'],
            defaults={
                'title': post_data['title'],
                'author': admin_user,
                'content': post_data['content'],
                'category': category,
                'status': 'published',
                'publish_date': timezone.now(),
            }
        )
        if created:
            # 添加标签
            post_tags = [tags[tag_name] for tag_name in post_data['tags'] if tag_name in tags]
            post.tags.set(post_tags)
            post.views = 100 + hash(post_data['title']) % 500  # 随机阅读量
            post.save()
            print(f'创建文章: {post_data["title"]}')

    # 创建友情链接
    links_data = [
        ('Django官网', 'https://www.djangoproject.com/', 'Django官方网站'),
        ('Python官网', 'https://www.python.org/', 'Python官方网站'),
        ('GitHub', 'https://github.com/', '代码托管平台'),
        ('Stack Overflow', 'https://stackoverflow.com/', '技术问答社区'),
    ]
    
    for name, url, desc in links_data:
        link, created = Link.objects.get_or_create(
            name=name,
            url=url,
            defaults={'description': desc}
        )
        if created:
            print(f'创建友情链接: {name}')

    # 创建静态页面
    pages_data = [
        {
            'title': '关于我',
            'slug': 'about',
            'page_type': 'about',
            'content': '''# 关于我

你好，欢迎来到我的博客！

我是一名热爱技术的开发者，专注于Python和Web开发领域。

## 技术栈

- **后端**: Python, Django, Flask
- **前端**: JavaScript, Vue, React
- **数据库**: MySQL, PostgreSQL, MongoDB
- **运维**: Docker, Linux, Nginx

## 联系方式

- GitHub: https://github.com
- Email: admin@example.com

欢迎交流！
''',
        },
        {
            'title': '友情链接',
            'slug': 'links',
            'page_type': 'links',
            'content': '''# 友情链接

欢迎各位站长交换友链！

## 友链申请要求

1. 网站内容健康，无违法违规内容
2. 原创内容为主，有一定更新频率
3. 已在贵站添加本站链接

## 本站信息

- 网站名称: 个人博客
- 网站地址: https://example.com
- 网站描述: 一个专注于技术分享的个人博客

申请友链请在下方留言或通过邮箱联系。
''',
        },
        {
            'title': '留言板',
            'slug': 'guestbook',
            'page_type': 'guestbook',
            'content': '''# 留言板

欢迎在此留言交流！

## 留言须知

1. 请文明发言，禁止人身攻击
2. 禁止发布广告和垃圾信息
3. 留言需经过审核后才会显示

感谢您的支持！
''',
        },
    ]
    
    for page_data in pages_data:
        page, created = Page.objects.get_or_create(
            page_type=page_data['page_type'],
            defaults={
                'title': page_data['title'],
                'slug': page_data['slug'],
                'content': page_data['content'],
            }
        )
        if created:
            print(f'创建静态页面: {page_data["title"]}')

    print('\n=== 测试数据创建完成 ===')

if __name__ == '__main__':
    create_test_data()
