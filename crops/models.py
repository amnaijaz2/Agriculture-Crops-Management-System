"""
Crop model for agriculture management.
"""
from django.db import models
from django.conf import settings


class CropStatus(models.TextChoices):
    """Crop status choices."""
    AVAILABLE = 'AVAILABLE', 'Available'
    RESERVED = 'RESERVED', 'Reserved'
    SOLD = 'SOLD', 'Sold'
    OUT_OF_STOCK = 'OUT_OF_STOCK', 'Out of Stock'


class CropType(models.TextChoices):
    """Crop type choices."""
    GRAIN = 'GRAIN', 'Grain'
    VEGETABLE = 'VEGETABLE', 'Vegetable'
    FRUIT = 'FRUIT', 'Fruit'
    PULSE = 'PULSE', 'Pulse'
    SPICE = 'SPICE', 'Spice'
    OTHER = 'OTHER', 'Other'


class Crop(models.Model):
    """Crop model for storing crop listings."""
    name = models.CharField(max_length=200)
    crop_type = models.CharField(max_length=20, choices=CropType.choices, default=CropType.OTHER)
    quantity = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    unit = models.CharField(max_length=20, default='kg')
    price = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    farmer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='crops',
        limit_choices_to={'role': 'FARMER'}
    )
    location = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=CropStatus.choices,
        default=CropStatus.AVAILABLE
    )
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'crops'
        verbose_name = 'Crop'
        verbose_name_plural = 'Crops'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.quantity} {self.unit} @ {self.farmer.username}"
