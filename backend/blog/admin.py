"""
博客应用的Admin配置
用于Django管理后台
"""
from django.contrib import admin
from .models import Category, Tag, Article, Comment


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    分类管理配置
    """
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']
    ordering = ['-created_at']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    """
    标签管理配置
    """
    list_display = ['name', 'created_at']
    search_fields = ['name']
    ordering = ['name']


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    """
    文章管理配置
    """
    list_display = ['title', 'status', 'category', 'author', 'view_count', 'is_top', 'created_at']
    list_filter = ['status', 'category', 'is_top', 'created_at']
    search_fields = ['title', 'content']
    filter_horizontal = ['tags']
    ordering = ['-is_top', '-created_at']
    date_hierarchy = 'created_at'

    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'summary', 'content', 'cover_image')
        }),
        ('分类与标签', {
            'fields': ('category', 'tags')
        }),
        ('发布设置', {
            'fields': ('status', 'is_top', 'author')
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    """
    评论管理配置
    """
    list_display = ['nickname', 'article', 'content', 'is_visible', 'created_at']
    list_filter = ['is_visible', 'created_at']
    search_fields = ['nickname', 'content', 'article__title']
    ordering = ['-created_at']
    actions = ['make_visible', 'make_invisible']

    def make_visible(self, request, queryset):
        """批量设置评论为可见"""
        count = queryset.update(is_visible=True)
        self.message_user(request, f'成功设置 {count} 条评论为可见')

    def make_invisible(self, request, queryset):
        """批量设置评论为不可见"""
        count = queryset.update(is_visible=False)
        self.message_user(request, f'成功设置 {count} 条评论为不可见')

    make_visible.short_description = '设置所选评论为可见'
    make_invisible.short_description = '设置所选评论为不可见'
