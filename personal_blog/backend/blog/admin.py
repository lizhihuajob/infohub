"""
博客应用管理后台配置
定义 Django Admin 中博客模型的展示和编辑方式
"""

from django.contrib import admin
from .models import Category, Tag, Post


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    分类模型管理配置
    
    定义分类在管理后台的列表展示、搜索、编辑等行为
    """
    # 列表页显示的字段
    list_display = ['name', 'slug', 'post_count', 'created_at']
    # 可搜索的字段
    search_fields = ['name', 'description']
    # 可编辑的字段
    fields = ['name', 'slug', 'description']
    # 预填充字段（根据 name 自动生成 slug）
    prepopulated_fields = {'slug': ['name']}
    
    def post_count(self, obj):
        """
        计算分类下的文章数量
        
        参数:
            obj: Category 实例
            
        返回:
            int: 该分类下的文章数量
        """
        return obj.posts.count()
    post_count.short_description = '文章数量'


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    标签模型管理配置
    
    定义标签在管理后台的列表展示、搜索、编辑等行为
    """
    list_display = ['name', 'slug', 'post_count', 'created_at']
    search_fields = ['name']
    fields = ['name', 'slug']
    prepopulated_fields = {'slug': ['name']}
    
    def post_count(self, obj):
        """
        计算标签关联的文章数量
        
        参数:
            obj: Tag 实例
            
        返回:
            int: 使用该标签的文章数量
        """
        return obj.posts.count()
    post_count.short_description = '文章数量'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    """
    文章模型管理配置
    
    定义文章在管理后台的列表展示、搜索、筛选、编辑等行为
    这是管理后台最常用的功能，提供了完整的文章管理界面
    """
    # 列表页显示的字段
    list_display = [
        'title', 'author', 'category', 'status', 
        'is_top', 'views', 'published_at', 'created_at'
    ]
    # 列表页可筛选的字段
    list_filter = ['status', 'category', 'tags', 'is_top', 'created_at']
    # 可搜索的字段
    search_fields = ['title', 'content', 'summary']
    # 只读字段（不可编辑）
    readonly_fields = ['views', 'created_at', 'updated_at']
    # 默认排序
    ordering = ['-is_top', '-created_at']
    # 分页设置
    list_per_page = 20
    
    # 字段分组（编辑页面）
    fieldsets = (
        # 基本信息组
        ('基本信息', {
            'fields': ('title', 'slug', 'author', 'category', 'tags')
        }),
        # 内容组
        ('内容', {
            'fields': ('summary', 'content', 'cover_image')
        }),
        # 发布设置组
        ('发布设置', {
            'fields': ('status', 'is_top', 'published_at')
        }),
        # 统计信息组（折叠显示）
        ('统计信息', {
            'fields': ('views', 'created_at', 'updated_at'),
            'classes': ('collapse',)  # 折叠显示
        }),
    )
    
    # 预填充字段
    prepopulated_fields = {'slug': ['title']}
    
    # 多对多字段的展示方式
    filter_horizontal = ['tags']
    
    # 日期层级筛选
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        """
        获取文章查询集
        
        预加载关联数据，优化查询性能
        
        参数:
            request: HTTP 请求对象
            
        返回:
            QuerySet: 优化后的文章查询集
        """
        qs = super().get_queryset(request)
        # 预加载外键关联数据，减少数据库查询次数
        return qs.select_related('author', 'category').prefetch_related('tags')
    
    def save_model(self, request, obj, form, change):
        """
        保存文章模型
        
        自动设置作者为当前登录用户
        
        参数:
            request: HTTP 请求对象
            obj: Post 实例
            form: 表单实例
            change: 是否为修改操作
        """
        # 如果是新建文章，自动设置作者
        if not change:
            obj.author = request.user
        super().save_model(request, obj, form, change)
