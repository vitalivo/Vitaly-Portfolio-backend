# from .base import *
# import dj_database_url

# # Security settings
# DEBUG = False
# SECURE_SSL_REDIRECT = True
# SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
# SESSION_COOKIE_SECURE = True
# CSRF_COOKIE_SECURE = True

# # Database from environment variable
# DATABASES = {
#     'default': dj_database_url.config(
#         default=config('DATABASE_URL')
#     )
# }

# # Static files storage
# STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.StaticFilesStorage'

# # Media files storage (AWS S3)
# DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
# AWS_ACCESS_KEY_ID = config('AWS_ACCESS_KEY_ID', default='')
# AWS_SECRET_ACCESS_KEY = config('AWS_SECRET_ACCESS_KEY', default='')
# AWS_STORAGE_BUCKET_NAME = config('AWS_STORAGE_BUCKET_NAME', default='')
# AWS_S3_REGION_NAME = config('AWS_S3_REGION_NAME', default='us-east-1')
# AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
# AWS_DEFAULT_ACL = 'public-read'

# # Logging
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,
#     'handlers': {
#         'file': {
#             'level': 'INFO',
#             'class': 'logging.FileHandler',
#             'filename': BASE_DIR / 'logs' / 'django.log',
#         },
#     },
#     'loggers': {
#         'django': {
#             'handlers': ['file'],
#             'level': 'INFO',
#             'propagate': True,
#         },
#     },
# }

# # Sentry for error tracking
# import sentry_sdk
# from sentry_sdk.integrations.django import DjangoIntegration

# sentry_sdk.init(
#     dsn=config('SENTRY_DSN', default=''),
#     integrations=[DjangoIntegration()],
#     traces_sample_rate=1.0,
#     send_default_pii=True
# )

from .base import *
import dj_database_url
import os

# ✅ БЕЗОПАСНОСТЬ
DEBUG = False
SECRET_KEY = config('SECRET_KEY')

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
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL'),
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# ✅ СТАТИЧЕСКИЕ ФАЙЛЫ с WhiteNoise
MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')

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