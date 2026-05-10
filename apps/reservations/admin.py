from django.contrib import admin
from .models import Reservation

@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'phone_number', 'reservation_time', 'guest_count', 'assigned_table', 'reservation_status']
    list_filter = ['reservation_status', 'reservation_time']
    search_fields = ['customer_name', 'phone_number', 'assigned_table__table_number']
    date_hierarchy = 'reservation_time'