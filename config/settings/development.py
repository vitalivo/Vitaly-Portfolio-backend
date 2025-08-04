from .base import *
import dj_database_url  # ✅ ДОБАВЛЯЕМ для Docker

# Debug settings
DEBUG = True

ALLOWED_HOSTS = [
    'vitaly-portfolio-backend-production.up.railway.app',
    '.railway.app',
    '.vercel.app',
    'localhost',
    '127.0.0.1',
    '0.0.0.0'
]

# ✅ Database for development (поддержка Docker)
if config('DATABASE_URL', default=''):
    # Docker PostgreSQL
    DATABASES = {
        'default': dj_database_url.config(
            default=config('DATABASE_URL'),
            conn_max_age=600,
        )
    }
else:
    # Локальная PostgreSQL (ваши настройки)
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': config('DB_NAME', default='vitaly_portfolio'),
            'USER': config('DB_USER', default='admin'),
            'PASSWORD': config('DB_PASSWORD', default='admin123'),
            'HOST': config('DB_HOST', default='localhost'),
            'PORT': config('DB_PORT', default='5432'),
        }
    }




# Debug toolbar settings
INTERNAL_IPS = [
    '127.0.0.1',
    'localhost',
]

# ✅ CORS для Docker и локальной разработки
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://frontend:3000",  # для Docker
]

CORS_ALLOW_ALL_ORIGINS = True  # только для разработки
CORS_ALLOW_CREDENTIALS = True

# ✅ CSRF для Docker
CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://frontend:3000",
]

# Email backend for development
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

# ✅ Если есть Gmail настройки (для Docker), используем их
if config('GMAIL_USER', default='') and config('GMAIL_APP_PASSWORD', default=''):
    EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
    EMAIL_HOST = 'smtp.gmail.com'
    EMAIL_PORT = 587
    EMAIL_USE_TLS = True
    EMAIL_HOST_USER = config('GMAIL_USER')
    EMAIL_HOST_PASSWORD = config('GMAIL_APP_PASSWORD')
    DEFAULT_FROM_EMAIL = f'Vitaly Portfolio <{config("GMAIL_USER")}>'

# ✅ СТАТИЧЕСКИЕ ФАЙЛЫ
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# 🔧 ЛОГИРОВАНИЕ
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {process:d} {thread:d} {message}',
            'style': '{',
        },
        'simple': {
            'format': '{levelname} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'file': {
            'level': 'INFO',
            'class': 'logging.FileHandler',
            'filename': BASE_DIR / 'logs' / 'django.log',
            'formatter': 'verbose',
        },
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
    },
    'root': {
        'handlers': ['console', 'file'],
        'level': 'INFO',
    },
    'loggers': {
        'apps.contacts': {
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}

LOGS_DIR = BASE_DIR / 'logs'
LOGS_DIR.mkdir(exist_ok=True)
