# api/index.py
import os
import sys
from pathlib import Path

# Добавляем корневую папку проекта в Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BASE_DIR))

# Устанавливаем настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

# Инициализируем Django
import django
django.setup()

from django.core.wsgi import get_wsgi_application
from django.http import HttpResponse

# Создаем WSGI приложение
application = get_wsgi_application()

# Функция-обработчик для Vercel
def handler(request):
    return application(request.environ, lambda status, headers: None)

# Экспортируем для Vercel
app = application