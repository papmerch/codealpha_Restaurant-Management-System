# Restaurant Management System

A comprehensive Django-based Restaurant Management System with REST API, admin panel, and reporting capabilities.

## Features

- **Authentication & Authorization**: JWT-based auth with role-based permissions (Admin, Manager, Staff, Customer)
- **Menu Management**: CRUD operations for menu items and categories
- **Table Management**: Table availability tracking and management
- **Reservation System**: Full reservation workflow with conflict prevention
- **Order Processing**: Complete order lifecycle from creation to completion
- **Inventory Management**: Stock tracking, low-stock alerts, and inventory history
- **Reporting & Analytics**: Daily, weekly, monthly sales, top-selling items, dashboard stats

## Tech Stack

- **Backend**: Django 5.0 + Django REST Framework
- **Database**: SQLite (development) / PostgreSQL (production)
- **Authentication**: JWT (djangorestframework-simplejwt)
- **API Documentation**: Swagger/OpenAPI (drf-yasg)
- **Frontend**: Bootstrap 5 (Admin Dashboard)

## Project Structure

```
restaurant_management/
├── apps/
│   ├── users/          # Authentication & user management
│   ├── menu/           # Menu items & categories
│   ├── tables/         # Table management
│   ├── reservations/   # Reservation system
│   ├── orders/         # Order processing
│   ├── inventory/      # Inventory management
│   └── reports/        # Analytics & reporting
├── config/             # Django settings & URLs
├── templates/          # HTML templates
├── manage.py
├── requirements.txt
└── .env
```

## Setup Instructions

### Prerequisites
- Python 3.8+
- pip

### Installation

1. Navigate to project directory:
```bash
cd restaurant_management
```

2. Create virtual environment:
```bash
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser:
```bash
python manage.py createsuperuser
```

6. Run server:
```bash
python manage.py runserver
```

### Default Login Credentials

After creating the superuser, you can login at:
- **Admin Panel**: http://localhost:8000/admin/
- **Username**: `admin`
- **Password**: `admin`

## API Documentation

Access API docs at:
- Swagger: http://localhost:8000/swagger/
- ReDoc: http://localhost:8000/redoc/

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register new user
- `POST /api/auth/login/` - Login (returns JWT tokens)
- `POST /api/auth/logout/` - Logout
- `GET /api/auth/me/` - Current user profile

### Menu
- `GET /api/menu/categories/` - List categories
- `POST /api/menu/categories/` - Create category
- `GET /api/menu/items/` - List menu items
- `POST /api/menu/items/` - Create menu item
- `PUT /api/menu/items/{id}/` - Update menu item
- `DELETE /api/menu/items/{id}/` - Delete menu item

### Tables
- `GET /api/tables/` - List tables
- `POST /api/tables/` - Create table
- `PATCH /api/tables/{id}/status/` - Update table status

### Reservations
- `GET /api/reservations/` - List reservations
- `POST /api/reservations/` - Create reservation
- `DELETE /api/reservations/{id}/` - Cancel reservation
- `GET /api/reservations/upcoming/` - Upcoming reservations

### Orders
- `GET /api/orders/` - List orders
- `POST /api/orders/` - Create order
- `PATCH /api/orders/{id}/` - Update order status
- `POST /api/orders/{id}/cancel/` - Cancel order
- `POST /api/orders/{id}/payment/` - Update payment status

### Inventory
- `GET /api/inventory/items/` - List inventory
- `PATCH /api/inventory/items/{id}/` - Update stock
- `GET /api/inventory/items/low_stock/` - Low stock items

### Reports
- `GET /api/reports/dashboard/` - Dashboard statistics
- `GET /api/reports/daily-sales/` - Daily sales
- `GET /api/reports/weekly-sales/` - Weekly sales
- `GET /api/reports/monthly-sales/` - Monthly sales
- `GET /api/reports/top-items/` - Top selling items

## Example API Requests

### Login
```bash
curl -X POST http://localhost:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "admin", "password": "password"}'
```

### Create Order
```bash
curl -X POST http://localhost:8000/api/orders/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "customer_name": "John Doe",
    "items": [
      {"menu_item": 1, "quantity": 2},
      {"menu_item": 3, "quantity": 1}
    ]
  }'
```

### Get Dashboard Stats
```bash
curl -X GET http://localhost:8000/api/reports/dashboard/ \
  -H "Authorization: Bearer YOUR_TOKEN"
```

## Admin Panel

Access Django admin at: http://localhost:8000/admin/

Manage:
- Users & Permissions
- Menu Items & Categories
- Tables
- Reservations
- Orders
- Inventory

## User Roles

| Role | Permissions |
|------|-------------|
| Admin | Full access to all features |
| Manager | Manage menu, orders, reservations, reports |
| Staff | Manage orders and tables |
| Customer | View menu, make reservations |

## Database Schema

Key models:
- **User**: Authentication and user profiles
- **Category**: Menu item categories
- **MenuItem**: Individual menu items with pricing
- **Table**: Restaurant tables with capacity
- **Reservation**: Customer reservations
- **Order/OrderItem**: Orders with line items
- **InventoryItem**: Stock levels and suppliers

## Running Tests

```bash
python manage.py test
```

## Deployment

For production deployment:
1. Update `DEBUG=False` in `.env`
2. Configure PostgreSQL database
3. Use Gunicorn: `gunicorn config.wsgi:application`
4. Set up reverse proxy (Nginx)

## Future Improvements

- [ ] Real-time kitchen dashboard
- [ ] WebSocket notifications
- [ ] QR code menu/ordering
- [ ] Payment gateway integration
- [ ] Email/SMS notifications
- [ ] Multi-branch support
- [ ] Audit logging
- [ ] Redis caching