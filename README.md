# Agriculture Crops Management System

A full-stack Django application for managing agriculture crops, users, and orders with JWT authentication and role-based access control.

## Technology Stack

- **Backend:** Django 5, Django REST Framework
- **Frontend:** Django templates with Bootstrap 5
- **Database:** PostgreSQL (SQLite for quick local dev)
- **Authentication:** JWT (Simple JWT)
- **Roles:** Admin, Farmer, Broker, Client

## Project Structure

```
Crops/
├── config/                 # Django project settings
├── authentication/         # Auth (login, register, JWT)
├── users/                  # User CRUD, roles
├── crops/                  # Crops CRUD
├── orders/                 # Orders, status tracking
├── dashboards/             # Role-based dashboards
├── templates/              # HTML templates
├── static/                 # CSS, JS
├── manage.py
└── requirements.txt
```

## Setup Instructions

### 1. Create Virtual Environment

```bash
cd Crops
python -m venv venv

# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

Create a `.env` file in the project root (copy from `.env.example`):

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
ALLOWED_HOSTS=localhost,127.0.0.1

# For SQLite (quick start - no PostgreSQL needed)
DB_ENGINE=sqlite

# For PostgreSQL
DB_ENGINE=postgresql
DB_NAME=crops_db
DB_USER=postgres
DB_PASSWORD=your_password
DB_HOST=localhost
DB_PORT=5432
```

### 4. Run Migrations

```bash
python manage.py makemigrations users crops orders
python manage.py migrate
```

### 5. Seed Sample Data (Optional)

```bash
python manage.py seed_data
```

This creates:
- **Admin:** admin / admin123
- **Farmers:** farmer1, farmer2 / farmer123
- **Broker:** broker1 / broker123
- **Clients:** client1, client2 / client123
- Sample crops and orders

### 6. Create Superuser (if not using seed)

```bash
python manage.py createsuperuser
```

### 7. Run Development Server

```bash
python manage.py runserver
```

Visit: http://127.0.0.1:8000/

## API Endpoints

### Authentication
- `POST /api/auth/register/` - Register
- `POST /api/auth/login/` - Login (returns JWT)
- `POST /api/auth/token/refresh/` - Refresh JWT
- `GET /api/auth/profile/` - Current user (requires JWT)
- `POST /api/auth/logout/` - Logout

### Users (Admin only)
- `GET /api/users/` - List users
- `POST /api/users/` - Create user
- `GET /api/users/{id}/` - User detail
- `PUT /api/users/{id}/` - Update user
- `DELETE /api/users/{id}/` - Delete user

### Crops
- `GET /api/crops/` - List crops
- `POST /api/crops/` - Create crop (Farmer/Admin)
- `GET /api/crops/{id}/` - Crop detail
- `PUT /api/crops/{id}/` - Update crop
- `DELETE /api/crops/{id}/` - Delete crop

### Orders
- `GET /api/orders/` - List orders
- `POST /api/orders/` - Place order
- `GET /api/orders/{id}/` - Order detail
- `PATCH /api/orders/{id}/update_status/` - Update status
- `GET /api/orders/{id}/history/` - Order status history

### Using the API with JWT

```bash
# Login
curl -X POST http://127.0.0.1:8000/api/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'

# Use the returned access token
curl http://127.0.0.1:8000/api/crops/ \
  -H "Authorization: Bearer <access_token>"
```

## User Roles & Permissions

| Role   | Dashboard | Crops  | Orders | Users |
|--------|-----------|--------|--------|-------|
| Admin  | Full stats| All CRUD| All    | CRUD  |
| Farmer | My crops  | My CRUD| My sales| -     |
| Broker | Listings  | View   | Manage | -     |
| Client | My orders | Browse | Place  | -     |

## License

MIT
