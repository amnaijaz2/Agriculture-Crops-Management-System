"""
API views for Crops module.
"""
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Crop
from .serializers import CropSerializer, CropCreateUpdateSerializer
from users.permissions import IsAdminOrFarmer, IsAdmin


class CropViewSet(viewsets.ModelViewSet):
    """ViewSet for Crop CRUD operations."""
    queryset = Crop.objects.select_related('farmer').all()
    serializer_class = CropSerializer
    permission_classes = [IsAuthenticated]
    filterset_fields = ['crop_type', 'status', 'farmer']
    search_fields = ['name', 'location', 'description']

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminOrFarmer()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return CropCreateUpdateSerializer
        return CropSerializer

    def perform_create(self, serializer):
        if self.request.user.role == 'FARMER':
            serializer.save(farmer=self.request.user)
        else:
            farmer_id = self.request.data.get('farmer')
            from users.models import User
            farmer = User.objects.get(id=farmer_id) if farmer_id else self.request.user
            serializer.save(farmer=farmer)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response(
            {'success': True, 'data': CropSerializer(serializer.instance).data, 'message': 'Crop created successfully.'},
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        if request.user.role == 'FARMER' and instance.farmer != request.user:
            return Response(
                {'success': False, 'error': {'message': 'You can only edit your own crops.'}},
                status=status.HTTP_403_FORBIDDEN
            )
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {'success': True, 'data': CropSerializer(instance).data, 'message': 'Crop updated successfully.'}
        )
