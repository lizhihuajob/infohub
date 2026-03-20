#!/bin/bash

# 创建数据目录
mkdir -p /app/data

# 运行数据库迁移
python manage.py migrate

# 创建超级用户（如果不存在）
python manage.py shell << EOF
from django.contrib.auth import get_user_model
User = get_user_model()
if not User.objects.filter(username='admin').exists():
    User.objects.create_superuser('admin', 'admin@example.com', 'admin123')
    print('超级用户已创建: admin / admin123')
else:
    print('超级用户已存在')
EOF

# 启动服务器
python manage.py runserver 0.0.0.0:8000
