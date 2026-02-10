"""
Admin configuration for Crop model.
"""
from django.contrib import admin
from .models import Crop


@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ('name', 'crop_type', 'quantity', 'price', 'farmer', 'status', 'created_at')
    list_filter = ('crop_type', 'status')
    search_fields = ('name', 'location', 'farmer__username')
    raw_id_fields = ('farmer',)
