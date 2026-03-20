#!/usr/bin/env python
"""
直接通过SQL创建数据库表，绕过Django迁移的锁定问题
"""
import os
import sqlite3

# 删除旧数据库
if os.path.exists('db.sqlite3'):
    os.remove('db.sqlite3')
    print("Old database removed")

conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

# 基本配置
cursor.execute("PRAGMA journal_mode = DELETE;")
cursor.execute("PRAGMA synchronous = FULL;")
cursor.execute("PRAGMA foreign_keys = ON;")

# 创建Django系统表
cursor.execute("""
CREATE TABLE IF NOT EXISTS django_migrations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    app VARCHAR(255) NOT NULL,
    name VARCHAR(255) NOT NULL,
    applied DATETIME NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS django_content_type (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    app_label VARCHAR(100) NOT NULL,
    model VARCHAR(100) NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS django_session (
    session_key VARCHAR(40) PRIMARY KEY,
    session_data TEXT NOT NULL,
    expire_date DATETIME NOT NULL
);
""")

# 创建auth表
cursor.execute("""
CREATE TABLE IF NOT EXISTS auth_user (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    password VARCHAR(128) NOT NULL,
    last_login DATETIME NULL,
    is_superuser BOOL NOT NULL,
    username VARCHAR(150) NOT NULL UNIQUE,
    last_name VARCHAR(150) NOT NULL,
    email VARCHAR(254) NOT NULL,
    is_staff BOOL NOT NULL,
    is_active BOOL NOT NULL,
    date_joined DATETIME NOT NULL,
    first_name VARCHAR(150) NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS auth_group (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(150) NOT NULL UNIQUE
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS auth_permission (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(255) NOT NULL,
    content_type_id INTEGER NOT NULL,
    codename VARCHAR(100) NOT NULL,
    FOREIGN KEY (content_type_id) REFERENCES django_content_type (id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS auth_user_groups (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    group_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES auth_user (id),
    FOREIGN KEY (group_id) REFERENCES auth_group (id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS auth_group_permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    group_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL,
    FOREIGN KEY (group_id) REFERENCES auth_group (id),
    FOREIGN KEY (permission_id) REFERENCES auth_permission (id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS auth_user_user_permissions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    permission_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES auth_user (id),
    FOREIGN KEY (permission_id) REFERENCES auth_permission (id)
);
""")

# 创建admin表
cursor.execute("""
CREATE TABLE IF NOT EXISTS django_admin_log (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action_time DATETIME NOT NULL,
    object_id TEXT NULL,
    object_repr VARCHAR(200) NOT NULL,
    action_flag SMALLINT UNSIGNED NOT NULL,
    change_message TEXT NOT NULL,
    content_type_id INTEGER NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (content_type_id) REFERENCES django_content_type (id),
    FOREIGN KEY (user_id) REFERENCES auth_user (id)
);
""")

# 创建blogapp表
cursor.execute("""
CREATE TABLE IF NOT EXISTS blogapp_category (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(50) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    parent_id INTEGER NULL,
    FOREIGN KEY (parent_id) REFERENCES blogapp_category (id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS blogapp_tag (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    slug VARCHAR(50) NOT NULL UNIQUE,
    created_at DATETIME NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS blogapp_post (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    slug VARCHAR(50) NOT NULL,
    content TEXT NOT NULL,
    excerpt VARCHAR(500) NOT NULL,
    cover_image VARCHAR(100) NULL,
    status VARCHAR(20) NOT NULL,
    views INTEGER UNSIGNED NOT NULL,
    publish_date DATETIME NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    author_id INTEGER NOT NULL,
    category_id INTEGER NULL,
    FOREIGN KEY (author_id) REFERENCES auth_user (id),
    FOREIGN KEY (category_id) REFERENCES blogapp_category (id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS blogapp_post_tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    post_id INTEGER NOT NULL,
    tag_id INTEGER NOT NULL,
    FOREIGN KEY (post_id) REFERENCES blogapp_post (id),
    FOREIGN KEY (tag_id) REFERENCES blogapp_tag (id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS blogapp_comment (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_name VARCHAR(100) NOT NULL,
    author_email VARCHAR(254) NOT NULL,
    author_url VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    post_id INTEGER NOT NULL,
    parent_id INTEGER NULL,
    FOREIGN KEY (post_id) REFERENCES blogapp_post (id),
    FOREIGN KEY (parent_id) REFERENCES blogapp_comment (id)
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS blogapp_link (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name VARCHAR(100) NOT NULL,
    url VARCHAR(200) NOT NULL,
    description TEXT NOT NULL,
    created_at DATETIME NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS blogapp_page (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title VARCHAR(200) NOT NULL,
    slug VARCHAR(50) NOT NULL UNIQUE,
    content TEXT NOT NULL,
    page_type VARCHAR(20) NOT NULL UNIQUE,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS blogapp_guestbook (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    author_name VARCHAR(100) NOT NULL,
    author_email VARCHAR(254) NOT NULL,
    author_url VARCHAR(200) NOT NULL,
    content TEXT NOT NULL,
    status VARCHAR(20) NOT NULL,
    created_at DATETIME NOT NULL
);
""")

# 创建索引
cursor.execute("CREATE INDEX IF NOT EXISTS idx_post_status ON blogapp_post(status);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_post_publish ON blogapp_post(publish_date);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_post_slug ON blogapp_post(slug);")
cursor.execute("CREATE INDEX IF NOT EXISTS idx_comment_status ON blogapp_comment(status);")

conn.commit()
conn.close()

print("All tables created successfully!")

# 创建超级用户
os.environ['DJANGO_SETTINGS_MODULE'] = 'blog.settings'
import django
django.setup()

from django.contrib.auth.models import User
from django.utils import timezone

if not User.objects.filter(username='admin').exists():
    user = User.objects.create(
        username='admin',
        email='admin@example.com',
        is_staff=True,
        is_superuser=True,
        is_active=True,
        date_joined=timezone.now(),
        first_name='Admin',
        last_name='User'
    )
    user.set_password('admin123456')
    user.save()
    print("Superuser created: admin / admin123456")
else:
    print("Superuser already exists")
