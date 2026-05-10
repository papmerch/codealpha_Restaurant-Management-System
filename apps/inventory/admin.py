from django.contrib import admin
from .models import InventoryItem, InventoryLog

class InventoryLogInline(admin.TabularInline):
    model = InventoryLog
    extra = 0
    readonly_fields = ['change_amount', 'reason', 'timestamp']
    can_delete = False

@admin.register(InventoryItem)
class InventoryItemAdmin(admin.ModelAdmin):
    list_display = ['ingredient_name', 'current_stock', 'unit', 'minimum_threshold', 'supplier', 'last_updated']
    list_filter = ['unit']
    search_fields = ['ingredient_name', 'supplier']
    list_editable = ['current_stock', 'minimum_threshold']
    inlines = [InventoryLogInline]

@admin.register(InventoryLog)
class InventoryLogAdmin(admin.ModelAdmin):
    list_display = ['ingredient', 'change_amount', 'reason', 'timestamp']
    list_filter = ['reason', 'timestamp']
    search_fields = ['ingredient__ingredient_name']
    date_hierarchy = 'timestamp'