from rest_framework import serializers
from .models import Table

class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'table_number', 'seating_capacity', 'availability_status', 'location_section', 'created_at', 'updated_at']
        read_only_fields = ['id', 'created_at', 'updated_at']

class TableAvailabilitySerializer(serializers.Serializer):
    date = serializers.DateField()
    time = serializers.TimeField()
    guest_count = serializers.IntegerField(min_value=1)