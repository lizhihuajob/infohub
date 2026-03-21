#!/bin/bash

set -e

# 创建数据目录
mkdir -p /app/data
mkdir -p /app/media
mkdir -p /app/staticfiles

# 设置数据目录权限
chmod 755 /app/data
chmod 755 /app/media
chmod 755 /app/staticfiles

# 清理可能存在的锁定文件
echo "清理数据库锁定文件..."
rm -f /app/data/db.sqlite3-journal
rm -f /app/data/db.sqlite3-wal
rm -f /app/data/db.sqlite3-shm

# 等待函数：检查数据库是否可用
wait_for_db() {
    local max_attempts=30
    local attempt=1

    while [ $attempt -le $max_attempts ]; do
        if python -c "
import sqlite3
import sys
try:
    conn = sqlite3.connect('/app/data/db.sqlite3', timeout=5)
    conn.execute('SELECT 1')
    conn.close()
    sys.exit(0)
except Exception as e:
    sys.exit(1)
" 2>/dev/null; then
            echo "数据库连接正常"
            return 0
        fi
        echo "等待数据库可用... ($attempt/$max_attempts)"
        sleep 2
        attempt=$((attempt + 1))
    done

    echo "数据库连接超时"
    return 1
}

# 运行数据库迁移（带重试）
run_migrations() {
    local max_attempts=5
    local attempt=1

    while [ $attempt -le $max_attempts ]; do
        echo "执行数据库迁移... (尝试 $attempt/$max_attempts)"

        # 先尝试创建表结构
        if python manage.py migrate --run-syncdb --noinput 2>&1; then
            echo "数据库迁移成功"
            return 0
        fi

        echo "迁移失败，等待重试..."
        sleep 3

        # 清理锁定文件后重试
        rm -f /app/data/db.sqlite3-journal
        rm -f /app/data/db.sqlite3-wal
        rm -f /app/data/db.sqlite3-shm

        attempt=$((attempt + 1))
    done

    echo "数据库迁移失败，已达到最大重试次数"
    return 1
}

# 主执行流程
main() {
    # 检查数据库文件是否存在且被锁定
    if [ -f /app/data/db.sqlite3 ]; then
        echo "检测到现有数据库文件"

        # 检查文件是否被其他进程占用
        if fuser /app/data/db.sqlite3 >/dev/null 2>&1; then
            echo "警告：数据库文件被其他进程占用，尝试等待..."
            sleep 5
        fi

        # 备份现有数据库（如果存在）
        if [ -f /app/data/db.sqlite3 ]; then
            echo "备份现有数据库..."
            cp /app/data/db.sqlite3 /app/data/db.sqlite3.backup.$(date +%Y%m%d_%H%M%S) 2>/dev/null || true
        fi
    fi

    # 执行迁移
    if ! run_migrations; then
        echo "迁移失败，尝试重新创建数据库..."

        # 如果迁移失败，删除损坏的数据库文件
        rm -f /app/data/db.sqlite3
        rm -f /app/data/db.sqlite3-journal
        rm -f /app/data/db.sqlite3-wal
        rm -f /app/data/db.sqlite3-shm

        # 重新执行迁移
        if ! run_migrations; then
            echo "错误：无法完成数据库迁移"
            exit 1
        fi
    fi

    # 收集静态文件
    echo "收集静态文件..."
    python manage.py collectstatic --noinput || true

    # 创建超级用户（如果不存在）- 使用环境变量
    SUPERUSER_USERNAME=${SUPERUSER_USERNAME:-admin}
    SUPERUSER_EMAIL=${SUPERUSER_EMAIL:-admin@example.com}
    SUPERUSER_PASSWORD=${SUPERUSER_PASSWORD:-}

    if [ -n "$SUPERUSER_PASSWORD" ]; then
        echo "检查超级用户..."
        python manage.py shell << EOF
from django.contrib.auth import get_user_model
import os
User = get_user_model()
username = os.environ.get('SUPERUSER_USERNAME', 'admin')
email = os.environ.get('SUPERUSER_EMAIL', 'admin@example.com')
password = os.environ.get('SUPERUSER_PASSWORD', '')
if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f'超级用户已创建: {username}')
else:
    print(f'超级用户已存在: {username}')
EOF
    else
        echo "警告: 未设置SUPERUSER_PASSWORD环境变量，跳过创建超级用户"
    fi

    echo "启动应用服务器..."

    # 根据环境选择启动方式
    if [ "${DEBUG:-False}" = "True" ] || [ "${DEBUG:-False}" = "true" ] || [ "${DEBUG:-False}" = "1" ]; then
        echo "使用Django开发服务器启动（DEBUG模式）"
        exec python manage.py runserver 0.0.0.0:8000
    else
        echo "使用Gunicorn启动（生产模式）"
        exec gunicorn myblog.wsgi:application --bind 0.0.0.0:8000 --workers 2 --threads 4 --timeout 60 --access-logfile - --error-logfile -
    fi
}

# 执行主函数
main
