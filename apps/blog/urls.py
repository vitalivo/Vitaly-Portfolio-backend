from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'blog'

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'tags', views.TagViewSet)
router.register(r'posts', views.PostViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'subscriptions', views.SubscriptionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('stats/', views.blog_stats, name='blog-stats'),
]
