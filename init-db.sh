#!/bin/bash
# 初始化数据库脚本

echo "正在初始化数据库..."

# 执行数据库迁移
docker-compose exec backend python manage.py migrate

# 创建超级管理员
echo ""
echo "请创建超级管理员账户:"
docker-compose exec backend python manage.py createsuperuser

echo ""
echo "数据库初始化完成！"
