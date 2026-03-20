"""
博客应用视图
定义 API 接口，处理博客相关的 HTTP 请求
"""

from rest_framework import generics, status, filters
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import Category, Tag, Post
from .serializers import (
    CategorySerializer, 
    TagSerializer, 
    PostListSerializer, 
    PostDetailSerializer,
    PostCreateUpdateSerializer
)


# =============================================================================
# 分类 API 视图
# =============================================================================

class CategoryListView(generics.ListAPIView):
    """
    分类列表 API
    
    获取所有文章分类列表
    任何人都可以访问
    
    接口: GET /api/blog/categories/
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class CategoryDetailView(generics.RetrieveAPIView):
    """
    分类详情 API
    
    获取单个分类的详细信息
    
    接口: GET /api/blog/categories/<slug>/
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]
    # 使用 slug 作为查找字段
    lookup_field = 'slug'


# =============================================================================
# 标签 API 视图
# =============================================================================

class TagListView(generics.ListAPIView):
    """
    标签列表 API
    
    获取所有文章标签列表
    任何人都可以访问
    
    接口: GET /api/blog/tags/
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]


class TagDetailView(generics.RetrieveAPIView):
    """
    标签详情 API
    
    获取单个标签的详细信息
    
    接口: GET /api/blog/tags/<slug>/
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'


# =============================================================================
# 文章 API 视图
# =============================================================================

class PostListView(generics.ListAPIView):
    """
    文章列表 API
    
    获取已发布的文章列表，支持分页、搜索、筛选
    任何人都可以访问
    
    接口: GET /api/blog/posts/
    
    查询参数:
        - search: 搜索关键词（搜索标题和内容）
        - category: 按分类 slug 筛选
        - tag: 按标签 slug 筛选
        - page: 页码
    """
    serializer_class = PostListSerializer
    permission_classes = [AllowAny]
    
    # 配置过滤和搜索
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['title', 'summary', 'content']
    
    def get_queryset(self):
        """
        获取文章查询集
        
        只返回已发布的文章，支持按分类和标签筛选
        
        返回:
            QuerySet: 筛选后的文章查询集
        """
        # 基础查询：只获取已发布文章
        queryset = Post.objects.filter(status=Post.Status.PUBLISHED)
        
        # 获取查询参数
        category_slug = self.request.query_params.get('category')
        tag_slug = self.request.query_params.get('tag')
        
        # 按分类筛选
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        
        # 按标签筛选
        if tag_slug:
            queryset = queryset.filter(tags__slug=tag_slug)
        
        # 预加载关联数据，优化查询性能
        return queryset.select_related('author', 'category').prefetch_related('tags')


class PostDetailView(generics.RetrieveAPIView):
    """
    文章详情 API
    
    获取单篇文章的完整信息
    访问时会自动增加文章浏览次数
    
    接口: GET /api/blog/posts/<slug>/
    """
    queryset = Post.objects.filter(status=Post.Status.PUBLISHED)
    serializer_class = PostDetailSerializer
    permission_classes = [AllowAny]
    lookup_field = 'slug'
    
    def get_object(self):
        """
        获取文章对象
        
        获取文章的同时增加浏览次数
        
        返回:
            Post: 文章实例
        """
        obj = super().get_object()
        # 增加浏览次数
        obj.increase_views()
        return obj


class PostCreateView(generics.CreateAPIView):
    """
    创建文章 API
    
    管理员创建新文章
    需要登录认证
    
    接口: POST /api/blog/posts/create/
    
    请求体:
        - title: 文章标题（必填）
        - slug: URL 标识（必填）
        - content: 文章内容（必填）
        - summary: 文章摘要（可选）
        - category_id: 分类 ID（可选）
        - tag_ids: 标签 ID 列表（可选）
        - status: 状态（draft/published，默认 draft）
        - is_top: 是否置顶（默认 false）
    """
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        """
        执行创建操作
        
        自动设置当前用户为作者
        """
        serializer.save(author=self.request.user)


class PostUpdateView(generics.UpdateAPIView):
    """
    更新文章 API
    
    管理员更新已有文章
    需要登录认证
    
    接口: PUT /api/blog/posts/<id>/update/
    """
    queryset = Post.objects.all()
    serializer_class = PostCreateUpdateSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'


class PostDeleteView(generics.DestroyAPIView):
    """
    删除文章 API
    
    管理员删除文章
    需要登录认证
    
    接口: DELETE /api/blog/posts/<id>/delete/
    """
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticated]
    lookup_field = 'pk'


# =============================================================================
# 管理员文章列表 API
# =============================================================================

class AdminPostListView(generics.ListAPIView):
    """
    管理员文章列表 API
    
    获取所有文章（包括草稿），用于管理后台
    需要登录认证
    
    接口: GET /api/blog/admin/posts/
    
    查询参数:
        - status: 按状态筛选（draft/published）
        - search: 搜索关键词
    """
    serializer_class = PostListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [filters.SearchFilter]
    search_fields = ['title', 'content']
    
    def get_queryset(self):
        """
        获取文章查询集
        
        管理员可以查看所有文章，支持按状态筛选
        
        返回:
            QuerySet: 筛选后的文章查询集
        """
        queryset = Post.objects.all()
        
        # 按状态筛选
        status_param = self.request.query_params.get('status')
        if status_param:
            queryset = queryset.filter(status=status_param)
        
        return queryset.select_related('author', 'category').prefetch_related('tags')


# =============================================================================
# 功能 API
# =============================================================================

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def publish_post(request, pk):
    """
    发布文章 API
    
    将草稿状态的文章发布
    需要登录认证
    
    接口: POST /api/blog/posts/<id>/publish/
    
    参数:
        pk: 文章 ID
        
    返回:
        发布成功返回文章详情，失败返回错误信息
    """
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    serializer = PostDetailSerializer(post)
    return Response(serializer.data)


@api_view(['POST'])
def increment_views(request, slug):
    """
    增加文章浏览次数 API
    
    单独调用以增加文章浏览次数
    任何人都可以访问
    
    接口: POST /api/blog/posts/<slug>/view/
    
    参数:
        slug: 文章 URL 标识
        
    返回:
        更新后的浏览次数
    """
    post = get_object_or_404(Post, slug=slug, status=Post.Status.PUBLISHED)
    post.increase_views()
    return Response({'views': post.views})


# =============================================================================
# 统计 API
# =============================================================================

@api_view(['GET'])
def blog_stats(request):
    """
    博客统计信息 API
    
    获取博客的基本统计数据
    任何人都可以访问
    
    接口: GET /api/blog/stats/
    
    返回:
        - total_posts: 已发布文章总数
        - total_categories: 分类总数
        - total_tags: 标签总数
        - total_views: 总浏览次数
    """
    stats = {
        'total_posts': Post.objects.filter(status=Post.Status.PUBLISHED).count(),
        'total_categories': Category.objects.count(),
        'total_tags': Tag.objects.count(),
        'total_views': sum(
            Post.objects.filter(status=Post.Status.PUBLISHED).values_list('views', flat=True)
        ) or 0
    }
    return Response(stats)
