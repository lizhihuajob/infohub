from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from markdownx.models import MarkdownxField
from markdownx.utils import markdownify
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Category(models.Model):
    """文章分类"""
    name = models.CharField('分类名称', max_length=100)
    slug = models.SlugField('URL别名', unique=True, max_length=100)
    description = models.TextField('描述', blank=True)
    parent = models.ForeignKey('self', verbose_name='父分类', on_delete=models.CASCADE,
                               null=True, blank=True, related_name='children')
    order = models.PositiveIntegerField('排序', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:category', kwargs={'slug': self.slug})

    def get_full_name(self):
        """获取完整分类路径"""
        if self.parent:
            return f"{self.parent.get_full_name()} > {self.name}"
        return self.name


class Tag(models.Model):
    """文章标签"""
    name = models.CharField('标签名称', max_length=50)
    slug = models.SlugField('URL别名', unique=True, max_length=50)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = '标签'
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blog:tag', kwargs={'slug': self.slug})


class Post(models.Model):
    """博客文章"""
    STATUS_CHOICES = [
        ('draft', '草稿'),
        ('published', '已发布'),
    ]

    title = models.CharField('标题', max_length=200)
    slug = models.SlugField('URL别名', unique=True, max_length=200)
    author = models.ForeignKey(User, verbose_name='作者', on_delete=models.CASCADE,
                               related_name='blog_posts')
    category = models.ForeignKey(Category, verbose_name='分类', on_delete=models.CASCADE,
                                 related_name='posts')
    tags = models.ManyToManyField(Tag, verbose_name='标签', blank=True, related_name='posts')
    
    # 封面图片
    cover_image = models.ImageField('封面图片', upload_to='posts/covers/%Y/%m/', blank=True)
    cover_thumbnail = ImageSpecField(source='cover_image',
                                     processors=[ResizeToFill(400, 250)],
                                     format='JPEG',
                                     options={'quality': 85})
    
    # 内容
    summary = models.TextField('摘要', max_length=500, blank=True,
                               help_text='如果不填写，将自动从正文中提取')
    content = MarkdownxField('正文内容')
    
    # 状态
    status = models.CharField('状态', max_length=10, choices=STATUS_CHOICES,
                              default='draft')
    
    # 统计
    views = models.PositiveIntegerField('阅读量', default=0)
    
    # 时间
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    published_at = models.DateTimeField('发布时间', null=True, blank=True)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-published_at', '-created_at']
        indexes = [
            models.Index(fields=['-published_at']),
            models.Index(fields=['status', '-published_at']),
        ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:post_detail', kwargs={'slug': self.slug})

    def get_content_html(self):
        """将Markdown转换为HTML"""
        return markdownify(self.content)

    def get_reading_time(self):
        """估算阅读时长（分钟）"""
        words_per_minute = 300
        word_count = len(self.content)
        minutes = word_count // words_per_minute
        return max(1, minutes)

    def save(self, *args, **kwargs):
        # 自动提取摘要
        if not self.summary and self.content:
            plain_text = self.content[:200]
            self.summary = plain_text + '...' if len(self.content) > 200 else plain_text
        
        # 发布时设置发布时间
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        
        super().save(*args, **kwargs)

    def increase_views(self):
        """增加阅读量"""
        self.views += 1
        self.save(update_fields=['views'])


class Comment(models.Model):
    """评论"""
    STATUS_CHOICES = [
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
    ]

    post = models.ForeignKey(Post, verbose_name='文章', on_delete=models.CASCADE,
                             related_name='comments')
    parent = models.ForeignKey('self', verbose_name='父评论', on_delete=models.CASCADE,
                               null=True, blank=True, related_name='replies')
    
    # 评论者信息
    name = models.CharField('姓名', max_length=50)
    email = models.EmailField('邮箱')
    website = models.URLField('网站', blank=True)
    
    # 内容
    content = models.TextField('评论内容')
    
    # 状态
    status = models.CharField('状态', max_length=10, choices=STATUS_CHOICES,
                              default='pending')
    
    # 是否为垃圾评论
    is_spam = models.BooleanField('垃圾评论', default=False)
    
    # 时间
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = '评论'
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.name} 评论了 {self.post.title}'

    def get_absolute_url(self):
        return f"{self.post.get_absolute_url()}#comment-{self.id}"


class Page(models.Model):
    """静态页面（关于我、友情链接等）"""
    PAGE_TYPES = [
        ('about', '关于我'),
        ('links', '友情链接'),
        ('guestbook', '留言板'),
        ('custom', '自定义'),
    ]

    title = models.CharField('页面标题', max_length=200)
    slug = models.SlugField('URL别名', unique=True, max_length=100)
    page_type = models.CharField('页面类型', max_length=20, choices=PAGE_TYPES,
                                 default='custom')
    content = MarkdownxField('页面内容')
    is_published = models.BooleanField('是否发布', default=True)
    order = models.PositiveIntegerField('排序', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '页面'
        verbose_name_plural = '页面'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:page', kwargs={'slug': self.slug})

    def get_content_html(self):
        return markdownify(self.content)


class Link(models.Model):
    """友情链接"""
    name = models.CharField('网站名称', max_length=100)
    url = models.URLField('网站链接')
    description = models.CharField('描述', max_length=200, blank=True)
    logo = models.ImageField('Logo', upload_to='links/', blank=True)
    order = models.PositiveIntegerField('排序', default=0)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = '友情链接'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.name
