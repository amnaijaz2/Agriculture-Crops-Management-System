"""
API URL configuration for Crops module.
"""
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import api_views

router = DefaultRouter()
router.register(r'', api_views.CropViewSet, basename='crop')

urlpatterns = [
    path('', include(router.urls)),
]
