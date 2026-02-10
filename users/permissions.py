"""
Role-based permission classes for API views.
"""
from rest_framework import permissions
from .models import Role


class IsAdmin(permissions.BasePermission):
    """Allow access only to Admin users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == Role.ADMIN


class IsFarmer(permissions.BasePermission):
    """Allow access only to Farmer users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == Role.FARMER


class IsBroker(permissions.BasePermission):
    """Allow access only to Broker users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == Role.BROKER


class IsClient(permissions.BasePermission):
    """Allow access only to Client users."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == Role.CLIENT


class IsAdminOrFarmer(permissions.BasePermission):
    """Allow access to Admin or Farmer."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [Role.ADMIN, Role.FARMER]


class IsAdminOrBroker(permissions.BasePermission):
    """Allow access to Admin or Broker."""
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in [Role.ADMIN, Role.BROKER]


class IsAdminOrReadOnly(permissions.BasePermission):
    """Allow Admin to edit, others read-only."""
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return request.user.is_authenticated
        return request.user.is_authenticated and request.user.role == Role.ADMIN
