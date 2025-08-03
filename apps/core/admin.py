from django.contrib import admin
from .models import SiteSettings, SEOSettings

admin.site.register(SiteSettings)
admin.site.register(SEOSettings)