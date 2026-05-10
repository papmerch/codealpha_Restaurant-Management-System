from django.db import models
from django.utils import timezone

class Reservation(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('seated', 'Seated'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('no_show', 'No Show'),
    ]
    
    customer_name = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(blank=True)
    reservation_time = models.DateTimeField()
    guest_count = models.IntegerField()
    assigned_table = models.ForeignKey('tables.Table', on_delete=models.SET_NULL, null=True, blank=True, related_name='reservations')
    reservation_status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    special_requests = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['reservation_time']
    
    def __str__(self):
        return f"{self.customer_name} - {self.reservation_time.strftime('%Y-%m-%d %H:%M')}"