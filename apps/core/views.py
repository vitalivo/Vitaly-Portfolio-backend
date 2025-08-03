from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import SiteSettings, SEOSettings
from .serializers import SiteSettingsSerializer, SEOSettingsSerializer

@api_view(['GET'])
def health_check(request):
    return Response({'status': 'ok', 'message': 'API is working'})

class SiteSettingsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SiteSettings.objects.filter(is_active=True)
    serializer_class = SiteSettingsSerializer

class SEOSettingsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = SEOSettings.objects.filter(is_active=True)
    serializer_class = SEOSettingsSerializer
