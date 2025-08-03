from .base import *
import dj_database_url
import os

# ✅ БЕЗОПАСНОСТЬ
DEBUG = False
SECRET_KEY = config('SECRET_KEY')

# ✅ ДОМЕНЫ
ALLOWED_HOSTS = [
    'alluring-flow-production.up.railway.app',  # ваш Railway URL
    '.railway.app',
    'vitalyportfolio.vercel.app',
    '.vercel.app',
    'localhost',
    '127.0.0.1',
]

# ✅ ПОЛНЫЙ MIDDLEWARE С WHITENOISE
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # ✅ Добавляем WhiteNoise
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ✅ CORS ДЛЯ ПРОДАКШЕНА
CORS_ALLOWED_ORIGINS = [
    "https://vitalyportfolio.vercel.app",
    "http://localhost:3000",
]
CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "https://vitalyportfolio.vercel.app",
    "https://alluring-flow-production.up.railway.app",
]

# ✅ БАЗА ДАННЫХ
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# ✅ СТАТИЧЕСКИЕ ФАЙЛЫ
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ✅ EMAIL
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = config('GMAIL_USER')
EMAIL_HOST_PASSWORD = config('GMAIL_APP_PASSWORD')

# ✅ ЛОГИРОВАНИЕ
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
        'level': 'INFO',
    },
}