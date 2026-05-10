from django.urls import path
from .views import (
    DailySalesView, WeeklySalesView, MonthlySalesView,
    TopSellingItemsView, LowStockView, ReservationStatsView, DashboardStatsView
)

urlpatterns = [
    path('dashboard/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('daily-sales/', DailySalesView.as_view(), name='daily-sales'),
    path('weekly-sales/', WeeklySalesView.as_view(), name='weekly-sales'),
    path('monthly-sales/', MonthlySalesView.as_view(), name='monthly-sales'),
    path('top-items/', TopSellingItemsView.as_view(), name='top-items'),
    path('low-stock/', LowStockView.as_view(), name='low-stock'),
    path('reservations/', ReservationStatsView.as_view(), name='reservation-stats'),
]