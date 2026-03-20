from django import template
from django.db.models import Count
from ..models import Post, Category, Tag, Link

register = template.Library()


@register.simple_tag
def get_recent_posts(limit=5):
    """获取最新文章"""
    return Post.objects.filter(status='published').order_by('-published_at')[:limit]


@register.simple_tag
def get_hot_posts(limit=5):
    """获取热门文章"""
    return Post.objects.filter(status='published').order_by('-views')[:limit]


@register.simple_tag
def get_categories():
    """获取所有分类"""
    return Category.objects.filter(parent=None).prefetch_related('children')


@register.simple_tag
def get_tags(limit=20):
    """获取标签云"""
    return Tag.objects.all()[:limit]


@register.simple_tag
def get_links():
    """获取友情链接"""
    return Link.objects.filter(is_active=True).order_by('order', '-created_at')


@register.filter
def timesince_zh(value):
    """中文时间差"""
    from django.utils.timesince import timesince
    from django.utils import timezone
    
    if not value:
        return ""
    
    now = timezone.now()
    diff = now - value
    
    if diff.days == 0:
        if diff.seconds < 60:
            return "刚刚"
        elif diff.seconds < 3600:
            return f"{diff.seconds // 60}分钟前"
        else:
            return f"{diff.seconds // 3600}小时前"
    elif diff.days == 1:
        return "昨天"
    elif diff.days < 7:
        return f"{diff.days}天前"
    elif diff.days < 30:
        return f"{diff.days // 7}周前"
    elif diff.days < 365:
        return f"{diff.days // 30}个月前"
    else:
        return f"{diff.days // 365}年前"


@register.filter
def truncatechars_zh(value, length=100):
    """中文截断"""
    if len(value) <= length:
        return value
    return value[:length] + '...'
