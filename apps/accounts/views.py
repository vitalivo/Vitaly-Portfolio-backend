from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import UserProfile
from .serializers import UserProfileSerializer

@api_view(['GET'])
def profile_info(request):
    return Response({'message': 'Accounts API is working'})

class UserProfileViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
