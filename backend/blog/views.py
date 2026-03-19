"""
博客应用的视图函数
提供API接口的实现
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated
from django.db import models
from django.utils import timezone

from .models import Category, Tag, Article, Comment
from .serializers import (
    CategorySerializer, TagSerializer,
    ArticleListSerializer, ArticleDetailSerializer,
    ArticleCreateUpdateSerializer, CommentSerializer
)


class CategoryViewSet(viewsets.ModelViewSet):
    """
    分类视图集
    提供分类的CRUD操作
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        获取查询集
        普通用户只能看到有文章的分类
        """
        queryset = Category.objects.all()
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(articles__status='published').distinct()
        return queryset


class TagViewSet(viewsets.ModelViewSet):
    """
    标签视图集
    提供标签的CRUD操作
    """
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]


class ArticleViewSet(viewsets.ModelViewSet):
    """
    文章视图集
    提供文章的CRUD操作和额外功能
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        """
        获取查询集
        根据用户权限和查询参数过滤
        """
        queryset = Article.objects.select_related('category', 'author').prefetch_related('tags')

        # 非管理员只能看到已发布的文章
        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status='published')
        elif not self.request.user.is_staff:
            # 普通用户只能看到已发布的文章和自己写的文章
            queryset = queryset.filter(
                models.Q(status='published') | models.Q(author=self.request.user)
            )

        # 按分类过滤
        category_id = self.request.query_params.get('category')
        if category_id:
            queryset = queryset.filter(category_id=category_id)

        # 按标签过滤
        tag_id = self.request.query_params.get('tag')
        if tag_id:
            queryset = queryset.filter(tags__id=tag_id)

        # 搜索功能
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(title__icontains=search) | models.Q(content__icontains=search)
            )

        return queryset.distinct()

    def get_serializer_class(self):
        """
        根据不同操作返回不同的序列化器
        """
        if self.action == 'list':
            return ArticleListSerializer
        elif self.action in ['create', 'update', 'partial_update']:
            return ArticleCreateUpdateSerializer
        return ArticleDetailSerializer

    def retrieve(self, request, *args, **kwargs):
        """
        获取文章详情，并增加阅读量
        """
        instance = self.get_object()
        instance.increase_view_count()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def perform_create(self, serializer):
        """
        创建文章时自动设置作者
        """
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def publish(self, request, pk=None):
        """
        发布文章
        """
        article = self.get_object()
        if article.author != request.user and not request.user.is_staff:
            return Response(
                {'error': '您没有权限发布此文章'},
                status=status.HTTP_403_FORBIDDEN
            )
        article.status = 'published'
        article.save()
        return Response({'message': '文章已发布', 'status': article.status})

    @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated])
    def unpublish(self, request, pk=None):
        """
        取消发布文章
        """
        article = self.get_object()
        if article.author != request.user and not request.user.is_staff:
            return Response(
                {'error': '您没有权限取消发布此文章'},
                status=status.HTTP_403_FORBIDDEN
            )
        article.status = 'draft'
        article.save()
        return Response({'message': '文章已转为草稿', 'status': article.status})


class CommentViewSet(viewsets.ModelViewSet):
    """
    评论视图集
    提供评论的CRUD操作
    """
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer

    def get_queryset(self):
        """
        获取查询集
        管理员可以看到所有评论，普通用户只能看到可见评论
        """
        queryset = Comment.objects.select_related('article', 'parent')

        # 按文章过滤
        article_id = self.request.query_params.get('article')
        if article_id:
            queryset = queryset.filter(article_id=article_id)

        # 非管理员只能看到可见评论
        if not self.request.user.is_staff:
            queryset = queryset.filter(is_visible=True)

        return queryset

    def perform_create(self, serializer):
        """
        创建评论时自动设置为可见
        """
        serializer.save(is_visible=True)
