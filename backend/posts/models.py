from django.db import models
from django.utils import timezone


class Post(models.Model):
    """博客文章模型"""
    title = models.CharField(max_length=200, verbose_name='标题')
    content = models.TextField(verbose_name='内容')
    author = models.CharField(max_length=100, verbose_name='作者', default='admin')
    created_time = models.DateTimeField(default=timezone.now, verbose_name='创建时间')
    updated_time = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    is_published = models.BooleanField(default=True, verbose_name='是否发布')
    views = models.PositiveIntegerField(default=0, verbose_name='浏览量')

    class Meta:
        verbose_name = '博客文章'
        verbose_name_plural = verbose_name
        ordering = ['-created_time']

    def __str__(self):
        return self.title

    def increase_views(self):
        """增加浏览量"""
        self.views += 1
        self.save(update_fields=['views'])
