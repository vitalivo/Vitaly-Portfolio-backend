from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter, OrderingFilter
from .models import Category, Technology, Project, Skill
from .serializers import CategorySerializer, TechnologySerializer, ProjectSerializer, SkillSerializer

class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name_en', 'name_ru', 'name_he']
    ordering_fields = ['position', 'created_at']
    ordering = ['position']

class TechnologyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Technology.objects.filter(is_active=True)
    serializer_class = TechnologySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['name']
    ordering_fields = ['position', 'created_at']
    ordering = ['position']

class ProjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Project.objects.filter(status='published')
    serializer_class = ProjectSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['categories', 'technologies', 'is_featured']
    search_fields = ['title_en', 'title_ru', 'title_he', 'description_en']
    ordering_fields = ['published_at', 'order']
    ordering = ['-published_at', 'order']

    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured_projects = self.queryset.filter(is_featured=True)
        serializer = self.get_serializer(featured_projects, many=True)
        return Response(serializer.data)

class SkillViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Skill.objects.filter(is_active=True)
    serializer_class = SkillSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['category']
    search_fields = ['name_en', 'name_ru', 'name_he']
    ordering_fields = ['position', 'level']
    ordering = ['category', 'position']
