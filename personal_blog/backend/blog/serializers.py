"""
博客应用序列化器
用于将模型实例转换为 JSON 数据，供 API 使用
"""

from rest_framework import serializers
from .models import Category, Tag, Post


class CategorySerializer(serializers.ModelSerializer):
    """
    分类模型序列化器
    
    用于序列化和反序列化 Category 模型数据
    """
    class Meta:
        # 指定序列化的模型
        model = Category
        # 指定序列化的字段
        fields = ['id', 'name', 'slug', 'description', 'created_at']
        # 只读字段
        read_only_fields = ['created_at']


class TagSerializer(serializers.ModelSerializer):
    """
    标签模型序列化器
    
    用于序列化和反序列化 Tag 模型数据
    """
    class Meta:
        model = Tag
        fields = ['id', 'name', 'slug', 'created_at']
        read_only_fields = ['created_at']


class PostListSerializer(serializers.ModelSerializer):
    """
    文章列表序列化器
    
    用于文章列表展示，包含基本信息，不包含完整内容
    减少数据传输量，提高列表加载速度
    
    额外字段:
        author_name: 作者用户名
        category_name: 分类名称
        tag_list: 标签列表
    """
    # 添加额外字段，便于前端展示
    author_name = serializers.CharField(source='author.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    tag_list = TagSerializer(source='tags', many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'author_name', 'category_name',
            'tag_list', 'summary', 'cover_image', 'views', 'is_top',
            'status', 'published_at', 'created_at'
        ]
        read_only_fields = ['views', 'created_at', 'published_at']


class PostDetailSerializer(serializers.ModelSerializer):
    """
    文章详情序列化器
    
    用于文章详情展示，包含完整内容
    用于单个文章的完整信息展示
    
    额外字段:
        author_name: 作者用户名
        category: 完整分类信息
        tags: 完整标签信息列表
    """
    author_name = serializers.CharField(source='author.username', read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'author_name', 'category', 'tags',
            'summary', 'content', 'cover_image', 'views', 'is_top',
            'status', 'published_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['views', 'created_at', 'updated_at', 'published_at']


class PostCreateUpdateSerializer(serializers.ModelSerializer):
    """
    文章创建和更新序列化器
    
    用于管理员创建和编辑文章
    支持通过 ID 指定分类和标签
    
    额外字段:
        category_id: 分类 ID
        tag_ids: 标签 ID 列表
    """
    category_id = serializers.PrimaryKeyRelatedField(
        queryset=Category.objects.all(),
        source='category',
        required=False,
        allow_null=True,
        label='分类ID'
    )
    tag_ids = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        source='tags',
        many=True,
        required=False,
        label='标签ID列表'
    )
    
    class Meta:
        model = Post
        fields = [
            'id', 'title', 'slug', 'category_id', 'tag_ids',
            'summary', 'content', 'cover_image', 'status', 'is_top'
        ]
    
    def create(self, validated_data):
        """
        创建文章
        
        自动设置作者为当前请求用户
        
        参数:
            validated_data: 验证后的数据
            
        返回:
            Post: 新创建的文章实例
        """
        # 从请求上下文中获取当前用户
        request = self.context.get('request')
        if request and hasattr(request, 'user'):
            validated_data['author'] = request.user
        return super().create(validated_data)
