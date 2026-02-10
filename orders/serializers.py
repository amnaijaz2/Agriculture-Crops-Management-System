"""
Serializers for Orders API.
"""
from rest_framework import serializers
from .models import Order, OrderStatusHistory
from crops.serializers import CropSerializer
from users.serializers import UserSerializer


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order model."""
    crop_detail = CropSerializer(source='crop', read_only=True)
    client_detail = UserSerializer(source='client', read_only=True)
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'client', 'client_detail', 'crop', 'crop_detail',
            'quantity', 'total_amount', 'status', 'status_display',
            'shipping_address', 'notes', 'created_at', 'updated_at'
        ]
        read_only_fields = ['total_amount', 'created_at', 'updated_at']


class OrderCreateSerializer(serializers.ModelSerializer):
    """Serializer for creating orders."""

    class Meta:
        model = Order
        fields = ['crop', 'quantity', 'shipping_address', 'notes']

    def validate(self, attrs):
        crop = attrs['crop']
        quantity = attrs['quantity']
        if quantity <= 0:
            raise serializers.ValidationError({'quantity': 'Quantity must be positive.'})
        if crop.quantity < quantity:
            raise serializers.ValidationError({'quantity': f'Only {crop.quantity} {crop.unit} available.'})
        if crop.status != 'AVAILABLE':
            raise serializers.ValidationError({'crop': 'This crop is not available for purchase.'})
        return attrs


class OrderUpdateStatusSerializer(serializers.ModelSerializer):
    """Serializer for updating order status."""

    class Meta:
        model = Order
        fields = ['status']


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    """Serializer for order status history."""
    changed_by_name = serializers.CharField(source='changed_by.username', read_only=True)

    class Meta:
        model = OrderStatusHistory
        fields = ['id', 'from_status', 'to_status', 'changed_by_name', 'note', 'created_at']
