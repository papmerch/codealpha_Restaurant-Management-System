from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.utils import timezone
from datetime import timedelta
from .models import Reservation
from .serializers import ReservationSerializer, ReservationCreateSerializer
from apps.tables.models import Table

class ReservationViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    def get_serializer_class(self):
        if self.action == 'create':
            return ReservationCreateSerializer
        return ReservationSerializer
    
    def get_queryset(self):
        queryset = Reservation.objects.select_related('assigned_table').all()
        
        status_filter = self.request.query_params.get('status')
        if status_filter:
            queryset = queryset.filter(reservation_status=status_filter)
        
        date_from = self.request.query_params.get('date_from')
        date_to = self.request.query_params.get('date_to')
        
        if date_from:
            queryset = queryset.filter(reservation_time__gte=date_from)
        if date_to:
            queryset = queryset.filter(reservation_time__lte=date_to)
        
        return queryset
    
    def perform_create(self, serializer):
        reservation = serializer.save()
        guest_count = reservation.guest_count
        
        available_table = Table.objects.filter(
            seating_capacity__gte=guest_count,
            availability_status='available'
        ).first()
        
        if available_table:
            reservation.assigned_table = available_table
            reservation.reservation_status = 'confirmed'
            available_table.availability_status = 'reserved'
            available_table.save()
            reservation.save()
    
    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        reservation = self.get_object()
        
        if reservation.reservation_status in ['cancelled', 'completed']:
            return Response({'error': 'Cannot cancel this reservation'}, status=status.HTTP_400_BAD_REQUEST)
        
        reservation.reservation_status = 'cancelled'
        reservation.save()
        
        if reservation.assigned_table:
            reservation.assigned_table.availability_status = 'available'
            reservation.assigned_table.save()
        
        return Response(ReservationSerializer(reservation).data)
    
    @action(detail=False, methods=['get'])
    def upcoming(self, request):
        upcoming_reservations = Reservation.objects.filter(
            reservation_time__gte=timezone.now(),
            reservation_status__in=['pending', 'confirmed']
        ).select_related('assigned_table')[:10]
        
        serializer = self.get_serializer(upcoming_reservations, many=True)
        return Response(serializer.data)