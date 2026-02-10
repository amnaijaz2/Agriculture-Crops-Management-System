"""
Template-based views for Crops module.
"""
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from .models import Crop
from .forms import CropForm


class FarmerOrAdminMixin(UserPassesTestMixin):
    """Allow Farmer or Admin to manage crops."""
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.role in ['FARMER', 'ADMIN']


class CropListView(LoginRequiredMixin, ListView):
    """Display list of crops."""
    model = Crop
    template_name = 'crops/crop_list.html'
    context_object_name = 'crops'
    paginate_by = 12

    def get_queryset(self):
        qs = Crop.objects.select_related('farmer')
        if self.request.user.role == 'FARMER':
            qs = qs.filter(farmer=self.request.user)
        return qs.order_by('-created_at')


class CropDetailView(LoginRequiredMixin, DetailView):
    """Display crop details."""
    model = Crop
    template_name = 'crops/crop_detail.html'
    context_object_name = 'crop'


class CropCreateView(LoginRequiredMixin, FarmerOrAdminMixin, CreateView):
    """Create new crop."""
    model = Crop
    form_class = CropForm
    template_name = 'crops/crop_form.html'
    success_url = reverse_lazy('crops:crop_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def form_valid(self, form):
        if self.request.user.role == 'FARMER':
            form.instance.farmer = self.request.user
        elif hasattr(form, 'cleaned_data') and form.cleaned_data.get('farmer'):
            form.instance.farmer = form.cleaned_data['farmer']
        else:
            form.instance.farmer = self.request.user
        return super().form_valid(form)


class CropUpdateView(LoginRequiredMixin, FarmerOrAdminMixin, UpdateView):
    """Update crop."""
    model = Crop
    form_class = CropForm
    template_name = 'crops/crop_form.html'
    context_object_name = 'crop'
    success_url = reverse_lazy('crops:crop_list')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.role == 'FARMER':
            return qs.filter(farmer=self.request.user)
        return qs


class CropDeleteView(LoginRequiredMixin, FarmerOrAdminMixin, DeleteView):
    """Delete crop."""
    model = Crop
    template_name = 'crops/crop_confirm_delete.html'
    success_url = reverse_lazy('crops:crop_list')
    context_object_name = 'crop'

    def get_queryset(self):
        qs = super().get_queryset()
        if self.request.user.role == 'FARMER':
            return qs.filter(farmer=self.request.user)
        return qs
