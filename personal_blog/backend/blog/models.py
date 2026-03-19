"""
博客应用数据模型
定义博客文章、分类、标签等数据模型
"""

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Category(models.Model):
    """
    文章分类模型
    
    用于对文章进行分类管理，如技术、生活、随笔等
    
    属性:
        name: 分类名称
        slug: URL 友好的标识符
        description: 分类描述
        created_at: 创建时间
    """
    name = models.CharField(
        max_length=100,
        verbose_name='分类名称',
        help_text='分类的显示名称'
    )
    slug = models.SlugField(
        max_length=100,
        unique=True,
        verbose_name='URL标识',
        help_text='用于URL的短标识，如 tech、life 等'
    )
    description = models.TextField(
        blank=True,
        verbose_name='分类描述',
        help_text='对分类的简要描述'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    
    class Meta:
        # 数据库表名
        db_table = 'blog_categories'
        # 单数显示名称
        verbose_name = '文章分类'
        # 复数显示名称
        verbose_name_plural = '文章分类'
        # 默认排序方式
        ordering = ['-created_at']
    
    def __str__(self):
        """返回分类名称的字符串表示"""
        return self.name


class Tag(models.Model):
    """
    文章标签模型
    
    用于给文章添加标签，便于检索和关联
    
    属性:
        name: 标签名称
        slug: URL 友好的标识符
        created_at: 创建时间
    """
    name = models.CharField(
        max_length=50,
        verbose_name='标签名称',
        help_text='标签的显示名称'
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
        verbose_name='URL标识',
        help_text='用于URL的短标识'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    
    class Meta:
        db_table = 'blog_tags'
        verbose_name = '文章标签'
        verbose_name_plural = '文章标签'
        ordering = ['-created_at']
    
    def __str__(self):
        """返回标签名称的字符串表示"""
        return self.name


class Post(models.Model):
    """
    博客文章模型
    
    这是博客系统的核心模型，存储所有文章信息
    
    属性:
        title: 文章标题
        slug: URL 友好的标识符
        author: 作者（外键关联到 User 模型）
        category: 所属分类
        tags: 关联标签（多对多关系）
        summary: 文章摘要
        content: 文章内容（支持 Markdown）
        cover_image: 封面图片
        status: 发布状态（草稿/已发布）
        views: 浏览次数
        is_top: 是否置顶
        created_at: 创建时间
        updated_at: 更新时间
        published_at: 发布时间
    """
    
    # 文章状态选项
    class Status(models.TextChoices):
        """文章发布状态枚举"""
        DRAFT = 'draft', '草稿'
        PUBLISHED = 'published', '已发布'
    
    title = models.CharField(
        max_length=200,
        verbose_name='文章标题',
        help_text='文章的标题，建议简洁明了'
    )
    slug = models.SlugField(
        max_length=200,
        unique=True,
        verbose_name='URL标识',
        help_text='用于URL的短标识，如 my-first-post'
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='blog_posts',
        verbose_name='作者'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='所属分类'
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name='posts',
        verbose_name='标签'
    )
    summary = models.TextField(
        max_length=500,
        blank=True,
        verbose_name='文章摘要',
        help_text='文章的简短描述，用于列表展示'
    )
    content = models.TextField(
        verbose_name='文章内容',
        help_text='支持 Markdown 格式的文章内容'
    )
    cover_image = models.ImageField(
        upload_to='posts/covers/%Y/%m/',
        blank=True,
        null=True,
        verbose_name='封面图片',
        help_text='文章的封面图片'
    )
    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.DRAFT,
        verbose_name='发布状态'
    )
    views = models.PositiveIntegerField(
        default=0,
        verbose_name='浏览次数'
    )
    is_top = models.BooleanField(
        default=False,
        verbose_name='是否置顶',
        help_text='置顶文章会在列表中优先显示'
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='创建时间'
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name='更新时间'
    )
    published_at = models.DateTimeField(
        null=True,
        blank=True,
        verbose_name='发布时间'
    )
    
    class Meta:
        db_table = 'blog_posts'
        verbose_name = '博客文章'
        verbose_name_plural = '博客文章'
        # 排序：置顶优先，然后按发布时间倒序
        ordering = ['-is_top', '-published_at', '-created_at']
        # 添加数据库索引，优化查询性能
        indexes = [
            models.Index(fields=['-created_at']),
            models.Index(fields=['status', '-created_at']),
            models.Index(fields=['slug']),
        ]
    
    def __str__(self):
        """返回文章标题的字符串表示"""
        return self.title
    
    def publish(self):
        """
        发布文章
        将状态改为已发布，并设置发布时间
        """
        self.status = self.Status.PUBLISHED
        self.published_at = timezone.now()
        self.save()
    
    def increase_views(self):
        """
        增加浏览次数
        用于统计文章阅读量
        """
        self.views += 1
        self.save(update_fields=['views'])
    
    @property
    def is_published(self):
        """
        检查文章是否已发布
        
        返回:
            bool: 如果文章已发布返回 True，否则返回 False
        """
        return self.status == self.Status.PUBLISHED
