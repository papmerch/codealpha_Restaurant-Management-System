from rest_framework import serializers
from .models import Order, OrderItem
from apps.menu.serializers import MenuItemSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    menu_item_details = MenuItemSerializer(source='menu_item', read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'menu_item', 'menu_item_details', 'quantity', 'item_price', 'subtotal', 'notes', 'created_at']
        read_only_fields = ['id', 'item_price', 'subtotal', 'created_at']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    table_number = serializers.CharField(source='table.table_number', read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'order_number', 'table', 'table_number', 'customer_name', 'customer_phone', 
                  'order_status', 'total_amount', 'payment_status', 'notes', 'items', 
                  'created_at', 'updated_at', 'completed_at']
        read_only_fields = ['id', 'order_number', 'total_amount', 'created_at', 'updated_at', 'completed_at']

class OrderCreateSerializer(serializers.Serializer):
    table = serializers.IntegerField(required=False)
    customer_name = serializers.CharField(max_length=200)
    customer_phone = serializers.CharField(max_length=20, required=False, allow_blank=True)
    notes = serializers.CharField(required=False, allow_blank=True)
    items = serializers.ListField(
        child=serializers.DictField(
            child=serializers.JSONField()
        )
    )
    
    def validate_items(self, value):
        if not value:
            raise serializers.ValidationError('At least one item is required')
        for item in value:
            if 'menu_item' not in item or 'quantity' not in item:
                raise serializers.ValidationError('Each item must have menu_item and quantity')
            if item['quantity'] < 1:
                raise serializers.ValidationError('Quantity must be at least 1')
        return value

class OrderStatusUpdateSerializer(serializers.Serializer):
    order_status = serializers.ChoiceField(choices=Order.STATUS_CHOICES)