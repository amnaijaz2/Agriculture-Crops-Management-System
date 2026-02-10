"""
User model with role-based authorization.
"""
from django.contrib.auth.models import AbstractUser
from django.db import models


class Role(models.TextChoices):
    """User role choices."""
    ADMIN = 'ADMIN', 'Admin'
    FARMER = 'FARMER', 'Farmer'
    BROKER = 'BROKER', 'Broker'
    CLIENT = 'CLIENT', 'Client'


class User(AbstractUser):
    """Custom User model with role-based access control."""
    role = models.CharField(
        max_length=10,
        choices=Role.choices,
        default=Role.CLIENT
    )
    phone = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.username} ({self.get_role_display()})"

    @property
    def is_admin(self):
        return self.role == Role.ADMIN

    @property
    def is_farmer(self):
        return self.role == Role.FARMER

    @property
    def is_broker(self):
        return self.role == Role.BROKER

    @property
    def is_client(self):
        return self.role == Role.CLIENT
