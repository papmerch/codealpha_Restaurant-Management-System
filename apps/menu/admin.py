from django.contrib import admin
from .models import Category, MenuItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name']

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'availability_status', 'preparation_time', 'created_at']
    list_filter = ['category', 'availability_status']
    search_fields = ['name', 'description']
    list_editable = ['availability_status', 'price']