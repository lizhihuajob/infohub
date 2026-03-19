#!/usr/bin/env python
"""
Django项目的命令行工具入口
"""
import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blog_project.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "无法导入Django。请确保已安装Django并且 "
            "PYTHONPATH环境变量中包含您的虚拟环境。"
        ) from exc
    execute_from_command_line(sys.argv)
