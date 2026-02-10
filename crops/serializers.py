"""
Serializers for Crops API.
"""
from rest_framework import serializers
from .models import Crop, CropStatus, CropType
from users.serializers import UserSerializer


class CropSerializer(serializers.ModelSerializer):
    """Serializer for Crop model."""
    farmer_detail = UserSerializer(source='farmer', read_only=True)
    crop_type_display = serializers.CharField(source='get_crop_type_display', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Crop
        fields = [
            'id', 'name', 'crop_type', 'crop_type_display', 'quantity', 'unit',
            'price', 'farmer', 'farmer_detail', 'location', 'status', 'status_display',
            'description', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']


class CropCreateUpdateSerializer(serializers.ModelSerializer):
    """Serializer for creating/updating crops."""

    class Meta:
        model = Crop
        fields = [
            'name', 'crop_type', 'quantity', 'unit', 'price',
            'location', 'status', 'description'
        ]
