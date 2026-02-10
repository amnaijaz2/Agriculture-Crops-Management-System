"""
API views for Authentication - JWT based.
"""
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import RegisterSerializer, UserProfileSerializer


def get_tokens_for_user(user):
    """Generate JWT tokens for user."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
        'user': UserProfileSerializer(user).data,
    }


@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    """Register a new user and return JWT tokens."""
    serializer = RegisterSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        tokens = get_tokens_for_user(user)
        return Response(
            {
                'success': True,
                'message': 'Registration successful.',
                'data': tokens,
            },
            status=status.HTTP_201_CREATED
        )
    return Response(
        {'success': False, 'error': {'details': serializer.errors}},
        status=status.HTTP_400_BAD_REQUEST
    )


class CustomTokenObtainPairView(TokenObtainPairView):
    """Custom JWT token view that includes user data in response."""

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            from django.contrib.auth import get_user_model
            User = get_user_model()
            user = User.objects.get(username=request.data.get('username'))
            response.data['user'] = UserProfileSerializer(user).data
            response.data['success'] = True
        return response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def profile(request):
    """Get current user profile."""
    serializer = UserProfileSerializer(request.user)
    return Response({'success': True, 'data': serializer.data})


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    """Logout - client should discard tokens."""
    return Response({'success': True, 'message': 'Logged out successfully.'})
