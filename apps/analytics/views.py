from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter
from .models import PageView, Event, Visitor, VisitorSession, DailyStatistics
from .serializers import PageViewSerializer, EventSerializer, VisitorSerializer, VisitorSessionSerializer, DailyStatisticsSerializer

class PageViewViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = PageView.objects.all()
    serializer_class = PageViewSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['path', 'is_bot', 'is_mobile', 'country']
    ordering = ['-created_at']

class EventViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['name', 'category']
    ordering = ['-created_at']

class VisitorViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Visitor.objects.all()
    serializer_class = VisitorSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['country', 'is_bot']
    ordering = ['-last_visit_at']

class VisitorSessionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = VisitorSession.objects.all()
    serializer_class = VisitorSessionSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['visitor', 'is_bounce']
    ordering = ['-start_time']

class DailyStatisticsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = DailyStatistics.objects.all()
    serializer_class = DailyStatisticsSerializer
    filter_backends = [OrderingFilter]
    ordering = ['-date']
