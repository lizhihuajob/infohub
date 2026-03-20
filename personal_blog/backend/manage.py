#!/usr/bin/env python
"""
Django 项目管理脚本
用于执行各种 Django 管理命令，如启动服务器、执行迁移、创建超级用户等
"""
import os
import sys


def main():
    """Django 管理命令入口函数"""
    # 设置默认的 Django 设置模块
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'blog_project.settings')
    
    try:
        # 导入 Django 的命令执行函数
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # 如果导入失败，给出友好的错误提示
        raise ImportError(
            "无法导入 Django。请确保 Django 已安装并在 "
            "PYTHONPATH 环境变量中可用。您是否忘记激活虚拟环境？"
        ) from exc
    
    # 执行命令行传入的管理命令
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()
