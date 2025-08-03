from django.core.management.base import BaseCommand
from apps.contacts.models import ContactMessage
from apps.contacts.utils import send_contact_notification

class Command(BaseCommand):
    help = 'Тестирует систему уведомлений'

    def handle(self, *args, **options):
        self.stdout.write('🧪 Тестируем систему уведомлений...')
        
        # Создаем тестовое сообщение
        test_message = ContactMessage.objects.create(
            name='Test User',
            email='test@example.com',
            subject='Тестовое сообщение',
            message='Это тестовое сообщение для проверки системы уведомлений.',
            status='new'
        )
        
        self.stdout.write(f'✅ Создано тестовое сообщение: #{test_message.id}')
        
        # Отправляем уведомления
        results = send_contact_notification(test_message)
        
        # Выводим результаты
        if results['email']:
            self.stdout.write(self.style.SUCCESS('✅ Email отправлен успешно'))
        else:
            self.stdout.write(self.style.ERROR('❌ Ошибка отправки Email'))
            
        if results['telegram']:
            self.stdout.write(self.style.SUCCESS('✅ Telegram отправлен успешно'))
        else:
            self.stdout.write(self.style.ERROR('❌ Ошибка отправки Telegram'))
        
        # Удаляем тестовое сообщение
        test_message.delete()
        self.stdout.write('🗑️ Тестовое сообщение удалено')
        
        if results['email'] and results['telegram']:
            self.stdout.write(self.style.SUCCESS('🎉 ВСЕ УВЕДОМЛЕНИЯ РАБОТАЮТ!'))
        else:
            self.stdout.write(self.style.WARNING('⚠️ Некоторые уведомления не работают'))
