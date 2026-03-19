"""
博客应用的数据模型定义
"""
from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """
    博客文章分类模型
    用于对文章进行分类管理
    """
    name = models.CharField('分类名称', max_length=100, unique=True)
    description = models.TextField('分类描述', blank=True, default='')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
        ordering = ['-created_at']

    def __str__(self):
        return self.name


class Tag(models.Model):
    """
    博客文章标签模型
    用于给文章添加标签，便于检索
    """
    name = models.CharField('标签名称', max_length=50, unique=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'
        ordering = ['name']

    def __str__(self):
        return self.name


class Article(models.Model):
    """
    博客文章模型
    存储博客文章的核心内容
    """
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '已发布'),
    ]

    title = models.CharField('文章标题', max_length=200)
    summary = models.TextField('文章摘要', max_length=500, blank=True, default='')
    content = models.TextField('文章内容')
    cover_image = models.ImageField(
        '封面图片',
        upload_to='articles/covers/',
        blank=True,
        null=True
    )
    status = models.CharField(
        '发布状态',
        max_length=10,
        choices=STATUS_CHOICES,
        default='draft'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name='所属分类',
        related_name='articles'
    )
    tags = models.ManyToManyField(Tag, blank=True, verbose_name='标签', related_name='articles')
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='作者',
        related_name='articles'
    )
    view_count = models.PositiveIntegerField('阅读量', default=0)
    is_top = models.BooleanField('是否置顶', default=False)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-is_top', '-created_at']

    def __str__(self):
        return self.title

    def increase_view_count(self):
        """增加阅读量"""
        self.view_count += 1
        self.save(update_fields=['view_count'])


class Comment(models.Model):
    """
    文章评论模型
    允许访客对文章进行评论
    """
    article = models.ForeignKey(
        Article,
        on_delete=models.CASCADE,
        verbose_name='所属文章',
        related_name='comments'
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        null=True,
        blank=True,
        verbose_name='父评论',
        related_name='replies'
    )
    nickname = models.CharField('昵称', max_length=50)
    email = models.EmailField('邮箱', blank=True, default='')
    content = models.TextField('评论内容', max_length=1000)
    is_visible = models.BooleanField('是否显示', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.nickname}: {self.content[:20]}...'
