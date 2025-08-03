from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import ContactMessage, ContactResponse, Newsletter
from .serializers import ContactMessageSerializer, ContactResponseSerializer, NewsletterSerializer

class ContactMessageViewSet(viewsets.ModelViewSet):
    queryset = ContactMessage.objects.all()
    serializer_class = ContactMessageSerializer
    permission_classes = [AllowAny]  # 🎯 КЛЮЧЕВОЕ ИСПРАВЛЕНИЕ!
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status', 'is_read']
    ordering = ['-created_at']

class ContactResponseViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = ContactResponse.objects.all()
    serializer_class = ContactResponseSerializer
    filter_backends = [OrderingFilter]
    ordering = ['-created_at']

class NewsletterViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Newsletter.objects.filter(is_active=True)
    serializer_class = NewsletterSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['status']
    ordering = ['-created_at']
