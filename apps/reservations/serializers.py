from rest_framework import serializers
from .models import Reservation
from apps.tables.models import Table

class ReservationSerializer(serializers.ModelSerializer):
    table_number = serializers.CharField(source='assigned_table.table_number', read_only=True)
    
    class Meta:
        model = Reservation
        fields = ['id', 'customer_name', 'phone_number', 'email', 'reservation_time', 
                  'guest_count', 'assigned_table', 'table_number', 'reservation_status', 
                  'special_requests', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']
    
    def validate(self, attrs):
        reservation_time = attrs.get('reservation_time')
        guest_count = attrs.get('guest_count')
        
        if reservation_time and reservation_time < timezone.now():
            raise serializers.ValidationError({'reservation_time': 'Reservation time must be in the future'})
        
        if guest_count and guest_count > 20:
            raise serializers.ValidationError({'guest_count': 'Maximum 20 guests per reservation'})
        
        return attrs

class ReservationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ['customer_name', 'phone_number', 'email', 'reservation_time', 'guest_count', 'special_requests']
    
    def validate(self, attrs):
        reservation_time = attrs.get('reservation_time')
        guest_count = attrs.get('guest_count')
        
        if reservation_time and reservation_time < timezone.now():
            raise serializers.ValidationError({'reservation_time': 'Reservation time must be in the future'})
        
        if guest_count and guest_count > 20:
            raise serializers.ValidationError({'guest_count': 'Maximum 20 guests per reservation'})
        
        available_tables = Table.objects.filter(
            seating_capacity__gte=guest_count,
            availability_status='available'
        )
        
        if not available_tables.exists():
            raise serializers.ValidationError({'guest_count': 'No available tables for this guest count'})
        
        return attrs