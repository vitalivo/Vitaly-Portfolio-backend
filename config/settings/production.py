# config/settings/production.py
from .base import *
import os
from decouple import config

DEBUG = False
SECRET_KEY = config('SECRET_KEY', default='django-insecure-temporary-key')

# ✅ ALLOWED_HOSTS
ALLOWED_HOSTS = [
    '.vercel.app',
    'localhost',
    '127.0.0.1',
]

# config/settings/production.py
CORS_ALLOWED_ORIGINS = [
    "https://vitaly-portfolio-frontend-lushchb1r-vitalivo-gmailcoms-projects.vercel.app",  # ← НОВЫЙ URL
    "https://vitaly-portfolio1.vercel.app",  # ← СТАРЫЙ URL (на всякий случай)
]

CORS_ALLOW_ALL_ORIGINS = False  # ← Возвращаем безопасность# ← БЕЗОПАСНОСТЬ
CORS_ALLOW_CREDENTIALS = True

# ✅ CSRF
CSRF_TRUSTED_ORIGINS = [
    "https://vitaly-portfolio1.vercel.app",
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# ✅ БАЗА ДАННЫХ (Neon PostgreSQL)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('PGDATABASE'),
        'USER': os.environ.get('PGUSER'),
        'PASSWORD': os.environ.get('PGPASSWORD'),
        'HOST': os.environ.get('PGHOST'),
        'PORT': os.environ.get('PGPORT', 5432),
        'OPTIONS': {
            'sslmode': 'require',
        },
    }
}

# ✅ СТАТИЧЕСКИЕ ФАЙЛЫ - ОТКЛЮЧАЕМ ДЛЯ VERCEL
STATIC_URL = '/static/'
STATIC_ROOT = None
STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# ✅ МЕДИА ФАЙЛЫ - ОТКЛЮЧАЕМ ДЛЯ VERCEL
MEDIA_URL = '/media/'
MEDIA_ROOT = None

# ✅ БЕЗОПАСНОСТЬ ДЛЯ VERCEL
SECURE_SSL_REDIRECT = False  # ← ВАЖНО: False для Vercel
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# ✅ ЛОГИРОВАНИЕ
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}