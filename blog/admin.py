from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Tag, Post, Comment, Page, Link


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'order', 'created_at']
    list_filter = ['parent']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    list_editable = ['order']


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    search_fields = ['name']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'views', 'published_at', 'is_published']
    list_filter = ['status', 'category', 'tags', 'created_at']
    search_fields = ['title', 'content', 'summary']
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ['tags']
    date_hierarchy = 'published_at'
    list_editable = ['status']
    
    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'slug', 'author', 'category', 'tags')
        }),
        ('内容', {
            'fields': ('summary', 'content', 'cover_image')
        }),
        ('状态', {
            'fields': ('status', 'views', 'published_at')
        }),
    )
    
    def is_published(self, obj):
        return obj.status == 'published'
    is_published.boolean = True
    is_published.short_description = '已发布'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.select_related('author', 'category').prefetch_related('tags')


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['name', 'post', 'status', 'is_spam', 'created_at', 'short_content']
    list_filter = ['status', 'is_spam', 'created_at']
    search_fields = ['name', 'email', 'content', 'post__title']
    list_editable = ['status', 'is_spam']
    actions = ['approve_comments', 'reject_comments', 'mark_as_spam']
    
    def short_content(self, obj):
        return obj.content[:100] + '...' if len(obj.content) > 100 else obj.content
    short_content.short_description = '评论内容'
    
    @admin.action(description='通过选中的评论')
    def approve_comments(self, request, queryset):
        queryset.update(status='approved')
    
    @admin.action(description='拒绝选中的评论')
    def reject_comments(self, request, queryset):
        queryset.update(status='rejected')
    
    @admin.action(description='标记为垃圾评论')
    def mark_as_spam(self, request, queryset):
        queryset.update(is_spam=True, status='rejected')


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ['title', 'page_type', 'is_published', 'order', 'created_at']
    list_filter = ['page_type', 'is_published']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ['is_published', 'order']


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'description', 'is_active', 'order']
    list_filter = ['is_active']
    search_fields = ['name', 'url', 'description']
    list_editable = ['is_active', 'order']
