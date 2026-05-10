from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('admin/', admin.site.urls),
    path('api/auth/', include('apps.users.urls')),
    path('api/menu/', include('apps.menu.urls')),
    path('api/tables/', include('apps.tables.urls')),
    path('api/reservations/', include('apps.reservations.urls')),
    path('api/orders/', include('apps.orders.urls')),
    path('api/inventory/', include('apps.inventory.urls')),
    path('api/reports/', include('apps.reports.urls')),
    path('', include('config.api_docs_urls')),
]