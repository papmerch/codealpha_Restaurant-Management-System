from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from datetime import timedelta
from django.db.models import Sum, Count, Avg, F
from apps.orders.models import Order
from apps.reservations.models import Reservation
from apps.inventory.models import InventoryItem
from apps.menu.models import MenuItem
from apps.orders.models import OrderItem

class DailySalesView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        date_str = request.query_params.get('date')
        
        if date_str:
            from datetime import datetime
            date = datetime.strptime(date_str, '%Y-%m-%d').date()
        else:
            date = timezone.now().date()
        
        start_of_day = timezone.make_aware(timezone.datetime.combine(date, timezone.datetime.min.time()))
        end_of_day = start_of_day + timedelta(days=1)
        
        orders = Order.objects.filter(
            created_at__gte=start_of_day,
            created_at__lt=end_of_day,
            order_status__in=['completed', 'served', 'ready', 'preparing', 'pending']
        )
        
        total_orders = orders.count()
        total_revenue = orders.aggregate(total=Sum('total_amount'))['total'] or 0
        avg_order = total_revenue / total_orders if total_orders > 0 else 0
        
        return Response({
            'date': str(date),
            'total_orders': total_orders,
            'total_revenue': float(total_revenue),
            'average_order_value': float(avg_order)
        })

class WeeklySalesView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        today = timezone.now().date()
        start_of_week = today - timedelta(days=today.weekday())
        end_of_week = start_of_week + timedelta(days=7)
        
        orders = Order.objects.filter(
            created_at__date__gte=start_of_week,
            created_at__date__lt=end_of_week,
            order_status__in=['completed', 'served']
        )
        
        total_orders = orders.count()
        total_revenue = orders.aggregate(total=Sum('total_amount'))['total'] or 0
        avg_order = total_revenue / total_orders if total_orders > 0 else 0
        
        return Response({
            'period': f'{start_of_week} to {end_of_week}',
            'total_orders': total_orders,
            'total_revenue': float(total_revenue),
            'average_order_value': float(avg_order)
        })

class MonthlySalesView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        today = timezone.now().date()
        start_of_month = today.replace(day=1)
        
        if today.month == 12:
            end_of_month = today.replace(year=today.year + 1, month=1, day=1)
        else:
            end_of_month = today.replace(month=today.month + 1, day=1)
        
        orders = Order.objects.filter(
            created_at__date__gte=start_of_month,
            created_at__date__lt=end_of_month,
            order_status__in=['completed', 'served']
        )
        
        total_orders = orders.count()
        total_revenue = orders.aggregate(total=Sum('total_amount'))['total'] or 0
        avg_order = total_revenue / total_orders if total_orders > 0 else 0
        
        return Response({
            'period': f'{start_of_month.strftime("%B")} {start_of_month.year}',
            'total_orders': total_orders,
            'total_revenue': float(total_revenue),
            'average_order_value': float(avg_order)
        })

class TopSellingItemsView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        limit = int(request.query_params.get('limit', 10))
        
        top_items = OrderItem.objects.values(
            'menu_item__name'
        ).annotate(
            total_sold=Sum('quantity'),
            total_revenue=Sum('subtotal')
        ).order_by('-total_sold')[:limit]
        
        return Response(list(top_items))

class LowStockView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        from django.db.models import F
        low_stock = InventoryItem.objects.filter(
            current_stock__lte=F('minimum_threshold')
        ).values('ingredient_name', 'current_stock', 'unit', 'minimum_threshold')
        
        return Response(list(low_stock))

class ReservationStatsView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        status_counts = Reservation.objects.values('reservation_status').annotate(count=Count('id'))
        total = Reservation.objects.count()
        
        avg_guests = Reservation.objects.aggregate(avg=Avg('guest_count'))['avg'] or 0
        
        return Response({
            'total_reservations': total,
            'status_breakdown': {item['reservation_status']: item['count'] for item in status_counts},
            'average_guests': float(avg_guests)
        })

class DashboardStatsView(views.APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        today = timezone.now().date()
        start_of_day = timezone.make_aware(timezone.datetime.combine(today, timezone.datetime.min.time()))
        
        today_orders = Order.objects.filter(created_at__gte=start_of_day).count()
        today_revenue = Order.objects.filter(
            created_at__gte=start_of_day,
            order_status='completed',
            payment_status='paid'
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        upcoming_reservations = Reservation.objects.filter(
            reservation_time__gte=timezone.now(),
            reservation_status__in=['pending', 'confirmed']
        ).count()
        
        low_stock_count = InventoryItem.objects.filter(
            current_stock__lte=F('minimum_threshold')
        ).count()
        
        active_orders = Order.objects.filter(
            order_status__in=['pending', 'preparing', 'ready', 'served']
        ).count()
        
        return Response({
            'today_orders': today_orders,
            'today_revenue': float(today_revenue),
            'upcoming_reservations': upcoming_reservations,
            'low_stock_items': low_stock_count,
            'active_orders': active_orders
        })