# 个人博客系统

基于 Django + Vue 3 开发的个人博客网站。

## 技术栈

### 后端
- **Django 4.2** - Python Web 框架
- **Django REST Framework** - RESTful API 框架
- **SQLite** - 数据库（轻量级，无需额外配置）
- **django-cors-headers** - 跨域支持

### 前端
- **Vue 3** - 渐进式 JavaScript 框架
- **Element Plus** - UI 组件库
- **Vue Router** - 路由管理
- **Pinia** - 状态管理
- **Axios** - HTTP 客户端
- **Markdown-it** - Markdown 渲染
- **Highlight.js** - 代码高亮

### 部署
- **Docker** - 容器化部署
- **Docker Compose** - 多容器编排
- **Nginx** - 反向代理和静态文件服务

## 项目结构

```
personal_blog/
├── backend/                 # Django 后端
│   ├── blog/               # 博客应用
│   │   ├── models.py       # 数据模型
│   │   ├── views.py        # API 视图
│   │   ├── urls.py         # 路由配置
│   │   ├── admin.py        # 管理后台配置
│   │   └── serializers.py  # 序列化器
│   ├── blog_project/       # Django 项目配置
│   │   ├── settings.py     # 项目设置
│   │   ├── urls.py         # 根路由
│   │   └── wsgi.py         # WSGI 配置
│   ├── Dockerfile          # 后端 Docker 配置
│   ├── requirements.txt    # Python 依赖
│   └── manage.py           # Django 管理脚本
├── frontend/               # Vue 前端
│   ├── src/
│   │   ├── api/           # API 接口封装
│   │   ├── components/    # 公共组件
│   │   ├── views/         # 页面组件
│   │   │   ├── admin/    # 管理后台页面
│   │   │   └── ...       # 前台页面
│   │   ├── router/        # 路由配置
│   │   ├── utils/         # 工具函数
│   │   ├── App.vue        # 根组件
│   │   └── main.js        # 入口文件
│   ├── Dockerfile         # 前端 Docker 配置
│   ├── package.json       # Node.js 依赖
│   └── vite.config.js     # Vite 配置
├── nginx/                 # Nginx 配置
│   └── nginx.conf         # Nginx 配置文件
├── docker-compose.yml     # Docker Compose 配置
├── start.sh              # 启动脚本
├── stop.sh               # 停止脚本
└── README.md             # 项目说明
```

## 功能特性

### 前台功能
- ✅ 首页展示博客统计和最新文章
- ✅ 文章列表（支持搜索、分页）
- ✅ 文章详情（支持 Markdown 渲染、代码高亮）
- ✅ 文章分类浏览
- ✅ 标签云展示
- ✅ 响应式设计

### 管理后台
- ✅ 仪表盘统计
- ✅ 文章管理（创建、编辑、删除、发布）
- ✅ 分类管理
- ✅ 标签管理
- ✅ 支持 Markdown 编辑和实时预览

## 快速开始

### 环境要求
- Docker
- Docker Compose

### 启动项目

1. 克隆项目（或解压项目文件）
```bash
cd personal_blog
```

2. 运行启动脚本
```bash
./start.sh
```

3. 创建超级用户（首次运行）
```bash
docker-compose exec backend python manage.py createsuperuser
```

4. 访问服务
- 前端页面: http://localhost:5173
- 后端 API: http://localhost:8000
- Django 管理后台: http://localhost:8000/admin

### 停止项目

```bash
./stop.sh
```

## 常用命令

```bash
# 查看日志
docker-compose logs -f

# 查看后端日志
docker-compose logs -f backend

# 查看前端日志
docker-compose logs -f frontend

# 进入后端容器
docker-compose exec backend bash

# 进入前端容器
docker-compose exec frontend sh

# 执行 Django 命令
docker-compose exec backend python manage.py <command>

# 数据库迁移
docker-compose exec backend python manage.py migrate

# 创建超级用户
docker-compose exec backend python manage.py createsuperuser

# 重建容器
docker-compose up -d --build
```

## API 接口

### 文章接口
- `GET /api/blog/posts/` - 文章列表
- `GET /api/blog/posts/<slug>/` - 文章详情
- `POST /api/blog/posts/create/` - 创建文章
- `PUT /api/blog/posts/<id>/update/` - 更新文章
- `DELETE /api/blog/posts/<id>/delete/` - 删除文章
- `POST /api/blog/posts/<id>/publish/` - 发布文章

### 分类接口
- `GET /api/blog/categories/` - 分类列表
- `GET /api/blog/categories/<slug>/` - 分类详情

### 标签接口
- `GET /api/blog/tags/` - 标签列表
- `GET /api/blog/tags/<slug>/` - 标签详情

### 管理接口
- `GET /api/blog/admin/posts/` - 管理员文章列表（包含草稿）

### 统计接口
- `GET /api/blog/stats/` - 博客统计信息

## 开发说明

### 后端开发
- 后端代码位于 `backend/` 目录
- 使用 Django 的 MTV 架构
- API 使用 Django REST Framework 构建
- 数据库使用 SQLite，数据持久化在 `data/db/` 目录

### 前端开发
- 前端代码位于 `frontend/src/` 目录
- 使用 Vue 3 Composition API
- UI 组件使用 Element Plus
- 路由使用 Vue Router
- API 请求封装在 `api/` 目录

## 注意事项

1. **开发环境**：项目默认在开发模式下运行，如需生产部署请修改配置
2. **数据库**：使用 SQLite，数据存储在 Docker 卷中，删除容器不会丢失数据
3. **静态文件**：开发环境下由 Django 开发服务器提供，生产环境需要配置 Nginx
4. **跨域**：开发环境已配置 CORS，允许前端访问后端 API

## 后续计划

- [ ] 用户认证系统（JWT）
- [ ] 文章评论功能
- [ ] 文章点赞功能
- [ ] 全文搜索（Elasticsearch）
- [ ] 文章导入导出
- [ ] 主题切换
- [ ] 响应式图片处理
- [ ] SEO 优化

## 许可证

MIT License
