"""
API views for Orders module.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Order, OrderStatusHistory
from .serializers import (
    OrderSerializer, OrderCreateSerializer, OrderUpdateStatusSerializer,
    OrderStatusHistorySerializer
)
from users.permissions import IsAdminOrBroker
from users.models import Role


class OrderViewSet(viewsets.ModelViewSet):
    """ViewSet for Order operations."""
    queryset = Order.objects.select_related('client', 'crop', 'crop__farmer').all()
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['status', 'client', 'crop']
    http_method_names = ['get', 'post', 'patch', 'head', 'options']

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.role == Role.CLIENT:
            return qs.filter(client=self.request.user)
        if self.request.user.role == Role.FARMER:
            return qs.filter(crop__farmer=self.request.user)
        return qs

    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        if self.action in ['partial_update', 'update_status']:
            return OrderUpdateStatusSerializer
        return OrderSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save(client=request.user)
        return Response(
            {'success': True, 'data': OrderSerializer(order).data, 'message': 'Order placed successfully.'},
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['patch'], permission_classes=[IsAuthenticated])
    def update_status(self, request, pk=None):
        """Update order status (Broker/Admin/Farmer)."""
        order = self.get_object()
        user = request.user
        if user.role not in [Role.ADMIN, Role.BROKER] and order.crop.farmer != user:
            return Response(
                {'success': False, 'error': {'message': 'You do not have permission to update this order.'}},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = OrderUpdateStatusSerializer(order, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        old_status = order.status
        serializer.save()
        OrderStatusHistory.objects.create(
            order=order, from_status=old_status, to_status=order.status, changed_by=user
        )
        return Response(
            {'success': True, 'data': OrderSerializer(order).data, 'message': 'Order status updated.'}
        )

    @action(detail=True, methods=['get'])
    def history(self, request, pk=None):
        """Get order status history."""
        order = self.get_object()
        history = OrderStatusHistory.objects.filter(order=order).select_related('changed_by')
        serializer = OrderStatusHistorySerializer(history, many=True)
        return Response({'success': True, 'data': serializer.data})
