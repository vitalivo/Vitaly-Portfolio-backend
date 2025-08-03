from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'site-settings', views.SiteSettingsViewSet)
router.register(r'seo-settings', views.SEOSettingsViewSet)

urlpatterns = [
    path('health/', views.health_check, name='health_check'),
    path('', include(router.urls)),
]
