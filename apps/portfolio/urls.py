from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'categories', views.CategoryViewSet)
router.register(r'technologies', views.TechnologyViewSet)
router.register(r'projects', views.ProjectViewSet)
router.register(r'skills', views.SkillViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
