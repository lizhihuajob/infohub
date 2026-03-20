"""
Django 项目配置文件
包含所有项目级别的配置，如数据库、中间件、应用、静态文件等
"""

import os
from pathlib import Path

# 项目根目录
# BASE_DIR 指向包含 manage.py 的目录
BASE_DIR = Path(__file__).resolve().parent.parent

# 数据目录（用于存放 SQLite 数据库等）
DATA_DIR = BASE_DIR / 'data'
DATA_DIR.mkdir(exist_ok=True)

# =============================================================================
# 安全设置
# =============================================================================

# 安全密钥（生产环境必须更改）
# 从环境变量读取，如果不存在则使用默认值（仅开发环境）
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-dev-key-change-in-production')

# 调试模式
# 开发环境设为 True，生产环境必须设为 False
DEBUG = os.environ.get('DEBUG', '1') == '1'

# 允许访问的主机
# 开发环境允许所有主机，生产环境需要指定具体域名
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '*').split(',')


# =============================================================================
# 应用配置
# =============================================================================

# Django 内置应用
DJANGO_APPS = [
    'django.contrib.admin',      # 管理后台
    'django.contrib.auth',       # 认证系统
    'django.contrib.contenttypes',  # 内容类型框架
    'django.contrib.sessions',   # 会话管理
    'django.contrib.messages',   # 消息框架
    'django.contrib.staticfiles',  # 静态文件管理
]

# 第三方应用
THIRD_PARTY_APPS = [
    'rest_framework',            # Django REST Framework
    'corsheaders',               # 跨域资源共享
    'django_filters',            # Django 过滤器
]

# 自定义应用
LOCAL_APPS = [
    'blog',                      # 博客应用
]

# 合并所有应用
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS


# =============================================================================
# 中间件配置
# =============================================================================

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # 跨域中间件（必须在最前面）
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# =============================================================================
# URL 和模板配置
# =============================================================================

# 根 URL 配置
ROOT_URLCONF = 'blog_project.urls'

# 模板配置
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # 项目级模板目录
        'APP_DIRS': True,  # 允许从应用中加载模板
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

# WSGI 应用入口
WSGI_APPLICATION = 'blog_project.wsgi.application'


# =============================================================================
# 数据库配置
# 使用 SQLite（根据要求不使用 MySQL）
# =============================================================================

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': DATA_DIR / 'db.sqlite3',
    }
}


# =============================================================================
# 密码验证
# =============================================================================

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# =============================================================================
# 国际化配置
# =============================================================================

# 语言代码
LANGUAGE_CODE = 'zh-hans'  # 简体中文

# 时区
TIME_ZONE = 'Asia/Shanghai'

# 启用国际化
USE_I18N = True

# 启用时区支持
USE_TZ = True


# =============================================================================
# 静态文件和媒体文件配置
# =============================================================================

# 静态文件 URL
STATIC_URL = 'static/'

# 静态文件收集目录（生产环境使用）
STATIC_ROOT = BASE_DIR / 'staticfiles'

# 媒体文件配置（用户上传的文件）
MEDIA_URL = '/media/'
MEDIA_ROOT = DATA_DIR / 'media'


# =============================================================================
# 主键字段类型
# =============================================================================

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# =============================================================================
# Django REST Framework 配置
# =============================================================================

REST_FRAMEWORK = {
    # 默认权限类
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',  # 开发环境允许所有访问
    ],
    # 默认分页类
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    # 默认渲染器
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
}


# =============================================================================
# 跨域资源共享 (CORS) 配置
# =============================================================================

# 允许所有来源（开发环境）
CORS_ALLOW_ALL_ORIGINS = True

# 允许的 HTTP 方法
CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]

# 允许的请求头
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]


# =============================================================================
# 日志配置（可选）
# =============================================================================

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}
