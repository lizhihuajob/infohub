# Django 个人博客使用说明

## 项目概述

基于 Django 4.2 开发的个人博客系统，支持 Markdown 文章编辑、分类标签管理、评论系统、搜索功能等。

## 快速开始

### 1. 启动服务

```bash
docker-compose up -d
```

服务启动后访问：http://localhost:8080

### 2. 创建数据库表

```bash
docker-compose run web python manage.py migrate
```

### 3. 创建超级用户

```bash
# 方式一：使用脚本创建（用户名：admin，密码：admin123456）
docker-compose run web python create_superuser.py

# 方式二：交互式创建
docker-compose run web python manage.py createsuperuser
```

### 4. 创建测试数据（可选）

```bash
docker-compose run web python create_test_data.py
```

### 5. 访问后台管理

后台地址：http://localhost:8080/admin/

使用超级用户账号登录，可管理文章、分类、标签、评论等内容。

## 主要功能

### 前台功能

- **首页**：最新文章列表、分页、热门文章、分类目录、标签云
- **文章详情**：Markdown 内容渲染、代码高亮、目录导航、上/下一篇导航
- **分类/标签归档**：按分类或标签筛选文章
- **搜索**：支持按标题和内容关键词搜索
- **静态页面**：关于我、友情链接、留言板
- **评论系统**：支持访客评论、嵌套回复、审核机制

### 后台功能

- **文章管理**：Markdown 编辑器、封面上传、状态管理
- **分类/标签管理**：层级分类、标签管理
- **评论审核**：待审核评论列表、一键通过/拒绝
- **媒体管理**：图片上传与管理
- **友情链接**：合作站点管理

## 项目结构

```
.
├── blog/                    # 项目配置目录
│   ├── settings.py          # Django 配置
│   ├── urls.py              # URL 路由
│   └── wsgi.py              # WSGI 配置
├── blogapp/                 # 博客应用
│   ├── models.py            # 数据模型
│   ├── views.py             # 视图逻辑
│   ├── forms.py             # 表单定义
│   ├── admin.py             # 后台管理配置
│   ├── urls.py              # 应用 URL 路由
│   └── migrations/          # 数据库迁移文件
├── templates/               # 模板目录
│   ├── base.html            # 基础模板
│   └── blogapp/             # 应用模板
├── static/                  # 静态文件
├── media/                   # 媒体上传目录
├── Dockerfile               # Docker 构建配置
├── docker-compose.yml       # Docker Compose 配置
├── requirements.txt         # Python 依赖
├── create_superuser.py      # 超级用户创建脚本
└── create_test_data.py      # 测试数据创建脚本
```

## 开发说明

### 安装新依赖

修改 `requirements.txt` 后，重新构建镜像：

```bash
docker-compose build --no-cache
```

### 数据库迁移

```bash
# 创建迁移文件
docker-compose run web python manage.py makemigrations

# 执行迁移
docker-compose run web python manage.py migrate
```

### 收集静态文件（生产环境）

```bash
docker-compose run web python manage.py collectstatic
```

## 技术栈

- **框架**: Django 4.2
- **数据库**: SQLite3（开发环境）
- **Markdown**: markdown + django-markdownx
- **图片处理**: django-imagekit + Pillow
- **前端框架**: Bootstrap 5.3
- **容器化**: Docker + Docker Compose

## 注意事项

1. 生产环境请修改 `DEBUG = False`，并配置合适的数据库（如 PostgreSQL）
2. 请修改默认的 `SECRET_KEY` 和管理员密码
3. 建议配置 HTTPS 确保数据传输安全
4. 可根据需要配置邮件服务、缓存、CDN 等
