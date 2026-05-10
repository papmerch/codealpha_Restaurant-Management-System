from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .models import Table
from .serializers import TableSerializer

class TableViewSet(viewsets.ModelViewSet):
    queryset = Table.objects.all()
    serializer_class = TableSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    @action(detail=True, methods=['patch'])
    def status(self, request, pk=None):
        table = self.get_object()
        new_status = request.data.get('availability_status')
        
        if new_status not in ['available', 'occupied', 'reserved', 'maintenance']:
            return Response({'error': 'Invalid status'}, status=status.HTTP_400_BAD_REQUEST)
        
        table.availability_status = new_status
        table.save()
        return Response(TableSerializer(table).data)