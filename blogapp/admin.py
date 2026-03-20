from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Tag, Post, Comment, Link, Page, Guestbook


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'parent', 'created_at')
    list_filter = ('parent', 'created_at')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'created_at')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0
    fields = ('author_name', 'author_email', 'content', 'status', 'created_at')
    readonly_fields = ('created_at',)


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'status', 'views', 'publish_date', 'cover_image_preview')
    list_filter = ('status', 'category', 'tags', 'publish_date')
    search_fields = ('title', 'content', 'excerpt')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)
    inlines = [CommentInline]
    actions = ['make_published', 'make_draft']
    date_hierarchy = 'publish_date'
    readonly_fields = ('views', 'cover_image_preview')

    def cover_image_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" style="max-height: 50px;"/>', obj.cover_thumbnail.url)
        return '-'
    cover_image_preview.short_description = '封面预览'

    def make_published(self, request, queryset):
        queryset.update(status='published')
    make_published.short_description = '标记为已发布'

    def make_draft(self, request, queryset):
        queryset.update(status='draft')
    make_draft.short_description = '标记为草稿'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'author_email', 'post', 'status', 'created_at', 'content_summary')
    list_filter = ('status', 'created_at', 'post')
    search_fields = ('author_name', 'author_email', 'content')
    actions = ['approve_comments', 'reject_comments']
    readonly_fields = ('created_at', 'updated_at')

    def content_summary(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_summary.short_description = '内容摘要'

    def approve_comments(self, request, queryset):
        queryset.update(status='approved')
    approve_comments.short_description = '通过审核'

    def reject_comments(self, request, queryset):
        queryset.update(status='rejected')
    reject_comments.short_description = '拒绝/删除'


@admin.register(Link)
class LinkAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', 'created_at')
    search_fields = ('name', 'url')


@admin.register(Page)
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'page_type', 'updated_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}


@admin.register(Guestbook)
class GuestbookAdmin(admin.ModelAdmin):
    list_display = ('author_name', 'author_email', 'status', 'created_at', 'content_summary')
    list_filter = ('status', 'created_at')
    search_fields = ('author_name', 'author_email', 'content')
    actions = ['approve_messages', 'reject_messages']

    def content_summary(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
    content_summary.short_description = '内容摘要'

    def approve_messages(self, request, queryset):
        queryset.update(status='approved')
    approve_messages.short_description = '通过审核'

    def reject_messages(self, request, queryset):
        queryset.update(status='rejected')
    reject_messages.short_description = '拒绝/删除'
