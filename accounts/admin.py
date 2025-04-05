from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.html import format_html
from django.urls import reverse
from .models import Profile

class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = 'Profile'
    fk_name = 'user'

class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_phone', 'get_orders')
    list_select_related = ('profile',)
    
    def get_phone(self, obj):
        try:
            return obj.profile.phone
        except Profile.DoesNotExist:
            return '-'
    get_phone.short_description = 'Phone'
    
    def get_orders(self, obj):
        orders_count = obj.orders.count()
        if orders_count > 0:
            url = reverse('admin:orders_order_changelist') + f'?user__id__exact={obj.id}'
            return format_html('<a href="{}">{} orders</a>', url, orders_count)
        return '0 orders'
    get_orders.short_description = 'Orders'
    
    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)

# Unregister the default UserAdmin and register our custom one
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'address', 'city', 'postal_code']
    raw_id_fields = ['user']
    search_fields = ['user__username', 'user__email', 'phone', 'address', 'city']