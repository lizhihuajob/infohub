from django.db import models
from django.conf import settings


class Comment(models.Model):
    STATUS_CHOICES = (
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
        ('spam', '垃圾评论'),
    )

    post = models.ForeignKey(
        'blog.Post',
        on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='文章'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        related_name='replies',
        verbose_name='父评论'
    )
    author_name = models.CharField('姓名', max_length=50)
    author_email = models.EmailField('邮箱')
    author_url = models.URLField('网址', blank=True)
    content = models.TextField('评论内容')
    user_agent = models.CharField('用户代理', max_length=255, blank=True)
    ip_address = models.GenericIPAddressField('IP地址', null=True, blank=True)
    status = models.CharField('状态', max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author_name} - {self.post.title}'

    def is_reply(self):
        return self.parent is not None

    def get_approved_replies(self):
        return self.replies.filter(status='approved')


class GuestbookMessage(models.Model):
    STATUS_CHOICES = (
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
    )

    author_name = models.CharField('姓名', max_length=50)
    author_email = models.EmailField('邮箱')
    content = models.TextField('留言内容')
    status = models.CharField('状态', max_length=10, choices=STATUS_CHOICES, default='pending')
    ip_address = models.GenericIPAddressField('IP地址', null=True, blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '留言'
        verbose_name_plural = '留言板'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author_name} - {self.created_at.strftime("%Y-%m-%d")}'
