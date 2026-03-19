"""
博客应用配置
定义应用的基本信息和配置
"""

from django.apps import AppConfig


class BlogConfig(AppConfig):
    """
    博客应用配置类
    
    属性:
        default_auto_field: 默认自动字段类型
        name: 应用名称（Python 包路径）
        verbose_name: 应用的中文显示名称
    """
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog'
    verbose_name = '博客管理'
    
    def ready(self):
        """
        应用就绪时执行的初始化操作
        可用于注册信号处理器等
        """
        pass
