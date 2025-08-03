from rest_framework import serializers
from .models import SiteSettings, SEOSettings

class SiteSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteSettings
        fields = '__all__'

class SEOSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SEOSettings
        fields = '__all__'
