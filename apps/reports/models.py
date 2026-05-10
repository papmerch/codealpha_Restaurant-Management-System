from django.db import models

class Report(models.Model):
    TYPE_CHOICES = [
        ('daily_sales', 'Daily Sales'),
        ('weekly_sales', 'Weekly Sales'),
        ('monthly_sales', 'Monthly Sales'),
        ('inventory', 'Inventory Report'),
        ('reservations', 'Reservation Report'),
    ]
    
    report_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    date_from = models.DateField()
    date_to = models.DateField()
    data = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.report_type} - {self.date_from} to {self.date_to}"