#!/bin/bash

# 创建必要的目录
mkdir -p /app/data /app/staticfiles /app/media

# 如果data目录中的数据库为空或不存在，从内置数据库复制
if [ -f /app/data_initial/db.sqlite3 ]; then
    if [ ! -f /app/data/db.sqlite3 ] || [ ! -s /app/data/db.sqlite3 ]; then
        echo "初始化新数据库..."
        cp /app/data_initial/db.sqlite3 /app/data/
        echo "数据库初始化完成"
    else
        echo "使用现有数据库"
    fi
else
    echo "警告: 没有找到初始数据库文件，将创建新数据库"
fi

# 运行数据库迁移（仅当有新迁移时）
echo "检查/运行数据库迁移..."
python manage.py migrate --noinput || echo "迁移命令执行完成（可能没有新迁移）"

# 收集静态文件
python manage.py collectstatic --noinput

# 直接通过Django shell创建超级用户
echo "检查/创建超级用户..."
cat > /tmp/create_superuser.py << 'ENDOFFILE
import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myblog.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()
username = os.environ.get('DJANGO_SUPERUSER_USERNAME', 'admin')
email = os.environ.get('DJANGO_SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('DJANGO_SUPERUSER_PASSWORD', 'admin123')

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'超级用户已创建: {username}')
else:
    print(f'超级用户已存在: {username}')
ENDOFFILE

python /tmp/create_superuser.py
rm -f /tmp/create_superuser.py

# 启动Gunicorn服务器（生产环境）
if [ "$DEBUG" = "1" ]; then
    echo "启动开发服务器..."
    python manage.py runserver 0.0.0.0:8000
else
    echo "启动Gunicorn生产服务器..."
    gunicorn --workers=1 --bind=0.0.0.0:8000 --timeout=120 myblog.wsgi:application
fi
