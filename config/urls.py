"""
URL configuration for Agriculture Crops Management System.
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('login/', RedirectView.as_view(url='/auth/login/', permanent=False)),
    path('api/auth/', include('authentication.api_urls')),
    path('users/', include('users.urls')),
    path('api/users/', include('users.api_urls')),
    path('crops/', include('crops.urls')),
    path('api/crops/', include('crops.api_urls')),
    path('orders/', include('orders.urls')),
    path('api/orders/', include('orders.api_urls')),
    path('dashboard/', include('dashboards.urls')),
    path('', RedirectView.as_view(url='/dashboard/', permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
