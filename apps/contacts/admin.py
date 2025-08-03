from django.contrib import admin
from .models import ContactMessage, ContactResponse, Newsletter

admin.site.register(ContactMessage)
admin.site.register(ContactResponse)
admin.site.register(Newsletter)