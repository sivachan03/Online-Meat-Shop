from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from datetime import timedelta
from shop.models import Product, Category
from orders.models import Order, OrderItem

class DashboardAdmin(admin.AdminSite):
    site_header = 'Premium Meat Shop Administration'
    site_title = 'Meat Shop Admin'
    index_title = 'Management Dashboard'
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
        ]
        return custom_urls + urls
    
    def dashboard_view(self, request):
        # Get date ranges
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        start_of_month = today.replace(day=1)
        
        # Sales statistics
        total_sales = Order.objects.filter(paid=True).aggregate(
            total=Sum('items__price'))['total'] or 0
        
        sales_today = Order.objects.filter(
            paid=True, created__date=today).aggregate(
            total=Sum('items__price'))['total'] or 0
            
        sales_this_week = Order.objects.filter(
            paid=True, created__date__gte=start_of_week).aggregate(
            total=Sum('items__price'))['total'] or 0
            
        sales_this_month = Order.objects.filter(
            paid=True, created__date__gte=start_of_month).aggregate(
            total=Sum('items__price'))['total'] or 0
        
        # Order statistics
        total_orders = Order.objects.count()
        pending_orders = Order.objects.filter(status='pending').count()
        processing_orders = Order.objects.filter(status='processing').count()
        shipped_orders = Order.objects.filter(status='shipped').count()
        
        # Product statistics
        total_products = Product.objects.count()
        out_of_stock = Product.objects.filter(stock=0).count()
        low_stock = Product.objects.filter(stock__gt=0, stock__lte=5).count()
        
        # Top selling products
        top_products = OrderItem.objects.values(
            'product__name').annotate(
            total_sold=Sum('quantity')).order_by('-total_sold')[:5]
        
        # Recent orders
        recent_orders = Order.objects.order_by('-created')[:10]
        
        context = {
            'title': 'Dashboard',
            'total_sales': total_sales,
            'sales_today': sales_today,
            'sales_this_week': sales_this_week,
            'sales_this_month': sales_this_month,
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'processing_orders': processing_orders,
            'shipped_orders': shipped_orders,
            'total_products': total_products,
            'out_of_stock': out_of_stock,
            'low_stock': low_stock,
            'top_products': top_products,
            'recent_orders': recent_orders,
        }
        
        return render(request, 'admin/dashboard.html', context)

# Create a custom admin site
dashboard_site = DashboardAdmin(name='dashboard')

# Register models with the custom admin site
dashboard_site.register(Product)
dashboard_site.register(Category)
dashboard_site.register(Order)