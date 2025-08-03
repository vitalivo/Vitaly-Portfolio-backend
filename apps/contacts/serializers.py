from rest_framework import serializers
from .models import ContactMessage, ContactResponse, Newsletter

class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']  # Только нужные поля для создания
        
    def create(self, validated_data):
        """Создаем сообщение с дополнительными полями"""
        return ContactMessage.objects.create(
            name=validated_data['name'],
            email=validated_data['email'],
            subject=validated_data['subject'],
            message=validated_data['message'],
            status='new',  # Устанавливаем статус по умолчанию
            is_read=False,  # По умолчанию не прочитано
        )    

class ContactResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactResponse
        fields = '__all__'

class NewsletterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Newsletter
        fields = '__all__'
