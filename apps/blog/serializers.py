from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Category, Tag, Post, Comment, Subscription


class AuthorSerializer(serializers.ModelSerializer):
    """Сериализатор для автора поста"""
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email']


class CategorySerializer(serializers.ModelSerializer):
    """Сериализатор для категорий"""
    posts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Category
        fields = [
            'id', 'slug', 'name_en', 'name_ru', 'name_he',
            'description_en', 'description_ru', 'description_he',
            'icon', 'color', 'order', 'posts_count'
        ]
    
    def get_posts_count(self, obj):
        return obj.posts.filter(status='published', is_active=True).count()


class TagSerializer(serializers.ModelSerializer):
    """Сериализатор для тегов"""
    posts_count = serializers.SerializerMethodField()
    
    class Meta:
        model = Tag
        fields = [
            'id', 'slug', 'name_en', 'name_ru', 'name_he',
            'description_en', 'description_ru', 'description_he',
            'color', 'posts_count'
        ]
    
    def get_posts_count(self, obj):
        return obj.posts.filter(status='published', is_active=True).count()


class PostListSerializer(serializers.ModelSerializer):
    """Сериализатор для списка постов"""
    author = AuthorSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id', 'slug', 'title_en', 'title_ru', 'title_he',
            'subtitle_en', 'subtitle_ru', 'subtitle_he',
            'excerpt_en', 'excerpt_ru', 'excerpt_he',
            'thumbnail', 'cover_image', 'author', 'categories', 'tags',
            'read_time', 'is_featured', 'published_at', 'views_count'
        ]


class PostDetailSerializer(serializers.ModelSerializer):
    """Сериализатор для детального просмотра поста"""
    author = AuthorSerializer(read_only=True)
    categories = CategorySerializer(many=True, read_only=True)
    tags = TagSerializer(many=True, read_only=True)
    
    class Meta:
        model = Post
        fields = [
            'id', 'slug', 'title_en', 'title_ru', 'title_he',
            'subtitle_en', 'subtitle_ru', 'subtitle_he',
            'excerpt_en', 'excerpt_ru', 'excerpt_he',
            'content_en', 'content_ru', 'content_he',
            'thumbnail', 'cover_image', 'author', 'categories', 'tags',
            'read_time', 'is_featured', 'published_at', 'views_count',
            'allow_comments', 'meta_title', 'meta_description', 'meta_keywords'
        ]


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для комментариев"""
    replies = serializers.SerializerMethodField()
    post = serializers.PrimaryKeyRelatedField(queryset=Post.objects.all(), write_only=True)  # ✅ ДОБАВЛЕНО
    
    class Meta:
        model = Comment
        fields = [
            'id', 'post', 'author_name', 'author_email', 'author_website',  # ✅ Добавлено 'post'
            'content', 'created_at', 'parent', 'replies'
        ]
        extra_kwargs = {
            'post': {'write_only': True},  # Только для записи, не показываем в ответе
        }
    
    def get_replies(self, obj):
        if obj.replies.exists():
            return CommentSerializer(obj.replies.filter(is_active=True, is_approved=True), many=True).data
        return []


class SubscriptionSerializer(serializers.ModelSerializer):
    """Сериализатор для подписок"""
    class Meta:
        model = Subscription
        fields = ['id', 'email', 'name', 'language', 'created_at', 'is_active']
        read_only_fields = ['id', 'created_at']
