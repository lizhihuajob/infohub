from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Post, Link, StaticPage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'parent', 'order', 'get_post_count', 'created_at']
    list_filter = ['parent', 'created_at']
    search_fields = ['name', 'description']
    prepopulated_fields = {'slug': ('name',)}
    ordering = ['order', 'name']

    def get_post_count(self, obj):
        return obj.get_post_count()
    get_post_count.short_description = '文章数量'


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'category', 'status', 'views', 'is_featured', 'published_at', 'created_at']
    list_filter = ['status', 'category', 'is_featured', 'created_at', 'author']
    search_fields = ['title', 'content', 'summary']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'published_at'
    ordering = ['-created_at']
    raw_id_fields = ['author']
    filter_horizontal = []

    fieldsets = (
        ('基本信息', {
            'fields': ('title', 'slug', 'author', 'category', 'tags')
        }),
        ('内容', {
            'fields': ('cover_image', 'summary', 'content')
        }),
        ('发布设置', {
            'fields': ('status', 'is_featured', 'allow_comments', 'published_at')
        }),
    )

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ['name', 'url', 'order', 'is_active', 'created_at']
    list_filter = ['is_active', 'created_at']
    search_fields = ['name', 'url', 'description']
    ordering = ['order', '-created_at']


@admin.register(StaticPage)
class StaticPageAdmin(admin.ModelAdmin):
    list_display = ['title', 'slug', 'page_type', 'is_published', 'updated_at']
    list_filter = ['page_type', 'is_published', 'created_at']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
