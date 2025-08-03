from rest_framework import serializers
from .models import Category, Technology, Project, Skill

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class TechnologySerializer(serializers.ModelSerializer):
    class Meta:
        model = Technology
        fields = '__all__'

class ProjectSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True, read_only=True)
    technologies = TechnologySerializer(many=True, read_only=True)
    
    class Meta:
        model = Project
        fields = '__all__'

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = '__all__'
