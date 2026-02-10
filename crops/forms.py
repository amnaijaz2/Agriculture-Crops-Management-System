"""
Forms for Crop CRUD operations.
"""
from django import forms
from django.contrib.auth import get_user_model
from .models import Crop, CropType, CropStatus

User = get_user_model()


class CropForm(forms.ModelForm):
    """Form for creating/editing crops."""
    class Meta:
        model = Crop
        fields = [
            'name', 'crop_type', 'quantity', 'unit', 'price',
            'location', 'status', 'description'
        ]

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Crop Name'}),
            'crop_type': forms.Select(attrs={'class': 'form-select'}, choices=CropType.choices),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Quantity', 'step': '0.01'}),
            'unit': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Unit (e.g. kg)'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price', 'step': '0.01'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'status': forms.Select(attrs={'class': 'form-select'}, choices=CropStatus.choices),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Description'}),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user and user.role == 'ADMIN':
            self.fields['farmer'] = forms.ModelChoiceField(
                queryset=User.objects.filter(role='FARMER'),
                required=True,
                widget=forms.Select(attrs={'class': 'form-select'}),
                empty_label='Select Farmer'
            )
            if self.instance and self.instance.pk:
                self.fields['farmer'].initial = self.instance.farmer
