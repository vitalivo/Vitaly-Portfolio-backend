from django.apps import AppConfig

class ContactsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'apps.contacts'
    
    def ready(self):
        """Импортируем signals при запуске приложения"""
        import apps.contacts.signals