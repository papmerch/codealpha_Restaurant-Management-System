from rest_framework import serializers
from .models import Report

class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ['id', 'report_type', 'date_from', 'date_to', 'data', 'created_at']
        read_only_fields = ['id', 'created_at']

class DailySalesSerializer(serializers.Serializer):
    date = serializers.DateField()
    total_orders = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    average_order_value = serializers.DecimalField(max_digits=10, decimal_places=2)

class SalesReportSerializer(serializers.Serializer):
    period = serializers.CharField()
    total_orders = serializers.IntegerField()
    total_revenue = serializers.DecimalField(max_digits=12, decimal_places=2)
    average_order_value = serializers.DecimalField(max_digits=10, decimal_places=2)
    top_items = serializers.ListField()

class LowStockReportSerializer(serializers.Serializer):
    ingredient_name = serializers.CharField()
    current_stock = serializers.DecimalField(max_digits=10, decimal_places=2)
    unit = serializers.CharField()
    minimum_threshold = serializers.DecimalField(max_digits=10, decimal_places=2)

class ReservationStatsSerializer(serializers.Serializer):
    total_reservations = serializers.IntegerField()
    confirmed = serializers.IntegerField()
    cancelled = serializers.IntegerField()
    completed = serializers.IntegerField()
    average_guests = serializers.FloatField()