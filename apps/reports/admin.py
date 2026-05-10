from django.contrib import admin
from .models import Report

@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ['report_type', 'date_from', 'date_to', 'created_at']
    list_filter = ['report_type', 'created_at']