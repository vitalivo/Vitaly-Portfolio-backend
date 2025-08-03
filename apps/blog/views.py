from rest_framework import generics, filters, viewsets, status
from rest_framework.decorators import api_view, action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q, F, Prefetch, Sum
from django.utils import timezone
from .models import Category, Tag, Post, Comment, Subscription
from .serializers import (
    CategorySerializer, TagSerializer, PostListSerializer,
    PostDetailSerializer, CommentSerializer, SubscriptionSerializer
)

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для категорий"""
    queryset = Category.objects.filter(is_active=True).order_by('order')
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name_en', 'name_ru', 'name_he']
    ordering = ['order']

class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для тегов"""
    queryset = Tag.objects.filter(is_active=True).order_by('name_en')
    serializer_class = TagSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name_en', 'name_ru', 'name_he']
    ordering = ['name_en']

class PostViewSet(viewsets.ReadOnlyModelViewSet):
    """ViewSet для постов"""
    lookup_field = 'slug'
    queryset = Post.objects.filter(status='published', is_active=True).select_related('author').prefetch_related('categories', 'tags')
    serializer_class = PostListSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['categories__slug', 'tags__slug', 'is_featured', 'author']
    search_fields = ['title_en', 'title_ru', 'title_he', 'excerpt_en', 'excerpt_ru', 'excerpt_he']
    ordering_fields = ['published_at', 'views_count', 'created_at']
    ordering = ['-published_at']

    def get_serializer_class(self):
        """Используем разные сериализаторы для списка и детального просмотра"""
        if self.action == 'retrieve':
            return PostDetailSerializer
        return PostListSerializer

    def retrieve(self, request, *args, **kwargs):
        """Увеличиваем счетчик просмотров при детальном просмотре"""
        instance = self.get_object()
        # Увеличиваем счетчик просмотров
        Post.objects.filter(pk=instance.pk).update(views_count=F('views_count') + 1)
        # Обновляем объект для корректного отображения
        instance.refresh_from_db()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def featured(self, request):
        """Получить рекомендуемые посты"""
        featured_posts = self.queryset.filter(is_featured=True)
        page = self.paginate_queryset(featured_posts)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = self.get_serializer(featured_posts, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def comments(self, request, slug=None):
        """Получить комментарии к посту"""
        post = self.get_object()
        comments = Comment.objects.filter(
            post=post, 
            is_active=True, 
            is_approved=True,
            parent=None
        ).select_related('post').prefetch_related('replies')
        
        page = self.paginate_queryset(comments)
        if page is not None:
            serializer = CommentSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        
        serializer = CommentSerializer(comments, many=True)
        return Response(serializer.data)

class CommentViewSet(viewsets.ModelViewSet):  # ✅ ИЗМЕНЕНО: ModelViewSet вместо ReadOnlyModelViewSet
    """ViewSet для комментариев"""
    queryset = Comment.objects.filter(is_active=True, is_approved=True).select_related('post').prefetch_related('replies')
    serializer_class = CommentSerializer
    permission_classes = [AllowAny]  # ✅ ДОБАВЛЕНО: Разрешить анонимные комментарии
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['post', 'post__slug']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """Показываем только одобренные комментарии в списке"""
        if self.action in ['list', 'retrieve']:
            return Comment.objects.filter(is_active=True, is_approved=True).select_related('post').prefetch_related('replies')
        return Comment.objects.all()
    
    def perform_create(self, serializer):
        """Создание комментария с дополнительными данными"""
        # Комментарии создаются неодобренными для модерации
        serializer.save(
            is_approved=False,  # ✅ Требует модерации
            ip_address=self.request.META.get('REMOTE_ADDR'),
            user_agent=self.request.META.get('HTTP_USER_AGENT', '')[:500]  # Ограничиваем длину
        )
    
    def create(self, request, *args, **kwargs):
        """Переопределяем создание для кастомного ответа"""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response({
            'message': 'Comment submitted successfully! It will appear after moderation.',
            'status': 'pending_approval'
        }, status=status.HTTP_201_CREATED)

class SubscriptionViewSet(viewsets.ModelViewSet):  # ✅ ИЗМЕНЕНО: ModelViewSet вместо ReadOnlyModelViewSet
    """ViewSet для подписок"""
    queryset = Subscription.objects.filter(is_active=True)
    serializer_class = SubscriptionSerializer
    permission_classes = [AllowAny]  # ✅ ДОБАВЛЕНО: Разрешить анонимные подписки
    
    def get_queryset(self):
        """Администраторы видят все подписки, обычные пользователи - только свои"""
        if self.request.user.is_staff:
            return Subscription.objects.all()
        return Subscription.objects.filter(is_active=True)
    
    def perform_create(self, serializer):
        """Создание подписки с дополнительными данными"""
        serializer.save(
            ip_address=self.request.META.get('REMOTE_ADDR'),
            is_active=True,
            # TODO: Добавить генерацию токена подтверждения и отправку email
        )
    
    def create(self, request, *args, **kwargs):
        """Переопределяем создание для обработки дубликатов"""
        email = request.data.get('email')
        
        # Проверяем существующую подписку
        if Subscription.objects.filter(email=email).exists():
            return Response({
                'message': 'This email is already subscribed!',
                'status': 'already_subscribed'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        
        return Response({
            'message': 'Successfully subscribed! Check your email for confirmation.',
            'status': 'subscribed'
        }, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def blog_stats(request):
    """Статистика блога"""
    stats = {
        'total_posts': Post.objects.filter(status='published', is_active=True).count(),
        'total_categories': Category.objects.filter(is_active=True).count(),
        'total_tags': Tag.objects.filter(is_active=True).count(),
        'featured_posts': Post.objects.filter(status='published', is_active=True, is_featured=True).count(),
        'total_views': Post.objects.filter(status='published', is_active=True).aggregate(
            total=Sum('views_count')
        )['total'] or 0,
        'total_comments': Comment.objects.filter(is_active=True, is_approved=True).count(),
        'total_subscriptions': Subscription.objects.filter(is_active=True).count(),
    }
    return Response(stats)