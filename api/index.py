# api/index.py
import os
import sys
from pathlib import Path

# Добавляем корневую директорию в Python path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

# Устанавливаем настройки Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.production')

import django
from django.core.wsgi import get_wsgi_application

# Инициализируем Django
django.setup()

# Получаем WSGI приложение
app = get_wsgi_application()