from django.contrib import admin
from django.utils.html import format_html
from django.urls import reverse
from .models import Order, OrderItem

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['product']
    extra = 0
    fields = ['product', 'price', 'quantity', 'get_total']
    readonly_fields = ['get_total']
    
    def get_total(self, obj):
        return obj.get_cost()
    get_total.short_description = 'Total'

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user_link', 'first_name', 'last_name', 'email', 'city', 
                    'paid', 'status_colored', 'created', 'updated', 'order_total']
    list_filter = ['paid', 'status', 'created', 'updated']
    search_fields = ['first_name', 'last_name', 'email', 'address']
    inlines = [OrderItemInline]
   # list_editable = ['paid', 'status']
   # list_editable = ['status']
    date_hierarchy = 'created'
    ordering = ['-created']
    readonly_fields = ['order_total']
   
    fieldsets = (
        ('Customer Information', {
            'fields': (('first_name', 'last_name'), 'email', 'user')
        }),
        ('Shipping Information', {
            'fields': ('address', ('postal_code', 'city'))
        }),
        ('Order Status', {
            'fields': (('paid', 'status'), 'created', 'updated')
        }),
        ('Order Summary', {
            'fields': ('order_total',)
        }),
    )
    
    def user_link(self, obj):
        if obj.user:
            url = reverse('admin:auth_user_change', args=[obj.user.id])
            return format_html('<a href="{}">{}</a>', url, obj.user.username)
        return '-'
    user_link.short_description = 'User'
    
    def status_colored(self, obj):
        colors = {
            'pending': 'orange',
            'processing': 'blue',
            'shipped': 'purple',
            'delivered': 'green',
            'cancelled': 'red',
        }
        return format_html(
            '<span style="color: {};">{}</span>',
            colors.get(obj.status, 'black'),
            obj.get_status_display()
        )
    status_colored.short_description = 'Status'
    
    def order_total(self, obj):
        return f"${obj.get_total_cost()}"
    order_total.short_description = 'Order Total'
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.prefetch_related('items__product')
        return queryset