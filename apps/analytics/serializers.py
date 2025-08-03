from rest_framework import serializers
from .models import PageView, Event, Visitor, VisitorSession, DailyStatistics

class PageViewSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageView
        fields = '__all__'

class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = '__all__'

class VisitorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Visitor
        fields = '__all__'

class VisitorSessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = VisitorSession
        fields = '__all__'

class DailyStatisticsSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyStatistics
        fields = '__all__'
