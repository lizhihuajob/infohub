from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify
from taggit.managers import TaggableManager
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
import markdown
import readtime


class Category(models.Model):
    name = models.CharField('分类名称', max_length=100)
    slug = models.SlugField('URL别名', unique=True, blank=True)
    description = models.TextField('分类描述', blank=True)
    parent = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='children',
        verbose_name='父分类'
    )
    order = models.IntegerField('排序', default=0)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = '分类'
        ordering = ['order', 'name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:category', args=[self.slug])

    def get_post_count(self):
        return self.posts.filter(status='published').count()


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('published', '已发布'),
    )

    title = models.CharField('标题', max_length=200)
    slug = models.SlugField('URL别名', unique=True, blank=True)
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
        related_name='posts',
        verbose_name='作者'
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='posts',
        verbose_name='分类'
    )
    tags = TaggableManager(blank=True, verbose_name='标签')
    cover_image = models.ImageField('封面图', upload_to='covers/%Y/%m/', blank=True, null=True)
    cover_thumbnail = ImageSpecField(
        source='cover_image',
        processors=[ResizeToFill(300, 200)],
        format='JPEG',
        options={'quality': 85}
    )
    summary = models.TextField('摘要', max_length=500, blank=True)
    content = models.TextField('内容')
    status = models.CharField('状态', max_length=10, choices=STATUS_CHOICES, default='draft')
    views = models.PositiveIntegerField('阅读量', default=0)
    is_featured = models.BooleanField('推荐', default=False)
    allow_comments = models.BooleanField('允许评论', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)
    published_at = models.DateTimeField('发布时间', null=True, blank=True)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = '文章'
        ordering = ['-published_at', '-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        if self.status == 'published' and not self.published_at:
            self.published_at = timezone.now()
        if not self.summary and self.content:
            self.summary = self.content[:200] + '...' if len(self.content) > 200 else self.content
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('blog:post_detail', args=[self.slug])

    def get_content_html(self):
        return markdown.markdown(
            self.content,
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
                'markdown.extensions.tables',
            ]
        )

    def get_reading_time(self):
        result = readtime.of_markdown(self.content)
        return result.minutes if result.minutes > 0 else 1

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def get_next_post(self):
        return Post.objects.filter(
            status='published',
            published_at__gt=self.published_at
        ).order_by('published_at').first()

    def get_previous_post(self):
        return Post.objects.filter(
            status='published',
            published_at__lt=self.published_at
        ).order_by('-published_at').first()


class Link(models.Model):
    name = models.CharField('网站名称', max_length=100)
    url = models.URLField('网站地址')
    description = models.CharField('网站描述', max_length=200, blank=True)
    logo = models.ImageField('Logo', upload_to='links/', blank=True, null=True)
    order = models.IntegerField('排序', default=0)
    is_active = models.BooleanField('是否启用', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = '友情链接'
        ordering = ['order', '-created_at']

    def __str__(self):
        return self.name


class StaticPage(models.Model):
    PAGE_TYPE_CHOICES = (
        ('about', '关于我'),
        ('guestbook', '留言板'),
        ('custom', '自定义页面'),
    )

    title = models.CharField('标题', max_length=200)
    slug = models.SlugField('URL别名', unique=True)
    page_type = models.CharField('页面类型', max_length=20, choices=PAGE_TYPE_CHOICES, default='custom')
    content = models.TextField('内容')
    is_published = models.BooleanField('是否发布', default=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '静态页面'
        verbose_name_plural = '静态页面'
        ordering = ['title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog:static_page', args=[self.slug])

    def get_content_html(self):
        return markdown.markdown(
            self.content,
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
            ]
        )
