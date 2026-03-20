import sqlite3
import os

# 删除旧数据库
if os.path.exists('db.sqlite3'):
    os.remove('db.sqlite3')
    print("Old database removed")

# 创建新数据库并禁用WAL模式
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()
cursor.execute("PRAGMA journal_mode = DELETE;")
cursor.execute("PRAGMA synchronous = FULL;")
conn.commit()
conn.close()
print("New database created with DELETE journal mode")
