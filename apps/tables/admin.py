from django.contrib import admin
from .models import Table

@admin.register(Table)
class TableAdmin(admin.ModelAdmin):
    list_display = ['table_number', 'seating_capacity', 'availability_status', 'location_section']
    list_filter = ['availability_status', 'location_section']
    search_fields = ['table_number', 'location_section']
    list_editable = ['availability_status']