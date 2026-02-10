"""
Forms for Orders module.
"""
from django import forms
from .models import Order, OrderStatus
from crops.models import Crop


class OrderCreateForm(forms.ModelForm):
    """Form for placing an order."""
    class Meta:
        model = Order
        fields = ['crop', 'quantity', 'shipping_address', 'notes']
        widgets = {
            'crop': forms.Select(attrs={'class': 'form-select'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity', 'step': '0.01'}),
            'shipping_address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Shipping Address'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Notes (optional)'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['crop'].queryset = Crop.objects.filter(status='AVAILABLE', quantity__gt=0)


class OrderStatusUpdateForm(forms.ModelForm):
    """Form for updating order status."""
    class Meta:
        model = Order
        fields = ['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-select'}, choices=OrderStatus.choices),
        }
