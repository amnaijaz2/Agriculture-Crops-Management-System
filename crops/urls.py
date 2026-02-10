"""
URL configuration for Crops module.
"""
from django.urls import path
from . import views

app_name = 'crops'

urlpatterns = [
    path('', views.CropListView.as_view(), name='crop_list'),
    path('create/', views.CropCreateView.as_view(), name='crop_create'),
    path('<int:pk>/', views.CropDetailView.as_view(), name='crop_detail'),
    path('<int:pk>/edit/', views.CropUpdateView.as_view(), name='crop_update'),
    path('<int:pk>/delete/', views.CropDeleteView.as_view(), name='crop_delete'),
]
