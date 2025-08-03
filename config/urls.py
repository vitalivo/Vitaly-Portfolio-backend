from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

# ✅ ДОБАВЛЯЕМ ТОЛЬКО HEALTH CHECK
def health_check(request):
    return JsonResponse({"status": "healthy", "service": "vitaly-portfolio-api"})

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # ✅ ДОБАВЛЯЕМ HEALTH CHECK
    path('api/health/', health_check, name='health_check'),
    
    # Ваши существующие маршруты
    path('api/core/', include('apps.core.urls')),
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/portfolio/', include('apps.portfolio.urls')),
    path('api/blog/', include('apps.blog.urls')),
    path('api/contacts/', include('apps.contacts.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)