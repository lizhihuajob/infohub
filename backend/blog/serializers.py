"""
博客应用的序列化器
用于将模型数据转换为JSON格式
"""
from rest_framework import serializers
from .models import Category, Tag, Article, Comment


class CategorySerializer(serializers.ModelSerializer):
    """
    分类序列化器
    """
    article_count = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'article_count', 'created_at', 'updated_at']

    def get_article_count(self, obj):
        """获取该分类下的文章数量"""
        return obj.articles.filter(status='published').count()


class TagSerializer(serializers.ModelSerializer):
    """
    标签序列化器
    """
    article_count = serializers.SerializerMethodField()

    class Meta:
        model = Tag
        fields = ['id', 'name', 'article_count', 'created_at']

    def get_article_count(self, obj):
        """获取该标签下的文章数量"""
        return obj.articles.filter(status='published').count()


class ArticleListSerializer(serializers.ModelSerializer):
    """
    文章列表序列化器（用于列表展示，不包含完整内容）
    """
    category_name = serializers.CharField(source='category.name', read_only=True)
    tags_list = TagSerializer(source='tags', many=True, read_only=True)
    author_name = serializers.CharField(source='author.username', read_only=True)

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'summary', 'cover_image', 'status',
            'category_name', 'tags_list', 'author_name',
            'view_count', 'is_top', 'created_at', 'updated_at'
        ]


class ArticleDetailSerializer(serializers.ModelSerializer):
    """
    文章详情序列化器（包含完整内容）
    """
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    author_name = serializers.CharField(source='author.username', read_only=True)
    comment_count = serializers.SerializerMethodField()

    class Meta:
        model = Article
        fields = [
            'id', 'title', 'summary', 'content', 'cover_image', 'status',
            'category', 'tags', 'author_name', 'view_count', 'is_top',
            'comment_count', 'created_at', 'updated_at'
        ]

    def get_comment_count(self, obj):
        """获取文章评论数量"""
        return obj.comments.filter(is_visible=True).count()


class CommentSerializer(serializers.ModelSerializer):
    """
    评论序列化器
    """
    replies = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'article', 'parent', 'nickname', 'email',
            'content', 'is_visible', 'replies', 'created_at'
        ]
        read_only_fields = ['is_visible']

    def get_replies(self, obj):
        """获取子评论"""
        if obj.replies.exists():
            return CommentSerializer(
                obj.replies.filter(is_visible=True),
                many=True
            ).data
        return []


class ArticleCreateUpdateSerializer(serializers.ModelSerializer):
    """
    文章创建和更新序列化器
    """
    class Meta:
        model = Article
        fields = [
            'title', 'summary', 'content', 'cover_image', 'status',
            'category', 'tags', 'is_top'
        ]

    def validate_title(self, value):
        """验证标题"""
        if len(value) < 2:
            raise serializers.ValidationError('标题至少需要2个字符')
        return value

    def validate_content(self, value):
        """验证内容"""
        if len(value) < 10:
            raise serializers.ValidationError('内容至少需要10个字符')
        return value
