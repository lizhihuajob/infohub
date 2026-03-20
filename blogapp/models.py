from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from markdownx.models import MarkdownxField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
import markdown
from django.utils.html import strip_tags


class Category(models.Model):
    name = models.CharField('分类名称', max_length=100)
    slug = models.SlugField('URL别名', unique=True)
    description = models.TextField('描述', blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children', verbose_name='父分类')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '分类'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blogapp:category_detail', kwargs={'slug': self.slug})


class Tag(models.Model):
    name = models.CharField('标签名称', max_length=100)
    slug = models.SlugField('URL别名', unique=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '标签'
        verbose_name_plural = verbose_name
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('blogapp:tag_detail', kwargs={'slug': self.slug})


class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', '草稿'),
        ('published', '已发布'),
    )

    title = models.CharField('标题', max_length=200)
    slug = models.SlugField('URL别名', unique_for_date='publish_date')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts', verbose_name='作者')
    content = MarkdownxField('内容')
    excerpt = models.TextField('摘要', blank=True, max_length=500)
    cover_image = models.ImageField('封面图片', upload_to='post_covers/%Y/%m/', blank=True, null=True)
    cover_thumbnail = ImageSpecField(
        source='cover_image',
        processors=[ResizeToFill(400, 300)],
        format='JPEG',
        options={'quality': 85}
    )
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, related_name='posts', verbose_name='分类')
    tags = models.ManyToManyField(Tag, related_name='posts', verbose_name='标签', blank=True)
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='draft')
    views = models.PositiveIntegerField('阅读量', default=0)
    publish_date = models.DateTimeField('发布时间', default=timezone.now)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '文章'
        verbose_name_plural = verbose_name
        ordering = ['-publish_date']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blogapp:post_detail', kwargs={
            'year': self.publish_date.year,
            'month': self.publish_date.month,
            'day': self.publish_date.day,
            'slug': self.slug
        })

    def save(self, *args, **kwargs):
        if not self.excerpt:
            md = markdown.Markdown(extensions=['extra', 'codehilite', 'toc'])
            html_content = md.convert(self.content)
            self.excerpt = strip_tags(html_content)[:200] + '...'
        super().save(*args, **kwargs)

    def increase_views(self):
        self.views += 1
        self.save(update_fields=['views'])

    def get_reading_time(self):
        word_count = len(strip_tags(self.content))
        return max(1, round(word_count / 300))


class Comment(models.Model):
    STATUS_CHOICES = (
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
    )

    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='文章')
    author_name = models.CharField('昵称', max_length=100)
    author_email = models.EmailField('邮箱')
    author_url = models.URLField('网址', blank=True)
    content = models.TextField('内容')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='replies', verbose_name='父评论')
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '评论'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author_name} - {self.content[:20]}'


class Link(models.Model):
    name = models.CharField('网站名称', max_length=100)
    url = models.URLField('网址')
    description = models.TextField('描述', blank=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name
        ordering = ['created_at']

    def __str__(self):
        return self.name


class Page(models.Model):
    TYPE_CHOICES = (
        ('about', '关于我'),
        ('links', '友情链接'),
        ('guestbook', '留言板'),
    )

    title = models.CharField('标题', max_length=200)
    slug = models.SlugField('URL别名', unique=True)
    content = MarkdownxField('内容')
    page_type = models.CharField('页面类型', max_length=20, choices=TYPE_CHOICES, unique=True)
    created_at = models.DateTimeField('创建时间', auto_now_add=True)
    updated_at = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '静态页面'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blogapp:page_detail', kwargs={'slug': self.slug})


class Guestbook(models.Model):
    STATUS_CHOICES = (
        ('pending', '待审核'),
        ('approved', '已通过'),
        ('rejected', '已拒绝'),
    )

    author_name = models.CharField('昵称', max_length=100)
    author_email = models.EmailField('邮箱')
    author_url = models.URLField('网址', blank=True)
    content = models.TextField('内容')
    status = models.CharField('状态', max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = '留言'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.author_name} - {self.content[:20]}'
