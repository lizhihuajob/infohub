#!/usr/bin/env python
"""
直接初始化数据库，绕过迁移系统的锁定问题
"""
import os
import sys
import sqlite3

# 删除旧数据库
if os.path.exists('db.sqlite3'):
    os.remove('db.sqlite3')
    print("Old database removed")

# 创建基础表结构
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# 启用WAL模式
cursor.execute("PRAGMA journal_mode = WAL;")
cursor.execute("PRAGMA synchronous = NORMAL;")
cursor.execute("PRAGMA temp_store = MEMORY;")
cursor.execute("PRAGMA mmap_size = 30000000000;")
conn.commit()

print("Database created with WAL mode enabled")

# 关闭连接
conn.close()

# 现在设置Django并创建表
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog.settings')

import django
django.setup()

from django.db import connection

# 打印所有模型
print("\nCreating database tables...")

# 使用syncdb创建表
from django.core.management import call_command
try:
    call_command('migrate', '--run-syncdb', verbosity=2)
    print("\nTables created successfully!")
except Exception as e:
    print(f"Error during migration: {e}")
    sys.exit(1)
