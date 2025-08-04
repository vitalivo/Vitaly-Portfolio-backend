
from .base import *
import dj_database_url
import os

# ✅ БЕЗОПАСНОСТЬ
DEBUG = False
SECRET_KEY = config('SECRET_KEY', default='django-insecure-temporary-key-for-railway-deployment-2024')

# ✅ ДОМЕНЫ (обновим после развертывания)
ALLOWED_HOSTS = [
    'vitaly-portfolio-backend.railway.app',
    'vitalyportfolio-api.railway.app',
    'vitalyportfolio.vercel.app',
    '.vercel.app',
    '.railway.app',
    'localhost',
    '127.0.0.1',
]

# ✅ CORS ДЛЯ ПРОДАКШЕНА
CORS_ALLOWED_ORIGINS = [
    "https://vitalyportfolio.vercel.app",
    "https://vitaly-portfolio-frontend.vercel.app",
    "http://localhost:3000",  # для разработки
]

CORS_ALLOW_ALL_ORIGINS = False
CORS_ALLOW_CREDENTIALS = True

CSRF_TRUSTED_ORIGINS = [
    "https://vitalyportfolio.vercel.app",
    "https://vitaly-portfolio-frontend.vercel.app",
    "https://vitaly-portfolio-backend.railway.app",
]

# ✅ БАЗА ДАННЫХ (Railway PostgreSQL)
import dj_database_url

DATABASES = {
    'default': dj_database_url.config(
        default='postgresql://postgres:ByFMTjoIGObRXjHpLDAMFEUhmTAIgcm@postgres.railway.internal:5432/railway',
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# ✅ СТАТИЧЕСКИЕ ФАЙЛЫ с WhiteNoise
# MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# ✅ МЕДИА ФАЙЛЫ
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# ✅ БЕЗОПАСНОСТЬ
SECURE_SSL_REDIRECT = True
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