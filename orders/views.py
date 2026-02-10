"""
Template-based views for Orders module.
"""
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Order
from .forms import OrderCreateForm, OrderStatusUpdateForm


class ClientOrBrokerOrAdminMixin(UserPassesTestMixin):
    """Allow Client, Broker, or Admin."""
    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.role in ['CLIENT', 'BROKER', 'ADMIN']


class OrderListView(LoginRequiredMixin, ListView):
    """Display list of orders."""
    model = Order
    template_name = 'orders/order_list.html'
    context_object_name = 'orders'
    paginate_by = 15

    def get_queryset(self):
        qs = Order.objects.select_related('client', 'crop', 'crop__farmer')
        if self.request.user.role == 'CLIENT':
            qs = qs.filter(client=self.request.user)
        elif self.request.user.role == 'FARMER':
            qs = qs.filter(crop__farmer=self.request.user)
        return qs.order_by('-created_at')


class OrderDetailView(LoginRequiredMixin, DetailView):
    """Display order details."""
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        qs = Order.objects.select_related('client', 'crop', 'crop__farmer')
        if self.request.user.role == 'CLIENT':
            return qs.filter(client=self.request.user)
        elif self.request.user.role == 'FARMER':
            return qs.filter(crop__farmer=self.request.user)
        return qs


class OrderCreateView(LoginRequiredMixin, ClientOrBrokerOrAdminMixin, CreateView):
    """Place a new order."""
    model = Order
    form_class = OrderCreateForm
    template_name = 'orders/order_form.html'
    success_url = reverse_lazy('orders:order_list')

    def get_initial(self):
        initial = super().get_initial()
        crop_id = self.request.GET.get('crop')
        if crop_id:
            initial['crop'] = crop_id
        return initial

    def form_valid(self, form):
        form.instance.client = self.request.user
        return super().form_valid(form)


class OrderStatusUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Update order status (Broker/Admin/Farmer)."""
    model = Order
    form_class = OrderStatusUpdateForm
    template_name = 'orders/order_status_form.html'
    context_object_name = 'order'
    success_url = reverse_lazy('orders:order_list')

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.role in ['ADMIN', 'BROKER', 'FARMER']

    def get_queryset(self):
        qs = Order.objects.all()
        if self.request.user.role == 'FARMER':
            return qs.filter(crop__farmer=self.request.user)
        return qs
