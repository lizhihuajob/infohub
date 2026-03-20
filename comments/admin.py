from django.contrib import admin
from .models import Comment, GuestbookMessage


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'post', 'status', 'created_at', 'ip_address']
    list_filter = ['status', 'created_at']
    search_fields = ['author_name', 'author_email', 'content', 'post__title']
    actions = ['approve_comments', 'reject_comments', 'mark_as_spam']

    def approve_comments(self, request, queryset):
        count = queryset.update(status='approved')
        self.message_user(request, f'已通过 {count} 条评论。')
    approve_comments.short_description = '通过所选评论'

    def reject_comments(self, request, queryset):
        count = queryset.update(status='rejected')
        self.message_user(request, f'已拒绝 {count} 条评论。')
    reject_comments.short_description = '拒绝所选评论'

    def mark_as_spam(self, request, queryset):
        count = queryset.update(status='spam')
        self.message_user(request, f'已标记 {count} 条评论为垃圾评论。')
    mark_as_spam.short_description = '标记为垃圾评论'


@admin.register(GuestbookMessage)
class GuestbookMessageAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'status', 'created_at', 'ip_address']
    list_filter = ['status', 'created_at']
    search_fields = ['author_name', 'author_email', 'content']
    actions = ['approve_messages', 'reject_messages']

    def approve_messages(self, request, queryset):
        count = queryset.update(status='approved')
        self.message_user(request, f'已通过 {count} 条留言。')
    approve_messages.short_description = '通过所选留言'

    def reject_messages(self, request, queryset):
        count = queryset.update(status='rejected')
        self.message_user(request, f'已拒绝 {count} 条留言。')
    reject_messages.short_description = '拒绝所选留言'
