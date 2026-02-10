"""
Admin configuration for Order models.
"""
from django.contrib import admin
from .models import Order, OrderStatusHistory


class OrderStatusHistoryInline(admin.TabularInline):
    model = OrderStatusHistory
    extra = 0
    readonly_fields = ['from_status', 'to_status', 'changed_by', 'created_at']


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'crop', 'quantity', 'total_amount', 'status', 'created_at')
    list_filter = ('status',)
    search_fields = ('client__username', 'crop__name')
    inlines = [OrderStatusHistoryInline]


@admin.register(OrderStatusHistory)
class OrderStatusHistoryAdmin(admin.ModelAdmin):
    list_display = ('order', 'from_status', 'to_status', 'changed_by', 'created_at')
