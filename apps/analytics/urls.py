from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'page-views', views.PageViewViewSet)
router.register(r'events', views.EventViewSet)
router.register(r'visitors', views.VisitorViewSet)
router.register(r'sessions', views.VisitorSessionViewSet)
router.register(r'daily-stats', views.DailyStatisticsViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
