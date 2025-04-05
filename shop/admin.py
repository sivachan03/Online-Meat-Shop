from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'description_preview', 'image_preview']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    list_filter = ['name']
    def description_preview(self, obj):
        return obj.description[:50] + '...' if len(obj.description) > 50 else obj.description
    description_preview.short_description = 'Description'
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Image'

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'category', 'price', 'weight', 'stock', 'available', 'image_preview', 'created', 'updated']
    list_filter = ['available', 'created', 'updated', 'category']
    list_editable = ['price', 'stock', 'available']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    date_hierarchy = 'created'
    ordering = ['name']
    readonly_fields = ['image_full']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'weight', 'stock', 'available')
        }),
        ('Media', {
            'fields': ('image', 'image_full')
        }),
        #('Timestamps', {
            #'fields': ('created', 'updated'),
           # 'classes': ('collapse',)
        #}),
    )
    
    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="30" height="30" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Image'
    
    def image_full(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="300" />', obj.image.url)
        return "No Image"
    image_full.short_description = 'Image Preview'