from rest_framework import serializers
from .models import Post


class PostSerializer(serializers.ModelSerializer):
    """博客文章序列化器"""
    created_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    updated_time = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'title', 'content', 'author', 'created_time', 'updated_time', 'is_published', 'views']
        read_only_fields = ['views']