from django.db import models

class Table(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('occupied', 'Occupied'),
        ('reserved', 'Reserved'),
        ('maintenance', 'Maintenance'),
    ]
    
    SECTION_CHOICES = [
        ('indoor', 'Indoor'),
        ('outdoor', 'Outdoor'),
        ('vip', 'VIP'),
        ('bar', 'Bar'),
    ]
    
    table_number = models.CharField(max_length=10, unique=True)
    seating_capacity = models.IntegerField()
    availability_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    location_section = models.CharField(max_length=20, choices=SECTION_CHOICES, default='indoor')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['table_number']
    
    def __str__(self):
        return f"Table {self.table_number} ({self.seating_capacity} seats)"