"""
Dashboard views - statistics and overview.
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.db.models import Sum, Count
from users.models import User
from crops.models import Crop
from orders.models import Order


class DashboardView(LoginRequiredMixin, TemplateView):
    """Main dashboard with statistics and charts."""
    template_name = 'dashboards/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user

        # Role-based statistics
        if user.role == 'ADMIN':
            context['total_users'] = User.objects.count()
            context['total_crops'] = Crop.objects.count()
            context['total_orders'] = Order.objects.count()
            context['total_revenue'] = Order.objects.aggregate(total=Sum('total_amount'))['total'] or 0
            context['recent_orders'] = Order.objects.select_related('client', 'crop').order_by('-created_at')[:10]
            context['recent_users'] = User.objects.order_by('-date_joined')[:5]
        elif user.role == 'FARMER':
            my_crops = Crop.objects.filter(farmer=user)
            context['total_crops'] = my_crops.count()
            context['total_stock'] = my_crops.aggregate(total=Sum('quantity'))['total'] or 0
            my_orders = Order.objects.filter(crop__farmer=user)
            context['total_orders'] = my_orders.count()
            context['total_revenue'] = my_orders.aggregate(total=Sum('total_amount'))['total'] or 0
            context['recent_orders'] = my_orders.select_related('client', 'crop').order_by('-created_at')[:10]
        elif user.role == 'BROKER':
            context['total_crops'] = Crop.objects.filter(status='AVAILABLE').count()
            context['total_orders'] = Order.objects.count()
            context['recent_orders'] = Order.objects.select_related('client', 'crop').order_by('-created_at')[:10]
        else:  # CLIENT
            my_orders = Order.objects.filter(client=user)
            context['total_orders'] = my_orders.count()
            context['total_spent'] = my_orders.aggregate(total=Sum('total_amount'))['total'] or 0
            context['available_crops'] = Crop.objects.filter(status='AVAILABLE', quantity__gt=0).count()
            context['recent_orders'] = my_orders.select_related('crop', 'crop__farmer').order_by('-created_at')[:10]

        # Crop type distribution for charts
        context['crop_types'] = Crop.objects.values('crop_type').annotate(count=Count('id')).order_by('-count')[:6]
        context['order_statuses'] = Order.objects.values('status').annotate(count=Count('id'))
        return context


class RedirectDashboardView(LoginRequiredMixin, TemplateView):
    """Redirect root to dashboard."""
    template_name = 'dashboards/dashboard.html'

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
