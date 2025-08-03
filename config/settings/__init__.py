from decouple import config

# Determine which settings to use
ENVIRONMENT = config('DJANGO_ENVIRONMENT', default='development')

if ENVIRONMENT == 'production':
    from .production import *
elif ENVIRONMENT == 'testing':
    from .base import *
    # Add testing specific settings here
else:
    from .development import *