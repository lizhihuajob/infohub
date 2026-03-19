from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from .models import Post
from .serializers import PostSerializer


class IsAdminOrReadOnly(permissions.BasePermission):
    """
    自定义权限：只有管理员可以写，其他人只读
    """
    def has_permission(self, request, view):
        # 读取权限对所有人开放
        if request.method in permissions.SAFE_METHODS:
            return True
        # 写入权限需要管理员身份（这里简化为is_staff）
        return request.user and request.user.is_staff


class PostViewSet(viewsets.ModelViewSet):
    """
    博客文章视图集
    提供CRUD操作
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_queryset(self):
        """获取已发布的文章列表"""
        queryset = Post.objects.filter(is_published=True).order_by('-created_time')
        return queryset

    def retrieve(self, request, *args, **kwargs):
        """获取单篇文章详情，同时增加浏览量"""
        instance = self.get_object()
        instance.increase_views()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def admin_list(self, request):
        """管理员获取所有文章（包括未发布的）"""
        if not (request.user and request.user.is_staff):
            return Response({"detail": "没有权限"}, status=403)
        queryset = Post.objects.all().order_by('-created_time')
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)