from .models import Category, Tag, Post


def blog_context(request):
    """全局上下文处理器"""
    context = {}
    
    # 热门文章（按阅读量排序）
    context['hot_posts'] = Post.objects.filter(
        status='published'
    ).order_by('-views')[:5]
    
    # 分类目录树
    context['categories'] = Category.objects.filter(
        parent=None
    ).prefetch_related('children')
    
    # 标签云
    context['tags'] = Tag.objects.all()[:20]
    
    # 最新文章（用于侧边栏）
    context['recent_posts'] = Post.objects.filter(
        status='published'
    ).order_by('-published_at')[:5]
    
    return context
