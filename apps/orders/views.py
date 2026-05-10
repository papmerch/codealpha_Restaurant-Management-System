from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.utils import timezone
from django.db import transaction
from .models import Order, OrderItem
from .serializers import OrderSerializer, OrderCreateSerializer, OrderStatusUpdateSerializer
from apps.menu.models import MenuItem
from apps.tables.models import Table
from apps.inventory.models import InventoryItem

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.select_related('table').prefetch_related('items__menu_item').all()
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return OrderCreateSerializer
        if self.action in ['update', 'partial_update']:
            return OrderStatusUpdateSerializer
        return OrderSerializer
    
    def get_queryset(self):
        queryset = Order.objects.select_related('table').prefetch_related('items__menu_item')
        
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(order_status=status_filter)
        
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        
        if date_from:
            queryset = queryset.filter(created_at__gte=date_from)
        if date_to:
            queryset = queryset.filter(created_at__lte=date_to)
        
        return queryset
    
    @transaction.atomic
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        table = None
        table_id = serializer.validated_data.get('table')
        if table_id:
            try:
                table = Table.objects.get(id=table_id)
                table.availability_status = 'occupied'
                table.save()
            except Table.DoesNotExist:
                pass
        
        order = Order.objects.create(
            table=table,
            customer_name=serializer.validated_data.get('customer_name', 'Walk-in Customer'),
            customer_phone=serializer.validated_data.get('customer_phone', ''),
            notes=serializer.validated_data.get('notes', ''),
            order_status='pending'
        )
        
        total = 0
        for item_data in serializer.validated_data['items']:
            menu_item = MenuItem.objects.get(id=item_data['menu_item'])
            
            if menu_item.availability_status != 'available':
                order.delete()
                return Response(
                    {'error': f'Item {menu_item.name} is not available'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            order_item = OrderItem.objects.create(
                order=order,
                menu_item=menu_item,
                quantity=item_data['quantity'],
                notes=item_data.get('notes', '')
            )
            total += order_item.subtotal
            
            self._deduct_inventory(menu_item, item_data['quantity'])
        
        order.total_amount = total
        order.save()
        
        return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
    
    def _deduct_inventory(self, menu_item, quantity):
        pass
    
    @transaction.atomic
    def partial_update(self, request, *args, **kwargs):
        order = self.get_object()
        serializer = OrderStatusUpdateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        
        old_status = order.order_status
        new_status = serializer.validated_data['order_status']
        
        order.order_status = new_status
        
        if new_status == 'completed':
            order.completed_at = timezone.now()
            if order.payment_status == 'paid' and order.table:
                order.table.availability_status = 'available'
                order.table.save()
        elif old_status == 'completed' and new_status != 'completed':
            order.completed_at = None
            if order.table:
                order.table.availability_status = 'occupied'
                order.table.save()
        
        order.save()
        return Response(OrderSerializer(order).data)
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        order = self.get_object()
        
        if order.order_status in ['completed', 'served']:
            return Response({'error': 'Cannot cancel completed or served orders'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.order_status = 'cancelled'
        order.save()
        
        if order.table:
            order.table.availability_status = 'available'
            order.table.save()
        
        return Response(OrderSerializer(order).data)
    
    @action(detail=True, methods=['post'])
    def payment(self, request, pk=None):
        order = self.get_object()
        payment_status = request.data.get('payment_status')
        
        if payment_status not in ['pending', 'paid', 'failed']:
            return Response({'error': 'Invalid payment status'}, status=status.HTTP_400_BAD_REQUEST)
        
        order.payment_status = payment_status
        order.save()
        
        return Response(OrderSerializer(order).data)