from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'profiles', views.UserProfileViewSet)

urlpatterns = [
    path('info/', views.profile_info, name='profile_info'),
    path('', include(router.urls)),
]
