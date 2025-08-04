from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

# ✅ HEALTH CHECK
def health_check(request):
    return JsonResponse({"status": "healthy", "service": "vitaly-portfolio-api"})

# ✅ API ROOT - ГЛАВНАЯ СТРАНИЦА
def api_root(request):
    return JsonResponse({
        "message": "Vitaly Portfolio API",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "health": "/api/health/",
            "core": "/api/core/",
            "accounts": "/api/accounts/",
            "portfolio": "/api/portfolio/",
            "blog": "/api/blog/",
            "contacts": "/api/contacts/",
            "analytics": "/api/analytics/",
            "admin": "/admin/"
        },
        "documentation": "https://github.com/your-username/vitaly-portfolio-backend"
    })

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # ✅ ГЛАВНАЯ СТРАНИЦА API
    path('', api_root, name='api_root'),
    
    # ✅ HEALTH CHECK
    path('api/health/', health_check, name='health_check'),
    
    # ✅ ВАШИ API МАРШРУТЫ
    path('api/core/', include('apps.core.urls')),
    path('api/accounts/', include('apps.accounts.urls')),
    path('api/portfolio/', include('apps.portfolio.urls')),
    path('api/blog/', include('apps.blog.urls')),
    path('api/contacts/', include('apps.contacts.urls')),
    path('api/analytics/', include('apps.analytics.urls')),
]

# ✅ СТАТИЧЕСКИЕ ФАЙЛЫ (только для разработки)
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)